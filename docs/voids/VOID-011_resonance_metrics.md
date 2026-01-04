# VOID-011 — Metriken der Resonanz (MI, PLV, FD)

**Status:** OPEN
**Priority:** high

## Symptom
MI/FD sind aktuell Minimal-Stubs in `src/core/metrics.py`. Es fehlt eine testbare, robuste Implementierung + eine Toy-Simulation, die zeigt, dass die Metriken auf synthetischen Daten sinnvoll reagieren.

## Bridge (Option B)
- `src/tools/toy_resonance_dataset.py` erzeugt synthetische Signale
- `src/core/metrics.py` wird in v1.1 schrittweise realisiert (MI, FD)
- Tests: deterministische Seeds, monotone Checks (z.B. mehr Kopplung → höherer PLV)

## Closing Path
- MI: binning-basierte Mutual Information (ohne SciPy-Abhängigkeit)
- FD: einfache Box-Counting Approximation
- `tests/unit/` erweitert
