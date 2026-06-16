# `tools/` — Guards, Linters & Receipt Pipeline (ANNEX)

> [FACT] These tools enforce the project's governance membrane (DeepJump
> Protocol v1.2). They read GOLD/IMMUTABLE artefacts and never rewrite them.

## Layout

| Path | Purpose | Wired into |
|------|---------|------------|
| `verify_pointers.py` | Dead-pointer scan across `index/`/modules (`--strict`) | core membrane + DeepJump CI (blocking) |
| `claim_lint.py` | Untagged-claim scan over `index,spec,receipts,tools` | core membrane + DeepJump CI (blocking) |
| `port_lint.py` | Port-matrix (K0..K4) + flood guard (MAX_CLAIMS_PER_RECEIPT) | core membrane + DeepJump CI (blocking) |
| `frame_lint.py` | Frame Operator lint v0.1.1 (opt-in `FRAME_LINT_PATHS`) | `make frame-lint` (not in core membrane) |
| `receipt_lint.py` | Receipt-format lint | `make benchmark-replay` |
| `status_emit.py` | Emit HMAC-signed status receipt | `make status` |
| `status_verify.py` | Status-receipt re-check | `make status-verify` <!-- noqa: claim-lint --> |
| `snapshot_guard.py` | Strict snapshot manifest of seeds/audit inputs | `make snapshot` |
| `voids_backlog_gen.py` | Regenerate / drift-scan `docs/voids_backlog.md` | `make voids-backlog[-check]` |
| `workflow_posture_check.py` | Workflow permissions + concurrency posture | `make workflow-posture-check` |
| `pipeline_essentials.py` | Pipeline-essentials report | `make pipeline-essentials` |
| `metatron_check.py` | FOKUS-marker guard (G4) for PR bodies | `metatron-guard.yml` |
| `verify_cards.py` | Bridge/card data lint | (manual) |
| `mzm/gate_toggle.py` | Policy-based consent/φ gate toggle CLI | `make gate-test`, `ci.yml` gate-policy job |

## Claim discipline

[FACT] `claim_lint.py` checks that non-trivial claims in `index,spec,receipts,tools`
carry an epistemic tag. The tool's enforced tag set is `[FACT]`, `[HYP]`, `[MET]`,
`[TODO]`, `[RISK]`. The broader project taxonomy is bilingual — `[FAKT]`/`[FACT]`,
`[INFERENZ]`/`[INFERENCE]`, `[MODELL]`/`[MODEL]`, `[HYPOTHESE]`/`[HYPOTHESIS]`,
`[METAPHER]`/`[METAPHOR]`, plus `[SPEC]`, `[POESIE]`, `[EXECUTED]`. Do not
"normalize" one language variant into the other; both are canonical.

## Test coverage note

[FACT] As of 2026-06-16 these tools have no dedicated unit test:
`metatron_check.py`, `mzm/gate_toggle.py`, `receipt_lint.py`, `status_verify.py`,
`verify_cards.py`. Adding guard-the-guard coverage is a tracked roadmap item
(`docs/roadmap/revolutionary_forward_architecture_2026-06-16.md`).
