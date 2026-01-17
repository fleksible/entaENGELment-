"""MZM (Minimal Zero Model) Package.

Implementiert die Gate-Toggle-Logik und Policy-Enforcement
für das entaENGELment Framework.
"""

from .gate_toggle import Context, gate_open, load_policy

__all__ = ["Context", "load_policy", "gate_open"]
