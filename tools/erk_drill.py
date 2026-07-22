#!/usr/bin/env python3
"""ERK Guard-Drill — die Fixtures als lebende Grenz-Übung.

Replayt alle ERK-Fixtures unter ``tests/fixtures/erk/`` und gleicht das
Ergebnis mit den dokumentierten Erwartungen ab (im Geist von
``docs/governance/GUARD_DRILL_CONTRACT_v0_1.md``): Der Lauf zeigt
menschenlesbar, dass die Grenzen des Kernels halten — nicht nur, dass eine
Testsuite grün ist.

Grenzen:
  - Rein lesend; kein Event wird erzeugt, nichts wird geschrieben.
  - Ein Drill macht keinen Claim wahr; er zeigt nur das Verhalten der Grenzen.

Usage:
    python tools/erk_drill.py [--fixtures tests/fixtures/erk]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from src.core.evidence_routing import ReplayState, replay_events
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.core.evidence_routing import ReplayState, replay_events

DEFAULT_FIXTURES = Path("tests") / "fixtures" / "erk"


def _load_fixture(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def _check_allowed_proposal(state: ReplayState) -> list[str]:
    problems = []
    if state.current_tag("clm-001") != "[HYPOTHESE]":
        problems.append("Proposal allein darf den Tag nicht ändern")
    if state.retag_history:
        problems.append("es darf kein Retagging geben")
    if state.rejected_events:
        problems.append("der Stream sollte ohne Ablehnungen replayen")
    return problems


def _check_human_approved(state: ReplayState) -> list[str]:
    problems = []
    if state.current_tag("clm-001") != "[MODEL]":
        problems.append("nach HumanDecision(APPROVE) sollte der Tag [MODEL] sein")
    if len(state.retag_history) != 1:
        problems.append("genau ein Retagging erwartet")
    if state.rejected_events:
        problems.append("der Stream sollte ohne Ablehnungen replayen")
    return problems


def _check_metaphor(state: ReplayState) -> list[str]:
    problems = []
    if state.current_tag("clm-010") != "[HYPOTHESE]":
        problems.append("Metapher darf keine Promotion tragen")
    guard = state.guard_decisions.get("gd-010", {})
    if guard.get("decision") != "HOLD":
        problems.append("Guard sollte HOLD sein")
    if "METAPHOR_IS_NOT_EVIDENCE" not in guard.get("reason_codes", []):
        problems.append("Reason-Code METAPHOR_IS_NOT_EVIDENCE erwartet")
    return problems


def _check_retraction(state: ReplayState) -> list[str]:
    problems = []
    claim = state.claims.get("clm-001", {})
    if not claim.get("retracted"):
        problems.append("Claim sollte als RETRACTED markiert sein")
    if len(state.retag_history) != 1:
        problems.append("die Retag-Historie darf durch Retraction nicht verschwinden")
    if "hd-001" not in state.human_decisions or "gd-001" not in state.guard_decisions:
        problems.append("Entscheidungs-Historie sollte vollständig erhalten bleiben")
    return problems


def _check_private_export(state: ReplayState) -> list[str]:
    from src.core.evidence_routing import reduce_public_export

    problems = []
    serialized = json.dumps(reduce_public_export(state).to_dict())
    for marker in ("PRIVATE_TEXT", "/private/diary", "biographical", "clm-020", "mat-020"):
        if marker in serialized:
            problems.append(f"privater Marker oder Roh-ID im Export: {marker}")
    return problems


DRILLS = {
    "allowed_proposal.jsonl": (
        "Erlaubter Übergang bleibt Vorschlag (Invarianten 1/7)",
        _check_allowed_proposal,
    ),
    "human_approved_retag.jsonl": (
        "Retagging nur nach HumanDecision(APPROVE) (Invariante 2)",
        _check_human_approved,
    ),
    "metaphor_no_promotion.jsonl": (
        "Metapher ist keine Evidenz (Invariante 3)",
        _check_metaphor,
    ),
    "retraction_non_destructive.jsonl": (
        "Rücknahme ist append-only (Invariante 6)",
        _check_retraction,
    ),
    "private_reduced_export.jsonl": (
        "Public Export bleibt reduziert (Invariante 11)",
        _check_private_export,
    ),
}


def run_drills(fixtures_dir: Path) -> bool:
    """Alle Drills laufen lassen; True bei durchgehend gehaltenen Grenzen."""
    all_ok = True
    for name, (description, check) in DRILLS.items():
        path = fixtures_dir / name
        if not path.is_file():
            print(f"[erk-drill] FEHLT   {name} — Fixture nicht gefunden")
            all_ok = False
            continue
        state = replay_events(_load_fixture(path))
        problems = check(state)
        if problems:
            all_ok = False
            print(f"[erk-drill] BRUCH   {name} — {description}")
            for problem in problems:
                print(f"[erk-drill]         -> {problem}")
        else:
            print(f"[erk-drill] HÄLT    {name} — {description}")
    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="ERK-Fixtures als Guard-Drill replayen")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES), help="Fixture-Verzeichnis")
    args = parser.parse_args()

    ok = run_drills(Path(args.fixtures))
    if ok:
        print("[erk-drill] Alle Grenzen halten. (Kein Claim wird dadurch wahr.)")
    else:
        raise SystemExit("[erk-drill] Mindestens eine Grenze hält nicht — bitte prüfen.")


if __name__ == "__main__":
    main()
