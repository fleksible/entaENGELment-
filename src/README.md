# `src/` — Python Core (ANNEX)

> [FAKT] Sovereign Python core. Per `EPISTEMIC_HYGIENE.md` §5 the JS workspace
> does not gate or rewrite this code. Changes follow Plan-First (CLAUDE.md).

This directory holds the computational kernel of the entaENGELment framework.
It is **ANNEX** (changeable after plan), not GOLD. Receipts and policies it reads
remain GOLD/IMMUTABLE.

## Layout

| Path | Purpose | Claim |
|------|---------|-------|
| `core/eci.py` | Elliptic Cumulative Integral coherence metric | [FAKT] |
| `core/ledger.py` | Append-only JSONL event ledger with SHA-256 hash chain | [FAKT] |
| `core/metrics.py` | Resonance metrics (MI, PLV, FD/Higuchi, …) — see VOID-011 | [FAKT] |
| `core/stability_guard.py` | Stability gate (core variant) | [FAKT] |
| `cglg/gate_logic.py` | φ ≥ threshold gate predicate | [FAKT] |
| `cglg/mutual_perception.py` | Mutual-perception averaging helper | [FAKT] |
| `stability/hessian_void.py` | Hessian spectral analysis for void detection | [FAKT] |
| `stability/spectral_void.py` | Spectral void taxonomy classifier (MOD_18) | [FAKT] |
| `stability/stability_guard.py` | Spectral taxonomy → gate mapper (MOD_14) | [FAKT] |
| `tools/throat_vector.py` | Throat-vector topology computation | [FAKT] |
| `tools/toy_resonance_dataset.py` | Synthetic resonance dataset (VOID-011 evidence) | [FAKT] |
| `tools/cauchy_detector.py` | Cauchy residual outlier detection | [HYPOTHESE] reference status under review (audit R4) |
| `meta_backprop.py` | Backpropagation helper | [HYPOTHESE] reference status under review (audit R4) |

## Boundary notes

- [MODELL] Resonance metrics carry a `SIMULATION_PROXY` boundary: they operate on
  synthetic / toy data, not validated empirical signals (see `VOIDMAP.yml`
  VOID-010/011). Do not present metric output as empirical evidence.
- [FAKT] Two modules (`tools/cauchy_detector.py`, `meta_backprop.py`) appear
  unreferenced as of 2026-06-16. They are **not** deleted (G3 deletion ban);
  archival, if any, goes through `NICHTRAUM/archive/` after consent.

## Running

See the repository `Makefile`: `make test`, `make lint`, `make type-check`,
`make verify`.
