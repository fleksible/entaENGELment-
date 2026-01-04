"""Stability analysis module for entaENGELment Framework.

Provides Hessian-based void detection and stability classification.

- MOD_16: Hessian void analysis (compute_hessian_numerical, classify_stability, detect_void_type)
- MOD_18: Spectral taxonomy (SpectralVoidClass, classify_spectral_void)
- MOD_14 Integration: Gate mapping (map_taxonomy_to_gate)
"""

# MOD_16: Hessian-based analysis
from .hessian_void import (
    classify_stability,
    compute_hessian_numerical,
    detect_void_type,
)

# MOD_18: Spectral taxonomy
from .spectral_void import SpectralVoidClass, classify_spectral_void

# MOD_14 Integration: Gate decisions
from .stability_guard import map_taxonomy_to_gate

__all__ = [
    # MOD_16
    "compute_hessian_numerical",
    "classify_stability",
    "detect_void_type",
    # MOD_18
    "SpectralVoidClass",
    "classify_spectral_void",
    # MOD_14 Integration
    "map_taxonomy_to_gate",
]
