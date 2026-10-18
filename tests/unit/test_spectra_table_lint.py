"""VOID-010: Quellenpflicht der Spektren-Tabelle (data/spectra/)."""

from pathlib import Path

import pytest

from tools import spectra_table_lint as lint

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = lint.load_schema()
TAGS = lint.policy_tags()
HEADER = ",".join(c["name"] for c in SCHEMA["columns"])

# Formal gültige Beispielzeile: prüft nur den Lint, ist KEIN Datensatz der Tabelle.
VALID = (
    "SPEC-001,Beispielorganismus,organism,VIS,400,700,Laborbedingung X,"
    '"Autor A (2020) Titel. Journal",10.1000/example,peer_reviewed,2026-10-18,'
    "nur Beispielorganismus unter X,[FACT],keine Aussage über andere Spezies"
)


def _lint(*rows: str) -> list[str]:
    return lint.lint_text("\n".join((HEADER, *rows)) + "\n", SCHEMA, TAGS)


def test_committed_table_passes():
    table = ROOT / SCHEMA["table"]
    assert lint.lint_text(table.read_text(encoding="utf-8"), SCHEMA, TAGS) == []


def test_valid_row_passes():
    assert _lint(VALID) == []


def test_schema_claim_tags_exist_in_policy():
    allowed = next(c["allowed"] for c in SCHEMA["columns"] if c["name"] == "claim_tag")
    assert set(allowed) <= TAGS


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("10.1000/example", "", "Pflichtfeld 'source_doi_or_url' leer"),
        ("10.1000/example", "example.org", "'source_doi_or_url' passt nicht"),
        (",400,700,", ",700,400,", "'wavelength_max_nm' < 'wavelength_min_nm'"),
        ("peer_reviewed", "blog", "'source_type'='blog' nicht erlaubt"),
        ("2026-10-18", "18.10.2026", "'accessed' ist kein ISO-Datum"),
        ("[FACT]", "[MODEL]", "'claim_tag'='[MODEL]' nicht erlaubt"),
        (",400,700,", ",nan,nan,", "'wavelength_min_nm' ist keine Zahl"),
        (",400,700,", ",400,inf,", "'wavelength_max_nm' ist keine Zahl"),
        ("Spezies", "Spezies,überzählig", "mehr Zellen als Spalten"),
    ],
)
def test_invalid_rows_are_rejected(old, new, expected):
    errors = _lint(VALID.replace(old, new, 1))
    assert any(expected in e for e in errors), errors


def test_duplicate_record_id_is_rejected():
    assert any("doppelt" in e for e in _lint(VALID, VALID))


def test_wrong_header_is_rejected():
    errors = lint.lint_text("record_id,subject\n", SCHEMA, TAGS)
    assert errors and "Kopfzeile" in errors[0]
