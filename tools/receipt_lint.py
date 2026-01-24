#!/usr/bin/env python3
"""
receipt_lint.py

Hard-fail on YAML duplicate keys and enforce canonical evidence_ref style.

Why:
- YAML parsers (including PyYAML) silently overwrite duplicate keys by default.
- This creates invisible audit drift (first values are lost).
- Receipts are DRAFT, so we canonicalize now and enforce via CI.

Rules (strict):
- Reject duplicate keys anywhere in YAML.
- For any `evidence_ref` string, disallow legacy ".json:" notation (require JSON pointer ".json#/...").
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Iterator

try:
    import yaml
except ImportError as e:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from e


class DuplicateKeyError(ValueError):
    pass


class NoDuplicateSafeLoader(yaml.SafeLoader):
    """YAML loader that raises on duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):  # type: ignore[override]
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                # Try to include line/col if available
                mark = getattr(key_node, "start_mark", None)
                loc = ""
                if mark is not None:
                    loc = f" (line {mark.line + 1}, col {mark.column + 1})"
                raise DuplicateKeyError(f"Duplicate key: {key!r}{loc}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def iter_yaml_files(path: Path) -> Iterator[Path]:
    if path.is_file():
        yield path
        return
    for p in sorted(path.rglob("*.yml")):
        yield p
    for p in sorted(path.rglob("*.yaml")):
        yield p


def find_evidence_refs(obj: Any) -> Iterator[str]:
    """Yield evidence_ref string values from a nested YAML structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "evidence_ref" and isinstance(v, str):
                yield v
            else:
                yield from find_evidence_refs(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from find_evidence_refs(item)


def is_legacy_manifest_colon(ref: str) -> bool:
    # Disallow "ark_cephalo_manifest_v2.json:dot.path"
    # Allow JSON pointer "ark_cephalo_manifest_v2.json#/..."
    return ".json:" in ref and ".json#/" not in ref


def lint_file(path: Path, strict: bool) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=NoDuplicateSafeLoader)
    except DuplicateKeyError as e:
        errors.append(f"{path}: {e}")
        return errors
    except Exception as e:  # pragma: no cover
        errors.append(f"{path}: YAML parse error: {e}")
        return errors

    for ref in find_evidence_refs(data):
        if is_legacy_manifest_colon(ref):
            errors.append(
                f"{path}: legacy evidence_ref style detected (use JSON pointer): {ref}"
            )
        # Optional: enforce that manifest refs use JSON pointer
        if strict and ref.endswith(".json"):
            errors.append(f"{path}: evidence_ref missing JSON pointer fragment: {ref}")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "path",
        nargs="+",
        help="File or directory of receipts/YAML to lint (e.g. ark/p4/receipts).",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict evidence_ref checks (recommended for CI).",
    )
    args = ap.parse_args()

    all_errors: list[str] = []
    for raw in args.path:
        p = Path(raw)
        if not p.exists():
            all_errors.append(f"{p}: path does not exist")
            continue
        for yf in iter_yaml_files(p):
            all_errors.extend(lint_file(yf, strict=args.strict))

    if all_errors:
        print("=== RECEIPT LINT: FAIL ===")
        for e in all_errors:
            print(f"- {e}")
        return 1

    print("=== RECEIPT LINT: PASS ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
