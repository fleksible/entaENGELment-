#!/usr/bin/env python3
"""Prüft Events gegen spec/runtime_eventlog_v0_1.json ([SPEC-WIP], keine Laufzeit-Erzwingung).

Regeln aus ``field_rules`` der Spec:
- ``required_fields``: vorhanden und nicht leer
- ``required_one_of``: je Gruppe mindestens eine Alternative vorhanden und nicht leer
- ``reduced_forbidden_fields``: im reduzierten/öffentlichen Export abwesend (``--export``)

Felder werden aus Envelope (event_id, timestamp, …) und ``payload`` zusammengelesen;
das Format entspricht den ERK-Events (``type`` + ``payload``). Event-Typen außerhalb
des Spec-Vokabulars werden übersprungen, nicht als Fehler gewertet.

Usage:
    python tools/eventlog_spec_check.py EVENTS.jsonl [--export]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

SPEC_PATH = Path(__file__).resolve().parents[1] / "spec" / "runtime_eventlog_v0_1.json"


def load_spec() -> dict[str, Any]:
    spec: dict[str, Any] = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    return spec


def _fields(event: Mapping[str, Any]) -> dict[str, Any]:
    fields = {k: v for k, v in event.items() if k not in ("type", "event_type", "payload")}
    payload = event.get("payload")
    if isinstance(payload, Mapping):
        fields.update(payload)
    return fields


def _present(fields: Mapping[str, Any], name: str) -> bool:
    value = fields.get(name)
    return value is not None and value != "" and value != []


def check_event(
    event: Mapping[str, Any], spec: Mapping[str, Any], *, export: bool = False
) -> list[str] | None:
    """Befunde für ein Event; ``None``, wenn der Typ nicht im Spec-Vokabular steht."""
    event_type = event.get("type") or event.get("event_type")
    rules = spec["event_types"].get(event_type)
    if rules is None:
        return None
    fields = _fields(event)
    errors = [
        f"{event_type}: Pflichtfeld '{name}' fehlt oder ist leer"
        for name in rules["required_fields"]
        if not _present(fields, name)
    ]
    for group in rules.get("required_one_of", []):
        if not any(_present(fields, name) for name in group):
            errors.append(f"{event_type}: eines von {group} erforderlich")
    if export:
        errors.extend(
            f"{event_type}: '{name}' darf im reduzierten Export nicht stehen"
            for name in rules.get("reduced_forbidden_fields", [])
            if name in fields
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("events", type=Path, help="JSONL-Datei mit Events")
    parser.add_argument("--export", action="store_true", help="als reduzierten Export prüfen")
    args = parser.parse_args()

    spec = load_spec()
    checked = skipped = 0
    findings: list[str] = []
    for line_no, line in enumerate(args.events.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        result = check_event(json.loads(line), spec, export=args.export)
        if result is None:
            skipped += 1
            continue
        checked += 1
        findings.extend(f"Zeile {line_no}: {e}" for e in result)
    for finding in findings:
        print(f"[FAIL] {finding}")
    print(f"[INFO] {checked} Events geprüft, {skipped} außerhalb des Spec-Vokabulars übersprungen")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
