# Report: Fractalsense Issue #345 provenance-first reconstruction

**Datum:** 2026-09-23  
**Fokus:** Issue #345 Browsermodule  
**Authority:** DERIVED  
**Branch:** `agent/issue-345-provenance-restore-20260923`  
**Base:** `main@17fd78e2d71e4b314c54051a0922a7aa0b82c03e`

## Ziel

[FAKT] Issue #345 verlangt die Rekonstruktion der drei abgeschnittenen Browsermodule
`fractal-visualizer.js`, `presentation-mode.js` und `resonance-enhancer.js`
mit expliziter Provenienzklasse, Tests und Known-Loss-Dokumentation.

[FAKT] Dieser Pass verändert keine GOLD-Datei, kein Receipt und keine VOIDMAP-ID.

## Evidenz / Provenienz

[FAKT] `Fractalsense/fractal-visualizer.js` ist über die Git-API bis
`522a2633586f49b592d14f446096102c11dd143a` vom 2026-01-17 zurückverfolgbar.

[FAKT] `Fractalsense/presentation-mode.js` und
`Fractalsense/resonance-enhancer.js` sind über die Git-API bis
`e9b8b3986cd7612bee5c1d31a2d7ec54bd3bbae8` vom 2026-01-19 zurückverfolgbar.

[FAKT] Im initialen FractalSense-Import vom 2026-01-19 existierten vollständige
minifizierte Artefakte der drei Module.

[FAKT] Die Januar-Blobs sind byte-identisch zu den heute unter
`NICHTRAUM/archive/fractalsense/` erhaltenen Artefakten:

| Modul | Januar-Blob | aktueller Archiv-Blob | Ergebnis |
|---|---|---|---|
| `fractal-visualizer.min.js` | `f76f0903ca6672e51b770cec5d772435a5c5c334` | `f76f0903ca6672e51b770cec5d772435a5c5c334` | [FAKT] identisch |
| `presentation-mode.min.js` | `f384949d4325d672809ae4750eae164274525cd4` | `f384949d4325d672809ae4750eae164274525cd4` | [FAKT] identisch |
| `resonance-enhancer.min.js` | `1bb51e3cb4d83cf1e569bcec207c61896bd95979` | `1bb51e3cb4d83cf1e569bcec207c61896bd95979` | [FAKT] identisch |

[INFERENZ] Die vollständigen minifizierten Artefakte sind damit ein historischer
Repo-Witness für die fehlende Produktlogik; sie sind stärker als eine Rekonstruktion
aus Call-Sites allein.

[FAKT] Ein früherer Kommentar in Issue #345 ordnete alle drei Human-Readable-Dateien
einem Juli-Commit zu. Die aktuelle Git-Pfadhistorie widerspricht dieser Datierung.

[INFERENZ] Der Issue-Kommentar wird deshalb in diesem Report als überholt behandelt;
die Reparatur stützt sich auf die nachprüfbaren Januar-Historien und Blob-SHAs.

## Rekonstruktionsklassen

### `Fractalsense/fractal-visualizer.js`

**Klasse:** `RESTORED`

[FAKT] Das Archivartefakt liefert den fehlenden Abschluss von `getParams()`, die
`reset()`-Semantik, den Klassenschluss und `window.FractalVisualizer`.

[FAKT] Die wiederhergestellte Produktsemantik wurde gegenüber dem Archivartefakt nicht
inhaltlich erweitert.

[FAKT] Known Loss: ursprüngliches Formatting und mögliche Kommentare im abgeschnittenen
Tail sind nicht rekonstruierbar.

### `Fractalsense/presentation-mode.js`

**Klasse:** `RECONSTRUCTED`

[FAKT] Das Archivartefakt liefert die vollständige Action-Routing-Semantik für
`showFractal`, `zoomIn`, `zoomOut`, `activateSensors`,
`simulateSensorMovement`, `activateSound`, `changeSoundType`,
`changeColorMode`, `activateAllModules` und `resetAll`.

[FAKT] Der historische Minified-Build behandelt unbekannte Action-Typen als stillen No-op.

[FAKT] Die reparierte Quelle ergänzt bewusst einen expliziten Fehler für unbekannte
Action-Typen, um die Abnahmeregel aus #345 fail-closed umzusetzen.

[INFERENZ] Wegen dieser absichtlichen Härtung ist die Datei nicht als reine historische
Wiederherstellung klassifiziert.

[FAKT] Known Loss: ursprüngliches Formatting und mögliche Kommentare im abgeschnittenen
Tail sind nicht rekonstruierbar.

### `Fractalsense/resonance-enhancer.js`

**Klasse:** `RECONSTRUCTED`

[FAKT] Das Archivartefakt liefert die fehlenden Implementierungen von
`animateCosmicTheme()`, `animateSoundWave()`, `onSensorDataUpdate()` und
`onFractalUpdate()`.

[FAKT] Der historische Build begrenzt Cosmic-DOM nur über den UI-üblichen
Intensity-Bereich und entfernt Star-/Nebula-Nodes beim Wechsel in einen
nicht-kosmischen Modus nicht explizit.

[FAKT] Die reparierte Quelle ergänzt eine Clamp auf 1..10 sowie
`clearCosmicTheme()`, sodass Cosmic-Nodes begrenzt und beim Moduswechsel entfernt
werden.

[INFERENZ] Wegen dieser absichtlichen Härtung ist die Datei als `RECONSTRUCTED`
klassifiziert.

[FAKT] Known Loss: ursprüngliches Formatting und mögliche Kommentare im abgeschnittenen
Tail sind nicht rekonstruierbar.

## Caller-Befund

[FAKT] `Fractalsense/app.js` instanziiert die vier globalen Klassen
`FractalVisualizer`, `SensorSimulator`, `ResonanceEnhancer` und
`PresentationMode`.

[FAKT] `Fractalsense/index.html` lud vor diesem Patch ausschließlich `app.js`.

[FAKT] Der Patch lädt nun die vier Modulquellen vor `app.js` in Abhängigkeitsreihenfolge.

[INFERENZ] Diese Änderung ist ein aktueller Caller-Fix und keine Behauptung über den
ursprünglichen historischen HTML-Build.

## Tests

[FAKT] Neu ist
`__tests__/unit/fractalsense-browser-modules.test.js`.

[FAKT] Die Suite prüft Parse/Load aller drei reparierten Quellen, Browser-Script-Reihenfolge,
`FractalVisualizer.getParams()` und `reset()`, dokumentierte Presentation-Actions,
verzögerte Actions, unbekannte Actions als Fail-Closed-Fehler, begrenztes Cosmic-DOM
mit Cleanup sowie Sound-Wave-, Sensor- und Fractal-Reaktionen.

## Coverage-Ratchet

[FAKT] Die erste Coverage-Ausführung instrumentierte die drei vorher unparsbaren Dateien
erstmals und maß:

| Datei | Statements | Branches | Functions | Lines |
|---|---:|---:|---:|---:|
| `fractal-visualizer.js` | 66.39% | 59.37% | 60.86% | 65.94% |
| `presentation-mode.js` | 57.94% | 45.26% | 54.83% | 62.08% |
| `resonance-enhancer.js` | 46.33% | 31.25% | 35.48% | 47.05% |

[FAKT] Der bestehende globale uncovered-count Ratchet blieb unverändert bei
181 Statements, 28 Branches, 51 Functions und 170 Lines.

[FAKT] Die drei wiederhergestellten Module erhielten danach eigene Mindestprozente,
abgerundet auf die gemessenen Werte. Dadurch werden sie aus der globalen
uncovered-count-Berechnung herausgenommen, ohne den bisherigen Global-Guard zu lockern.

## Verifikation

[FAKT] Erste JS-Ausführung: 4 Test-Suites / 66 Tests bestanden; Coverage scheiterte
erwartungsgemäß am alten Ratchet, weil die drei Module neu instrumentierbar waren.

[FAKT] Nach dem gemessenen Split-Ratchet bestand die zweite vollständige CI-Runde:

- `Tests`: SUCCESS
  - JavaScript Tests + Coverage: SUCCESS
  - Python Tests 3.10: SUCCESS
  - Python Tests 3.11: SUCCESS
  - Python Tests 3.12: SUCCESS
  - UI Build: SUCCESS
  - All Tests Pass: SUCCESS
- `DeepJump CI`: SUCCESS
- `CI Pipeline - entaENGELment Framework`: SUCCESS
- `Smoke Tests`: SUCCESS
- `Policy Lint`: SUCCESS
- `Metatron Guard`: SUCCESS
- `Python Quality`: SUCCESS

[FAKT] Finale JS-Messung: 4 Test-Suites / 66 Tests bestanden.

## Nicht getan

[FAKT] Kein Merge nach `main`.

[FAKT] Keine VOIDMAP-Änderung.

[FAKT] Keine GOLD-, Runtime- oder Kanon-Promotion.

[FAKT] Keine Änderung historischer Archive unter `NICHTRAUM/`.

[FAKT] Keine Behauptung, dass Formatting oder Kommentare der ursprünglichen
unminifizierten Tails historisch wiederhergestellt wurden.

## Offene Punkte

[HYPOTHESE] Zusätzliche Tests für `app.js` und `sensor-simulator.js` könnten den
unveränderten globalen Coverage-Ratchet später weiter verschärfen.

[HYPOTHESE] Ein späterer dedizierter Browser-E2E-Smoke könnte zusätzlich prüfen, dass
`index.html` in einem echten Browser ohne fehlende Globals startet.

## Artefakte

- `Fractalsense/fractal-visualizer.js`
- `Fractalsense/presentation-mode.js`
- `Fractalsense/resonance-enhancer.js`
- `Fractalsense/index.html`
- `__tests__/unit/fractalsense-browser-modules.test.js`
- `jest.config.js`
- `OUT/fractalsense_issue_345_provenance_restore_2026-09-23.md`
