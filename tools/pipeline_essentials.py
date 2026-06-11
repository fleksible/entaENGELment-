#!/usr/bin/env python3
"""Static checklist for DeepJump pipeline expansion candidates."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EssentialCheck:
    id: str
    title: str
    path: str
    needles: tuple[str, ...]
    recommendation: str
    status_when_present: str = "covered"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


CHECKS: tuple[EssentialCheck, ...] = (
    EssentialCheck(
        id="ESS-001",
        title="Canonical local verify entrypoint",
        path="Makefile",
        needles=("verify: port-lint test verify-pointers claim-lint",),
        recommendation="Keep `make verify` as the single local pre-merge command.",
    ),
    EssentialCheck(
        id="ESS-002",
        title="Receipt lint in release gate",
        path=".github/workflows/release.yml",
        needles=("tools/receipt_lint.py",),
        recommendation="Promote receipt lint into a reusable local/PR target once scope is stable.",
    ),
    EssentialCheck(
        id="ESS-003",
        title="VOID backlog drift check",
        path="Makefile",
        needles=("voids-backlog-check",),
        recommendation="Run backlog drift checks in PR CI to catch stale governance docs early.",
    ),
    EssentialCheck(
        id="ESS-004",
        title="Frame operator lint exists",
        path="Makefile",
        needles=("frame-lint", "FRAME_LINT_PATHS"),
        recommendation="Define canonical frame-lint scope, then add it to the verify chain.",
    ),
    EssentialCheck(
        id="ESS-005",
        title="HMAC status verification path",
        path="Makefile",
        needles=("status-verify: status", "tools/status_verify.py"),
        recommendation="Keep signed status verification separate from fork PRs that lack secrets.",
    ),
    EssentialCheck(
        id="ESS-006",
        title="Strict snapshot guard path",
        path="Makefile",
        needles=("snapshot:", "--strict"),
        recommendation="Upload snapshot manifests from scheduled and trusted CI runs.",
    ),
    EssentialCheck(
        id="ESS-007",
        title="Dependency vulnerability scan",
        path=".github/workflows/ci.yml",
        needles=("pip-audit",),
        recommendation="Mirror a lightweight dependency audit target locally for release prep.",
    ),
    EssentialCheck(
        id="ESS-008",
        title="Pinned GitHub Actions",
        path=".github/workflows/ci.yml",
        needles=("actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",),
        recommendation="Keep action SHAs pinned and rotate them through reviewable dependency PRs.",
    ),
)


def check_file(repo_root: Path, check: EssentialCheck) -> tuple[bool, str]:
    target = repo_root / check.path
    if not target.exists():
        return False, f"missing file: {check.path}"
    text = target.read_text(encoding="utf-8")
    missing = [needle for needle in check.needles if needle not in text]
    if missing:
        return False, "missing: " + ", ".join(f"`{needle}`" for needle in missing)
    return True, check.status_when_present


def build_report(repo_root: Path) -> str:
    rows: list[str] = []
    opportunities: list[str] = []
    for check in CHECKS:
        covered, detail = check_file(repo_root, check)
        status = "COVERED" if covered else "OPEN"
        rows.append(f"| {check.id} | {status} | {check.title} | `{check.path}` | {detail} |")
        opportunities.append(f"- **{check.id}**: {check.recommendation}")

    return "\n".join(
        [
            "# Pipeline Essentials Report",
            "",
            "[FACT] Static scan of local files for DeepJump pipeline essentials.",
            "",
            "| ID | Status | Essential | Evidence | Detail |",
            "|----|--------|-----------|----------|--------|",
            *rows,
            "",
            "## Ausbau-Möglichkeiten",
            "",
            *opportunities,
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=get_repo_root())
    parser.add_argument("--out", type=Path, help="Optional Markdown output path.")
    args = parser.parse_args()

    report = build_report(args.repo_root.resolve())
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
