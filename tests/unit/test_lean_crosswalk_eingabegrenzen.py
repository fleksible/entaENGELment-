"""Eingabegrenzen des Lean-Crosswalks (Audit-Polish zu v0.1).

Ungültig typisierte Eingaben dürfen nie ein Beweisurteil erzeugen, schon gar
nicht ``FORMAL_CLOSED``. Sie enden in ``HOLD_INVALID_EVIDENCE``; nur ein echtes
``run_ok=False`` behält den Vorrang ``RUN_FAILED``. Keine Eingabe an dieser
Grenze darf eine Exception auslösen.

Die Hash-Prüfung in ``validate_card`` prüft nur Format und Gleichheit des
übergebenen Werts. Sie belegt nicht, dass der Hash aus einer echten
Lean-Ausgabe stammt.
"""

from __future__ import annotations

import pytest

from src.core import lean_crosswalk as lc

INVALID = "HOLD_INVALID_EVIDENCE"
ORIGIN = "a" * 64

INVALID_AXIOMS = [
    pytest.param("", id="leerer-string"),
    pytest.param("sorryAx", id="string-sorryAx"),
    pytest.param("propext", id="string-propext"),
    pytest.param({}, id="leeres-dict"),
    pytest.param({"propext": 1}, id="dict"),
    pytest.param(None, id="None"),
    pytest.param(b"sorryAx", id="bytes"),
    pytest.param(bytearray(b"propext"), id="bytearray"),
    pytest.param(iter(()), id="iterator"),
    pytest.param(range(0), id="range"),
    pytest.param(0, id="int"),
    pytest.param([""], id="leerer-name"),
    pytest.param([None], id="None-element"),
    pytest.param(["propext", 3], id="int-element"),
    pytest.param([b"propext"], id="bytes-element"),
    pytest.param(["has space"], id="leerzeichen-im-namen"),
    pytest.param(["propext, Quot.sound"], id="komma-im-namen"),
    pytest.param([["propext"]], id="verschachtelt"),
]


@pytest.mark.parametrize("axioms", INVALID_AXIOMS)
def test_invalid_axiom_input_never_yields_a_verdict(axioms):
    verdict = lc.assess(True, 1, axioms)
    assert verdict.status == INVALID
    assert verdict.axioms == ()
    assert verdict.foreign_axioms == ()


@pytest.mark.parametrize(
    "decl_count",
    [
        pytest.param(-1, id="negativ"),
        pytest.param(True, id="True"),
        pytest.param(False, id="False"),
        pytest.param(1.0, id="float"),
        pytest.param("1", id="string"),
        pytest.param(None, id="None"),
    ],
)
def test_invalid_decl_count(decl_count):
    assert lc.assess(True, decl_count, []).status == INVALID


@pytest.mark.parametrize(
    "run_ok",
    [
        pytest.param("false", id="string-false"),
        pytest.param("False", id="string-False"),
        pytest.param("", id="leerer-string"),
        pytest.param(1, id="int-1"),
        pytest.param(0, id="int-0"),
        pytest.param(None, id="None"),
    ],
)
def test_invalid_run_ok(run_ok):
    assert lc.evidence_gate(run_ok) == INVALID
    assert lc.assess(run_ok, 1, []).status == INVALID


@pytest.mark.parametrize("flag", ["evidence_integrity", "parse_known", "full_axiom_list"])
@pytest.mark.parametrize("value", ["false", "yes", 1, 0, None])
def test_invalid_gate_flags(flag, value):
    assert lc.evidence_gate(True, **{flag: value}) == INVALID
    assert lc.assess(True, 1, [], **{flag: value}).status == INVALID


def test_failed_run_keeps_highest_priority_over_any_invalid_input():
    assert lc.assess(False, -1, "sorryAx", parse_known="x").status == "RUN_FAILED"
    assert lc.assess(False, True, None).status == "RUN_FAILED"
    assert lc.evidence_gate(False, evidence_integrity="nope") == "RUN_FAILED"


def test_invalid_input_wins_over_declaration_status():
    # Eingabekontrolle nach dem Gate, aber vor fehlender/doppelter Deklaration.
    assert lc.assess(True, 0, "sorryAx").status == INVALID
    assert lc.assess(True, 2, None).status == INVALID


@pytest.mark.parametrize("container", [list, tuple, set, frozenset])
def test_valid_containers_keep_their_classification(container):
    cases = {
        ("propext",): "FORMAL_CLOSED",
        (): "FORMAL_CLOSED",
        ("Foo.propext",): "HOLD_TRUST_BOUNDARY",
        ("sorryAx",): "OPEN_OBLIGATION",
    }
    for axioms, status in cases.items():
        assert lc.assess(True, 1, container(axioms)).status == status
    mixed = lc.assess(True, 1, container(("sorryAx", "Foo.propext", "propext")))
    assert mixed.status == "OPEN_OBLIGATION"
    assert mixed.foreign_axioms == ("Foo.propext",)


# --- validate_card: Format des übergebenen Herkunfts-Hashes ----------------


def card_and_verdict():
    verdict = lc.assess(True, 1, ["propext"])
    return lc.build_card(verdict, ORIGIN), verdict


@pytest.mark.parametrize(
    "bad",
    [
        pytest.param("", id="leer"),
        pytest.param("abc", id="zu-kurz"),
        pytest.param("A" * 64, id="grossbuchstaben"),
        pytest.param("g" * 64, id="kein-hex"),
        pytest.param("a" * 65, id="zu-lang"),
        pytest.param(" " + "a" * 63, id="leerzeichen"),
        pytest.param(None, id="None"),
        pytest.param(123, id="int"),
        pytest.param(b"a" * 64, id="bytes"),
    ],
)
def test_invalid_origin_rejected_even_if_card_matches(bad):
    card, verdict = card_and_verdict()
    card["origin_sha256"] = bad
    assert lc.validate_card(card, verdict, bad) == ("PROVENANCE_DRIFT",)


def test_valid_but_different_origin_rejected():
    card, verdict = card_and_verdict()
    assert lc.validate_card(card, verdict, "b" * 64) == ("PROVENANCE_DRIFT",)


def test_valid_matching_origin_passes():
    card, verdict = card_and_verdict()
    assert lc.validate_card(card, verdict, ORIGIN) == ()


def test_invalid_origin_does_not_hide_other_findings():
    card, verdict = card_and_verdict()
    card["kind"] = "EPI-VOID"
    card["origin_sha256"] = ""
    reasons = lc.validate_card(card, verdict, "")
    assert "TYPE_DRIFT" in reasons
    assert reasons.count("PROVENANCE_DRIFT") == 1


def test_malformed_card_with_invalid_origin_reports_both():
    _, verdict = card_and_verdict()
    assert lc.validate_card({}, verdict, "") == ("MALFORMED_CARD", "PROVENANCE_DRIFT")
