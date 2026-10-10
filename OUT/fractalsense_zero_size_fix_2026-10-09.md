# Report: FractalSense-Canvas bei Nullgröße

**Datum:** 2026-10-09
**Nachtrag:** 2026-10-10
**Fokus:** FractalSense-Absturz beheben
**Authority:** DERIVED / REVIEW-PENDING
**Basis:** main `a7773db68d97dbd8271b0921d011934d2e921170`; Befund aus PR #388.

## Ziel
Der versteckte mobile Canvas darf beim Resize keine ImageData mit Nullgröße
anfordern und muss nach dem Wiedereinblenden die aktuelle Größe verwenden.

## Aktionen
- [x] Sechs Komponententests mit echtem React-Mount in jsdom ergänzt.
  Canvas-API und ResizeObserver sind kontrollierte Test-Doubles.
- [x] RED: alle sechs Fälle scheitern vor dem Fix; Nullgrößen erzeugen den
  `IndexSizeError` aus dem Befundbericht.
- [x] Rendern beginnt erst nach der ersten Messung; Breite/Höhe <= 0 werden
  vor der ImageData-Allokation abgefangen. Interaktion bei Nullgröße wird ignoriert.
- [x] ResizeObserver am Container ersetzt den Window-Listener und wird beim
  Unmount getrennt. Unveränderte Maße lösen keinen neuen Render aus.
- [x] GREEN: sechs neue Fälle und 23 bestehende UI-Tests bestehen.
- [x] `pnpm turbo run typecheck lint build test`: 5/5 Tasks erfolgreich.
- [x] `make verify`: 665 Tests und 165 Subtests erfolgreich; Pointer-/Claim-/Port-Gates bestehen.
- [x] ruff, black --check und mypy: erfolgreich (100 bzw. 48 geprüfte Dateien).

## Nicht getan
- Keine weiteren UI-Befunde aus #388 geändert.
- Keine GOLD-/Receipt-/Release-Änderung, kein Merge.
- Kein echter Browser-/Gerätetest bestätigt: Chromium-Download in dieser
  Umgebung liefert ein ungültiges ZIP. jsdom ersetzt diesen Nachweis nicht.

## Risiken
- Der lokale pnpm-Wrapper verwendete 11.25.0; Node war 24.19.0. Der unveränderte
  CI-Vertrag nutzt pnpm 10.33.0 und Node 22 und muss separat bestehen.
- Ein aktueller Audit findet neue Next.js-Advisories auf dem Basisstand. Der
  Versionspatch wird separat angeboten; ein rotes Security-Gate darf nicht
  durch Ignorieren dieser neuen Befunde umgangen werden.

## Nachtrag zur Security-Basis (10. Oktober)
Die initiale GitHub-CI auf `88e8b30` bestand in zehn Workflow-Läufen; nur der
Security-Audit scheiterte am bereits auf main vorhandenen Next.js-High-Fund.
Der separate Dependency-PR hebt Next.js/eslint-config-next auf 16.3.8 an.
Dieser Canvas-Branch übernimmt dessen Commit als zweiten Elternteil; der
PR-Vergleich erfolgt gegen den Dependency-Branch und zeigt weiterhin nur den
Canvas-Fix. Zuerst Dependency-PR integrieren, danach Canvas-PR auf main umstellen
und die dann aktuellen Gates prüfen. Kein Merge in main wurde vorgenommen.

## Offene Punkte
- [ ] Mobile im echten Browser: Controls öffnen, Viewport ändern, Canvas öffnen;
  keine Seitenexception und korrekt neu gezeichneter Canvas.
- [ ] CODEOWNERS-/Claude-/Diogenes-Review und CI vor Integration.

## Artefakte
- `ui-app/components/fractalsense/FractalCanvas.tsx`
- `ui-app/test/fractal-canvas.test.jsx`
- `ui-app/jest.config.mjs`
- `ui-app/package.json`
