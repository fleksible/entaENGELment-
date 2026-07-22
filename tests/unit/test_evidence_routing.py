"""Unit-Tests für den Evidence Routing Kernel v0.1a (src/core/evidence_routing.py)."""

import hashlib
import json
from pathlib import Path

import pytest

from src.core.evidence_routing import (
    DEFAULT_CLAIM_POLICY_PATH,
    GUARD_HOLD,
    GUARD_PROPOSE,
    GUARD_STOP,
    ClaimCandidate,
    EvidenceRelation,
    EvidenceRoutingError,
    HumanDecision,
    MaterialRef,
    ReasonCode,
    Retraction,
    TransitionRequest,
    apply_approved_transition,
    compute_permitted_transitions,
    compute_state_digest,
    evaluate_transition_request,
    load_claim_policy,
    model_from_payload,
    normalize_claim_tag,
    normalize_trust,
    record_retraction,
    reduce_public_export,
    replay_events,
    validate_evidence_relations,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "erk"


def load_fixture(name):
    events = []
    with open(FIXTURES / name, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def make_material(material_id="mat-001", *, kind="measurement", trust="REVIEWED", **overrides):
    data = {
        "material_id": material_id,
        "schema_version": "erk.v0.1",
        "kind": kind,
        "source": "repo",
        "revision": "r1",
        "locator": "docs/audit/example.md",
        "digest": "sha256:01",
        "origin": "repo_annex",
        "actor": "role:maintainer",
        "trust": trust,
        "visibility": "reduced",
        "status": "ACTIVE",
    }
    data.update(overrides)
    return MaterialRef(**data)


def make_claim(claim_id="clm-001", *, claim_tag="[HYPOTHESE]", **overrides):
    data = {
        "claim_id": claim_id,
        "schema_version": "erk.v0.1",
        "claim_text": "Beispiel-Claim.",
        "claim_tag": claim_tag,
        "actor": "role:maintainer",
        "origin": "repo_annex",
        "visibility": "reduced",
        "status": "ACTIVE",
        "material_refs": ["mat-001"],
    }
    data.update(overrides)
    return ClaimCandidate(**data)


def make_relation(relation_id="rel-001", *, relation_type="SUPPORTS", **overrides):
    data = {
        "relation_id": relation_id,
        "schema_version": "erk.v0.1",
        "claim_id": "clm-001",
        "material_id": "mat-001",
        "relation_type": relation_type,
        "actor": "role:maintainer",
        "origin": "repo_annex",
        "visibility": "reduced",
        "status": "ACTIVE",
        "reason_codes": [],
    }
    data.update(overrides)
    return EvidenceRelation(**data)


def make_request(request_id="req-001", *, from_tag="[HYPOTHESE]", to_tag="[MODEL]", **overrides):
    data = {
        "request_id": request_id,
        "schema_version": "erk.v0.1",
        "claim_id": "clm-001",
        "from_tag": from_tag,
        "to_tag": to_tag,
        "actor": "role:maintainer",
        "origin": "repo_annex",
        "requested_at": 1752900003.0,
        "evidence_relation_ids": ["rel-001"],
        "reason_codes": [],
        "visibility": "reduced",
        "status": "OPEN",
    }
    data.update(overrides)
    return TransitionRequest(**data)


def make_human_decision(decision_id="hd-001", *, decision="APPROVE", **overrides):
    data = {
        "decision_id": decision_id,
        "schema_version": "erk.v0.1",
        "request_id": "req-001",
        "decision": decision,
        "human_actor": "role:project_initiator",
        "decided_at": 1752900005.0,
        "reason_codes": [],
        "visibility": "reduced",
        "status": "RECORDED",
    }
    data.update(overrides)
    return HumanDecision(**data)


def evaluate(request, *, claims=None, materials=None, relations=None, policy=None):
    policy = policy or load_claim_policy()
    return evaluate_transition_request(
        request,
        policy=policy,
        claims=claims if claims is not None else {"clm-001": make_claim()},
        materials=materials if materials is not None else {"mat-001": make_material()},
        relations=relations if relations is not None else {"rel-001": make_relation()},
        decision_id="gd-test",
    )


class TestPolicyLoading:
    def test_load_claim_policy_version_and_digest(self):
        policy = load_claim_policy()
        assert policy.version == "0.2"
        expected = hashlib.sha256(DEFAULT_CLAIM_POLICY_PATH.read_bytes()).hexdigest()
        assert policy.digest == expected
        assert "[HYPOTHESE]" in policy.tags

    def test_invalid_policy_structure_fails_closed(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("just_a_string_without_tags\n", encoding="utf-8")
        with pytest.raises(EvidenceRoutingError):
            load_claim_policy(bad)


class TestNormalization:
    def test_alias_normalization(self):
        policy = load_claim_policy()
        result = normalize_claim_tag("[FAKT]", policy)
        assert result.tag == "[FACT]"
        assert result.alias_applied is True
        assert result.known is True

    def test_known_tag_passthrough(self):
        policy = load_claim_policy()
        result = normalize_claim_tag("[HYPOTHESE]", policy)
        assert result.tag == "[HYPOTHESE]"
        assert result.alias_applied is False
        assert result.known is True

    def test_unknown_tag_marked_unknown(self):
        policy = load_claim_policy()
        result = normalize_claim_tag("[TOTALLY-NEW]", policy)
        assert result.known is False

    def test_unknown_trust_becomes_untrusted(self):
        assert normalize_trust("SOMETHING_NEW") == "UNTRUSTED"
        assert normalize_trust(None) == "UNTRUSTED"
        assert normalize_trust("REVIEWED") == "REVIEWED"


class TestPermittedTransitions:
    def test_allowed_neighborhood(self):
        policy = load_claim_policy()
        assert "[MODEL]" in compute_permitted_transitions("[HYPOTHESE]", policy)
        assert "[VOID]" in compute_permitted_transitions("[HYPOTHESE]", policy)

    def test_denied_neighborhood(self):
        policy = load_claim_policy()
        assert "[CANON]" not in compute_permitted_transitions("[HYPOTHESE]", policy)

    def test_unknown_tag_fails_closed(self):
        policy = load_claim_policy()
        with pytest.raises(EvidenceRoutingError) as excinfo:
            compute_permitted_transitions("[TOTALLY-NEW]", policy)
        assert ReasonCode.UNKNOWN_FROM_TAG in excinfo.value.reason_codes


class TestGuardEvaluation:
    def test_allowed_transition_proposes(self):
        decision = evaluate(make_request())
        assert decision.decision == GUARD_PROPOSE
        assert ReasonCode.POLICY_TRANSITION_ALLOWED.value in decision.reason_codes
        assert ReasonCode.HUMAN_DECISION_REQUIRED.value in decision.reason_codes

    def test_denied_transition_stops(self):
        decision = evaluate(make_request(to_tag="[CANON]"))
        assert decision.decision == GUARD_STOP
        assert ReasonCode.POLICY_TRANSITION_DENIED.value in decision.reason_codes

    def test_unknown_from_tag_stops(self):
        decision = evaluate(
            make_request(from_tag="[TOTALLY-NEW]"),
            claims={"clm-001": make_claim(claim_tag="[TOTALLY-NEW]")},
        )
        assert decision.decision == GUARD_STOP
        assert ReasonCode.UNKNOWN_FROM_TAG.value in decision.reason_codes

    def test_unknown_to_tag_stops(self):
        decision = evaluate(make_request(to_tag="[TOTALLY-NEW]"))
        assert decision.decision == GUARD_STOP
        assert ReasonCode.UNKNOWN_TO_TAG.value in decision.reason_codes

    def test_missing_evidence_relation_holds(self):
        decision = evaluate(make_request(), relations={})
        assert decision.decision == GUARD_HOLD
        assert ReasonCode.MISSING_EVIDENCE_RELATION.value in decision.reason_codes

    def test_metaphor_material_holds(self):
        decision = evaluate(
            make_request(),
            materials={"mat-001": make_material(kind="metaphor")},
        )
        assert decision.decision == GUARD_HOLD
        assert ReasonCode.METAPHOR_IS_NOT_EVIDENCE.value in decision.reason_codes

    def test_untrusted_only_evidence_holds(self):
        decision = evaluate(
            make_request(),
            materials={"mat-001": make_material(trust="UNTRUSTED")},
        )
        assert decision.decision == GUARD_HOLD
        assert ReasonCode.UNTRUSTED_MATERIAL.value in decision.reason_codes

    def test_decision_records_policy_version_and_digest(self):
        policy = load_claim_policy()
        decision = evaluate(make_request(), policy=policy)
        assert decision.policy_version == policy.version
        assert decision.policy_digest == policy.digest


class TestValidateEvidenceRelations:
    def test_missing_material_flagged(self):
        result = validate_evidence_relations([make_relation()], {})
        assert result.ok is False
        assert ReasonCode.MISSING_MATERIAL in result.reason_codes

    def test_untrusted_material_flagged_but_structurally_ok(self):
        result = validate_evidence_relations(
            [make_relation()], {"mat-001": make_material(trust="UNTRUSTED")}
        )
        assert result.ok is True
        assert ReasonCode.UNTRUSTED_MATERIAL in result.reason_codes


class TestModelParsing:
    def test_unknown_payload_field_fails_closed(self):
        payload = make_material().to_payload()
        payload["surprise_field"] = "nope"
        with pytest.raises(EvidenceRoutingError) as excinfo:
            model_from_payload(MaterialRef, payload)
        assert ReasonCode.EVENT_SCHEMA_INVALID in excinfo.value.reason_codes

    def test_missing_required_field_fails_closed(self):
        payload = make_material().to_payload()
        del payload["digest"]
        with pytest.raises(EvidenceRoutingError):
            model_from_payload(MaterialRef, payload)

    def test_unknown_reason_code_fails_closed(self):
        payload = make_relation().to_payload()
        payload["reason_codes"] = ["FREESTYLE_CODE"]
        with pytest.raises(EvidenceRoutingError):
            model_from_payload(EvidenceRelation, payload)


class TestHumanOnlyRetagging:
    def test_apply_without_approve_fails_closed(self):
        policy = load_claim_policy()
        request = make_request()
        guard = evaluate(request, policy=policy)
        rejected = make_human_decision(decision="REJECT")
        with pytest.raises(EvidenceRoutingError) as excinfo:
            apply_approved_transition(
                request,
                policy=policy,
                claims={"clm-001": make_claim()},
                guard_decision=guard,
                human_decision=rejected,
            )
        assert ReasonCode.HUMAN_DECISION_REQUIRED in excinfo.value.reason_codes

    def test_apply_with_approve_returns_retag_payload(self):
        policy = load_claim_policy()
        request = make_request()
        guard = evaluate(request, policy=policy)
        payload = apply_approved_transition(
            request,
            policy=policy,
            claims={"clm-001": make_claim()},
            guard_decision=guard,
            human_decision=make_human_decision(),
        )
        assert payload["claim_id"] == "clm-001"
        assert payload["from_tag"] == "[HYPOTHESE]"
        assert payload["to_tag"] == "[MODEL]"
        assert ReasonCode.HUMAN_APPROVED.value in payload["reason_codes"]


class TestRetraction:
    def test_record_retraction_requires_known_claim(self):
        retraction = Retraction(
            retraction_id="ret-001",
            schema_version="erk.v0.1",
            claim_id="clm-unknown",
            actor="role:project_initiator",
            retracted_at=1752900007.0,
            reason_codes=["RETRACTION_RECORDED"],
            visibility="reduced",
            status="RECORDED",
        )
        with pytest.raises(EvidenceRoutingError):
            record_retraction(retraction, claims={})

    def test_retraction_is_non_destructive_in_replay(self):
        state = replay_events(load_fixture("retraction_non_destructive.jsonl"))
        assert state.claims["clm-001"]["retracted"] is True
        # Historie bleibt vollständig erhalten:
        assert len(state.retag_history) == 1
        assert "req-001" in state.requests
        assert "hd-001" in state.human_decisions
        assert state.rejected_events == []


class TestStateDigest:
    def test_state_digest_stable_for_identical_stream(self):
        events = load_fixture("human_approved_retag.jsonl")
        first = replay_events(events)
        second = replay_events(load_fixture("human_approved_retag.jsonl"))
        assert first.state_digest == second.state_digest
        assert compute_state_digest(first) == compute_state_digest(second)

    def test_state_digest_changes_on_state_change(self):
        base = replay_events(load_fixture("allowed_proposal.jsonl"))
        extended = replay_events(load_fixture("human_approved_retag.jsonl"))
        assert base.state_digest != extended.state_digest


class TestReducedExport:
    def test_export_contains_only_allowlisted_fields(self):
        state = replay_events(load_fixture("human_approved_retag.jsonl"))
        export = reduce_public_export(state).to_dict()
        claim_entry = export["claims"][0]
        assert set(claim_entry) == {
            "claim_ref",
            "schema_version",
            "claim_tag",
            "status",
            "retracted",
        }
        material_entry = export["materials"][0]
        assert set(material_entry) == {
            "material_ref",
            "schema_version",
            "kind",
            "trust",
            "status",
        }

    def test_export_excludes_private_content(self):
        state = replay_events(load_fixture("private_reduced_export.jsonl"))
        export = reduce_public_export(state).to_dict()
        serialized = json.dumps(export)
        assert export["claims"] == []
        assert export["materials"] == []
        assert export["guard_decisions"] == []
        assert export["retractions"] == []
        assert "PRIVATE_TEXT" not in serialized
        assert "/private/diary" not in serialized
        assert "biographical" not in serialized
        assert "initiator_private_name" not in serialized
        assert "private_chat" not in serialized

    def test_private_only_changes_do_not_change_public_projection_or_digest(self):
        first_events = load_fixture("private_reduced_export.jsonl")
        second_events = load_fixture("private_reduced_export.jsonl")
        second_events[1]["payload"]["claim_text"] = "A completely different private sentence"
        second_events[0]["payload"]["kind"] = "private category with identifying detail"

        first = reduce_public_export(replay_events(first_events)).to_dict()
        second = reduce_public_export(replay_events(second_events)).to_dict()
        assert first == second
        assert first["export_digest"] == second["export_digest"]

    def test_free_form_material_kind_is_reduced_to_other(self):
        events = load_fixture("allowed_proposal.jsonl")
        events[0]["payload"]["kind"] = "patient-kevin-secret-category"
        export = reduce_public_export(replay_events(events)).to_dict()
        assert export["materials"][0]["kind"] == "other"
        assert "patient-kevin-secret-category" not in json.dumps(export)

    def test_export_contains_no_raw_internal_ids(self):
        # Sprechende interne IDs dürfen den Export niemals erreichen.
        events = load_fixture("human_approved_retag.jsonl")
        renames = {
            "clm-001": "claim:private-biographical-thread",
            "mat-001": "material:private-medical-note",
            "req-001": "request:kevin-personal-promotion",
            "gd-001": "guard:private-guard-run",
            "hd-001": "human:private-approval",
        }
        serialized_stream = json.dumps(events)
        for old, new in renames.items():
            serialized_stream = serialized_stream.replace(f'"{old}"', f'"{new}"')
        state = replay_events(json.loads(serialized_stream))
        assert state.rejected_events == []
        export = reduce_public_export(state).to_dict()
        serialized = json.dumps(export)
        for raw_id in renames.values():
            assert raw_id not in serialized
        # Exportlokale Referenzen vorhanden und intern konsistent:
        assert export["claims"][0]["claim_ref"] == "claim:c001"
        assert export["materials"][0]["material_ref"] == "material:m001"
        assert export["guard_decisions"][0]["guard_ref"] == "guard:g001"
        assert export["guard_decisions"][0]["request_ref"] == "request:q001"

    def test_export_is_deterministic_for_identical_state(self):
        first = reduce_public_export(
            replay_events(load_fixture("retraction_non_destructive.jsonl"))
        ).to_dict()
        second = reduce_public_export(
            replay_events(load_fixture("retraction_non_destructive.jsonl"))
        ).to_dict()
        assert first == second
        # Retraction verweist per exportlokaler Referenz auf den Claim:
        assert first["retractions"][0]["claim_ref"] == first["claims"][0]["claim_ref"]


class TestReferentialIntegrity:
    """Korrekturdelta: Evidence-Claim-Bindung und exakte Guard-/Human-Referenzen."""

    def test_cross_claim_evidence_is_blocked_in_guard(self):
        # Relation gehört zu Claim A, Request will Claim B befördern.
        claims = {
            "clm-A": make_claim(claim_id="clm-A"),
            "clm-B": make_claim(claim_id="clm-B"),
        }
        relation_for_a = make_relation(claim_id="clm-A")
        request_for_b = make_request(claim_id="clm-B")
        decision = evaluate(request_for_b, claims=claims, relations={"rel-001": relation_for_a})
        assert decision.decision == GUARD_STOP
        assert ReasonCode.EVIDENCE_CLAIM_MISMATCH.value in decision.reason_codes

    def test_cross_claim_evidence_is_visible_in_replay(self):
        events = load_fixture("allowed_proposal.jsonl")
        # Zweiten Claim einfügen und den Request auf ihn umbiegen — die
        # Relation bleibt an clm-001 gebunden.
        claim_b = make_claim(claim_id="clm-B").to_payload()
        events.insert(
            2,
            {
                "type": "CLAIM_CREATED",
                "event_id": "evt-x-claim-b",
                "timestamp": 1752900001.5,
                "payload": claim_b,
            },
        )
        for event in events:
            if event["type"] == "TRANSITION_REQUESTED":
                event["payload"]["claim_id"] = "clm-B"
        state = replay_events(events)
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.EVIDENCE_CLAIM_MISMATCH.value in rejected_codes
        assert state.retag_history == []

    def test_validate_evidence_relations_flags_claim_mismatch(self):
        result = validate_evidence_relations(
            [make_relation(claim_id="clm-A")],
            {"mat-001": make_material()},
            claim_id="clm-B",
        )
        assert result.ok is False
        assert ReasonCode.EVIDENCE_CLAIM_MISMATCH in result.reason_codes

    def _retag_stream_with(self, **retag_overrides):
        events = load_fixture("human_approved_retag.jsonl")
        for event in events:
            if event["type"] == "CLAIM_RETAGGED":
                event["payload"].update(retag_overrides)
        return events

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("claim_id", "clm-002"),
            ("from_tag", "[METAPHER]"),
            ("to_tag", "[SPEC-WIP]"),
        ],
    )
    def test_retag_payload_must_match_stored_request(self, field, value):
        events = self._retag_stream_with(**{field: value})
        if field == "claim_id":
            events.insert(
                2,
                {
                    "type": "CLAIM_CREATED",
                    "event_id": "evt-x-claim-2",
                    "timestamp": 1752900001.5,
                    "payload": make_claim(claim_id="clm-002").to_payload(),
                },
            )
        state = replay_events(events)
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.REQUEST_REFERENCE_MISMATCH.value in rejected_codes

    def test_stored_propose_is_recomputed_before_retag(self):
        events = load_fixture("human_approved_retag.jsonl")
        # The persisted guard still says PROPOSE, but the actual referenced
        # material is a metaphor and therefore recomputes to HOLD.
        events[0]["payload"]["kind"] = "metaphor"
        state = replay_events(events)
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        assert state.retag_history == []
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.GUARD_REFERENCE_MISMATCH.value in rejected_codes

    def test_retag_with_wrong_guard_id_is_rejected(self):
        state = replay_events(self._retag_stream_with(guard_decision_id="gd-does-not-exist"))
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        assert len(state.rejected_events) == 1
        assert ReasonCode.GUARD_REFERENCE_MISMATCH.value in state.rejected_events[0]["reason_codes"]

    def test_retag_with_missing_guard_id_field_is_rejected(self):
        events = load_fixture("human_approved_retag.jsonl")
        for event in events:
            if event["type"] == "CLAIM_RETAGGED":
                del event["payload"]["guard_decision_id"]
        state = replay_events(events)
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        assert len(state.rejected_events) == 1
        assert ReasonCode.EVENT_SCHEMA_INVALID.value in state.rejected_events[0]["reason_codes"]

    def test_retag_with_guard_of_other_request_is_rejected(self):
        # Zweiter Request mit eigenem PROPOSE-Guard; der Retag referenziert
        # dessen Guard-ID statt der des eigenen Requests.
        events = load_fixture("human_approved_retag.jsonl")
        second_request = make_request(request_id="req-002", to_tag="[VOID]").to_payload()
        second_guard = {
            "decision_id": "gd-002",
            "schema_version": "erk.v0.1",
            "request_id": "req-002",
            "decision": "PROPOSE",
            "reason_codes": ["POLICY_TRANSITION_ALLOWED", "HUMAN_DECISION_REQUIRED"],
            "policy_version": "0.2",
            "policy_digest": load_claim_policy().digest,
            "actor": "erk.guard",
            "origin": "computational",
            "visibility": "reduced",
            "status": "RECORDED",
        }
        insert_at = next(
            index for index, event in enumerate(events) if event["type"] == "CLAIM_RETAGGED"
        )
        events.insert(
            insert_at,
            {
                "type": "TRANSITION_REQUESTED",
                "event_id": "evt-x-req2",
                "timestamp": 1752900005.2,
                "payload": second_request,
            },
        )
        events.insert(
            insert_at + 1,
            {
                "type": "GUARD_DECISION_RECORDED",
                "event_id": "evt-x-gd2",
                "timestamp": 1752900005.3,
                "payload": second_guard,
            },
        )
        for event in events:
            if event["type"] == "CLAIM_RETAGGED":
                event["payload"]["guard_decision_id"] = "gd-002"
        state = replay_events(events)
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.GUARD_REFERENCE_MISMATCH.value in rejected_codes

    def test_retag_digest_must_match_referenced_guard(self):
        state = replay_events(self._retag_stream_with(policy_digest="sha256:some-other-digest"))
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        assert len(state.rejected_events) == 1
        assert ReasonCode.POLICY_DIGEST_MISMATCH.value in state.rejected_events[0]["reason_codes"]

    def test_retag_digest_must_match_loaded_policy(self):
        policy = load_claim_policy()
        events = load_fixture("human_approved_retag.jsonl")
        for event in events:
            if event["type"] in {"GUARD_DECISION_RECORDED", "CLAIM_RETAGGED"}:
                event["payload"]["policy_digest"] = "sha256:some-other-digest"
        state = replay_events(events, policy=policy)
        assert state.current_tag("clm-001") == "[HYPOTHESE]"
        assert "gd-001" in state.guard_decisions
        assert any(ReasonCode.POLICY_DIGEST_MISMATCH.value in warning for warning in state.warnings)
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.POLICY_DIGEST_MISMATCH.value in rejected_codes

    def test_approve_without_propose_guard_is_rejected_in_replay(self):
        events = load_fixture("metaphor_no_promotion.jsonl")
        events.append(
            {
                "type": "HUMAN_DECISION_RECORDED",
                "event_id": "evt-x-approve",
                "timestamp": 1752910005.0,
                "payload": {
                    "decision_id": "hd-010",
                    "schema_version": "erk.v0.1",
                    "request_id": "req-010",
                    "decision": "APPROVE",
                    "human_actor": "role:project_initiator",
                    "decided_at": 1752910005.0,
                    "reason_codes": ["HUMAN_APPROVED"],
                    "visibility": "reduced",
                    "status": "RECORDED",
                },
            }
        )
        state = replay_events(events)
        assert "hd-010" not in state.human_decisions
        assert len(state.rejected_events) == 1

    def test_reject_without_propose_guard_stays_recordable(self):
        events = load_fixture("metaphor_no_promotion.jsonl")
        events.append(
            {
                "type": "HUMAN_DECISION_RECORDED",
                "event_id": "evt-x-reject",
                "timestamp": 1752910005.0,
                "payload": {
                    "decision_id": "hd-011",
                    "schema_version": "erk.v0.1",
                    "request_id": "req-010",
                    "decision": "REJECT",
                    "human_actor": "role:project_initiator",
                    "decided_at": 1752910005.0,
                    "reason_codes": ["HUMAN_REJECTED"],
                    "visibility": "reduced",
                    "status": "RECORDED",
                },
            }
        )
        state = replay_events(events)
        assert "hd-011" in state.human_decisions
        assert state.rejected_events == []


class TestDuplicateStableIds:
    """Korrekturdelta: Stabile IDs dürfen im Replay nicht still überschrieben werden."""

    def _assert_duplicate_rejected(self, events, store_getter, original_probe):
        state = replay_events(events)
        rejected_codes = [code for entry in state.rejected_events for code in entry["reason_codes"]]
        assert ReasonCode.DUPLICATE_STABLE_ID.value in rejected_codes
        # Erster Datensatz bleibt unverändert erhalten:
        assert original_probe(store_getter(state))
        return state

    def test_duplicate_request_id_does_not_overwrite(self):
        events = load_fixture("allowed_proposal.jsonl")
        second = make_request(to_tag="[VOID]").to_payload()
        events.append(
            {
                "type": "TRANSITION_REQUESTED",
                "event_id": "evt-x-dup-req",
                "timestamp": 1752900010.0,
                "payload": second,
            }
        )
        self._assert_duplicate_rejected(
            events,
            lambda state: state.requests,
            lambda requests: requests["req-001"]["to_tag"] == "[MODEL]",
        )

    def test_duplicate_guard_decision_id_does_not_overwrite(self):
        events = load_fixture("allowed_proposal.jsonl")
        duplicate = dict(events[4]["payload"])
        duplicate["decision"] = "STOP"
        events.append(
            {
                "type": "GUARD_DECISION_RECORDED",
                "event_id": "evt-x-dup-gd",
                "timestamp": 1752900010.0,
                "payload": duplicate,
            }
        )
        self._assert_duplicate_rejected(
            events,
            lambda state: state.guard_decisions,
            lambda guards: guards["gd-001"]["decision"] == "PROPOSE",
        )

    def test_duplicate_human_decision_id_does_not_overwrite(self):
        events = load_fixture("human_approved_retag.jsonl")
        contradiction = {
            "decision_id": "hd-001",
            "schema_version": "erk.v0.1",
            "request_id": "req-001",
            "decision": "REJECT",
            "human_actor": "role:project_initiator",
            "decided_at": 1752900010.0,
            "reason_codes": ["HUMAN_REJECTED"],
            "visibility": "reduced",
            "status": "RECORDED",
        }
        events.append(
            {
                "type": "HUMAN_DECISION_RECORDED",
                "event_id": "evt-x-dup-hd",
                "timestamp": 1752900010.0,
                "payload": contradiction,
            }
        )
        self._assert_duplicate_rejected(
            events,
            lambda state: state.human_decisions,
            lambda humans: humans["hd-001"]["decision"] == "APPROVE",
        )

    def test_duplicate_relation_id_does_not_overwrite(self):
        events = load_fixture("allowed_proposal.jsonl")
        duplicate = make_relation(relation_type="CONTRADICTS").to_payload()
        events.append(
            {
                "type": "EVIDENCE_RELATION_RECORDED",
                "event_id": "evt-x-dup-rel",
                "timestamp": 1752900010.0,
                "payload": duplicate,
            }
        )
        self._assert_duplicate_rejected(
            events,
            lambda state: state.relations,
            lambda relations: relations["rel-001"]["relation_type"] == "SUPPORTS",
        )
