#!/usr/bin/env python3
"""Workflow posture drift check.

Scans `.github/workflows/*.yml` and `.github/workflows/*.yaml` and verifies
that each workflow keeps the CI/CD membrane contract:

- a top-level ``permissions`` block is declared;
- a top-level ``concurrency`` block is declared;
- ``concurrency.cancel-in-progress`` is ``true``;
- any permission broader than ``contents: read`` is documented as an
  exception in ``docs/ci/WORKFLOW_MAP.md`` (the workflow filename must be
  mentioned there).

The check is read-only, deterministic, and needs no network access. It
prints a PASS/FAIL summary and exits non-zero on drift.

Usage:
    python3 tools/workflow_posture_check.py [--root .]
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
WORKFLOW_GLOBS = ("*.yml", "*.yaml")
WORKFLOW_MAP_REL = "docs/ci/WORKFLOW_MAP.md"


def find_workflows(root: Path) -> list[Path]:
    """Return workflow files under ``.github/workflows`` sorted by name."""
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return []
    files: set[Path] = set()
    for pattern in WORKFLOW_GLOBS:
        files.update(wf_dir.glob(pattern))
    return sorted(files, key=lambda p: p.name)


def is_minimal_permissions(permissions: Any) -> bool:
    """True if permissions are no broader than ``contents: read``.

    A mapping is minimal when every entry is ``contents`` set to ``read`` (or
    ``none``). Any extra scope, any ``write`` value, or a broad string form
    such as ``write-all`` counts as broader and must be documented.
    """
    if isinstance(permissions, dict):
        for scope, level in permissions.items():
            if str(scope).strip().lower() != "contents":
                return False
            if str(level).strip().lower() not in ("read", "none"):
                return False
        return True
    # String forms ("read-all", "write-all") or anything else are not minimal.
    return False


def check_workflow(path: Path, workflow_map_text: str) -> list[str]:
    """Return a list of posture problems for a single workflow file."""
    problems: list[str] = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        return [f"YAML parse error: {exc}"]

    if not isinstance(doc, dict):
        return ["top-level YAML is not a mapping"]

    # permissions
    if "permissions" not in doc:
        problems.append("missing top-level 'permissions'")
    elif not is_minimal_permissions(doc["permissions"]):
        if path.name not in workflow_map_text:
            problems.append(
                "permissions broader than 'contents: read' but not documented "
                f"in {WORKFLOW_MAP_REL}"
            )

    # concurrency
    concurrency = doc.get("concurrency")
    if "concurrency" not in doc:
        problems.append("missing top-level 'concurrency'")
    elif not isinstance(concurrency, dict):
        problems.append("'concurrency' is not a mapping")
    elif concurrency.get("cancel-in-progress") is not True:
        problems.append("'concurrency.cancel-in-progress' is not true")

    return problems


def build_results(root: Path) -> tuple[bool, list[str]]:
    """Run the check and return (ok, report_lines)."""
    workflows = find_workflows(root)
    map_path = root / WORKFLOW_MAP_REL
    workflow_map_text = map_path.read_text(encoding="utf-8") if map_path.exists() else ""

    lines: list[str] = ["# Workflow Posture Check", ""]
    if not workflows:
        lines.append("No workflow files found under .github/workflows/.")
        return True, lines

    all_ok = True
    for wf in workflows:
        problems = check_workflow(wf, workflow_map_text)
        rel = wf.relative_to(root) if wf.is_relative_to(root) else wf
        if problems:
            all_ok = False
            lines.append(f"FAIL {rel}")
            for problem in problems:
                lines.append(f"  - {problem}")
        else:
            lines.append(f"PASS {rel}")

    lines.append("")
    if all_ok:
        lines.append(f"PASS: {len(workflows)} workflow(s) meet the posture contract.")
    else:
        lines.append("FAIL: workflow posture drift detected. See items above.")
    return all_ok, lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify GitHub Actions workflows declare permissions and "
        "concurrency guards (deterministic, read-only).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=f"Repository root to scan (default: {REPO_ROOT}).",
    )
    args = parser.parse_args(argv)

    ok, lines = build_results(args.root)
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
