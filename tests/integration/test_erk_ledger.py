"""Integrationstests: Evidence Routing Kernel v0.1a über die öffentliche Ledger-Event-API."""

import json
from pathlib import Path

import pytest

from src.core.evidence_routing import replay_events
from src.core.ledger import Ledger, load_ledger, verify_chain_from_file

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "erk"


def load_fixture(name):
    events = []
    with open(FIXTURES / name, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def test_generic_event_appends_jsonl_with_valid_chain(tmp_path):
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    for fixture_event in load_fixture("allowed_proposal.jsonl"):
        ledger.event(
            fixture_event["type"],
            fixture_event["payload"],
            event_id=fixture_event["event_id"],
            timestamp=fixture_event["timestamp"],
        )

    assert ledger.verify_chain() is True
    assert verify_chain_from_file(path) is True
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 5


def test_explicit_event_id_and_timestamp_are_respected(tmp_path):
    ledger = Ledger(tmp_path / "erk_events.jsonl")
    event = ledger.event(
        "CLAIM_CREATED", {"claim_id": "clm-x"}, event_id="evt-fixed", timestamp=1752900001.0
    )
    assert event.event_id == "evt-fixed"
    assert event.timestamp == 1752900001.0


def test_non_serializable_payload_fails_closed(tmp_path):
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    with pytest.raises(ValueError):
        ledger.event("CLAIM_CREATED", {"claim_id": object()})
    # Nichts wurde angehängt:
    assert ledger.get_events() == []
    assert not path.exists() or path.read_text(encoding="utf-8") == ""


def test_invalid_event_type_fails_closed(tmp_path):
    ledger = Ledger(tmp_path / "erk_events.jsonl")
    with pytest.raises(ValueError):
        ledger.event("", {"claim_id": "clm-x"})
    with pytest.raises(ValueError):
        ledger.event("CLAIM_CREATED", ["not", "a", "mapping"])


def test_payload_mutation_after_emit_does_not_change_stored_event(tmp_path):
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    payload = {"claim_id": "clm-001", "nested": {"claim_tag": "[HYPOTHESE]"}}
    event = ledger.event("CLAIM_CREATED", payload)

    payload["claim_id"] = "clm-MUTATED"
    payload["nested"]["claim_tag"] = "[CANON]"

    assert event.payload["claim_id"] == "clm-001"
    assert event.payload["nested"]["claim_tag"] == "[HYPOTHESE]"
    stored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert stored["payload"]["claim_id"] == "clm-001"
    assert stored["payload"]["nested"]["claim_tag"] == "[HYPOTHESE]"
    assert ledger.verify_chain() is True
    assert verify_chain_from_file(path) is True


def test_ledger_file_roundtrip_replays_to_expected_state(tmp_path):
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    for fixture_event in load_fixture("human_approved_retag.jsonl"):
        ledger.event(
            fixture_event["type"],
            fixture_event["payload"],
            event_id=fixture_event["event_id"],
            timestamp=fixture_event["timestamp"],
        )

    loaded = load_ledger(path)
    state = replay_events(loaded)
    assert state.current_tag("clm-001") == "[MODEL]"
    assert state.rejected_events == []

    # Derselbe persistierte Stream ergibt denselben State-Digest:
    assert replay_events(load_ledger(path)).state_digest == state.state_digest


def test_ledger_hash_chain_and_state_digest_are_distinct_concepts(tmp_path):
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    for fixture_event in load_fixture("human_approved_retag.jsonl"):
        ledger.event(
            fixture_event["type"],
            fixture_event["payload"],
            event_id=fixture_event["event_id"],
            timestamp=fixture_event["timestamp"],
        )

    state = replay_events(load_ledger(path))
    last_event_hash = ledger.get_events()[-1]["hash"]

    # Ledger-Hash sichert die Eventkette; State-Digest identifiziert den
    # rekonstruierten Zustand — zwei getrennte Funktionen, zwei Werte.
    assert last_event_hash != state.state_digest

    # Der Replay-State-Digest hängt nicht von Ledger-Hash-Feldern ab: ein
    # direkter Fixture-Replay (ohne hash/prev_hash) ergibt denselben Digest.
    fixture_state = replay_events(load_fixture("human_approved_retag.jsonl"))
    assert fixture_state.state_digest == state.state_digest


def test_metric_and_gate_semantics_unchanged(tmp_path):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.metric("mzm.phi", 0.85)
    ledger.gate("mzm_gate_v1", passed=True, reason="PASS_ALL_CONSTRAINTS")
    ledger.event("CLAIM_CREATED", {"claim_id": "clm-001"})

    types = [event["type"] for event in ledger.get_events()]
    assert types == ["metric", "gate", "CLAIM_CREATED"]
    assert ledger.verify_chain() is True
    assert verify_chain_from_file(path) is True
