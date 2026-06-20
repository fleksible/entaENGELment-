#!/usr/bin/env python3
"""Detect drift between VOIDMAP.yml (GOLD source of truth) and the UI mirror.

The UI keeps a hand-synced, read-only copy of the VOID registry in
``ui-app/lib/voidmap-parser.ts`` so it can render without a build-time YAML
parse. This script compares the verbatim-mirrored fields of that copy against
``VOIDMAP.yml`` and fails (exit code 1) if they disagree, so a stale UI copy
cannot silently show an outdated VOID reality.

Checked fields (must match byte-for-byte): ``status``, ``priority``, ``title``.
These are short, prominently rendered, and intended to be exact mirrors.

NOT checked: the free-form ``notes`` field is intentionally **abridged** in the
UI mirror (a human-readable summary of the multi-line YAML note), so it is not
byte-compared here. Everything the checker does compare it requires to be exact.

It is intentionally dependency-light: YAML is parsed with PyYAML (already used
elsewhere in the repo) and the TypeScript mirror is scanned with a small regex
rather than a JS parser.

Usage:
    python tools/voidmap_ui_drift_check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
VOIDMAP_YML = REPO_ROOT / "VOIDMAP.yml"
UI_MIRROR = REPO_ROOT / "ui-app" / "lib" / "voidmap-parser.ts"

# Fields compared byte-for-byte between VOIDMAP.yml and the UI mirror.
CHECKED_FIELDS = ("status", "priority", "title")

# Matches a UI mirror object entry. The mirror keeps the fields in the order
# id, title, status, priority on consecutive lines, e.g.:
#   id: 'VOID-002',
#   title: 'CI Pipeline Integration',
#   status: 'CLOSED',
#   priority: 'high',
_ENTRY_RE = re.compile(
    r"id:\s*'(?P<id>[^']+)',\s*"
    r"title:\s*'(?P<title>[^']*)',\s*"
    r"status:\s*'(?P<status>[^']+)',\s*"
    r"priority:\s*'(?P<priority>[^']+)'",
    re.DOTALL,
)


def load_yaml_voids() -> dict[str, dict[str, str]]:
    data = yaml.safe_load(VOIDMAP_YML.read_text(encoding="utf-8"))
    voids: dict[str, dict[str, str]] = {}
    for void in data.get("voids", []) or []:
        if not isinstance(void, dict):
            continue
        vid = void.get("id")
        if not vid:
            continue
        voids[str(vid)] = {f: str(void.get(f, "")) for f in CHECKED_FIELDS}
    return voids


def load_ui_voids() -> dict[str, dict[str, str]]:
    text = UI_MIRROR.read_text(encoding="utf-8")
    voids: dict[str, dict[str, str]] = {}
    for match in _ENTRY_RE.finditer(text):
        voids[match.group("id")] = {f: match.group(f) for f in CHECKED_FIELDS}
    return voids


def main() -> int:
    if not VOIDMAP_YML.exists():
        print(f"ERROR: {VOIDMAP_YML} not found", file=sys.stderr)
        return 2
    if not UI_MIRROR.exists():
        print(f"ERROR: {UI_MIRROR} not found", file=sys.stderr)
        return 2

    yaml_voids = load_yaml_voids()
    ui_voids = load_ui_voids()

    problems: list[str] = []

    for vid in sorted(set(yaml_voids) - set(ui_voids)):
        problems.append(f"  - {vid}: present in VOIDMAP.yml but missing in UI mirror")

    for vid in sorted(set(ui_voids) - set(yaml_voids)):
        problems.append(f"  - {vid}: present in UI mirror but missing in VOIDMAP.yml")

    for vid in sorted(set(yaml_voids) & set(ui_voids)):
        for field in CHECKED_FIELDS:
            expected = yaml_voids[vid][field]
            actual = ui_voids[vid][field]
            if expected != actual:
                problems.append(
                    f"  - {vid}: {field} drift " f"(VOIDMAP.yml={expected!r}, UI={actual!r})"
                )

    if problems:
        print("VOIDMAP <-> UI drift detected:", file=sys.stderr)
        print("\n".join(problems), file=sys.stderr)
        print(
            "\nRe-sync ui-app/lib/voidmap-parser.ts with VOIDMAP.yml.",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {len(yaml_voids)} VOIDs in sync between VOIDMAP.yml and UI mirror "
        f"(fields checked: {', '.join(CHECKED_FIELDS)})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
