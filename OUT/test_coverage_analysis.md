# Report: Test-Coverage-Analyse & Verbesserungsvorschläge

**Datum:** 2026-06-20
**Fokus:** Test-Coverage analysieren

## Ziel
Den Ist-Zustand der Testabdeckung über alle Sprachen (Python + JS/TS) erfassen
und priorisierte Bereiche vorschlagen, in denen die Tests verbessert werden sollten.

## Methodik
- `pytest --cov` mit der in `pyproject.toml` konfigurierten Coverage-Quelle (`src`, `tools`) ausgeführt.
- Zusätzliche `--cov`-Läufe für die **nicht** in der Config erfassten Python-Pakete
  (`audit`, `bio_spiral_viewer`, `ledger`, `mapping`, `scripts`).
- CI-Workflows (`ci.yml`, `test.yml`) und Test-Runner-Konfiguration (`jest.config.js`,
  `package.json`) gelesen, um die tatsächlich in CI ausgeführten Tests zu bestimmen.
- JS/TS-Testbestand inventarisiert (`__tests__/`, `Fractalsense/`, `ui-app/`).

## Ist-Zustand (Zahlen)

### Python (`src/` + `tools/`, in Coverage-Config)
- **186 Tests, alle grün.** Gesamt-Coverage **62 %** (780 von 2050 Statements ungetestet).

| Modul | Cover | Bemerkung |
|-------|-------|-----------|
| `tools/intake_add.py` | **0 %** | komplett ungetestet |
| `tools/intake_shadow_copy.py` | **0 %** | komplett ungetestet (Hook-Pfad!) |
| `tools/verify_cards.py` | **0 %** | komplett ungetestet |
| `tools/voidmap_ui_drift_check.py` | **0 %** | komplett ungetestet |
| `src/meta_backprop.py` | **0 %** | komplett ungetestet |
| `src/cglg/gate_logic.py` | **0 %** | komplett ungetestet |
| `src/cglg/mutual_perception.py` | **0 %** | komplett ungetestet |
| `src/tools/cauchy_detector.py` | **0 %** | komplett ungetestet |
| `tools/status_emit.py` | 28 % | Statuserzeugung kaum abgedeckt |
| `tools/metatron_check.py` | 49 % | Guard-Check (G4) — kritisch, halb getestet |
| `tools/status_verify.py` | 49 % | |
| `tools/receipt_lint.py` | 54 % | IMMUTABLE-Audit-Trail-Validierung |
| `tools/port_lint.py` | 56 % | |
| `tools/snapshot_guard.py` | 59 % | |
| `src/core/ledger.py` | 69 % | Kern-Datenstruktur |
| `tools/mzm/gate_toggle.py` | 70 % | Gate-Policy (in CI separat smoke-getestet) |

### Python (NICHT in Coverage-Config — blinder Fleck)
Diese Pakete liegen außerhalb von `[tool.coverage.run] source` und tauchen in keinem
Coverage-Report auf, obwohl sie produktiver Code sind:

| Modul | Cover | Statements |
|-------|-------|-----------|
| `audit/check_annex.py` | **0 %** | 36 |
| `audit/consistency_check.py` | **0 %** | 32 |
| `bio_spiral_viewer/cli.py` | **0 %** | 59 |
| `bio_spiral_viewer/data_models.py` | **0 %** | 60 |
| `bio_spiral_viewer/loader.py` | **0 %** | 48 |
| `bio_spiral_viewer/metrics.py` | **0 %** | 13 |
| `bio_spiral_viewer/viewer.py` | **0 %** | 11 |
| `scripts/triad_compare.py` | **0 %** | 54 |
| `mapping/tensor_validator.py` | 74 % | (hat Tests, aber Paket nicht in Config) |
| `ledger/replay_determinism.py` | 88 % | (hat Tests, aber Paket nicht in Config) |

### JavaScript / TypeScript
- **Nur eine einzige JS-Testdatei:** `__tests__/unit/fractal-math.test.js`.
- **Coverage-Illusion:** Diese Datei importiert den echten Quellcode *nicht*. Sie
  re-implementiert `calculateMandelbrot` inline und testet die Kopie. `jest.config.js`
  sammelt aber Coverage über `Fractalsense/**/*.js` → die ausgelieferten Module
  (`fractal-visualizer.js`, `app.js`, `presentation-mode.js`, `resonance-enhancer.js`,
  `sensor-simulator.js`) sind faktisch bei ~0 % realer Abdeckung. Die
  Coverage-Thresholds (branches 50 / functions 60 / lines 60) greifen daher ins Leere.
- **`ui-app/` (Next.js): keine Tests.** ~15 Komponenten und Logik-Module
  (`lib/voidmap-parser.ts`, `lib/guard-definitions.ts`, `lib/colormaps.ts`) ohne jeden Test;
  CI macht nur `build`, keinen Testlauf.
- **`packages/types/src/index.ts`:** keine Tests (ggf. nur Typen — niedrige Prio).

### CI-Lücken (strukturell)
1. **`test.yml` (PR-blockierend) führt für Python nur `cd Fractalsense && pytest` aus.**
   Die gesamte Root-`tests/`-Suite (die 186 Tests inkl. Ethics/Stability/Guards) läuft
   dort **nicht**. Der echte Coverage-Gate liegt in `ci.yml`.
2. **`ci.yml` `build`-Job läuft mit `if: github.event_name != 'pull_request'`** — also nur
   bei Push auf `main`/`claude/**`, **nicht auf PRs**. Auf PRs ist `ci.yml` rein advisory.
   Ergebnis: Der `coverage report --fail-under=50`-Gate schützt PRs **nicht**.
3. Coverage-Baseline ist mit **50 %** niedrig (Ist 62 %), bietet also keinen
   Regressionsschutz nach oben.

## Vorgeschlagene Verbesserungsbereiche (priorisiert)

### P0 — Guard- & Sicherheitslogik (passt zum Projekt-Kern)
Die Guards (G1–G6) sind das Herz des Projekts, aber genau ihre Tooling-Implementierung ist
schwach abgedeckt:
- `tools/metatron_check.py` (49 %) — G4-Guard. Switch-Detection-Pfade testen.
- `tools/receipt_lint.py` (54 %) — Validierung des IMMUTABLE Audit-Trails (G1).
- `audit/check_annex.py` (0 %) — prüft genau das Annex-Prinzip (G1) und ist ungetestet.
- `src/core/ledger.py` (69 %) — Fehler-/Edge-Pfade (Zeilen 111-133, 270-302).

### P1 — Komplett ungetestete produktive Module
- `tools/intake_shadow_copy.py` (0 %) — läuft als PostToolUse-Hook, also aktiv im Betrieb.
- `tools/intake_add.py` (0 %), `tools/verify_cards.py` (0 %),
  `tools/voidmap_ui_drift_check.py` (0 %), `tools/status_emit.py` (28 %).
- `bio_spiral_viewer/` (gesamtes Paket 0 %) — `data_models`, `loader`, `metrics` sind gut
  unit-testbar (reine Datenlogik).

### P2 — JS/TS-Abdeckung real machen
- `fractal-math.test.js` so umbauen, dass es die **echte** `fractal-visualizer.js`
  importiert (z. B. Math-Funktionen aus der Klasse extrahieren/exportieren), statt eine
  Kopie zu testen — sonst ist die JS-Coverage-Zahl wertlos.
- Für `ui-app/lib/*.ts` (Parser, Guard-Definitionen) Unit-Tests ergänzen (Vitest/Jest);
  diese reinen Funktionen sind risikoarm und schnell abzudecken.

### P3 — CI-Härtung (verhindert künftige Regression)
- `ci.yml`-`build`-Job (oder `test.yml`) so anpassen, dass die **Root-`tests/`-Suite mit
  Coverage-Gate auch auf Pull Requests** läuft — aktuell schützt der Gate nur Pushes.
- `--fail-under` schrittweise von 50 → ~62 % anheben (Ist-Stand einfrieren), danach
  pro PR leicht erhöhen.
- `ui-app` einen echten `test`-Schritt in CI geben (nicht nur `build`).

## Nicht getan (bewusst ausgelassen)
- **Keine** Tests geschrieben oder Code geändert (reine Analyse, Read-Only / Witness-Mode).
- **Keine** GOLD-Pfade (`index/`, `policies/`, `VOIDMAP.yml`) angefasst.
- Keine Anpassung von `pyproject.toml`/CI — nur als Empfehlung dokumentiert.

## Risiken
- Die 62 %-Zahl überschätzt die reale Abdeckung, da `audit/`, `bio_spiral_viewer/`,
  `scripts/` gar nicht in der Coverage-Quelle stehen → echtes Bild liegt darunter.
- JS-Coverage-Threshold suggeriert Sicherheit, die nicht existiert (Test gegen Code-Kopie).
- PRs sind aktuell nicht durch den Python-Coverage-Gate geschützt.

## Offene Punkte
- [ ] ☐ Soll ich als Folge-Task konkrete Tests für die P0-Guard-Module schreiben?
- [ ] ☐ Soll `bio_spiral_viewer`/`audit` in `[tool.coverage.run] source` aufgenommen werden?
- [ ] ☐ Soll der CI-Coverage-Gate auf PRs ausgeweitet werden (P3)?

## Artefakte
- `OUT/test_coverage_analysis.md` (dieser Report)
