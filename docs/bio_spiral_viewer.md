# Bio Spiral Viewer

Konsolenanwendung zur Exploration der Bio-Spiral- und Lyra-Strukturen im entaENGELment-Ökosystem.

---

## Überblick

Der Bio Spiral Viewer liest Manifest- und Zustandsdateien, berechnet daraus die Resonanzmetrik und gibt Gate/ETHICS/KONFAB-Überlagerungen strukturiert aus.

**Resonanzmetrik:**
```
R(t) = MI_TwinPass × PLV × (1 − Leakage)
```

| Komponente | Bedeutung |
|------------|-----------|
| `MI_TwinPass` | Mutual Information (Twin-Pass) |
| `PLV` | Phase-Locking Value |
| `Leakage` | Informationsverlust |

---

## Installation

```bash
# Repository klonen
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-

# Virtual Environment
python -m venv .venv
source .venv/bin/activate

# Installation
pip install -e .
```

---

## Quickstart

```bash
python -m bio_spiral_viewer
```

### Optionale Parameter

```bash
python -m bio_spiral_viewer \
  --state data/state/bio_spiral_state.json \
  --manifest data/manifest/bio_spiral_manifest.json
```

| Parameter | Beschreibung | Default |
|-----------|--------------|---------|
| `--state` | Pfad zur Zustandsdatei | `data/state/bio_spiral_state.json` |
| `--manifest` | Pfad zum Manifest | `data/manifest/bio_spiral_manifest.json` |

---

## Modul-Struktur

```
bio_spiral_viewer/
├── __init__.py      # Package-Exports
├── __main__.py      # CLI-Einstiegspunkt
├── cli.py           # Argument-Parsing & Hauptlogik
├── data_models.py   # Pydantic/Dataclass-Modelle
├── loader.py        # JSON-Loader für State/Manifest
├── metrics.py       # Resonanzmetrik-Berechnung
└── viewer.py        # Konsolen-Output-Formatierung
```

---

## Daten-Layout

### Zustandsdatei (`bio_spiral_state.json`)

```json
{
  "timestamp": "2025-10-22T12:00:00Z",
  "mi_twin_pass": 0.85,
  "plv": 0.92,
  "leakage": 0.05,
  "gate_status": "OPEN",
  "ethics_flag": "GREEN"
}
```

### Manifest (`bio_spiral_manifest.json`)

```json
{
  "version": "1.0",
  "seeds": [...],
  "checkpoints": [...],
  "konfab_overlays": [...]
}
```

---

## Integration mit Framework

Der Bio Spiral Viewer respektiert die Gate/ETHICS-Logik des Frameworks:

- **Gate OPEN:** Volle Anzeige aller Metriken
- **Gate CLOSED:** Reduzierte Ausgabe, Warnung
- **ETHICS RED:** Blockiert Ausgabe, zeigt Reason-Code

---

## Weiterführend

- [`docs/masterindex.md`](./masterindex.md) — Gesamtübersicht
- [`src/core/metrics.py`](../src/core/metrics.py) — Kernmetrik-Implementierung
- [`docs/voids/VOID-011_resonance_metrics.md`](./voids/VOID-011_resonance_metrics.md) — Metriken-Spezifikation
