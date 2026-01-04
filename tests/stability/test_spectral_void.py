"""
tests/stability/test_spectral_void.py

Unit tests for MOD_18 Spectral Taxonomy.
"""

import numpy as np

from src.stability.spectral_void import SpectralVoidClass, classify_spectral_void
from src.stability.stability_guard import map_taxonomy_to_gate


class TestSpectralVoidClassification:
    """Tests for classify_spectral_void function."""

    def test_robust_basin(self):
        """All positive, well-conditioned eigenvalues -> BASIN"""
        ev = [1.0, 2.0, 3.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.BASIN

    def test_soft_basin_low_eigenvalue(self):
        """Positive but with very small eigenvalue -> SOFT_BASIN"""
        ev = [1e-5, 1.0, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.SOFT_BASIN

    def test_soft_basin_high_kappa(self):
        """High condition number -> SOFT_BASIN"""
        ev = [1e-4, 1e3]  # kappa = 1e7 > 1e6
        assert classify_spectral_void(ev) == SpectralVoidClass.SOFT_BASIN

    def test_flat_void(self):
        """Zero eigenvalue, no negatives -> FLAT_VOID"""
        ev = [0.0, 1.0, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.FLAT_VOID

    def test_flat_void_near_zero(self):
        """Near-zero eigenvalue within eps -> FLAT_VOID"""
        ev = [1e-10, 1.0, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.FLAT_VOID

    def test_ridge_saddle(self):
        """One negative eigenvalue -> RIDGE_SADDLE"""
        ev = [-1.0, 1.0, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.RIDGE_SADDLE

    def test_multi_saddle(self):
        """Multiple negative eigenvalues -> MULTI_SADDLE"""
        ev = [-2.0, -1.0, 1.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.MULTI_SADDLE

    def test_degenerate_saddle(self):
        """Negative + zero eigenvalue -> DEGENERATE_SADDLE"""
        ev = [-1.0, 0.0, 1.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.DEGENERATE_SADDLE

    def test_inverted_max(self):
        """All negative eigenvalues -> INVERTED_MAX"""
        ev = [-3.0, -2.0, -1.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.INVERTED_MAX

    def test_undefined_nan(self):
        """NaN in eigenvalues -> UNDEFINED"""
        ev = [1.0, np.nan, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.UNDEFINED

    def test_undefined_inf(self):
        """Inf in eigenvalues -> UNDEFINED"""
        ev = [1.0, np.inf, 2.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.UNDEFINED

    def test_undefined_empty(self):
        """Empty input -> UNDEFINED"""
        assert classify_spectral_void([]) == SpectralVoidClass.UNDEFINED

    def test_robustness_2d_array(self):
        """2D array input is flattened correctly"""
        ev = np.array([[1.0, 2.0], [3.0, 4.0]])
        assert classify_spectral_void(ev) == SpectralVoidClass.BASIN

    def test_robustness_column_vector(self):
        """Column vector (N,1) is handled correctly"""
        ev = np.array([[1.0], [2.0], [3.0]])
        assert classify_spectral_void(ev) == SpectralVoidClass.BASIN

    def test_single_positive_eigenvalue(self):
        """Single positive eigenvalue -> BASIN (kappa=1.0)"""
        ev = [5.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.BASIN

    def test_single_negative_eigenvalue(self):
        """Single negative eigenvalue -> INVERTED_MAX"""
        ev = [-5.0]
        assert classify_spectral_void(ev) == SpectralVoidClass.INVERTED_MAX


class TestStabilityGuard:
    """Tests for map_taxonomy_to_gate function."""

    def test_basin_allows(self):
        """BASIN -> ALLOW with SAFE reason"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.BASIN, False)
        assert decision == "ALLOW"
        assert reason == "SAFE_BASIN_ROBUST"

    def test_soft_basin_warns(self):
        """SOFT_BASIN -> ALLOW with WARN reason"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.SOFT_BASIN, False)
        assert decision == "ALLOW"
        assert reason == "WARN_BASIN_SOFT"

    def test_flat_void_blocks_without_consent(self):
        """FLAT_VOID without consent -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.FLAT_VOID, False)
        assert decision == "BLOCK"
        assert reason == "BLOCK_NEED_CONSENT_FLAT_VOID"

    def test_flat_void_allows_with_consent(self):
        """FLAT_VOID with consent -> ALLOW"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.FLAT_VOID, True)
        assert decision == "ALLOW"
        assert reason == "AUTH_CONSENT_FLAT_VOID"

    def test_ridge_saddle_blocks(self):
        """RIDGE_SADDLE -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.RIDGE_SADDLE, True)
        assert decision == "BLOCK"
        assert reason == "BLOCK_UNSTABLE_SADDLE"

    def test_multi_saddle_blocks(self):
        """MULTI_SADDLE -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.MULTI_SADDLE, True)
        assert decision == "BLOCK"
        assert reason == "BLOCK_UNSTABLE_SADDLE"

    def test_degenerate_saddle_blocks(self):
        """DEGENERATE_SADDLE -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.DEGENERATE_SADDLE, True)
        assert decision == "BLOCK"
        assert reason == "BLOCK_UNSTABLE_DEGENERATE"

    def test_inverted_max_blocks(self):
        """INVERTED_MAX -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.INVERTED_MAX, True)
        assert decision == "BLOCK"
        assert reason == "BLOCK_UNSTABLE_INVERSION"

    def test_undefined_blocks(self):
        """UNDEFINED -> BLOCK"""
        decision, reason = map_taxonomy_to_gate(SpectralVoidClass.UNDEFINED, True)
        assert decision == "BLOCK"
        assert reason == "BLOCK_UNDEFINED_STATE"
