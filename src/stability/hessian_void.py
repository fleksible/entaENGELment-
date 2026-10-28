"""Hessian-basierte Void-Analyse (MOD_16).

Implementiert Stabilitäts-Klassifizierung via Hessian-Eigenwertanalyse:
- STABLE: alle λ > 0 (Minimum, sicher)
- FLAT: λ ≈ 0 und kein λ < 0 (VOID, Consent erforderlich)
- UNSTABLE: mindestens ein λ < 0 (Sattel/Maximum, blockieren), auch wenn
  zusätzlich flache Richtungen vorliegen
"""

import numbers
from collections.abc import Callable

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

    result: np.ndarray = (H + H.T) / 2  # Symmetrisierung
    return result


def _validated_hessian(hessian: np.ndarray) -> np.ndarray:
    """Prüft die Matrix kontrolliert; ungültige Eingaben lösen ``ValueError`` aus.

    ``np.linalg.eigvalsh`` liest nur das untere Dreieck. Eine nicht symmetrische
    Matrix würde daher still als eine andere Matrix klassifiziert; sie wird
    stattdessen abgewiesen.
    """
    try:
        matrix: np.ndarray = np.asarray(hessian, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"hessian is not numeric: {exc}") from exc
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError(f"hessian must be a non-empty square matrix, got shape {matrix.shape}")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("hessian contains NaN or infinite entries")
    scale = float(np.max(np.abs(matrix)))
    if float(np.max(np.abs(matrix - matrix.T))) > 1e-10 * scale:
        raise ValueError("hessian is not symmetric")
    return matrix


def classify_stability(hessian: np.ndarray, threshold: float = 1e-6) -> tuple[str, np.ndarray]:
    """Klassifiziert Stabilitätstyp via Hessian-Eigenwerte.

    Eigenwerte mit ``|λ| <= threshold`` gelten als numerisch null (flach).
    Negative Krümmung (``λ < -threshold``) hat Vorrang vor flachen Richtungen:
    ein degenerierter Sattel wie ``[-1, 0]`` ist UNSTABLE, nicht FLAT.

    Args:
        hessian: Symmetrische Hessian-Matrix
        threshold: Numerische Toleranz für Null-Erkennung (endlich, >= 0)

    Returns:
        Tuple (status, eigenvalues) wobei status in {'STABLE', 'FLAT', 'UNSTABLE'}

    Raises:
        ValueError: Bei nicht quadratischer, nicht endlicher oder nicht
            symmetrischer Matrix oder ungültiger Toleranz.
    """
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, numbers.Real)
        or not np.isfinite(threshold)
        or threshold < 0
    ):
        raise ValueError(f"threshold must be a finite number >= 0, got {threshold!r}")
    eigvals = np.linalg.eigvalsh(_validated_hessian(hessian))

    if np.any(eigvals < -threshold):
        return "UNSTABLE", eigvals  # negative Richtung, auch neben flachen
    if np.any(np.abs(eigvals) <= threshold):
        return "FLAT", eigvals  # VOID: flache Richtung
    return "STABLE", eigvals


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
    return float((a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2)
