#!/usr/bin/env python3
"""Verify evidence_ref entries in ark/p4/receipts against referenced files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml


RECEIPTS_DIR = Path("ark/p4/receipts")


def iter_evidence_refs(data: Any) -> Iterable[Tuple[str, str]]:
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "evidence_ref" and isinstance(value, str):
                yield (key, value)
            else:
                yield from iter_evidence_refs(value)
    elif isinstance(data, list):
        for item in data:
            yield from iter_evidence_refs(item)


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _resolve_json_pointer(doc: Any, pointer: str) -> Any:
    if pointer == "" or pointer == "/":
        return doc
    if not pointer.startswith("/"):
        raise KeyError(f"invalid JSON pointer '{pointer}'")
    current = doc
    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not token.isdigit():
                raise KeyError(f"expected list index for '{token}'")
            index = int(token)
            current = current[index]
        else:
            current = current[token]
    return current


def _resolve_dot_path(doc: Any, path: str) -> Any:
    current = doc
    for token in path.split("."):
        if isinstance(current, list):
            if not token.isdigit():
                raise KeyError(f"expected list index for '{token}'")
            current = current[int(token)]
        else:
            current = current[token]
    return current


def verify_evidence_ref(ref: str, root: Path, json_cache: Dict[Path, Any]) -> List[str]:
    errors: List[str] = []
    if "#/" in ref:
        file_part, _, pointer = ref.partition("#")
        target_path = root / file_part
        if not target_path.exists():
            return [f"missing file '{file_part}'"]
        if target_path.suffix != ".json":
            return [f"JSON pointer used for non-JSON file '{file_part}'"]
        doc = json_cache.setdefault(target_path, _load_json(target_path))
        try:
            _resolve_json_pointer(doc, pointer)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"broken JSON pointer '{ref}': {exc}")
        return errors

    if ":" in ref:
        file_part, _, tail = ref.partition(":")
        target_path = root / file_part
        if not target_path.exists():
            return [f"missing file '{file_part}'"]
        if target_path.suffix == ".json" and tail:
            doc = json_cache.setdefault(target_path, _load_json(target_path))
            try:
                _resolve_dot_path(doc, tail)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"broken dot path '{ref}': {exc}")
        return errors

    target_path = root / ref
    if not target_path.exists():
        return [f"missing file '{ref}'"]
    return []


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    receipts_path = root / RECEIPTS_DIR
    if not receipts_path.exists():
        print(f"Receipts directory not found: {receipts_path}")
        return 1

    json_cache: Dict[Path, Any] = {}
    failures: List[str] = []
    for yaml_path in sorted(receipts_path.glob("*.yaml")):
        with yaml_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        for _, ref in iter_evidence_refs(data):
            errors = verify_evidence_ref(ref, root, json_cache)
            for error in errors:
                failures.append(f"{yaml_path}: {error}")

    if failures:
        print("Broken evidence_ref entries detected:")
        for entry in failures:
            print(f"- {entry}")
        return 1

    print("All evidence_ref entries resolved successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
