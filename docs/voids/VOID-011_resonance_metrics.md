# VOID-011 — Metriken der Resonanz (MI, PLV, FD)

**Status:** CLOSED (2026-10-18)
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

## Closure (2026-10-18)

- Export: `data/metrics/void011_resonance_metrics.csv` + `.meta.json` (ECI, PLV, MI, FD, PF; Seeds 7/42 × Kopplung 0.1/0.35/0.8, n=256).
- Jede Zeile trägt `SIMULATION_PROXY`; das Meta enthält `claim_boundary`, `csv_sha256` und keinen Zeitstempel.
- Reproduzierbar: `python tools/void011_metrics_export.py --check`; Test: `tests/unit/test_void011_metrics_export.py`.
- Plausibilitätsgrenze: PLV steigt je Seed mit der Kopplung (`checks.plv_monotone_in_coupling`).
- Beim Abschluss behoben: `fd()` normierte die Higuchi-Kurvenlänge mit 1/k statt 1/k². Die Steigung war um −1 verschoben und klemmte fast immer auf 1.0. Referenztests in `tests/unit/test_core5_metrics.py`: weißes Rauschen ≈ 2.0, Random Walk ≈ 1.5.
- Nachtrag (Gesamtcheck 2026-10-18): Der Histogramm-Schätzer `mi()` hat einen Positiv-Bias von ~0,5 nats bei unabhängigen Signalen (n=256, √n Bins je Achse). Der Export führt deshalb `MI_BASELINE` (Mittel über 8 feste Permutationen von b) und `MI_EXCESS = MI − MI_BASELINE`; `checks.mi_excess_monotone_in_coupling` prüft die Kopplungsordnung. `mi()` selbst bleibt unverändert. Das Meta bindet die erzeugenden Quellen per `source_sha256`.
- Grenze: Die Werte beschreiben Toy-Signale. Sie sind kein Nachweis über reale Resonanz und begründen keinen `[FACT]`-Status.
