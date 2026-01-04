"""
Unit tests for src/core/eci.py
Requires: pytest, numpy
"""

from src.core.eci import bootstrap_ci, compute_eci


def test_compute_eci_basic():
    # likert 7 -> norm 1.0, behavior 1.0, physio 1.0
    val = compute_eci(1.0, 1.0, 1.0, {"w_likert": 0.5, "w_behavior": 0.3, "w_physio": 0.2})
    assert 0.99 >= val >= 0.99 or (abs(val - 1.0) < 1e-6)


def test_compute_eci_no_physio():
    # physio missing -> redistribution
    val = compute_eci(0.5, 0.5, None, {"w_likert": 0.6, "w_behavior": 0.3, "w_physio": 0.1})
    # redistribution -> weights become 0.666..., 0.333...
    assert abs(val - 0.5) < 1e-6


def test_bootstrap_ci():
    data = [0.1 * i for i in range(1, 11)]
    lower, upper = bootstrap_ci(data, n_bootstrap=200, ci=0.8)
    assert 0.0 <= lower <= upper <= 1.0
