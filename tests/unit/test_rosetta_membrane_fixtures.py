"""Guard tests for the Rosetta membrane translation fixtures v0.1."""

import json
from pathlib import Path

import pytest

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "narratives"
    / "grimm2"
    / "fixtures"
    / "rosetta_membrane_translation_fixtures_v0_1.json"
)

EXPECTED_IDS = {
    "same-word-different-lore",
    "different-words-preserved-relation",
    "one-to-many-translation",
    "round-trip-loss",
    "untranslated-remainder",
    "question-shift",
    "protected-origin-public-reduction",
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
    assert payload["invariants"]["humanCommitRequired"] is True
    assert payload["invariants"]["promotionEffect"] == "NONE"

    ids = {fixture["id"] for fixture in payload["fixtures"]}
    assert ids == EXPECTED_IDS
    assert len(payload["fixtures"]) == 7


def test_every_fixture_is_question_indexed_and_hold(payload):
    for fixture in payload["fixtures"]:
        provenance = fixture["questionProvenance"]
        assert provenance["questionId"].strip()
        assert provenance["askedByRef"].strip()
        assert provenance["questionTextRef"].strip()
        assert fixture["expected"]["verdict"] == "HOLD"


def test_same_word_does_not_create_translation(by_id):
    fixture = by_id["same-word-different-lore"]
    assert fixture["sourceItems"] == fixture["targetItems"]
    assert fixture["translationEdges"] == []
    assert fixture["expected"]["translationEstablished"] is False
    assert fixture["expected"]["identityClaim"] is False


def test_different_words_may_preserve_relation_without_promotion(by_id):
    fixture = by_id["different-words-preserved-relation"]
    edge = fixture["translationEdges"][0]

    assert edge["sourceRef"] != edge["targetRef"]
    assert edge["preservedRelation"].strip()
    assert edge["knownLoss"]
    assert fixture["expected"]["translationCandidate"] is True
    assert fixture["expected"]["identityClaim"] is False
    assert fixture["expected"]["promotion"] is False


def test_one_to_many_stays_non_functional_and_ambiguous(by_id):
    fixture = by_id["one-to-many-translation"]
    edges = fixture["translationEdges"]
    sources = [edge["sourceRef"] for edge in edges]
    targets = [edge["targetRef"] for edge in edges]

    assert len(set(sources)) == 1
    assert len(set(targets)) > 1
    assert fixture["expected"]["cardinality"] == "ONE_TO_MANY"
    assert fixture["expected"]["functionLike"] is False
    assert fixture["expected"]["ambiguityPreserved"] is True


def test_round_trip_loss_is_explicit(by_id):
    fixture = by_id["round-trip-loss"]
    expected = fixture["expected"]

    assert expected["roundTripIdentity"] is False
    assert expected["originalRef"] != expected["returnedRef"]
    assert fixture["translationEdges"][0]["knownLoss"]
    assert fixture["reverseTranslation"]["knownLoss"]


def test_untranslated_remainder_is_not_autofilled(by_id):
    fixture = by_id["untranslated-remainder"]

    translated_sources = {edge["sourceRef"] for edge in fixture["translationEdges"]}
    assert set(fixture["untranslatedSource"]).isdisjoint(translated_sources)
    assert fixture["untranslatedSource"]
    assert fixture["expected"]["loreCompletionForbidden"] is True
    assert fixture["expected"]["remainderStatus"] == "OPEN_KENOGRAM"


def test_question_shift_changes_edge_set_without_erasing_overlap(by_id):
    fixture = by_id["question-shift"]
    first, second = fixture["contexts"]

    pairs1 = {(edge["sourceRef"], edge["targetRef"]) for edge in first["translationEdges"]}
    pairs2 = {(edge["sourceRef"], edge["targetRef"]) for edge in second["translationEdges"]}

    assert pairs1 != pairs2
    assert pairs1 & pairs2 == {("a1", "b1")}
    assert fixture["expected"]["contextIndexed"] is True
    assert fixture["expected"]["edgeSetsEqual"] is False


def test_protected_origin_reduces_public_output_without_reconstruction(by_id):
    fixture = by_id["protected-origin-public-reduction"]
    serialized = json.dumps(fixture, ensure_ascii=False)

    assert fixture["protectedOrigin"] is True
    assert fixture["publicReconstructionAllowed"] is False
    assert fixture["expected"]["publicRelationAllowed"] is True
    assert fixture["expected"]["originReconstructionForbidden"] is True
    assert fixture["expected"]["promotion"] is False
    assert "biographical particulars" in serialized.lower()


@pytest.mark.parametrize("fixture_id", sorted(EXPECTED_IDS))
def test_translation_edges_never_hide_known_loss(by_id, fixture_id):
    fixture = by_id[fixture_id]
    for edge in fixture.get("translationEdges", []):
        assert isinstance(edge["knownLoss"], list)
        assert edge["knownLoss"]
        assert all(isinstance(item, str) and item.strip() for item in edge["knownLoss"])
