"""
tests/unit/test_gate_strict.py

Strict-Mode Safety Tests for MZM Gate.

Tests that strict mode:
1. Raises GateBlockedError when gate fails
2. Ledger contains gate event with passed=False and correct reason
3. Ledger contains exception metric
"""

import pytest

from src.core.ledger import Ledger
from tools.mzm.gate_toggle import Context, GateBlockedError, gate_open, load_policy


class TestGateStrictMode:
    """Tests for MZM Gate strict mode enforcement."""

    def test_strict_mode_raises_on_phi_below_min(self):
        """Strict mode raises GateBlockedError when phi is below policy minimum."""
        # Load actual policy to avoid drift
        policy = load_policy()
        phi_min = policy["constraints"]["phi_min"]

        # Create context with phi below minimum
        ctx = Context(
            phi=phi_min - 0.1,  # Below minimum
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        # Create in-memory ledger
        ledger = Ledger()

        # Should raise GateBlockedError in strict mode
        with pytest.raises(GateBlockedError) as exc_info:
            gate_open(ctx, policy, ledger=ledger, strict=True)

        assert "BLOCK_PHI_BELOW_MIN" in str(exc_info.value)

        # Verify ledger contains gate fail event
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1
        assert gate_events[0]["payload"]["gate_id"] == "mzm_gate_v1"
        assert gate_events[0]["payload"]["passed"] is False
        assert gate_events[0]["payload"]["reason"] == "BLOCK_PHI_BELOW_MIN"

        # Verify ledger contains exception metric
        metric_events = ledger.get_events("metric")
        exception_metrics = [
            e for e in metric_events if e["payload"]["metric_id"] == "exception.GateBlockedError"
        ]
        assert len(exception_metrics) == 1
        assert exception_metrics[0]["payload"]["value"] == 1.0

    def test_strict_mode_raises_on_rcc_ec_failed(self):
        """Strict mode raises GateBlockedError when RCC:EC is not fulfilled."""
        policy = load_policy()

        ctx = Context(
            phi=1.0,  # Above minimum
            rcc_ec=False,  # RCC:EC failed
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        ledger = Ledger()

        with pytest.raises(GateBlockedError) as exc_info:
            gate_open(ctx, policy, ledger=ledger, strict=True)

        assert "BLOCK_RCC_EC_FAILED" in str(exc_info.value)

        gate_events = ledger.get_events("gate")
        assert gate_events[0]["payload"]["reason"] == "BLOCK_RCC_EC_FAILED"

    def test_strict_mode_raises_on_m_norm_invalid(self):
        """Strict mode raises GateBlockedError when M norm is invalid."""
        policy = load_policy()

        ctx = Context(
            phi=1.0,
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=0.5,  # Invalid (should be 1.0)
            psi_lock=True,
        )

        ledger = Ledger()

        with pytest.raises(GateBlockedError) as exc_info:
            gate_open(ctx, policy, ledger=ledger, strict=True)

        assert "BLOCK_M_NORM_INVALID" in str(exc_info.value)

    def test_strict_mode_raises_on_psi_lock_missing(self):
        """Strict mode raises GateBlockedError when psi_lock is missing."""
        policy = load_policy()

        ctx = Context(
            phi=1.0,
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=False,  # Lock missing
        )

        ledger = Ledger()

        with pytest.raises(GateBlockedError) as exc_info:
            gate_open(ctx, policy, ledger=ledger, strict=True)

        assert "BLOCK_PSI_LOCK_MISSING" in str(exc_info.value)

    def test_non_strict_mode_returns_false_without_exception(self):
        """Non-strict mode returns False without raising exception."""
        policy = load_policy()
        phi_min = policy["constraints"]["phi_min"]

        ctx = Context(
            phi=phi_min - 0.1,  # Below minimum
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        ledger = Ledger()

        # Should NOT raise, just return False
        result = gate_open(ctx, policy, ledger=ledger, strict=False)
        assert result is False

        # Gate event should still be logged
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1
        assert gate_events[0]["payload"]["passed"] is False

        # No exception metric should be logged
        metric_events = ledger.get_events("metric")
        exception_metrics = [
            e for e in metric_events if e["payload"]["metric_id"] == "exception.GateBlockedError"
        ]
        assert len(exception_metrics) == 0

    def test_strict_mode_passes_when_all_constraints_met(self):
        """Strict mode returns True when all constraints are satisfied."""
        policy = load_policy()

        ctx = Context(
            phi=1.0,  # Above minimum
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        ledger = Ledger()

        result = gate_open(ctx, policy, ledger=ledger, strict=True)
        assert result is True

        # Gate event should show pass
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1
        assert gate_events[0]["payload"]["passed"] is True
        assert gate_events[0]["payload"]["reason"] == "PASS_ALL_CONSTRAINTS"

    def test_ledger_metrics_are_logged(self):
        """Ledger contains phi and m_norm_l2 metrics."""
        policy = load_policy()

        ctx = Context(
            phi=0.85,
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        ledger = Ledger()
        gate_open(ctx, policy, ledger=ledger, strict=False)

        metric_events = ledger.get_events("metric")
        phi_metrics = [e for e in metric_events if e["payload"]["metric_id"] == "mzm.phi"]
        m_norm_metrics = [e for e in metric_events if e["payload"]["metric_id"] == "mzm.m_norm_l2"]

        assert len(phi_metrics) == 1
        assert phi_metrics[0]["payload"]["value"] == 0.85

        assert len(m_norm_metrics) == 1
        assert m_norm_metrics[0]["payload"]["value"] == 1.0

    def test_ledger_hash_chain_integrity(self):
        """Verify ledger hash chain is valid after gate operations."""
        policy = load_policy()

        ctx = Context(
            phi=0.85,
            rcc_ec=True,
            non_overlap=True,
            m_norm_l2=1.0,
            psi_lock=True,
        )

        ledger = Ledger()
        gate_open(ctx, policy, ledger=ledger, strict=False)

        # Verify hash chain integrity
        assert ledger.verify_chain() is True
