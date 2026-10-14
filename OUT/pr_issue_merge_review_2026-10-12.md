# Report: PR-/Issue-Merge-Prüfung

**Datum:** 2026-10-12
**Fokus:** Merge-Reife PRs und Issues

## Ziel
Alle offenen PRs auf Merge-Reife prüfen, alle offenen Issues gegen `main` abgleichen und
weitere nötige Korrekturen benennen. Keine Merges, keine Code-Änderungen (Plan-First, G0).

## Ausgangslage `main` (`a7773db`)
- `make verify`: grün. 665 Tests bestanden, Pointer (0 CORE fehlend), Claim-Lint ohne Befund [FACT]
- `make verify-governance`: grün. 15 Workflows erfüllen den Posture-Vertrag, 22 VOIDs synchron [FACT]
- 4 optionale Pointer fehlen (`out/status/…`, `out/badges/…`, `out/verify.json`,
  `out/snapshot_manifest.json`). Das sind generierte Artefakte, kein Fehler.
- **JS-Audit auf `main` ist rot:** Next.js `<16.3.8` (GHSA-cjq9-62q9-8jv4, high) [FACT].
  Das ist die einzige Ursache, warum alle 7 Dependabot-PRs rot sind.

## Befund: PRs (11 offen)

### Menschliche PRs: alle CI-grün, mergebar (`clean`), ohne offene Review-Threads

| PR | Inhalt | CI | Review | Empfehlung |
|----|--------|----|--------|------------|
| #391 | Next.js 16.3.8 (Security), Turbo `agentGuidance: false` | grün | Codex: keine Befunde | **zuerst mergen** — entsperrt alle Dependabot-PRs |
| #389 | FractalSense: Nullgrößen-Absturz + ResizeObserver | grün | Codex: keine Befunde | nach #391: Base auf `main` umstellen, CI abwarten, mergen |
| #390 | Dependabot-uv: expliziter PyPI-Index | grün | Codex: keine Befunde | mergen; danach uv-Lauf auswerten |
| #388 | UI-Review-Report (nur `OUT/`) | grün | 5 Codex-Threads, alle gelöst | mergen |

Nachprüfungen dieser Session:
- #391 lokal mit pnpm 10.33.0 (`pnpm audit --audit-level=high`) am 12.10. erneut grün:
  1 moderate, 1 high (braces, bestehende Ausnahme) [FACT]
- #389 enthält #391 als Elternteil; die PR-Differenz zeigt nur den Canvas-Fix [FACT]
- #390: Der heutige uv-Lauf (Run 38223076749) scheitert erneut mit
  `unknown url type: '/pypi/rpds-py/json'`. Das ist genau der Fehler, den #390 adressiert [FACT].
  Ob #390 ihn behebt, zeigt erst ein Lauf nach dem Merge [HYP].
  (Log per Mustersuche ausgewertet, nicht vollständig gelesen.)

### Dependabot-PRs: alle rot nur wegen JS-Audit (Next.js auf `main`)
Tests, UI-Build, Workspace, DeepJump und Lint sind in jedem dieser PRs grün.

| PR | Update | Art | Empfehlung |
|----|--------|-----|------------|
| #398 | autoprefixer 10.5.4 → 10.6.1 | minor | nach #391 rebasen, mergen |
| #397 | jest-environment-jsdom 30.4.1 → 30.5.2 | minor | nach #391 rebasen, mergen |
| #396 | postcss 8.5.23 → 8.5.29 | patch | nach #391 rebasen, mergen |
| #395 | electron 44.4.5 → 44.7.0 | minor | nach #391 rebasen, mergen |
| #394 | @testing-library/jest-dom 6.9.1 → 7.0.1 | **major** | Tests grün; vor Merge Changelog prüfen |
| #393 | actions/setup-node 7.0.0 → 7.1.0 | minor | nach #391 rebasen, mergen |
| #392 | actions/upload-artifact 7.0.1 → 7.0.2 | patch | nach #391 rebasen, mergen |

Die npm-PRs ändern alle `pnpm-lock.yaml`. Nach jedem Merge muss der nächste neu
rebased werden (`@dependabot rebase`).

## Befund: Issues (5 offen)

| Issue | Stand auf `main` | Was fehlt |
|-------|------------------|-----------|
| #333 Python-Lock | uv-Lock, gehashte Exporte, gelockte CI/SBOM sind umgesetzt. `release.yml` und `void-sync.yml` installieren inzwischen gelockt (#378, #379) [FACT] | nur noch der Dependabot-uv-Fehler. Nach #390 und einem grünen uv-Lauf schließbar |
| #332 Security-Settings | Private Reporting aktiv, `SECURITY.md` verlinkt den Weg (#381 gemergt), Branch-Schutz mit 5 Pflicht-Checks [FACT] | Checkliste im Issue ist veraltet. Offen: CodeQL-Trigger dokumentieren, externer Test-Report (nur durch einen Menschen möglich) |
| #311 VOID-010/011 überfällig | beide `IN_PROGRESS`, Zieltermin 2026-07-15 (≈ 3 Monate über) | Entscheidung: neuer `target_date` in `VOIDMAP.yml` (GOLD → nur mit OK) oder Abschlussarbeit |
| #305 Annex F v0.3 | keine Umsetzung; Scanner/Rohdaten (`phasor.py`, 42 QRS-Ereignisse) fehlen | Forschungsarbeit; Blocker sind die Rohdaten |
| #278 Governance-Drafts | 2 von 5 Punkten erledigt (Check-Namen, SoT-Pfade; Altpfade nicht mehr auffindbar) [FACT] | 3 Punkte in `spec/runtime_eventlog_v0_1.json` und `policies/claim_tags_v0_2.yaml` (GOLD → nur mit OK). Checkliste im Issue nicht abgehakt |

## Befund: weitere Korrekturen
1. **UI-Bugs aus #388 noch offen** (auf `main` nachgeprüft) [FACT]:
   - Mobile-Navigation `min-w-[56px]` × 7 > 375 px (`ui-app/components/layout/Navigation.tsx:39`)
   - tesser3TAKT-Grid ohne `min-w-0` (`Tesser3TaktHudV2.tsx`)
   - Hydration #418 durch `toLocaleTimeString` (`AttentionStream.tsx:115`)
   - Zoom gesperrt (`app/layout.tsx:13-14`, WCAG 1.4.4)
2. **`datetime.utcnow()`** in `ledger/replay_determinism.py:139` erzeugt 104 Deprecation-Warnungen im Testlauf.
3. **Electron `Index.html`** lädt 4 Skripte zur Laufzeit vom CDN; offline bricht es ab.
4. **Branch-Aufräumen vom 07.10. nicht ausgeführt:** 16 veraltete Branches liegen
   weiter auf `origin`, `archive/*`-Tags gibt es keine. Befehle stehen in
   `OUT/branch_cleanup_2026-10-07.md`. Aus Cloud-Sessions ist das gesperrt.
5. **Verwaiste Workflow-Einträge:** „Temporary Black Format“, „Temporary Lockfile Refresh“
   und „Temporary Merge Main“ sind in Actions noch als `active` gelistet; die Dateien gibt
   es auf `main` nicht mehr. Kosmetisch; über GitHub → Actions deaktivierbar.

## Aktionen
- [x] 11 PRs: Details, Check-Runs, Reviews, Review-Threads und Diffs geprüft
- [x] Fehlerursache der roten Dependabot-PRs aus dem Job-Log bestimmt
- [x] #391 lokal erneut auditiert (pnpm 10.33.0)
- [x] Heutigen uv-Dependabot-Lauf ausgewertet
- [x] 5 Issues inkl. Kommentare gegen `main` abgeglichen
- [x] `make verify` und `make verify-governance` auf `main` ausgeführt
- [x] UI-Befunde aus #388 im Code nachgeprüft

## Nicht getan
- Keine Merges, keine Rebases, keine Issue-Kommentare. Merge ist ein Außenschritt und braucht OK (G0).
- Keine GOLD-Änderung (`VOIDMAP.yml`, `spec/`, `policies/`).
- Kein `make verify-js` auf `main`; JS-Status stammt aus der CI der PRs.
- Changelog von jest-dom 7 nicht gelesen.

## Risiken
- [RISK] Solange #391 offen ist, bleibt `main` mit einer bekannten Next.js-High-Lücke.
- [RISK] Laut Stand in #332 (02.10.) ist der JS-Audit kein Pflicht-Check im Branch-Schutz.
  Dependabot-PRs wären trotz rotem Audit technisch mergebar.
- [RISK] #389 zeigt nach dem Merge von #391 weiter auf dessen Branch. Nur wenn der Branch
  über GitHub gelöscht wird, stellt GitHub die Base automatisch um. Bei `git push --delete`
  schließt GitHub den PR. Base deshalb vorher selbst auf `main` stellen.

## Offene Punkte
- [ ] ☐ OK für Merge-Reihenfolge: #391 → #389 (Base umstellen) → #390 → #388 → Dependabot nacheinander
- [ ] ☐ #394 (jest-dom 7, major): Changelog prüfen
- [ ] ☐ #333 nach grünem uv-Lauf schließen
- [ ] ☐ #332/#278: Checklisten im Issue aktualisieren
- [ ] ☐ #311: Entscheidung neuer Zieltermin (GOLD) oder Abschlussarbeit
- [ ] ☐ UI-Fix-PR für die P1-Bugs 2–4 und den Zoom (Empfehlung aus #388)
- [ ] ☐ Branch-Aufräumen lokal ausführen (Befehle in `OUT/branch_cleanup_2026-10-07.md`)

## Artefakte
- `OUT/pr_issue_merge_review_2026-10-12.md`
