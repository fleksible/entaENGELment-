"""
tests/unit/test_stability_strict.py

Strict-Mode Safety Tests for Stability Guard.

Tests that strict mode:
1. Raises StabilityBlockedError when decision is BLOCK
2. Ledger contains gate event with passed=False and correct reason
3. Ledger contains exception metric
"""

import pytest

from src.core.ledger import Ledger
from src.stability.spectral_void import SpectralVoidClass
from src.stability.stability_guard import StabilityBlockedError, map_taxonomy_to_gate


class TestStabilityStrictMode:
    """Tests for Stability Guard strict mode enforcement."""

    def test_strict_mode_raises_on_flat_void_without_consent(self):
        """Strict mode raises StabilityBlockedError for FLAT_VOID without consent."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.FLAT_VOID,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_NEED_CONSENT_FLAT_VOID" in str(exc_info.value)

        # Verify ledger contains gate fail event
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1
        assert gate_events[0]["payload"]["gate_id"] == "stability_taxonomy_v1"
        assert gate_events[0]["payload"]["passed"] is False
        assert gate_events[0]["payload"]["reason"] == "BLOCK_NEED_CONSENT_FLAT_VOID"

        # Verify ledger contains exception metric
        metric_events = ledger.get_events("metric")
        exception_metrics = [
            e
            for e in metric_events
            if e["payload"]["metric_id"] == "exception.StabilityBlockedError"
        ]
        assert len(exception_metrics) == 1
        assert exception_metrics[0]["payload"]["value"] == 1.0

    def test_strict_mode_raises_on_ridge_saddle(self):
        """Strict mode raises StabilityBlockedError for RIDGE_SADDLE."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.RIDGE_SADDLE,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_UNSTABLE_SADDLE" in str(exc_info.value)

        gate_events = ledger.get_events("gate")
        assert gate_events[0]["payload"]["reason"] == "BLOCK_UNSTABLE_SADDLE"

    def test_strict_mode_raises_on_multi_saddle(self):
        """Strict mode raises StabilityBlockedError for MULTI_SADDLE."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.MULTI_SADDLE,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_UNSTABLE_SADDLE" in str(exc_info.value)

    def test_strict_mode_raises_on_degenerate_saddle(self):
        """Strict mode raises StabilityBlockedError for DEGENERATE_SADDLE."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.DEGENERATE_SADDLE,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_UNSTABLE_DEGENERATE" in str(exc_info.value)

    def test_strict_mode_raises_on_inverted_max(self):
        """Strict mode raises StabilityBlockedError for INVERTED_MAX."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.INVERTED_MAX,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_UNSTABLE_INVERSION" in str(exc_info.value)

    def test_strict_mode_raises_on_undefined(self):
        """Strict mode raises StabilityBlockedError for UNDEFINED."""
        ledger = Ledger()

        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.UNDEFINED,
                has_consent=False,
                ledger=ledger,
                strict=True,
            )

        assert "BLOCK_UNDEFINED_STATE" in str(exc_info.value)

    def test_non_strict_mode_returns_block_without_exception(self):
        """Non-strict mode returns BLOCK without raising exception."""
        ledger = Ledger()

        decision, reason = map_taxonomy_to_gate(
            void_class=SpectralVoidClass.FLAT_VOID,
            has_consent=False,
            ledger=ledger,
            strict=False,
        )

        assert decision == "BLOCK"
        assert reason == "BLOCK_NEED_CONSENT_FLAT_VOID"

        # Gate event should still be logged
        gate_events = ledger.get_events("gate")
        assert len(gate_events) == 1
        assert gate_events[0]["payload"]["passed"] is False

        # No exception metric should be logged
        metric_events = ledger.get_events("metric")
        exception_metrics = [
            e
            for e in metric_events
            if e["payload"]["metric_id"] == "exception.StabilityBlockedError"
        ]
        assert len(exception_metrics) == 0

    def test_strict_mode_allows_basin(self):
        """Strict mode returns ALLOW for BASIN."""
        ledger = Ledger()

        decision, reason = map_taxonomy_to_gate(
            void_class=SpectralVoidClass.BASIN,
            has_consent=False,
            ledger=ledger,
            strict=True,
        )

        assert decision == "ALLOW"
        assert reason == "SAFE_BASIN_ROBUST"

        gate_events = ledger.get_events("gate")
        assert gate_events[0]["payload"]["passed"] is True

    def test_strict_mode_allows_soft_basin(self):
        """Strict mode returns ALLOW for SOFT_BASIN (with warning)."""
        ledger = Ledger()

        decision, reason = map_taxonomy_to_gate(
            void_class=SpectralVoidClass.SOFT_BASIN,
            has_consent=False,
            ledger=ledger,
            strict=True,
        )

        assert decision == "ALLOW"
        assert reason == "WARN_BASIN_SOFT"

    def test_strict_mode_allows_flat_void_with_consent(self):
        """Strict mode returns ALLOW for FLAT_VOID with consent."""
        ledger = Ledger()

        decision, reason = map_taxonomy_to_gate(
            void_class=SpectralVoidClass.FLAT_VOID,
            has_consent=True,
            ledger=ledger,
            strict=True,
        )

        assert decision == "ALLOW"
        assert reason == "AUTH_CONSENT_FLAT_VOID"

        gate_events = ledger.get_events("gate")
        assert gate_events[0]["payload"]["passed"] is True

    def test_span_wrapper_creates_span_events(self):
        """Verify span wrapper creates span_start and span_end events."""
        ledger = Ledger()

        map_taxonomy_to_gate(
            void_class=SpectralVoidClass.BASIN,
            has_consent=False,
            ledger=ledger,
            strict=False,
        )

        # Check for span events
        span_start_events = ledger.get_events("span_start")
        span_end_events = ledger.get_events("span_end")

        assert len(span_start_events) == 1
        assert span_start_events[0]["payload"]["name"] == "stability.map_taxonomy_to_gate"

        assert len(span_end_events) == 1
        assert span_end_events[0]["payload"]["name"] == "stability.map_taxonomy_to_gate"

    def test_gate_event_has_span_id(self):
        """Gate event should have span_id from the wrapping span."""
        ledger = Ledger()

        map_taxonomy_to_gate(
            void_class=SpectralVoidClass.BASIN,
            has_consent=False,
            ledger=ledger,
            strict=False,
        )

        gate_events = ledger.get_events("gate")
        span_start_events = ledger.get_events("span_start")

        # Gate event should have span_id matching the span
        assert len(gate_events) == 1
        assert "span_id" in gate_events[0]
        assert gate_events[0]["span_id"] == span_start_events[0]["payload"]["span_id"]

    def test_ledger_hash_chain_integrity(self):
        """Verify ledger hash chain is valid after stability operations."""
        ledger = Ledger()

        map_taxonomy_to_gate(
            void_class=SpectralVoidClass.BASIN,
            has_consent=False,
            ledger=ledger,
            strict=False,
        )

        assert ledger.verify_chain() is True

    def test_strict_mode_works_without_ledger(self):
        """Strict mode works even without a ledger."""
        with pytest.raises(StabilityBlockedError) as exc_info:
            map_taxonomy_to_gate(
                void_class=SpectralVoidClass.FLAT_VOID,
                has_consent=False,
                ledger=None,
                strict=True,
            )

        assert "BLOCK_NEED_CONSENT_FLAT_VOID" in str(exc_info.value)
