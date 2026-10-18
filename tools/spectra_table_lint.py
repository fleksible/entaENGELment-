#!/usr/bin/env python3
"""VOID-010: Quellenpflicht-Lint für data/spectra/spectra_sources.csv.

Prüft die Tabelle gegen ``data/spectra/spectra_sources.schema.json``:
- Kopfzeile exakt in Schema-Reihenfolge
- Pflichtfelder nicht leer (insbesondere Quelle und DOI/URL)
- Muster (record_id, DOI/URL), erlaubte Werte, Zahlen, ISO-Datum
- wavelength_max_nm >= wavelength_min_nm
- claim_tag erlaubt UND in policies/claim_tags_v0_2.yaml definiert
- record_id eindeutig

Eine leere Tabelle (nur Kopfzeile) ist gültig: Das Gerüst darf ohne Daten
existieren, erfundene Daten sind ausgeschlossen. Exit 1 bei Befunden.

Usage:
    python tools/spectra_table_lint.py [--table PATH]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "spectra" / "spectra_sources.schema.json"
POLICY_PATH = ROOT / "policies" / "claim_tags_v0_2.yaml"


def load_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return schema


def policy_tags() -> set[str]:
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
    return set(policy["tags"])


def _number(value: str) -> float | None:
    """Endliche Zahl oder ``None`` (NaN/inf gelten nicht als Zahl)."""
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def lint_text(text: str, schema: dict[str, Any], known_tags: set[str]) -> list[str]:
    """Gibt Befunde als ``Zeile N: …``-Strings zurück (leer = gültig)."""
    columns = schema["columns"]
    names = [c["name"] for c in columns]
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != names:
        return [f"Kopfzeile weicht vom Schema ab: {reader.fieldnames} != {names}"]

    errors: list[str] = []
    seen: set[str] = set()
    for line_no, row in enumerate(reader, start=2):
        if None in row:  # DictReader legt überzählige Zellen unter None ab
            errors.append(f"Zeile {line_no}: mehr Zellen als Spalten im Schema")
        for col in columns:
            name = col["name"]
            value = (row.get(name) or "").strip()
            if col.get("required") and not value:
                errors.append(f"Zeile {line_no}: Pflichtfeld '{name}' leer")
                continue
            if "pattern" in col and not re.match(col["pattern"], value):
                errors.append(f"Zeile {line_no}: '{name}' passt nicht zu {col['pattern']}")
            if "allowed" in col and value not in col["allowed"]:
                errors.append(f"Zeile {line_no}: '{name}'={value!r} nicht erlaubt")
            if col.get("type") == "number":
                number = _number(value)
                if number is None:
                    errors.append(f"Zeile {line_no}: '{name}' ist keine Zahl")
                elif "min" in col and number < col["min"]:
                    errors.append(f"Zeile {line_no}: '{name}' < {col['min']}")
            if col.get("type") == "date":
                try:
                    dt.date.fromisoformat(value)
                except ValueError:
                    errors.append(f"Zeile {line_no}: '{name}' ist kein ISO-Datum")
            if "not_less_than" in col:
                low, high = _number(row.get(col["not_less_than"]) or ""), _number(value)
                if low is not None and high is not None and high < low:
                    errors.append(f"Zeile {line_no}: '{name}' < '{col['not_less_than']}'")
            if col.get("policy") and value not in known_tags:
                errors.append(f"Zeile {line_no}: claim_tag {value!r} fehlt in der Policy")
        record_id = (row.get("record_id") or "").strip()
        if record_id in seen:
            errors.append(f"Zeile {line_no}: record_id {record_id} doppelt")
        seen.add(record_id)
    return errors


def main() -> int:
    schema = load_schema()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--table", type=Path, default=ROOT / schema["table"])
    args = parser.parse_args()

    errors = lint_text(args.table.read_text(encoding="utf-8"), schema, policy_tags())
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        return 1
    print(f"[OK] {args.table}: Quellenpflicht erfüllt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
