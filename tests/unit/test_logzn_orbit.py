# ruff: noqa: I001
"""Minimal executable evidence for VOID-LOGZN-001.

Slice S-3a. These tests do not claim the RZT/LOG-ZN operator as such; they
only show that the mathematical substrate described in
docs/rzt/LOG_ZN_ORBIT_001.md is reachable and behaves as written in the
underlying stdlib/numpy primitives.

Semantic status:
- VOID-LOGZN-001 remains formally OPEN.
- Evidence position shifts: docs-only -> executable evidence present.
"""

from __future__ import annotations

import cmath
import math

import numpy as np


def test_cmath_log_branch_cut_orientation() -> None:
    # Two points infinitesimally above and below the negative real axis.
    eps = 1e-12
    above = cmath.log(complex(-1.0, eps))
    below = cmath.log(complex(-1.0, -eps))

    # Real parts: |z| = 1 on both sides -> ln(1) = 0.
    assert math.isclose(above.real, 0.0, abs_tol=1e-9)
    assert math.isclose(below.real, 0.0, abs_tol=1e-9)

    # Imaginary parts land on opposite sides of the principal branch cut:
    # above -> +pi, below -> -pi.
    assert math.isclose(above.imag, math.pi, abs_tol=1e-6)
    assert math.isclose(below.imag, -math.pi, abs_tol=1e-6)

    # Therefore the two log values straddle the cut; their difference
    # is approximately 2*pi in the imaginary direction.
    assert math.isclose(above.imag - below.imag, 2.0 * math.pi, abs_tol=1e-6)


def test_phase_unwrap_tracks_winding_number() -> None:
    # Two full continuous revolutions: theta sweeps 0 -> 4*pi.
    n = 401
    theta = np.linspace(0.0, 4.0 * math.pi, n)

    # numpy.angle on exp(i*theta) wraps into (-pi, pi]; numpy.unwrap should
    # recover the underlying continuous phase without 2*pi jumps.
    wrapped = np.angle(np.exp(1j * theta))
    unwrapped = np.unwrap(wrapped)

    # Wrapped signal carries at least one 2*pi discontinuity (the visible
    # return to the same circle position).
    max_wrapped_jump = float(np.max(np.abs(np.diff(wrapped))))
    assert max_wrapped_jump > math.pi

    # Unwrapped signal is monotone in the small step regime and has no
    # 2*pi discontinuity.
    max_unwrapped_jump = float(np.max(np.abs(np.diff(unwrapped))))
    assert max_unwrapped_jump < math.pi

    # Total developed phase recovers the input range up to numpy.unwrap's
    # constant offset; the span equals 4*pi (= winding number 2 * 2*pi).
    span = float(unwrapped[-1] - unwrapped[0])
    assert math.isclose(span, 4.0 * math.pi, abs_tol=1e-6)
