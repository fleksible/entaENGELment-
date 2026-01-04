"""Hessian-basierte Void-Analyse (MOD_16).

Implementiert Stabilitäts-Klassifizierung via Hessian-Eigenwertanalyse:
- STABLE: alle λ > 0 (Minimum, sicher)
- FLAT: λ ≈ 0 (VOID, Consent erforderlich)
- UNSTABLE: λ < 0 (Sattel/Maximum, blockieren)
"""

from typing import Callable

import numpy as np


def compute_hessian_numerical(
    func: Callable[[np.ndarray], float], point: np.ndarray, eps: float = 1e-5
) -> np.ndarray:
    """Numerische Hessian-Approximation via finite Differenzen.

    Args:
        func: Skalare Funktion f: R^n -> R
        point: Punkt an dem Hessian berechnet wird
        eps: Schrittweite für finite Differenzen

    Returns:
        Symmetrische Hessian-Matrix H_ij = d²f/dx_i dx_j
    """
    n = len(point)
    H = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            e_i = np.zeros(n)
            e_j = np.zeros(n)
            e_i[i] = eps
            e_j[j] = eps

            f_pp = func(point + e_i + e_j)
            f_p0 = func(point + e_i)
            f_0p = func(point + e_j)
            f_00 = func(point)

            H[i, j] = (f_pp - f_p0 - f_0p + f_00) / (eps * eps)

    return (H + H.T) / 2  # Symmetrisierung


def classify_stability(hessian: np.ndarray, threshold: float = 1e-6) -> tuple[str, np.ndarray]:
    """Klassifiziert Stabilitätstyp via Hessian-Eigenwerte.

    Args:
        hessian: Symmetrische Hessian-Matrix
        threshold: Numerische Toleranz für Null-Erkennung

    Returns:
        Tuple (status, eigenvalues) wobei status in {'STABLE', 'FLAT', 'UNSTABLE'}
    """
    eigvals = np.linalg.eigvalsh(hessian)

    if np.all(eigvals > threshold):
        return "STABLE", eigvals
    elif np.any(np.abs(eigvals) < threshold):
        return "FLAT", eigvals  # VOID: flache Richtung
    else:
        return "UNSTABLE", eigvals


def detect_void_type(hessian: np.ndarray) -> str:
    """Vereinfachte Void-Typ-Erkennung.

    Args:
        hessian: Symmetrische Hessian-Matrix

    Returns:
        'stable', 'flat', oder 'unstable'
    """
    status, _ = classify_stability(hessian)
    return status.lower()


def rosenbrock(x: np.ndarray, a: float = 1.0, b: float = 100.0) -> float:
    """Rosenbrock-Funktion: (a-x)² + b(y-x²)².

    Standard-Testfunktion mit globalem Minimum bei (a, a²).
    """
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2
