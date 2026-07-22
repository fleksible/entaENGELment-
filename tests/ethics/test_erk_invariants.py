"""Ethics-Tests: die zwölf harten Invarianten des Evidence Routing Kernel v0.1a.

Die Nummerierung entspricht docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md, Abschnitt 7.
"""

import json
from pathlib import Path

import pytest

from src.core.evidence_routing import (
    GUARD_HOLD,
    GUARD_PROPOSE,
    GUARD_STOP,
    ClaimCandidate,
    EvidenceRelation,
    EvidenceRoutingError,
    HumanDecision,
    MaterialRef,
    ReasonCode,
    TransitionRequest,
    apply_approved_transition,
    evaluate_transition_request,
    load_claim_policy,
    record_human_decision,
    reduce_public_export,
    replay_events,
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


def make_material(**overrides):
    data = {
        "material_id": "mat-001",
        "schema_version": "erk.v0.1",
        "kind": "measurement",
        "source": "repo",
        "revision": "r1",
        "locator": "docs/audit/example.md",
        "digest": "sha256:01",
        "origin": "repo_annex",
        "actor": "role:maintainer",
        "trust": "REVIEWED",
        "visibility": "reduced",
        "status": "ACTIVE",
    }
    data.update(overrides)
    return MaterialRef(**data)


def make_claim(**overrides):
    data = {
        "claim_id": "clm-001",
        "schema_version": "erk.v0.1",
        "claim_text": "Beispiel-Claim.",
        "claim_tag": "[HYPOTHESE]",
        "actor": "role:maintainer",
        "origin": "repo_annex",
        "visibility": "reduced",
        "status": "ACTIVE",
        "material_refs": ["mat-001"],
    }
    data.update(overrides)
    return ClaimCandidate(**data)


def make_relation(**overrides):
    data = {
        "relation_id": "rel-001",
        "schema_version": "erk.v0.1",
        "claim_id": "clm-001",
        "material_id": "mat-001",
        "relation_type": "SUPPORTS",
        "actor": "role:maintainer",
        "origin": "repo_annex",
        "visibility": "reduced",
        "status": "ACTIVE",
        "reason_codes": [],
    }
    data.update(overrides)
    return EvidenceRelation(**data)


def make_request(**overrides):
    data = {
        "request_id": "req-001",
        "schema_version": "erk.v0.1",
        "claim_id": "clm-001",
        "from_tag": "[HYPOTHESE]",
        "to_tag": "[MODEL]",
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


def make_human_decision(**overrides):
    data = {
        "decision_id": "hd-001",
        "schema_version": "erk.v0.1",
        "request_id": "req-001",
        "decision": "APPROVE",
        "human_actor": "role:project_initiator",
        "decided_at": 1752900005.0,
        "reason_codes": [],
        "visibility": "reduced",
        "status": "RECORDED",
    }
    data.update(overrides)
    return HumanDecision(**data)


def evaluate(request, **overrides):
    policy = overrides.pop("policy", None) or load_claim_policy()
    kwargs = {
        "claims": {"clm-001": make_claim()},
        "materials": {"mat-001": make_material()},
        "relations": {"rel-001": make_relation()},
        "decision_id": "gd-test",
    }
    kwargs.update(overrides)
    return evaluate_transition_request(request, policy=policy, **kwargs)


def test_invariant_01_policy_is_not_truth():
    """Eine erlaubte Policy-Kante führt nie allein zum Retagging."""
    decision = evaluate(make_request())
    assert decision.decision == GUARD_PROPOSE  # nur ein Vorschlag, kein Retag
    # Im Replay: Stream mit erlaubter Kante und PROPOSE, aber ohne HumanDecision,
    # lässt den Claim-Tag unverändert.
    state = replay_events(load_fixture("allowed_proposal.jsonl"))
    assert state.current_tag("clm-001") == "[HYPOTHESE]"
    assert state.retag_history == []


def test_invariant_02_human_approval_required():
    """Jedes tatsächliche Retagging benötigt ein passendes HumanDecision-Approve."""
    policy = load_claim_policy()
    request = make_request()
    guard = evaluate(request, policy=policy)
    # apply ohne APPROVE (DEFER) fail-closed:
    with pytest.raises(EvidenceRoutingError):
        apply_approved_transition(
            request,
            policy=policy,
            claims={"clm-001": make_claim()},
            guard_decision=guard,
            human_decision=make_human_decision(decision="DEFER"),
        )
    # Ein synthetisch eingeschleustes CLAIM_RETAGGED ohne HumanDecision-Event
    # wird im Replay sichtbar quarantänisiert, nicht angewendet:
    events = load_fixture("allowed_proposal.jsonl")
    events.append(
        {
            "type": "CLAIM_RETAGGED",
            "event_id": "evt-forged",
            "timestamp": 1752900099.0,
            "payload": {
                "schema_version": "erk.v0.1",
                "claim_id": "clm-001",
                "from_tag": "[HYPOTHESE]",
                "to_tag": "[MODEL]",
                "request_id": "req-001",
                "guard_decision_id": "gd-001",
                "human_decision_id": "hd-does-not-exist",
                "policy_version": "0.2",
                "policy_digest": policy.digest,
                "reason_codes": ["HUMAN_APPROVED", "POLICY_TRANSITION_ALLOWED"],
                "actor": "erk.guard",
                "visibility": "reduced",
                "status": "APPLIED",
            },
        }
    )
    state = replay_events(events)
    assert state.current_tag("clm-001") == "[HYPOTHESE]"
    assert len(state.rejected_events) == 1
    assert ReasonCode.HUMAN_DECISION_REQUIRED.value in state.rejected_events[0]["reason_codes"]


def test_invariant_03_metaphor_is_not_evidence():
    """Metapher oder Rosetta darf keine Promotion begründen."""
    for kind in ("metaphor", "rosetta"):
        decision = evaluate(make_request(), materials={"mat-001": make_material(kind=kind)})
        assert decision.decision == GUARD_HOLD
        assert ReasonCode.METAPHOR_IS_NOT_EVIDENCE.value in decision.reason_codes


def test_invariant_04_provenance_is_not_evidence():
    """Materialpointer und Ledger-Receipt beweisen keinen Claim."""
    for relation_type in ("PROVENANCE_ONLY", "MOTIVATES"):
        decision = evaluate(
            make_request(),
            relations={"rel-001": make_relation(relation_type=relation_type)},
        )
        assert decision.decision == GUARD_HOLD
        assert ReasonCode.PROVENANCE_IS_NOT_EVIDENCE.value in decision.reason_codes


def test_invariant_05_void_is_valid():
    """Ein Claim darf unbegrenzt in [VOID] verbleiben."""
    policy = load_claim_policy()
    void_claim = make_claim(claim_tag="[VOID]")
    # Kein Mechanismus erzwingt eine Transition: Der Guard bewertet nur
    # explizit gestellte Requests; ohne Request bleibt [VOID] bestehen.
    events = [
        {
            "type": "CLAIM_CREATED",
            "event_id": "evt-void-1",
            "timestamp": 1752900000.0,
            "payload": void_claim.to_payload(),
        }
    ]
    state = replay_events(events, policy=policy)
    assert state.current_tag("clm-001") == "[VOID]"
    assert state.rejected_events == []
    assert state.warnings == []
    # [VOID] ist zudem von fast überall erreichbar — u.a. aus [HYPOTHESE]:
    decision = evaluate(make_request(to_tag="[VOID]", evidence_relation_ids=[]))
    assert decision.decision == GUARD_PROPOSE


def test_invariant_06_retraction_is_append_only():
    """Rücknahme löscht oder überschreibt keine Historie."""
    state = replay_events(load_fixture("retraction_non_destructive.jsonl"))
    assert state.claims["clm-001"]["retracted"] is True
    assert len(state.retag_history) == 1  # Historie vollständig erhalten
    assert "gd-001" in state.guard_decisions
    assert "hd-001" in state.human_decisions
    assert "ret-001" in state.retractions
    assert state.rejected_events == []


def test_invariant_07_guard_state_is_not_claim_state():
    """PROPOSE/HOLD/STOP verändert den Claim-Tag nicht."""
    for fixture in ("allowed_proposal.jsonl", "metaphor_no_promotion.jsonl"):
        state = replay_events(load_fixture(fixture))
        for record in state.claims.values():
            assert record["current_tag"] == record["claim_tag"]
    # Auch ein STOP verändert nichts (pure Funktion, kein State-Write):
    claims = {"clm-001": make_claim()}
    decision = evaluate(make_request(to_tag="[CANON]"), claims=claims)
    assert decision.decision == GUARD_STOP
    assert claims["clm-001"].claim_tag == "[HYPOTHESE]"


def test_invariant_08_untrusted_stays_bounded():
    """Untrusted Material führt niemals direkt zu Retagging."""
    decision = evaluate(make_request(), materials={"mat-001": make_material(trust="UNTRUSTED")})
    assert decision.decision in (GUARD_HOLD, GUARD_STOP)
    assert ReasonCode.UNTRUSTED_MATERIAL.value in decision.reason_codes
    # Unbekannter Trust-Level wird auf UNTRUSTED reduziert, nie aufgewertet:
    decision = evaluate(
        make_request(), materials={"mat-001": make_material(trust="BRAND_NEW_LEVEL")}
    )
    assert decision.decision in (GUARD_HOLD, GUARD_STOP)


def test_invariant_09_consent_fails_closed():
    """Fehlender erforderlicher Consent erzeugt HOLD oder STOP."""
    for status in ("CONSENT_MISSING", "CONSENT_REVOKED"):
        decision = evaluate(make_request(), claims={"clm-001": make_claim(status=status)})
        assert decision.decision in (GUARD_HOLD, GUARD_STOP)
        assert ReasonCode.CONSENT_MISSING.value in decision.reason_codes
    # Auch apply_approved_transition ist fail-closed:
    policy = load_claim_policy()
    request = make_request()
    guard = evaluate(request, policy=policy)
    with pytest.raises(EvidenceRoutingError) as excinfo:
        apply_approved_transition(
            request,
            policy=policy,
            claims={"clm-001": make_claim(status="CONSENT_REVOKED")},
            guard_decision=guard,
            human_decision=make_human_decision(),
        )
    assert ReasonCode.CONSENT_MISSING in excinfo.value.reason_codes


def test_invariant_10_replay_is_deterministic():
    """Identischer Stream plus identische Policy ergibt identischen State-Digest."""
    policy = load_claim_policy()
    first = replay_events(load_fixture("human_approved_retag.jsonl"), policy=policy)
    second = replay_events(load_fixture("human_approved_retag.jsonl"), policy=policy)
    assert first.state_digest == second.state_digest
    assert reduce_public_export(first).to_dict() == reduce_public_export(second).to_dict()


def test_invariant_11_public_export_is_reduced():
    """Private und unbekannte Felder fehlen vollständig im Export."""
    state = replay_events(load_fixture("private_reduced_export.jsonl"))
    export = reduce_public_export(state).to_dict()
    serialized = json.dumps(export)
    for private_marker in (
        "PRIVATE_TEXT",
        "/private/diary",
        "biographical",
        "initiator_private_name",
        "private_chat",
        "claim_text",
        "locator",
    ):
        assert private_marker not in serialized
    # Kein dynamisches Durchreichen unbekannter Felder:
    assert set(export) == {
        "export_schema_version",
        "policy_version",
        "policy_digest",
        "export_digest",
        "claims",
        "materials",
        "guard_decisions",
        "retractions",
    }


def test_invariant_12_policy_drift_is_visible():
    """Ein Digest-Wechsel wird erkannt und nie still akzeptiert."""
    policy = load_claim_policy()
    request = make_request()
    guard = evaluate(request, policy=policy)
    drifted_guard = GuardDecisionWithDigest(guard, "sha256:other-policy-digest")
    with pytest.raises(EvidenceRoutingError) as excinfo:
        apply_approved_transition(
            request,
            policy=policy,
            claims={"clm-001": make_claim()},
            guard_decision=drifted_guard.build(),
            human_decision=make_human_decision(),
        )
    assert ReasonCode.POLICY_DIGEST_MISMATCH in excinfo.value.reason_codes
    # Im Replay wird Drift als Warnung sichtbar, nicht still geschluckt:
    events = load_fixture("allowed_proposal.jsonl")
    events[-1]["payload"]["policy_digest"] = "sha256:other-policy-digest"
    state = replay_events(events, policy=policy)
    assert any(ReasonCode.POLICY_DIGEST_MISMATCH.value in warning for warning in state.warnings)


class GuardDecisionWithDigest:
    """Testhelfer: GuardDecision mit abweichendem Policy-Digest nachbauen."""

    def __init__(self, guard, digest):
        self.guard = guard
        self.digest = digest

    def build(self):
        from src.core.evidence_routing import GuardDecision

        data = self.guard.to_payload()
        data["policy_digest"] = self.digest
        return GuardDecision(**data)


# ---------------------------------------------------------------------------
# Zusätzliche Referential-Integrity- und Privacy-Tests (Korrekturdelta,
# keine Umnummerierung der zwölf Invarianten)
# ---------------------------------------------------------------------------


def test_referential_cross_claim_evidence_is_blocked():
    """Evidenz eines anderen Claims darf keinen Übergang stützen."""
    claims = {
        "clm-A": make_claim(claim_id="clm-A"),
        "clm-B": make_claim(claim_id="clm-B"),
    }
    decision = evaluate(
        make_request(claim_id="clm-B"),
        claims=claims,
        relations={"rel-001": make_relation(claim_id="clm-A")},
    )
    assert decision.decision == GUARD_STOP
    assert ReasonCode.EVIDENCE_CLAIM_MISMATCH.value in decision.reason_codes


def test_privacy_human_actor_is_asserted_label_not_identity():
    """human_actor ist eine nicht authentifizierte Rollenbehauptung.

    Der Kernel authentifiziert die Person hinter dem Label nicht: Die
    strukturelle Validierung hängt nur vom Event (Request + PROPOSE-Guard) ab,
    nicht vom Label-Inhalt — und das Label erreicht den Public Export nicht.
    """
    policy = load_claim_policy()
    request = make_request()
    guard = evaluate(request, policy=policy)
    requests = {"req-001": request}
    guards = {"gd-test": guard}
    for actor_label in ("role:project_initiator", "anyone:unverified-string"):
        decision = make_human_decision(human_actor=actor_label)
        # Beide Labels sind strukturell gleichwertig — keine Identitätsprüfung:
        assert (
            record_human_decision(decision, requests=requests, guard_decisions=guards) is decision
        )
    # Das Label taucht in keinem Public Export auf:
    state = replay_events(load_fixture("human_approved_retag.jsonl"))
    serialized = json.dumps(reduce_public_export(state).to_dict())
    assert "role:project_initiator" not in serialized
    assert "human_actor" not in serialized
