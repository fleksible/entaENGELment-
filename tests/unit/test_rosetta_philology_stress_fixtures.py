"""Guard tests for Rosetta taxonomy and philology stress fixtures v0.1."""

import json
from pathlib import Path

import pytest

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "narratives"
    / "grimm2"
    / "fixtures"
    / "rosetta_philology_stress_fixtures_v0_1.json"
)

EXPECTED_IDS = {
    "ousia-split-stress",
    "energeia-reader-rebinding",
    "logos-relational-role",
    "hen-agathon-interpretive-synthesis",
    "universal-harmony-collapse",
}

CARDINALITIES = {
    "ONE_TO_ONE",
    "ONE_TO_MANY",
    "MANY_TO_ONE",
    "MANY_TO_MANY",
}

COVERAGE = {
    "TOTAL_WITHIN_SCOPE",
    "PARTIAL_WITHIN_SCOPE",
    "NO_MAPPING_FOUND_WITHIN_SCOPE",
}

ATTRIBUTION_FACTORS = {
    "INTERPRETER",
    "LANGUAGE_AFFORDANCE",
    "HISTORICAL_PATH",
    "EDITORIAL_CHOICE",
    "READER_REBINDING",
}

ATTRIBUTION_STATUS = {
    "SUPPORTED",
    "PARTIAL",
    "CONTESTED",
    "UNKNOWN",
}


@pytest.fixture(scope="module")
def payload():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def by_id(payload):
    return {fixture["id"]: fixture for fixture in payload["fixtures"]}


def test_fixture_inventory_and_global_guards(payload):
    assert payload["schemaVersion"] == "0.1"
    assert payload["authorityStatus"] == "DERIVED"
    assert payload["invariants"]["observedDeltaNotKnownCause"] is True
    assert payload["invariants"]["mappingCardinalityNotSemanticIdentity"] is True
    assert payload["invariants"]["promotionEffect"] == "NONE"
    assert payload["invariants"]["humanCommitRequired"] is True

    ids = {fixture["id"] for fixture in payload["fixtures"]}
    assert ids == EXPECTED_IDS
    assert len(payload["fixtures"]) == 5


def test_every_fixture_keeps_question_provenance_and_no_promotion(payload):
    for fixture in payload["fixtures"]:
        provenance = fixture["questionProvenance"]
        assert provenance["questionId"].strip()
        assert provenance["askedByRef"].strip()
        assert provenance["questionTextRef"].strip()
        assert fixture["expected"]["promotion"] is False
        assert fixture["expected"]["verdict"] in {"HOLD", "STOP"}


def test_transformation_delta_is_small_and_actor_neutral(payload):
    for fixture in payload["fixtures"]:
        delta = fixture["transformationDelta"]
        assert set(delta) == {"preserved", "lost", "introduced"}
        assert all(isinstance(delta[key], list) for key in delta)


def test_mapping_topology_is_separate_and_typed(payload):
    for fixture in payload["fixtures"]:
        topology = fixture["mappingTopology"]
        assert topology["cardinality"] in CARDINALITIES
        assert topology["coverage"] in COVERAGE


def test_attribution_is_optional_but_typed(payload):
    for fixture in payload["fixtures"]:
        for candidate in fixture.get("attributionCandidates", []):
            assert candidate["factor"] in ATTRIBUTION_FACTORS
            assert candidate["status"] in ATTRIBUTION_STATUS
            assert isinstance(candidate["evidenceRefs"], list)
            assert isinstance(candidate["counterevidenceRefs"], list)


def test_ousia_models_split_without_assigning_cause(by_id):
    fixture = by_id["ousia-split-stress"]
    assert fixture["mappingTopology"]["cardinality"] == "ONE_TO_MANY"
    assert fixture["expected"]["semanticIdentity"] is False
    assert fixture["expected"]["causationAssigned"] is False

    factor_status_pairs = {
        (candidate["factor"], candidate["status"])
        for candidate in fixture["attributionCandidates"]
    }
    assert ("LANGUAGE_AFFORDANCE", "PARTIAL") in factor_status_pairs


def test_energeia_reader_rebinding_is_a_new_event(by_id):
    fixture = by_id["energeia-reader-rebinding"]
    later = fixture["laterEvent"]

    assert later["kind"] == "READER_REBINDING"
    assert later["sourceVersionRef"] != later["targetVersionRef"]
    assert fixture["expected"]["readerEventSeparate"] is True
    assert fixture["expected"]["sourceIntentionRecovered"] is False

    introduced = later["transformationDelta"]["introduced"]
    assert "modern physical-science sense as default reading" in introduced


def test_logos_requires_context_before_gloss_equivalence(by_id):
    fixture = by_id["logos-relational-role"]
    assert fixture["mappingTopology"]["cardinality"] == "ONE_TO_MANY"
    assert fixture["expected"]["requiresContext"] is True
    assert fixture["expected"]["lexicalInvariantSufficient"] is False


def test_hen_agathon_keeps_interpretive_path_visible(by_id):
    fixture = by_id["hen-agathon-interpretive-synthesis"]
    assert fixture["mappingTopology"]["cardinality"] == "MANY_TO_ONE"
    assert fixture["expected"]["lexicalIdentity"] is False
    assert fixture["expected"]["sourceAttributionAllowed"] is False
    assert fixture["expected"]["pathMustRemainVisible"] is True

    introduced = fixture["transformationDelta"]["introduced"]
    target = "unqualified identity attribution to the earliest source"
    assert target in introduced


def test_universal_harmony_collapse_fails_closed(by_id):
    fixture = by_id["universal-harmony-collapse"]
    assert fixture["expected"]["verdict"] == "STOP"
    assert fixture["expected"]["distinctionErasure"] is True
    assert fixture["expected"]["equivalenceClosureAllowed"] is False
    assert fixture["invalidDerivation"] == "A = B = C = D"
