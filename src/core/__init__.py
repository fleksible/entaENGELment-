# Core metrics for entaENGELment Framework
"""Core-Module des entaENGELment Frameworks.

Enthält die fünf Kern-Metriken (Core-5):
- ECI (Ethical Consent Index)
- PLV (Phase Locking Value)
- MI (Mutual Information)
- FD (Fractal Dimension)
- PF (Power Flux)

Zusätzlich: Evidence Routing Kernel v0.1a (bewusst kleine, stabile Exports).
"""

from .evidence_routing import (
    ClaimCandidate,
    ClaimPolicy,
    EvidenceRelation,
    EvidenceRoutingError,
    GuardDecision,
    HumanDecision,
    MaterialRef,
    ReasonCode,
    ReducedPublicExport,
    ReplayState,
    Retraction,
    TransitionRequest,
    apply_approved_transition,
    compute_permitted_transitions,
    compute_state_digest,
    evaluate_transition_request,
    load_claim_policy,
    normalize_claim_tag,
    record_human_decision,
    record_retraction,
    reduce_public_export,
    replay_events,
)
from .metrics import eci, fd, mi, pf, plv

__all__ = [
    # Core-5 Metriken
    "eci",
    "plv",
    "mi",
    "fd",
    "pf",
    # Evidence Routing Kernel v0.1a — Kernmodelle
    "MaterialRef",
    "ClaimCandidate",
    "EvidenceRelation",
    "TransitionRequest",
    "GuardDecision",
    "HumanDecision",
    "Retraction",
    "ReplayState",
    "ReducedPublicExport",
    "ClaimPolicy",
    "ReasonCode",
    "EvidenceRoutingError",
    # Evidence Routing Kernel v0.1a — Kernfunktionen
    "load_claim_policy",
    "normalize_claim_tag",
    "compute_permitted_transitions",
    "evaluate_transition_request",
    "record_human_decision",
    "apply_approved_transition",
    "record_retraction",
    "replay_events",
    "reduce_public_export",
    "compute_state_digest",
]
