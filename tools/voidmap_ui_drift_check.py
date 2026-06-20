#!/usr/bin/env python3
"""Detect drift between VOIDMAP.yml (GOLD source of truth) and the UI mirror.

The UI keeps a hand-synced, read-only copy of the VOID registry in
``ui-app/lib/voidmap-parser.ts`` so it can render without a build-time YAML
parse. This script compares the ``id`` -> ``status`` mapping of that mirror
against ``VOIDMAP.yml`` and fails (exit code 1) if they disagree, so a stale
UI copy cannot silently show an outdated VOID reality.

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

# Matches an object entry like:  id: 'VOID-002', ... status: 'CLOSED',
_ENTRY_RE = re.compile(
    r"id:\s*'(?P<id>[^']+)'.*?status:\s*'(?P<status>[^']+)'",
    re.DOTALL,
)


def load_yaml_statuses() -> dict[str, str]:
    data = yaml.safe_load(VOIDMAP_YML.read_text(encoding="utf-8"))
    statuses: dict[str, str] = {}
    for void in data.get("voids", []) or []:
        if not isinstance(void, dict):
            continue
        vid = void.get("id")
        status = void.get("status")
        if vid and status:
            statuses[str(vid)] = str(status)
    return statuses


def load_ui_statuses() -> dict[str, str]:
    text = UI_MIRROR.read_text(encoding="utf-8")
    statuses: dict[str, str] = {}
    for match in _ENTRY_RE.finditer(text):
        statuses[match.group("id")] = match.group("status")
    return statuses


def main() -> int:
    if not VOIDMAP_YML.exists():
        print(f"ERROR: {VOIDMAP_YML} not found", file=sys.stderr)
        return 2
    if not UI_MIRROR.exists():
        print(f"ERROR: {UI_MIRROR} not found", file=sys.stderr)
        return 2

    yaml_statuses = load_yaml_statuses()
    ui_statuses = load_ui_statuses()

    problems: list[str] = []

    missing_in_ui = sorted(set(yaml_statuses) - set(ui_statuses))
    for vid in missing_in_ui:
        problems.append(f"  - {vid}: present in VOIDMAP.yml but missing in UI mirror")

    extra_in_ui = sorted(set(ui_statuses) - set(yaml_statuses))
    for vid in extra_in_ui:
        problems.append(f"  - {vid}: present in UI mirror but missing in VOIDMAP.yml")

    for vid in sorted(set(yaml_statuses) & set(ui_statuses)):
        if yaml_statuses[vid] != ui_statuses[vid]:
            problems.append(
                f"  - {vid}: status drift "
                f"(VOIDMAP.yml={yaml_statuses[vid]}, UI={ui_statuses[vid]})"
            )

    if problems:
        print("VOIDMAP <-> UI drift detected:", file=sys.stderr)
        print("\n".join(problems), file=sys.stderr)
        print(
            "\nRe-sync ui-app/lib/voidmap-parser.ts with VOIDMAP.yml.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {len(yaml_statuses)} VOIDs in sync between VOIDMAP.yml and UI mirror.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
