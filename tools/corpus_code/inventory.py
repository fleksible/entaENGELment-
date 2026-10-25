#!/usr/bin/env python3
"""Hash- und Duplikatinventar für das Korpus-Dataset (läuft per ``datalad run`` im Dataset).

[MODEL] Erfasst je Datei unter ``<inbox>`` Größe und SHA-256, gruppiert inhaltsgleiche
Dateien, liest Zip-Archive nur als Liste (Mitglieder werden gehasht, nie entpackt) und
schreibt einen öffentlichen Anker ohne Dateinamen (``public_anchor.json``) nach
PRIVACY_BOUNDARY.md, Abschnitt „Public-anchor only“.

[RISK] Der Anker ist nicht rekonstruierend, aber eine Bestätigung: Wer eine Datei besitzt,
kann prüfen, ob ihr Hash im Korpus vorkommt, sofern er die Einzelhashes kennt. Nach
außen geht deshalb nur der Wurzelhash, nie die Liste.

Usage (im Dataset):
    python3 code/inventory.py inbox derived/inventory
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "0.1.0"
MAX_MEMBER_BYTES = 512 * 1024 * 1024  # Zip-Mitglieder darüber werden nicht gehasht
MAX_ARCHIVE_TOTAL_BYTES = 8 * 1024 * 1024 * 1024  # Schutz vor Zip-Bomben je Archiv


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_inputs(inbox: Path) -> list[Path]:
    return sorted(
        p
        for p in inbox.rglob("*")
        if (p.is_file() or p.is_symlink())
        and not any(part.startswith(".") for part in p.relative_to(inbox).parts)
    )


def zip_members(path: Path) -> list[dict[str, Any]]:
    """Mitglieder eines Zip-Archivs mit Größe und SHA-256, ohne etwas auf die Platte zu schreiben."""
    members: list[dict[str, Any]] = []
    total = 0
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda i: i.filename):
            if info.is_dir():
                continue
            entry: dict[str, Any] = {"member": info.filename, "size": info.file_size}
            total += info.file_size
            if info.file_size > MAX_MEMBER_BYTES or total > MAX_ARCHIVE_TOTAL_BYTES:
                entry["status"] = "skipped: zu groß"
            else:
                digest = hashlib.sha256()
                with archive.open(info) as handle:
                    for chunk in iter(lambda: handle.read(1 << 16), b""):
                        digest.update(chunk)
                entry["sha256"] = digest.hexdigest()
            members.append(entry)
    return members


def duplicate_groups(items: list[tuple[str, str, int]]) -> list[dict[str, Any]]:
    """items: (sha256, ort, größe) → Gruppen mit mehr als einem Ort, größte Ersparnis zuerst."""
    by_hash: dict[str, list[tuple[str, int]]] = {}
    for sha, where, size in items:
        by_hash.setdefault(sha, []).append((where, size))
    groups = [
        {
            "sha256": sha,
            "size": places[0][1],
            "count": len(places),
            "redundant_bytes": places[0][1] * (len(places) - 1),
            "locations": sorted(where for where, _ in places),
        }
        for sha, places in by_hash.items()
        if len(places) > 1
    ]
    return sorted(groups, key=lambda g: (-g["redundant_bytes"], g["sha256"]))


def public_anchor(file_hashes: list[str]) -> dict[str, Any]:
    root = hashlib.sha256("\n".join(sorted(file_hashes)).encode("ascii")).hexdigest()
    return {
        "schemaVersion": "corpus-public-anchor/0.1",
        "visibility": "public-anchor",
        "entryCount": len(file_hashes),
        "distinctContentCount": len(set(file_hashes)),
        "snapshotRootHash": root,
        "rootHashRule": "sha256 über die sortierten, zeilengetrennten SHA-256 aller Dateien",
    }


def run(inbox: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    files: list[dict[str, Any]] = []
    archives: list[dict[str, Any]] = []
    missing: list[str] = []
    for path in iter_inputs(inbox):
        rel = path.relative_to(inbox).as_posix()
        if not path.exists():
            missing.append(rel)
            continue
        entry = {"path": rel, "size": path.stat().st_size, "sha256": sha256_file(path)}
        files.append(entry)
        if path.suffix.lower() == ".zip":
            try:
                archives.append({"path": rel, "members": zip_members(path)})
            except (OSError, zipfile.BadZipFile, ValueError) as exc:
                archives.append({"path": rel, "error": f"{type(exc).__name__}: {exc}"[:300]})

    file_items = [(f["sha256"], f["path"], f["size"]) for f in files]
    member_items = [
        (m["sha256"], f"{a['path']}!{m['member']}", m["size"])
        for a in archives
        for m in a.get("members", [])
        if "sha256" in m
    ]
    file_dupes = duplicate_groups(file_items)
    member_dupes = duplicate_groups(file_items + member_items)
    inventory = {
        "schema": "corpus-inventory/0.1",
        "script_version": SCRIPT_VERSION,
        "summary": {
            "files": len(files),
            "bytes": sum(f["size"] for f in files),
            "distinct_contents": len({f["sha256"] for f in files}),
            "duplicate_groups": len(file_dupes),
            "redundant_bytes": sum(g["redundant_bytes"] for g in file_dupes),
            "archives": len(archives),
            "archive_members": sum(len(a.get("members", [])) for a in archives),
            "cross_archive_duplicate_groups": len(member_dupes),
            "missing_content": len(missing),
        },
        "files": files,
        "missing_content": missing,
        "duplicates": file_dupes,
        "archives": archives,
        "duplicates_including_archive_members": member_dupes,
    }
    anchor = public_anchor([f["sha256"] for f in files])
    (out / "inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "public_anchor.json").write_text(
        json.dumps(anchor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "SUMMARY.md").write_text(render_summary(inventory, anchor), encoding="utf-8")
    return inventory


def render_summary(inventory: dict[str, Any], anchor: dict[str, Any]) -> str:
    s = inventory["summary"]
    lines = [
        "# Korpus-Inventar",
        "",
        f"- Dateien: {s['files']} ({s['bytes']} Byte), verschiedene Inhalte: {s['distinct_contents']}",
        f"- Duplikatgruppen: {s['duplicate_groups']}, redundante Byte: {s['redundant_bytes']}",
        f"- Archive: {s['archives']} mit {s['archive_members']} Mitgliedern; "
        f"Gruppen inkl. Archivmitglieder: {s['cross_archive_duplicate_groups']}",
        f"- Ohne lokalen Inhalt: {s['missing_content']}",
        f"- Öffentlicher Anker: `{anchor['snapshotRootHash']}` ({anchor['entryCount']} Einträge)",
        "",
        "## Größte Duplikatgruppen (Dateien)",
        "",
        "| Anzahl | Größe | Orte |",
        "|---:|---:|---|",
    ]
    for group in inventory["duplicates"][:20]:
        places = "<br>".join(f"`{p}`" for p in group["locations"])
        lines.append(f"| {group['count']} | {group['size']} | {places} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("Usage: inventory.py <inbox> <out>", file=sys.stderr)
        return 2
    inventory = run(Path(args[0]), Path(args[1]))
    print(f"[INVENTORY] {json.dumps(inventory['summary'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
