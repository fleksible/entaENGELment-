# VOIDMAP Backlog

> Auto-generated from `VOIDMAP.yml`. Do not edit by hand.
> Regenerate via: `python3 tools/voids_backlog_gen.py`
> Source `last_updated`: 2026-06-11

## Summary

| Status | Count |
|--------|-------|
| OPEN | 1 |
| IN_PROGRESS | 2 |
| SUSPENDED | 1 |
| CLOSED | 9 |
| **Total** | **13** |

## OPEN

| ID | Title | Priority | Owner | Domain | Target | Symptom |
|---|---|---|---|---|---|---|
| VOID-LOGZN-001 | LOG-ZN Orbit als Windungs-Gedächtnisoperator | high | fleks | [MATH][META] | — | Der entwickelte Winkel / log(z)-Orbit ist als neuer RZT-Operator erkannt, aber noch nicht in Tests, Metrics oder Receipts verankert. |

## IN_PROGRESS

| ID | Title | Priority | Owner | Domain | Target | Symptom |
|---|---|---|---|---|---|---|
| VOID-010 | Taxonomie & Spektren (Empirie) | high | fleks | [PHYS] | 2026-07-15 | Spektrale Zuordnung ohne belastbare Literatur-/Datenbasis |
| VOID-011 | Metriken der Resonanz (MI, PLV, FD) | high | fleks | [MATH] | 2026-07-15 | MI/FD implementation exists; evidence boundary needs simulation receipt and claim-tagged metric export |

## SUSPENDED

| ID | Title | Priority | Owner | Domain | Target | Symptom |
|---|---|---|---|---|---|---|
| VOID-014 | Protein-Design (in-silico, safety-bounded) | medium | fleks | [BIO] | — | Exploration gewünscht, aber hohes Risiko bei operativen Laboranleitungen |

## CLOSED (chronological, newest first)

| ID | Title | Closed | Evidence |
|---|---|---|---|
| VOID-003 | Status Emit Receipt Format | 2026-03-06 | tools/status_emit.py |
| VOID-012 | GateProof Checkliste (Governance) | 2026-03-06 | policies/gateproof_v1.yaml, tests/ethics/test_fail_safe_expired_consent.py |
| VOID-013 | Sensor-Architektur (BOM & Protokoll) | 2026-03-06 | docs/sensors/bom.md, spec/sensors.spec.json |
| VOID-023 | MICRO/MESO/MACRO Tagging konsistent ausrollen | 2026-03-06 | policies/port_codebooks.yaml |
| VOID-002 | CI Pipeline Integration | 2026-02-15 | .github/workflows/deepjump-ci.yml |
| VOID-020 | Port-Matrix Suite (K0..K4) fehlt | 2026-01-13 | tools/port_lint.py, tests/test_port_lint.py |
| VOID-021 | Port-Codebooks fehlen | 2026-01-13 | policies/port_codebooks.yaml |
| VOID-022 | Flood-Guard Threshold fehlt (MAX_CLAIMS_PER_RECEIPT) | 2026-01-13 | tools/port_lint.py |
| VOID-001 | DeepJump Protocol Implementation | 2026-01-04 | — |
