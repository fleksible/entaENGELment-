"""Lean-Crosswalk: Klassifikation von ``#print axioms``-Befunden und Kartenprüfung.

ANNEX / SPEC-WIP. Vertrag: ``docs/annex/LEAN_CROSSWALK_v0_1.md``.
Herkunft: ATLAS-CROSSWALK-LEAN-001 v0.3 (``reference.py``), hier korrigiert.

Grenzen dieses Moduls:

* Es führt Lean nicht aus. Es bewertet nur, was ein Lean-Lauf geliefert hat.
* ``FORMAL_CLOSED`` heißt: die genannte Lean-Deklaration hängt nur von den
  Standardaxiomen ab. Ob die Deklaration meint, was ein Mensch behauptet,
  bleibt eine getrennte, ungeprüfte Frage (``semantic_reentry``).
* Der Leser ``parse_print_axioms`` kennt nur die in der Lean-Dokumentation
  gezeigten Zeilenformen. Er wurde noch nie gegen eine echte Lean-Ausgabe
  gefahren (FIXTURE_ONLY / NOT_KERNEL_VERIFIED). Alles Unbekannte führt zu
  ``HOLD_INVALID_EVIDENCE``, nie zu einem Beweisurteil.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

# Die einzige Quelle der Status. Reihenfolge = Vorrang (oben gewinnt).
STATUSES: tuple[str, ...] = (
    "RUN_FAILED",
    "HOLD_INVALID_EVIDENCE",
    "HOLD_DECL_MISSING",
    "HOLD_DECL_DUPLICATE",
    "OPEN_OBLIGATION",
    "HOLD_TRUST_BOUNDARY",
    "FORMAL_CLOSED",
)

KINDS: Mapping[str, str] = {
    "RUN_FAILED": "NO_VERDICT",
    "HOLD_INVALID_EVIDENCE": "NO_VERDICT",
    "HOLD_DECL_MISSING": "NO_VERDICT",
    "HOLD_DECL_DUPLICATE": "NO_VERDICT",
    "OPEN_OBLIGATION": "PROOF-VOID",
    "HOLD_TRUST_BOUNDARY": "PROOF-DEPENDENCY",
    "FORMAL_CLOSED": "FORMAL-PROOF",
}

CEILINGS: Mapping[str, str] = {
    status: ("NONE" if kind == "NO_VERDICT" else "FORMAL") for status, kind in KINDS.items()
}

PRIMARY_REASONS: Mapping[str, str] = {
    "RUN_FAILED": "PROCESS_FAILED",
    "HOLD_INVALID_EVIDENCE": "EVIDENCE_UNUSABLE",
    "HOLD_DECL_MISSING": "DECLARATION_MISSING",
    "HOLD_DECL_DUPLICATE": "DECLARATION_DUPLICATE",
    "OPEN_OBLIGATION": "SORRY_DEPENDENCY",
    "HOLD_TRUST_BOUNDARY": "FOREIGN_AXIOM",
    "FORMAL_CLOSED": "STANDARD_AXIOMS_ONLY",
}

SUMMARY_TEMPLATES: Mapping[str, str] = {
    "RUN_FAILED": "Lean-Lauf gescheitert – kein Beweisurteil.",
    "HOLD_INVALID_EVIDENCE": (
        "Beweislage unbrauchbar (Format, Hash oder Vollständigkeit) – kein Beweisurteil."
    ),
    "HOLD_DECL_MISSING": "Erwartete Deklaration fehlt in der Ausgabe – kein Beweisurteil.",
    "HOLD_DECL_DUPLICATE": "Erwartete Deklaration mehrfach in der Ausgabe – kein Beweisurteil.",
    "OPEN_OBLIGATION": "Offene Beweisverpflichtung: hängt von sorryAx ab.",
    "HOLD_TRUST_BOUNDARY": "Hält nur unter nicht freigegebenen Zusatzannahmen.",
    "FORMAL_CLOSED": (
        "Formal geschlossen unter den Standardaxiomen; "
        "keine Aussage über die Bedeutung der Formalisierung."
    ),
}

# Exakter Namensvergleich: ``Foo.propext`` ist nicht ``propext``.
ALLOWED: frozenset[str] = frozenset({"propext", "Classical.choice", "Quot.sound"})
SORRY = "sorryAx"

# Zulässige Behälter für eine Axiomliste. Text, Bytes und Mappings sind keine Listen.
AXIOM_CONTAINERS = (list, tuple, set, frozenset)
AxiomInput = list[str] | tuple[str, ...] | set[str] | frozenset[str]

SEMANTIC_REENTRY = "SEPARATE_UNREVIEWED"
PROSE_REVIEW_STATE = "UNVERIFIED_PROSE"
CARD_FIELDS: frozenset[str] = frozenset(
    {
        "status",
        "kind",
        "claim_ceiling",
        "semantic_reentry",
        "origin_sha256",
        "axioms",
        "summary",
        "notes",
        "prose_review_state",
    }
)
_SHA256 = re.compile(r"[0-9a-f]{64}")

if not set(KINDS) == set(STATUSES) == set(SUMMARY_TEMPLATES) == set(PRIMARY_REASONS):
    raise RuntimeError("Statusquelle inkonsistent")


@dataclass(frozen=True)
class Verdict:
    """Strukturiertes Urteil zu genau einer Lean-Deklaration."""

    status: str
    kind: str
    claim_ceiling: str
    primary_reason: str
    axioms: tuple[str, ...] = ()
    foreign_axioms: tuple[str, ...] = ()


def _verdict(status: str, axioms: Iterable[str] = (), foreign: Iterable[str] = ()) -> Verdict:
    return Verdict(
        status=status,
        kind=KINDS[status],
        claim_ceiling=CEILINGS[status],
        primary_reason=PRIMARY_REASONS[status],
        axioms=tuple(sorted(set(axioms))),
        foreign_axioms=tuple(sorted(set(foreign))),
    )


def evidence_gate(
    run_ok: bool,
    evidence_integrity: bool = True,
    parse_known: bool = True,
    full_axiom_list: bool = True,
) -> str:
    """Vorprüfung: ``RUN_FAILED``, ``HOLD_INVALID_EVIDENCE`` oder ``PASS``.

    Nur ein echtes ``run_ok is False`` ergibt ``RUN_FAILED`` und hat Vorrang vor
    allem anderen. Jeder Schalter, der kein echtes ``bool`` ist (etwa ``"false"``,
    ``1`` oder ``None``), ergibt ``HOLD_INVALID_EVIDENCE``.
    """
    if run_ok is False:
        return "RUN_FAILED"
    flags = (run_ok, evidence_integrity, parse_known, full_axiom_list)
    if any(type(flag) is not bool for flag in flags):
        return "HOLD_INVALID_EVIDENCE"
    if not (evidence_integrity and parse_known and full_axiom_list):
        return "HOLD_INVALID_EVIDENCE"
    return "PASS"


def _valid_axiom_list(axioms: object) -> bool:
    """Nur ausdrückliche Sammlungen nichtleerer Axiomnamen; kein Text, kein Mapping."""
    if not isinstance(axioms, AXIOM_CONTAINERS):
        return False
    return all(isinstance(a, str) and _AXIOM_NAME.fullmatch(a) is not None for a in axioms)


def assess(
    run_ok: bool,
    decl_count: int,
    axioms: AxiomInput,
    *,
    evidence_integrity: bool = True,
    parse_known: bool = True,
    full_axiom_list: bool = True,
) -> Verdict:
    """Urteil nach Vorrang: Lauf > Beweislage > Deklaration > sorryAx > Fremdaxiom.

    Eingabekontrolle nach dem Gate und vor dem Deklarationsstatus:
    ``decl_count`` muss ein echtes ``int`` (kein ``bool``) und mindestens 0 sein,
    ``axioms`` eine ``list``, ``tuple``, ``set`` oder ``frozenset`` aus
    nichtleeren Axiomnamen. Sonst ``HOLD_INVALID_EVIDENCE``.
    """
    gate = evidence_gate(run_ok, evidence_integrity, parse_known, full_axiom_list)
    if gate != "PASS":
        return _verdict(gate)
    if type(decl_count) is not int or decl_count < 0:
        return _verdict("HOLD_INVALID_EVIDENCE")
    if not _valid_axiom_list(axioms):
        return _verdict("HOLD_INVALID_EVIDENCE")
    if decl_count == 0:
        return _verdict("HOLD_DECL_MISSING")
    if decl_count != 1:
        return _verdict("HOLD_DECL_DUPLICATE")
    foreign = [a for a in axioms if a != SORRY and a not in ALLOWED]
    if SORRY in axioms:
        # Mischfall: sorryAx gewinnt, Fremdaxiome bleiben als Zusatzbefund erhalten.
        return _verdict("OPEN_OBLIGATION", axioms, foreign)
    if foreign:
        return _verdict("HOLD_TRUST_BOUNDARY", axioms, foreign)
    return _verdict("FORMAL_CLOSED", axioms)


def classify(run_ok: bool, decl_count: int, axioms: AxiomInput, **gate: bool) -> str:
    """Nur der Status von :func:`assess` (Kompatibilität zu v0.3)."""
    return assess(run_ok, decl_count, axioms, **gate).status


def summary_for(status: str) -> str:
    return SUMMARY_TEMPLATES[status]


def build_card(verdict: Verdict, origin_sha256: str, notes: str | None = None) -> dict:
    """Sichtbare Karte. Die Zusammenfassung kommt fest aus der Vorlage;
    freier Text darf nur in ``notes`` stehen und bleibt ``UNVERIFIED_PROSE``."""
    if not _SHA256.fullmatch(origin_sha256):
        raise ValueError("origin_sha256 muss 64 Kleinbuchstaben-Hexzeichen haben")
    if notes is not None and not isinstance(notes, str):
        raise TypeError("notes muss Text oder None sein")
    return {
        "status": verdict.status,
        "kind": verdict.kind,
        "claim_ceiling": verdict.claim_ceiling,
        "semantic_reentry": SEMANTIC_REENTRY,
        "origin_sha256": origin_sha256,
        "axioms": list(verdict.axioms),
        "summary": summary_for(verdict.status),
        "notes": notes,
        "prose_review_state": PROSE_REVIEW_STATE,
    }


def validate_card(card: object, verdict: Verdict, origin_sha256: str) -> tuple[str, ...]:
    """Prüft eine sichtbare Karte gegen Urteil und Herkunft.

    Leeres Ergebnis heißt bestanden. Freier Text in ``notes`` wird nicht
    inhaltlich geprüft; geprüft wird nur, dass er als ungeprüft markiert ist
    und nicht im Zusammenfassungsfeld steht.
    """
    # Der übergebene Hash wird auf Typ und Format geprüft. Das belegt nur seine
    # Form, nicht dass er aus einer echten Lean-Ausgabe berechnet wurde.
    origin_ok = isinstance(origin_sha256, str) and _SHA256.fullmatch(origin_sha256) is not None
    if not isinstance(card, dict) or set(card) != CARD_FIELDS:
        return ("MALFORMED_CARD",) if origin_ok else ("MALFORMED_CARD", "PROVENANCE_DRIFT")
    reasons: list[str] = []
    if card["status"] != verdict.status:
        reasons.append("STATUS_DRIFT")
    if card["kind"] != KINDS[verdict.status]:
        reasons.append("TYPE_DRIFT")
    if card["claim_ceiling"] != CEILINGS[verdict.status]:
        reasons.append("CLAIM_ESCALATION")
    if card["semantic_reentry"] != SEMANTIC_REENTRY:
        reasons.append("SEMANTIC_PROMOTION")
    if not origin_ok or card["origin_sha256"] != origin_sha256:
        reasons.append("PROVENANCE_DRIFT")
    if card["axioms"] != list(verdict.axioms):
        reasons.append("AXIOM_DISPLAY_DRIFT")
    if card["summary"] != summary_for(verdict.status):
        reasons.append("UNVERIFIED_SUMMARY")
    if card["prose_review_state"] != PROSE_REVIEW_STATE:
        reasons.append("PROSE_PROMOTION")
    if card["notes"] is not None and not isinstance(card["notes"], str):
        reasons.append("MALFORMED_CARD")
    return tuple(reasons)


# --- Rohausgabe von ``#print axioms`` ---------------------------------------

_PREFIX = r"(?:\S+:\d+:\d+: )?(?:info: )?"
_DEPENDS = re.compile(rf"^{_PREFIX}'(?P<decl>.+)' depends on axioms: \[(?P<axioms>.+)\]$")
_NONE = re.compile(rf"^{_PREFIX}'(?P<decl>.+)' does not depend on any axioms$")
_AXIOM_NAME = re.compile(r"[^\s,\[\]]+")


@dataclass(frozen=True)
class ParsedOutput:
    records: tuple[tuple[str, tuple[str, ...]], ...]
    unknown_lines: tuple[str, ...]


def parse_print_axioms(output: str) -> ParsedOutput:
    """Liest nur die dokumentierten Zeilenformen; alles andere ist unbekannt."""
    records: list[tuple[str, tuple[str, ...]]] = []
    unknown: list[str] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        match = _DEPENDS.match(line)
        if match:
            names = tuple(match["axioms"].split(", "))
            if all(_AXIOM_NAME.fullmatch(name) for name in names):
                records.append((match["decl"], names))
                continue
        match = _NONE.match(line)
        if match:
            records.append((match["decl"], ()))
            continue
        unknown.append(line)
    return ParsedOutput(tuple(records), tuple(unknown))


def audit_raw(exit_code: int, output: str, expected_decls: Sequence[str]) -> dict[str, Verdict]:
    """Rohausgabe → ein Urteil je erwarteter Deklaration, fail-closed.

    * Exit-Code ungleich 0: alle ``RUN_FAILED``, die Ausgabe wird nicht gelesen.
    * Unbekannte Zeile oder unerwartete Deklaration: alle ``HOLD_INVALID_EVIDENCE``.
    * Fehlende oder doppelte Deklaration: nur diese erhält ein HOLD.
    """
    if len(set(expected_decls)) != len(expected_decls):
        raise ValueError("erwartete Deklarationen müssen eindeutig sein")
    if exit_code != 0:
        return {decl: assess(False, 0, []) for decl in expected_decls}
    parsed = parse_print_axioms(output)
    seen = Counter(decl for decl, _ in parsed.records)
    if parsed.unknown_lines or set(seen) - set(expected_decls):
        return {decl: assess(True, 0, [], parse_known=False) for decl in expected_decls}
    axioms_of = dict(parsed.records)
    return {
        decl: assess(True, seen[decl], list(axioms_of.get(decl, ())) if seen[decl] == 1 else [])
        for decl in expected_decls
    }
