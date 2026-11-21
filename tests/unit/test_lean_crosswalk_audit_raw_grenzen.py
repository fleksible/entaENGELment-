"""Eingabegrenzen von ``audit_raw`` (Abschluss des lokalen Polish).

Nur ein echtes ``int`` ist ein Exit-Code: ``0`` heißt Erfolg, jede andere ganze
Zahl ``RUN_FAILED``. Alles andere (``False``, ``True``, ``0.0``, ``"0"``,
``None`` …) ergibt ``HOLD_INVALID_EVIDENCE`` und nie ein Beweisurteil. Eine
Ausgabe, die kein Text ist, ergibt bei Exit-Code 0 ebenfalls
``HOLD_INVALID_EVIDENCE`` statt einer Exception. Ein echter Exit-Code ungleich 0
behält Vorrang vor einer unbrauchbaren Ausgabe.

``expected_decls`` gehört bewusst nicht zu diesem Schritt.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.core import lean_crosswalk as lc

RAW = Path(__file__).resolve().parents[1] / "fixtures" / "lean_crosswalk" / "raw"
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
OK_OUTPUT = (RAW / "ok_all.txt").read_text(encoding="utf-8")
BASE = {
    f"{NS}.thm_direct_gap": "OPEN_OBLIGATION",
    f"{NS}.thm_transitive_gap": "OPEN_OBLIGATION",
    f"{NS}.thm_closed_formal": "FORMAL_CLOSED",
    f"{NS}.thm_custom_axiom": "HOLD_TRUST_BOUNDARY",
    f"{NS}.thm_mixed": "OPEN_OBLIGATION",
}


def statuses(exit_code, output) -> dict[str, str]:
    return {d: v.status for d, v in lc.audit_raw(exit_code, output, EXPECTED_DECLS).items()}


def every(status: str) -> dict[str, str]:
    return dict.fromkeys(EXPECTED_DECLS, status)


@pytest.mark.parametrize(
    "exit_code",
    [
        pytest.param(False, id="False"),
        pytest.param(True, id="True"),
        pytest.param(0.0, id="float-0"),
        pytest.param(1.0, id="float-1"),
        pytest.param("0", id="string-0"),
        pytest.param(None, id="None"),
        pytest.param(b"0", id="bytes-0"),
    ],
)
def test_invalid_exit_code_never_yields_a_verdict(exit_code):
    assert statuses(exit_code, OK_OUTPUT) == every("HOLD_INVALID_EVIDENCE")


def test_exit_code_zero_still_reads_output():
    assert statuses(0, OK_OUTPUT) == BASE


@pytest.mark.parametrize("exit_code", [1, 2, -1, 137])
def test_nonzero_int_exit_code_is_run_failed(exit_code):
    assert statuses(exit_code, OK_OUTPUT) == every("RUN_FAILED")


@pytest.mark.parametrize(
    "output",
    [
        pytest.param(None, id="None"),
        pytest.param(OK_OUTPUT.encode("utf-8"), id="bytes"),
        pytest.param(bytearray(OK_OUTPUT.encode("utf-8")), id="bytearray"),
        pytest.param(OK_OUTPUT.splitlines(), id="zeilenliste"),
        pytest.param(123, id="int"),
    ],
)
def test_non_text_output_is_invalid_evidence(output):
    assert statuses(0, output) == every("HOLD_INVALID_EVIDENCE")


def test_failed_run_keeps_priority_over_unusable_output():
    assert statuses(1, None) == every("RUN_FAILED")


def test_invalid_exit_code_and_invalid_output():
    assert statuses(False, None) == every("HOLD_INVALID_EVIDENCE")
