"""
tests/ethics/test_stability_negative_priority.py

Fail-closed regression tests for finding B2.

Negative curvature takes precedence over flat directions: a degenerate saddle
such as eigenvalues [-1, 0] or [-5, 0] must block even with consent, in the core
path (MOD_16 -> stability_gate) and in the MOD_18 path (spectral taxonomy ->
map_taxonomy_to_gate). The two taxonomies stay distinct; only their blocking
decisions are compared, under the same zero tolerance.
"""

import itertools

import numpy as np
import pytest

from src.core.stability_guard import check_stability_safe, requires_consent, stability_gate
from src.stability.hessian_void import classify_stability
from src.stability.spectral_void import SpectralVoidClass, classify_spectral_void
from src.stability.stability_guard import map_taxonomy_to_gate


@pytest.mark.parametrize("eigvals", [[-1.0, 0.0], [-5.0, 0.0], [0.0, -1.0], [-1.0, 0.0, 2.0]])
@pytest.mark.parametrize("consent", [False, True])
def test_degenerate_saddle_blocks_even_with_consent(eigvals, consent):
    H = np.diag(eigvals)

    status, _ = classify_stability(H)
    assert status == "UNSTABLE"
    allow, reason = stability_gate(H, consent_available=consent)
    assert allow is False
    assert reason.startswith("UNSTABLE")

    void_class = classify_spectral_void(eigvals)
    assert void_class == SpectralVoidClass.DEGENERATE_SADDLE
    decision, _ = map_taxonomy_to_gate(void_class, has_consent=consent)
    assert decision == "BLOCK"


def test_rotated_degenerate_saddle_blocks_with_consent():
    """Same spectrum in a non-diagonal basis (rotation by 30 degrees)."""
    theta = np.pi / 6
    Q = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    H = Q @ np.diag([-1.0, 0.0]) @ Q.T
    H = (H + H.T) / 2
    assert stability_gate(H, consent_available=True)[0] is False


def test_pure_flat_still_requires_consent():
    H = np.diag([2.0, 0.0])
    assert classify_stability(H)[0] == "FLAT"
    assert stability_gate(H, consent_available=False)[0] is False
    assert stability_gate(H, consent_available=True)[0] is True
    assert requires_consent(H) is True


@pytest.mark.parametrize("consent", ["false", 1, "yes", None])
def test_truthy_non_bool_consent_is_not_consent(consent):
    H = np.diag([2.0, 0.0])
    assert stability_gate(H, consent_available=consent)[0] is False
    assert map_taxonomy_to_gate(SpectralVoidClass.FLAT_VOID, has_consent=consent)[0] == "BLOCK"


@pytest.mark.parametrize(
    "matrix",
    [
        np.array([[np.nan, 0.0], [0.0, 1.0]]),
        np.array([[np.inf, 0.0], [0.0, 1.0]]),
        np.array([[1.0, 3.0], [0.0, 1.0]]),  # not symmetric
        np.array([1.0, 2.0]),  # not a matrix
        np.ones((2, 3)),  # not square
        np.zeros((0, 0)),  # empty
        [["a", "b"], ["c", "d"]],  # not numeric
    ],
)
@pytest.mark.parametrize("consent", [False, True])
def test_invalid_matrix_is_handled_and_blocks(matrix, consent):
    with pytest.raises(ValueError):
        classify_stability(matrix)
    allow, reason = stability_gate(matrix, consent_available=consent)
    assert allow is False
    assert reason.startswith("INVALID")
    assert check_stability_safe(matrix) is False
    with pytest.raises(ValueError):
        requires_consent(matrix)


def test_non_symmetric_matrix_with_positive_lower_triangle_is_not_stable():
    """eigvalsh reads only the lower triangle; [[1,3],[0,1]] would look STABLE."""
    H = np.array([[1.0, 3.0], [0.0, 1.0]])
    assert stability_gate(H, consent_available=True)[0] is False


@pytest.mark.parametrize("threshold", [-1.0, float("nan"), float("inf"), True, "1e-6", None])
def test_invalid_threshold_is_rejected(threshold):
    with pytest.raises(ValueError):
        classify_stability(np.eye(2), threshold=threshold)


TOL = 1e-6
VALUES = [-2.0, -1.0, -10 * TOL, -TOL, -TOL / 2, 0.0, TOL / 2, TOL, 10 * TOL, 0.5, 2.0]


@pytest.mark.parametrize("consent", [False, True])
def test_core_and_mod18_agree_on_blocking_under_same_tolerance(consent):
    """Blocking decisions agree; taxonomies are not equated."""
    for pair in itertools.product(VALUES, repeat=2):
        eigvals = np.array(pair)
        core_allow, _ = stability_gate(np.diag(eigvals), consent_available=consent)
        mod18_decision, _ = map_taxonomy_to_gate(
            classify_spectral_void(eigvals, eps=TOL), has_consent=consent
        )
        assert core_allow == (mod18_decision == "ALLOW"), (pair, consent)
        if any(v < -TOL for v in pair):
            assert core_allow is False
