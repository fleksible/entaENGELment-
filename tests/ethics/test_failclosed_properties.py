"""
tests/ethics/test_failclosed_properties.py

Property-based versions of the fail-closed invariants from the deterministic
regression tests (B1, B2, B4, B5, B3, bootstrap_ci).

Hypothesis only finds what these properties state; the strategies deliberately
include NaN, +inf, -inf, bool and non-numeric values. ``derandomize=True`` keeps
CI runs reproducible (same examples on every run, no example database).
"""

import json
import math
import tempfile
from pathlib import Path

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from src.core.eci import bootstrap_ci, permutation_test
from src.core.ledger import Ledger, verify_chain_from_file
from src.core.stability_guard import stability_gate
from src.stability.hessian_void import classify_stability
from src.stability.spectral_void import classify_spectral_void
from src.stability.stability_guard import map_taxonomy_to_gate
from tools.mzm.gate_toggle import Context, GateBlockedError, gate_open, load_policy

PROPERTY_SETTINGS = settings(
    derandomize=True,
    database=None,
    deadline=None,
    max_examples=300,
    suppress_health_check=[HealthCheck.too_slow],
)

POLICY = load_policy()
C = POLICY["constraints"]

any_float = st.floats(allow_nan=True, allow_infinity=True)
not_quite_numbers = st.one_of(
    st.booleans(),
    st.none(),
    st.text(max_size=5),
    st.integers(min_value=-(10**400), max_value=10**400),
)
gate_numbers = st.one_of(any_float, not_quite_numbers)
gate_flags = st.one_of(st.booleans(), st.integers(-1, 2), st.text(max_size=5), st.none())


def _is_finite_real(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


# --- B1: gate ---------------------------------------------------------------


@PROPERTY_SETTINGS
@given(
    phi=gate_numbers,
    m=gate_numbers,
    rcc_ec=gate_flags,
    non_overlap=gate_flags,
    psi_lock=gate_flags,
    with_ledger=st.booleans(),
    strict=st.booleans(),
)
def test_gate_open_implies_every_condition(
    phi, m, rcc_ec, non_overlap, psi_lock, with_ledger, strict
):
    ctx = Context(phi=phi, rcc_ec=rcc_ec, non_overlap=non_overlap, m_norm_l2=m, psi_lock=psi_lock)
    ledger = Ledger() if with_ledger else None
    try:
        opened = gate_open(ctx, POLICY, ledger=ledger, strict=strict)
    except GateBlockedError:
        opened = False
        assert strict

    if opened:
        assert _is_finite_real(phi) and phi >= C["phi_min"]
        assert _is_finite_real(m) and abs(m - C["m_norm_l2"]) < 1e-9
        assert rcc_ec is True and non_overlap is True and psi_lock is True

    if ledger is not None:
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1 and gate_events[0]["payload"]["passed"] is opened
        for event in ledger.get_events("metric"):
            assert math.isfinite(event["payload"]["value"])
        assert ledger.verify_chain() is True


@PROPERTY_SETTINGS
@given(phi=any_float, m=any_float)
def test_non_finite_inputs_never_open(phi, m):
    ctx = Context(phi=phi, rcc_ec=True, non_overlap=True, m_norm_l2=m, psi_lock=True)
    if not (math.isfinite(phi) and math.isfinite(m)):
        assert gate_open(ctx, POLICY) is False


# --- B2: negative curvature has priority -------------------------------------

TAU = 1e-6
eigenvalue = st.one_of(
    st.floats(-1e3, 1e3, allow_nan=False),
    st.sampled_from([0.0, TAU, -TAU, TAU / 2, -TAU / 2, 2 * TAU, -2 * TAU]),
)


@PROPERTY_SETTINGS
@given(
    values=st.lists(eigenvalue, min_size=1, max_size=4),
    angle=st.floats(0, math.pi),
    consent=st.booleans(),
)
def test_negative_direction_blocks_even_with_consent(values, angle, consent):
    spectrum = np.array(values)
    H = np.diag(spectrum)
    if spectrum.size >= 2:
        Q = np.eye(spectrum.size)
        Q[:2, :2] = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
        H = Q @ H @ Q.T
        H = (H + H.T) / 2
    margin = 1e-9 * max(1.0, float(np.max(np.abs(spectrum))))
    if np.any(spectrum < -TAU - margin):
        assert classify_stability(H, threshold=TAU)[0] == "UNSTABLE"
        assert stability_gate(H, consent_available=consent)[0] is False


@PROPERTY_SETTINGS
@given(values=st.lists(eigenvalue, min_size=1, max_size=4), consent=st.booleans())
def test_core_and_mod18_agree_on_blocking(values, consent):
    spectrum = np.array(values)
    core_allow, _ = stability_gate(np.diag(spectrum), consent_available=consent)
    decision, _ = map_taxonomy_to_gate(
        classify_spectral_void(spectrum, eps=TAU), has_consent=consent
    )
    assert core_allow == (decision == "ALLOW")


# --- B5 / B4: ledger -----------------------------------------------------------

json_leaf = st.one_of(
    st.none(), st.booleans(), any_float, st.integers(-(10**6), 10**6), st.text(max_size=8)
)
json_like = st.recursive(
    json_leaf,
    lambda children: st.one_of(
        st.lists(children, max_size=3), st.dictionaries(st.text(max_size=5), children, max_size=3)
    ),
    max_leaves=8,
)


def _strict_json_ok(value):
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError):
        return False
    return True


@PROPERTY_SETTINGS
@given(
    operations=st.lists(
        st.tuples(
            st.sampled_from(["metric", "gate"]), st.one_of(any_float, not_quite_numbers), json_like
        ),
        min_size=1,
        max_size=6,
    )
)
def test_rejected_payloads_never_change_ledger_state(operations):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "events.jsonl"
        ledger = Ledger(path)
        for kind, value, tag in operations:
            before = (
                ledger._prev_hash,
                len(ledger._events),
                path.read_bytes() if path.exists() else b"",
            )
            try:
                if kind == "metric":
                    ledger.metric("m", value, tag=tag)
                else:
                    ledger.gate("g", passed=value, reason=None)
                accepted = True
            except ValueError:
                accepted = False
            if accepted:
                if kind == "metric":
                    assert _is_finite_real(value) and _strict_json_ok(tag)
                else:
                    assert isinstance(value, bool)
            else:
                after = (
                    ledger._prev_hash,
                    len(ledger._events),
                    path.read_bytes() if path.exists() else b"",
                )
                assert after == before
        assert ledger.verify_chain() is True
        assert verify_chain_from_file(path) is True

        reopened = Ledger(path)
        reopened.metric("after_reopen", 1.0)
        assert reopened.verify_chain() is True
        assert verify_chain_from_file(path) is True


# --- B3 / bootstrap -------------------------------------------------------------


@PROPERTY_SETTINGS
@given(observed=any_float, samples=st.lists(any_float, max_size=5), n_perm=st.integers(-5, 50))
def test_permutation_test_never_returns_a_pvalue(observed, samples, n_perm):
    with pytest.raises(NotImplementedError):
        permutation_test(observed, samples, n_perm=n_perm)


finite = st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False)


@PROPERTY_SETTINGS
@given(
    values=st.lists(finite, min_size=1, max_size=20),
    seed=st.integers(0, 2**32 - 1),
    ci=st.floats(0.01, 0.99),
)
def test_bootstrap_is_reproducible_and_within_data_range(values, seed, ci):
    first = bootstrap_ci(values, n_bootstrap=50, ci=ci, seed=seed)
    assert first == bootstrap_ci(values, n_bootstrap=50, ci=ci, seed=seed)
    lower, upper = first
    tolerance = 1e-9 * max(1.0, max(abs(v) for v in values))
    assert min(values) - tolerance <= lower <= upper <= max(values) + tolerance


@PROPERTY_SETTINGS
@given(values=st.lists(any_float, min_size=1, max_size=10))
def test_bootstrap_rejects_non_finite_data(values):
    if not all(math.isfinite(v) for v in values):
        with pytest.raises(ValueError):
            bootstrap_ci(values, n_bootstrap=10, seed=0)
