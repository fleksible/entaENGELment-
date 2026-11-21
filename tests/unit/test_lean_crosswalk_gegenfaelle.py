"""Gegenfälle zum Lean-Crosswalk (ATLAS-CROSSWALK-LEAN-001, Repo-Stand v0.1).

Diese Tests beschreiben die vier Mängel des v0.3-Übergabepakets. Am
übernommenen Ausgangsstand sind sie rot; erst die Korrektur macht sie grün.

Die CSV-Tabellen unter ``tests/fixtures/lean_crosswalk/tables`` sind die von
Hand gesetzte Vorgabe. Sie werden hier gelesen und nie aus dem Code erzeugt,
damit der Code sich nicht selbst prüft.

Die Rohausgaben unter ``tests/fixtures/lean_crosswalk/raw`` sind
FIXTURE_ONLY / NOT_KERNEL_VERIFIED: handgeschrieben, kein echter Lean-Lauf.
"""

from __future__ import annotations

import csv
import tomllib
from pathlib import Path

import pytest

from src.core import lean_crosswalk as lc

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "lean_crosswalk"
TABLES = FIXTURES / "tables"
RAW = FIXTURES / "raw"
LEAN = FIXTURES / "lean"

ORIGIN = "a" * 64
OTHER_ORIGIN = "b" * 64
NS = "CrosswalkProbe.Basic"
EXPECTED_DECLS = tuple(
    f"{NS}.{name}"
    for name in (
        "thm_direct_gap",
        "thm_transitive_gap",
        "thm_closed_formal",
        "thm_custom_axiom",
        "thm_mixed",
    )
)


def rows(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def example_verdict(status: str) -> lc.Verdict:
    """Ein Urteil je Status, erzeugt über die öffentliche Klassifikation."""
    inputs = {
        "RUN_FAILED": {"run_ok": False, "decl_count": 1, "axioms": []},
        "HOLD_INVALID_EVIDENCE": {
            "run_ok": True,
            "decl_count": 1,
            "axioms": [],
            "parse_known": False,
        },
        "HOLD_DECL_MISSING": {"run_ok": True, "decl_count": 0, "axioms": []},
        "HOLD_DECL_DUPLICATE": {"run_ok": True, "decl_count": 2, "axioms": []},
        "OPEN_OBLIGATION": {"run_ok": True, "decl_count": 1, "axioms": ["sorryAx", "propext"]},
        "HOLD_TRUST_BOUNDARY": {"run_ok": True, "decl_count": 1, "axioms": ["Foo.extra"]},
        "FORMAL_CLOSED": {"run_ok": True, "decl_count": 1, "axioms": ["propext"]},
    }[status]
    verdict = lc.assess(**inputs)
    assert verdict.status == status
    return verdict


MUTATIONS = {
    "baseline": lambda card: card,
    "kind_changed": lambda card: {**card, "kind": "EPI-VOID"},
    "claim_ceiling_fact": lambda card: {**card, "claim_ceiling": "FACT"},
    "semantic_reentry_reviewed": lambda card: {**card, "semantic_reentry": "REVIEWED"},
    "origin_hash_changed": lambda card: {**card, "origin_sha256": OTHER_ORIGIN},
    "visible_axiom_set_changed": lambda card: {**card, "axioms": ["Injected.axiom"]},
    "template_free_claim": lambda card: {
        **card,
        "summary": "Beweis erbracht: die Aussage ist damit wahr.",
    },
    "unverified_prose_as_certified": lambda card: {**card, "prose_review_state": "CERTIFIED"},
}


# --- Mangel 2: eine Statusquelle für Klassifikation, Karten und Tabellen ----


def test_status_source_matches_every_table():
    table_statuses = (
        {r["expected_status"] for r in rows("derivation_truth_table.csv")}
        | {r["expected_status"] for r in rows("audit_matrix.csv")}
        | {r["visible_status"] for r in rows("audit_matrix.csv")}
        | {r["source_status"] for r in rows("audit_negative_cases.csv")}
        | {r["expected_gate"] for r in rows("evidence_preflight_table.csv")} - {"PASS"}
    )
    assert set(lc.STATUSES) == table_statuses
    assert len(lc.STATUSES) == 7


@pytest.mark.parametrize("status", sorted(lc.STATUSES) if hasattr(lc, "STATUSES") else ["?"])
def test_every_status_renders_a_valid_card(status):
    verdict = example_verdict(status)
    card = lc.build_card(verdict, ORIGIN)
    assert lc.validate_card(card, verdict, ORIGIN) == ()


# --- Mangel 3: die Matrix läuft gegen den echten Kartenprüfer ---------------


def test_audit_matrix_runs_against_card_validator():
    items = rows("audit_matrix.csv")
    assert len(items) == 49
    for row in items:
        expected = example_verdict(row["expected_status"])
        visible_card = lc.build_card(example_verdict(row["visible_status"]), ORIGIN)
        reasons = lc.validate_card(visible_card, expected, ORIGIN)
        if row["verdict"] == "PASS":
            assert reasons == (), row
        else:
            assert row["failure_code"] in reasons, (row, reasons)


# --- Mangel 1: die Negativfälle werden wirklich ausgeführt ------------------


def test_negative_cases_are_executed():
    items = rows("audit_negative_cases.csv")
    assert len(items) == 56
    assert {r["mutation"] for r in items} == set(MUTATIONS)
    for row in items:
        verdict = example_verdict(row["source_status"])
        card = MUTATIONS[row["mutation"]](lc.build_card(verdict, ORIGIN))
        reasons = lc.validate_card(card, verdict, ORIGIN)
        if row["expected_verdict"] == "PASS":
            assert reasons == (), (row, reasons)
        else:
            assert row["expected_reason"] in reasons, (row, reasons)


def test_summary_is_bound_to_template_and_prose_lives_apart():
    verdict = example_verdict("FORMAL_CLOSED")
    card = lc.build_card(verdict, ORIGIN, notes="Freie Anmerkung, ungeprüft.")
    assert card["summary"] == lc.summary_for("FORMAL_CLOSED")
    assert card["prose_review_state"] == "UNVERIFIED_PROSE"
    assert lc.validate_card(card, verdict, ORIGIN) == ()
    moved = {**card, "summary": card["notes"]}
    assert "UNVERIFIED_SUMMARY" in lc.validate_card(moved, verdict, ORIGIN)


# --- Mischfall: Fremdaxiome gehen nicht verloren ----------------------------


def test_mixed_case_keeps_foreign_axioms():
    verdict = lc.assess(True, 1, ["sorryAx", "Foo.propext", "propext"])
    assert verdict.status == "OPEN_OBLIGATION"
    assert verdict.foreign_axioms == ("Foo.propext",)
    assert verdict.axioms == ("Foo.propext", "propext", "sorryAx")


# --- Vorprüfung: vollständig aufgezählt ------------------------------------


def test_evidence_preflight_table_exhaustive():
    items = rows("evidence_preflight_table.csv")
    seen = set()
    for row in items:
        key = tuple(
            row[k] == "True"
            for k in ("run_ok", "evidence_integrity", "parse_known", "full_axiom_list")
        )
        assert key not in seen
        seen.add(key)
        assert lc.evidence_gate(*key) == row["expected_gate"], row
    assert len(seen) == 16


# --- Verkabelung Rohausgabe → Merkmale (FIXTURE_ONLY) -----------------------


def audit(name: str, exit_code: int = 0) -> dict[str, str]:
    text = (RAW / name).read_text(encoding="utf-8")
    return {decl: v.status for decl, v in lc.audit_raw(exit_code, text, EXPECTED_DECLS).items()}


BASE = {
    f"{NS}.thm_direct_gap": "OPEN_OBLIGATION",
    f"{NS}.thm_transitive_gap": "OPEN_OBLIGATION",
    f"{NS}.thm_closed_formal": "FORMAL_CLOSED",
    f"{NS}.thm_custom_axiom": "HOLD_TRUST_BOUNDARY",
    f"{NS}.thm_mixed": "OPEN_OBLIGATION",
}


def every(status: str) -> dict[str, str]:
    return dict.fromkeys(EXPECTED_DECLS, status)


@pytest.mark.parametrize(
    ("name", "exit_code", "expected"),
    [
        ("ok_all.txt", 0, BASE),
        ("ok_with_position_prefix.txt", 0, BASE),
        ("missing_decl.txt", 0, {**BASE, f"{NS}.thm_custom_axiom": "HOLD_DECL_MISSING"}),
        ("duplicate_decl.txt", 0, {**BASE, f"{NS}.thm_closed_formal": "HOLD_DECL_DUPLICATE"}),
        ("wrapped_line.txt", 0, every("HOLD_INVALID_EVIDENCE")),
        ("unexpected_decl.txt", 0, every("HOLD_INVALID_EVIDENCE")),
        ("run_failed_partial.txt", 1, every("RUN_FAILED")),
        ("run_failed_partial.txt", 0, every("HOLD_INVALID_EVIDENCE")),
        ("ok_all.txt", 1, every("RUN_FAILED")),
        ("lookalike_axiom.txt", 0, {**BASE, f"{NS}.thm_closed_formal": "HOLD_TRUST_BOUNDARY"}),
    ],
)
def test_raw_output_wiring(name, exit_code, expected):
    assert audit(name, exit_code) == expected


def test_raw_output_mixed_case_keeps_foreign_axiom():
    text = (RAW / "ok_all.txt").read_text(encoding="utf-8")
    verdict = lc.audit_raw(0, text, EXPECTED_DECLS)[f"{NS}.thm_mixed"]
    assert verdict.foreign_axioms == (f"{NS}.externalAssumption",)


# --- Mangel 4: der Lean-Teil ist als Projekt aufrufbar ----------------------


def test_lean_fixture_is_a_lake_project():
    config = tomllib.loads((LEAN / "lakefile.toml").read_text(encoding="utf-8"))
    libs = config.get("lean_lib", [])
    assert any("CrosswalkProbe.Basic" in lib.get("roots", []) for lib in libs)
    assert (LEAN / "lean-toolchain").read_text(encoding="utf-8").startswith("leanprover/lean4:")


def test_audit_file_starts_with_import():
    """In Lean muss ``import`` vor jedem Befehl stehen; ein ``/-!``-Moduldoc davor bricht den Kopf."""
    lines = [
        line
        for line in (LEAN / "CrosswalkProbe" / "Audit.lean")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert lines[0].startswith("import ")
    expected = {f"#print axioms {decl}" for decl in EXPECTED_DECLS}
    assert {line for line in lines if line.startswith("#print axioms")} == expected
