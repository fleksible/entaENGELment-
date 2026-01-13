# Port Matrix Update — Audit (2026-01-13)

**Scope:** Port-Matrix Hardening (K0..K4)  
**Status:** PASS (docs/tools/tests added)  
**Note:** This audit is additive; no runtime behavior changed.

## What changed
- Added Port-Marker linter: `tools/port_lint.py`
- Added codebooks: `policies/port_codebooks.yaml`
- Added tests: `tests/test_port_lint.py`
- Added Makefile target: `make port-lint` and included in `make verify`
- Added VOIDMAP entries: VOID-020..VOID-023 (status aligned to evidence)

## Markers (semantics)
- **K0::NEBEL** — Nebelzone / unklare Stelle (Kenogramm)
- **K1::FADEN** — Consent/Permission (explicit, no inference)
- **K2::PORT?** — Kontext-Bridge (1-edge, reason-codes)
- **K3::LEAK** — Leakage-Risiko / tighten guards
- **K4::PASS** — Audit-PASS (test path / receipt ref)

## Test evidence
- `pytest -q` includes `tests/test_port_lint.py`
- Linter can be run via `make port-lint`

## Risks / follow-ups
- This is a docs+tooling hardening step; it does not implement runtime consent detection.
