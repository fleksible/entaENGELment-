#!/usr/bin/env python3
"""Verify relative markdown links in core docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOC_FILES = [
    Path("docs/START_HERE.md"),
    Path("docs/masterindex.md"),
    Path("docs/canvas_links.md"),
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_ignored_link(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )


def normalize_target(target: str) -> str:
    trimmed = target.split("#", 1)[0].split("?", 1)[0]
    return trimmed.strip()


def extract_links(text: str) -> list[str]:
    return [match for match in LINK_RE.findall(text) if match]


def looks_like_relative_path(target: str) -> bool:
    return "/" in target or "." in target


def verify_docs_links() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    missing: list[str] = []

    for doc_path in DOC_FILES:
        full_path = repo_root / doc_path
        if not full_path.exists():
            missing.append(f"Missing doc file: {doc_path}")
            continue
        content = full_path.read_text(encoding="utf-8")
        for target in extract_links(content):
            if is_ignored_link(target):
                continue
            normalized = normalize_target(target)
            if not normalized or not looks_like_relative_path(normalized):
                continue
            resolved = (full_path.parent / normalized).resolve()
            if not resolved.exists():
                missing.append(f"Broken link in {doc_path}: {target}")

    if missing:
        for entry in missing:
            print(f"[verify_docs_links] {entry}", file=sys.stderr)
        return 1

    print("✅ docs links ok")
    return 0


def main() -> None:
    sys.exit(verify_docs_links())


if __name__ == "__main__":
    main()
