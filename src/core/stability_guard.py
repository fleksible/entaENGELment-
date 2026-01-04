"""Stability-basierte Safety-Guards (MOD_14 ← MOD_16).

Implementiert Fail-Safe-Logik basierend auf Hessian-Stabilität:
- STABLE → Proceed
- FLAT (VOID) → Consent erforderlich
- UNSTABLE → Block
"""

from typing import Tuple
import numpy as np

from src.stability.hessian_void import classify_stability


def stability_gate(
    hessian: np.ndarray,
    consent_available: bool = False
) -> Tuple[bool, str]:
    """Safety-Gate basierend auf Hessian-Stabilität.

    Args:
        hessian: Symmetrische Hessian-Matrix
        consent_available: Ob expliziter Consent vorliegt

    Returns:
        Tuple (allow, reason) - ob Aktion erlaubt und Begründung
    """
    status, eigvals = classify_stability(hessian)

    if status == 'STABLE':
        return True, f"STABLE: All eigenvalues positive (min={eigvals.min():.2e})"

    elif status == 'FLAT':
        if consent_available:
            return True, "FLAT: Proceeding with explicit consent (VOID acknowledged)"
        else:
            return False, "FLAT: VOID detected, consent required before proceeding"

    else:  # UNSTABLE
        return False, f"UNSTABLE: Negative eigenvalues detected (min={eigvals.min():.2e})"


def check_stability_safe(hessian: np.ndarray) -> bool:
    """Schnellcheck: Ist der Zustand sicher (STABLE)?

    Args:
        hessian: Symmetrische Hessian-Matrix

    Returns:
        True nur wenn STABLE
    """
    status, _ = classify_stability(hessian)
    return status == 'STABLE'


def requires_consent(hessian: np.ndarray) -> bool:
    """Prüft ob VOID-Zustand vorliegt (Consent nötig).

    Args:
        hessian: Symmetrische Hessian-Matrix

    Returns:
        True wenn FLAT (VOID) Status
    """
    status, _ = classify_stability(hessian)
    return status == 'FLAT'
