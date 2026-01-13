#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Port Matrix Linter (K0..K4) — Repo-konform.
Ziel:
- Erkennt Port-Marker in Docs/Specs/Policies:  K0::NEBEL, K1::FADEN, K2::PORT?, K3::LEAK, K4::PASS
- Optional: Receipt Flood-Guard (MAX_CLAIMS_PER_RECEIPT)
WICHTIG:
- Kein "alle Markdown brauchen Marker" Zwang.
- Marker werden nur validiert, wenn eine Datei überhaupt Port-Marker enthält."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

MARKERS = [
    "K0::NEBEL",
    "K1::FADEN",
    "K2::PORT?",
    "K3::LEAK",
    "K4::PASS",
]

# Robust: match markers as tokens (handles '?' safely)
MARKER_RE = re.compile(r"(?<!\w)(K0::NEBEL|K1::FADEN|K2::PORT\?|K3::LEAK|K4::PASS)(?!\w)")

# Optional simple "claims flood" heuristic for receipts (JSON/YAML text scan)
MAX_CLAIMS_PER_RECEIPT = 50
CLAIM_TAG_RE = re.compile(r"\b(FACT|HYP|MET|TODO|RISK)\b")

# File filters
DEFAULT_SCAN_EXTS = {".md", ".txt", ".yaml", ".yml", ".json"}
EXCLUDE_DIR_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}


def iter_files(root: Path, exts: set[str]) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIR_PARTS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            yield p


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def extract_markers(text: str) -> List[str]:
    return MARKER_RE.findall(text)


def validate_marker_sequence(found: List[str]) -> List[str]:
    """
    If markers appear, enforce they are in non-decreasing "order" from K0..K4.
    Gaps are allowed (docs may only mention K2/K3, etc).
    Reordering backwards is flagged.
    """
    if not found:
        return []
    order = {m: i for i, m in enumerate(MARKERS)}
    idxs = [order[m] for m in found if m in order]
    errs: List[str] = []
    # Only check for backwards movement
    for a, b in zip(idxs, idxs[1:]):
        if b < a:
            errs.append("marker_order_backwards")
            break
    return errs


def validate_receipt_flood(text: str) -> List[str]:
    """
    Very light heuristic: if a file looks like a receipt and has too many claim tags, flag.
    This is intentionally conservative (no parsing dependency).
    """
    # heuristic trigger
    if "receipt" not in text.lower() and "receipts" not in text.lower():
        return []
    tags = CLAIM_TAG_RE.findall(text)
    if len(tags) > MAX_CLAIMS_PER_RECEIPT:
        return ["receipt_claim_flood"]
    return []


def lint_file(p: Path) -> List[Tuple[str, str]]:
    """
    Returns list of (error_code, message).
    Only enforces marker rules if file contains any markers.
    """
    txt = read_text(p)
    if not txt:
        return []
    found = extract_markers(txt)
    errors: List[Tuple[str, str]] = []
    if found:
        seq_errs = validate_marker_sequence(found)
        if seq_errs:
            errors.append(("K_MARKER_ORDER", f"{p.as_posix()}: marker order goes backwards: {found}"))
    # Receipt flood heuristic only on JSON/YAML-like files to avoid noisy docs
    if p.suffix.lower() in {".json", ".yaml", ".yml"}:
        flood = validate_receipt_flood(txt)
        if flood:
            errors.append(
                ("RECEIPT_FLOOD", f"{p.as_posix()}: too many claim tags (> {MAX_CLAIMS_PER_RECEIPT})")
            )
    return errors


def main(argv: List[str]) -> int:
    root = Path(".")
    exts = DEFAULT_SCAN_EXTS
    # Allow limiting scope
    only_path = None
    if "--path" in argv:
        i = argv.index("--path")
        if i + 1 >= len(argv):
            print("Usage: python tools/port_lint.py [--path <dir_or_file>]", file=sys.stderr)
            return 2
        only_path = Path(argv[i + 1])
    targets: List[Path]
    if only_path:
        if only_path.is_file():
            targets = [only_path]
        else:
            targets = list(iter_files(only_path, exts))
    else:
        targets = list(iter_files(root, exts))
    all_errors: List[Tuple[str, str]] = []
    for p in targets:
        all_errors.extend(lint_file(p))
    if all_errors:
        print("❌ Port-Lint: errors found\n", file=sys.stderr)
        for code, msg in all_errors:
            print(f"- [{code}] {msg}", file=sys.stderr)
        return 1
    if os.getenv("PORT_LINT_QUIET") != "1":
        print("✅ Port-Lint: OK (no errors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
