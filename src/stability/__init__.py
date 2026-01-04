"""Stability analysis module for entaENGELment Framework.

Provides Hessian-based void detection and stability classification.
"""

from .hessian_void import (
    compute_hessian_numerical,
    classify_stability,
    detect_void_type,
)

__all__ = [
    "compute_hessian_numerical",
    "classify_stability",
    "detect_void_type",
# MOD_16 & MOD_18 Stability Analysis Package

# Export the Taxonomy (MOD_18)
from .spectral_void import SpectralVoidClass, classify_spectral_void

# Export the Guard (MOD_14 Integration)
from .stability_guard import map_taxonomy_to_gate

__all__ = [
    "SpectralVoidClass",
    "classify_spectral_void",
    "map_taxonomy_to_gate",
]
