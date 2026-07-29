"""Unit tests for the read-only BRIDGE_VIEW v0.1 projection."""

from dataclasses import replace

import pytest

from src.core.bridge_view import (
    PROMOTION_HUMAN_REVIEW,
    BridgeViewError,
    BridgeViewReason,
    project_bridge_view,
)
from src.core.evidence_bridge_adapter import BridgeRecord, translate_bridge_record
from src.core.evidence_routing import TRUST_REVIEWED, TRUST_UNTRUSTED

RECEIPT = "receipts/2026-07-28_void027_bridge_view_v0_1.json"


def make_record(**overrides):
    data = {
        "bridge_id": "brg-view-001",
        "source_register": "physical",
        "source_pointer": "fixtures/bridge/source-001.json",
        "source_digest": "sha256:00",
        "transferred_property": "measured ordering",
        "preserved_relation": "ordering remains visible",
        "relation_type": "SUPPORTS",
        "known_loss": ["raw samples are not included"],
        "falsifier": "the documented ordering cannot be reproduced",
        "rollback": "revert the introducing commit and withdraw the receipt",
        "claim_id": "clm-existing-001",
        "m5_review_pointer": "docs/annex/DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER_v0_1.md#m5-review",
    }
    data.update(overrides)
    return BridgeRecord(**data)


def make_translation(**overrides):
    return translate_bridge_record(make_record(**overrides), trust=TRUST_REVIEWED)


def assert_reason(excinfo, reason):
    assert reason in excinfo.value.reasons


def test_complete_valid_record_is_projected_for_human_review():
    view = project_bridge_view(make_translation(), receipt=RECEIPT)

    assert view.complete is True
    assert view.source.startswith("mat-bridge-")
    assert view.target == "clm-existing-001"
    assert view.relation == "SUPPORTS"
    assert view.register == "physical"
    assert view.status == "ACTIVE"
    assert view.known_loss == ("raw samples are not included",)
    assert view.review_pointer == "docs/annex/DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER_v0_1.md#m5-review"
    assert view.promotion_eligibility == PROMOTION_HUMAN_REVIEW


def test_missing_known_loss_fails_closed():
    translation = make_translation()
    translation = replace(
        translation,
        context=replace(translation.context, known_loss=()),
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.KNOWN_LOSS_REQUIRED)


def test_unknown_relation_is_not_guessed():
    translation = make_translation()
    translation = replace(
        translation,
        relation=replace(translation.relation, relation_type="PROVES"),
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.UNKNOWN_RELATION)


def test_noncanonical_id_is_rejected():
    translation = make_translation()
    translation = replace(
        translation,
        material=replace(translation.material, material_id="Material 01"),
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.NON_CANONICAL_ID)


def test_existing_target_id_vocabulary_is_preserved():
    view = project_bridge_view(
        make_translation(claim_id="clm-A"),
        receipt=RECEIPT,
    )

    assert view.target == "clm-A"


def test_impermissible_promotion_is_rejected():
    translation = make_translation(
        source_register="formal",
        relation_type="CONTEXTUALIZES",
        m5_review_pointer=None,
    )
    translation = replace(
        translation,
        relation=replace(translation.relation, relation_type="SUPPORTS"),
        promotion_capable=True,
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.PROMOTION_NOT_ALLOWED)


def test_untrusted_material_cannot_claim_review_eligibility():
    translation = make_translation()
    translation = replace(
        translation,
        material=replace(translation.material, trust=TRUST_UNTRUSTED),
        promotion_capable=True,
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.PROMOTION_NOT_ALLOWED)


def test_promotion_flag_must_match_reviewed_material():
    translation = replace(make_translation(), promotion_capable=False)

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.PROMOTION_NOT_ALLOWED)


def test_missing_review_pointer_is_not_silently_downgraded():
    translation = make_translation(
        relation_type="CONTEXTUALIZES",
        m5_review_pointer=None,
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.REVIEW_POINTER_REQUIRED)


def test_rollback_and_receipt_references_are_preserved_exactly():
    translation = make_translation(
        rollback="revert commit abc123 and retain its history",
    )

    view = project_bridge_view(translation, receipt=RECEIPT)

    assert view.rollback == "revert commit abc123 and retain its history"
    assert view.receipt == RECEIPT


@pytest.mark.parametrize(
    "review_pointer",
    [
        "C:/outside/review.md",
        "file:/etc/review.md",
        "https:example.com/review.md",
    ],
)
def test_uri_like_review_pointer_is_rejected(review_pointer):
    translation = make_translation()
    translation = replace(
        translation,
        context=replace(
            translation.context,
            m5_review_pointer=review_pointer,
        ),
    )

    with pytest.raises(BridgeViewError) as excinfo:
        project_bridge_view(translation, receipt=RECEIPT)
    assert_reason(excinfo, BridgeViewReason.POINTER_INVALID)
