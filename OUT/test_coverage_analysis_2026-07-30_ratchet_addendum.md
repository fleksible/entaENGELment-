# Addendum: JS-Coverage-Ratchet

**Datum:** 2026-07-30  
**Bezug:** `OUT/test_coverage_analysis_2026-07-30.md`, PR #344

## Status

Dieses Addendum ersetzt ausschließlich die Aussage im Hauptreport, der
`coverageThreshold` müsse als Prozentwert auf `0` stehen. Die übrigen Befunde und
Prioritäten des Reports bleiben unverändert.

## Änderung nach Review

Der Prozentwert `0` bildet den gemessenen Ist-Stand zwar ehrlich ab, ist aber kein
wirksamer Ratchet: Er verhindert weder zusätzliche ungetestete Logik noch einen
erneuten Instrumentierungsverlust.

Jest interpretiert negative `coverageThreshold`-Werte als die maximal erlaubte Zahl
unabgedeckter Einheiten. PR #344 friert deshalb die im CI-Artefakt gemessene absolute
Baseline ein:

| Metrik | erfasst | abgedeckt | maximal unabgedeckt |
|---|---:|---:|---:|
| Statements | 181 | 0 | 181 |
| Branches | 28 | 0 | 28 |
| Functions | 51 | 0 | 51 |
| Lines | 170 | 0 | 170 |

Konfiguration:

```js
coverageThreshold: {
  global: {
    branches: -28,
    functions: -51,
    lines: -170,
    statements: -181
  }
}
```

## Schutzwirkung

- Der aktuelle, real gemessene Nullstand bleibt grün.
- Zusätzliche ungetestete Logik erhöht die Zahl unabgedeckter Einheiten und macht CI rot.
- Werden die drei syntaktisch unvollständigen Dateien repariert und dadurch wieder
  instrumentierbar, müssen gleichzeitig Tests ergänzt oder die Baseline in einem
  expliziten Review neu beschlossen werden.
- Neue Tests verringern die unabgedeckten Zähler; die Schwellen können anschließend nur
  nach unten nachgezogen werden.

## Begrenzung

Die Baseline umfasst derzeit nur die zwei parsebaren Dateien `Fractalsense/app.js` und
`Fractalsense/sensor-simulator.js`. Die Dateien `fractal-visualizer.js`,
`presentation-mode.js` und `resonance-enhancer.js` scheitern weiterhin beim Parsen und
werden deshalb nicht in den Zählern erfasst. Dieser Defekt bleibt ein separater
Rekonstruktions- und Testauftrag.

FOKUS: JS-Coverage-Gate vom sichtbaren Nullwert zu einem fail-closed Ratchet schärfen
