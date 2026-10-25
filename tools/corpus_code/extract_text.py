#!/usr/bin/env python3
"""Textextraktion für das Korpus-Dataset (läuft per ``datalad run`` im Dataset).

[MODEL] Liest jede Datei unter ``<inbox>`` und schreibt ihren Text nach
``<out>/<relativer Pfad>.txt``. Nur Standardbibliothek; PDF über das externe Programm
``pdftotext`` (poppler), falls vorhanden. Deterministisch: sortierte Reihenfolge und keine
Zeitstempel im Log, damit ``datalad rerun`` bytegleiche Ergebnisse liefern kann.

[RISK] Extrahierter Text ist eine Lesehilfe, kein Original: Layout, Bilder, Fußnoten und
Formeln können fehlen. Maßgeblich bleibt die Originaldatei unter ``inbox/``.

Usage (im Dataset):
    python3 code/extract_text.py inbox derived/text
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path
from typing import Any

# Nur Standardbibliothek (läuft im Dataset ohne Projektabhängigkeiten). Gegen XML-Angriffe:
# DTDs (und damit Entity-Deklarationen) lehnt ein expat-Vorlauf in jeder Kodierung ab
# (OOXML enthält keine), Größe begrenzt.
from xml.etree import ElementTree  # nosec B405
from xml.parsers import expat

SCRIPT_VERSION = "0.1.0"
LOG_NAME = "_extraction_log.json"
TEXT_SUFFIXES = frozenset(
    {".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv", ".py", ".tex", ".html"}
)
DOCX_SUFFIXES = frozenset({".docx"})
PDF_SUFFIXES = frozenset({".pdf"})
MAX_DOCX_XML_BYTES = 64 * 1024 * 1024  # Schutz vor Zip-Bomben in DOCX-Containern
PDF_TIMEOUT_S = 300
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# Fehler einer einzelnen Datei; sie landen im Log, der Lauf geht weiter.
EXTRACT_ERRORS = (
    OSError,
    ValueError,
    KeyError,
    RuntimeError,  # verschlüsseltes Zip-Mitglied
    NotImplementedError,  # nicht unterstützte Kompression (z. B. Deflate64)
    zlib.error,
    zipfile.BadZipFile,
    expat.ExpatError,
    ElementTree.ParseError,
    subprocess.TimeoutExpired,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_inputs(inbox: Path) -> list[Path]:
    """Alle Einträge unter inbox, auch annex-Symlinks ohne lokalen Inhalt; ohne Dotfiles."""
    return sorted(
        p
        for p in inbox.rglob("*")
        if (p.is_file() or p.is_symlink())
        and not any(part.startswith(".") for part in p.relative_to(inbox).parts)
    )


def decode_text(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8", errors="replace")


def reject_dtd(data: bytes) -> None:
    """Bricht bei einer DTD ab; expat erkennt sie unabhängig von der Kodierung (z. B. UTF-16)."""

    def refuse(*_args: object) -> None:
        raise ValueError("word/document.xml enthält eine DTD (abgelehnt)")

    parser = expat.ParserCreate()
    parser.StartDoctypeDeclHandler = refuse
    parser.EntityDeclHandler = refuse
    parser.Parse(data, True)


def extract_docx(path: Path) -> str:
    """Absätze aus word/document.xml; Tabs und Zeilenumbrüche bleiben als Whitespace erhalten."""
    with zipfile.ZipFile(path) as archive:
        info = archive.getinfo("word/document.xml")
        if info.file_size > MAX_DOCX_XML_BYTES:
            raise ValueError(f"word/document.xml zu groß ({info.file_size} Byte)")
        data = archive.read(info)
    reject_dtd(data)
    # Ohne DTD gibt es keine Entity-Expansion; die Größe ist oben begrenzt.
    root = ElementTree.fromstring(data)  # nosec B314
    paragraphs: list[str] = []
    for paragraph in root.iter(f"{W_NS}p"):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{W_NS}t" and node.text:
                parts.append(node.text)
            elif node.tag == f"{W_NS}tab":
                parts.append("\t")
            elif node.tag in (f"{W_NS}br", f"{W_NS}cr"):
                parts.append("\n")
        paragraphs.append("".join(parts))
    return "\n".join(paragraphs).rstrip() + "\n"


def pdftotext_version() -> str:
    if shutil.which("pdftotext") is None:
        return "missing"
    probe = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True, check=False)
    lines = (probe.stderr or probe.stdout).strip().splitlines()
    return lines[0] if lines else "unknown"


def extract_pdf(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        timeout=PDF_TIMEOUT_S,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"pdftotext Exit {result.returncode}: {decode_text(result.stderr)[:200]}")
    return decode_text(result.stdout)


def extract_one(path: Path, has_pdftotext: bool) -> tuple[str, str | None, str]:
    """Gibt (Methode, Text oder None, Detail) zurück."""
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return "text", decode_text(path.read_bytes()), ""
    if suffix in DOCX_SUFFIXES:
        return "docx", extract_docx(path), ""
    if suffix in PDF_SUFFIXES:
        if not has_pdftotext:
            return "pdftotext", None, "pdftotext nicht installiert"
        return "pdftotext", extract_pdf(path), ""
    return "none", None, f"kein Extraktor für {suffix or 'Dateien ohne Endung'}"


def run(inbox: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    has_pdftotext = shutil.which("pdftotext") is not None
    entries: list[dict[str, Any]] = []
    produced: set[str] = set()
    for path in iter_inputs(inbox):
        rel = path.relative_to(inbox).as_posix()
        entry: dict[str, Any] = {"path": rel}
        if not path.exists():
            entry.update(status="missing", detail="Inhalt nicht lokal (git annex get)")
            entries.append(entry)
            continue
        entry["sha256"] = sha256_file(path)
        try:
            method, text, detail = extract_one(path, has_pdftotext)
        except EXTRACT_ERRORS as exc:
            entry.update(status="error", detail=f"{type(exc).__name__}: {exc}"[:300])
            entries.append(entry)
            continue
        entry["method"] = method
        if text is None:
            entry.update(status="skipped", detail=detail)
        else:
            target = out / f"{rel}.txt"
            data = text.encode("utf-8")
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            except OSError as exc:
                # z. B. Quelle "a.md" neben Verzeichnis "a.md.txt/": Ausgabepfade kollidieren.
                entry.update(status="error", detail=f"Ausgabe {rel}.txt: {type(exc).__name__}")
                entries.append(entry)
                continue
            produced.add(target.relative_to(out).as_posix())
            entry.update(
                status="ok", output=f"{rel}.txt", output_sha256=sha256_bytes(data), chars=len(text)
            )
        entries.append(entry)

    stale = sorted(
        p.relative_to(out).as_posix()
        for p in out.rglob("*.txt")
        if p.relative_to(out).as_posix() not in produced
    )
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    log = {
        "schema": "corpus-extraction-log/0.1",
        "script_version": SCRIPT_VERSION,
        "pdftotext": pdftotext_version(),
        "counts": dict(sorted(counts.items())),
        "stale_outputs": stale,
        "entries": entries,
    }
    (out / LOG_NAME).write_text(
        json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return log


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("Usage: extract_text.py <inbox> <out>", file=sys.stderr)
        return 2
    log = run(Path(args[0]), Path(args[1]))
    print(f"[EXTRACT] {json.dumps(log['counts'], ensure_ascii=False)}")
    if log["stale_outputs"]:
        print(f"[EXTRACT] {len(log['stale_outputs'])} veraltete Ausgaben (siehe {LOG_NAME})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
