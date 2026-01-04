"""
src/stability/stability_guard.py

MOD_18 -> MOD_14 Integration.
Maps spectral taxonomy to gate decisions with normalized reason codes.
"""

from .spectral_void import SpectralVoidClass


def map_taxonomy_to_gate(void_class: SpectralVoidClass, has_consent: bool) -> tuple[str, str]:
    """
    MOD_18 -> MOD_14 Integration.

    Args:
        void_class: The spectral taxonomy classification
        has_consent: Whether explicit consent is present

    Returns:
        Tuple of (Decision, ReasonCode) for auditing
    """
    # SAFE ZONES
    if void_class == SpectralVoidClass.BASIN:
        return "ALLOW", "SAFE_BASIN_ROBUST"

    if void_class == SpectralVoidClass.SOFT_BASIN:
        # Allowed but logged as warning
        return "ALLOW", "WARN_BASIN_SOFT"

    # CONSENT ZONES (The Void)
    if void_class == SpectralVoidClass.FLAT_VOID:
        if has_consent:
            return "ALLOW", "AUTH_CONSENT_FLAT_VOID"
        return "BLOCK", "BLOCK_NEED_CONSENT_FLAT_VOID"

    # DANGER ZONES (Saddles)
    if void_class in [SpectralVoidClass.RIDGE_SADDLE, SpectralVoidClass.MULTI_SADDLE]:
        return "BLOCK", "BLOCK_UNSTABLE_SADDLE"

    if void_class == SpectralVoidClass.DEGENERATE_SADDLE:
        return "BLOCK", "BLOCK_UNSTABLE_DEGENERATE"

    if void_class == SpectralVoidClass.INVERTED_MAX:
        return "BLOCK", "BLOCK_UNSTABLE_INVERSION"

    return "BLOCK", "BLOCK_UNDEFINED_STATE"
