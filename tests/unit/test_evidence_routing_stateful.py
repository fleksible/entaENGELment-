"""Zustandsbehaftete Dauerprobe für den Evidence Routing Kernel v0.1a.

Die Probe erzeugt viele Abfolgen aus Antrag, Guard-Bewertung, menschlicher
Entscheidung, Widerruf, Statusübergang und Retraction und spielt sie nach
jedem Schritt durch die produktive Implementierung (`replay_events`,
`evaluate_transition_request`, `record_human_decision`,
`apply_approved_transition`). Es gibt keine Mocks und kein Zweitmodell des
Kernels.

Geprüft wird eine Sicherheitsaussage: Ein Claim-Tag ändert sich nur, wenn die
Änderung im Eventstream vollständig begründet ist. Die Begründung wird hier
unabhängig vom Kernel aus dem selbst geschriebenen Stream nachgerechnet.

``derandomize=True`` und ``database=None`` halten die Abfolgen bei jedem Lauf
gleich. Alle menschlichen Entscheidungen tragen ein ausdrücklich synthetisches
Akteurslabel; es steht für keine reale Person und keine reale Freigabe.
"""

import collections

from hypothesis import HealthCheck, settings
from hypothesis import strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    initialize,
    precondition,
    rule,
    run_state_machine_as_test,
)

from src.core.evidence_routing import (
    GUARD_HOLD,
    GUARD_PROPOSE,
    GUARD_STOP,
    PROMOTION_CAPABLE_RELATION_TYPES,
    PROMOTION_TAGS,
    ClaimCandidate,
    EvidenceRelation,
    EvidenceRoutingError,
    GuardDecision,
    HumanDecision,
    MaterialRef,
    ReasonCode,
    Retraction,
    TransitionRequest,
    apply_approved_transition,
    evaluate_transition_request,
    load_claim_policy,
    normalize_claim_tag,
    record_human_decision,
    record_retraction,
    replay_events,
)
from src.core.ledger import Ledger, load_ledger, verify_chain_from_file

POLICY = load_claim_policy()
SCHEMA = "erk.v0.1"
SYNTHETIC_HUMAN = "role:synthetic_test_human"
START_TAG = "[HYPOTHESE]"
CLAIMS = ("clm-a", "clm-b", "clm-c")
# Zieltags: erlaubte Nachbarn, ein Alias, eine verbotene Kante, ein unbekanntes Tag.
TARGET_TAGS = (
    "[MODEL]",
    "[INFERENZ]",
    "[SPEC-WIP]",
    "[SPEC]",
    "[VOID]",
    "[CANON]",
    "[FAKT]",
    "[TOTALLY-NEW]",
)
EVIDENCE_KINDS = ("supports", "untrusted", "metaphor", "motivates", "none", "foreign")
HUMAN_VALUES = ("APPROVE", "REJECT", "DEFER", "WITHDRAW")
# Fast gültige Übergänge: alles stimmt bis auf genau einen Punkt.
DEFECTS = (
    "no_decision",
    "withdrawn",
    "rejected_afterwards",
    "deferred_afterwards",
    "cites_rejection",
    "cites_deferral",
    "cites_withdrawal",
    "approval_of_other_request",
    "claimed_guard_without_evidence",
    "untrusted_evidence",
    "metaphor_evidence",
    "claim_moved_on",
    "retracted",
)
SECOND_THOUGHT = {
    "withdrawn": "WITHDRAW",
    "rejected_afterwards": "REJECT",
    "deferred_afterwards": "DEFER",
}
CITED_INSTEAD_OF_APPROVAL = {
    "cites_rejection": "REJECT",
    "cites_deferral": "DEFER",
    "cites_withdrawal": "WITHDRAW",
}
WEAK_EVIDENCE = {
    "claimed_guard_without_evidence": "motivates",
    "untrusted_evidence": "untrusted",
    "metaphor_evidence": "metaphor",
}

STATEFUL_SETTINGS = settings(
    derandomize=True,
    database=None,
    deadline=None,
    max_examples=100,
    stateful_step_count=40,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)


def material(material_id, kind, trust):
    return MaterialRef(
        material_id=material_id,
        schema_version=SCHEMA,
        kind=kind,
        source="synthetic",
        revision="r1",
        locator="tests/synthetic",
        digest="sha256:00",
        origin="stateful_probe",
        actor="role:synthetic_test_agent",
        trust=trust,
        visibility="reduced",
        status="ACTIVE",
    )


def relation(claim_id, name, relation_type, material_id):
    return EvidenceRelation(
        relation_id=f"rel-{claim_id}-{name}",
        schema_version=SCHEMA,
        claim_id=claim_id,
        material_id=material_id,
        relation_type=relation_type,
        actor="role:synthetic_test_agent",
        origin="stateful_probe",
        visibility="reduced",
        status="ACTIVE",
        reason_codes=[],
    )


def tag(value):
    return normalize_claim_tag(value, POLICY).tag


class TransitionMachine(RuleBasedStateMachine):
    """Schreibt einen Eventstream und prüft nach jedem Schritt den Replay-Zustand."""

    seen: collections.Counter = collections.Counter()

    def __init__(self):
        super().__init__()
        self.events = []
        self.materials = {}
        self.claims = {}
        self.relations = {}
        self.requests = {}
        self.guards = {}
        self.humans = []
        self.retracted = set()
        self.tags = {}
        self.state = None
        self.accepted_retags = 0

    # --- Stream schreiben ---------------------------------------------------------

    def append(self, event_type, payload):
        number = len(self.events) + 1
        self.events.append(
            {
                "type": event_type,
                "event_id": f"evt-{number:04d}",
                "timestamp": float(number),
                "payload": payload,
            }
        )
        self.observe()

    def next_id(self, prefix):
        return f"{prefix}-{len(self.events) + 1:04d}"

    def replay_inputs(self):
        return {
            "claims": self.claims,
            "current_tags": {c: self.state.current_tag(c) for c in self.claims},
            "claim_statuses": {c: str(self.state.claims[c]["status"]) for c in self.claims},
        }

    def accepted_humans(self):
        return [h for h in self.humans if h.decision_id in self.state.human_decisions]

    def write_request(self, claim_id, to_tag, relation_ids, from_tag=None):
        request = TransitionRequest(
            request_id=self.next_id("req"),
            schema_version=SCHEMA,
            claim_id=claim_id,
            from_tag=from_tag or self.tags[claim_id],
            to_tag=to_tag,
            actor="role:synthetic_test_agent",
            origin="stateful_probe",
            requested_at=float(len(self.events) + 1),
            evidence_relation_ids=relation_ids,
            reason_codes=[],
            visibility="reduced",
            status="OPEN",
        )
        self.append("TRANSITION_REQUESTED", request.to_payload())
        if request.request_id not in self.state.requests:
            return None
        self.requests[request.request_id] = request
        return request

    def write_evaluated_guard(self, request):
        guard = evaluate_transition_request(
            request,
            policy=POLICY,
            materials=self.materials,
            relations=self.relations,
            decision_id=self.next_id("gd"),
            **self.replay_inputs(),
        )
        assert guard.decision in {GUARD_PROPOSE, GUARD_HOLD, GUARD_STOP}
        self.guards[guard.decision_id] = guard
        self.seen[f"guard_{guard.decision}"] += 1
        self.append("GUARD_DECISION_RECORDED", guard.to_payload())
        return guard

    def write_claimed_guard(self, request):
        # Ein behauptetes PROPOSE ohne Bewertung. Aufzeichnen lässt es sich;
        # tragen darf es nur, wenn die frische Bewertung dasselbe ergibt.
        guard = GuardDecision(
            decision_id=self.next_id("gd"),
            schema_version=SCHEMA,
            request_id=request.request_id,
            decision=GUARD_PROPOSE,
            reason_codes=[
                ReasonCode.POLICY_TRANSITION_ALLOWED.value,
                ReasonCode.HUMAN_DECISION_REQUIRED.value,
            ],
            policy_version=POLICY.version,
            policy_digest=POLICY.digest,
            actor="erk.guard",
            origin="computational",
            visibility="reduced",
            status="RECORDED",
        )
        self.guards[guard.decision_id] = guard
        self.seen["guard_claimed"] += 1
        self.append("GUARD_DECISION_RECORDED", guard.to_payload())
        return guard

    def write_human(self, request, value):
        human = HumanDecision(
            decision_id=self.next_id("hd"),
            schema_version=SCHEMA,
            request_id=request.request_id,
            decision=value,
            human_actor=SYNTHETIC_HUMAN,
            decided_at=float(len(self.events) + 1),
            reason_codes=[],
            visibility="reduced",
            status="RECORDED",
        )
        self.humans.append(human)
        self.append("HUMAN_DECISION_RECORDED", human.to_payload())
        return human

    def write_retraction(self, claim_id):
        retraction = Retraction(
            retraction_id=self.next_id("ret"),
            schema_version=SCHEMA,
            claim_id=claim_id,
            actor=SYNTHETIC_HUMAN,
            retracted_at=float(len(self.events) + 1),
            reason_codes=[ReasonCode.RETRACTION_RECORDED.value],
            visibility="reduced",
            status="RECORDED",
        )
        record_retraction(retraction, claims=self.claims)
        self.retracted.add(claim_id)
        self.seen["retraction"] += 1
        self.append("RETRACTION_RECORDED", retraction.to_payload())

    def raw_retag(self, request, guard_id, human_id):
        """Ein Statusübergang, am Konstruktor vorbei direkt in den Stream geschrieben."""
        return {
            "schema_version": SCHEMA,
            "claim_id": request.claim_id,
            "from_tag": tag(request.from_tag),
            "to_tag": tag(request.to_tag),
            "request_id": request.request_id,
            "guard_decision_id": guard_id,
            "human_decision_id": human_id,
            "policy_version": POLICY.version,
            "policy_digest": POLICY.digest,
            "reason_codes": [
                ReasonCode.HUMAN_APPROVED.value,
                ReasonCode.POLICY_TRANSITION_ALLOWED.value,
            ],
            "actor": SYNTHETIC_HUMAN,
            "visibility": request.visibility,
            "status": "APPLIED",
        }

    def open_claims(self):
        """Claims, von deren Tag eine erlaubte, belegpflichtige Kante ausgeht."""
        return [
            claim_id
            for claim_id in CLAIMS
            if claim_id not in self.retracted
            and any(t in PROMOTION_TAGS for t in POLICY.allowed_next(self.tags[claim_id]))
        ]

    def propose(self, claim_id, evidence="supports"):
        """Antrag entlang einer erlaubten Kante samt echter Guard-Bewertung."""
        target = next(
            t for t in sorted(POLICY.allowed_next(self.tags[claim_id])) if t in PROMOTION_TAGS
        )
        request = self.write_request(claim_id, target, [f"rel-{claim_id}-{evidence}"])
        return request, self.write_evaluated_guard(request)

    def apply_released(self, request, guard, approval):
        """Der Weg über den produktiven Konstruktor; was er freigibt, wird geschrieben."""
        payload = apply_approved_transition(
            request,
            policy=POLICY,
            guard_decision=guard,
            human_decision=approval,
            human_decisions=self.accepted_humans(),
            **self.replay_inputs(),
        )
        self.append("CLAIM_RETAGGED", payload)
        assert self.tags[request.claim_id] == tag(request.to_tag)

    # --- Beobachtung und unabhängige Begründungsprüfung -----------------------------

    def observe(self):
        before = self.state
        state = replay_events(self.events, policy=POLICY)
        for claim_id in self.claims:
            new = state.current_tag(claim_id)
            old = self.tags.get(claim_id, new)
            if new != old:
                self.assert_change_is_justified(claim_id, old, new, before)
                self.accepted_retags += 1
                self.seen["status_changed"] += 1
            self.tags[claim_id] = new
        assert (
            len(state.retag_history) == self.accepted_retags
        ), "a retag was accepted that changed no tag"
        self.state = state

    def teardown(self):
        # Derselbe Stream ergibt denselben Zustand, auch nach allen Abweisungen.
        if self.events:
            again = replay_events(self.events, policy=POLICY)
            assert again.state_digest == self.state.state_digest

    def assert_change_is_justified(self, claim_id, old, new, before):
        last = self.events[-1]
        assert last["type"] == "CLAIM_RETAGGED", "tag changed without a retag event"
        payload = last["payload"]
        assert payload["claim_id"] == claim_id
        assert claim_id not in self.retracted, "retracted claim was retagged"

        request = self.requests.get(payload["request_id"])
        assert request is not None, "retag without a recorded request"
        assert request.claim_id == claim_id
        assert tag(request.from_tag) == old, "retag from a tag the claim no longer has"
        assert tag(request.to_tag) == new
        assert new in POLICY.allowed_next(old), "retag along an edge the policy does not allow"

        guard = self.guards.get(payload["guard_decision_id"])
        assert guard is not None, "retag without a recorded guard decision"
        assert guard.request_id == request.request_id
        assert guard.decision == GUARD_PROPOSE

        decisions = [
            human
            for human in self.humans
            if human.request_id == request.request_id
            and human.decision_id in before.human_decisions
        ]
        assert decisions, "retag without any human decision"
        assert all(human.decision != "WITHDRAW" for human in decisions), "retag after withdrawal"
        latest = decisions[-1]
        assert latest.decision == "APPROVE", "latest human decision is not an approval"
        assert latest.decision_id == payload["human_decision_id"], "retag cites another decision"
        assert latest.human_actor == SYNTHETIC_HUMAN

        if new in PROMOTION_TAGS:
            carrying = [
                self.relations[relation_id]
                for relation_id in request.evidence_relation_ids
                if relation_id in self.relations
            ]
            assert any(
                item.claim_id == claim_id
                and item.relation_type in PROMOTION_CAPABLE_RELATION_TYPES
                and self.materials[item.material_id].trust in {"TRUSTED", "REVIEWED"}
                and self.materials[item.material_id].kind != "metaphor"
                for item in carrying
            ), "promotion without evidence that may carry it"

    # --- Aufbau ----------------------------------------------------------------------

    @initialize()
    def setup(self):
        for item in (
            material("mat-measured", "measurement", "REVIEWED"),
            material("mat-untrusted", "document", "UNTRUSTED"),
            material("mat-metaphor", "metaphor", "REVIEWED"),
        ):
            self.materials[item.material_id] = item
            self.append("MATERIAL_REGISTERED", item.to_payload())
        for claim_id in CLAIMS:
            claim = ClaimCandidate(
                claim_id=claim_id,
                schema_version=SCHEMA,
                claim_text="Synthetischer Claim der Dauerprobe.",
                claim_tag=START_TAG,
                actor="role:synthetic_test_agent",
                origin="stateful_probe",
                visibility="reduced",
                status="ACTIVE",
                material_refs=["mat-measured"],
            )
            self.claims[claim_id] = claim
            self.append("CLAIM_CREATED", claim.to_payload())
            for name, relation_type, material_id in (
                ("supports", "SUPPORTS", "mat-measured"),
                ("untrusted", "SUPPORTS", "mat-untrusted"),
                ("metaphor", "SUPPORTS", "mat-metaphor"),
                ("motivates", "MOTIVATES", "mat-measured"),
            ):
                item = relation(claim_id, name, relation_type, material_id)
                self.relations[item.relation_id] = item
                self.append("EVIDENCE_RELATION_RECORDED", item.to_payload())
        assert self.state.rejected_events == []
        assert set(self.tags.values()) == {START_TAG}

    # --- Freie Regeln: beliebige Reihenfolgen und Verweise ----------------------------

    @rule(
        claim_id=st.sampled_from(CLAIMS),
        to_tag=st.sampled_from(TARGET_TAGS),
        evidence=st.sampled_from(EVIDENCE_KINDS),
        stale=st.booleans(),
    )
    def request_transition(self, claim_id, to_tag, evidence, stale):
        other = CLAIMS[(CLAIMS.index(claim_id) + 1) % len(CLAIMS)]
        relation_ids = {
            "none": [],
            "foreign": [f"rel-{other}-supports"],
        }.get(evidence, [f"rel-{claim_id}-{evidence}"])
        request = self.write_request(
            claim_id, to_tag, relation_ids, from_tag=START_TAG if stale else None
        )
        if request is None:
            # Fremde Evidenz hängt der Kernel nicht um; der Antrag bleibt draußen.
            assert evidence == "foreign"

    @precondition(lambda self: self.requests)
    @rule(data=st.data(), claimed=st.booleans())
    def record_guard(self, data, claimed):
        request = self.requests[data.draw(st.sampled_from(sorted(self.requests)))]
        if claimed:
            self.write_claimed_guard(request)
        else:
            self.write_evaluated_guard(request)

    @precondition(lambda self: self.requests)
    @rule(data=st.data(), value=st.sampled_from(HUMAN_VALUES))
    def human_decides(self, data, value):
        request = self.requests[data.draw(st.sampled_from(sorted(self.requests)))]
        has_proposal = any(
            guard.request_id == request.request_id and guard.decision == GUARD_PROPOSE
            for guard in self.guards.values()
        )
        withdrawn = any(
            earlier.request_id == request.request_id and earlier.decision == "WITHDRAW"
            for earlier in self.accepted_humans()
        )
        # Auch eine unzulässige Entscheidung wird geschrieben: Der Replay muss sie abweisen.
        human = self.write_human(request, value)
        accepted = human.decision_id in self.state.human_decisions
        if value == "APPROVE":
            assert accepted == (has_proposal and not withdrawn)
        else:
            assert accepted
        try:
            record_human_decision(human, requests=self.requests, guard_decisions=self.guards)
            constructive_ok = True
        except EvidenceRoutingError:
            constructive_ok = False
        assert constructive_ok == (value != "APPROVE" or has_proposal)
        self.seen[f"human_{value}_{'accepted' if accepted else 'refused'}"] += 1

    @precondition(lambda self: self.requests and self.guards and self.humans)
    @rule(data=st.data(), write_anyway=st.booleans())
    def apply_with_any_references(self, data, write_anyway):
        request = self.requests[data.draw(st.sampled_from(sorted(self.requests)))]
        history = self.accepted_humans()
        if not history:
            return
        guard = self.guards[data.draw(st.sampled_from(sorted(self.guards)))]
        human = data.draw(st.sampled_from(history))
        try:
            payload = apply_approved_transition(
                request,
                policy=POLICY,
                guard_decision=guard,
                human_decision=human,
                human_decisions=history,
                **self.replay_inputs(),
            )
        except EvidenceRoutingError:
            self.seen["apply_refused"] += 1
            if not write_anyway:
                return
            payload = self.raw_retag(request, guard.decision_id, human.decision_id)
            self.seen["refused_then_written"] += 1
        self.append("CLAIM_RETAGGED", payload)

    @precondition(lambda self: self.requests)
    @rule(data=st.data(), known_guard=st.booleans(), known_human=st.booleans())
    def write_retag_directly(self, data, known_guard, known_human):
        request = self.requests[data.draw(st.sampled_from(sorted(self.requests)))]
        guard_id = "gd-0000"
        if known_guard and self.guards:
            guard_id = data.draw(st.sampled_from(sorted(self.guards)))
        human_id = "hd-0000"
        if known_human and self.humans:
            human_id = data.draw(st.sampled_from(self.humans)).decision_id
        self.seen["retag_written_directly"] += 1
        self.append("CLAIM_RETAGGED", self.raw_retag(request, guard_id, human_id))

    # Retraction ist endgültig; sie kommt erst, wenn der Stream schon Geschichte hat.
    @precondition(lambda self: len(self.events) > 60 and len(self.retracted) < len(CLAIMS) - 1)
    @rule(claim_id=st.sampled_from(CLAIMS))
    def retract(self, claim_id):
        self.write_retraction(claim_id)

    # --- Geführte Regeln: der zulässige Weg und seine nächsten Nachbarn ----------------

    @precondition(lambda self: self.open_claims())
    @rule(data=st.data(), pause=st.sampled_from(("none", "DEFER", "REJECT")))
    def approved_transition(self, data, pause):
        """Antrag, Vorschlag, Freigabe, Statusübergang; optional mit früherem Zögern."""
        claim_id = data.draw(st.sampled_from(self.open_claims()))
        request, guard = self.propose(claim_id)
        assert guard.decision == GUARD_PROPOSE
        if pause != "none":
            self.write_human(request, pause)
        approval = self.write_human(request, "APPROVE")
        record_human_decision(approval, requests=self.requests, guard_decisions=self.guards)
        self.apply_released(request, guard, approval)
        self.seen["approved_transition"] += 1

    @precondition(lambda self: self.open_claims())
    @rule(data=st.data(), defect=st.sampled_from(DEFECTS))
    def almost_valid_transition(self, data, defect):
        """Alles stimmt bis auf einen Punkt; der Übergang wird trotzdem geschrieben."""
        if defect == "retracted" and len(self.retracted) >= len(CLAIMS) - 1:
            return
        claim_id = data.draw(st.sampled_from(self.open_claims()))
        tag_before = self.tags[claim_id]
        request, guard = self.propose(claim_id, WEAK_EVIDENCE.get(defect, "supports"))
        human_id = "hd-0000"

        if defect == "no_decision":
            assert guard.decision == GUARD_PROPOSE
        elif defect in SECOND_THOUGHT:
            human_id = self.write_human(request, "APPROVE").decision_id
            self.write_human(request, SECOND_THOUGHT[defect])
        elif defect in CITED_INSTEAD_OF_APPROVAL:
            # Die jüngste Entscheidung wird korrekt zitiert; sie ist nur keine Freigabe.
            human_id = self.write_human(request, CITED_INSTEAD_OF_APPROVAL[defect]).decision_id
            assert human_id in self.state.human_decisions
        elif defect == "approval_of_other_request":
            other, _ = self.propose(claim_id)
            human_id = self.write_human(other, "APPROVE").decision_id
        elif defect in {"untrusted_evidence", "metaphor_evidence"}:
            # Die echte Bewertung schlägt nichts vor; die Freigabe findet keinen Vorschlag.
            assert guard.decision != GUARD_PROPOSE
            human_id = self.write_human(request, "APPROVE").decision_id
            assert human_id not in self.state.human_decisions
        elif defect == "claimed_guard_without_evidence":
            assert guard.decision != GUARD_PROPOSE
            guard = self.write_claimed_guard(request)
            # Das behauptete PROPOSE lässt die Freigabe zu; tragen darf es nicht.
            human_id = self.write_human(request, "APPROVE").decision_id
            assert human_id in self.state.human_decisions
        elif defect == "claim_moved_on":
            # Zwei freigegebene Anträge vom selben Ausgangstag; der zweite kommt zu spät.
            human_id = self.write_human(request, "APPROVE").decision_id
            twin, twin_guard = self.propose(claim_id)
            self.apply_released(twin, twin_guard, self.write_human(twin, "APPROVE"))
            tag_before = self.tags[claim_id]
        elif defect == "retracted":
            human_id = self.write_human(request, "APPROVE").decision_id
            self.write_retraction(claim_id)

        rejected_before = len(self.state.rejected_events)
        self.append("CLAIM_RETAGGED", self.raw_retag(request, guard.decision_id, human_id))
        assert self.tags[claim_id] == tag_before, f"transition despite defect: {defect}"
        assert len(self.state.rejected_events) > rejected_before, "refusal left no trace"
        self.seen[f"defect_{defect}"] += 1


def test_no_status_change_without_a_complete_justification():
    """Viele reproduzierbare Abfolgen; jede Tag-Änderung muss begründet sein."""
    TransitionMachine.seen.clear()
    run_state_machine_as_test(TransitionMachine, settings=STATEFUL_SETTINGS)
    seen = TransitionMachine.seen
    # Die Probe darf nicht leer laufen: echte Übergänge, echte Abweisungen, jeder Defekt.
    reached = [
        "status_changed",
        "approved_transition",
        "apply_refused",
        "refused_then_written",
        "retag_written_directly",
        "guard_PROPOSE",
        "guard_HOLD",
        "guard_STOP",
        "guard_claimed",
        "human_APPROVE_refused",
        "human_WITHDRAW_accepted",
        "retraction",
        *(f"defect_{defect}" for defect in DEFECTS),
    ]
    for key in reached:
        assert seen[key] >= 5, f"probe reached too rarely: {key} ({seen[key]})"


def test_request_approval_withdrawal_and_transition_through_the_ledger(tmp_path):
    """Ein lesbarer Durchgang über das produktive Ledger: halten, freigeben, widerrufen."""
    machine = TransitionMachine()
    machine.setup()

    # Antrag und Vorschlag ohne Freigabe: nichts ändert sich, auch nicht direkt geschrieben.
    first, first_guard = machine.propose("clm-a")
    assert first_guard.decision == GUARD_PROPOSE
    machine.append("CLAIM_RETAGGED", machine.raw_retag(first, first_guard.decision_id, "hd-0000"))
    assert machine.tags["clm-a"] == START_TAG

    # Freigabe: genau jetzt ist der Übergang zulässig.
    machine.apply_released(first, first_guard, machine.write_human(first, "APPROVE"))
    assert machine.tags["clm-a"] == tag(first.to_tag) != START_TAG

    # Freigabe und danach Widerruf: der Übergang bleibt aus.
    second, second_guard = machine.propose("clm-b")
    withdrawn_approval = machine.write_human(second, "APPROVE")
    machine.write_human(second, "WITHDRAW")
    machine.append(
        "CLAIM_RETAGGED",
        machine.raw_retag(second, second_guard.decision_id, withdrawn_approval.decision_id),
    )
    assert machine.tags["clm-b"] == START_TAG
    # Eine erneute Freigabe nach dem Widerruf wird abgewiesen; es braucht einen neuen Antrag.
    late_approval = machine.write_human(second, "APPROVE")
    assert late_approval.decision_id not in machine.state.human_decisions
    assert len(machine.state.rejected_events) == 3

    # Derselbe Stream über das produktive Ledger: Kette gültig, Zustand identisch.
    path = tmp_path / "erk_events.jsonl"
    ledger = Ledger(path)
    for event in machine.events:
        ledger.event(
            event["type"],
            event["payload"],
            event_id=event["event_id"],
            timestamp=event["timestamp"],
        )
    assert verify_chain_from_file(path) is True
    persisted = replay_events(load_ledger(path), policy=POLICY)
    assert persisted.state_digest == machine.state.state_digest
    assert persisted.current_tag("clm-a") == tag(first.to_tag)
    assert persisted.current_tag("clm-b") == START_TAG
