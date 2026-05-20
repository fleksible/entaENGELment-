#!/usr/bin/env python3
"""Verify save-state card templates.

This checker intentionally uses only the Python standard library. It validates
small JSON templates under cards/templates/ without treating them as immutable
receipts or runtime evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ISO_LIKE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

REQUIRED_FIELDS: dict[str, set[str]] = {
    "ack_triade": {
        "ack_me",
        "ack_mensch",
        "ack_sys",
        "body_signal",
        "rationale",
        "mode_from",
        "mode_to",
    },
    "nectar_attune": {
        "signal",
        "texture",
        "intensity",
        "boundary",
        "next_hold",
    },
    "rubedo_stop": {
        "marker",
        "hue_load",
        "abx_stress",
        "hold_reason",
        "next_safe_action",
    },
    "synthosia_scope": {
        "gate",
        "included_concepts",
        "forbidden_actions",
        "go_condition",
    },
    "reentry_vector": {
        "status",
        "current_hold",
        "next_action",
        "source_doc",
    },
    "ruecknahme_exit": {
        "exit_gesture",
        "sediment_action",
        "released_state",
        "no_trace",
        "post_exit_claim",
        "boundary",
    },
}


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"{path}: invalid JSON: {exc}"]
    except OSError as exc:
        return None, [f"{path}: read error: {exc}"]

    if not isinstance(data, dict):
        return None, [f"{path}: top-level JSON value must be an object"]
    return data, []


def validate_ruecknahme_exit(path: Path, fields: dict[str, Any]) -> list[str]:
    """Validate Rücknahme-specific release semantics.

    For this card type, `no_trace: true` is the invariant. It represents a
    successful release state, not a telemetry target.
    """
    errors: list[str] = []

    if fields.get("no_trace") is not True:
        errors.append(f"{path}: ruecknahme_exit requires fields.no_trace to be true")

    if fields.get("released_state") is not True:
        errors.append(f"{path}: ruecknahme_exit requires fields.released_state to be true")

    if fields.get("post_exit_claim") not in ("none", ""):
        errors.append(
            f"{path}: ruecknahme_exit post_exit_claim must be 'none' or empty"
        )

    return errors


def validate_card(path: Path) -> list[str]:
    data, errors = load_json(path)
    if data is None:
        return errors

    for key in ("card_type", "timestamp", "fields"):
        if key not in data:
            errors.append(f"{path}: missing top-level key: {key}")

    card_type = data.get("card_type")
    timestamp = data.get("timestamp")
    fields = data.get("fields")

    if not isinstance(card_type, str) or not card_type:
        errors.append(f"{path}: card_type must be a non-empty string")
        return errors

    if card_type not in REQUIRED_FIELDS:
        allowed = ", ".join(sorted(REQUIRED_FIELDS))
        errors.append(f"{path}: unknown card_type {card_type!r}; allowed: {allowed}")
        return errors

    if not isinstance(timestamp, str) or not ISO_LIKE.search(timestamp):
        errors.append(f"{path}: timestamp must be an ISO-like string")

    if not isinstance(fields, dict):
        errors.append(f"{path}: fields must be an object")
        return errors

    required = REQUIRED_FIELDS[card_type]
    missing = sorted(required - set(fields))
    if missing:
        errors.append(f"{path}: missing fields: {', '.join(missing)}")

    for field_name, value in fields.items():
        if isinstance(value, (dict, list, str, int, float, bool)) or value is None:
            continue
        errors.append(f"{path}: field {field_name!r} has unsupported type")

    if card_type == "ruecknahme_exit":
        errors.extend(validate_ruecknahme_exit(path, fields))

    return errors


def iter_cards(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(root.rglob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify save-state card JSON templates")
    parser.add_argument(
        "path",
        nargs="?",
        default="cards/templates",
        help="Card file or directory to verify (default: cards/templates)",
    )
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"VERIFY CARDS: FAIL\n- path does not exist: {root}")
        return 1

    cards = iter_cards(root)
    if not cards:
        print(f"VERIFY CARDS: FAIL\n- no JSON card templates found under: {root}")
        return 1

    errors: list[str] = []
    for card in cards:
        errors.extend(validate_card(card))

    if errors:
        print("VERIFY CARDS: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VERIFY CARDS: PASS ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
