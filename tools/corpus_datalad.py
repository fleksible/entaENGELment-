#!/usr/bin/env python3
"""Privates Korpus als DataLad-Dataset: anlegen, importieren, extrahieren, inventarisieren.

[MODEL] Das Dataset liegt außerhalb jedes Git-Arbeitsbaums, also nie im öffentlichen Repo.
Alle Dateiinhalte liegen im git-annex (inhaltsadressiert per SHA-256); Code, README und
Inventar liegen in git. Extraktion und Inventar laufen per ``datalad run`` mit den ins
Dataset kopierten Skripten (``code/``), damit ``datalad rerun`` sie ohne dieses Repo
wiederholen kann.

[RISK] Das Dataset enthält private Bedeutung (PRIVACY_BOUNDARY.md). Dieses Werkzeug legt
kein Remote an und überträgt nichts ins Netz; ein Drive- oder GitHub-Remote ist ein eigener,
bewusster Schritt (Runbook: docs/runbooks/DATALAD_KORPUS_v0_1.md).

Usage:
    python tools/corpus_datalad.py init --dataset ~/korpus
    python tools/corpus_datalad.py import --dataset ~/korpus --from ~/Downloads/export --label "Drive 2026-10-25"
    python tools/corpus_datalad.py extract --dataset ~/korpus
    python tools/corpus_datalad.py inventory --dataset ~/korpus
    python tools/corpus_datalad.py sources --dataset ~/korpus [--glob "*.md"]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

TOOL_VERSION = "0.1.0"
CODE_DIR = Path(__file__).resolve().parent / "corpus_code"
DATASET_SCRIPTS = ("extract_text.py", "inventory.py")
INBOX = "inbox"
TEXT_OUT = "derived/text"
INVENTORY_OUT = "derived/inventory"
IMPORTS_OUT = "derived/inventory/imports"
GIT_CONTROL_NAMES = frozenset({".git", ".gitattributes", ".gitignore", ".gitmodules"})
INERT_SUFFIX = "~import"
GITATTRIBUTES = """\
# corpus_datalad: Code, README und Inventar in git (diffbar); alle übrigen Inhalte im annex.
/README.md annex.largefiles=nothing
code/** annex.largefiles=nothing
derived/inventory/** annex.largefiles=nothing
derived/text/_extraction_log.json annex.largefiles=nothing
"""
DATASET_README = """\
# Privates Korpus (DataLad)

Angelegt mit `tools/corpus_datalad.py` v{version} aus dem entaENGELment-Repo.
**Privat:** nicht in ein öffentliches Repo pushen (PRIVACY_BOUNDARY.md).

| Pfad | Inhalt | Ablage |
|------|--------|--------|
| `inbox/<import>/` | Originale, unverändert | git-annex (SHA-256-Schlüssel) |
| `derived/text/` | extrahierter Text, `_extraction_log.json` | annex bzw. Log in git |
| `derived/inventory/` | `inventory.json`, `SUMMARY.md`, `public_anchor.json`, `imports/` | git |
| `code/` | Skripte für `datalad run` | git |

Wiederholen: `datalad rerun <commit>`; Herkunft eines Ergebnisses: `git log -- <pfad>`.
Nur der Wurzelhash aus `public_anchor.json` darf nach außen.
"""


class CorpusError(RuntimeError):
    """Fehler mit verständlicher Meldung für die CLI."""


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise CorpusError(f"Programm nicht gefunden: {cmd[0]}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()[-800:]
        raise CorpusError(
            f"{' '.join(cmd[:3])} … fehlgeschlagen (Exit {result.returncode}):\n{detail}"
        )
    return result.stdout


def require_tools() -> None:
    missing = [name for name in ("datalad", "git-annex") if shutil.which(name) is None]
    if missing:
        raise CorpusError(
            f"Nicht installiert: {', '.join(missing)}. Siehe docs/runbooks/DATALAD_KORPUS_v0_1.md."
        )


def inside_git_worktree(path: Path) -> Path | None:
    """Wurzel des Git-Arbeitsbaums, in dem ``path`` läge, sonst None."""
    probe = path.resolve()
    while not probe.exists():
        probe = probe.parent
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=probe if probe.is_dir() else probe.parent,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    return Path(top.stdout.strip()) if top.returncode == 0 else None


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60].strip("-") or "import"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dataset(path: Path) -> Path:
    dataset = path.expanduser().resolve()
    if not (dataset / ".datalad").is_dir():
        raise CorpusError(f"{dataset} ist kein DataLad-Dataset (fehlt .datalad/); erst init")
    return dataset


# --- Befehle -------------------------------------------------------------------------


def cmd_init(dataset: Path) -> Path:
    target = dataset.expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        raise CorpusError(f"{target} existiert und ist nicht leer")
    worktree = inside_git_worktree(target)
    if worktree is not None:
        raise CorpusError(
            f"{target} läge im Git-Arbeitsbaum {worktree}. Das Korpus gehört außerhalb jedes "
            "Repos, insbesondere des öffentlichen (PRIVACY_BOUNDARY.md)."
        )
    require_tools()
    _run(["datalad", "create", str(target)])
    for sub in (INBOX, TEXT_OUT, IMPORTS_OUT, "code"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    for name in DATASET_SCRIPTS:
        shutil.copyfile(CODE_DIR / name, target / "code" / name)
    with (target / ".gitattributes").open("a", encoding="utf-8") as handle:
        handle.write("\n" + GITATTRIBUTES)
    (target / "README.md").write_text(DATASET_README.format(version=TOOL_VERSION), encoding="utf-8")
    _run(
        ["datalad", "save", "-m", f"init: Korpus-Dataset (corpus_datalad v{TOOL_VERSION})"],
        cwd=target,
    )
    return target


def _inert_path(rel: str) -> str:
    """Git-Steuerdateien aus dem Export würden im Dataset wirken (z. B. annex.largefiles
    überschreiben); sie werden mit Suffix als gewöhnliche Daten abgelegt."""
    return "/".join(p + INERT_SUFFIX if p in GIT_CONTROL_NAMES else p for p in rel.split("/"))


def cmd_import(dataset: Path, source: Path, label: str) -> dict[str, Any]:
    ds = _dataset(dataset)
    src = source.expanduser().resolve()
    if not src.is_dir():
        raise CorpusError(f"Quelle {src} ist kein Verzeichnis")
    if src == ds or ds in src.parents or src in ds.parents:
        raise CorpusError("Quelle und Dataset dürfen sich nicht enthalten")
    slug = _slugify(label)
    target = ds / INBOX / slug
    record_path = ds / IMPORTS_OUT / f"{slug}.json"
    if target.exists() or record_path.exists():
        raise CorpusError(f"Import '{slug}' existiert bereits; anderen --label wählen")

    files: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    stored: set[str] = set()
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src).as_posix()
        if path.is_symlink():
            skipped.append({"path": rel, "reason": "Symlink nicht übernommen"})
        elif path.is_file():
            entry: dict[str, Any] = {
                "path": rel,
                "size": path.stat().st_size,
                "sha256": _sha256(path),
            }
            inert = _inert_path(rel)
            if inert != rel:
                entry["stored_as"] = inert
            if inert in stored:
                raise CorpusError(f"Ablagepfad doppelt: {inert} (Import abgebrochen)")
            stored.add(inert)
            files.append(entry)
    if not files:
        raise CorpusError(f"Keine Dateien in {src}")

    for entry in files:
        destination = target / entry.get("stored_as", entry["path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / entry["path"], destination)
        if _sha256(destination) != entry["sha256"]:
            raise CorpusError(
                f"Kopie weicht ab: {entry['path']} (Import abgebrochen, nicht gespeichert)"
            )

    record = {
        "schema": "corpus-import/0.1",
        "tool_version": TOOL_VERSION,
        "label": label,
        "slug": slug,
        "source_dir": str(src),
        "file_count": len(files),
        "bytes": sum(f["size"] for f in files),
        "files": files,
        "skipped": skipped,
    }
    # In einem Klon fehlt der (leere, von git nicht getragene) Ordner aus init.
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    _run(
        [
            "datalad",
            "save",
            "-m",
            f"import: {label} ({len(files)} Dateien)",
            str(target.relative_to(ds)),
            str(record_path.relative_to(ds)),
        ],
        cwd=ds,
    )
    return record


def _datalad_run(
    ds: Path, message: str, inputs: list[str], outputs: list[str], command: str
) -> None:
    # Fehlende lokale Inhalte werden von den Skripten als missing protokolliert.
    # DataLad soll sie vorher weder nachladen noch den Lauf daran abbrechen.
    cmd = ["datalad", "run", "--assume-ready", "inputs", "-m", message]
    for item in inputs:
        cmd += ["--input", item]
    for item in outputs:
        cmd += ["--output", item]
    _run([*cmd, command], cwd=ds)


def cmd_extract(dataset: Path) -> dict[str, Any]:
    ds = _dataset(dataset)
    _datalad_run(
        ds,
        "extract: Text aus inbox/ (code/extract_text.py)",
        [INBOX],
        [TEXT_OUT],
        f"python3 code/extract_text.py {INBOX} {TEXT_OUT}",
    )
    log: dict[str, Any] = json.loads(
        (ds / TEXT_OUT / "_extraction_log.json").read_text(encoding="utf-8")
    )
    return log


def cmd_inventory(dataset: Path) -> dict[str, Any]:
    ds = _dataset(dataset)
    outputs = [
        f"{INVENTORY_OUT}/{n}" for n in ("inventory.json", "public_anchor.json", "SUMMARY.md")
    ]
    _datalad_run(
        ds,
        "inventory: Hashes, Duplikate, Archivmitglieder (code/inventory.py)",
        [INBOX],
        outputs,
        f"python3 code/inventory.py {INBOX} {INVENTORY_OUT}",
    )
    inventory: dict[str, Any] = json.loads(
        (ds / INVENTORY_OUT / "inventory.json").read_text(encoding="utf-8")
    )
    return inventory


def sources_for_reentry(
    dataset: Path, pattern: str = "*", role: str = "input"
) -> list[dict[str, str]]:
    """Quellen-Einträge für ein reentry_crate-Manifest; sha256 bindet die Bytes (Abgleich beim save)."""
    ds = _dataset(dataset)
    inventory_path = ds / INVENTORY_OUT / "inventory.json"
    if not inventory_path.is_file():
        raise CorpusError("Noch kein Inventar; erst 'inventory' ausführen")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    entries: list[dict[str, str]] = []
    used: set[str] = set()
    for item in inventory["files"]:
        if not fnmatch(item["path"], pattern):
            continue
        base_id = f"{_slugify(Path(item['path']).stem)[:40]}-{item['sha256'][:8]}"
        source_id, number = base_id, 2
        while source_id in used:  # gleicher Name und Inhalt an mehreren Orten
            source_id, number = f"{base_id}-{number}", number + 1
        used.add(source_id)
        entries.append(
            {
                "id": source_id,
                "path": str(ds / INBOX / item["path"]),
                "role": role,
                "sha256": item["sha256"],
            }
        )
    return entries


# --- CLI -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Privates Korpus als DataLad-Dataset")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, text in (
        ("init", "Dataset außerhalb jedes Git-Repos anlegen"),
        ("extract", "Textextraktion per datalad run"),
        ("inventory", "Hash-/Duplikatinventar per datalad run"),
    ):
        sub.add_parser(name, help=text).add_argument("--dataset", required=True, type=Path)
    p_import = sub.add_parser("import", help="Ordner nach inbox/<label>/ übernehmen")
    p_import.add_argument("--dataset", required=True, type=Path)
    p_import.add_argument("--from", dest="source", required=True, type=Path)
    p_import.add_argument("--label", required=True)
    p_sources = sub.add_parser("sources", help="Quellen-Einträge für reentry_crate ausgeben")
    p_sources.add_argument("--dataset", required=True, type=Path)
    p_sources.add_argument("--glob", default="*")
    p_sources.add_argument("--role", default="input", choices=("input", "context", "output"))
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            print(f"[INIT] {cmd_init(args.dataset)}")
        elif args.command == "import":
            record = cmd_import(args.dataset, args.source, args.label)
            print(f"[IMPORT] {record['file_count']} Dateien → inbox/{record['slug']}/")
            if record["skipped"]:
                print(f"[IMPORT] {len(record['skipped'])} übersprungen (siehe Import-Record)")
        elif args.command == "extract":
            log = cmd_extract(args.dataset)
            print(f"[EXTRACT] {json.dumps(log['counts'], ensure_ascii=False)}")
        elif args.command == "inventory":
            summary = cmd_inventory(args.dataset)["summary"]
            print(f"[INVENTORY] {json.dumps(summary, ensure_ascii=False)}")
        else:
            entries = sources_for_reentry(args.dataset, args.glob, args.role)
            print(json.dumps({"sources": entries}, indent=2, ensure_ascii=False))
    except CorpusError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
