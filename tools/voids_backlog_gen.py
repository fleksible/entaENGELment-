#!/usr/bin/env python3
"""VOIDMAP Backlog Generator.

Reads VOIDMAP.yml and emits a deterministic Markdown backlog document.

Usage:
    python3 tools/voids_backlog_gen.py [--source VOIDMAP.yml]
                                       [--out docs/voids_backlog.md]
                                       [--check]

In --check mode, the script compares the freshly generated output against
the existing file and exits with code 1 if they differ. Otherwise the file
is written (creating parent directories as needed).

The output ordering is deterministic:
- Groups: OPEN, IN_PROGRESS, SUSPENDED, CLOSED, OTHER (if any).
- OPEN/IN_PROGRESS/SUSPENDED/OTHER: sorted by ID ascending (string sort).
- CLOSED: sorted by close date descending; within same date by ID ascending
  (stable sort).

Missing fields render as an em-dash (—). External network access is not used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "VOIDMAP.yml"
DEFAULT_OUT = REPO_ROOT / "docs" / "voids_backlog.md"

STATUS_ORDER = ["OPEN", "IN_PROGRESS", "SUSPENDED", "CLOSED"]
EMPTY = "—"


def cell(value: Any) -> str:
    """Render a value as a Markdown-safe table cell."""
    if value is None or value == "":
        return EMPTY
    if isinstance(value, list):
        if not value:
            return EMPTY
        rendered = ", ".join(str(v) for v in value)
    else:
        rendered = str(value)
    rendered = rendered.replace("\r", "")
    first_line = next((ln for ln in rendered.split("\n") if ln.strip()), "")
    first_line = first_line.strip()
    if not first_line:
        return EMPTY
    return first_line.replace("|", r"\|")


def load_voidmap(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"VOIDMAP source is not a YAML mapping: {path}")
    return data


def group_voids(voids: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {s: [] for s in STATUS_ORDER}
    other: list[dict[str, Any]] = []
    for v in voids:
        if not isinstance(v, dict):
            continue
        status = str(v.get("status") or "").upper()
        if status in groups:
            groups[status].append(v)
        else:
            other.append(v)
    if other:
        groups["OTHER"] = other
    return groups


def sort_by_id(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda v: str(v.get("id") or ""))


def sort_closed(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = sorted(items, key=lambda v: str(v.get("id") or ""))
    return sorted(by_id, key=lambda v: str(v.get("closed") or ""), reverse=True)


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_No entries._\n"
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def render_active_table(items: list[dict[str, Any]]) -> str:
    headers = ["ID", "Title", "Priority", "Owner", "Domain", "Target", "Symptom"]
    rows = [
        [
            cell(v.get("id")),
            cell(v.get("title")),
            cell(v.get("priority")),
            cell(v.get("owner")),
            cell(v.get("domain")),
            cell(v.get("target_date")),
            cell(v.get("symptom")),
        ]
        for v in items
    ]
    return render_table(headers, rows)


def render_closed_table(items: list[dict[str, Any]]) -> str:
    headers = ["ID", "Title", "Closed", "Evidence"]
    rows = [
        [
            cell(v.get("id")),
            cell(v.get("title")),
            cell(v.get("closed")),
            cell(v.get("evidence")),
        ]
        for v in items
    ]
    return render_table(headers, rows)


def render_document(data: dict[str, Any], source_rel: str) -> str:
    metadata = data.get("metadata") or {}
    last_updated = metadata.get("last_updated") or ""
    voids_raw = data.get("voids") or []
    voids = voids_raw if isinstance(voids_raw, list) else []

    groups = group_voids(voids)

    out: list[str] = []
    out.append("# VOIDMAP Backlog")
    out.append("")
    out.append(f"> Auto-generated from `{source_rel}`. Do not edit by hand.")
    out.append("> Regenerate via: `python3 tools/voids_backlog_gen.py`")
    if last_updated:
        out.append(f"> Source `last_updated`: {last_updated}")
    out.append("")

    out.append("## Summary")
    out.append("")
    out.append("| Status | Count |")
    out.append("|--------|-------|")
    for s in STATUS_ORDER:
        out.append(f"| {s} | {len(groups.get(s, []))} |")
    if "OTHER" in groups:
        out.append(f"| OTHER | {len(groups['OTHER'])} |")
    out.append(f"| **Total** | **{len(voids)}** |")
    out.append("")

    out.append("## OPEN")
    out.append("")
    out.append(render_active_table(sort_by_id(groups.get("OPEN", []))).rstrip("\n"))
    out.append("")

    out.append("## IN_PROGRESS")
    out.append("")
    out.append(render_active_table(sort_by_id(groups.get("IN_PROGRESS", []))).rstrip("\n"))
    out.append("")

    out.append("## SUSPENDED")
    out.append("")
    out.append(render_active_table(sort_by_id(groups.get("SUSPENDED", []))).rstrip("\n"))
    out.append("")

    out.append("## CLOSED (chronological, newest first)")
    out.append("")
    out.append(render_closed_table(sort_closed(groups.get("CLOSED", []))).rstrip("\n"))
    out.append("")

    if "OTHER" in groups:
        out.append("## OTHER (unrecognized status)")
        out.append("")
        out.append(render_active_table(sort_by_id(groups["OTHER"])).rstrip("\n"))
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate docs/voids_backlog.md from VOIDMAP.yml (deterministic).",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Source VOIDMAP file (default: {DEFAULT_SOURCE.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output Markdown file (default: {DEFAULT_OUT.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare current output against existing file; exit 1 on drift.",
    )
    args = parser.parse_args(argv)

    source: Path = args.source
    out_path: Path = args.out

    if not source.exists():
        print(f"[ERROR] Source not found: {source}", file=sys.stderr)
        return 2

    data = load_voidmap(source)
    try:
        source_rel = str(source.resolve().relative_to(REPO_ROOT))
    except ValueError:
        source_rel = str(source)
    rendered = render_document(data, source_rel)

    if args.check:
        if not out_path.exists():
            print(f"[CHECK] Output missing: {out_path}", file=sys.stderr)
            return 1
        existing = out_path.read_text(encoding="utf-8")
        if existing != rendered:
            print(f"[CHECK] Drift detected: {out_path}", file=sys.stderr)
            return 1
        print(f"[CHECK] Up to date: {out_path}")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"[OK] Wrote {out_path} ({len(rendered)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
