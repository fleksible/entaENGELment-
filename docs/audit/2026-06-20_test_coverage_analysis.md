# Report: Test-Coverage-Analyse

**Datum:** 2026-06-20
**Fokus:** Test-Coverage-Analyse

## Ziel

Analyse der aktuellen Testabdeckung (Python + JS/TS) und Identifikation
konkreter Bereiche, in denen die Testabdeckung verbessert werden sollte.

## Methode

- `python3 -m pytest --cov=src --cov=tools --cov-report=term-missing`
  (numpy/scipy/pyyaml/jsonschema/pytest-cov lokal nachinstalliert, da im
  Basisimage nicht vorhanden; `tests/cpt/test_cpt_harness.py` bleibt wegen
  fehlendem `scipy` ausgeschlossen)
- Statische Durchsicht von `src/`, `tools/`, `Fractalsense/`, `ui-app/`,
  `bio_spiral_viewer/`, `Plugins/` gegen vorhandene Tests in `tests/`,
  `Fractalsense/tests/`, `__tests__/`
- `jest --coverage` (scheitert mangels installierter `node_modules` /
  `jest-environment-jsdom` — siehe „Nicht getan")

## Ergebnis: Python (`src/` + `tools/`)

185 Tests grün. Gesamt-Statement-Coverage: **62 %** (780/2050 Zeilen ohne Coverage).

### 0 % Coverage (kein einziger Test)

| Modul | Stmts | Anmerkung |
|---|---|---|
| `tools/intake_add.py` | 96 | Intake-Pipeline, ungetestet |
| `tools/intake_shadow_copy.py` | 78 | Shadow-Copy-Hook-Logik, ungetestet |
| `tools/verify_cards.py` | 89 | Card-Verifikation, ungetestet |
| `tools/voidmap_ui_drift_check.py` | 54 | VOIDMAP/UI-Drift-Check, ungetestet |
| `src/cglg/gate_logic.py` | 2 | Trivial, aber 0 % |
| `src/cglg/mutual_perception.py` | 2 | Trivial, aber 0 % |
| `src/meta_backprop.py` | 3 | Trivial, aber 0 % |
| `src/tools/cauchy_detector.py` | 2 | Trivial, aber 0 % |

Die vier kleinen `src/`-Stubs sind reine Ein-Zeiler-Funktionen — sehr
günstige "Quick Wins", da ein einziger Testfall pro Modul die Coverage
sofort auf 100 % hebt.

Die vier `tools/*`-Module mit 0 % sind dagegen substanziell (jeweils
50–100 Anweisungen) und bislang komplett ungetestet — das ist das größte
Einzelrisiko, da Bugs hier erst zur Laufzeit (z.B. im Shadow-Copy-Hook oder
bei der Card-Verifikation) auffallen würden.

### Niedrige Coverage (<60 %)

| Modul | Coverage | Fehlende Bereiche |
|---|---|---|
| `tools/status_emit.py` | 28 % | `build_status_payload`, `build_receipt`, `emit_status`, `emit_receipt`, `main` — die HMAC-Signierlogik selbst (`sign_payload`, `canonical_json`) ist getestet, aber die CLI-Pfade drumherum nicht |
| `tools/metatron_check.py` | 49 % | `main()` (CLI-Entry) ungetestet |
| `tools/status_verify.py` | 49 % | `main()` (CLI-Entry) ungetestet |
| `tools/receipt_lint.py` | 54 % | `lint_file` Fehlerzweige, `main()` |
| `tools/port_lint.py` | 56 % | `validate_marker_sequence`, `validate_receipt_flood`, `main()` |
| `tools/snapshot_guard.py` | 59 % | `main()` CLI-Pfad |

### Mittlere Coverage (60–80 %, ausbaufähig)

`src/core/ledger.py` (69 %), `tools/mzm/gate_toggle.py` (70 %),
`src/core/eci.py` (71 %), `tools/pipeline_essentials.py` (75 %),
`tools/verify_pointers.py` (76 %), `tools/frame_lint.py` (77 %).

Gemeinsames Muster: Die **Kernlogik** ist meist getestet, die
**CLI-`main()`-Funktionen und Fehlerpfade** (ungültige Eingaben, fehlende
Dateien, Exit-Codes) sind es überwiegend nicht.

### Gut abgedeckt (≥90 %)

`src/core/stability_guard.py`, `src/stability/spectral_void.py`,
`src/stability/stability_guard.py`, `src/stability/hessian_void.py`,
`src/tools/throat_vector.py`, `src/core/metrics.py`,
`tools/voids_backlog_gen.py`, `tools/workflow_posture_check.py`,
`src/tools/toy_resonance_dataset.py`.

## Ergebnis: JavaScript/TypeScript

- `__tests__/unit/fractal-math.test.js` ist der einzige JS-Test im Repo
  (Jest-Setup über `jest.config.js`, Coverage-Schwelle 50/60/60/60 %
  konfiguriert, aber nur gegen `Fractalsense/**/*.js` gemessen).
- **`ui-app/` (Next.js-App) hat keine einzige Testdatei** — weder
  Unit- noch Component-Tests für `components/fractalsense/`,
  `components/guards/`, `components/metatron/`,
  `components/nichtraum/`, `components/voidmap/`, `lib/voidmap-parser.ts`,
  `lib/colormaps.ts`, `lib/guard-definitions.ts`. Das ist die größte
  Lücke im gesamten Repo, da hier nutzersichtbare UI-Logik (Parser,
  Guard-Status-Darstellung) ungetestet bleibt.
- `Fractalsense/*.js` (App-Logik, `fractal-visualizer.js`,
  `resonance-enhancer.js`, `sensor-simulator.js`,
  `presentation-mode.js`) hat **keine** `.test.js`-Pendants — nur die
  Python-Seite von Fractalsense (`color_generator`, `sound_generator`,
  `modular_app_structure`) ist getestet.

## Weitere ungetestete Bereiche (kein Coverage-Tooling vorhanden)

- `bio_spiral_viewer/` (CLI, Loader, Metrics, Viewer) — kein `tests/`-Ordner.
- `adapters/`, `aggregates/`, `overlay/`, `lyra/`, `dashboard/` — überwiegend
  Daten/Config, aber `adapters/msi_adapter_v1.yaml` hat z.B. keinen
  Schema-Test.
- `scripts/triad_compare.py` — keine Tests.
- `Plugins/SynthosiaCore/` (Unreal-Engine-C++-Plugin) — kein Testharness
  im Repo erkennbar (vermutlich extern/UE-seitig getestet — außerhalb der
  Reichweite dieser Analyse).

## Priorisierte Empfehlungen

1. **`ui-app/` Testbasis aufbauen** (höchster Impact): Vitest/Jest +
   React Testing Library für `lib/voidmap-parser.ts` (reine Funktion,
   leicht testbar) und die Guard-/Voidmap-Komponenten.
2. **`tools/intake_add.py`, `tools/intake_shadow_copy.py`,
   `tools/verify_cards.py`, `tools/voidmap_ui_drift_check.py`** —
   0 %-Module mit Substanz; nach dem bestehenden Muster aus
   `tests/test_tools_coverage.py` (Import + direkter Funktionsaufruf statt
   Subprocess) ergänzen.
3. **CLI-`main()`-Pfade** der bereits teilweise getesteten `tools/*`
   nachziehen (Exit-Codes, Argparse-Fehlerfälle) — vor allem
   `status_emit.py`, da hier sicherheitsrelevante Signier-/Empfangslogik
   liegt und nur 28 % abgedeckt sind.
4. **Vier triviale `src/`-Stubs** (`gate_logic.py`,
   `mutual_perception.py`, `meta_backprop.py`, `cauchy_detector.py`) —
   ein Testfall pro Funktion, sehr geringer Aufwand.
5. **Fractalsense-JS** (`fractal-visualizer.js`, `resonance-enhancer.js`,
   `sensor-simulator.js`) — bislang nur Python-Seite getestet, die
   eigentliche Visualisierungslogik in JS nicht.
6. **`bio_spiral_viewer/`** — eigenes `tests/`-Verzeichnis fehlt komplett;
   sollte vor weiterem Ausbau des Moduls nachgezogen werden.

## Nicht getan

- Keine Tests geschrieben oder Code geändert (reine Analyse, Pattern B /
  Witness Mode).
- JS-Coverage-Report nicht erzeugt (fehlende `node_modules` in dieser
  Umgebung; `npx jest --coverage` schlägt mangels installiertem
  `jest-environment-jsdom` fehl). Empfehlung: `pnpm install` lokal/CI
  ausführen und Report erneut ziehen.
- `tests/cpt/test_cpt_harness.py` nicht in die Coverage-Zahl eingeflossen
  (fehlendes `scipy` in dieser Umgebung).
- `Plugins/SynthosiaCore/` (C++/UE) nicht bewertet — außerhalb des
  Python/JS-Tooling-Radius dieser Analyse.

## Risiken

- Sicherheitsrelevante Signierlogik (`tools/status_emit.py`,
  `tools/status_verify.py`) ist nur zu 28–49 % abgedeckt — Regressionen
  in Fehlerpfaden würden nicht auffallen.
- `ui-app/` ohne jegliche Tests bedeutet: Refactorings am
  Voidmap-Parser oder den Guard-Komponenten haben keinen
  Regressionsschutz.

## Offene Punkte

- [ ] ☐ Entscheidung: JS-Coverage-Threshold in `jest.config.js` auf
      `ui-app/` ausweiten, sobald dort Tests existieren?
- [ ] ☐ `pnpm install` in CI/Sandbox nachziehen, um echten JS-Coverage-Report
      zu erhalten.
- [ ] ☐ Priorisierung der 6 Empfehlungen mit Team abstimmen.

## Artefakte

- `docs/audit/2026-06-20_test_coverage_analysis.md` (dieser Report)
