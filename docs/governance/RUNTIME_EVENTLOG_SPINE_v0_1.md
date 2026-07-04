# RUNTIME_EVENTLOG_SPINE_v0_1

**Status:** Draft / Intake-Kandidat  
**Datum:** 2026-07-04  
**Claim-Status:** [SPEC-WIP]  
**Bezug:** `spec/runtime_eventlog_v0_1.json`

---

## Zweck

Das Runtime Eventlog dokumentiert Zustandsänderungen. Es ist Ereignisspur, nicht Wahrheitsquelle.

---

## Eventgruppen

- `CLAIM_CREATED`
- `CLAIM_RETAGGED`
- `VOID_OPENED`
- `VOID_CLOSED`
- `GUARD_DRILL_RUN`
- `R_DOWN_APPLIED`
- `VERIFY_PASS`
- `VERIFY_PASS_UNSIGNED`
- `SIGNED_EVIDENCE_PASS`
- `SIGNED_EVIDENCE_SKIPPED`
- `SIGNED_EVIDENCE_FAIL`

---

## Grundregeln

1. Events sollen append-only sein.
2. Event-Hashes machen Änderungen prüfbar, aber nicht wahr.
3. Öffentliche Snapshots müssen reduziert bleiben.
4. Claim-Transitionen brauchen Status, Grund und Actor.
5. VOID-Schließung braucht einen Evidence- oder Review-Pfad.
6. Guard-Drills brauchen ein Ergebnis und möglichst ein Receipt.

---

## Nächste Schritte

- Gegen bestehende Ledger-Implementierung prüfen.
- Eventtypen zunächst als Draft behalten.
- Später serverseitige Transition-Regeln definieren.
