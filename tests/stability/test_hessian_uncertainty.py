"""Tests für die Unsicherheit numerisch geschätzter Hessians (B9/V11).

Abgedeckt: Fehlerschranke aus deklarierten Annahmen, Behandlung fehlender
Unsicherheitsinformation, abgeleitete Matrizen, der verbleibende
Matrix-only-Zugang, das Gegenbeispiel zur Richardson-"Zertifizierung",
MOD_18-Unsicherheit, Rotationsinvarianz und Eingabevalidierung.
"""

from fractions import Fraction

import numpy as np
import pytest

from src.core.stability_guard import stability_gate
from src.stability.hessian_void import (
    EstimatedHessian,
    classify_stability,
    compute_hessian_numerical,
    eigenvalue_bounds,
)
from src.stability.spectral_void import (
    SpectralVoidClass,
    classify_hessian_spectral_void,
    classify_spectral_void,
)

EPS_MACH = float(np.finfo(float).eps)


def counterexample(t):
    """f(t) = -t² + 10t⁴ - 8t⁶, f''(0) = -2, f⁽⁴⁾(t) = 240 - 2880t²."""
    x = t[0]
    return -(x**2) + 10 * x**4 - 8 * x**6


class TestCounterexample:
    def test_two_agreeing_step_sizes_give_the_wrong_sign(self):
        """h=1 and h=0.5 both give +2, but f''(0) = -2: agreement is no certificate."""
        H = compute_hessian_numerical(counterexample, np.array([0.0]), eps=0.5)
        assert np.asarray(H)[0, 0] == pytest.approx(2.0)
        assert H.richardson_estimate[0, 0] == pytest.approx(0.0, abs=1e-12)

    def test_agreement_alone_does_not_release(self):
        H = compute_hessian_numerical(counterexample, np.array([0.0]), eps=0.5)
        assert classify_stability(H)[0] == "UNRESOLVED"
        assert stability_gate(H, consent_available=True)[0] is False

    def test_valid_declared_bound_with_large_step_stays_unresolved(self):
        # |f⁽⁴⁾| <= 480 on [-0.5, 0.5] -> truncation bound 480·0.25/12 = 10.
        H = compute_hessian_numerical(
            counterexample,
            np.array([0.0]),
            eps=0.5,
            fourth_derivative_bound=480.0,
            evaluation_error=1e-14,
        )
        assert H.error_bound[0, 0] >= 10.0
        assert classify_stability(H)[0] == "UNRESOLVED"

    def test_valid_declared_bound_with_small_step_finds_negative_curvature(self):
        # Automatic step ≈ 1.2e-4; |f⁽⁴⁾| <= 241 on that interval.
        H = compute_hessian_numerical(
            counterexample,
            np.array([0.0]),
            fourth_derivative_bound=241.0,
            evaluation_error=1e-30,
        )
        assert np.asarray(H)[0, 0] == pytest.approx(-2.0, abs=1e-5)
        assert classify_stability(H)[0] == "UNSTABLE"
        assert stability_gate(H, consent_available=True)[0] is False

    def test_documented_limit_false_declarations_are_not_detected(self):
        """Documented limit, not desired behaviour: the bound is only as good as the
        declared assumptions. A false M4 (true max is 480 on [-0.5, 0.5]) yields a
        wrong STABLE. The assumptions are recorded on the estimate."""
        H = compute_hessian_numerical(
            counterexample,
            np.array([0.0]),
            eps=0.5,
            fourth_derivative_bound=1.0,
            evaluation_error=1e-14,
        )
        assert classify_stability(H)[0] == "STABLE"
        assert any("declared" in item for item in H.assumptions)


class TestMissingAndDerivedUncertainty:
    @staticmethod
    def _declared_quadratic():
        return compute_hessian_numerical(
            lambda q: q[0] ** 2 + q[1] ** 2,
            np.array([0.5, -0.25]),
            fourth_derivative_bound=0.0,
            evaluation_error=1e-15,
        )

    def test_declared_estimate_is_classified(self):
        H = self._declared_quadratic()
        assert isinstance(H, EstimatedHessian)
        assert classify_stability(H)[0] == "STABLE"

    @pytest.mark.parametrize(
        "derive",
        [
            lambda H: H * 1.0,
            lambda H: H.copy(),
            lambda H: (H + H.T) / 2,
            lambda H: H[:, :],
            lambda H: H.T,
        ],
    )
    def test_derived_matrices_lose_the_bound_and_block(self, derive):
        D = derive(self._declared_quadratic())
        assert isinstance(D, EstimatedHessian)
        assert D.error_bound is None
        assert classify_stability(D)[0] == "UNRESOLVED"
        assert stability_gate(D, consent_available=True)[0] is False

    def test_only_one_declaration_is_rejected(self):
        with pytest.raises(ValueError, match="together"):
            compute_hessian_numerical(
                lambda q: q[0] ** 2, np.array([0.0]), fourth_derivative_bound=0.0
            )

    def test_tiny_coordinate_without_exact_stencil_has_no_bound(self):
        H = compute_hessian_numerical(
            lambda q: q[0] ** 2 + q[1] ** 2,
            np.array([1e-20, 0.0]),
            fourth_derivative_bound=0.0,
            evaluation_error=1e-15,
        )
        assert H.error_bound is None
        assert classify_stability(H)[0] == "UNRESOLVED"

    def test_documented_matrix_only_access_is_not_protected(self):
        """Remaining matrix-only access: np.asarray drops the estimate mark and the
        matrix is then treated as exact (caller-supplied)."""
        H = compute_hessian_numerical(lambda q: q[0] ** 2 + 1e-8 * q[1] ** 2 + 10, np.ones(2))
        plain = np.asarray(H)
        assert type(plain) is np.ndarray
        assert classify_stability(plain)[0] != "UNRESOLVED"


class TestErrorBound:
    def test_stencil_points_are_exactly_representable_when_bounded(self):
        x = np.array([0.3, -2.2, 1e3])
        H = compute_hessian_numerical(
            lambda q: float(np.sum(q**2)), x, fourth_derivative_bound=0.0, evaluation_error=1e-9
        )
        assert H.error_bound is not None
        for xk, h in zip(x.tolist(), H.steps.tolist(), strict=True):
            assert Fraction(xk + h) == Fraction(xk) + Fraction(h)
            assert Fraction(xk - h) == Fraction(xk) - Fraction(h)

    def test_bound_contains_analytic_hessian(self):
        def f(q):
            return np.sin(q[0]) * np.cos(q[1]) + 0.5 * q[0] * q[1]

        x = np.array([0.4, -0.3])
        H = compute_hessian_numerical(f, x, fourth_derivative_bound=1.0, evaluation_error=1e-15)
        exact = np.array(
            [
                [-np.sin(x[0]) * np.cos(x[1]), -np.cos(x[0]) * np.sin(x[1]) + 0.5],
                [-np.cos(x[0]) * np.sin(x[1]) + 0.5, -np.sin(x[0]) * np.cos(x[1])],
            ]
        )
        assert np.all(np.abs(np.asarray(H) - exact) <= H.error_bound)
        mu, delta = eigenvalue_bounds(H)
        true = np.linalg.eigvalsh(exact)
        assert np.all(np.abs(mu - true) <= delta)

    def test_flat_tolerance_does_not_depend_on_offset_but_uncertainty_may(self):
        def make(offset):
            return compute_hessian_numerical(
                lambda q: q[0] ** 2 + q[1] ** 2 + offset,
                np.array([1.0, 1.0]),
                fourth_derivative_bound=0.0,
                evaluation_error=4 * EPS_MACH * (8.0 + offset),
            )

        small, large = make(0.0), make(1e4)
        assert large.eigenvalue_uncertainty() > small.eigenvalue_uncertainty()
        # Same decision threshold; only the uncertainty band widened.
        assert classify_stability(small, threshold=1e-6)[0] == "STABLE"
        assert classify_stability(large, threshold=1e-6)[0] == "STABLE"


class TestRotationInvariance:
    @staticmethod
    def _rotation(theta):
        return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    @pytest.mark.parametrize(
        "spectrum,expected",
        [
            ([2.0, 1.0], "STABLE"),
            ([2.0, 0.0], "FLAT"),
            ([-1.0, 0.0], "UNSTABLE"),
            ([3, -2], "UNSTABLE"),
        ],
    )
    def test_exact_matrix_classification_is_rotation_invariant(self, spectrum, expected):
        """Tolerance: spectra are >= 1e-3 away from ±threshold, far above the
        ~1e-15 rounding of Q·D·Qᵀ."""
        for theta in np.linspace(0.0, np.pi, 13):
            Q = self._rotation(theta)
            H = Q @ np.diag(spectrum) @ Q.T
            H = (H + H.T) / 2
            assert classify_stability(H)[0] == expected

    def test_estimated_rotated_saddle_is_reference_or_unresolved(self):
        """No bitwise invariance is required for coordinate-dependent differences;
        the result must be the reference class or UNRESOLVED."""
        for theta in np.linspace(0.0, np.pi, 7):
            Q = self._rotation(theta)

            def f(q, Q=Q):
                y = Q.T @ q
                return float(y[0] ** 2 - y[1] ** 2)

            H = compute_hessian_numerical(
                f, np.array([0.2, -0.1]), fourth_derivative_bound=0.0, evaluation_error=1e-14
            )
            assert classify_stability(H)[0] in ("UNSTABLE", "UNRESOLVED")


class TestMod18Uncertainty:
    @pytest.mark.parametrize(
        "eigvals,delta,expected",
        [
            ([2.0, 1.0], 0.1, SpectralVoidClass.BASIN),
            ([2.0, 1e-9], 1e-10, SpectralVoidClass.FLAT_VOID),
            ([2.0, 1e-9], 1e-6, SpectralVoidClass.UNDEFINED),
            ([-1.0, 1e-9], 1e-10, SpectralVoidClass.DEGENERATE_SADDLE),
            ([-1.0, 2.0], 2.0, SpectralVoidClass.UNDEFINED),
            ([2.0, 1.0], float("nan"), SpectralVoidClass.UNDEFINED),
            ([2.0, 1.0], -1.0, SpectralVoidClass.UNDEFINED),
            ([2.0, 1.0], True, SpectralVoidClass.UNDEFINED),
        ],
    )
    def test_eigenvalue_uncertainty(self, eigvals, delta, expected):
        assert classify_spectral_void(eigvals, eigval_uncertainty=delta) == expected

    def test_without_uncertainty_behaviour_is_unchanged(self):
        assert classify_spectral_void([2.0, 1e-9]) == SpectralVoidClass.FLAT_VOID

    def test_matrix_helper_treats_plain_matrix_as_exact_and_invalid_as_undefined(self):
        assert classify_hessian_spectral_void(np.diag([2.0, 1.0])) == SpectralVoidClass.BASIN
        assert classify_hessian_spectral_void(np.array([[1.0, 3.0], [0.0, 1.0]])) == (
            SpectralVoidClass.UNDEFINED
        )


class TestValidation:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"point": np.array([np.nan, 0.0])},
            {"point": np.zeros((2, 2))},
            {"point": np.array([])},
            {"eps": 0.0},
            {"eps": -1e-3},
            {"eps": float("inf")},
            {"fourth_derivative_bound": -1.0, "evaluation_error": 0.0},
            {"fourth_derivative_bound": 0.0, "evaluation_error": float("nan")},
        ],
    )
    def test_invalid_arguments_raise(self, kwargs):
        args = {"point": np.zeros(2)} | kwargs
        point = args.pop("point")
        with pytest.raises(ValueError):
            compute_hessian_numerical(lambda q: float(np.sum(q**2)), point, **args)

    def test_non_finite_function_value_raises(self):
        with pytest.raises(ValueError, match="non-finite"):
            compute_hessian_numerical(lambda q: float("nan"), np.zeros(2))
