#!/usr/bin/env python3
"""EntaENGELment Intake Helper — Calm Intake Layer (PR #255).

Copies a session-generated artefact into the semipermeable intake layer
(``docs/intake/raw/<date>/``), appends a row to ``docs/intake/INDEX.md`` and
optionally writes a metadata record under ``docs/intake/records/``.

House rules honoured (see docs/intake/README.md):
  - Capture is allowed; canonisation is forbidden.
  - Source files are copied, never deleted (G3).
  - Writes stay strictly inside docs/intake/. The tool refuses to touch
    canon / spec / VOIDMAP / glossary / roadmap or anything outside intake.

Usage:
    python tools/intake_add.py --file PATH --title "Title" --source "Claude"
                               [--no-record] [--root .]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import shutil
from pathlib import Path

INTAKE_REL = Path("docs/intake")
RAW_REL = INTAKE_REL / "raw"
RECORDS_REL = INTAKE_REL / "records"

# Paths the helper must never write into (defence in depth).
FORBIDDEN_PREFIXES = (
    "index",
    "spec",
    "policies",
    "seeds",
    "docs/spec",
    "docs/specs",
    "docs/glossary",
    "docs/roadmap",
    "docs/canon",
)
FORBIDDEN_FILES = ("VOIDMAP.yml", "VOIDMAP.yaml")

PLACEHOLDER_MARKER = "noch keine Eintr"  # matches the empty-table row


def _slugify(title: str) -> str:
    """Turn a title into a filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower())
    slug = slug.strip("-")
    return slug or "untitled"


def _today() -> str:
    return _dt.date.today().isoformat()


def _next_sequence(records_dir: Path, date_str: str) -> int:
    """Return the next per-day sequence number based on existing records."""
    highest = 0
    pattern = re.compile(rf"INTAKE-{re.escape(date_str)}-(\d+)")
    if records_dir.exists():
        for child in records_dir.iterdir():
            found = pattern.search(child.name)
            if found:
                highest = max(highest, int(found.group(1)))
    return highest + 1


def _assert_inside_intake(target: Path, intake_root: Path) -> None:
    """Refuse to proceed if a write target escapes docs/intake/."""
    resolved = target.resolve()
    intake_resolved = intake_root.resolve()
    if intake_resolved not in resolved.parents and resolved != intake_resolved:
        raise SystemExit(f"[intake] refusing to write outside docs/intake/: {target}")


def _assert_not_forbidden(rel_target: Path) -> None:
    """Belt-and-suspenders guard against canon/spec/VOIDMAP writes."""
    posix = rel_target.as_posix()
    for prefix in FORBIDDEN_PREFIXES:
        if posix.startswith(prefix + "/") or posix == prefix:
            raise SystemExit(f"[intake] forbidden destination: {posix}")
    for forbidden in FORBIDDEN_FILES:
        if posix.endswith(forbidden):
            raise SystemExit(f"[intake] forbidden destination: {posix}")


def _append_index_row(index_path: Path, row: str) -> None:
    """Append a table row, dropping the empty-table placeholder if present."""
    lines = index_path.read_text(encoding="utf-8").splitlines()
    kept = [ln for ln in lines if PLACEHOLDER_MARKER not in ln]
    while kept and kept[-1].strip() == "":
        kept.pop()
    kept.append(row)
    kept.append("")
    index_path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def _write_record(records_dir: Path, intake_id: str, title: str, source: str,
                  date_str: str, raw_rel: str) -> Path:
    """Write a minimal intake record stub."""
    record_path = records_dir / f"{intake_id}.md"
    body = (
        f"# {intake_id} — {title}\n\n"
        "## Herkunft\n\n"
        f"- Datum: {date_str}\n"
        f"- Quelle / Gegenüber: {source}\n"
        "- Kontext: \n"
        f"- Abgelegte Kopie: {raw_rel}\n\n"
        "## Kurzbeschreibung\n\n_(1–5 Sätze.)_\n\n"
        "## Entscheidung\n\n"
        "- Status: raw\n"
        "- Nächste Prüfung: \n"
        "- Verantwortliche Entscheidung: \n\n"
        "## Grenzen\n\n"
        "Intake-Record. Kein Kanon, kein Beweis, keine abgeschlossene Bewertung. "
        "Externe Inhalte sind untrusted (G5).\n"
    )
    record_path.write_text(body, encoding="utf-8")
    return record_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a file to the calm intake layer")
    parser.add_argument("--file", required=True, help="Path to the source document")
    parser.add_argument("--title", required=True, help="Human-readable title")
    parser.add_argument("--source", required=True, help="Origin, e.g. Claude / local")
    parser.add_argument("--no-record", action="store_true", help="Skip record stub")
    parser.add_argument("--root", default=".", help="Repository root (default: .)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    intake_root = root / INTAKE_REL
    raw_root = root / RAW_REL
    records_dir = root / RECORDS_REL
    index_path = root / INTAKE_REL / "INDEX.md"

    source_file = Path(args.file)
    if not source_file.is_file():
        raise SystemExit(f"[intake] source file not found: {source_file}")
    if not index_path.is_file():
        raise SystemExit(f"[intake] missing {index_path}; is docs/intake/ set up?")

    date_str = _today()
    seq = _next_sequence(records_dir, date_str)
    intake_id = f"INTAKE-{date_str}-{seq:03d}"
    slug = _slugify(args.title)

    dest_dir = raw_root / date_str
    dest_name = f"{slug}{source_file.suffix}"
    dest_path = dest_dir / dest_name

    rel_dest = dest_path.relative_to(root)
    _assert_inside_intake(dest_path, intake_root)
    _assert_not_forbidden(rel_dest)

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, dest_path)  # copy, never move/delete (G3)

    raw_rel = rel_dest.as_posix()
    row = (
        f"| {intake_id} | {date_str} | {args.title} | {args.source} "
        f"| raw | (offen) | ja |"
    )
    _append_index_row(index_path, row)

    record_msg = "(no record)"
    if not args.no_record:
        rec = _write_record(records_dir, intake_id, args.title, args.source,
                            date_str, raw_rel)
        _assert_inside_intake(rec, intake_root)
        record_msg = rec.relative_to(root).as_posix()

    print(f"[intake] id={intake_id}")
    print(f"[intake] copied -> {raw_rel}")
    print(f"[intake] index  -> {index_path.relative_to(root).as_posix()}")
    print(f"[intake] record -> {record_msg}")
    print("[intake] source left untouched; no canonisation performed.")


if __name__ == "__main__":
    main()
