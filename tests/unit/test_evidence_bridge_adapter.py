"""Unit-Tests für den Dual-Format Claim Bridge Adapter v0.1 (M1 -> ERK)."""

import dataclasses

import pytest

from src.core.evidence_bridge_adapter import (
    BRIDGE_SCHEMA_VERSION,
    BridgeAdapterError,
    BridgeReason,
    BridgeRecord,
    bridge_record_from_mapping,
    translate_bridge_record,
    validate_bridge_record,
)
from src.core.evidence_routing import (
    PROMOTION_CAPABLE_RELATION_TYPES,
    TRUST_REVIEWED,
    VISIBILITY_PRIVATE,
    ReasonCode,
    load_claim_policy,
)


def make_record(**overrides):
    data = {
        "bridge_id": "brg-001",
        "source_register": "formal",
        "source_pointer": "docs/annex/example_structure.md#L10-L20",
        "source_digest": "sha256:00",
        "transferred_property": "Ordnungsrelation der Knoten",
        "preserved_relation": "Nachbarschaft bleibt unter der Projektion erhalten",
        "relation_type": "CONTEXTUALIZES",
        "known_loss": ["Kantengewichte gehen verloren"],
        "falsifier": "Ein Gegenbeispiel mit vertauschter Nachbarschaft",
        "rollback": "HumanDecision(WITHDRAW) auf req-001",
        "intended_use": "explain",
    }
    data.update(overrides)
    return BridgeRecord(**data)


class TestStructuralValidation:
    def test_valid_record_passes(self):
        validate_bridge_record(make_record())

    @pytest.mark.parametrize(
        "field,reason",
        [
            ("transferred_property", BridgeReason.TRANSFERRED_PROPERTY_REQUIRED),
            ("preserved_relation", BridgeReason.PRESERVED_RELATION_REQUIRED),
            ("falsifier", BridgeReason.FALSIFIER_REQUIRED),
            ("rollback", BridgeReason.ROLLBACK_REQUIRED),
            ("source_pointer", BridgeReason.SOURCE_POINTER_REQUIRED),
        ],
    )
    def test_missing_mandatory_text_fails_closed(self, field, reason):
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(**{field: "   "}))
        assert reason in excinfo.value.reasons

    def test_known_loss_is_mandatory(self):
        # Eine Brücke ohne sichtbaren Verlust behauptet implizit Identität.
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(known_loss=[]))
        assert BridgeReason.KNOWN_LOSS_REQUIRED in excinfo.value.reasons

    def test_blank_known_loss_entry_is_rejected(self):
        with pytest.raises(BridgeAdapterError):
            validate_bridge_record(make_record(known_loss=["  "]))

    def test_unknown_register_and_relation_fail_closed(self):
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(source_register="astrology"))
        assert BridgeReason.UNKNOWN_SOURCE_REGISTER in excinfo.value.reasons

        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(relation_type="PROVES"))
        assert BridgeReason.UNKNOWN_RELATION_TYPE in excinfo.value.reasons

    def test_unknown_fields_are_rejected(self):
        payload = dataclasses.asdict(make_record())
        payload["secret_score"] = 0.9
        with pytest.raises(BridgeAdapterError):
            bridge_record_from_mapping(payload)

    def test_mapping_roundtrip(self):
        payload = dataclasses.asdict(make_record())
        assert bridge_record_from_mapping(payload) == make_record()


class TestRegisterReach:
    """Wie weit ein Quellregister relational reichen darf."""

    @pytest.mark.parametrize("register", ["myth", "metaphor", "psychological", "ui"])
    @pytest.mark.parametrize("relation", sorted(PROMOTION_CAPABLE_RELATION_TYPES))
    def test_non_promoting_registers_cannot_support(self, register, relation):
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(source_register=register, relation_type=relation))
        assert BridgeReason.REGISTER_CANNOT_PROMOTE in excinfo.value.reasons

    @pytest.mark.parametrize("register", ["myth", "metaphor", "psychological", "ui"])
    def test_non_promoting_registers_may_contextualize(self, register):
        validate_bridge_record(
            make_record(source_register=register, relation_type="CONTEXTUALIZES")
        )
        validate_bridge_record(make_record(source_register=register, relation_type="MOTIVATES"))

    @pytest.mark.parametrize("register", ["physical", "biological"])
    def test_physical_registers_need_m5_pointer_for_promotion(self, register):
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(source_register=register, relation_type="MEASURES"))
        assert BridgeReason.M5_REVIEW_REQUIRED in excinfo.value.reasons

        # Mit dokumentiertem M5-Review ist dieselbe Relation strukturell zulässig.
        validate_bridge_record(
            make_record(
                source_register=register,
                relation_type="MEASURES",
                m5_review_pointer="docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md#bench-001",
            )
        )

    @pytest.mark.parametrize("register", ["physical", "biological"])
    def test_physical_registers_may_contextualize_without_m5(self, register):
        validate_bridge_record(
            make_record(source_register=register, relation_type="CONTEXTUALIZES")
        )


class TestClaimTagBoundary:
    @pytest.mark.parametrize("tag", ["[FACT]", "[SPEC]", "[CANON]"])
    def test_adapter_must_not_assign_strong_tags(self, tag):
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(proposed_claim_tag=tag))
        assert BridgeReason.ADAPTER_CANNOT_ASSIGN_TAG in excinfo.value.reasons

    def test_alias_is_normalized_before_the_ban_applies(self):
        # [FAKT] normalisiert auf [FACT] und muss ebenso abgelehnt werden.
        policy = load_claim_policy()
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(proposed_claim_tag="[FAKT]"), policy=policy)
        assert BridgeReason.ADAPTER_CANNOT_ASSIGN_TAG in excinfo.value.reasons

    def test_unknown_tag_fails_closed(self):
        policy = load_claim_policy()
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(make_record(proposed_claim_tag="[TOTALLY-NEW]"), policy=policy)
        assert BridgeReason.UNKNOWN_CLAIM_TAG in excinfo.value.reasons

    def test_weak_tags_are_allowed(self):
        policy = load_claim_policy()
        for tag in ("[METAPHER]", "[ROSETTA]", "[HYPOTHESE]", "[MODEL]"):
            validate_bridge_record(make_record(proposed_claim_tag=tag), policy=policy)


class TestTranslation:
    def test_translation_emits_nothing_and_returns_proposals(self, tmp_path):
        translation = translate_bridge_record(make_record())
        assert translation.schema_version == BRIDGE_SCHEMA_VERSION
        assert translation.material.locator == "docs/annex/example_structure.md#L10-L20"
        # Relation zeigt auf genau das erzeugte Material:
        assert translation.relation.material_id == translation.material.material_id
        # Kein Claim ohne ausdrücklich vorgeschlagenes Tag:
        assert translation.claim is None
        # Nichts wurde geschrieben:
        assert list(tmp_path.iterdir()) == []

    def test_source_expression_never_leaves_the_bridge(self):
        translation = translate_bridge_record(make_record())
        serialized = str(translation.to_dict())
        assert "source_expression" not in serialized

    def test_trust_defaults_to_untrusted_and_blocks_promotion(self):
        translation = translate_bridge_record(
            make_record(relation_type="IMPLEMENTS", source_register="formal")
        )
        assert translation.material.trust == "UNTRUSTED"
        assert translation.promotion_capable is False
        assert ReasonCode.UNTRUSTED_MATERIAL.value in translation.relation.reason_codes

    def test_reviewed_trust_allows_promotion_capability(self):
        translation = translate_bridge_record(
            make_record(relation_type="IMPLEMENTS", source_register="formal"),
            trust=TRUST_REVIEWED,
        )
        assert translation.promotion_capable is True

    def test_protected_origin_forces_private_visibility(self):
        translation = translate_bridge_record(
            make_record(protected_origin=True, visibility="public")
        )
        assert translation.material.visibility == VISIBILITY_PRIVATE
        assert translation.relation.visibility == VISIBILITY_PRIVATE

    def test_metaphor_register_marks_kernel_reason_code(self):
        translation = translate_bridge_record(
            make_record(source_register="metaphor", relation_type="MOTIVATES")
        )
        assert translation.material.kind == "metaphor"
        assert ReasonCode.METAPHOR_IS_NOT_EVIDENCE.value in translation.relation.reason_codes
        assert translation.promotion_capable is False

    def test_provenance_only_marks_kernel_reason_code(self):
        translation = translate_bridge_record(make_record(relation_type="PROVENANCE_ONLY"))
        assert ReasonCode.PROVENANCE_IS_NOT_EVIDENCE.value in translation.relation.reason_codes
        assert translation.promotion_capable is False

    def test_relation_reason_codes_stay_within_kernel_vocabulary(self):
        known = {code.value for code in ReasonCode}
        for register, relation in (
            ("metaphor", "MOTIVATES"),
            ("formal", "PROVENANCE_ONLY"),
            ("governance", "CONTEXTUALIZES"),
        ):
            translation = translate_bridge_record(
                make_record(source_register=register, relation_type=relation)
            )
            assert set(translation.relation.reason_codes) <= known

    def test_adapter_local_reasons_never_reach_the_relation(self):
        translation = translate_bridge_record(
            make_record(source_register="metaphor", relation_type="MOTIVATES")
        )
        adapter_local = {reason.value for reason in BridgeReason}
        assert not (set(translation.relation.reason_codes) & adapter_local)
        # Sie erscheinen ausschließlich als Notiz im Übersetzungsergebnis:
        assert BridgeReason.REGISTER_CANNOT_PROMOTE in translation.notes

    def test_claim_candidate_uses_proposed_tag(self):
        policy = load_claim_policy()
        translation = translate_bridge_record(
            make_record(proposed_claim_tag="[HYPOTHESE]", claim_text="Beispielsatz."),
            policy=policy,
        )
        assert translation.claim is not None
        assert translation.claim.claim_tag == "[HYPOTHESE]"
        assert translation.claim.material_refs == [translation.material.material_id]

    def test_translation_is_deterministic(self):
        first = translate_bridge_record(make_record())
        second = translate_bridge_record(make_record())
        assert first.to_dict() == second.to_dict()


class TestSourceModuleMinimalTests:
    """Die vier Minimaltests aus dem Quellmodul 01_DUAL_FORMAT_CLAIM_BRIDGE."""

    def test_1_josephson_jesus_stays_metaphor(self):
        """Muss [METAPHER]/[ROSETTA] bleiben; kein Tunneling- oder Theologiebeweis."""
        policy = load_claim_policy()
        record = make_record(
            bridge_id="brg-josephson",
            source_register="metaphor",
            transferred_property="Vermittlung zwischen zwei getrennten Zuständen",
            preserved_relation="Kopplung über eine Barriere",
            relation_type="MOTIVATES",
            known_loss=["Keine Aussage über Ladungstransport oder Theologie"],
            proposed_claim_tag="[METAPHER]",
        )
        translation = translate_bridge_record(record, policy=policy)
        assert translation.promotion_capable is False
        assert translation.claim.claim_tag == "[METAPHER]"

        # Als Stützung derselben Brücke ist sie unzulässig:
        with pytest.raises(BridgeAdapterError):
            validate_bridge_record(dataclasses.replace(record, relation_type="SUPPORTS"))

    def test_2_seven_by_nine_yggdrasil_requires_relation_and_loss(self):
        """Muss die Knoten-/Kantenrelation und Gegenbeispiele nennen."""
        record = make_record(
            bridge_id="brg-yggdrasil",
            source_register="myth",
            transferred_property="Verzweigungsgrad der Knoten",
            preserved_relation="Baumstruktur ohne Zyklen",
            relation_type="CONTEXTUALIZES",
            known_loss=["Neun Welten sind keine Gitterdimension"],
            falsifier="Ein Gegenbeispiel mit Zyklus im behaupteten Baum",
        )
        translate_bridge_record(record)

        # Ohne benannten Verlust: keine Übersetzung.
        with pytest.raises(BridgeAdapterError):
            validate_bridge_record(dataclasses.replace(record, known_loss=[]))

    def test_3_rcc8_photonics_needs_m5_when_measuring(self):
        """Eine EC/PO-Zuordnung wird erst mit Messgröße und Prüfung tragend."""
        # Als formale Struktur bleibt sie ein Architekturhinweis:
        translate_bridge_record(
            make_record(
                bridge_id="brg-rcc8",
                source_register="formal",
                transferred_property="Überlappungsrelation zweier Regionen",
                preserved_relation="EC/PO-Unterscheidung",
                relation_type="CONTEXTUALIZES",
                known_loss=["Kein Layout, keine Kopplungsparameter, keine Messgröße"],
            )
        )
        # Sobald sie als Messung am Bauteil auftritt, greift das M5-Gate:
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(
                make_record(
                    bridge_id="brg-rcc8-bench",
                    source_register="physical",
                    relation_type="MEASURES",
                    known_loss=["Kalibrierung offen"],
                )
            )
        assert BridgeReason.M5_REVIEW_REQUIRED in excinfo.value.reasons

    def test_4_love_hrv_must_fail(self):
        """Ein normativer Begriff darf nicht durch einen physiologischen Proxy ersetzt werden."""
        # Der normative Wert selbst kann nichts messen oder stützen:
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(
                make_record(
                    bridge_id="brg-love",
                    source_register="psychological",
                    transferred_property="bedingungslose Zuwendung",
                    preserved_relation="Kohärenz",
                    relation_type="MEASURES",
                    known_loss=["Normativer Begriff ist keine Messgröße"],
                )
            )
        assert BridgeReason.REGISTER_CANNOT_PROMOTE in excinfo.value.reasons

        # Und das Biosignal darf ohne M5-Prüfung nichts stützen:
        with pytest.raises(BridgeAdapterError) as excinfo:
            validate_bridge_record(
                make_record(
                    bridge_id="brg-hrv",
                    source_register="biological",
                    transferred_property="HRV-Kennwert",
                    preserved_relation="zeitliche Variabilität",
                    relation_type="SUPPORTS",
                    known_loss=["Confounder nicht kontrolliert"],
                )
            )
        assert BridgeReason.M5_REVIEW_REQUIRED in excinfo.value.reasons
