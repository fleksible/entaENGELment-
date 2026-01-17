"""Tests für Stability Guards (MOD_14 ← MOD_16).

Testet Governance-Integration: FLAT erfordert Consent.
"""

import numpy as np

from src.core.stability_guard import (
    check_stability_safe,
    requires_consent,
    stability_gate,
)


def test_stable_allows_proceed():
    """STABLE-Status erlaubt Fortfahren ohne Consent."""
    stable_hessian = np.array([[2.0, 0.0], [0.0, 2.0]])

    allow, reason = stability_gate(stable_hessian, consent_available=False)

    assert allow is True
    assert "STABLE" in reason


def test_flat_requires_consent():
    """FLAT-Status blockiert ohne Consent (Fail-Safe)."""
    flat_hessian = np.array([[1.0, 0.0], [0.0, 1e-8]])

    allow, reason = stability_gate(flat_hessian, consent_available=False)
    assert allow is False
    assert "consent required" in reason.lower()

    # Mit Consent erlaubt
    allow, reason = stability_gate(flat_hessian, consent_available=True)
    assert allow is True
    assert "consent" in reason.lower()


def test_unstable_always_blocks():
    """UNSTABLE-Status blockiert immer (auch mit Consent)."""
    unstable_hessian = np.array([[1.0, 0.0], [0.0, -1.0]])

    allow, reason = stability_gate(unstable_hessian, consent_available=False)
    assert allow is False
    assert "UNSTABLE" in reason

    # Auch mit Consent blockiert
    allow, reason = stability_gate(unstable_hessian, consent_available=True)
    assert allow is False


def test_check_stability_safe():
    """Schnellcheck-Funktion."""
    stable = np.array([[2.0, 0.0], [0.0, 2.0]])
    flat = np.array([[2.0, 0.0], [0.0, 0.0]])
    unstable = np.array([[2.0, 0.0], [0.0, -2.0]])

    assert check_stability_safe(stable) is True
    assert check_stability_safe(flat) is False
    assert check_stability_safe(unstable) is False


def test_requires_consent():
    """VOID-Erkennung für Consent-Anforderung."""
    stable = np.array([[2.0, 0.0], [0.0, 2.0]])
    flat = np.array([[2.0, 0.0], [0.0, 0.0]])
    unstable = np.array([[2.0, 0.0], [0.0, -2.0]])

    assert requires_consent(stable) is False
    assert requires_consent(flat) is True
    assert requires_consent(unstable) is False
