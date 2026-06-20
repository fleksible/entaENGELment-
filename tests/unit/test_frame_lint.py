# ruff: noqa: I001
import tools.frame_lint as frame_lint

TAXONOMY = frame_lint.load_yaml(frame_lint.DEFAULT_TAXONOMY)


def severities(result):
    return [f.severity for f in result.findings]


def reason_codes(result):
    return [f.reason_code for f in result.findings]


def test_valid_hypothesis_with_gov_audit_frame_passes_without_fail():
    item = {
        "claim_id": "CLAIM-FRAME-VALID-001",
        "receipt_id": "REC-FRAME-001",
        "claim_tag": "HYPOTHESE",
        "operative_frame": {
            "frame_id": "GOV_AUDIT",
            "frame_reason": "RC_G6_FRAME_001",
            "counterfactual_frame": "MYTH_ARCHETYPE",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "FAIL" not in severities(result)


def test_missing_frame_for_hypothesis_fails_and_short_circuits_content():
    item = {
        "claim_id": "CLAIM-FRAME-MISSING-001",
        "receipt_id": "REC-FRAME-002",
        "claim_tag": "HYPOTHESE",
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G6_FRAME_001" in reason_codes(result)
    assert result.failed


def test_wrong_taxonomy_fails_without_keyerror():
    item = {
        "claim_id": "CLAIM-FRAME-WRONG-001",
        "receipt_id": "REC-FRAME-003",
        "claim_tag": "HYPOTHESE",
        "operative_frame": {
            "frame_id": "NOT_A_FRAME",
            "frame_reason": "RC_TEST",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G6_FRAME_002" in reason_codes(result)
    assert result.failed


def test_met_alias_normalizes_to_myth_archetype_as_info_event():
    item = {
        "claim_id": "CLAIM-FRAME-MET-001",
        "receipt_id": "REC-FRAME-004",
        "claim_tag": "METAPHER",
        "operative_frame": {
            "frame_id": "MET",
            "frame_reason": "RC_TEST",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G6_FRAME_ALIAS_001" in reason_codes(result)
    assert result.canonical_frame_id == "MYTH_ARCHETYPE"
    assert "FAIL" not in severities(result)


def test_trigger_term_under_non_matching_frame_warns_when_not_counterfactual():
    item = {
        "claim_id": "CLAIM-FRAME-TRIGGER-001",
        "receipt_id": "REC-FRAME-005",
        "claim_tag": "HYPOTHESE",
        "text": "Josephson remains a model candidate for the BETSE bridge.",
        "operative_frame": {
            "frame_id": "BIO_VMEM",
            "frame_reason": "RC_TEST",
            "counterfactual_frame": "GOV_AUDIT",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G4_FRAME_TRIGGER_WARN_001" in reason_codes(result)
    assert "FAIL" not in severities(result)


def test_trigger_term_under_declared_counterfactual_frame_infos_only():
    item = {
        "claim_id": "CLAIM-BETSE-JOSEPHSON-001",
        "receipt_id": "REC-FRAME-005B",
        "claim_tag": "HYPOTHESE",
        "text": "Josephson remains a model candidate for the BETSE bridge.",
        "operative_frame": {
            "frame_id": "BIO_VMEM",
            "frame_reason": "RC_TEST",
            "counterfactual_frame": "PHYS",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G4_FRAME_TRIGGER_INFO_001" in reason_codes(result)
    assert "RC_G4_FRAME_TRIGGER_WARN_001" not in reason_codes(result)
    assert "FAIL" not in severities(result)


def test_custom_valid_passes_with_warn_for_missing_taxonomy_patch():
    item = {
        "claim_id": "CLAIM-FRAME-CUSTOM-001",
        "receipt_id": "REC-FRAME-006",
        "claim_tag": "HYPOTHESE",
        "operative_frame": {
            "frame_id": "CUSTOM",
            "frame_reason": "RC_TEST",
            "custom_frame_id": "LOCAL_FRAME",
            "custom_frame_reason": "local experiment",
            "validation_rule": "manual review",
            "counterfactual_frame": "GOV_AUDIT",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G6_FRAME_CUSTOM_WARN_001" in reason_codes(result)
    assert "FAIL" not in severities(result)


def test_custom_missing_required_field_fails():
    item = {
        "claim_id": "CLAIM-FRAME-CUSTOM-MISSING-001",
        "receipt_id": "REC-FRAME-007",
        "claim_tag": "HYPOTHESE",
        "operative_frame": {
            "frame_id": "CUSTOM",
            "frame_reason": "RC_TEST",
            "custom_frame_id": "LOCAL_FRAME",
            "counterfactual_frame": "GOV_AUDIT",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G6_FRAME_CUSTOM_001" in reason_codes(result)
    assert result.failed


def test_voluntary_fact_frame_is_validated_against_declared_frame():
    item = {
        "claim_id": "CLAIM-FRAME-FACT-001",
        "receipt_id": "REC-FRAME-008",
        "claim_tag": "FAKT",
        "operative_frame": {
            "frame_id": "MYTH_ARCHETYPE",
            "frame_reason": "RC_TEST",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G8_MYTH_EVIDENCE_001" in reason_codes(result)
    assert result.failed


def test_myth_as_fact_pilot_hard_fail_path():
    item = {
        "claim_id": "CLAIM-MYTH-AS-FACT-001",
        "receipt_id": "REC-FRAME-009",
        "claim_tag": "FAKT",
        "text": "The mythic frame proves the operational fact.",
        "operative_frame": {
            "frame_id": "MYTH_ARCHETYPE",
            "frame_reason": "RC_TEST",
        },
    }

    result = frame_lint.lint_item(item, TAXONOMY)

    assert "RC_G8_MYTH_EVIDENCE_001" in reason_codes(result)
    assert result.failed
