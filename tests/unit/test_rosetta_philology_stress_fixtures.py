"""Guard tests for Rosetta philology stress fixtures v0.1."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "docs" / "narratives" / "grimm2" / "fixtures"
FIXTURE_PATH = FIXTURE_DIR / "rosetta_philology_stress_fixtures_v0_1.json"


@pytest.fixture(scope="module")
def payload():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def by_id(payload):
    return {fixture["id"]: fixture for fixture in payload["fixtures"]}


def test_fixture_inventory_and_global_guards(payload):
    ids = {fixture["id"] for fixture in payload["fixtures"]}

    assert payload["schemaVersion"] == "0.1"
    assert payload["authorityStatus"] == "DERIVED"
    assert payload["invariants"]["observedDeltaNotKnownCause"] is True
    assert payload["invariants"]["mappingCardinalityNotSemanticIdentity"] is True
    assert payload["invariants"]["promotionEffect"] == "NONE"
    assert payload["invariants"]["humanCommitRequired"] is True

    assert "ousia-split-stress" in ids
    assert "energeia-reader-rebinding" in ids
    assert "logos-relational-role" in ids
    assert "hen-agathon-interpretive-synthesis" in ids
    assert "universal-harmony-collapse" in ids
    assert len(ids) == 5


def test_every_fixture_keeps_question_provenance_and_no_promotion(payload):
    for fixture in payload["fixtures"]:
        provenance = fixture["questionProvenance"]
        assert provenance["questionId"].strip()
        assert provenance["askedByRef"].strip()
        assert provenance["questionTextRef"].strip()
        assert fixture["expected"]["promotion"] is False
        assert fixture["expected"]["verdict"] in {"HOLD", "STOP"}


def test_delta_and_mapping_are_separate(payload):
    for fixture in payload["fixtures"]:
        delta = fixture["transformationDelta"]
        topology = fixture["mappingTopology"]

        assert set(delta) == {"preserved", "lost", "introduced"}
        assert topology["cardinality"].strip()
        assert topology["coverage"].strip()


def test_attribution_candidates_are_explicit(payload):
    for fixture in payload["fixtures"]:
        for candidate in fixture.get("attributionCandidates", []):
            assert candidate["factor"].strip()
            assert candidate["status"].strip()
            assert isinstance(candidate["evidenceRefs"], list)
            assert isinstance(candidate["counterevidenceRefs"], list)


def test_ousia_models_split_without_assigning_cause(by_id):
    fixture = by_id["ousia-split-stress"]
    assert fixture["mappingTopology"]["cardinality"] == "ONE_TO_MANY"
    assert fixture["expected"]["semanticIdentity"] is False
    assert fixture["expected"]["causationAssigned"] is False


def test_energeia_reader_rebinding_is_a_new_event(by_id):
    fixture = by_id["energeia-reader-rebinding"]
    later = fixture["laterEvent"]
    introduced = later["transformationDelta"]["introduced"]

    assert later["kind"] == "READER_REBINDING"
    assert later["sourceVersionRef"] != later["targetVersionRef"]
    assert fixture["expected"]["readerEventSeparate"] is True
    assert fixture["expected"]["sourceIntentionRecovered"] is False
    assert "modern physical-science sense as default reading" in introduced


def test_logos_requires_context_before_gloss_equivalence(by_id):
    fixture = by_id["logos-relational-role"]
    assert fixture["mappingTopology"]["cardinality"] == "ONE_TO_MANY"
    assert fixture["expected"]["requiresContext"] is True
    assert fixture["expected"]["lexicalInvariantSufficient"] is False


def test_hen_agathon_keeps_interpretive_path_visible(by_id):
    fixture = by_id["hen-agathon-interpretive-synthesis"]
    introduced = fixture["transformationDelta"]["introduced"]
    target = "unqualified identity attribution to the earliest source"

    assert fixture["mappingTopology"]["cardinality"] == "MANY_TO_ONE"
    assert fixture["expected"]["lexicalIdentity"] is False
    assert fixture["expected"]["sourceAttributionAllowed"] is False
    assert fixture["expected"]["pathMustRemainVisible"] is True
    assert target in introduced


def test_universal_harmony_collapse_fails_closed(by_id):
    fixture = by_id["universal-harmony-collapse"]
    assert fixture["expected"]["verdict"] == "STOP"
    assert fixture["expected"]["distinctionErasure"] is True
    assert fixture["expected"]["equivalenceClosureAllowed"] is False
    assert fixture["invalidDerivation"] == "A = B = C = D"
