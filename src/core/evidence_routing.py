"""
src/core/evidence_routing.py

Evidence Routing Kernel v0.1a für das entaENGELment Framework.

Verbindet Claim-Tags, Materialverweise, Evidence-Relationen, Guard-Entscheidungen
und menschliche Entscheidungen zu einem deterministisch replaybaren Zustandsfluss.

Architekturgrenze (siehe docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md):
- Policy = zulässige syntaktische Nachbarschaft, kein Wahrheitsbeweis.
- Guard = lokale Durchlassentscheidung (PROPOSE/HOLD/STOP), kein Claim-Status.
- HumanDecision = einzige v0.1a-Quelle für tatsächliches Retagging.
- Replay = Rekonstruktion eines Zustands, keine Wiederholung der Wahrheit.
- Export = Reduktion, keine Rekonstruktion privater Herkunft.

Der Kernel führt keine Netzwerkzugriffe, keine Shell-Kommandos und keine
automatische Claim-Promotion aus.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Schema- und Vokabular-Konstanten
# ---------------------------------------------------------------------------

ERK_SCHEMA_VERSION = "erk.v0.1"
ERK_EXPORT_SCHEMA_VERSION = "erk_public_export.v0.2"

DEFAULT_CLAIM_POLICY_PATH = (
    Path(__file__).resolve().parents[2] / "policies" / "claim_tags_v0_2.yaml"
)

# Domain-Eventtypen des Kernels (Envelope: {"type": ..., "payload": {...}})
EVENT_MATERIAL_REGISTERED = "MATERIAL_REGISTERED"
EVENT_CLAIM_CREATED = "CLAIM_CREATED"
EVENT_EVIDENCE_RELATION_RECORDED = "EVIDENCE_RELATION_RECORDED"
EVENT_TRANSITION_REQUESTED = "TRANSITION_REQUESTED"
EVENT_GUARD_DECISION_RECORDED = "GUARD_DECISION_RECORDED"
EVENT_HUMAN_DECISION_RECORDED = "HUMAN_DECISION_RECORDED"
EVENT_CLAIM_RETAGGED = "CLAIM_RETAGGED"
EVENT_RETRACTION_RECORDED = "RETRACTION_RECORDED"

ERK_EVENT_TYPES = frozenset(
    {
        EVENT_MATERIAL_REGISTERED,
        EVENT_CLAIM_CREATED,
        EVENT_EVIDENCE_RELATION_RECORDED,
        EVENT_TRANSITION_REQUESTED,
        EVENT_GUARD_DECISION_RECORDED,
        EVENT_HUMAN_DECISION_RECORDED,
        EVENT_CLAIM_RETAGGED,
        EVENT_RETRACTION_RECORDED,
    }
)

# Envelope-Felder, wie sie der Ledger serialisiert (plus Fixture-Minimalform).
_ENVELOPE_ALLOWED_KEYS = frozenset(
    {"type", "payload", "event_id", "timestamp", "span_id", "hash", "prev_hash"}
)

GUARD_PROPOSE = "PROPOSE"
GUARD_HOLD = "HOLD"
GUARD_STOP = "STOP"
GUARD_DECISION_VALUES = frozenset({GUARD_PROPOSE, GUARD_HOLD, GUARD_STOP})

HUMAN_APPROVE = "APPROVE"
HUMAN_REJECT = "REJECT"
HUMAN_DEFER = "DEFER"
HUMAN_WITHDRAW = "WITHDRAW"
HUMAN_DECISION_VALUES = frozenset({HUMAN_APPROVE, HUMAN_REJECT, HUMAN_DEFER, HUMAN_WITHDRAW})

RELATION_TYPES = frozenset(
    {
        "SUPPORTS",
        "CONTRADICTS",
        "CONTEXTUALIZES",
        "MOTIVATES",
        "MEASURES",
        "IMPLEMENTS",
        "PROVENANCE_ONLY",
    }
)
# Relationen, die eine Promotion tragen können. MOTIVATES und PROVENANCE_ONLY
# sind explizit keine Evidenz für Promotion (Invarianten 3/4); CONTRADICTS und
# CONTEXTUALIZES stützen eine Hochstufung ebenfalls nicht.
PROMOTION_CAPABLE_RELATION_TYPES = frozenset({"SUPPORTS", "MEASURES", "IMPLEMENTS"})

TRUST_TRUSTED = "TRUSTED"
TRUST_REVIEWED = "REVIEWED"
TRUST_UNTRUSTED = "UNTRUSTED"
KNOWN_TRUST_LEVELS = frozenset({TRUST_TRUSTED, TRUST_REVIEWED, TRUST_UNTRUSTED})

VISIBILITY_PRIVATE = "private"
VISIBILITY_REDUCED = "reduced"
VISIBILITY_PUBLIC = "public"
KNOWN_VISIBILITIES = frozenset({VISIBILITY_PRIVATE, VISIBILITY_REDUCED, VISIBILITY_PUBLIC})

# Materialarten, die per Register-Regel keine Evidenz sind (metaphor_not_evidence).
NON_EVIDENCE_MATERIAL_KINDS = frozenset({"metaphor", "metapher", "rosetta"})

# Public exports never forward free-form material kinds. Known operational
# categories remain visible; every other value is reduced to ``other``.
PUBLIC_MATERIAL_KINDS = frozenset(
    {"measurement", "document", "note", "data", "file", "implementation", "specification"}
)

# Zieltags, deren Erreichen als Promotion gilt und Evidenz benötigt.
PROMOTION_TAGS = frozenset({"[INFERENZ]", "[MODEL]", "[FACT]", "[SPEC-WIP]", "[SPEC]", "[CANON]"})

CLAIM_STATUS_ACTIVE = "ACTIVE"
CLAIM_STATUS_RETRACTED = "RETRACTED"
# Claim-Status, die fehlenden oder zurückgezogenen Consent signalisieren (fail-closed).
CONSENT_BLOCKED_STATUSES = frozenset({"CONSENT_MISSING", "CONSENT_REVOKED"})


class ReasonCode(str, Enum):
    """Geschlossenes Reason-Code-Vokabular des Kernels (keine dynamischen Codes)."""

    POLICY_TRANSITION_ALLOWED = "POLICY_TRANSITION_ALLOWED"
    POLICY_TRANSITION_DENIED = "POLICY_TRANSITION_DENIED"
    UNKNOWN_FROM_TAG = "UNKNOWN_FROM_TAG"
    UNKNOWN_TO_TAG = "UNKNOWN_TO_TAG"
    ALIAS_NORMALIZED = "ALIAS_NORMALIZED"
    MISSING_MATERIAL = "MISSING_MATERIAL"
    MISSING_EVIDENCE_RELATION = "MISSING_EVIDENCE_RELATION"
    UNTRUSTED_MATERIAL = "UNTRUSTED_MATERIAL"
    METAPHOR_IS_NOT_EVIDENCE = "METAPHOR_IS_NOT_EVIDENCE"
    PROVENANCE_IS_NOT_EVIDENCE = "PROVENANCE_IS_NOT_EVIDENCE"
    HUMAN_DECISION_REQUIRED = "HUMAN_DECISION_REQUIRED"
    HUMAN_APPROVED = "HUMAN_APPROVED"
    HUMAN_REJECTED = "HUMAN_REJECTED"
    HUMAN_DEFERRED = "HUMAN_DEFERRED"
    CONSENT_MISSING = "CONSENT_MISSING"
    VISIBILITY_VIOLATION = "VISIBILITY_VIOLATION"
    RETRACTION_RECORDED = "RETRACTION_RECORDED"
    EVENT_SCHEMA_INVALID = "EVENT_SCHEMA_INVALID"
    EVENT_ORDER_INVALID = "EVENT_ORDER_INVALID"
    POLICY_DIGEST_MISMATCH = "POLICY_DIGEST_MISMATCH"
    UNKNOWN_EVENT_TYPE = "UNKNOWN_EVENT_TYPE"
    EVIDENCE_CLAIM_MISMATCH = "EVIDENCE_CLAIM_MISMATCH"
    GUARD_REFERENCE_MISMATCH = "GUARD_REFERENCE_MISMATCH"
    HUMAN_REFERENCE_MISMATCH = "HUMAN_REFERENCE_MISMATCH"
    REQUEST_REFERENCE_MISMATCH = "REQUEST_REFERENCE_MISMATCH"
    DUPLICATE_STABLE_ID = "DUPLICATE_STABLE_ID"


_KNOWN_REASON_CODES = frozenset(code.value for code in ReasonCode)


class EvidenceRoutingError(ValueError):
    """Fail-closed Fehler des Kernels mit kontrollierten Reason-Codes."""

    def __init__(self, message: str, reason_codes: Sequence[ReasonCode] = ()) -> None:
        super().__init__(message)
        self.reason_codes: tuple[ReasonCode, ...] = tuple(reason_codes)


# ---------------------------------------------------------------------------
# Kernmodelle
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MaterialRef:
    """Reduzierter Verweis auf Material; speichert keine privaten Rohinhalte."""

    material_id: str
    schema_version: str
    kind: str
    source: str
    revision: str
    locator: str
    digest: str
    origin: str
    actor: str
    trust: str
    visibility: str
    status: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClaimCandidate:
    claim_id: str
    schema_version: str
    claim_text: str
    claim_tag: str
    actor: str
    origin: str
    visibility: str
    status: str
    material_refs: list[str]

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRelation:
    relation_id: str
    schema_version: str
    claim_id: str
    material_id: str
    relation_type: str
    actor: str
    origin: str
    visibility: str
    status: str
    reason_codes: list[str]

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransitionRequest:
    request_id: str
    schema_version: str
    claim_id: str
    from_tag: str
    to_tag: str
    actor: str
    origin: str
    requested_at: float
    evidence_relation_ids: list[str]
    reason_codes: list[str]
    visibility: str
    status: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardDecision:
    decision_id: str
    schema_version: str
    request_id: str
    decision: str
    reason_codes: list[str]
    policy_version: str
    policy_digest: str
    actor: str
    origin: str
    visibility: str
    status: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HumanDecision:
    decision_id: str
    schema_version: str
    request_id: str
    decision: str
    human_actor: str
    decided_at: float
    reason_codes: list[str]
    visibility: str
    status: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Retraction:
    retraction_id: str
    schema_version: str
    claim_id: str
    actor: str
    retracted_at: float
    reason_codes: list[str]
    visibility: str
    status: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


_STR = "str"
_STR_LIST = "str_list"
_NUM = "num"

_MODEL_SPECS: dict[type, dict[str, str]] = {
    MaterialRef: {
        "material_id": _STR,
        "schema_version": _STR,
        "kind": _STR,
        "source": _STR,
        "revision": _STR,
        "locator": _STR,
        "digest": _STR,
        "origin": _STR,
        "actor": _STR,
        "trust": _STR,
        "visibility": _STR,
        "status": _STR,
    },
    ClaimCandidate: {
        "claim_id": _STR,
        "schema_version": _STR,
        "claim_text": _STR,
        "claim_tag": _STR,
        "actor": _STR,
        "origin": _STR,
        "visibility": _STR,
        "status": _STR,
        "material_refs": _STR_LIST,
    },
    EvidenceRelation: {
        "relation_id": _STR,
        "schema_version": _STR,
        "claim_id": _STR,
        "material_id": _STR,
        "relation_type": _STR,
        "actor": _STR,
        "origin": _STR,
        "visibility": _STR,
        "status": _STR,
        "reason_codes": _STR_LIST,
    },
    TransitionRequest: {
        "request_id": _STR,
        "schema_version": _STR,
        "claim_id": _STR,
        "from_tag": _STR,
        "to_tag": _STR,
        "actor": _STR,
        "origin": _STR,
        "requested_at": _NUM,
        "evidence_relation_ids": _STR_LIST,
        "reason_codes": _STR_LIST,
        "visibility": _STR,
        "status": _STR,
    },
    GuardDecision: {
        "decision_id": _STR,
        "schema_version": _STR,
        "request_id": _STR,
        "decision": _STR,
        "reason_codes": _STR_LIST,
        "policy_version": _STR,
        "policy_digest": _STR,
        "actor": _STR,
        "origin": _STR,
        "visibility": _STR,
        "status": _STR,
    },
    HumanDecision: {
        "decision_id": _STR,
        "schema_version": _STR,
        "request_id": _STR,
        "decision": _STR,
        "human_actor": _STR,
        "decided_at": _NUM,
        "reason_codes": _STR_LIST,
        "visibility": _STR,
        "status": _STR,
    },
    Retraction: {
        "retraction_id": _STR,
        "schema_version": _STR,
        "claim_id": _STR,
        "actor": _STR,
        "retracted_at": _NUM,
        "reason_codes": _STR_LIST,
        "visibility": _STR,
        "status": _STR,
    },
}


def model_from_payload(cls: type, payload: object) -> Any:
    """Payload strikt gegen das geschlossene Feldschema eines Modells parsen.

    Unbekannte Zusatzfelder, fehlende Pflichtfelder und falsche Typen führen
    fail-closed zu :class:`EvidenceRoutingError` (EVENT_SCHEMA_INVALID).
    """
    spec = _MODEL_SPECS.get(cls)
    if spec is None:
        raise EvidenceRoutingError(
            f"unknown model class: {cls!r}", [ReasonCode.EVENT_SCHEMA_INVALID]
        )
    if not isinstance(payload, Mapping):
        raise EvidenceRoutingError(
            f"{cls.__name__} payload must be a mapping", [ReasonCode.EVENT_SCHEMA_INVALID]
        )

    unknown = set(payload) - set(spec)
    if unknown:
        raise EvidenceRoutingError(
            f"{cls.__name__} payload has unknown fields: {sorted(unknown)}",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )

    data: dict[str, Any] = {}
    for name, kind in spec.items():
        if name not in payload:
            raise EvidenceRoutingError(
                f"{cls.__name__} payload missing required field: {name}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
        value = payload[name]
        if kind == _STR:
            if not isinstance(value, str):
                raise EvidenceRoutingError(
                    f"{cls.__name__}.{name} must be a string",
                    [ReasonCode.EVENT_SCHEMA_INVALID],
                )
        elif kind == _NUM:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise EvidenceRoutingError(
                    f"{cls.__name__}.{name} must be a number",
                    [ReasonCode.EVENT_SCHEMA_INVALID],
                )
            value = float(value)
        elif kind == _STR_LIST:
            if not isinstance(value, (list, tuple)) or not all(
                isinstance(item, str) for item in value
            ):
                raise EvidenceRoutingError(
                    f"{cls.__name__}.{name} must be a list of strings",
                    [ReasonCode.EVENT_SCHEMA_INVALID],
                )
            value = list(value)
        data[name] = value

    reason_codes = data.get("reason_codes")
    if reason_codes is not None:
        invalid = [code for code in reason_codes if code not in _KNOWN_REASON_CODES]
        if invalid:
            raise EvidenceRoutingError(
                f"{cls.__name__}.reason_codes contains unknown codes: {invalid}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )

    return cls(**data)


def normalize_trust(value: object) -> str:
    """Unbekannte Trust-Level werden fail-closed auf UNTRUSTED reduziert."""
    if isinstance(value, str) and value in KNOWN_TRUST_LEVELS:
        return value
    return TRUST_UNTRUSTED


# ---------------------------------------------------------------------------
# Policy laden und Tag-Nachbarschaft
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClaimPolicy:
    """Read-only Sicht auf policies/claim_tags_v0_2.yaml (kein Truth-Maker)."""

    version: str
    digest: str
    tags: dict[str, tuple[str, ...]]
    aliases: dict[str, str]

    def is_known_tag(self, tag: str) -> bool:
        return tag in self.tags

    def allowed_next(self, tag: str) -> tuple[str, ...]:
        return self.tags.get(tag, ())


@dataclass(frozen=True)
class TagNormalization:
    """Ergebnis der Alias-Normalisierung eines Claim-Tags."""

    tag: str
    known: bool
    alias_applied: bool


def load_claim_policy(path: str | Path | None = None) -> ClaimPolicy:
    """Claim-Tag-Policy read-only laden; Version und SHA-256-Digest erfassen."""
    policy_path = Path(path) if path is not None else DEFAULT_CLAIM_POLICY_PATH
    raw = policy_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()

    data = yaml.safe_load(raw)
    if not isinstance(data, Mapping):
        raise EvidenceRoutingError(
            f"claim policy is not a mapping: {policy_path}", [ReasonCode.EVENT_SCHEMA_INVALID]
        )

    version = data.get("version")
    tags_raw = data.get("tags")
    if not isinstance(version, str) or not isinstance(tags_raw, Mapping):
        raise EvidenceRoutingError(
            f"claim policy missing 'version' or 'tags': {policy_path}",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )

    tags: dict[str, tuple[str, ...]] = {}
    for tag, info in tags_raw.items():
        if not isinstance(tag, str) or not isinstance(info, Mapping):
            raise EvidenceRoutingError(
                f"claim policy tag entry invalid: {tag!r}", [ReasonCode.EVENT_SCHEMA_INVALID]
            )
        allowed = info.get("allowed_next", [])
        if not isinstance(allowed, (list, tuple)) or not all(
            isinstance(item, str) for item in allowed
        ):
            raise EvidenceRoutingError(
                f"claim policy allowed_next invalid for tag: {tag!r}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
        tags[tag] = tuple(allowed)

    aliases_raw = data.get("compatibility_notes", {})
    aliases: dict[str, str] = {}
    if isinstance(aliases_raw, Mapping):
        spelling = aliases_raw.get("spelling_aliases", {})
        if isinstance(spelling, Mapping):
            for alias, target in spelling.items():
                if isinstance(alias, str) and isinstance(target, str):
                    aliases[alias] = target

    return ClaimPolicy(version=version, digest=digest, tags=tags, aliases=aliases)


def normalize_claim_tag(tag: str, policy: ClaimPolicy) -> TagNormalization:
    """Bekannte Aliasformen normalisieren; unbekannte Tags bleiben markiert unbekannt."""
    if not isinstance(tag, str):
        raise EvidenceRoutingError("claim tag must be a string", [ReasonCode.EVENT_SCHEMA_INVALID])
    candidate = tag.strip()
    alias_applied = False
    if candidate in policy.aliases:
        candidate = policy.aliases[candidate]
        alias_applied = True
    return TagNormalization(
        tag=candidate, known=policy.is_known_tag(candidate), alias_applied=alias_applied
    )


def compute_permitted_transitions(tag: str, policy: ClaimPolicy) -> tuple[str, ...]:
    """Erlaubte Folgetags gemäß Draft-Register; unbekannter Tag fail-closed."""
    normalized = normalize_claim_tag(tag, policy)
    if not normalized.known:
        raise EvidenceRoutingError(f"unknown claim tag: {tag!r}", [ReasonCode.UNKNOWN_FROM_TAG])
    return policy.allowed_next(normalized.tag)


# ---------------------------------------------------------------------------
# Strukturelle Validierung und Guard-Bewertung
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ValidationResult:
    """Strukturiertes Validierungsergebnis ohne stille Reparatur."""

    ok: bool
    reason_codes: tuple[ReasonCode, ...]


def validate_evidence_relations(
    relations: Sequence[EvidenceRelation],
    materials: Mapping[str, MaterialRef],
    *,
    claim_id: str | None = None,
) -> ValidationResult:
    """Evidence-Relationen strukturell prüfen (kein Wahrheitsurteil).

    Mit ``claim_id`` wird zusätzlich die Claim-Bindung erzwungen: Jede Relation
    muss an genau diesen Claim gebunden sein (EVIDENCE_CLAIM_MISMATCH sonst).
    """
    codes: list[ReasonCode] = []
    ok = True
    for relation in relations:
        if relation.relation_type not in RELATION_TYPES:
            ok = False
            _append_once(codes, ReasonCode.EVENT_SCHEMA_INVALID)
        if claim_id is not None and relation.claim_id != claim_id:
            ok = False
            _append_once(codes, ReasonCode.EVIDENCE_CLAIM_MISMATCH)
        material = materials.get(relation.material_id)
        if material is None:
            ok = False
            _append_once(codes, ReasonCode.MISSING_MATERIAL)
            continue
        if normalize_trust(material.trust) == TRUST_UNTRUSTED:
            _append_once(codes, ReasonCode.UNTRUSTED_MATERIAL)
    return ValidationResult(ok=ok, reason_codes=tuple(codes))


def _append_once(codes: list[ReasonCode], code: ReasonCode) -> None:
    if code not in codes:
        codes.append(code)


def evaluate_transition_request(
    request: TransitionRequest,
    *,
    policy: ClaimPolicy,
    claims: Mapping[str, ClaimCandidate],
    materials: Mapping[str, MaterialRef],
    relations: Mapping[str, EvidenceRelation],
    decision_id: str,
    current_tags: Mapping[str, str] | None = None,
    claim_statuses: Mapping[str, str] | None = None,
) -> GuardDecision:
    """Reine Guard-Bewertung eines TransitionRequests.

    Erzeugt ausschließlich PROPOSE, HOLD oder STOP. Verändert niemals den
    Claim-Tag (Invariante 7) und synthetisiert keine HumanDecision.
    """
    codes: list[ReasonCode] = []
    stop = False
    hold = False

    claim = claims.get(request.claim_id)
    if claim is None:
        stop = True
        _append_once(codes, ReasonCode.EVENT_ORDER_INVALID)

    from_norm = normalize_claim_tag(request.from_tag, policy)
    to_norm = normalize_claim_tag(request.to_tag, policy)
    if from_norm.alias_applied or to_norm.alias_applied:
        _append_once(codes, ReasonCode.ALIAS_NORMALIZED)
    if not from_norm.known:
        stop = True
        _append_once(codes, ReasonCode.UNKNOWN_FROM_TAG)
    if not to_norm.known:
        stop = True
        _append_once(codes, ReasonCode.UNKNOWN_TO_TAG)

    if from_norm.known and to_norm.known:
        if to_norm.tag in policy.allowed_next(from_norm.tag):
            _append_once(codes, ReasonCode.POLICY_TRANSITION_ALLOWED)
        else:
            stop = True
            _append_once(codes, ReasonCode.POLICY_TRANSITION_DENIED)

    if claim is not None:
        current = None
        if current_tags is not None:
            current = current_tags.get(request.claim_id)
        if current is None:
            current = claim.claim_tag
        current_norm = normalize_claim_tag(current, policy)
        if from_norm.known and current_norm.tag != from_norm.tag:
            hold = True
            _append_once(codes, ReasonCode.EVENT_ORDER_INVALID)

        status = claim.status
        if claim_statuses is not None:
            status = claim_statuses.get(request.claim_id, status)
        if status in CONSENT_BLOCKED_STATUSES:
            stop = True
            _append_once(codes, ReasonCode.CONSENT_MISSING)
        if status == CLAIM_STATUS_RETRACTED:
            stop = True
            _append_once(codes, ReasonCode.RETRACTION_RECORDED)

        if request.visibility == VISIBILITY_PUBLIC and claim.visibility == VISIBILITY_PRIVATE:
            hold = True
            _append_once(codes, ReasonCode.VISIBILITY_VIOLATION)

    resolved: list[tuple[EvidenceRelation, MaterialRef | None]] = []
    for relation_id in request.evidence_relation_ids:
        relation = relations.get(relation_id)
        if relation is None:
            hold = True
            _append_once(codes, ReasonCode.MISSING_EVIDENCE_RELATION)
            continue
        if relation.claim_id != request.claim_id:
            # Cross-Claim-Evidenz: fail-closed, keine automatische Umhängung.
            stop = True
            _append_once(codes, ReasonCode.EVIDENCE_CLAIM_MISMATCH)
            continue
        material = materials.get(relation.material_id)
        if material is None:
            hold = True
            _append_once(codes, ReasonCode.MISSING_MATERIAL)
            continue
        resolved.append((relation, material))

    if to_norm.known and to_norm.tag in PROMOTION_TAGS:
        if not request.evidence_relation_ids:
            hold = True
            _append_once(codes, ReasonCode.MISSING_EVIDENCE_RELATION)
        promotion_capable = 0
        for relation, material in resolved:
            if material is None:
                continue
            if material.kind.strip().lower() in NON_EVIDENCE_MATERIAL_KINDS:
                hold = True
                _append_once(codes, ReasonCode.METAPHOR_IS_NOT_EVIDENCE)
                continue
            if relation.relation_type not in PROMOTION_CAPABLE_RELATION_TYPES:
                _append_once(codes, ReasonCode.PROVENANCE_IS_NOT_EVIDENCE)
                continue
            if normalize_trust(material.trust) == TRUST_UNTRUSTED:
                _append_once(codes, ReasonCode.UNTRUSTED_MATERIAL)
                continue
            promotion_capable += 1
        if resolved and promotion_capable == 0:
            # Nur Metapher-, Provenienz- oder Untrusted-Material: gebundene Grenze.
            hold = True

    if stop:
        decision = GUARD_STOP
    elif hold:
        decision = GUARD_HOLD
    else:
        decision = GUARD_PROPOSE
        _append_once(codes, ReasonCode.HUMAN_DECISION_REQUIRED)

    return GuardDecision(
        decision_id=decision_id,
        schema_version=ERK_SCHEMA_VERSION,
        request_id=request.request_id,
        decision=decision,
        reason_codes=[code.value for code in codes],
        policy_version=policy.version,
        policy_digest=policy.digest,
        actor="erk.guard",
        origin="computational",
        visibility=request.visibility,
        status="RECORDED",
    )


# ---------------------------------------------------------------------------
# Menschliche Entscheidung, Retagging, Retraction
# ---------------------------------------------------------------------------


def record_human_decision(
    decision: HumanDecision,
    *,
    requests: Mapping[str, TransitionRequest],
    guard_decisions: Mapping[str, GuardDecision],
) -> HumanDecision:
    """Menschliche Entscheidung strukturell validieren (niemals synthetisieren).

    ``human_actor`` is an asserted actor label, not authenticated human
    identity: Der Kernel authentifiziert die Person hinter dem Label nicht.

    APPROVE gilt nur als anwendbare Freigabe, wenn für denselben Request eine
    konkrete GuardDecision(PROPOSE) existiert. REJECT, DEFER und WITHDRAW
    dürfen als Entscheidungsgeschichte auch ohne anwendbares Proposal
    aufgezeichnet werden.
    """
    if decision.decision not in HUMAN_DECISION_VALUES:
        raise EvidenceRoutingError(
            f"unknown human decision value: {decision.decision!r}",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )
    if decision.request_id not in requests:
        raise EvidenceRoutingError(
            f"human decision references unknown request: {decision.request_id!r}",
            [ReasonCode.EVENT_ORDER_INVALID],
        )
    if decision.decision == HUMAN_APPROVE and not any(
        gd.request_id == decision.request_id and gd.decision == GUARD_PROPOSE
        for gd in guard_decisions.values()
    ):
        raise EvidenceRoutingError(
            f"approve without PROPOSE guard decision for request: {decision.request_id!r}",
            [ReasonCode.EVENT_ORDER_INVALID],
        )
    return decision


def apply_approved_transition(
    request: TransitionRequest,
    *,
    policy: ClaimPolicy,
    claims: Mapping[str, ClaimCandidate],
    guard_decision: GuardDecision,
    human_decision: HumanDecision,
    human_decisions: Sequence[HumanDecision] = (),
    retractions: Sequence[Retraction] = (),
    current_tags: Mapping[str, str] | None = None,
    claim_statuses: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """CLAIM_RETAGGED-Payload nur unter allen v0.1a-Bedingungen erzeugen.

    Fail-closed: jede verletzte Bedingung führt zu EvidenceRoutingError.
    Die Funktion verändert selbst keinen Zustand und schreibt kein Event.
    """
    claim = claims.get(request.claim_id)
    if claim is None:
        raise EvidenceRoutingError(
            f"claim does not exist: {request.claim_id!r}", [ReasonCode.EVENT_ORDER_INVALID]
        )
    if guard_decision.request_id != request.request_id:
        raise EvidenceRoutingError(
            "guard decision does not belong to this request", [ReasonCode.EVENT_ORDER_INVALID]
        )
    if human_decision.request_id != request.request_id:
        raise EvidenceRoutingError(
            "human decision does not belong to this request", [ReasonCode.EVENT_ORDER_INVALID]
        )
    if guard_decision.decision != GUARD_PROPOSE:
        raise EvidenceRoutingError(
            f"guard decision is not PROPOSE: {guard_decision.decision!r}",
            [ReasonCode.HUMAN_DECISION_REQUIRED],
        )
    if human_decision.decision != HUMAN_APPROVE:
        raise EvidenceRoutingError(
            f"human decision is not APPROVE: {human_decision.decision!r}",
            [ReasonCode.HUMAN_DECISION_REQUIRED],
        )

    from_norm = normalize_claim_tag(request.from_tag, policy)
    to_norm = normalize_claim_tag(request.to_tag, policy)
    if not from_norm.known or not to_norm.known:
        raise EvidenceRoutingError(
            "transition uses unknown tags",
            [ReasonCode.UNKNOWN_FROM_TAG if not from_norm.known else ReasonCode.UNKNOWN_TO_TAG],
        )
    if to_norm.tag not in policy.allowed_next(from_norm.tag):
        raise EvidenceRoutingError(
            f"policy edge no longer allowed: {from_norm.tag} -> {to_norm.tag}",
            [ReasonCode.POLICY_TRANSITION_DENIED],
        )
    if guard_decision.policy_digest != policy.digest:
        raise EvidenceRoutingError(
            "policy digest changed since guard decision (drift must be re-evaluated)",
            [ReasonCode.POLICY_DIGEST_MISMATCH],
        )

    for later in human_decisions:
        if (
            later.request_id == request.request_id
            and later.decision == HUMAN_WITHDRAW
            and later.decided_at >= human_decision.decided_at
        ):
            raise EvidenceRoutingError(
                "approval was withdrawn by a later human decision",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
    for retraction in retractions:
        if retraction.claim_id == request.claim_id:
            raise EvidenceRoutingError(
                "claim has a recorded retraction", [ReasonCode.RETRACTION_RECORDED]
            )

    status = claim.status
    if claim_statuses is not None:
        status = claim_statuses.get(request.claim_id, status)
    if status in CONSENT_BLOCKED_STATUSES:
        raise EvidenceRoutingError(
            "required consent is missing or revoked", [ReasonCode.CONSENT_MISSING]
        )
    if status == CLAIM_STATUS_RETRACTED:
        raise EvidenceRoutingError("claim has been retracted", [ReasonCode.RETRACTION_RECORDED])
    if request.visibility == VISIBILITY_PUBLIC and claim.visibility == VISIBILITY_PRIVATE:
        raise EvidenceRoutingError(
            "public transition on private claim violates visibility boundary",
            [ReasonCode.VISIBILITY_VIOLATION],
        )

    current = None
    if current_tags is not None:
        current = current_tags.get(request.claim_id)
    if current is None:
        current = claim.claim_tag
    current_norm = normalize_claim_tag(current, policy)
    if current_norm.tag != from_norm.tag:
        raise EvidenceRoutingError(
            f"claim tag moved since request: current={current_norm.tag} from={from_norm.tag}",
            [ReasonCode.EVENT_ORDER_INVALID],
        )

    return {
        "schema_version": ERK_SCHEMA_VERSION,
        "claim_id": request.claim_id,
        "from_tag": from_norm.tag,
        "to_tag": to_norm.tag,
        "request_id": request.request_id,
        "guard_decision_id": guard_decision.decision_id,
        "human_decision_id": human_decision.decision_id,
        "policy_version": policy.version,
        "policy_digest": policy.digest,
        "reason_codes": [
            ReasonCode.HUMAN_APPROVED.value,
            ReasonCode.POLICY_TRANSITION_ALLOWED.value,
        ],
        "actor": human_decision.human_actor,
        "visibility": request.visibility,
        "status": "APPLIED",
    }


_RETAG_PAYLOAD_FIELDS = frozenset(
    {
        "schema_version",
        "claim_id",
        "from_tag",
        "to_tag",
        "request_id",
        "guard_decision_id",
        "human_decision_id",
        "policy_version",
        "policy_digest",
        "reason_codes",
        "actor",
        "visibility",
        "status",
    }
)


def record_retraction(
    retraction: Retraction,
    *,
    claims: Mapping[str, ClaimCandidate],
) -> Retraction:
    """Retraction validieren; löscht nichts, erzeugt nur neuen append-only Zustand."""
    if retraction.claim_id not in claims:
        raise EvidenceRoutingError(
            f"retraction references unknown claim: {retraction.claim_id!r}",
            [ReasonCode.EVENT_ORDER_INVALID],
        )
    return retraction


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------


@dataclass
class ReplayState:
    """Deterministisch rekonstruierter Zustand eines persistierten Eventstreams."""

    schema_version: str = ERK_SCHEMA_VERSION
    claims: dict[str, dict[str, Any]] = field(default_factory=dict)
    materials: dict[str, dict[str, Any]] = field(default_factory=dict)
    relations: dict[str, dict[str, Any]] = field(default_factory=dict)
    requests: dict[str, dict[str, Any]] = field(default_factory=dict)
    guard_decisions: dict[str, dict[str, Any]] = field(default_factory=dict)
    human_decisions: dict[str, dict[str, Any]] = field(default_factory=dict)
    retractions: dict[str, dict[str, Any]] = field(default_factory=dict)
    retag_history: list[dict[str, Any]] = field(default_factory=list)
    rejected_events: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    policy_version: str | None = None
    policy_digest: str | None = None

    @property
    def state_digest(self) -> str:
        return compute_state_digest(self)

    def current_tag(self, claim_id: str) -> str | None:
        record = self.claims.get(claim_id)
        if record is None:
            return None
        tag = record.get("current_tag")
        return tag if isinstance(tag, str) else None


def _reject(
    state: ReplayState, event: Mapping[str, Any], codes: Sequence[ReasonCode], note: str
) -> None:
    """Event sichtbar quarantänisieren — keine stille Reparatur, kein Verlust."""
    state.rejected_events.append(
        {
            "event_type": event.get("type"),
            "event_id": event.get("event_id"),
            "reason_codes": [code.value for code in codes],
            "note": note,
        }
    )


def _human_decisions_for_request(state: ReplayState, request_id: str) -> list[dict[str, Any]]:
    return [
        record
        for record in state.human_decisions.values()
        if record.get("request_id") == request_id
    ]


def replay_events(
    events: Sequence[Mapping[str, Any]],
    *,
    policy: ClaimPolicy | None = None,
) -> ReplayState:
    """Persistierten, geordneten Eventstream deterministisch replayen.

    Derselbe Stream plus dieselbe Policy ergeben denselben ReplayState und
    denselben state_digest (Invariante 10). Unzulässige Reihenfolgen werden
    fail-closed als rejected_events sichtbar gehalten.
    """
    # Replay is an enforcement boundary, not a policy-free deserializer. When
    # callers do not supply an explicit historical policy, use the repository
    # policy and bind every applied retag to it.
    if policy is None:
        policy = load_claim_policy()
    state = ReplayState(policy_version=policy.version, policy_digest=policy.digest)

    for event in events:
        if not isinstance(event, Mapping):
            state.rejected_events.append(
                {
                    "event_type": None,
                    "event_id": None,
                    "reason_codes": [ReasonCode.EVENT_SCHEMA_INVALID.value],
                    "note": "event envelope is not a mapping",
                }
            )
            continue
        event_type = event.get("type")
        payload = event.get("payload")
        if (
            not isinstance(event_type, str)
            or not isinstance(payload, Mapping)
            or not set(event) <= _ENVELOPE_ALLOWED_KEYS
        ):
            _reject(state, event, [ReasonCode.EVENT_SCHEMA_INVALID], "invalid event envelope")
            continue
        if event_type not in ERK_EVENT_TYPES:
            _reject(state, event, [ReasonCode.UNKNOWN_EVENT_TYPE], "unknown event type")
            continue

        try:
            _apply_event(state, event, event_type, payload, policy)
        except EvidenceRoutingError as exc:
            _reject(state, event, exc.reason_codes or [ReasonCode.EVENT_SCHEMA_INVALID], str(exc))

    return state


def _apply_event(
    state: ReplayState,
    event: Mapping[str, Any],
    event_type: str,
    payload: Mapping[str, Any],
    policy: ClaimPolicy,
) -> None:
    if event_type == EVENT_MATERIAL_REGISTERED:
        material = model_from_payload(MaterialRef, payload)
        if material.material_id in state.materials:
            raise EvidenceRoutingError(
                f"duplicate material_id: {material.material_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        record = material.to_payload()
        normalized_trust = normalize_trust(material.trust)
        if normalized_trust != material.trust:
            state.warnings.append(
                f"material {material.material_id}: unknown trust "
                f"{material.trust!r} normalized to UNTRUSTED"
            )
        record["trust"] = normalized_trust
        state.materials[material.material_id] = record
        return

    if event_type == EVENT_CLAIM_CREATED:
        claim = model_from_payload(ClaimCandidate, payload)
        if claim.claim_id in state.claims:
            raise EvidenceRoutingError(
                f"duplicate claim_id: {claim.claim_id}", [ReasonCode.DUPLICATE_STABLE_ID]
            )
        normalized = normalize_claim_tag(claim.claim_tag, policy)
        if not normalized.known:
            raise EvidenceRoutingError(
                f"claim uses unknown tag: {claim.claim_tag!r}",
                [ReasonCode.UNKNOWN_FROM_TAG],
            )
        if normalized.alias_applied:
            state.warnings.append(
                f"claim {claim.claim_id}: tag alias {claim.claim_tag!r} "
                f"normalized to {normalized.tag!r}"
            )
        current_tag = normalized.tag
        record = claim.to_payload()
        record["current_tag"] = current_tag
        record["retracted"] = False
        state.claims[claim.claim_id] = record
        return

    if event_type == EVENT_EVIDENCE_RELATION_RECORDED:
        relation = model_from_payload(EvidenceRelation, payload)
        if relation.relation_id in state.relations:
            raise EvidenceRoutingError(
                f"duplicate relation_id: {relation.relation_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        if relation.claim_id not in state.claims:
            raise EvidenceRoutingError(
                f"relation before claim creation: {relation.claim_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        if relation.material_id not in state.materials:
            raise EvidenceRoutingError(
                f"relation references unknown material: {relation.material_id}",
                [ReasonCode.MISSING_MATERIAL],
            )
        if relation.relation_type not in RELATION_TYPES:
            raise EvidenceRoutingError(
                f"unknown relation_type: {relation.relation_type}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
        state.relations[relation.relation_id] = relation.to_payload()
        return

    if event_type == EVENT_TRANSITION_REQUESTED:
        request = model_from_payload(TransitionRequest, payload)
        if request.request_id in state.requests:
            raise EvidenceRoutingError(
                f"duplicate request_id: {request.request_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        if request.claim_id not in state.claims:
            raise EvidenceRoutingError(
                f"transition request before claim creation: {request.claim_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        for relation_id in request.evidence_relation_ids:
            relation_record = state.relations.get(relation_id)
            if relation_record is not None and relation_record.get("claim_id") != request.claim_id:
                # Cross-Claim-Evidenz fail-closed sichtbar machen, nicht umhängen.
                raise EvidenceRoutingError(
                    f"request {request.request_id} references evidence of another claim: "
                    f"{relation_id}",
                    [ReasonCode.EVIDENCE_CLAIM_MISMATCH],
                )
        state.requests[request.request_id] = request.to_payload()
        return

    if event_type == EVENT_GUARD_DECISION_RECORDED:
        guard = model_from_payload(GuardDecision, payload)
        if guard.decision_id in state.guard_decisions:
            raise EvidenceRoutingError(
                f"duplicate guard decision_id: {guard.decision_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        if guard.request_id not in state.requests:
            raise EvidenceRoutingError(
                f"guard decision for unknown request: {guard.request_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        if guard.decision not in GUARD_DECISION_VALUES:
            raise EvidenceRoutingError(
                f"unknown guard decision value: {guard.decision}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
        if guard.policy_digest != policy.digest or guard.policy_version != policy.version:
            # Drift sichtbar machen, nie still akzeptieren (Invariante 12).
            state.warnings.append(
                f"guard decision {guard.decision_id}: "
                f"{ReasonCode.POLICY_DIGEST_MISMATCH.value} "
                f"(recorded={guard.policy_version}/{guard.policy_digest} "
                f"loaded={policy.version}/{policy.digest})"
            )
        state.guard_decisions[guard.decision_id] = guard.to_payload()
        return

    if event_type == EVENT_HUMAN_DECISION_RECORDED:
        human = model_from_payload(HumanDecision, payload)
        if human.decision_id in state.human_decisions:
            # Entscheidungsgeschichte ist append-only über NEUE IDs; dieselbe
            # decision_id darf keine zweite Entscheidung simulieren.
            raise EvidenceRoutingError(
                f"duplicate human decision_id: {human.decision_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        if human.request_id not in state.requests:
            raise EvidenceRoutingError(
                f"human decision for unknown request: {human.request_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        if human.decision not in HUMAN_DECISION_VALUES:
            raise EvidenceRoutingError(
                f"unknown human decision value: {human.decision}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
        if human.decision == HUMAN_APPROVE and not any(
            record.get("request_id") == human.request_id and record.get("decision") == GUARD_PROPOSE
            for record in state.guard_decisions.values()
        ):
            # APPROVE ist nur als Freigabe eines konkreten Proposals anwendbar;
            # REJECT/DEFER/WITHDRAW bleiben als Entscheidungsgeschichte zulässig.
            raise EvidenceRoutingError(
                f"approve without PROPOSE guard decision for request: {human.request_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        prior = _human_decisions_for_request(state, human.request_id)
        if human.decision == HUMAN_APPROVE and any(
            record.get("decision") == HUMAN_WITHDRAW for record in prior
        ):
            raise EvidenceRoutingError(
                "approve after withdrawal is not a valid order",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        state.human_decisions[human.decision_id] = human.to_payload()
        return

    if event_type == EVENT_CLAIM_RETAGGED:
        _apply_retag_event(state, payload, policy)
        return

    if event_type == EVENT_RETRACTION_RECORDED:
        retraction = model_from_payload(Retraction, payload)
        if retraction.retraction_id in state.retractions:
            raise EvidenceRoutingError(
                f"duplicate retraction_id: {retraction.retraction_id}",
                [ReasonCode.DUPLICATE_STABLE_ID],
            )
        claim_record = state.claims.get(retraction.claim_id)
        if claim_record is None:
            raise EvidenceRoutingError(
                f"retraction for unknown claim: {retraction.claim_id}",
                [ReasonCode.EVENT_ORDER_INVALID],
            )
        # Append-only: Historie bleibt vollständig, nur der Status ändert sich.
        state.retractions[retraction.retraction_id] = retraction.to_payload()
        claim_record["retracted"] = True
        claim_record["status"] = CLAIM_STATUS_RETRACTED
        return

    raise EvidenceRoutingError(
        f"unhandled event type: {event_type}", [ReasonCode.UNKNOWN_EVENT_TYPE]
    )


def _model_from_state_record(cls: type, record: Mapping[str, Any]) -> Any:
    """Rebuild a closed kernel model from a replay record's model fields."""
    spec = _MODEL_SPECS[cls]
    try:
        payload = {name: record[name] for name in spec}
    except KeyError as exc:
        raise EvidenceRoutingError(
            f"stored {cls.__name__} record is incomplete: {exc.args[0]}",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        ) from exc
    return model_from_payload(cls, payload)


def _apply_retag_event(state: ReplayState, payload: Mapping[str, Any], policy: ClaimPolicy) -> None:
    # Vollständiges Feldschema: exakt die definierten Retag-Felder, keine Teilmenge.
    if set(payload) != _RETAG_PAYLOAD_FIELDS:
        missing = sorted(_RETAG_PAYLOAD_FIELDS - set(payload))
        unknown = sorted(set(payload) - _RETAG_PAYLOAD_FIELDS)
        raise EvidenceRoutingError(
            f"retag payload field set invalid (missing={missing} unknown={unknown})",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )
    for name in sorted(_RETAG_PAYLOAD_FIELDS - {"reason_codes"}):
        if not isinstance(payload[name], str):
            raise EvidenceRoutingError(
                f"retag payload field must be a string: {name}",
                [ReasonCode.EVENT_SCHEMA_INVALID],
            )
    reason_codes = payload["reason_codes"]
    if not isinstance(reason_codes, (list, tuple)) or not all(
        isinstance(code, str) and code in _KNOWN_REASON_CODES for code in reason_codes
    ):
        raise EvidenceRoutingError(
            "retag payload reason_codes must be a list of known codes",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )
    required_retag_codes = {
        ReasonCode.HUMAN_APPROVED.value,
        ReasonCode.POLICY_TRANSITION_ALLOWED.value,
    }
    if not required_retag_codes <= set(reason_codes):
        raise EvidenceRoutingError(
            "retag payload is missing required approval reason codes",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )
    if payload["schema_version"] != ERK_SCHEMA_VERSION or payload["status"] != "APPLIED":
        raise EvidenceRoutingError(
            "retag payload schema_version or status is invalid",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )
    if payload["visibility"] not in KNOWN_VISIBILITIES:
        raise EvidenceRoutingError(
            "retag payload visibility is invalid",
            [ReasonCode.EVENT_SCHEMA_INVALID],
        )

    claim_id = payload["claim_id"]
    request_id = payload["request_id"]
    claim_record = state.claims.get(claim_id)
    if claim_record is None:
        raise EvidenceRoutingError(
            f"retag before claim creation: {claim_id}", [ReasonCode.EVENT_ORDER_INVALID]
        )
    if claim_record.get("retracted"):
        raise EvidenceRoutingError(
            f"retag after retraction: {claim_id}", [ReasonCode.RETRACTION_RECORDED]
        )
    request_record = state.requests.get(request_id)
    if request_record is None:
        raise EvidenceRoutingError(
            f"retag for unknown request: {request_id}", [ReasonCode.EVENT_ORDER_INVALID]
        )
    request = _model_from_state_record(TransitionRequest, request_record)

    # Bind the mutation payload to the exact stored request. Aliases are
    # compared after normalization because generated retag payloads use the
    # canonical policy spelling.
    request_from = normalize_claim_tag(request.from_tag, policy)
    request_to = normalize_claim_tag(request.to_tag, policy)
    retag_from = normalize_claim_tag(payload["from_tag"], policy)
    retag_to = normalize_claim_tag(payload["to_tag"], policy)
    if (
        request.claim_id != claim_id
        or not request_from.known
        or not request_to.known
        or not retag_from.known
        or not retag_to.known
        or request_from.tag != retag_from.tag
        or request_to.tag != retag_to.tag
        or request.visibility != payload["visibility"]
    ):
        raise EvidenceRoutingError(
            f"retag payload does not match stored request: {request_id}",
            [ReasonCode.REQUEST_REFERENCE_MISMATCH],
        )

    # Exakte Guard-Referenz: genau die referenzierte GuardDecision muss existieren,
    # zu genau diesem Request gehören und PROPOSE sein. Irgendein anderer
    # PROPOSE-Guard für den Request genügt nicht.
    guard_id = payload["guard_decision_id"]
    guard_record = state.guard_decisions.get(guard_id)
    if (
        guard_record is None
        or guard_record.get("request_id") != request_id
        or guard_record.get("decision") != GUARD_PROPOSE
    ):
        raise EvidenceRoutingError(
            f"retag guard reference invalid: {guard_id} for request {request_id}",
            [ReasonCode.GUARD_REFERENCE_MISMATCH],
        )

    # Policy-Bindung: Retag, referenzierter Guard und geladene Policy müssen
    # dieselbe Version und denselben Digest tragen. Check drift before guard
    # recomputation so the quarantine reason remains precise.
    retag_digest = payload["policy_digest"]
    retag_policy_version = payload["policy_version"]
    if retag_digest != guard_record.get(
        "policy_digest"
    ) or retag_policy_version != guard_record.get("policy_version"):
        raise EvidenceRoutingError(
            f"retag policy differs from referenced guard decision: {guard_id}",
            [ReasonCode.POLICY_DIGEST_MISMATCH],
        )
    if retag_digest != policy.digest or retag_policy_version != policy.version:
        raise EvidenceRoutingError(
            f"retag policy differs from loaded policy (drift): {claim_id}",
            [ReasonCode.POLICY_DIGEST_MISMATCH],
        )

    # A persisted PROPOSE is historical evidence, not authority. Recompute the
    # guard against the replay state and current policy immediately before the
    # mutation, then require the stored decision to match that result exactly.
    claims = {
        stable_id: _model_from_state_record(ClaimCandidate, record)
        for stable_id, record in state.claims.items()
    }
    materials = {
        stable_id: _model_from_state_record(MaterialRef, record)
        for stable_id, record in state.materials.items()
    }
    relations = {
        stable_id: _model_from_state_record(EvidenceRelation, record)
        for stable_id, record in state.relations.items()
    }
    recomputed_guard = evaluate_transition_request(
        request,
        policy=policy,
        claims=claims,
        materials=materials,
        relations=relations,
        decision_id=guard_id,
        current_tags={
            stable_id: str(record.get("current_tag")) for stable_id, record in state.claims.items()
        },
        claim_statuses={
            stable_id: str(record.get("status")) for stable_id, record in state.claims.items()
        },
    )
    if (
        recomputed_guard.decision != GUARD_PROPOSE
        or guard_record.get("decision") != recomputed_guard.decision
        or list(guard_record.get("reason_codes", [])) != recomputed_guard.reason_codes
        or guard_record.get("policy_version") != recomputed_guard.policy_version
        or guard_record.get("policy_digest") != recomputed_guard.policy_digest
    ):
        raise EvidenceRoutingError(
            f"stored guard does not match fresh evaluation: {guard_id}",
            [ReasonCode.GUARD_REFERENCE_MISMATCH],
        )

    # Exakte Human-Referenz: genau die referenzierte HumanDecision muss existieren,
    # zum Request gehören und APPROVE sein.
    human_id = payload["human_decision_id"]
    approval = state.human_decisions.get(human_id)
    if (
        approval is None
        or approval.get("request_id") != request_id
        or approval.get("decision") != HUMAN_APPROVE
    ):
        raise EvidenceRoutingError(
            f"retag without matching human APPROVE: {request_id}",
            [ReasonCode.HUMAN_REFERENCE_MISMATCH, ReasonCode.HUMAN_DECISION_REQUIRED],
        )
    approved_at = approval.get("decided_at", 0.0)
    for record in _human_decisions_for_request(state, request_id):
        if record.get("decision") == HUMAN_WITHDRAW and record.get("decided_at", 0.0) >= float(
            approved_at
        ):
            raise EvidenceRoutingError(
                f"retag after withdrawal: {request_id}", [ReasonCode.EVENT_ORDER_INVALID]
            )

    from_tag = retag_from.tag
    to_tag = retag_to.tag
    if to_tag not in policy.allowed_next(from_tag):
        raise EvidenceRoutingError(
            f"retag edge not allowed by policy: {from_tag} -> {to_tag}",
            [ReasonCode.POLICY_TRANSITION_DENIED],
        )

    if claim_record.get("current_tag") != from_tag:
        raise EvidenceRoutingError(
            f"retag from_tag does not match current tag: {claim_id}",
            [ReasonCode.EVENT_ORDER_INVALID],
        )

    claim_record["current_tag"] = to_tag
    state.retag_history.append(
        {
            "claim_id": claim_id,
            "from_tag": from_tag,
            "to_tag": to_tag,
            "request_id": request_id,
            "guard_decision_id": guard_id,
            "human_decision_id": human_id,
            "policy_version": payload.get("policy_version"),
            "policy_digest": payload.get("policy_digest"),
        }
    )


# ---------------------------------------------------------------------------
# State-Digest und Public Export
# ---------------------------------------------------------------------------


def compute_state_digest(state: ReplayState) -> str:
    """Deterministischer Digest über die kanonisch sortierte Zustandsdarstellung.

    Bewusst getrennt vom Ledger-Hash: Der Ledger-Hash sichert die Eventkette,
    der State-Digest identifiziert den rekonstruierten Zustand. Volatile Felder
    (Objektadressen, Laufzeit) sind ausgeschlossen, weil nur serialisierte
    Inhalte eingehen.
    """
    canonical = {
        "schema_version": state.schema_version,
        "policy_version": state.policy_version,
        "policy_digest": state.policy_digest,
        "claims": state.claims,
        "materials": state.materials,
        "relations": state.relations,
        "requests": state.requests,
        "guard_decisions": state.guard_decisions,
        "human_decisions": state.human_decisions,
        "retractions": state.retractions,
        "retag_history": state.retag_history,
        "rejected_events": state.rejected_events,
        "warnings": state.warnings,
    }
    serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ReducedPublicExport:
    """Privacy-reduzierte Projektion; explizite Allowlist, kein Durchreichen."""

    export_schema_version: str
    policy_version: str | None
    policy_digest: str | None
    export_digest: str
    claims: list[dict[str, Any]]
    materials: list[dict[str, Any]]
    guard_decisions: list[dict[str, Any]]
    retractions: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _export_local_refs(ids: Sequence[str], prefix: str, letter: str) -> dict[str, str]:
    """Deterministische, exportlokale Referenzen aus kanonisch sortierten IDs.

    Die Referenz ist eine Positionskennung innerhalb dieses Exports
    (z.B. "claim:c001"). Sie wird nicht aus dem Rohwert gehasht und behauptet
    keine Anonymität — sie vermeidet nur das Durchreichen roher interner IDs.
    """
    return {
        internal_id: f"{prefix}:{letter}{index:03d}"
        for index, internal_id in enumerate(sorted(ids), start=1)
    }


def _is_publicly_exportable(record: Mapping[str, Any]) -> bool:
    """Only explicitly reduced/public records may enter a public projection."""
    return record.get("visibility") in {VISIBILITY_REDUCED, VISIBILITY_PUBLIC}


def _public_status(value: object, allowed: frozenset[str]) -> str:
    return value if isinstance(value, str) and value in allowed else "OTHER"


def _compute_export_digest(payload: Mapping[str, Any]) -> str:
    """Digest only the reduced projection; never commit to private state."""
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def reduce_public_export(state: ReplayState) -> ReducedPublicExport:
    """Public Export ausschließlich über Feld-Allowlists erzeugen.

    Standardmäßig entfallen: claim_text, Locator, Source-Pfade, Origin,
    Actor-Details, Rohmaterial, unbekannte Zusatzfelder — und rohe interne IDs
    (claim_id, material_id, request_id, decision_id, retraction_id). Interne
    Beziehungen werden über deterministische, exportlokale Referenzen
    dargestellt. Private Records werden vollständig ausgelassen. Zwei Exporte
    derselben öffentlichen Projektion sind identisch; der ``export_digest``
    bindet ausschließlich diese Projektion und verrät keine Änderung, die nur
    im privaten Replay-Zustand stattgefunden hat.
    """
    visible_claim_ids = [
        stable_id for stable_id, record in state.claims.items() if _is_publicly_exportable(record)
    ]
    visible_material_ids = [
        stable_id
        for stable_id, record in state.materials.items()
        if _is_publicly_exportable(record)
    ]
    visible_request_ids = [
        stable_id
        for stable_id, record in state.requests.items()
        if _is_publicly_exportable(record) and record.get("claim_id") in visible_claim_ids
    ]
    visible_guard_ids = [
        stable_id
        for stable_id, record in state.guard_decisions.items()
        if _is_publicly_exportable(record)
        and record.get("request_id") in visible_request_ids
        and record.get("policy_version") == state.policy_version
        and record.get("policy_digest") == state.policy_digest
    ]
    visible_retraction_ids = [
        stable_id
        for stable_id, record in state.retractions.items()
        if _is_publicly_exportable(record) and record.get("claim_id") in visible_claim_ids
    ]

    claim_refs = _export_local_refs(visible_claim_ids, "claim", "c")
    material_refs = _export_local_refs(visible_material_ids, "material", "m")
    request_refs = _export_local_refs(visible_request_ids, "request", "q")
    guard_refs = _export_local_refs(visible_guard_ids, "guard", "g")
    retraction_refs = _export_local_refs(visible_retraction_ids, "retraction", "r")

    claims = [
        {
            "claim_ref": claim_refs[claim_id],
            "schema_version": ERK_SCHEMA_VERSION,
            "claim_tag": record.get("current_tag"),
            "status": _public_status(
                record.get("status"), frozenset({CLAIM_STATUS_ACTIVE, CLAIM_STATUS_RETRACTED})
            ),
            "retracted": bool(record.get("retracted", False)),
        }
        for claim_id, record in sorted(state.claims.items())
        if claim_id in claim_refs
    ]
    materials = [
        {
            "material_ref": material_refs[material_id],
            "schema_version": ERK_SCHEMA_VERSION,
            "kind": (
                str(record.get("kind")).strip().lower()
                if str(record.get("kind")).strip().lower() in PUBLIC_MATERIAL_KINDS
                else "other"
            ),
            "trust": (
                record.get("trust")
                if record.get("trust") in KNOWN_TRUST_LEVELS
                else TRUST_UNTRUSTED
            ),
            "status": _public_status(
                record.get("status"), frozenset({CLAIM_STATUS_ACTIVE, CLAIM_STATUS_RETRACTED})
            ),
        }
        for material_id, record in sorted(state.materials.items())
        if material_id in material_refs
    ]
    guard_decisions = []
    for decision_id, record in sorted(state.guard_decisions.items()):
        if decision_id not in guard_refs:
            continue
        entry: dict[str, Any] = {
            "guard_ref": guard_refs[decision_id],
            "decision": record.get("decision"),
            "reason_codes": list(record.get("reason_codes", [])),
            "policy_version": state.policy_version,
            "policy_digest": state.policy_digest,
        }
        request_ref = request_refs.get(str(record.get("request_id")))
        if request_ref is not None:
            # Beziehung nur über die exportlokale Referenz; sonst weglassen.
            entry["request_ref"] = request_ref
        guard_decisions.append(entry)
    retractions = []
    for retraction_id, record in sorted(state.retractions.items()):
        if retraction_id not in retraction_refs:
            continue
        entry = {
            "retraction_ref": retraction_refs[retraction_id],
            "status": _public_status(record.get("status"), frozenset({"RECORDED"})),
        }
        claim_ref = claim_refs.get(str(record.get("claim_id")))
        if claim_ref is not None:
            entry["claim_ref"] = claim_ref
        retractions.append(entry)
    projection = {
        "export_schema_version": ERK_EXPORT_SCHEMA_VERSION,
        "policy_version": state.policy_version,
        "policy_digest": state.policy_digest,
        "claims": claims,
        "materials": materials,
        "guard_decisions": guard_decisions,
        "retractions": retractions,
    }
    return ReducedPublicExport(
        export_schema_version=ERK_EXPORT_SCHEMA_VERSION,
        policy_version=state.policy_version,
        policy_digest=state.policy_digest,
        export_digest=_compute_export_digest(projection),
        claims=claims,
        materials=materials,
        guard_decisions=guard_decisions,
        retractions=retractions,
    )
