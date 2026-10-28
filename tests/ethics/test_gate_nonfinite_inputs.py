"""
tests/ethics/test_gate_nonfinite_inputs.py

Fail-closed regression tests for the MZM gate (finding B1).

Invariant: an open gate implies that every defined gate condition holds and that
phi and m_norm_l2 are finite real numbers. NaN, +inf and -inf must block, alone
and combined, with and without ledger, with and without strict mode. With a
ledger the decision must still be made and logged; invalid raw metrics must not
abort it, and no substitute value is logged for them.
"""

import itertools
import math

import pytest

from src.core.ledger import Ledger
from tools.mzm.gate_toggle import Context, GateBlockedError, gate_open, load_policy, main

POLICY = load_policy()
NONFINITE = [math.nan, math.inf, -math.inf]
VALID_PHI = 1.0
VALID_M = 1.0


def _ctx(phi=VALID_PHI, m=VALID_M, rcc_ec=True, non_overlap=True, psi_lock=True):
    return Context(phi=phi, rcc_ec=rcc_ec, non_overlap=non_overlap, m_norm_l2=m, psi_lock=psi_lock)


def _expected_reason(phi, m):
    if not math.isfinite(phi) or phi < POLICY["constraints"]["phi_min"]:
        return "BLOCK_PHI_BELOW_MIN"
    if not math.isfinite(m) or abs(m - POLICY["constraints"]["m_norm_l2"]) >= 1e-9:
        return "BLOCK_M_NORM_INVALID"
    return None


CASES = (
    [(bad, VALID_M) for bad in NONFINITE]
    + [(VALID_PHI, bad) for bad in NONFINITE]
    + list(itertools.product(NONFINITE, NONFINITE))
)


@pytest.mark.parametrize("phi,m", CASES)
def test_nonfinite_inputs_block_without_ledger(phi, m):
    assert gate_open(_ctx(phi=phi, m=m), POLICY) is False


@pytest.mark.parametrize("phi,m", CASES)
def test_nonfinite_inputs_raise_in_strict_mode(phi, m):
    with pytest.raises(GateBlockedError) as exc_info:
        gate_open(_ctx(phi=phi, m=m), POLICY, strict=True)
    assert str(exc_info.value) == _expected_reason(phi, m)


@pytest.mark.parametrize("strict", [False, True])
@pytest.mark.parametrize("phi,m", CASES)
def test_nonfinite_inputs_block_and_are_logged_with_ledger(phi, m, strict):
    ledger = Ledger()
    if strict:
        with pytest.raises(GateBlockedError):
            gate_open(_ctx(phi=phi, m=m), POLICY, ledger=ledger, strict=True)
    else:
        assert gate_open(_ctx(phi=phi, m=m), POLICY, ledger=ledger) is False

    gate_events = ledger.get_events("gate")
    assert len(gate_events) == 1
    assert gate_events[0]["payload"]["passed"] is False
    assert gate_events[0]["payload"]["reason"] == _expected_reason(phi, m)

    # Only finite raw metrics are logged; nothing is invented for the others.
    logged = {
        e["payload"]["metric_id"]: e["payload"]["value"]
        for e in ledger.get_events("metric")
        if e["payload"]["metric_id"].startswith("mzm.")
    }
    expected = {}
    if math.isfinite(phi):
        expected["mzm.phi"] = phi
    if math.isfinite(m):
        expected["mzm.m_norm_l2"] = m
    assert logged == expected
    assert ledger.verify_chain() is True


def test_nonfinite_inputs_keep_persisted_ledger_valid(tmp_path):
    from src.core.ledger import verify_chain_from_file

    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    for phi, m in CASES:
        gate_open(_ctx(phi=phi, m=m), POLICY, ledger=ledger)
    text = path.read_text(encoding="utf-8")
    assert "NaN" not in text and "Infinity" not in text
    assert verify_chain_from_file(path) is True


GRID_PHI = [math.nan, math.inf, -math.inf, -1.0, 0.0, 0.79, 0.8, 0.81, 1.0, 1e308]
GRID_M = [math.nan, math.inf, -math.inf, 0.0, 1.0 - 1e-8, 1.0, 1.0 + 1e-10, 2.0]
GRID_BOOL = [True, False]


@pytest.mark.parametrize("rcc_ec", GRID_BOOL)
@pytest.mark.parametrize("non_overlap", GRID_BOOL)
@pytest.mark.parametrize("psi_lock", GRID_BOOL)
def test_open_implies_all_conditions(rcc_ec, non_overlap, psi_lock):
    """Deterministic grid: gate open => every defined condition holds."""
    c = POLICY["constraints"]
    for phi, m in itertools.product(GRID_PHI, GRID_M):
        ctx = _ctx(phi=phi, m=m, rcc_ec=rcc_ec, non_overlap=non_overlap, psi_lock=psi_lock)
        if gate_open(ctx, POLICY):
            assert math.isfinite(phi) and phi >= c["phi_min"]
            assert math.isfinite(m) and abs(m - c["m_norm_l2"]) < 1e-9
            assert rcc_ec is True and non_overlap is True and psi_lock is True


@pytest.mark.parametrize(
    "field,value",
    [
        ("phi", True),
        ("phi", "1.0"),
        ("phi", None),
        ("m", True),
        ("m", "1.0"),
        ("rcc_ec", "false"),
        ("non_overlap", 1),
        ("psi_lock", "yes"),
    ],
)
def test_non_real_or_non_bool_inputs_do_not_open(field, value):
    """Truthy substitutes are not accepted as fulfilled conditions."""
    kwargs = {field: value}
    assert gate_open(_ctx(**kwargs), POLICY) is False


def test_valid_context_still_opens():
    assert gate_open(_ctx(), POLICY) is True


@pytest.mark.parametrize(
    "argv",
    [
        ["gate", "nan", "true", "true", "1.0", "true"],
        ["gate", "0.9", "true", "true", "nan", "true"],
        ["gate", "inf", "true", "true", "1.0", "true"],
        ["gate", "-inf", "true", "true", "-inf", "true"],
    ],
)
def test_cli_does_not_open_on_nonfinite(argv, capsys, monkeypatch):
    monkeypatch.delenv("ENTA_LEDGER_PATH", raising=False)
    monkeypatch.delenv("ENTA_GATE_STRICT", raising=False)
    assert main(argv) == 0
    assert capsys.readouterr().out.strip() == "GateOpen=false"

    monkeypatch.setenv("ENTA_GATE_STRICT", "1")
    assert main(argv) == 1
