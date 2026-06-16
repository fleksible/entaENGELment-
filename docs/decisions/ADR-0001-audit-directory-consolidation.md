# ADR-0001: Audit-Reports in `docs/audit/` konsolidieren (statt neuem `docs/audits/`)

- **Status:** Proposed (Review-Frage offen, siehe Audit §10)
- **Datum:** 2026-06-16
- **Kontext-Fokus:** Revolutionary Repository Audit

## Context

Der Audit-Auftrag spezifiziert Deliverables unter `docs/audits/` (Plural). Das
Repository besitzt jedoch bereits ein etabliertes `docs/audit/` (Singular) mit 19
Audit-Dokumenten. Es gibt keine Referenz auf `docs/audits/` im Repo. Ein neues
`docs/audits/` neben `docs/audit/` würde eine stille Struktur-Duplikation erzeugen
— genau die Klasse von Problem, die dieser Audit aufdecken soll.

## Decision

Alle neuen Audit-Deliverables (Auditbericht, Ergebnisbericht) werden in das
**bestehende `docs/audit/`** geschrieben. Die Plural-Variante `docs/audits/` wird
**nicht** angelegt.

## Consequences

- (+) Keine Verzeichnis-Duplikation; ein einziger Ort für Audit-Reports.
- (+) Konsistent mit dem Anti-Duplikations-Ziel des Audits.
- (−) Abweichung vom wörtlichen Auftragspfad → als Review-Frage markiert.
- Reversibel: Umbenennung `docs/audit/` → `docs/audits/` ist jederzeit möglich,
  betrifft dann aber alle 19 Bestandsdateien und etwaige Querverweise.

## Alternatives Considered

1. **Neues `docs/audits/` anlegen** — verworfen: erzeugt Duplikat.
2. **`docs/audit/` → `docs/audits/` umbenennen** — verworfen für Phase 2:
   strukturelle Umbenennung von Bestands-Kanon erfordert Consent (G0/G1) und
   Querverweis-Prüfung. Kandidat für SEMANTIC REVIEW.

## Essence Preservation Note

Reine Verzeichnis-/Ablageentscheidung. Keine inhaltliche Umdeutung, kein
Kanon-Begriff berührt. Claim-Disziplin und symbolische Architektur unverändert.

## Update 2026-06-16 (Follow-up nach PR #252)

- [FAKT] `docs/audit/` bleibt vorerst der **bestätigte** kanonische Audit-Pfad.
  Eine spätere Pluralisierung (`docs/audits/`) wäre Gegenstand einer eigenen ADR.
- [FAKT] Die `.gitignore`-Regel `audit/` (erfasste auch `docs/audit/` und erzwang
  `git add -f`) wurde auf Root-Ebene eingegrenzt: `/audit/` (inkl. anker-korrekter
  Negationen `!/audit/…`). Neue Reports unter `docs/audit/` sind jetzt ohne `-f`
  trackbar; top-level `audit/`-Verhalten bleibt identisch.
- [FAKT] Rein struktureller Safe Patch — kein Kanon-, Spec-, VOID-, Claim- oder
  Roadmap-Inhalt verändert.

## Linked VOID / Spec / Claim

- Audit: `docs/audit/revolutionary_repo_audit_2026-06-16.md` §4, §8, §10
- Kein VOID, keine Spec berührt.
