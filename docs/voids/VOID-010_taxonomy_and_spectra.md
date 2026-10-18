# VOID-010 — Taxonomie & Spektren (Empirie)

**Status:** IN_PROGRESS
**Priority:** high
**Target:** 2027-01-31 (verlängert am 2026-10-18)

## Symptom
Die spektrale Taxonomie (z.B. MOD_18) ist konzeptionell definiert, aber es fehlt eine empirisch belastbare Zuordnung: *welche Quellen/Organismen/Materialien emittieren in welchen Spektren unter welchen Bedingungen?*

## Bridge

- Systematischer Literatur-Scan (peer-reviewed, sources first).
- Extraktion in eine kleine, zitierte Tabelle (CSV + Sources).
- Audit: jeder Datensatz bekommt Source, Timestamp, Scope und Claim-Boundary.

## Closing Path

- `data/spectra/` (CSV) with a small schema-backed source table.
- Evidence bundle under `data/receipts/` or `receipts/`.
- Tests: schema validation + Quellenpflicht.

## 2026-06-11 Re-baseline

Issue #240 correctly marked the previous 2026-06-01 target as overdue. The VOID remains open by design: the valuable ambiguity is empirical taxonomy, not implementation wiring. The next boundary is therefore a verifier-readable source table, not prose closure.

## Stand 2026-10-18

- Gerüst angelegt: `data/spectra/spectra_sources.csv` (nur Kopfzeile) und `spectra_sources.schema.json` ([SPEC-WIP]).
- Quellenpflicht-Lint: `python tools/spectra_table_lint.py`, Tests in `tests/unit/test_spectra_table_lint.py`.
- Offen bleibt der Literatur-Scan. Er braucht ≥ 5 begutachtete Quellen und wird manuell geprüft; bis dahin stehen keine Daten in der Tabelle.
