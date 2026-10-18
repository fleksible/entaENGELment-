# Report: Merge-Stand prüfen und Probleme beheben

**Datum:** 2026-10-18
**Fokus:** Merge-Stand und Repo-Pflege

## Ziel
Prüfen, ob alles gemergt ist, und aufgetauchte Probleme im Sinne des Repos beheben.
Grundlage ist der Stand aus `OUT/pr_issue_merge_review_2026-10-12.md`. Owner-OK
(G0) am 2026-10-18 für die folgenden Schritte:
- Merge der grünen PRs
- Dependabot-Sammel-PR
- `utcnow`-Fix
- UI-P1-Bugs plus Zoom

## Ausgangslage `main` (`7ed5bf9`)
- `make verify` und `make verify-governance` grün [FACT]
- **Security-Audit rot:** Next.js `<16.3.8`, darunter GHSA-cjq9-62q9-8jv4 (high).
  Zuletzt am 2026-10-12 im wöchentlichen Lauf gescheitert, lokal am 18.10. reproduziert [FACT]
- 14 offene PRs:
  - 5 menschliche: #388–#391, #399
  - 9 von Dependabot: #392–#398, #401, #402
- Der uv-Dependabot-Lauf scheitert weiter mit `unknown url type: '/pypi/rpds-py/json'` [FACT]

## Aktionen
- [x] Alle 14 offenen PRs lokal in einen Integrationsstand gemergt: konfliktfrei.
  Darauf grün [FACT]:
  - `make verify`
  - `verify-governance`
  - `verify-js`
  - Jest 66/66
  - Fractalsense 184/184
  - `pnpm audit --audit-level=high`
- [x] Nach `main` gemergt, in dieser Reihenfolge:
  - #391: Next.js 16.3.8, schließt die High-Lücke
  - #390: uv-Updater an expliziten PyPI-Index gebunden
  - #388: UI-Review-Report
  - #389: FractalSense-Absturz; Base vorher von #391 auf `main` umgestellt
  - #399: Merge-Prüfung 12.10.
- [x] Dependabot #392–#398 als ein Sammel-Commit, Lockfile mit pnpm 10.33.0 neu erzeugt.
  Grund: Die PRs ändern alle `pnpm-lock.yaml` und blockieren sich nach jedem Merge.
- [x] #394 (`@testing-library/jest-dom` 7, major) geprüft:
  - Verlangt Node ≥ 22; das Repo verlangt ≥ 22.12, die CI nutzt 22 [FACT]
  - Verlangt `@testing-library/dom` als Peer; pnpm installiert ihn automatisch mit (10.4.2) [FACT]
  - Einzige Nutzung: `__tests__/setup.js`; Jest danach 66/66 [FACT]
- [x] `ledger/replay_determinism.py`: `utcnow()` durch `now(timezone.utc)` ersetzt.
  Gleicher Wert, die 104 Deprecation-Warnungen sind weg [FACT].
- [x] UI-Bugs aus #388 mit Playwright reproduziert und behoben.
  Gemessen bei 375×812 und 1280×800, vorher/nachher [FACT]:

| Befund | vorher | nachher |
|--------|--------|---------|
| Mobile-Navigation | letzter Eintrag endet bei 392 px > 375 px | 375 px; alle Labels voll lesbar ab 375 px, darunter Ellipse bei „tesser3TAKT“ |
| tesser3TAKT | Seite 690 px breit | 375 px |
| Metatron | `pageerror` React #418 | kein Fehler |
| Zoom | `maximum-scale=1, user-scalable=no` | `width=device-width, initial-scale=1` |

## Nicht getan
- Keine GOLD-Änderung (`VOIDMAP.yml`, `spec/`, `policies/`, `index/`).
- #401 und #402 nicht selbst geschlossen. Beide bumpen nur `next` auf 16.3.8, das ist
  mit #391 auf `main`. Dependabot schließt sie selbst [HYP].
  - #401 ist zusätzlich kaputt: Es ändert nur `ui-app/package.json` ohne Lockfile
    und scheitert an `--frozen-lockfile`.
- #392–#398 nicht selbst geschlossen; Dependabot schließt sie nach dem Merge des
  Sammel-PR selbst [HYP].
- Weitere UI-Befunde (P2) aus #388 offen:
  - Kontrast
  - Label-Verknüpfung in FractalSense
  - `aria-current`
  - Demo-Badges
  - UI-Smoke-Test in CI
- Electron-CDN, Branch-Aufräumen (aus Cloud-Sessions gesperrt) und verwaiste
  „Temporary“-Workflows sind unverändert.
- Issues nicht kommentiert oder geschlossen.

## Risiken
- [RISK] Ob #390 den uv-Updater repariert, zeigt erst der nächste uv-Lauf (montags).
- [RISK] Der Sammel-PR enthält ein Major-Update (jest-dom 7). Die Tests sind grün,
  das Changelog wurde aber nicht gelesen: Die GitHub-Release-API ist aus der Session nicht erreichbar.
- [RISK] Unter 375 px zeigt die Mobile-Navigation „tesser3TA…“. Der Eintrag bleibt
  erreichbar, das Icon steht daneben.

## Offene Punkte
- [ ] ☐ Sammel-PR reviewen und mergen; danach prüfen, ob Dependabot #392–#398, #401, #402 geschlossen hat
- [ ] ☐ #333 schließen, sobald ein uv-Dependabot-Lauf nach #390 grün ist
- [ ] ☐ #332/#278: Checklisten im Issue aktualisieren (Stand siehe Report vom 12.10.)
- [ ] ☐ #311: neuer Zieltermin für VOID-010/011 (GOLD) oder Abschlussarbeit
- [ ] ☐ UI-P2-Punkte und Playwright-Smoke-Test in CI als eigener Scope
- [ ] ☐ Branch-Aufräumen lokal ausführen (`OUT/branch_cleanup_2026-10-07.md`)

## Artefakte
- `OUT/repo_merge_fix_2026-10-18.md`
- `package.json`, `ui-app/package.json`, `pnpm-lock.yaml`, 6 Workflows unter `.github/workflows/`
- `ledger/replay_determinism.py`
- `ui-app/components/layout/Navigation.tsx`, `ui-app/components/tesser3takt/Tesser3TaktHudV2.tsx`,
  `ui-app/components/metatron/AttentionStream.tsx`, `ui-app/app/layout.tsx`
