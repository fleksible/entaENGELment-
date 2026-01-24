# Backprop Report — P4 Receipt Canonicalization (2026-01-24)

## Summary
This change-set removes YAML duplicate-key hazards from Ark P4 receipts and enforces canonical receipt hygiene in CI.

**Why:**
- YAML duplicate keys are silently overwritten by common parsers.
- This compromises audit trails (invisible data loss) and allows drift.
- Receipts are currently DRAFT (TBD fields), so canonicalization is safe and expected.

## Changes

### Receipt canonicalization (DRAFT hygiene)
- Removed duplicate YAML keys across Ark P4 receipts (no silent overwrites).
- Normalized `evidence_ref` to **JSON Pointer** form only:
  - ✅ `ark_cephalo_manifest_v2.json#/...`
  - ❌ Removed legacy `ark_cephalo_manifest_v2.json:dot.path` entries.
- Consolidated `ARK_P4_PHI_0001.yaml` where duplicate blocks existed:
  - `component_under_test` now appears once
  - `procedure` now appears once
  - `outputs.hashes` now appears once (superset fields)

### Tooling: receipt_lint
Added `tools/receipt_lint.py`:
- Fails on duplicate YAML keys (custom SafeLoader).
- Fails on legacy `.json:` evidence_ref style (enforces `.json#/...`).

### CI enforcement
Updated `.github/workflows/deepjump-audit.reusable.yml`:
- Added `Receipt Lint` step:
  - `python3 tools/receipt_lint.py --strict ark/p4/receipts`

## Validation
Commands executed (expected PASS):
- `python3 tools/receipt_lint.py --strict ark/p4/receipts`
- `python3 tools/verify_pointers.py --strict`

## Notes
- No "freeze"/immutability was introduced. Receipts remain DRAFT until hashes/reviewers are finalized.
- Next recommended step: implement `tools/verify_receipt_evidence_refs.py` to resolve JSON pointers against the manifest and make Receipt→Manifest linkage fully machine-verifiable.
