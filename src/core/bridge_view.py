"""Read-only, fail-closed projection of an existing bridge translation.

``BRIDGE_VIEW_v0.1`` does not read files, access the network, emit events,
retag claims, authorize promotion, or mutate runtime state. It only renders
fields that already exist on a :class:`BridgeTranslation` plus an explicit,
repo-relative receipt pointer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
from typing import Any

from .evidence_bridge_adapter import (
    KNOWN_SOURCE_REGISTERS,
    M5_GATED_REGISTERS,
    NON_PROMOTING_REGISTERS,
    BridgeTranslation,
)
from .evidence_routing import PROMOTION_CAPABLE_RELATION_TYPES, RELATION_TYPES

BRIDGE_VIEW_SCHEMA_VERSION = "bridge_view.v0.1"
PROMOTION_NOT_ELIGIBLE = "NOT_ELIGIBLE"
PROMOTION_HUMAN_REVIEW = "ELIGIBLE_FOR_HUMAN_REVIEW"

_CANONICAL_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$", re.ASCII)
_CANONICAL_STATUS_RE = re.compile(r"^[A-Z][A-Z0-9_]*$", re.ASCII)
_RECEIPT_SUFFIXES = frozenset({".json", ".md", ".yaml", ".yml"})


class BridgeViewReason(str, Enum):
    """Closed reason vocabulary for projection failures."""

    INVALID_TRANSLATION = "INVALID_TRANSLATION"
    NON_CANONICAL_ID = "NON_CANONICAL_ID"
    IDENTIFIER_MISMATCH = "IDENTIFIER_MISMATCH"
    UNKNOWN_RELATION = "UNKNOWN_RELATION"
    UNKNOWN_REGISTER = "UNKNOWN_REGISTER"
    STATUS_INVALID = "STATUS_INVALID"
    STATUS_MISMATCH = "STATUS_MISMATCH"
    KNOWN_LOSS_REQUIRED = "KNOWN_LOSS_REQUIRED"
    REVIEW_POINTER_REQUIRED = "REVIEW_POINTER_REQUIRED"
    POINTER_INVALID = "POINTER_INVALID"
    PROMOTION_NOT_ALLOWED = "PROMOTION_NOT_ALLOWED"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"
    RECEIPT_REQUIRED = "RECEIPT_REQUIRED"


class BridgeViewError(ValueError):
    """Fail-closed projection error with machine-readable reasons."""

    def __init__(self, message: str, reasons: tuple[BridgeViewReason, ...]) -> None:
        super().__init__(message)
        self.reasons = reasons


@dataclass(frozen=True)
class BridgeView:
    """Human-readable projection; never an authorization or promotion."""

    schema_version: str
    source: str
    target: str
    relation: str
    register: str
    status: str
    known_loss: tuple[str, ...]
    review_pointer: str | None
    promotion_eligibility: str
    rollback: str
    receipt: str
    complete: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "register": self.register,
            "status": self.status,
            "known_loss": list(self.known_loss),
            "review_pointer": self.review_pointer,
            "promotion_eligibility": self.promotion_eligibility,
            "rollback": self.rollback,
            "receipt": self.receipt,
            "complete": self.complete,
        }


def _fail(message: str, reason: BridgeViewReason) -> None:
    raise BridgeViewError(message, (reason,))


def _require_text(value: object, *, label: str, reason: BridgeViewReason) -> str:
    if type(value) is not str or not value.strip() or value != value.strip():
        _fail(f"{label} must be non-empty canonical text", reason)
    return value


def _require_canonical_id(value: object, *, label: str) -> str:
    text = _require_text(value, label=label, reason=BridgeViewReason.NON_CANONICAL_ID)
    if _CANONICAL_ID_RE.fullmatch(text) is None:
        _fail(f"{label} is not a canonical kebab-case id", BridgeViewReason.NON_CANONICAL_ID)
    return text


def _require_repo_pointer(
    value: object,
    *,
    label: str,
    missing_reason: BridgeViewReason,
    receipt: bool = False,
) -> str:
    text = _require_text(value, label=label, reason=missing_reason)
    if "\\" in text or "://" in text:
        _fail(f"{label} must be a repo-relative pointer", BridgeViewReason.POINTER_INVALID)

    path_text, separator, fragment = text.partition("#")
    if separator and (not fragment or "#" in fragment):
        _fail(f"{label} has an invalid fragment", BridgeViewReason.POINTER_INVALID)
    segments = path_text.split("/")
    path = PurePosixPath(path_text)
    if (
        path.is_absolute()
        or not path.name
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        _fail(f"{label} must stay inside the repository", BridgeViewReason.POINTER_INVALID)
    if receipt and (segments[0] != "receipts" or path.suffix not in _RECEIPT_SUFFIXES):
        _fail(
            "receipt must point into receipts/ with a supported text suffix",
            BridgeViewReason.POINTER_INVALID,
        )
    return text


def project_bridge_view(
    translation: BridgeTranslation,
    *,
    receipt: str,
) -> BridgeView:
    """Project an already translated bridge record without side effects.

    A return value is always complete. Missing or contradictory fields raise
    ``BridgeViewError``; no partial view and no guessed downgrade is emitted.
    """

    if type(translation) is not BridgeTranslation:
        _fail(
            "translation must be a BridgeTranslation",
            BridgeViewReason.INVALID_TRANSLATION,
        )

    source = _require_canonical_id(translation.material.material_id, label="source")
    target = _require_canonical_id(translation.relation.claim_id, label="target")
    if translation.relation.material_id != source:
        _fail(
            "relation material_id does not match projected source",
            BridgeViewReason.IDENTIFIER_MISMATCH,
        )
    if translation.claim is not None and translation.claim.claim_id != target:
        _fail(
            "claim candidate id does not match projected target",
            BridgeViewReason.IDENTIFIER_MISMATCH,
        )

    relation = translation.relation.relation_type
    if type(relation) is not str or relation not in RELATION_TYPES:
        _fail(f"unknown relation: {relation!r}", BridgeViewReason.UNKNOWN_RELATION)

    register = translation.context.source_register
    if type(register) is not str or register not in KNOWN_SOURCE_REGISTERS:
        _fail(f"unknown register: {register!r}", BridgeViewReason.UNKNOWN_REGISTER)

    status = _require_text(
        translation.relation.status,
        label="status",
        reason=BridgeViewReason.STATUS_INVALID,
    )
    if _CANONICAL_STATUS_RE.fullmatch(status) is None:
        _fail("status must use the canonical uppercase vocabulary", BridgeViewReason.STATUS_INVALID)
    if translation.material.status != status:
        _fail(
            "material and relation status must match",
            BridgeViewReason.STATUS_MISMATCH,
        )

    known_loss = translation.context.known_loss
    if (
        type(known_loss) is not tuple
        or not known_loss
        or not all(
            type(item) is str and item.strip() and item == item.strip()
            for item in known_loss
        )
    ):
        _fail(
            "known_loss must contain at least one canonical text item",
            BridgeViewReason.KNOWN_LOSS_REQUIRED,
        )

    rollback = _require_text(
        translation.context.rollback,
        label="rollback",
        reason=BridgeViewReason.ROLLBACK_REQUIRED,
    )
    receipt_pointer = _require_repo_pointer(
        receipt,
        label="receipt",
        missing_reason=BridgeViewReason.RECEIPT_REQUIRED,
        receipt=True,
    )

    review_pointer = translation.context.m5_review_pointer
    if register in M5_GATED_REGISTERS and review_pointer is None:
        _fail(
            f"register {register!r} requires its documented review pointer",
            BridgeViewReason.REVIEW_POINTER_REQUIRED,
        )
    if review_pointer is not None:
        review_pointer = _require_repo_pointer(
            review_pointer,
            label="review_pointer",
            missing_reason=BridgeViewReason.REVIEW_POINTER_REQUIRED,
        )

    if (
        relation in PROMOTION_CAPABLE_RELATION_TYPES
        and register not in M5_GATED_REGISTERS
    ):
        _fail(
            f"register {register!r} may not project promotion eligibility",
            BridgeViewReason.PROMOTION_NOT_ALLOWED,
        )
    if (
        register in NON_PROMOTING_REGISTERS
        and relation in PROMOTION_CAPABLE_RELATION_TYPES
    ):
        _fail(
            f"register {register!r} is non-promoting",
            BridgeViewReason.PROMOTION_NOT_ALLOWED,
        )
    if translation.promotion_capable and relation not in PROMOTION_CAPABLE_RELATION_TYPES:
        _fail(
            "promotion flag contradicts the relation vocabulary",
            BridgeViewReason.PROMOTION_NOT_ALLOWED,
        )
    if translation.promotion_capable and register not in M5_GATED_REGISTERS:
        _fail(
            "promotion flag would create authority outside the reviewed registers",
            BridgeViewReason.PROMOTION_NOT_ALLOWED,
        )

    promotion_eligibility = (
        PROMOTION_HUMAN_REVIEW
        if translation.promotion_capable
        else PROMOTION_NOT_ELIGIBLE
    )
    return BridgeView(
        schema_version=BRIDGE_VIEW_SCHEMA_VERSION,
        source=source,
        target=target,
        relation=relation,
        register=register,
        status=status,
        known_loss=known_loss,
        review_pointer=review_pointer,
        promotion_eligibility=promotion_eligibility,
        rollback=rollback,
        receipt=receipt_pointer,
    )
