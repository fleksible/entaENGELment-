# Report: Repo-Review Funktion, UI, Verbesserungen

**Datum:** 2026-10-07
**Fokus:** Funktions- und UI-Review

## Ziel
Repo auf Funktionalität prüfen und UI- sowie sonstige Verbesserungen finden. Witness-Mode: nur lesen, keine Code-Änderung.

## Aktionen
- [x] Kern-Gates auf `main` (`a7773db`):
  - `make verify` grün (665 Tests)
  - `make verify-governance` grün
  - `make type-check` grün (48 Dateien)
  - `make lint` grün
  - Fractalsense-pytest 184/184
  - Jest 66/66
  - `pnpm turbo run typecheck lint build test` grün
- [x] Coverage gemessen: 73 % über `src/` und `tools/`
- [x] UI als statischer Export gebaut. Alle 7 Routen mit Playwright auf Desktop (1280×800) und Mobile (375×812) aufgerufen; dabei geprüft:
  - Seitenfehler
  - horizontales Überlaufen
  - axe-core-Analyse
- [x] Gefundene Bugs gezielt reproduziert und die Ursache im Code eingegrenzt

## Befund: Funktion
Alle Gates und Tests sind grün [FACT]. Die Bugs unten liegen in Bereichen ohne Test, vor allem in der UI: Es gibt keinen E2E- bzw. Browser-Test.

## Befund: UI (priorisiert)

### P1: Bugs
1. **FractalSense stürzt ab** (`components/fractalsense/FractalCanvas.tsx`) [FACT]
   - Reproduktion: Mobile → „Controls“ antippen → Gerät drehen (Resize). Danach zeigt die Seite „This page couldn’t load“.
   - Ursache: Der Resize-Handler misst den versteckten Container mit Breite 0. Danach wirft `ctx.createImageData(0, h)` einen `IndexSizeError`, und die ganze Seite fällt aus.
   - Fix: Bei `width/height <= 0` nicht rendern; `ResizeObserver` statt `window.resize` verwenden.
2. **Mobile-Navigation abgeschnitten** (`components/layout/Navigation.tsx`) [FACT]
   - 7 Einträge × `min-w-[56px]` = 392 px, das ist mehr als 375 px. „Nichtraum“ ist auf jedem Handy ≤ 390 px auf allen Seiten abgeschnitten.
   - Fix: `flex-1 min-w-0` statt fester Mindestbreite, alternativ weniger Einträge.
3. **tesser3TAKT läuft auf Mobile horizontal über** (`components/tesser3takt/Tesser3TaktHudV2.tsx:579`) [FACT]
   - Die Seite ist 690 px breit bei 375 px Viewport.
   - Ursache: Grid-Items ohne `min-w-0`; der `<pre>`-JSON-Block drückt die Spalte auf.
   - Fix: `min-w-0` an die Grid-Kinder bzw. `grid-cols-1`.
4. **Metatron: React-Hydration-Fehler #418** (`lib/mock-data.ts`, `AttentionStream.tsx`, `FocusIndicator.tsx`) [FACT]
   - Mock-Zeitstempel und „Seit 1h 0m“ werden beim statischen Build gerendert und weichen beim Laden ab.
   - Fix: Zeitwerte erst nach dem Mount erzeugen.

### P2: Barrierefreiheit (axe, Desktop)
5. **Zoom gesperrt** (`app/layout.tsx`: `maximumScale: 1, userScalable: false`). Verstößt gegen WCAG 1.4.4 und betrifft alle Seiten.
6. **Kontrast:** 162 Elemente mit zu wenig Kontrast, vor allem `text-zinc-500`/`zinc-600` auf `zinc-950`. Fix: auf `zinc-400` anheben.
7. **FractalSense:**
   - `<label>` sind nicht mit Inputs verknüpft (axe: critical)
   - doppelte Landmarks
   - Tablet (768 px): Der Canvas ist nur 128 px breit, weil Sidebar und Control-Panel die Breite belegen. Bis `lg` gestapelt layouten.
8. **Kleinkram:**
   - Navigation ohne `aria-current`
   - Emoji-Icons ohne `aria-hidden`
   - scrollbare Region in tesser3TAKT nicht per Tastatur erreichbar
   - Heading-Sprung auf `/voidmap`

### P2: Ehrliche Darstellung (Claim-Hygiene)
9. Simulierte Daten sind nicht als solche erkennbar:
   - Home zeigt bei allen Guards fest ✓, ohne Hinweis „simuliert“. `/guards` weist es aus, Home nicht.
   - Metatron zeigt den Badge „Live“ bei reinen Mock-Daten. Der Mock-Text „Found 12 VOIDs, 3 CLOSED“ ist veraltet; real sind es 22 VOIDs, davon 9 geschlossen.
   - Vorschlag: einheitlicher „Demo/Simuliert“-Badge.
10. Home-„Quick Navigation“ ohne tesser3TAKT-Karte. „Critical Open: 0“ steht in Rot, obwohl 0 eine gute Nachricht ist.

## Befund: Sonstige Verbesserungen
11. **VOIDMAP-Spiegel:** `ui-app/lib/voidmap-parser.ts` wird von Hand mit `VOIDMAP.yml` synchron gehalten; die Abhängigkeit `yaml` ist installiert, wird aber nicht genutzt.
    - Option: `VOIDMAP.yml` beim statischen Build parsen. Die GOLD-Datei bleibt dabei unverändert, nur gelesen. Damit entfällt das Drift-Risiko.
12. **UI-Smoke-Test in CI fehlt.** Ein Playwright-Smoke-Test hätte Punkte 1–4 gefangen. Er prüft:
    - alle Routen laden ohne `pageerror`
    - kein horizontales Überlaufen bei 375 px
    - axe ohne Findings der Stufe serious/critical
13. **Python-Deprecation:** `ledger/replay_determinism.py:139` nutzt `datetime.utcnow()` (104 Warnungen in `tests/test_replay_hash.py`). Fix: `datetime.now(timezone.utc)`.
14. **Coverage-Lücken** (0 %):
    - `tools/intake_add.py`, `tools/intake_shadow_copy.py`, `tools/verify_cards.py`, `tools/voidmap_ui_drift_check.py`
    - `tools/status_emit.py` liegt bei 28 %.
15. **Electron:** Die Härtung ist in Ordnung (Sandbox, Kontextisolation, CSP, SRI). `Index.html` lädt three.js aber zur Laufzeit vom CDN und läuft daher nicht offline. Option: lokal vendoren.

## Nicht getan
- Keine Code-Änderungen (Witness-Mode, Plan-First). Umsetzung erst nach OK.
- Kein Review von `bio_spiral_viewer/`, `dashboard/` und `lyra/` im Browser bzw. CLI-Betrieb; dort laufen nur die Tests.
- Keine Prüfung inhaltlicher bzw. theoretischer Claims.

## Risiken
- [RISK] P1-1 und P1-2 betreffen Mobile-Nutzung direkt: Absturz und abgeschnittene Navigation.
- [RISK] Ohne UI-Smoke-Test in CI kommen solche Regressionen unbemerkt durch alle grünen Gates.

## Offene Punkte
- [ ] ☐ Entscheidung, welche Punkte umgesetzt werden. Empfehlung: P1 (1–4) plus 5 und 12 als ein UI-PR.
- [ ] ☐ Punkt 11 (VOIDMAP beim Build parsen) als eigener Scope
- [ ] ☐ Punkte 13–14 als kleiner Python-Hygiene-PR

## Artefakte
- `OUT/repo_ui_review_2026-10-07_exploration.md`
- Screenshots und Playwright-Report liegen nur lokal in der Session (nicht committet)
