# VOID-011 — Metriken der Resonanz (MI, PLV, FD)

**Status:** IN_PROGRESS
**Priority:** high
**Target:** 2026-07-15

## Symptom

MI/FD are no longer mere minimal stubs: the current boundary has moved from "implement the metrics" to "make the simulation evidence explicit and claim-tagged." The verifier-relevant gap is now the absence of a deterministic metrics export/receipt that marks toy data as `SIMULATION_PROXY`.

## Bridge (Option B)

- `src/tools/toy_resonance_dataset.py` generates deterministic synthetic resonance signals.
- `src/core/metrics.py` supplies the Core-5 metric calls used by the toy bridge.
- `tests/unit/test_toy_resonance_dataset.py` checks deterministic shape/range behavior and the PLV monotonicity proxy.

## Closing Path

- Generate a stable toy metrics export under `data/metrics/` or `data/receipts/`.
- Mark the export with `SIMULATION_PROXY` so the empirical boundary is not confused with measured data.
- Keep tests deterministic by seed and avoid adding SciPy-only assumptions unless the dependency boundary is made explicit.
