"""
tests/ethics/test_b9_estimated_hessian_guard.py

Acceptance tests for finding B9 on the actual computation-to-guard path
(compute_hessian_numerical -> classify_stability -> stability_gate, and the MOD_18
path via classify_hessian_spectral_void -> map_taxonomy_to_gate), checked against
analytic reference Hessians.

The test matrices are the ones of docs/audit/harness/b9_hessian_offset_matrix.py
(7x7 grid x 6 offsets, and 400 cases from numpy default_rng(0)). On e8bea51 they
produced releases without consent for a FLAT reference (57/294 and 104/400).

Covered here: the reproduced cases on these matrices. Not covered: arbitrary
functions, points or offsets outside them; green tests are not a proof of safety.
"""

import itertools

import numpy as np
import pytest

from src.core.stability_guard import stability_gate
from src.stability.hessian_void import classify_stability, compute_hessian_numerical
from src.stability.spectral_void import SpectralVoidClass, classify_hessian_spectral_void
from src.stability.stability_guard import map_taxonomy_to_gate

EPS_MACH = float(np.finfo(float).eps)
AXIS = [-3.0, -1.5, -0.7, 0.0, 0.3, 1.0, 2.2]
OFFSETS = [0.0, 1.0, 10.0, 100.0, 1e3, 1e4]


def _matrix_cases():
    grid = [((x, y), c) for (x, y), c in itertools.product(itertools.product(AXIS, AXIS), OFFSETS)]
    rng = np.random.default_rng(0)
    sweep = []
    for _ in range(400):
        point = rng.uniform(-3, 3, 2)
        offset = float(10 ** rng.uniform(0, 4))
        sweep.append((tuple(point), offset))
    return grid + sweep


CASES = _matrix_cases()

# f = a*x^2 + b*y^2 + C with analytic Hessian diag(2a, 2b), independent of C.
REFERENCES = {
    "flat": (1.0, 1e-8, "FLAT"),
    "stable": (1.0, 1.0, "STABLE"),
    "saddle": (1.0, -1.0, "UNSTABLE"),
}


def _estimate(a, b, point, offset, declared):
    def f(q):
        return a * q[0] ** 2 + b * q[1] ** 2 + offset

    if not declared:
        return compute_hessian_numerical(f, np.array(point))
    # Valid declarations for this function: all fourth derivatives are 0; the
    # evaluation error of three terms with four roundings is <= 2*eps*sum|terms|,
    # declared with a factor 2 margin over a radius covering the stencil.
    radius = max(abs(point[0]), abs(point[1])) + 1e-3
    evaluation_error = 4 * EPS_MACH * ((abs(a) + abs(b)) * radius**2 + abs(offset))
    return compute_hessian_numerical(
        f, np.array(point), fourth_derivative_bound=0.0, evaluation_error=evaluation_error
    )


@pytest.mark.parametrize("name", REFERENCES)
def test_estimate_without_declared_assumptions_never_releases(name):
    a, b, _ = REFERENCES[name]
    for point, offset in CASES:
        H = _estimate(a, b, point, offset, declared=False)
        assert classify_stability(H)[0] == "UNRESOLVED"
        for consent in (False, True):
            allow, reason = stability_gate(H, consent_available=consent)
            assert allow is False and reason.startswith("UNRESOLVED")
        assert classify_hessian_spectral_void(H) == SpectralVoidClass.UNDEFINED


@pytest.mark.parametrize("name", REFERENCES)
def test_declared_estimates_never_contradict_the_analytic_reference(name):
    """Result is the reference class or UNRESOLVED; never a permissive flip."""
    a, b, reference = REFERENCES[name]
    for point, offset in CASES:
        H = _estimate(a, b, point, offset, declared=True)
        status = classify_stability(H)[0]
        assert status in (reference, "UNRESOLVED"), (point, offset, status)

        allow_without, _ = stability_gate(H, consent_available=False)
        allow_with, _ = stability_gate(H, consent_available=True)
        if reference == "FLAT":
            assert allow_without is False, (point, offset)
        if reference == "UNSTABLE":
            assert allow_without is False and allow_with is False, (point, offset)
        if status == "UNRESOLVED":
            assert allow_without is False and allow_with is False


def test_reproduced_b9_single_case_no_longer_releases_without_consent():
    """(1,1), C=10: on e8bea51 STABLE and released without consent."""
    a, b, _ = REFERENCES["flat"]
    for declared in (False, True):
        H = _estimate(a, b, (1.0, 1.0), 10.0, declared=declared)
        assert stability_gate(H, consent_available=False)[0] is False


def test_stable_and_saddle_references_are_resolved_on_the_tested_matrices():
    """Coverage of the tested range: no blanket UNRESOLVED for clear cases."""
    for name in ("stable", "saddle"):
        a, b, reference = REFERENCES[name]
        statuses = {classify_stability(_estimate(a, b, p, c, True))[0] for p, c in CASES}
        assert statuses == {reference}


@pytest.mark.parametrize("consent", [False, True])
def test_core_and_mod18_agree_on_blocking_for_estimates(consent):
    """Same tolerance on both paths; MOD_18 maps UNRESOLVED to UNDEFINED."""
    tau = 1e-6
    for name, (a, b, _) in REFERENCES.items():
        for point, offset in CASES[::7]:
            H = _estimate(a, b, point, offset, declared=True)
            core_allow, _ = stability_gate(H, consent_available=consent)
            mod18 = classify_hessian_spectral_void(H, eps=tau)
            decision, _ = map_taxonomy_to_gate(mod18, has_consent=consent)
            assert core_allow == (decision == "ALLOW"), (name, point, offset)
