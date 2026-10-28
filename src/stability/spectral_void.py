"""
src/stability/spectral_void.py

MOD_18: 7-Point Spectral Taxonomy based on Hessian Eigenvalues.
Classifies local geometry for stability analysis.

Robust against shape mismatches, NaNs, and edge cases.

Uncertainty: ``classify_spectral_void`` treats eigenvalues as exact unless an
``eigval_uncertainty`` δ is given; then every eigenvalue that cannot be assigned
unambiguously (negative / flat / positive) yields UNDEFINED, which blocks.
``classify_hessian_spectral_void`` derives δ from an ``EstimatedHessian``; an
estimate without declared error assumptions yields UNDEFINED. Plain eigenvalue
arrays carry no uncertainty: that entry point remains eigenvalue-only.
"""

import math
import numbers
from enum import Enum

import numpy as np

from .hessian_void import eigenvalue_bounds


class SpectralVoidClass(Enum):
    """
    MOD_18: 7-Point Taxonomy based on Hessian Eigenvalues.
    Refines the rough STABLE/FLAT/UNSTABLE signal.
    """

    BASIN = "BASIN"  # Robust local minimum
    SOFT_BASIN = "SOFT_BASIN"  # Stable but weak/ill-conditioned
    FLAT_VOID = "FLAT_VOID"  # Zero curvature detected
    RIDGE_SADDLE = "RIDGE_SADDLE"  # 1 direction down (Index 1)
    MULTI_SADDLE = "MULTI_SADDLE"  # >1 direction down (Index >1)
    DEGENERATE_SADDLE = "DEGENERATE_SADDLE"  # Saddle + Flatness
    INVERTED_MAX = "INVERTED_MAX"  # All directions down
    UNDEFINED = "UNDEFINED"  # Input error / NaNs


def classify_spectral_void(
    eigvals,
    eps: float = 1e-8,
    soft_thr: float = 1e-3,
    kappa_thr: float = 1e6,
    eigval_uncertainty: float | None = None,
) -> SpectralVoidClass:
    """
    Classifies local geometry. Robust against shape mismatches and NaNs.

    Args:
        eigvals: Eigenvalues (list, array, any shape - will be flattened)
        eps: Threshold for zero detection
        soft_thr: Threshold for soft basin detection
        kappa_thr: Condition number threshold for ill-conditioning
        eigval_uncertainty: Optional bound δ >= 0 on every eigenvalue's error.
            Any eigenvalue whose interval [λ-δ, λ+δ] is not unambiguously
            negative, flat or positive yields UNDEFINED. An invalid δ also
            yields UNDEFINED.

    Returns:
        SpectralVoidClass enum value
    """
    # 1. Robustness / Normalization
    ev = np.asarray(eigvals, dtype=float).ravel()
    if ev.size == 0 or not np.all(np.isfinite(ev)):
        return SpectralVoidClass.UNDEFINED

    if eigval_uncertainty is not None:
        delta = eigval_uncertainty
        if (
            isinstance(delta, bool)
            or not isinstance(delta, numbers.Real)
            or not math.isfinite(delta)
            or delta < 0
        ):
            return SpectralVoidClass.UNDEFINED
        certain = (ev + delta < -eps) | (np.abs(ev) + delta <= eps) | (ev - delta > eps)
        if not np.all(certain):
            return SpectralVoidClass.UNDEFINED

    # 2. Analysis
    ev_sorted = np.sort(ev)

    n_neg = int(np.sum(ev_sorted < -eps))
    n_zero = int(np.sum(np.abs(ev_sorted) <= eps))

    # Positive subset logic
    pos = ev_sorted[ev_sorted > eps]
    n_pos = pos.size

    # 3. Decision Tree (The Taxonomy)

    # Pure Hilltop
    if n_neg == ev_sorted.size:
        return SpectralVoidClass.INVERTED_MAX

    # Saddles (Any negative curvature)
    if n_neg > 0:
        if n_zero > 0:
            return SpectralVoidClass.DEGENERATE_SADDLE
        return SpectralVoidClass.RIDGE_SADDLE if n_neg == 1 else SpectralVoidClass.MULTI_SADDLE

    # Pure Flat
    if n_zero > 0:
        return SpectralVoidClass.FLAT_VOID

    # Basins (All positive) - Check Condition
    # Kappa calculation handles n_pos=1 gracefully (1.0 is stable)
    min_pos = float(pos[0])
    max_pos = float(pos[-1])
    kappa = (max_pos / min_pos) if n_pos >= 2 else 1.0

    if min_pos < soft_thr or kappa > kappa_thr:
        return SpectralVoidClass.SOFT_BASIN

    return SpectralVoidClass.BASIN


def classify_hessian_spectral_void(
    hessian, eps: float = 1e-8, soft_thr: float = 1e-3, kappa_thr: float = 1e6
) -> SpectralVoidClass:
    """MOD_18 taxonomy for a matrix, honouring the uncertainty of an estimate.

    A caller-supplied matrix is treated as exact. An ``EstimatedHessian``
    contributes its eigenvalue bound δ; without declared error assumptions it
    yields UNDEFINED (maps to BLOCK_UNDEFINED_STATE). Invalid matrices also
    yield UNDEFINED.
    """
    try:
        eigvals, delta = eigenvalue_bounds(hessian)
    except ValueError:
        return SpectralVoidClass.UNDEFINED
    if delta is None:
        return SpectralVoidClass.UNDEFINED
    return classify_spectral_void(eigvals, eps, soft_thr, kappa_thr, eigval_uncertainty=delta)
