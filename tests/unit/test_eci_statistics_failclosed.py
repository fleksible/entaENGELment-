"""
tests/unit/test_eci_statistics_failclosed.py

Regression tests for finding B3 and the bootstrap helper in src/core/eci.py.

B3: ``permutation_test`` is disabled until a test design is specified; it must
not return any p-value. ``bootstrap_ci`` keeps the percentile method, is
reproducible with a seed and rejects invalid input instead of returning a
seemingly valid interval.
"""

import math

import numpy as np
import pytest

from src.core.eci import bootstrap_ci, permutation_test


@pytest.mark.parametrize(
    "observed,samples",
    [(0.49, [0.1, 0.5, 0.9, 0.3, 0.7]), (0.51, [0.1, 0.5, 0.9, 0.3, 0.7]), (0.0, [])],
)
def test_permutation_test_produces_no_pvalue(observed, samples):
    with pytest.raises(NotImplementedError, match="null hypothesis and test design"):
        permutation_test(observed, samples, n_perm=99)


def test_permutation_test_does_not_touch_global_rng():
    np.random.seed(123)
    expected = np.random.random()
    np.random.seed(123)
    with pytest.raises(NotImplementedError):
        permutation_test(0.5, [0.1, 0.9])
    assert np.random.random() == expected


def test_bootstrap_ci_is_reproducible_with_seed():
    data = [0.1 * i for i in range(1, 11)]
    first = bootstrap_ci(data, n_bootstrap=500, ci=0.9, seed=7)
    second = bootstrap_ci(data, n_bootstrap=500, ci=0.9, seed=7)
    assert first == second
    lower, upper = first
    assert min(data) <= lower <= upper <= max(data)


def test_bootstrap_ci_does_not_use_global_rng():
    data = [0.1 * i for i in range(1, 11)]
    np.random.seed(0)
    a = bootstrap_ci(data, n_bootstrap=200, seed=3)
    np.random.seed(999)
    b = bootstrap_ci(data, n_bootstrap=200, seed=3)
    assert a == b


def test_bootstrap_ci_constant_data_gives_degenerate_interval():
    assert bootstrap_ci([0.5] * 10, n_bootstrap=100, seed=1) == (0.5, 0.5)


@pytest.mark.parametrize(
    "values",
    [
        [],
        [math.nan, 0.5],
        [math.inf, 0.5],
        [-math.inf],
        [[0.1, 0.2], [0.3, 0.4]],
        ["a", "b"],
    ],
)
def test_bootstrap_ci_rejects_invalid_data(values):
    with pytest.raises(ValueError):
        bootstrap_ci(values, n_bootstrap=10)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_bootstrap": 0},
        {"n_bootstrap": -5},
        {"n_bootstrap": 10.5},
        {"n_bootstrap": True},
        {"ci": 0.0},
        {"ci": 1.0},
        {"ci": 1.5},
        {"ci": -0.1},
        {"ci": math.nan},
        {"ci": True},
        {"seed": 1.5},
        {"seed": "7"},
        {"seed": True},
    ],
)
def test_bootstrap_ci_rejects_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        bootstrap_ci([0.1, 0.2, 0.3], **kwargs)
