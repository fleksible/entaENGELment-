# VOID-012 — GateProof (Ethik & Governance)

**Status:** OPEN
**Priority:** critical

## Symptom
Es existieren Guard- und Lint-Mechanismen, aber keine einheitliche, auditierbare Checkliste, die bei jedem "latent → manifest" Übergang durchlaufen wird.

## Bridge
Eine "GateProof"-Checkliste als Policy (und optional als Test-Suite), z.B.:
- Consent: gültig, scope korrekt
- KillSwitch: dominiert
- Claim-Lint: Facts haben Sources, Inference markiert
- Receipt: TransformID, ReasonCode, InputRefs vorhanden

## Closing Path
- `policies/gateproof_v1.yaml`
- `tests/ethics/` ergänzt (negative Tests)
