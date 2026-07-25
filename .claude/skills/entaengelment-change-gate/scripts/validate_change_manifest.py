#!/usr/bin/env python3
"""Change-Manifest Validator (entaengelment-change-gate v0.1).

Zweck: Ein Change-Manifest strukturell prüfen, bevor eine nichttriviale
Änderung ausgeführt wird. Der Validator operationalisiert ausschließlich
bereits vorhandene Repo-Regeln und führt keine neuen ein.

Quellenbindung (jede Regel unten trägt einen Repo-Pfad):
  - Guards G0-G6 .............. CLAUDE.md
  - GOLD/ANNEX/IMMUTABLE ...... .claude/rules/annex.md
  - Fokus / Fokus-Switch ...... .claude/rules/metatron.md
  - untrusted Inhalte ......... .claude/rules/security.md
  - Claim-Register ............ policies/claim_tags_v0_2.yaml (nur gelesen/referenziert)
  - HumanDecision-Grenze ...... docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md
  - verbotene Endzustände ..... docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md (§11)

Grenzen dieses Skripts:
  - Es ist kein Guard der Verify-Membran und in keiner CI-Stufe verdrahtet.
  - Es entscheidet nichts, was dem Menschen vorbehalten ist.
  - Sein Ergebnis ist ein lokaler technischer Befund, kein Claim-Status,
    kein Governance-Status und keine Validierung im Sinne von
    policies/claim_tags_v0_2.yaml.
  - Reine Lesearbeit: kein Netzwerk, kein Prozessstart, kein Schreibzugriff,
    keine Ausführung von Inhalten aus dem Manifest.

Usage:
    python3 .claude/skills/entaengelment-change-gate/scripts/\\
        validate_change_manifest.py <manifest.yaml> [--json] [--repo-root PATH]

Exit-Codes:
    0  ELIGIBLE_FOR_EXTERNAL_REVIEW  (kein Befund)
    1  HOLD                          (Befund oder selbst deklariertes HOLD)
    2  Eingabefehler                  (Datei nicht lesbar oder YAML nicht parsebar)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover - Kern-Dependency laut requirements.txt
    print("[ERROR] PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

SCHEMA_ID = "entaengelment-change-gate/change-manifest/v0.1"

# --------------------------------------------------------------------------
# Lokales Vokabular
#
# Diese Codes sind AUSSCHLIESSLICH lokal. Sie sind nicht die ReasonCodes aus
# src/core/evidence_routing.py, werden nie in Ledger, Receipts oder Events
# geschrieben und begründen keinen Projektstatus.
# --------------------------------------------------------------------------

# Befunde: Struktur
MANIFEST_UNPARSEABLE = "MANIFEST_UNPARSEABLE"
MANIFEST_NOT_MAPPING = "MANIFEST_NOT_MAPPING"
MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
UNKNOWN_FIELD = "UNKNOWN_FIELD"
FIELD_TYPE_INVALID = "FIELD_TYPE_INVALID"
EMPTY_REQUIRED_VALUE = "EMPTY_REQUIRED_VALUE"
UNKNOWN_ENUM_VALUE = "UNKNOWN_ENUM_VALUE"
FOCUS_WORD_COUNT_INVALID = "FOCUS_WORD_COUNT_INVALID"

# Befunde: Selbstautorisierung
FORBIDDEN_SELF_ATTESTATION = "FORBIDDEN_SELF_ATTESTATION"
FINAL_PASS_NOT_PERMITTED = "FINAL_PASS_NOT_PERMITTED"

# Befunde: Schichtgrenzen
GOLD_PATH_REQUIRES_HUMAN_DECISION = "GOLD_PATH_REQUIRES_HUMAN_DECISION"
GOLD_PATH_UNDECLARED = "GOLD_PATH_UNDECLARED"
IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION = "IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION"
IMMUTABLE_PATH_UNDECLARED = "IMMUTABLE_PATH_UNDECLARED"
NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION = "NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION"
NICHTRAUM_PATH_UNDECLARED = "NICHTRAUM_PATH_UNDECLARED"
PATH_ALLOWLIST_CONFLICT = "PATH_ALLOWLIST_CONFLICT"

# Befunde: Wirkung
HUMAN_DECISION_WITHOUT_QUESTION = "HUMAN_DECISION_WITHOUT_QUESTION"
PROMOTION_WITHOUT_HUMAN_DECISION = "PROMOTION_WITHOUT_HUMAN_DECISION"
AUTHORITY_EFFECT_UNDERSTATED = "AUTHORITY_EFFECT_UNDERSTATED"
CLAIM_EFFECT_UNDERSTATED = "CLAIM_EFFECT_UNDERSTATED"
POSSIBLE_PARALLEL_SYSTEM = "POSSIBLE_PARALLEL_SYSTEM"

# Befunde: Quellenbindung, Verlust, Rücknahme
SOURCE_OF_TRUTH_PATH_MISSING = "SOURCE_OF_TRUTH_PATH_MISSING"
SOURCE_OF_TRUTH_PATH_ESCAPES_REPO = "SOURCE_OF_TRUTH_PATH_ESCAPES_REPO"
MISSING_KNOWN_LOSS = "MISSING_KNOWN_LOSS"
UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS = "UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS"
REVERSIBLE_WITHOUT_ROLLBACK = "REVERSIBLE_WITHOUT_ROLLBACK"
IRREVERSIBLE_WITHOUT_ROLLBACK = "IRREVERSIBLE_WITHOUT_ROLLBACK"
IRREVERSIBLE_WITHOUT_HUMAN_DECISION = "IRREVERSIBLE_WITHOUT_HUMAN_DECISION"

# Ergebniswerte. Beide sind bereits belegte, ausdrücklich als "kein Status"
# markierte Formulierungen (docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §11).
# HOLD ist hier gate-lokal: keine Übersetzung nach M2-Navigation, ERK-Guard
# oder Claim-[VOID] (ebd. §9).
VERDICT_HOLD = "HOLD"
VERDICT_ELIGIBLE = "ELIGIBLE_FOR_EXTERNAL_REVIEW"

# --------------------------------------------------------------------------
# Enums und Pfadklassen
# --------------------------------------------------------------------------

CHANGE_CLASSES = (
    "DOCUMENTATION",
    "CODE",
    "TEST",
    "TOOLING",
    "WORKFLOW",
    "GOVERNANCE_ADJACENT",
    # Wörtlicher Repo-Begriff, docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §2:
    # mehrdeutige Eingaben bleiben unentschieden, es gibt keine automatische
    # Wahl der stärkeren Klasse.
    "CLASSIFICATION_UNDETERMINED",
)

EFFECT_VALUES = ("none", "requested")
REVERSIBILITY_VALUES = ("REVERSIBLE", "IRREVERSIBLE")
GATE_OUTCOMES = (VERDICT_HOLD, VERDICT_ELIGIBLE)

# Pfadklassen. Diese Listen sind Kopien und keine zweiten Definitionen;
# tests/unit/test_change_gate_manifest.py prüft, dass jedes Präfix in der
# jeweils genannten Quelldatei wörtlich belegt ist (Drift wird sichtbar).
#
# Quelle GOLD/IMMUTABLE: .claude/rules/annex.md (Schnellreferenz)
GOLD_PREFIXES = ("index/", "policies/", "VOIDMAP.yml", "VOIDMAP.yaml", "spec/", "seeds/")
IMMUTABLE_PREFIXES = ("data/receipts/", "receipts/")
# Quelle NICHTRAUM: CLAUDE.md (G2 Nichtraum-Schutz) — annex.md führt diese
# Schicht nicht, deshalb hier ein eigener Quellverweis.
NICHTRAUM_PREFIXES = ("NICHTRAUM/",)

# Geschützte Schichten in einer Tabelle: Schlüssel in affected_layers, Label
# für die Meldung, Reason-Code bei fehlender menschlicher Entscheidung,
# Reason-Code bei undeklarierter Freigabe, Pfadpräfixe.
PROTECTED_LAYERS = (
    ("gold", "GOLD", GOLD_PATH_REQUIRES_HUMAN_DECISION, GOLD_PATH_UNDECLARED, GOLD_PREFIXES),
    (
        "immutable",
        "IMMUTABLE",
        IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION,
        IMMUTABLE_PATH_UNDECLARED,
        IMMUTABLE_PREFIXES,
    ),
    (
        "nichtraum",
        "NICHTRAUM",
        NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION,
        NICHTRAUM_PATH_UNDECLARED,
        NICHTRAUM_PREFIXES,
    ),
)

# Flächen, deren Berührung eine Claim-Wirkung wahrscheinlich macht.
CLAIM_SURFACE_PREFIXES = GOLD_PREFIXES

# Fokus-Wortgrenzen. Quelle: .claude/rules/metatron.md ("FOKUS: <2-5 Wörter
# die das Ziel beschreiben>"). Gezählt wird whitespace-basiert; keine
# linguistische Tokenisierung.
FOCUS_MIN_WORDS = 2
FOCUS_MAX_WORDS = 5

# Endgültige Selbstattestierungen. Quelle:
# docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §11 (PASS, VALIDATED, PROVEN,
# SAFE, CLINICALLY_READY, ETHICALLY_APPROVED) plus [CANON] als höchster
# Claim-Tag aus policies/claim_tags_v0_2.yaml.
#
# Bekannter Verlust: "GOLD" wird hier bewusst NICHT geprüft, weil das Wort in
# Manifesten legitim als Schichtname vorkommt. GOLD-Wirkung wird stattdessen
# über die Pfadregeln erfasst.
SELF_ATTESTATION_TOKENS = (
    "AUTO_APPROVED",
    "CANON",
    "CLINICALLY_READY",
    "ETHICALLY_APPROVED",
    "PROVEN",
    "SAFE",
    "SELF_VALIDATED",
    "TRUE",
    "VALIDATED",
)


# Ein in eckige Klammern gesetzter Tag ist eine Referenz auf das Claim-Register
# (z.B. "[CANON]") und keine Selbstattestierung.
def _bare_token_pattern(token: str) -> re.Pattern[str]:
    return re.compile(r"(?<!\[)\b" + re.escape(token) + r"\b(?!\])")


_SELF_ATTESTATION_PATTERNS = tuple(
    (token, _bare_token_pattern(token)) for token in SELF_ATTESTATION_TOKENS
)
_FINAL_PASS_PATTERN = _bare_token_pattern("PASS")

# --------------------------------------------------------------------------
# Feldschema (geschlossen: unbekannte Felder sind fail-closed)
# --------------------------------------------------------------------------

REQUIRED_STRING_FIELDS = ("focus", "requested_change", "expected_gate_outcome")
REQUIRED_LIST_FIELDS = (
    "change_class",
    "existing_sources_of_truth",
    "known_loss",
    "falsifiers",
    "allowed_paths",
    "forbidden_paths",
    "verification_commands",
    "unresolved_points",
)
REQUIRED_MAPPING_FIELDS = (
    "affected_layers",
    "authority_effect",
    "claim_effect",
    "human_decision",
    "possible_parallel_system",
    "reversibility",
)
# Listen, die leer bleiben dürfen.
OPTIONAL_EMPTY_LISTS = ("known_loss", "forbidden_paths", "unresolved_points")

AFFECTED_LAYER_KEYS = ("gold", "annex", "immutable", "nichtraum", "untrusted_inputs")

# Getrennte Bedeutungen statt eines mehrdeutigen Bool-Flags:
# systems_checked = wogegen geprüft wurde, detected_overlaps = was gefunden
# wurde. Die frühere Form (`detected`/`overlaps`) ist damit ein unbekanntes
# Feld und läuft nicht still durch.
PARALLEL_SYSTEM_KEYS = ("systems_checked", "detected_overlaps", "mitigation")

TOP_LEVEL_FIELDS = tuple(
    sorted(REQUIRED_STRING_FIELDS + REQUIRED_LIST_FIELDS + REQUIRED_MAPPING_FIELDS)
)


class Finding(NamedTuple):
    """Ein einzelner Befund. Kein Fehler-Ranking, keine Gewichtung."""

    code: str
    field: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "field": self.field, "detail": self.detail}


class ValidationResult(NamedTuple):
    verdict: str
    findings: tuple[Finding, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA_ID,
            "verdict": self.verdict,
            "findings": [f.as_dict() for f in self.findings],
        }


# --------------------------------------------------------------------------
# Hilfsfunktionen (rein, ohne Seiteneffekte)
# --------------------------------------------------------------------------


def _is_str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _nonempty_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def _normalize_path(raw: str) -> str:
    """Pfad vereinheitlichen, ohne führende Punkte von Dot-Verzeichnissen zu verlieren."""
    value = raw.strip()
    while value.startswith("./"):
        value = value[2:]
    return value.rstrip("/")


def count_focus_words(focus: str) -> int:
    """Wörter im Fokus whitespace-basiert zählen.

    Bewusst einfach und deterministisch: ``str.split()`` fasst beliebige
    Whitespace-Folgen (auch Tabs und Zeilenumbrüche) zusammen, sodass
    zusätzlicher Whitespace das Ergebnis nicht verändert. Keine
    linguistische Tokenisierung, keine Silben- oder Bindestrich-Analyse —
    "Change-Gate Skill" zählt als zwei Wörter.
    """
    return len(focus.split())


def _matches_prefix(path: str, prefixes: Sequence[str]) -> bool:
    normalized = _normalize_path(path)
    for prefix in prefixes:
        clean = prefix.rstrip("/")
        if normalized == clean or normalized.startswith(clean + "/"):
            return True
    return False


def _collect_strings(node: Any) -> list[str]:
    """Alle String-Werte eines Manifests einsammeln (Werte, keine Schlüssel)."""
    found: list[str] = []
    if isinstance(node, str):
        found.append(node)
    elif isinstance(node, list):
        for item in node:
            found.extend(_collect_strings(item))
    elif isinstance(node, dict):
        for item in node.values():
            found.extend(_collect_strings(item))
    return found


# --------------------------------------------------------------------------
# Prüfschichten
# --------------------------------------------------------------------------


def _check_structure(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    for key in sorted(data.keys()):
        if not isinstance(key, str) or key not in TOP_LEVEL_FIELDS:
            findings.append(
                Finding(UNKNOWN_FIELD, str(key), "unbekanntes Feld; Schema ist geschlossen")
            )

    for field in REQUIRED_STRING_FIELDS:
        if field not in data:
            findings.append(Finding(MISSING_REQUIRED_FIELD, field, "Pflichtfeld fehlt"))
        elif not isinstance(data[field], str):
            findings.append(Finding(FIELD_TYPE_INVALID, field, "String erwartet"))
        elif not data[field].strip():
            findings.append(Finding(EMPTY_REQUIRED_VALUE, field, "leerer Pflichtwert"))
        elif field == "focus":
            # Der Fokus-Vertrag aus .claude/rules/metatron.md ist ausführbar:
            # 2-5 Wörter. Ein leerer Fokus ist oben schon gemeldet.
            words = count_focus_words(data[field])
            if not FOCUS_MIN_WORDS <= words <= FOCUS_MAX_WORDS:
                findings.append(
                    Finding(
                        FOCUS_WORD_COUNT_INVALID,
                        "focus",
                        f"{words} Wort(e); erlaubt sind {FOCUS_MIN_WORDS}-"
                        f"{FOCUS_MAX_WORDS} (.claude/rules/metatron.md)",
                    )
                )

    for field in REQUIRED_LIST_FIELDS:
        if field not in data:
            findings.append(Finding(MISSING_REQUIRED_FIELD, field, "Pflichtfeld fehlt"))
        elif not _is_str_list(data[field]):
            findings.append(Finding(FIELD_TYPE_INVALID, field, "Liste von Strings erwartet"))
        elif field not in OPTIONAL_EMPTY_LISTS and not _nonempty_strings(data[field]):
            findings.append(Finding(EMPTY_REQUIRED_VALUE, field, "leere Pflichtliste"))

    for field in REQUIRED_MAPPING_FIELDS:
        if field not in data:
            findings.append(Finding(MISSING_REQUIRED_FIELD, field, "Pflichtfeld fehlt"))
        elif not isinstance(data[field], dict):
            findings.append(Finding(FIELD_TYPE_INVALID, field, "Mapping erwartet"))

    findings.extend(_check_nested_shapes(data))
    return findings


def _check_nested_shapes(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    layers = data.get("affected_layers")
    if isinstance(layers, dict):
        for key in sorted(layers.keys()):
            if key not in AFFECTED_LAYER_KEYS:
                findings.append(
                    Finding(UNKNOWN_FIELD, f"affected_layers.{key}", "unbekannte Schicht")
                )
        for key in AFFECTED_LAYER_KEYS:
            if key not in layers:
                findings.append(
                    Finding(MISSING_REQUIRED_FIELD, f"affected_layers.{key}", "Schicht fehlt")
                )
            elif not _is_str_list(layers[key]):
                findings.append(
                    Finding(
                        FIELD_TYPE_INVALID,
                        f"affected_layers.{key}",
                        "Liste von Strings erwartet",
                    )
                )

    for field, allowed in (("authority_effect", EFFECT_VALUES), ("claim_effect", EFFECT_VALUES)):
        block = data.get(field)
        if not isinstance(block, dict):
            continue
        findings.extend(_check_closed_keys(block, ("value", "explanation"), field))
        findings.extend(_check_enum(block.get("value"), allowed, f"{field}.value"))
        if not isinstance(block.get("explanation"), str):
            findings.append(Finding(FIELD_TYPE_INVALID, f"{field}.explanation", "String erwartet"))

    human = data.get("human_decision")
    if isinstance(human, dict):
        findings.extend(_check_closed_keys(human, ("required", "questions"), "human_decision"))
        if not isinstance(human.get("required"), bool):
            findings.append(
                Finding(FIELD_TYPE_INVALID, "human_decision.required", "Boolean erwartet")
            )
        if not _is_str_list(human.get("questions")):
            findings.append(
                Finding(
                    FIELD_TYPE_INVALID, "human_decision.questions", "Liste von Strings erwartet"
                )
            )

    parallel = data.get("possible_parallel_system")
    if isinstance(parallel, dict):
        findings.extend(
            _check_closed_keys(parallel, PARALLEL_SYSTEM_KEYS, "possible_parallel_system")
        )
        for key in ("systems_checked", "detected_overlaps"):
            if key not in parallel:
                findings.append(
                    Finding(
                        MISSING_REQUIRED_FIELD,
                        f"possible_parallel_system.{key}",
                        "Pflichtfeld fehlt",
                    )
                )
            elif not _is_str_list(parallel[key]):
                findings.append(
                    Finding(
                        FIELD_TYPE_INVALID,
                        f"possible_parallel_system.{key}",
                        "Liste von Strings erwartet",
                    )
                )
        if not isinstance(parallel.get("mitigation"), str):
            findings.append(
                Finding(
                    FIELD_TYPE_INVALID, "possible_parallel_system.mitigation", "String erwartet"
                )
            )

    reversibility = data.get("reversibility")
    if isinstance(reversibility, dict):
        findings.extend(
            _check_closed_keys(reversibility, ("value", "rollback_path"), "reversibility")
        )
        findings.extend(
            _check_enum(reversibility.get("value"), REVERSIBILITY_VALUES, "reversibility.value")
        )
        if not isinstance(reversibility.get("rollback_path"), str):
            findings.append(
                Finding(FIELD_TYPE_INVALID, "reversibility.rollback_path", "String erwartet")
            )

    if _is_str_list(data.get("change_class")):
        for value in data["change_class"]:
            findings.extend(_check_enum(value, CHANGE_CLASSES, "change_class"))

    if isinstance(data.get("expected_gate_outcome"), str):
        findings.extend(
            _check_enum(data["expected_gate_outcome"], GATE_OUTCOMES, "expected_gate_outcome")
        )

    return findings


def _check_closed_keys(block: dict[str, Any], allowed: Sequence[str], prefix: str) -> list[Finding]:
    findings: list[Finding] = []
    for key in sorted(block.keys()):
        if key not in allowed:
            findings.append(Finding(UNKNOWN_FIELD, f"{prefix}.{key}", "unbekanntes Feld im Block"))
    return findings


def _check_enum(value: Any, allowed: Sequence[str], field: str) -> list[Finding]:
    if value is None:
        return [Finding(MISSING_REQUIRED_FIELD, field, "Pflichtwert fehlt")]
    if not isinstance(value, str):
        return [Finding(FIELD_TYPE_INVALID, field, "String erwartet")]
    if value not in allowed:
        return [
            Finding(
                UNKNOWN_ENUM_VALUE,
                field,
                "'{}' nicht in {{{}}}".format(value, ", ".join(allowed)),
            )
        ]
    return []


def _check_self_attestation(data: dict[str, Any]) -> list[Finding]:
    """Endgültige Selbstattestierung im gesamten Manifest erkennen."""
    findings: list[Finding] = []
    seen: set = set()
    for text in _collect_strings(data):
        for token, pattern in _SELF_ATTESTATION_PATTERNS:
            if pattern.search(text) and token not in seen:
                seen.add(token)
                findings.append(
                    Finding(
                        FORBIDDEN_SELF_ATTESTATION,
                        "manifest",
                        f"endgültige Selbstattestierung '{token}' ist nicht zulässig "
                        "(docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §11)",
                    )
                )
        if _FINAL_PASS_PATTERN.search(text) and "PASS" not in seen:
            seen.add("PASS")
            findings.append(
                Finding(
                    FINAL_PASS_NOT_PERMITTED,
                    "manifest",
                    "endgültiger 'PASS' ist kein zulässiger Agentenzustand "
                    "(docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md §5)",
                )
            )
    return findings


def _check_layer_boundaries(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    layers = data.get("affected_layers")
    if not isinstance(layers, dict):
        return findings

    human_ok = _human_decision_is_concrete(data)

    for key, label, human_code, undeclared_code, prefixes in PROTECTED_LAYERS:
        declared = _nonempty_strings(layers.get(key))
        if declared and not human_ok:
            findings.append(
                Finding(
                    human_code,
                    f"affected_layers.{key}",
                    f"{len(declared)} Pfad(e) berührt; erfordert "
                    "human_decision.required=true mit konkreter Frage "
                    "(.claude/rules/annex.md)",
                )
            )
        # Nicht deklarierte Berührung derselben Schicht über allowed_paths.
        # Fail-closed für jede geschützte Schicht: eine Freigabe ohne
        # Deklaration darf nicht still durchlaufen.
        undeclared = sorted(
            path
            for path in _nonempty_strings(data.get("allowed_paths"))
            if _matches_prefix(path, prefixes)
            and not any(_normalize_path(path) == _normalize_path(d) for d in declared)
        )
        if undeclared:
            findings.append(
                Finding(
                    undeclared_code,
                    "allowed_paths",
                    f"{label}-Pfad(e) freigegeben, aber nicht in "
                    f"affected_layers.{key} deklariert: " + ", ".join(undeclared),
                )
            )

    untrusted = _nonempty_strings(layers.get("untrusted_inputs"))
    if untrusted and not _nonempty_strings(data.get("known_loss")):
        findings.append(
            Finding(
                UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS,
                "affected_layers.untrusted_inputs",
                "untrusted Eingaben ohne deklarierten Verlust " "(.claude/rules/security.md)",
            )
        )

    return findings


def _check_path_conflicts(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    allowed = _nonempty_strings(data.get("allowed_paths"))
    forbidden = _nonempty_strings(data.get("forbidden_paths"))
    conflicts = sorted(
        {path for path in allowed if _matches_prefix(path, [_normalize_path(f) for f in forbidden])}
    )
    if conflicts:
        findings.append(
            Finding(
                PATH_ALLOWLIST_CONFLICT,
                "allowed_paths",
                "gleichzeitig erlaubt und verboten: {}".format(", ".join(conflicts)),
            )
        )
    return findings


def _human_decision_is_concrete(data: dict[str, Any]) -> bool:
    human = data.get("human_decision")
    if not isinstance(human, dict) or human.get("required") is not True:
        return False
    questions = _nonempty_strings(human.get("questions"))
    return any(q.strip().endswith("?") for q in questions)


def _mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Teil-Mapping holen; ein fehlender oder falsch getippter Block wird leer."""
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _check_effects(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    layers = _mapping(data, "affected_layers")
    change_class = _nonempty_strings(data.get("change_class"))
    governance_adjacent = "GOVERNANCE_ADJACENT" in change_class

    human = data.get("human_decision")
    if isinstance(human, dict) and human.get("required") is True:
        questions = _nonempty_strings(human.get("questions"))
        if not any(q.strip().endswith("?") for q in questions):
            findings.append(
                Finding(
                    HUMAN_DECISION_WITHOUT_QUESTION,
                    "human_decision.questions",
                    "human_decision.required=true ohne konkrete Frage (mit '?')",
                )
            )

    authority = _mapping(data, "authority_effect")
    claim = _mapping(data, "claim_effect")
    authority_value = authority.get("value")
    claim_value = claim.get("value")

    gold_touched = bool(_nonempty_strings(layers.get("gold")))
    claim_surface = sorted(
        path
        for path in _nonempty_strings(data.get("allowed_paths"))
        if _matches_prefix(path, CLAIM_SURFACE_PREFIXES)
    )

    authority_explanation = authority.get("explanation")
    authority_explained = isinstance(authority_explanation, str) and bool(
        authority_explanation.strip()
    )
    if authority_value == "none" and gold_touched:
        findings.append(
            Finding(
                AUTHORITY_EFFECT_UNDERSTATED,
                "authority_effect.value",
                "'none' behauptet, obwohl GOLD berührt wird",
            )
        )
    elif authority_value == "none" and governance_adjacent and not authority_explained:
        # Fail-closed, aber ohne Zwang zur Hochstufung: bei GOVERNANCE_ADJACENT
        # muss 'none' begründet sein. Verlangt wird eine Begründung, nicht der
        # Wechsel auf 'requested'.
        findings.append(
            Finding(
                AUTHORITY_EFFECT_UNDERSTATED,
                "authority_effect.explanation",
                "'none' bei GOVERNANCE_ADJACENT ohne Begründung",
            )
        )

    if claim_value == "none" and claim_surface:
        findings.append(
            Finding(
                CLAIM_EFFECT_UNDERSTATED,
                "claim_effect.value",
                "'none' behauptet, obwohl Claim-Fläche freigegeben ist: {}".format(
                    ", ".join(claim_surface)
                ),
            )
        )

    if (authority_value == "requested" or claim_value == "requested") and not (
        isinstance(human, dict) and human.get("required") is True
    ):
        findings.append(
            Finding(
                PROMOTION_WITHOUT_HUMAN_DECISION,
                "human_decision.required",
                "beantragte Authority-/Claim-Wirkung ohne menschliche Entscheidung "
                "(docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md §7, Invariante 2)",
            )
        )

    if governance_adjacent and not _nonempty_strings(data.get("known_loss")):
        findings.append(
            Finding(
                MISSING_KNOWN_LOSS,
                "known_loss",
                "GOVERNANCE_ADJACENT ohne deklarierten Verlust "
                "(docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §12)",
            )
        )

    return findings


def _check_parallel_system(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    parallel = data.get("possible_parallel_system")
    if not isinstance(parallel, dict):
        return findings

    # Zwei getrennte Bedeutungen: systems_checked = wogegen geprüft wurde,
    # detected_overlaps = was tatsächlich gefunden wurde. Ein leeres
    # detected_overlaps heißt nur "keine Überschneidung deklariert gefunden" —
    # nicht, dass keine Prüfung stattfand.
    systems_checked = _nonempty_strings(parallel.get("systems_checked"))
    detected_overlaps = _nonempty_strings(parallel.get("detected_overlaps"))
    mitigation = parallel.get("mitigation")
    mitigation_text = mitigation.strip() if isinstance(mitigation, str) else ""
    governance_adjacent = "GOVERNANCE_ADJACENT" in _nonempty_strings(data.get("change_class"))

    if detected_overlaps and not mitigation_text:
        findings.append(
            Finding(
                POSSIBLE_PARALLEL_SYSTEM,
                "possible_parallel_system.mitigation",
                "erkannte Überschneidung ohne benannte Gegenmaßnahme",
            )
        )
    if governance_adjacent and not systems_checked:
        findings.append(
            Finding(
                POSSIBLE_PARALLEL_SYSTEM,
                "possible_parallel_system.systems_checked",
                "GOVERNANCE_ADJACENT ohne benannte geprüfte Systeme; "
                "fail-closed statt stillschweigend verneint",
            )
        )
    return findings


def _check_sources_of_truth(data: dict[str, Any], repo_root: Path | None) -> list[Finding]:
    findings: list[Finding] = []
    for raw in _nonempty_strings(data.get("existing_sources_of_truth")):
        candidate = raw.strip()
        if candidate.startswith("/") or ".." in Path(candidate).parts:
            findings.append(
                Finding(
                    SOURCE_OF_TRUTH_PATH_ESCAPES_REPO,
                    "existing_sources_of_truth",
                    f"kein repo-relativer Pfad: {candidate}",
                )
            )
            continue
        if repo_root is not None and not (repo_root / candidate).exists():
            findings.append(
                Finding(
                    SOURCE_OF_TRUTH_PATH_MISSING,
                    "existing_sources_of_truth",
                    f"Pfad existiert nicht im Repository: {candidate}",
                )
            )
    return findings


def _check_reversibility(data: dict[str, Any]) -> list[Finding]:
    """Rücknahmepfad prüfen.

    Ein Rücknahmepfad ist in beiden Fällen Pflicht (CLAUDE.md G3:
    "Reversibilität erhalten"; docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md §3:
    jede Stufe nennt einen Rücknahmepfad). Der Validator prüft ausschließlich,
    **ob** ein Pfad konkret deklariert ist — nicht, ob er fachlich funktioniert.
    """
    findings: list[Finding] = []
    block = data.get("reversibility")
    if not isinstance(block, dict):
        return findings

    value = block.get("value")
    if value not in REVERSIBILITY_VALUES:
        # Unbekannter Wert ist bereits als UNKNOWN_ENUM_VALUE gemeldet.
        return findings

    rollback = block.get("rollback_path")
    if not isinstance(rollback, str) or not rollback.strip():
        code = (
            IRREVERSIBLE_WITHOUT_ROLLBACK
            if value == "IRREVERSIBLE"
            else REVERSIBLE_WITHOUT_ROLLBACK
        )
        findings.append(
            Finding(
                code,
                "reversibility.rollback_path",
                f"{value}: kein konkreter Rücknahmepfad deklariert (CLAUDE.md G3)",
            )
        )

    if value == "IRREVERSIBLE" and not _human_decision_is_concrete(data):
        findings.append(
            Finding(
                IRREVERSIBLE_WITHOUT_HUMAN_DECISION,
                "reversibility.value",
                "irreversible Änderung ohne konkrete menschliche Entscheidungsfrage",
            )
        )
    return findings


# --------------------------------------------------------------------------
# Öffentliche API
# --------------------------------------------------------------------------


def validate_manifest(data: Any, repo_root: Path | None = None) -> ValidationResult:
    """Ein geladenes Manifest prüfen. Rein, deterministisch, ohne Seiteneffekte.

    Bei identischer Eingabe ist das Ergebnis identisch: Befunde werden stabil
    nach (code, field, detail) sortiert; es gibt keine Zeitstempel, keine
    Zufallswerte und keine Umgebungsabhängigkeit ausser dem optionalen
    Existenz-Check gegen ``repo_root``.
    """
    if not isinstance(data, dict):
        return ValidationResult(
            VERDICT_HOLD,
            (Finding(MANIFEST_NOT_MAPPING, "manifest", "YAML-Mapping erwartet"),),
        )

    findings: list[Finding] = []
    findings.extend(_check_structure(data))
    findings.extend(_check_self_attestation(data))
    findings.extend(_check_layer_boundaries(data))
    findings.extend(_check_path_conflicts(data))
    findings.extend(_check_effects(data))
    findings.extend(_check_parallel_system(data))
    findings.extend(_check_sources_of_truth(data, repo_root))
    findings.extend(_check_reversibility(data))

    unique = sorted(set(findings), key=lambda f: (f.code, f.field, f.detail))
    verdict = VERDICT_HOLD if unique else VERDICT_ELIGIBLE
    # Ein selbst deklariertes HOLD wird respektiert und nie hochgestuft.
    if data.get("expected_gate_outcome") == VERDICT_HOLD:
        verdict = VERDICT_HOLD
    return ValidationResult(verdict, tuple(unique))


def load_manifest_text(text: str) -> tuple[Any, Finding | None]:
    """YAML-Text sicher laden (``safe_load``: keine Objektkonstruktion)."""
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as exc:
        first_line = str(exc).splitlines()[0] if str(exc).splitlines() else "YAML-Fehler"
        return None, Finding(MANIFEST_UNPARSEABLE, "manifest", first_line)


def render_text(result: ValidationResult) -> str:
    lines = ["=== CHANGE-GATE MANIFEST CHECK ==="]
    lines.append(f"schema: {SCHEMA_ID}")
    lines.append(f"verdict: {result.verdict}")
    if result.findings:
        lines.append("")
        lines.append(f"Befunde ({len(result.findings)}):")
        for finding in result.findings:
            lines.append(f"  - [{finding.code}] {finding.field}: {finding.detail}")
    else:
        lines.append("")
        lines.append("Keine strukturellen Befunde.")
    lines.append("")
    lines.append(
        "Hinweis: Dies ist ein begrenzter technischer Befund über das Manifest, "
        "kein Claim-Status, keine Freigabe und kein Ersatz für eine menschliche "
        "Entscheidung."
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Change-Manifest strukturell prüfen (lokal, offline, read-only)."
    )
    parser.add_argument("manifest", help="Pfad zum Change-Manifest (YAML)")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON ausgeben")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repo-Wurzel für den Existenz-Check von existing_sources_of_truth",
    )
    parser.add_argument(
        "--no-path-check",
        action="store_true",
        help="Existenz-Check der Source-of-Truth-Pfade überspringen",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[ERROR] Manifest nicht lesbar: {exc}", file=sys.stderr)
        return 2

    data, parse_finding = load_manifest_text(text)
    if parse_finding is not None:
        # Nicht parsebares YAML ist ein Eingabefehler, kein inhaltlicher
        # Befund: Exit 2, wie im Modul-Docstring und im Schema dokumentiert.
        # Das fail-closed Verdikt bleibt HOLD, damit der Befund sichtbar ist.
        result = ValidationResult(VERDICT_HOLD, (parse_finding,))
        _emit(result, as_json=args.json)
        return 2

    repo_root: Path | None = None
    if not args.no_path_check:
        repo_root = Path(args.repo_root) if args.repo_root else Path(__file__).resolve().parents[4]
    result = validate_manifest(data, repo_root)
    _emit(result, as_json=args.json)
    return 0 if result.verdict == VERDICT_ELIGIBLE else 1


def _emit(result: ValidationResult, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(render_text(result))


if __name__ == "__main__":
    sys.exit(main())
