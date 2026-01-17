"""
src/stability/stability_guard.py

MOD_18 -> MOD_14 Integration.
Maps spectral taxonomy to gate decisions with normalized reason codes.

Ledger Integration:
- Optional ledger parameter for audit logging
- Span wrapper for decision context
- Gate events: stability_taxonomy_v1 with pass/fail reason

Strict-Mode:
- When strict=True and decision is BLOCK, raises StabilityBlockedError
- Exception metric logged to ledger
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .spectral_void import SpectralVoidClass

if TYPE_CHECKING:
    from src.core.ledger import Ledger


class StabilityBlockedError(Exception):
    """Raised when stability check blocks in strict mode."""

    pass


def map_taxonomy_to_gate(
    void_class: SpectralVoidClass,
    has_consent: bool,
    ledger: Ledger | None = None,
    gate_id: str = "stability_taxonomy_v1",
    strict: bool = False,
) -> tuple[str, str]:
    """
    MOD_18 -> MOD_14 Integration.

    Maps spectral taxonomy classification to gate decision with optional
    ledger integration and strict-mode enforcement.

    Args:
        void_class: The spectral taxonomy classification
        has_consent: Whether explicit consent is present
        ledger: Optional Ledger instance for audit logging
        gate_id: Gate identifier for ledger events
        strict: If True, raises StabilityBlockedError on BLOCK decision

    Returns:
        Tuple of (Decision, ReasonCode) for auditing

    Raises:
        StabilityBlockedError: If strict=True and decision is BLOCK
    """

    def _evaluate() -> tuple[str, str]:
        """Internal evaluation logic."""
        # SAFE ZONES
        if void_class == SpectralVoidClass.BASIN:
            return "ALLOW", "SAFE_BASIN_ROBUST"

        if void_class == SpectralVoidClass.SOFT_BASIN:
            # Allowed but logged as warning
            return "ALLOW", "WARN_BASIN_SOFT"

        # CONSENT ZONES (The Void)
        if void_class == SpectralVoidClass.FLAT_VOID:
            if has_consent:
                return "ALLOW", "AUTH_CONSENT_FLAT_VOID"
            return "BLOCK", "BLOCK_NEED_CONSENT_FLAT_VOID"

        # DANGER ZONES (Saddles)
        if void_class in [SpectralVoidClass.RIDGE_SADDLE, SpectralVoidClass.MULTI_SADDLE]:
            return "BLOCK", "BLOCK_UNSTABLE_SADDLE"

        if void_class == SpectralVoidClass.DEGENERATE_SADDLE:
            return "BLOCK", "BLOCK_UNSTABLE_DEGENERATE"

        if void_class == SpectralVoidClass.INVERTED_MAX:
            return "BLOCK", "BLOCK_UNSTABLE_INVERSION"

        return "BLOCK", "BLOCK_UNDEFINED_STATE"

    # Execute with span wrapper if ledger provided
    if ledger is not None:
        with ledger.span("stability.map_taxonomy_to_gate"):
            decision, reason = _evaluate()

            # Log gate decision
            passed = decision == "ALLOW"
            ledger.gate(gate_id, passed=passed, reason=reason)

            # Strict mode: raise on BLOCK
            if strict and not passed:
                ledger.metric("exception.StabilityBlockedError", 1.0)
                raise StabilityBlockedError(reason)

            return decision, reason
    else:
        decision, reason = _evaluate()

        # Strict mode: raise on BLOCK (even without ledger)
        if strict and decision != "ALLOW":
            raise StabilityBlockedError(reason)

        return decision, reason
