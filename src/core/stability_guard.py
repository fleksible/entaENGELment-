"""Stability-basierte Safety-Guards (MOD_14 ← MOD_16).

Implementiert Fail-Safe-Logik basierend auf Hessian-Stabilität:
- STABLE → Proceed
- FLAT (VOID) → Consent erforderlich
- UNSTABLE → Block (auch mit Consent; negative Krümmung hat Vorrang vor flachen Richtungen)
- ungültige Matrix → Block (auch mit Consent)

STABLE bezeugt nur eine geometrische Klassifikation der übergebenen Matrix
unter der Toleranz von ``classify_stability``; es ist keine Einwilligung.
"""

import numpy as np

from src.stability.hessian_void import classify_stability


def stability_gate(hessian: np.ndarray, consent_available: bool = False) -> tuple[bool, str]:
    """Safety-Gate basierend auf Hessian-Stabilität.

    Args:
        hessian: Symmetrische Hessian-Matrix
        consent_available: Ob expliziter Consent vorliegt

    Returns:
        Tuple (allow, reason) - ob Aktion erlaubt und Begründung
    """
    try:
        status, eigvals = classify_stability(hessian)
    except ValueError as exc:
        # Ungültige Eingabe: kontrolliert blockieren, auch mit Consent.
        return False, f"INVALID: {exc}"

    if status == "STABLE":
        return True, f"STABLE: All eigenvalues positive (min={eigvals.min():.2e})"

    elif status == "FLAT":
        # Nur ein explizites bool True zählt als Consent (kein truthy Ersatz).
        if consent_available is True:
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
        True nur wenn STABLE (False auch bei ungültiger Matrix)
    """
    try:
        status, _ = classify_stability(hessian)
    except ValueError:
        return False
    return status == "STABLE"


def requires_consent(hessian: np.ndarray) -> bool:
    """Prüft ob VOID-Zustand vorliegt (Consent nötig).

    Args:
        hessian: Symmetrische Hessian-Matrix

    Returns:
        True wenn FLAT (VOID) Status

    Raises:
        ValueError: Bei ungültiger Matrix (die Frage ist dann nicht beantwortbar).
    """
    status, _ = classify_stability(hessian)
    return status == "FLAT"
