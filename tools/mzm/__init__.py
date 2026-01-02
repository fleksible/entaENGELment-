"""MZM (Minimal Zero Model) Package.

Implementiert die Gate-Toggle-Logik und Policy-Enforcement
für das entaENGELment Framework.
"""

from .gate_toggle import Context, load_policy, gate_open

__all__ = ["Context", "load_policy", "gate_open"]
