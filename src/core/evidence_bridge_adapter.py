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
from dataclasses import MISSING, asdict, dataclass, field, fields
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
# promotionsfähige Relation tragen dürfen. In v0.1 sind das die einzigen
# Register, die überhaupt promotionsfähig werden können.
M5_GATED_REGISTERS = frozenset({REGISTER_PHYSICAL, REGISTER_BIOLOGICAL})

# Register ohne jede promotionsfähige Reichweite — auch später nicht. Sie können
# Kontext geben oder motivieren, aber niemals stützen oder messen.
NON_PROMOTING_REGISTERS = frozenset(
    {REGISTER_MYTH, REGISTER_METAPHOR, REGISTER_PSYCHOLOGICAL, REGISTER_UI}
)

# Register, die in v0.1 nur Kontext und Provenienz tragen, deren spätere
# Öffnung aber an eine benannte Bedingung geknüpft ist. Der Kernel prüft für
# ``PROPOSE`` strukturell nur Relationstyp, Materialart und Trust — ein
# ``REVIEWED``-Dokument könnte dort sonst ein grünes Signal erhalten, das seine
# Reichweite überschätzt. Bis die jeweilige Bindung existiert: kein Proposal.
DEFERRED_PROMOTION_REGISTERS = {
    REGISTER_FORMAL: (
        "Öffnung erst mit formalem Review-Witness und gebundener Zieldomäne "
        "(target_register/claim_domain); niemals pauschal MEASURES"
    ),
    REGISTER_GOVERNANCE: (
        "Öffnung höchstens für IMPLEMENTS innerhalb explizit dokumentierter "
        "Authority-/Scope-Grenzen"
    ),
}

# Relationen, die ohne weitere Prüfung immer zulässig sind.
CONTEXT_ONLY_RELATIONS = frozenset({"MOTIVATES", "CONTEXTUALIZES", "PROVENANCE_ONLY"})

_REGISTER_ALLOWED_RELATIONS = {
    REGISTER_MYTH: CONTEXT_ONLY_RELATIONS,
    REGISTER_METAPHOR: CONTEXT_ONLY_RELATIONS,
    REGISTER_FORMAL: CONTEXT_ONLY_RELATIONS,
    REGISTER_PHYSICAL: CONTEXT_ONLY_RELATIONS | PROMOTION_CAPABLE_RELATION_TYPES,
    REGISTER_BIOLOGICAL: CONTEXT_ONLY_RELATIONS | PROMOTION_CAPABLE_RELATION_TYPES,
    REGISTER_PSYCHOLOGICAL: CONTEXT_ONLY_RELATIONS,
    REGISTER_GOVERNANCE: CONTEXT_ONLY_RELATIONS,
    REGISTER_UI: CONTEXT_ONLY_RELATIONS,
}

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
    PROMOTION_NOT_ENABLED_IN_V0_1 = "PROMOTION_NOT_ENABLED_IN_V0_1"
    M5_REVIEW_REQUIRED = "M5_REVIEW_REQUIRED"
    KNOWN_LOSS_REQUIRED = "KNOWN_LOSS_REQUIRED"
    KNOWN_LOSS_MUST_BE_LIST = "KNOWN_LOSS_MUST_BE_LIST"
    SOURCE_DIGEST_REQUIRED = "SOURCE_DIGEST_REQUIRED"
    FALSIFIER_REQUIRED = "FALSIFIER_REQUIRED"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"
    TRANSFERRED_PROPERTY_REQUIRED = "TRANSFERRED_PROPERTY_REQUIRED"
    PRESERVED_RELATION_REQUIRED = "PRESERVED_RELATION_REQUIRED"
    ADAPTER_CANNOT_ASSIGN_TAG = "ADAPTER_CANNOT_ASSIGN_TAG"
    UNKNOWN_CLAIM_TAG = "UNKNOWN_CLAIM_TAG"
    UNKNOWN_INTENDED_USE = "UNKNOWN_INTENDED_USE"
    UNKNOWN_VISIBILITY = "UNKNOWN_VISIBILITY"
    SOURCE_POINTER_REQUIRED = "SOURCE_POINTER_REQUIRED"
    BRIDGE_ID_REQUIRED = "BRIDGE_ID_REQUIRED"
    ACTOR_REQUIRED = "ACTOR_REQUIRED"
    CLAIM_ID_REQUIRED = "CLAIM_ID_REQUIRED"
    CLAIM_TEXT_REQUIRED = "CLAIM_TEXT_REQUIRED"
    CLAIM_POLICY_REQUIRED = "CLAIM_POLICY_REQUIRED"
    UNSUPPORTED_SCHEMA_VERSION = "UNSUPPORTED_SCHEMA_VERSION"
    RELATION_NOT_ALLOWED_FOR_REGISTER = "RELATION_NOT_ALLOWED_FOR_REGISTER"
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_MAPPING = "INVALID_MAPPING"
    INVALID_BOOLEAN = "INVALID_BOOLEAN"


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
class BridgeContext:
    """Die sechs Brückenfragen, die mit der Übersetzung erhalten bleiben.

    Ohne diesen Kontext wäre die Übersetzung eine Behauptung ohne Beschriftung:
    Man sähe die Relation, aber weder die übertragene Eigenschaft noch den
    Verlust, den Falsifikator, den Rücknahmeweg — und bei physischen Registern
    auch nicht, warum das M5-Gate passiert werden durfte.
    """

    source_register: str
    transferred_property: str
    preserved_relation: str
    known_loss: tuple[str, ...]
    falsifier: str
    rollback: str
    intended_use: str
    protected_origin: bool
    m5_review_pointer: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_register": self.source_register,
            "transferred_property": self.transferred_property,
            "preserved_relation": self.preserved_relation,
            "known_loss": list(self.known_loss),
            "falsifier": self.falsifier,
            "rollback": self.rollback,
            "intended_use": self.intended_use,
            "protected_origin": self.protected_origin,
            "m5_review_pointer": self.m5_review_pointer,
        }


@dataclass(frozen=True)
class BridgeTranslation:
    """Ergebnis einer Übersetzung — Vorschläge, kein Vollzug."""

    bridge_id: str
    schema_version: str
    material: MaterialRef
    relation: EvidenceRelation
    claim: ClaimCandidate | None
    promotion_capable: bool
    context: BridgeContext
    notes: tuple[BridgeReason, ...] = field(default=())

    @property
    def known_loss(self) -> tuple[str, ...]:
        """Der benannte Verlust bleibt am Ergebnis sichtbar."""
        return self.context.known_loss

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "bridge_id": self.bridge_id,
            "schema_version": self.schema_version,
            "material": asdict(self.material),
            "relation": asdict(self.relation),
            "claim": asdict(self.claim) if self.claim is not None else None,
            "promotion_capable": self.promotion_capable,
            "context": self.context.to_dict(),
            "notes": [note.value for note in self.notes],
        }
        return data


# ---------------------------------------------------------------------------
# Validierung
# ---------------------------------------------------------------------------


def _require_text(value: object, reason: BridgeReason, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise BridgeAdapterError(f"{label} is required and must be non-empty", [reason])
    return value.strip()


def _require_canonical_text(value: object, reason: BridgeReason, label: str) -> str:
    text = _require_text(value, reason, label)
    if value != text:
        raise BridgeAdapterError(
            f"{label} must not contain leading or trailing whitespace",
            [reason],
        )
    return text


def validate_bridge_record(record: BridgeRecord, *, policy: ClaimPolicy | None = None) -> None:
    """Strukturelle Vollständigkeit und Registergrenzen prüfen (fail-closed).

    Prüft nicht, ob eine behauptete Relation sachlich trägt — das bleibt
    menschliche Review-Arbeit (und für Messfragen: M5).
    """
    if type(record) is not BridgeRecord:
        raise BridgeAdapterError(
            "record must be a BridgeRecord; use bridge_record_from_mapping for JSON data",
            [BridgeReason.INVALID_MAPPING],
        )
    if type(record.schema_version) is not str or (record.schema_version != BRIDGE_SCHEMA_VERSION):
        raise BridgeAdapterError(
            f"schema_version must equal {BRIDGE_SCHEMA_VERSION!r}",
            [BridgeReason.UNSUPPORTED_SCHEMA_VERSION],
        )

    _require_canonical_text(record.bridge_id, BridgeReason.BRIDGE_ID_REQUIRED, "bridge_id")
    _require_canonical_text(record.actor, BridgeReason.ACTOR_REQUIRED, "actor")

    if type(record.source_register) is not str or (
        record.source_register not in KNOWN_SOURCE_REGISTERS
    ):
        raise BridgeAdapterError(
            f"unknown source_register: {record.source_register!r}",
            [BridgeReason.UNKNOWN_SOURCE_REGISTER],
        )
    if type(record.relation_type) is not str or record.relation_type not in RELATION_TYPES:
        raise BridgeAdapterError(
            f"unknown relation_type: {record.relation_type!r}",
            [BridgeReason.UNKNOWN_RELATION_TYPE],
        )
    if type(record.intended_use) is not str or record.intended_use not in INTENDED_USES:
        raise BridgeAdapterError(
            f"unknown intended_use: {record.intended_use!r}",
            [BridgeReason.UNKNOWN_INTENDED_USE],
        )
    if type(record.visibility) is not str or record.visibility not in KNOWN_VISIBILITIES:
        raise BridgeAdapterError(
            f"unknown visibility: {record.visibility!r}", [BridgeReason.UNKNOWN_VISIBILITY]
        )
    if type(record.protected_origin) is not bool:
        raise BridgeAdapterError("protected_origin must be a bool", [BridgeReason.INVALID_BOOLEAN])
    if record.claim_id is not None:
        _require_canonical_text(record.claim_id, BridgeReason.CLAIM_ID_REQUIRED, "claim_id")
    if record.m5_review_pointer is not None:
        _require_canonical_text(
            record.m5_review_pointer,
            BridgeReason.M5_REVIEW_REQUIRED,
            "m5_review_pointer",
        )

    _require_canonical_text(
        record.source_pointer,
        BridgeReason.SOURCE_POINTER_REQUIRED,
        "source_pointer",
    )
    _require_canonical_text(
        record.source_digest,
        BridgeReason.SOURCE_DIGEST_REQUIRED,
        "source_digest",
    )
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

    # Ein blanker String ist iterierbar: ohne diese Prüfung würde
    # known_loss="Kantengewichte" zeichenweise als Liste durchgehen.
    if type(record.known_loss) not in (list, tuple):
        raise BridgeAdapterError(
            "known_loss must be a list or tuple of strings, not a bare string",
            [BridgeReason.KNOWN_LOSS_MUST_BE_LIST],
        )

    # Known Loss ist Pflicht: Eine Brücke ohne sichtbaren Verlust behauptet
    # implizit Verlustfreiheit — und damit Identität.
    if not record.known_loss or not all(
        type(item) is str and item.strip() for item in record.known_loss
    ):
        raise BridgeAdapterError(
            "known_loss must list at least one concrete loss",
            [BridgeReason.KNOWN_LOSS_REQUIRED],
        )

    _validate_register_reach(record)
    _validate_proposed_tag(record, policy)


def _validate_register_reach(record: BridgeRecord) -> None:
    """Erzwingt, wie weit ein Quellregister relational reichen darf.

    Bei Verstoß wird abgebrochen, nicht abgestuft. Eine automatische
    Degradierung auf ``CONTEXTUALIZES`` wäre keine Übersetzung mehr, sondern
    eine Entscheidung: Der Aufrufer sagte ``MEASURES``. Die Korrektur ist ein
    neuer, ausdrücklich anders lautender Record — von einem Menschen.
    """
    hint = (
        f"Zulässig sind hier {sorted(CONTEXT_ONLY_RELATIONS)}. Der Adapter stuft "
        "nicht selbst ab; ein Mensch kann einen neuen Record mit ausdrücklich "
        "diesem Relationstyp einreichen."
    )

    allowed = _REGISTER_ALLOWED_RELATIONS[record.source_register]
    if record.relation_type not in allowed:
        if (
            record.relation_type in PROMOTION_CAPABLE_RELATION_TYPES
            and record.source_register in NON_PROMOTING_REGISTERS
        ):
            raise BridgeAdapterError(
                f"source_register {record.source_register!r} cannot carry a "
                f"promotion-capable relation ({record.relation_type}). {hint}",
                [BridgeReason.REGISTER_CANNOT_PROMOTE],
            )
        if (
            record.relation_type in PROMOTION_CAPABLE_RELATION_TYPES
            and record.source_register in DEFERRED_PROMOTION_REGISTERS
        ):
            condition = DEFERRED_PROMOTION_REGISTERS[record.source_register]
            raise BridgeAdapterError(
                f"source_register {record.source_register!r} is not promotion-enabled "
                f"in v0.1 ({record.relation_type}): {condition}. {hint}",
                [BridgeReason.PROMOTION_NOT_ENABLED_IN_V0_1],
            )
        raise BridgeAdapterError(
            f"relation_type {record.relation_type!r} is outside the allowed "
            f"vocabulary for source_register {record.source_register!r}. {hint}",
            [BridgeReason.RELATION_NOT_ALLOWED_FOR_REGISTER],
        )

    if (
        record.source_register in M5_GATED_REGISTERS
        and record.relation_type in PROMOTION_CAPABLE_RELATION_TYPES
        and record.m5_review_pointer is None
    ):
        raise BridgeAdapterError(
            f"source_register {record.source_register!r} requires a documented "
            f"m5_review_pointer before a promotion-capable relation is allowed. {hint}",
            [BridgeReason.M5_REVIEW_REQUIRED],
        )


def _validate_proposed_tag(record: BridgeRecord, policy: ClaimPolicy | None) -> None:
    if record.proposed_claim_tag is None:
        if record.claim_id is None:
            raise BridgeAdapterError(
                "claim_id is required when no ClaimCandidate is emitted",
                [BridgeReason.CLAIM_ID_REQUIRED],
            )
        return
    tag = _require_text(
        record.proposed_claim_tag,
        BridgeReason.UNKNOWN_CLAIM_TAG,
        "proposed_claim_tag",
    )
    _require_text(record.claim_text, BridgeReason.CLAIM_TEXT_REQUIRED, "claim_text")
    if type(policy) is not ClaimPolicy:
        raise BridgeAdapterError(
            "a loaded ClaimPolicy is required when proposing a ClaimCandidate",
            [BridgeReason.CLAIM_POLICY_REQUIRED],
        )
    normalized = normalize_claim_tag(tag, policy)
    if not normalized.known:
        raise BridgeAdapterError(f"unknown claim tag: {tag!r}", [BridgeReason.UNKNOWN_CLAIM_TAG])
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
        policy: Claim-Policy für Tag-Normalisierung; Pflicht, sobald der Record
            einen ``ClaimCandidate`` vorschlägt.
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
        # validate_bridge_record() garantiert für diesen Pfad eine geladene
        # Policy und einen bekannten, normalisierten Tag.
        assert policy is not None
        tag = normalize_claim_tag(record.proposed_claim_tag, policy).tag
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

    # Die sechs Brückenfragen bleiben am Ergebnis sichtbar — insbesondere der
    # Verlust und der Grund, aus dem ein physisches Register das Gate passierte.
    context = BridgeContext(
        source_register=record.source_register,
        transferred_property=record.transferred_property.strip(),
        preserved_relation=record.preserved_relation.strip(),
        known_loss=tuple(item.strip() for item in record.known_loss),
        falsifier=record.falsifier.strip(),
        rollback=record.rollback.strip(),
        intended_use=record.intended_use,
        protected_origin=record.protected_origin,
        m5_review_pointer=record.m5_review_pointer,
    )

    return BridgeTranslation(
        bridge_id=record.bridge_id,
        schema_version=BRIDGE_SCHEMA_VERSION,
        material=material,
        relation=relation,
        claim=claim,
        promotion_capable=promotion_capable,
        context=context,
        notes=tuple(notes),
    )


def bridge_record_from_mapping(payload: Mapping[str, Any]) -> BridgeRecord:
    """Bridge-Record aus einem Mapping bauen (geschlossenes Feldschema)."""
    if type(payload) is not dict:
        raise BridgeAdapterError(
            "bridge record payload must be a built-in dict",
            [BridgeReason.INVALID_MAPPING],
        )
    if not all(type(key) is str for key in payload):
        raise BridgeAdapterError(
            "bridge record field names must be strings",
            [BridgeReason.UNKNOWN_FIELD],
        )
    allowed = set(BridgeRecord.__dataclass_fields__)
    unknown = set(payload) - allowed
    if unknown:
        raise BridgeAdapterError(
            f"bridge record has unknown fields: {sorted(unknown)}",
            [BridgeReason.UNKNOWN_FIELD],
        )
    required = {
        item.name
        for item in fields(BridgeRecord)
        if item.default is MISSING and item.default_factory is MISSING
    }
    missing = required - set(payload)
    if missing:
        raise BridgeAdapterError(
            f"bridge record is missing required fields: {sorted(missing)}",
            [BridgeReason.MISSING_REQUIRED_FIELD],
        )
    data = dict(payload)
    known_loss = data.get("known_loss", [])
    if type(known_loss) in (list, tuple):
        data["known_loss"] = list(known_loss)
    try:
        return BridgeRecord(**data)
    except TypeError as exc:
        raise BridgeAdapterError(
            "bridge record payload does not match bridge.v0.1",
            [BridgeReason.INVALID_MAPPING],
        ) from exc
