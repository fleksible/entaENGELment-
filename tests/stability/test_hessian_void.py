"""Tests für Hessian-basierte Void-Analyse (MOD_16).

Testet die drei fundamentalen Stabilitäts-Zustände:
- STABLE: Minimum (alle Eigenwerte positiv)
- FLAT: VOID (mindestens ein Eigenwert ≈ 0)
- UNSTABLE: Sattel (mindestens ein Eigenwert negativ)
"""

import numpy as np

from src.stability.hessian_void import (
    classify_stability,
    compute_hessian_numerical,
    detect_void_type,
)


def test_stable_minimum():
    """Test: Quadratisches Minimum → STABLE."""

    def quadratic(x):
        return x[0] ** 2 + x[1] ** 2  # Minimum bei (0,0)

    H = compute_hessian_numerical(quadratic, np.array([0.0, 0.0]))
    status, eigvals = classify_stability(H)

    assert status == "STABLE"
    assert np.all(eigvals > 0)
    assert detect_void_type(H) == "stable"


def test_flat_direction_void():
    """Test: Flache Richtung → FLAT (VOID).

    f(x,y) = x² hat Hessian [[2, 0], [0, 0]].
    Der Eigenwert 0 in y-Richtung ist der VOID.
    """

    def flat_func(x):
        return x[0] ** 2  # Flach in y-Richtung

    H = compute_hessian_numerical(flat_func, np.array([0.0, 0.0]))
    status, eigvals = classify_stability(H)

    assert status == "FLAT"
    assert np.any(np.abs(eigvals) < 1e-4)
    assert detect_void_type(H) == "flat"


def test_saddle_unstable():
    """Test: Sattelpunkt → UNSTABLE.

    f(x,y) = x² - y² hat Hessian [[2, 0], [0, -2]].
    Negative Eigenwerte → instabil.
    """

    def saddle(x):
        return x[0] ** 2 - x[1] ** 2  # Sattel bei (0,0)

    H = compute_hessian_numerical(saddle, np.array([0.0, 0.0]))
    status, eigvals = classify_stability(H)

    assert status == "UNSTABLE"
    assert np.any(eigvals < 0)
    assert detect_void_type(H) == "unstable"


def test_hessian_symmetry():
    """Test: Hessian muss symmetrisch sein."""

    def mixed_func(x):
        return x[0] ** 2 + 2 * x[0] * x[1] + 3 * x[1] ** 2

    H = compute_hessian_numerical(mixed_func, np.array([1.0, 1.0]))

    assert np.allclose(H, H.T), "Hessian muss symmetrisch sein"


def test_eigenvalue_ordering():
    """Test: Eigenwerte sind aufsteigend sortiert (np.linalg.eigvalsh)."""

    def anisotropic(x):
        return x[0] ** 2 + 10 * x[1] ** 2  # Unterschiedliche Krümmungen

    H = compute_hessian_numerical(anisotropic, np.array([0.0, 0.0]))
    _, eigvals = classify_stability(H)

    assert eigvals[0] <= eigvals[1], "Eigenwerte sollten sortiert sein"
