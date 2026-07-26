"""
src/core/evidence_bridge_adapter.py

Dual-Format Claim Bridge Adapter v0.1 (M1 -> ERK).

Übersetzt einen Bridge-Record — die dokumentierte Übertragung *einer* Eigenschaft
aus einem Quellregister in ein Zielregister — in Vorschlagsobjekte des Evidence
Routing Kernel: ``MaterialRef``, ``EvidenceRelation`` und optional
``ClaimCandidate``.

Architekturgrenze (siehe docs/annex/DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER_v0_1.md):

- Der Adapter ist **reine Übersetzung**: kein Ledger-Event, kein Dateizugriff,
  kein Netzwerk, keine Zustandsänderung.
- Er behauptet **keine Registergleichheit**. Eine Brücke überträgt eine benannte
  Eigenschaft unter sichtbarem Verlust — nicht Identität.
- Metapher, Mythos, UI und Psychologie können **nie** eine promotionsfähige
  Relation erzeugen (``metaphor_not_evidence``).
- Physische und biologische Register brauchen einen M5-Review-Pointer, bevor sie
  promotionsfähig werden — kein Weg an der methodischen Prüfung vorbei.
- ``known_loss`` ist Pflicht: Eine Übersetzung, die den Verlust verschweigt,
  wird verweigert.
- Das Tag ``[FACT]`` vergibt der Adapter niemals selbst.

Der Kernel bleibt unverändert; dieses Modul importiert ihn nur.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from .evidence_routing import (
    ERK_SCHEMA_VERSION,
    KNOWN_VISIBILITIES,
    NON_EVIDENCE_MATERIAL_KINDS,
    PROMOTION_CAPABLE_RELATION_TYPES,
    RELATION_TYPES,
    TRUST_UNTRUSTED,
    VISIBILITY_PRIVATE,
    ClaimCandidate,
    ClaimPolicy,
    EvidenceRelation,
    MaterialRef,
    ReasonCode,
    normalize_claim_tag,
    normalize_trust,
)

BRIDGE_SCHEMA_VERSION = "bridge.v0.1"

# ---------------------------------------------------------------------------
# Quellregister und ihre erlaubte relationale Reichweite
# ---------------------------------------------------------------------------

REGISTER_MYTH = "myth"
REGISTER_METAPHOR = "metaphor"
REGISTER_FORMAL = "formal"
REGISTER_PHYSICAL = "physical"
REGISTER_BIOLOGICAL = "biological"
REGISTER_PSYCHOLOGICAL = "psychological"
REGISTER_GOVERNANCE = "governance"
REGISTER_UI = "ui"

KNOWN_SOURCE_REGISTERS = frozenset(
    {
        REGISTER_MYTH,
        REGISTER_METAPHOR,
        REGISTER_FORMAL,
        REGISTER_PHYSICAL,
        REGISTER_BIOLOGICAL,
        REGISTER_PSYCHOLOGICAL,
        REGISTER_GOVERNANCE,
        REGISTER_UI,
    }
)

# Register, deren Material per Definition keine Evidenz trägt. Ihr MaterialRef
# erhält eine ``kind``-Angabe aus NON_EVIDENCE_MATERIAL_KINDS, sodass auch der
# Kernel-Guard unabhängig vom Adapter greift (Invariante 3).
NON_EVIDENCE_REGISTERS = frozenset({REGISTER_MYTH, REGISTER_METAPHOR})

# Register, die erst nach dokumentierter methodischer Prüfung (M5) eine
# promotionsfähige Relation tragen dürfen.
M5_GATED_REGISTERS = frozenset({REGISTER_PHYSICAL, REGISTER_BIOLOGICAL})

# Register ohne jede promotionsfähige Reichweite: Sie können Kontext geben oder
# motivieren, aber niemals stützen oder messen.
NON_PROMOTING_REGISTERS = frozenset(
    {REGISTER_MYTH, REGISTER_METAPHOR, REGISTER_PSYCHOLOGICAL, REGISTER_UI}
)

# Relationen, die ohne weitere Prüfung immer zulässig sind.
CONTEXT_ONLY_RELATIONS = frozenset({"MOTIVATES", "CONTEXTUALIZES", "PROVENANCE_ONLY"})

# Materialart je Register für den erzeugten MaterialRef.
_REGISTER_MATERIAL_KIND = {
    REGISTER_MYTH: "metaphor",
    REGISTER_METAPHOR: "metaphor",
    REGISTER_FORMAL: "specification",
    REGISTER_PHYSICAL: "measurement",
    REGISTER_BIOLOGICAL: "measurement",
    REGISTER_PSYCHOLOGICAL: "note",
    REGISTER_GOVERNANCE: "document",
    REGISTER_UI: "note",
}

# Der Adapter darf diese Tags nicht selbst vergeben: Sie behaupten eine Geltung,
# die nur nach Evidenz und menschlicher Entscheidung entsteht.
ADAPTER_FORBIDDEN_CLAIM_TAGS = frozenset({"[FACT]", "[SPEC]", "[CANON]"})

INTENDED_USES = frozenset({"explain", "generate", "test", "visualize"})


class BridgeReason(str, Enum):
    """Adapter-lokale Befunde.

    Bewusst getrennt von :class:`~src.core.evidence_routing.ReasonCode`: Diese
    Werte erscheinen ausschließlich im Rückgabeobjekt der Übersetzung, niemals
    in einem Ledger-Event, in ``EvidenceRelation.reason_codes`` oder in einem
    Claim. Sie sind kein Projektstatus und kein Claim-Tag.
    """

    UNKNOWN_SOURCE_REGISTER = "UNKNOWN_SOURCE_REGISTER"
    UNKNOWN_RELATION_TYPE = "UNKNOWN_RELATION_TYPE"
    REGISTER_CANNOT_PROMOTE = "REGISTER_CANNOT_PROMOTE"
    M5_REVIEW_REQUIRED = "M5_REVIEW_REQUIRED"
    KNOWN_LOSS_REQUIRED = "KNOWN_LOSS_REQUIRED"
    FALSIFIER_REQUIRED = "FALSIFIER_REQUIRED"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"
    TRANSFERRED_PROPERTY_REQUIRED = "TRANSFERRED_PROPERTY_REQUIRED"
    PRESERVED_RELATION_REQUIRED = "PRESERVED_RELATION_REQUIRED"
    ADAPTER_CANNOT_ASSIGN_TAG = "ADAPTER_CANNOT_ASSIGN_TAG"
    UNKNOWN_CLAIM_TAG = "UNKNOWN_CLAIM_TAG"
    UNKNOWN_INTENDED_USE = "UNKNOWN_INTENDED_USE"
    UNKNOWN_VISIBILITY = "UNKNOWN_VISIBILITY"
    SOURCE_POINTER_REQUIRED = "SOURCE_POINTER_REQUIRED"


class BridgeAdapterError(ValueError):
    """Fail-closed Fehler der Übersetzung mit adapter-lokalen Befunden."""

    def __init__(self, message: str, reasons: Sequence[BridgeReason] = ()) -> None:
        super().__init__(message)
        self.reasons: tuple[BridgeReason, ...] = tuple(reasons)


# ---------------------------------------------------------------------------
# Eingabemodell
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BridgeRecord:
    """Dokumentierte Übertragung *einer* Eigenschaft zwischen zwei Registern.

    Die Pflichtfelder entsprechen den sechs Brückenfragen: Was ist die
    Quellform? Welche Eigenschaft wird übertragen? Welche Relation bleibt
    erhalten? Was geht verloren? Woran würde die Brücke scheitern? Wie wird sie
    zurückgenommen?
    """

    bridge_id: str
    source_register: str
    source_pointer: str
    source_digest: str
    transferred_property: str
    preserved_relation: str
    relation_type: str
    known_loss: list[str]
    falsifier: str
    rollback: str
    intended_use: str = "explain"
    protected_origin: bool = False
    visibility: str = "reduced"
    actor: str = "role:maintainer"
    claim_id: str | None = None
    proposed_claim_tag: str | None = None
    claim_text: str = ""
    m5_review_pointer: str | None = None
    schema_version: str = BRIDGE_SCHEMA_VERSION


@dataclass(frozen=True)
class BridgeTranslation:
    """Ergebnis einer Übersetzung — Vorschläge, kein Vollzug."""

    bridge_id: str
    schema_version: str
    material: MaterialRef
    relation: EvidenceRelation
    claim: ClaimCandidate | None
    promotion_capable: bool
    notes: tuple[BridgeReason, ...] = field(default=())

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "bridge_id": self.bridge_id,
            "schema_version": self.schema_version,
            "material": asdict(self.material),
            "relation": asdict(self.relation),
            "claim": asdict(self.claim) if self.claim is not None else None,
            "promotion_capable": self.promotion_capable,
            "notes": [note.value for note in self.notes],
        }
        return data


# ---------------------------------------------------------------------------
# Validierung
# ---------------------------------------------------------------------------


def _require_text(value: object, reason: BridgeReason, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BridgeAdapterError(f"{label} is required and must be non-empty", [reason])
    return value.strip()


def validate_bridge_record(record: BridgeRecord, *, policy: ClaimPolicy | None = None) -> None:
    """Strukturelle Vollständigkeit und Registergrenzen prüfen (fail-closed).

    Prüft nicht, ob eine behauptete Relation sachlich trägt — das bleibt
    menschliche Review-Arbeit (und für Messfragen: M5).
    """
    if record.source_register not in KNOWN_SOURCE_REGISTERS:
        raise BridgeAdapterError(
            f"unknown source_register: {record.source_register!r}",
            [BridgeReason.UNKNOWN_SOURCE_REGISTER],
        )
    if record.relation_type not in RELATION_TYPES:
        raise BridgeAdapterError(
            f"unknown relation_type: {record.relation_type!r}",
            [BridgeReason.UNKNOWN_RELATION_TYPE],
        )
    if record.intended_use not in INTENDED_USES:
        raise BridgeAdapterError(
            f"unknown intended_use: {record.intended_use!r}",
            [BridgeReason.UNKNOWN_INTENDED_USE],
        )
    if record.visibility not in KNOWN_VISIBILITIES:
        raise BridgeAdapterError(
            f"unknown visibility: {record.visibility!r}", [BridgeReason.UNKNOWN_VISIBILITY]
        )

    _require_text(record.source_pointer, BridgeReason.SOURCE_POINTER_REQUIRED, "source_pointer")
    _require_text(
        record.transferred_property,
        BridgeReason.TRANSFERRED_PROPERTY_REQUIRED,
        "transferred_property",
    )
    _require_text(
        record.preserved_relation,
        BridgeReason.PRESERVED_RELATION_REQUIRED,
        "preserved_relation",
    )
    _require_text(record.falsifier, BridgeReason.FALSIFIER_REQUIRED, "falsifier")
    _require_text(record.rollback, BridgeReason.ROLLBACK_REQUIRED, "rollback")

    # Known Loss ist Pflicht: Eine Brücke ohne sichtbaren Verlust behauptet
    # implizit Verlustfreiheit — und damit Identität.
    if not record.known_loss or not all(
        isinstance(item, str) and item.strip() for item in record.known_loss
    ):
        raise BridgeAdapterError(
            "known_loss must list at least one concrete loss",
            [BridgeReason.KNOWN_LOSS_REQUIRED],
        )

    _validate_register_reach(record)
    _validate_proposed_tag(record, policy)


def _validate_register_reach(record: BridgeRecord) -> None:
    """Erzwingt, wie weit ein Quellregister relational reichen darf."""
    if record.relation_type not in PROMOTION_CAPABLE_RELATION_TYPES:
        return

    if record.source_register in NON_PROMOTING_REGISTERS:
        reason = (
            BridgeReason.REGISTER_CANNOT_PROMOTE
            if record.source_register not in NON_EVIDENCE_REGISTERS
            else BridgeReason.REGISTER_CANNOT_PROMOTE
        )
        raise BridgeAdapterError(
            f"source_register {record.source_register!r} cannot carry a "
            f"promotion-capable relation ({record.relation_type}); "
            f"allowed: {sorted(CONTEXT_ONLY_RELATIONS)}",
            [reason],
        )

    if record.source_register in M5_GATED_REGISTERS and not (
        isinstance(record.m5_review_pointer, str) and record.m5_review_pointer.strip()
    ):
        raise BridgeAdapterError(
            f"source_register {record.source_register!r} requires a documented "
            "m5_review_pointer before a promotion-capable relation is allowed",
            [BridgeReason.M5_REVIEW_REQUIRED],
        )


def _validate_proposed_tag(record: BridgeRecord, policy: ClaimPolicy | None) -> None:
    if record.proposed_claim_tag is None:
        return
    tag = record.proposed_claim_tag
    if policy is not None:
        normalized = normalize_claim_tag(tag, policy)
        if not normalized.known:
            raise BridgeAdapterError(
                f"unknown claim tag: {tag!r}", [BridgeReason.UNKNOWN_CLAIM_TAG]
            )
        tag = normalized.tag
    if tag in ADAPTER_FORBIDDEN_CLAIM_TAGS:
        raise BridgeAdapterError(
            f"adapter must not assign claim tag {tag!r}; it requires evidence "
            "and an explicit human decision",
            [BridgeReason.ADAPTER_CANNOT_ASSIGN_TAG],
        )


# ---------------------------------------------------------------------------
# Übersetzung
# ---------------------------------------------------------------------------


def _derive_id(prefix: str, bridge_id: str) -> str:
    digest = hashlib.sha256(f"{prefix}:{bridge_id}".encode()).hexdigest()[:12]
    return f"{prefix}-bridge-{digest}"


def translate_bridge_record(
    record: BridgeRecord,
    *,
    policy: ClaimPolicy | None = None,
    trust: str = TRUST_UNTRUSTED,
) -> BridgeTranslation:
    """Bridge-Record in ERK-Vorschläge übersetzen.

    Erzeugt ``MaterialRef``, ``EvidenceRelation`` und optional
    ``ClaimCandidate``. Es wird **kein** Event emittiert, nichts geschrieben und
    kein Claim-Tag verändert. Der Aufrufer entscheidet, ob und wann die
    Vorschläge über den Kernel laufen — dort greifen Guard und HumanDecision
    unverändert.

    Args:
        record: vollständiger Bridge-Record.
        policy: optionale Claim-Policy für Tag-Normalisierung.
        trust: Trust-Level des Materials; Default ``UNTRUSTED`` (G5).

    Raises:
        BridgeAdapterError: bei jeder strukturellen oder registerbezogenen
            Verletzung — fail-closed, keine stille Reparatur.
    """
    validate_bridge_record(record, policy=policy)

    notes: list[BridgeReason] = []

    # protected_origin überschreibt die Sichtbarkeit nach unten, nie nach oben.
    visibility = VISIBILITY_PRIVATE if record.protected_origin else record.visibility

    material_kind = _REGISTER_MATERIAL_KIND[record.source_register]
    normalized_trust = normalize_trust(trust)

    material = MaterialRef(
        material_id=_derive_id("mat", record.bridge_id),
        schema_version=ERK_SCHEMA_VERSION,
        kind=material_kind,
        source=f"bridge:{record.source_register}",
        revision="r0",
        # Nur Pointer und Digest — niemals der Quellausdruck selbst.
        locator=record.source_pointer,
        digest=record.source_digest,
        origin="dual_format_bridge",
        actor=record.actor,
        trust=normalized_trust,
        visibility=visibility,
        status="ACTIVE",
    )

    claim_id = record.claim_id or _derive_id("clm", record.bridge_id)

    # Kernel-Reason-Codes: nur solche, die der Kernel selbst kennt. Der
    # Adapter erfindet hier nichts.
    relation_reasons: list[str] = []
    if material_kind in NON_EVIDENCE_MATERIAL_KINDS:
        relation_reasons.append(ReasonCode.METAPHOR_IS_NOT_EVIDENCE.value)
        notes.append(BridgeReason.REGISTER_CANNOT_PROMOTE)
    if record.relation_type == "PROVENANCE_ONLY":
        relation_reasons.append(ReasonCode.PROVENANCE_IS_NOT_EVIDENCE.value)
    if normalized_trust == TRUST_UNTRUSTED:
        relation_reasons.append(ReasonCode.UNTRUSTED_MATERIAL.value)

    relation = EvidenceRelation(
        relation_id=_derive_id("rel", record.bridge_id),
        schema_version=ERK_SCHEMA_VERSION,
        claim_id=claim_id,
        material_id=material.material_id,
        relation_type=record.relation_type,
        actor=record.actor,
        origin="dual_format_bridge",
        visibility=visibility,
        status="ACTIVE",
        reason_codes=relation_reasons,
    )

    claim: ClaimCandidate | None = None
    if record.proposed_claim_tag is not None:
        tag = record.proposed_claim_tag
        if policy is not None:
            tag = normalize_claim_tag(tag, policy).tag
        claim = ClaimCandidate(
            claim_id=claim_id,
            schema_version=ERK_SCHEMA_VERSION,
            claim_text=record.claim_text,
            claim_tag=tag,
            actor=record.actor,
            origin="dual_format_bridge",
            visibility=visibility,
            status="ACTIVE",
            material_refs=[material.material_id],
        )

    promotion_capable = (
        record.relation_type in PROMOTION_CAPABLE_RELATION_TYPES
        and material_kind not in NON_EVIDENCE_MATERIAL_KINDS
        and normalized_trust != TRUST_UNTRUSTED
    )

    return BridgeTranslation(
        bridge_id=record.bridge_id,
        schema_version=BRIDGE_SCHEMA_VERSION,
        material=material,
        relation=relation,
        claim=claim,
        promotion_capable=promotion_capable,
        notes=tuple(notes),
    )


def bridge_record_from_mapping(payload: Mapping[str, Any]) -> BridgeRecord:
    """Bridge-Record aus einem Mapping bauen (geschlossenes Feldschema)."""
    allowed = set(BridgeRecord.__dataclass_fields__)
    unknown = set(payload) - allowed
    if unknown:
        raise BridgeAdapterError(
            f"bridge record has unknown fields: {sorted(unknown)}",
            [BridgeReason.UNKNOWN_RELATION_TYPE],
        )
    data = dict(payload)
    known_loss = data.get("known_loss", [])
    if isinstance(known_loss, (list, tuple)):
        data["known_loss"] = list(known_loss)
    return BridgeRecord(**data)
