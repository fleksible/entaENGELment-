"""Vertragstests für spec/runtime_eventlog_v0_1.json (issue #278, [SPEC-WIP])."""

import json
from pathlib import Path

import pytest

from tools import eventlog_spec_check as check

ROOT = Path(__file__).resolve().parents[2]
SPEC = check.load_spec()
BASE = {"event_id": "evt-1", "timestamp": 1752900000.0}


def _event(event_type, **payload):
    return {"type": event_type, **BASE, "payload": {"actor": "role:maintainer", **payload}}


VOID_CLOSED = {"void_id": "VOID-011", "closure_reason": "closing path erfüllt"}
CLAIM = {"claim_id": "clm-1", "claim_tag": "[HYPOTHESE]"}


@pytest.mark.parametrize("proof", [{"evidence_ref": "data/x.csv"}, {"review_ref": "PR #1"}])
def test_void_closed_accepts_evidence_or_review(proof):
    assert check.check_event(_event("VOID_CLOSED", **VOID_CLOSED, **proof), SPEC) == []


@pytest.mark.parametrize(
    ("event_type", "fields"),
    [
        ("VOID_CLOSED", {**VOID_CLOSED, "review_ref": "   "}),
        ("CLAIM_CREATED", {**CLAIM, "claim_text": " \t"}),
        ("CLAIM_CREATED", {**CLAIM, "claim_tag": " ", "claim_ref": "ref-1"}),
    ],
)
def test_whitespace_only_values_count_as_missing(event_type, fields):
    assert check.check_event(_event(event_type, **fields), SPEC)


def test_void_closed_without_proof_is_rejected():
    errors = check.check_event(_event("VOID_CLOSED", **VOID_CLOSED), SPEC)
    assert errors and "evidence_ref" in errors[0] and "review_ref" in errors[0]


@pytest.mark.parametrize(
    "content",
    [{"claim_text": "Satz."}, {"claim_hash": "sha256:" + "0" * 64}, {"claim_ref": "ref-1"}],
)
def test_claim_created_accepts_text_hash_or_ref(content):
    assert check.check_event(_event("CLAIM_CREATED", **CLAIM, **content), SPEC) == []


def test_claim_created_without_content_is_rejected():
    assert check.check_event(_event("CLAIM_CREATED", **CLAIM), SPEC)


def test_reduced_export_must_not_carry_claim_text():
    with_text = _event("CLAIM_CREATED", **CLAIM, claim_text="Privater Satz.")
    with_hash = _event("CLAIM_CREATED", **CLAIM, claim_hash="sha256:" + "0" * 64)
    assert check.check_event(with_text, SPEC, export=True)
    assert check.check_event(with_hash, SPEC, export=True) == []


def test_unknown_event_type_is_skipped():
    assert check.check_event({"type": "MATERIAL_REGISTERED", "payload": {}}, SPEC) is None


def test_spec_rule_structure_is_consistent():
    for name, rules in SPEC["event_types"].items():
        for group in rules.get("required_one_of", []):
            assert len(group) >= 2, name
            assert not set(group) & set(rules["required_fields"]), name
        for field in rules.get("reduced_forbidden_fields", []):
            assert field not in rules["required_fields"], name


def test_erk_fixture_events_conform_to_spec():
    """Jedes ERK-Fixture-Event aus dem Spec-Vokabular erfüllt den Vertrag.

    CLAIM_CREATED trägt claim_text im privaten Log, CLAIM_RETAGGED strukturierte
    reason_codes statt eines Freitext-reason; beides deckt required_one_of ab.
    """
    events = [
        (path.name, json.loads(line))
        for path in sorted((ROOT / "tests" / "fixtures" / "erk").glob("*.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    checked = {}
    for name, event in events:
        result = check.check_event(event, SPEC)
        if result is None:
            continue
        checked[event["type"]] = checked.get(event["type"], 0) + 1
        assert result == [], f"{name} {event['event_id']}: {result}"
    assert {"CLAIM_CREATED", "CLAIM_RETAGGED"} <= set(checked)
