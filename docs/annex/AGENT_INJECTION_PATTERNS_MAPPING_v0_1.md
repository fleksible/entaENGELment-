# AGENT_INJECTION_PATTERNS_MAPPING_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** keines neu
**Datum:** 2026-10-28
**Anlass:** Vorschlag V7 (Checkup 2026-10-28, Gegen-Review)
**Bezug:** G5 in `AGENTS.md`, `.claude/rules/security.md`, `src/core/action_gate.py`,
`src/core/evidence_routing.py`

---

## 1. Zweck

Die vorhandenen Grenzen des Evidence Routing Kernel (ERK) und des Action-Gate
werden ehrlich auf die Architekturmuster gegen Prompt-Injection abgebildet. Es
wird nichts Neues implementiert; benannt wird, was existiert und was fehlt.

## 2. Vorhandene Grenzen

- **Action-Gate:** erzeugt ausschließlich inerte `ActionProposal`-Manifeste
  (`PROPOSE`/`HOLD`); keine Ausführung, kein Netzwerk, kein Dateisystem
  (strukturell geprüft in `tests/ethics/test_action_gate_no_execution.py`).
  `PROPOSE != AUTHORIZE`: Es gibt keinen ausführenden Consumer.
- **ERK:** Retagging nur nach `HumanDecision(APPROVE)` (Invariante 2); untrusted
  Material promotet nie direkt (Invariante 8); unbekannter Trust → `UNTRUSTED`.
- **Sichtbarkeit:** Ein Proposal ist nie öffentlicher als seine Quelle; der
  öffentliche Export lässt private Records ganz weg.
- **G5 (Regeln):** Muster-Erkennung (`SYSTEM:`, `IGNORE PREVIOUS` …) und
  Quarantäne. Das sind Regeln für Agenten, keine Laufzeitgrenze.

## 3. Abbildung auf die Entwurfsmuster

Muster nach Beurer-Kellner et al., „Design Patterns for Securing LLM Agents
against Prompt Injections“ (arXiv 2506.08837, Abschnitt 3.1; Volltext gelesen).

| Muster | Kern laut Paper | Stand im Repo |
|---|---|---|
| Action-Selector | Anfrage → vordefinierte Aktion, keine Rückkopplung aus Ergebnissen | **teilweise analog:** Das Action-Gate bildet eine Anweisung auf ein festes Manifest-Schema mit geschlossenem Reason-Code-Vokabular ab. Es wählt aber keine Aktion aus und führt nichts aus. |
| Plan-Then-Execute | Plan der Tool-Aufrufe vor dem Lesen untrusted Daten fixieren | **nicht implementiert.** Es gibt keinen Plan und keine Ausführung, nur inerte Vorschläge. |
| LLM Map-Reduce | untrusted Teile isoliert verarbeiten, dann aggregieren | nicht implementiert |
| Dual LLM | privilegiertes Modell ohne untrusted Daten, quarantänisiertes ohne Tools | nicht implementiert; G5 empfiehlt Quarantäne nur organisatorisch |
| Code-Then-Execute | Programm statt freier Planung; mit Capability-Tracking (CaMeL) | nicht implementiert |
| Context-Minimization | unnötigen Kontext nach Gebrauch entfernen | nicht implementiert |

Wichtig aus dem Paper: Ein fixierter Plan schützt nicht die **Parameter** der
Aufrufe. Untrusted Daten können Argumente weiter beeinflussen („the agent's plan
of tool calls is fixed, but a prompt injection can still manipulate the inputs to
these tool calls“). Die Datenfluss-Kontrolle von CaMeL adressiert genau das; das
Repo hat nichts Vergleichbares.

## 4. Lücke: Ableitungsverfolgung für Trust (VOID-Kandidat)

Heute trägt jedes `MaterialRef` seinen eigenen `trust`-Wert. Wird aus untrusted
Material ein neues Artefakt abgeleitet (Zusammenfassung, Extrakt, Übersetzung),
gibt es keinen Mechanismus, der den Status mitführt. Ein abgeleitetes Material
könnte mit `REVIEWED` angelegt werden, ohne dass seine Herkunft das verhindert.

**Vorgeschlagener VOID-Kandidat** (nicht in `VOIDMAP.yml` eingetragen; das ist
GOLD und braucht eine eigene Entscheidung):

- Titel: Trust-Ableitung für abgeleitetes Material
- Problem: kein `derived_from` und keine Regel „abgeleiteter Trust ≤ minimaler
  Trust der Quellen“
- Abnahme-Idee: ein abgeleitetes Material aus mindestens einer untrusted Quelle
  wird ohne `HumanDecision` nie besser als `UNTRUSTED` eingestuft; Test analog
  Invariante 8.

## 5. Tests in diesem PR

`tests/ethics/test_trust_visibility_boundaries.py` hält das heutige Verhalten fest:
unbekannter oder fehlerhafter Trust (Kleinschreibung, Leerzeichen, falscher Typ,
`str`-Subklasse im Action-Gate) → `UNTRUSTED`/`HOLD`; ein Proposal ist nie
öffentlicher als seine Quelle, und eine unbekannte Quell-Sichtbarkeit gilt als
`private`. Abgeleitetes Material deckt der Test nicht ab, weil es nicht modelliert ist.

## 6. Quellen

- Beurer-Kellner et al., Design Patterns for Securing LLM Agents against Prompt
  Injections, arXiv 2506.08837 (v3, 27.06.2025), https://arxiv.org/abs/2506.08837
  — Volltext (HTML) gelesen, Abschnitt 3.1 und 4.3.
- CaMeL wird nur über die Beschreibung in diesem Paper referenziert; das
  CaMeL-Paper selbst wurde nicht gelesen.
