# `src/` — Python Core (ANNEX)

> [FAKT] Sovereign Python core. Per `EPISTEMIC_HYGIENE.md` §5 the JS workspace
> does not gate or rewrite this code. Changes follow Plan-First (CLAUDE.md).

This directory holds the computational kernel of the entaENGELment framework.
It is **ANNEX** (changeable after plan), not GOLD. Receipts and policies it reads
remain GOLD/IMMUTABLE.

## Layout

The columns keep apart what a module verifiably computes and what that result
may claim. "Implemented" means code and tests exist; it says nothing about
empirical validity (`EPISTEMIC_HYGIENE.md`: a hypothesis must not pass as fact).

| Path | What the code verifiably does | State | Claim on meaning |
|------|-------------------------------|-------|------------------|
| `core/eci.py` | Ethical Consent Index: weighted mean of likert/behavior/physio proxies, clamped to [0, 1]; percentile bootstrap helper | implemented, tested | [HYPOTHESE] not validated as a consent measure. `permutation_test` is statistically empty (finding B3; disabled in PR #438) |
| `core/ledger.py` | Append-only JSONL event ledger with SHA-256 hash chain | implemented, tested | [FAKT] tamper-evident within documented assumptions; no authenticity |
| `core/metrics.py` | PLV, histogram MI, Higuchi FD, PF; `eci()` is only a clamped-mean proxy | implemented, tested | [MODELL] SIMULATION_PROXY (VOID-011); known MI bias |
| `core/stability_guard.py` | Gate decision from the MOD_16 classification | implemented, tested | [MODELL] geometric classification only; never consent (see findings B2/B9) |
| `cglg/gate_logic.py` | `phi >= threshold` | stub, marked [HYP] in the module | none |
| `cglg/mutual_perception.py` | `(a + b) / 2` | one-liner, no docstring, untested | none |
| `stability/hessian_void.py` | Finite-difference Hessian and eigenvalue classification | implemented, tested | [MODELL] |
| `stability/spectral_void.py` | 7-class taxonomy from eigenvalues (MOD_18) | implemented, tested | [MODELL] |
| `stability/stability_guard.py` | Taxonomy → ALLOW/BLOCK mapping (MOD_14) | implemented, tested | [MODELL] |
| `tools/throat_vector.py` | `sqrt(x² + y²) / (z + 1e-6)` | one-liner, one test | none; no topological statement is backed |
| `tools/toy_resonance_dataset.py` | Synthetic resonance dataset | implemented, tested | [MODELL] SIMULATION_PROXY, not empirical evidence |
| `tools/cauchy_detector.py` | `max(seq) - min(seq)` (range) | one-liner, untested | none; it performs no Cauchy or outlier detection |
| `meta_backprop.py` | Writes a review note into `policy["notes"]` | stub, marked [TODO] in the module | none; no optimisation |

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
