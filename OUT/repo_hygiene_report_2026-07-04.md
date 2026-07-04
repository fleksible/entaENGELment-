# Report: Repo Hygiene Pass 2026-07-04

**Datum:** 2026-07-04
**Fokus:** Repo-Hygiene PRs/Issues/Branches/CI

## Ziel

Vollständiger Repo-Hygiene-Pass: offene PRs, offene Issues, Branch-Sync/-Hygiene,
CI-/Verify-Status, WELCOME.md/README.md-Verbindungen, Governance-/Claim-Hygiene.
Konservativ, evidence-first, keine Merges, keine Löschungen.

## Environment

| Feld | Wert |
|------|------|
| Repo | `fleksible/entaENGELment-` |
| `main` HEAD | `fe0a4e679aebd32f729ce57ffd9f9c593cad1a80` |
| Arbeitsbranch | `claude/repo-hygiene-audit-ozvzlb` (identisch mit `main` bei Start) |
| GitHub-Zugriff | ja (MCP-Tools, kein `gh` CLI) |
| Verify-Befehl | `make verify` (kanonisch, vorhanden) |
| Hinweis | Session-Clone war shallow; für Branch-Analyse per `git fetch --unshallow` vervollständigt |

## Findings

### CI / Verify

| Check | Ergebnis | Evidenz |
|-------|----------|---------|
| `make verify` (lokal, main-Stand) | ✅ PASS | port-lint, pytest, verify-pointers --strict, claim-lint alle grün |
| `make verify-governance` (lokal, vor Fix) | ❌ FAIL | Drift `docs/voids_backlog.md` **und** Drift UI-Mirror (11 Abweichungen) — bestand bereits auf `main` |
| `make verify-governance` (lokal, nach Fix) | ✅ PASS | 13 Workflows Posture-PASS, Backlog up-to-date, 22 VOIDs in sync |
| `make verify-js` (lokal, nach UI-Mirror-Sync) | ✅ PASS | pnpm frozen lockfile + turbo typecheck/lint/build, 4/4 Tasks |
| `security-audit.yml` auf `main` (scheduled) | ❌ FAIL seit 2026-06-22 | Runs 2026-06-22 und 2026-06-29 failure; letzter push-Run 2026-06-16 success |
| `ci-js-workspace.yml` auf `main` | ✅ zuletzt grün | Run auf `ee6fa70` (2026-06-24) success |

**[FACT] P0-Finding — Security-Audit auf `main` rot:**
`pnpm audit --audit-level=high` findet 4 Vulnerabilities (2 low, 1 moderate, **1 high**).
High: `undici < 6.27.0` (GHSA-vxpw-j846-p89q, WebSocket DoS), Pfad:
`.` → `electron-builder` → `app-builder-lib` → `@electron/rebuild` → `node-gyp` → `undici`.
Lockfile pinnt `undici@6.26.0`. Das failt den Job „JS dependency audit (pnpm)"
auf **jedem** PR und auf den scheduled Runs von `main`.
**Vorgeschlagener Minimal-Fix (nicht in diesem Pass ausgeführt):** In `package.json`
existiert bereits ein `pnpm.overrides`-Block für genau dieses Muster (form-data,
postcss, js-yaml). Ein Eintrag `"undici@<6.27.0": ">=6.27.0"` + `pnpm install`
(Lockfile-Regen) + `make verify-js` sollte den Audit grün machen. Separater Fix-PR empfohlen.

**[FACT] Struktur-Finding — Dependabot-npm-PRs failen systematisch:**
`.github/dependabot.yml` setzt für npm `directory: "/ui-app"`, der pnpm-Lockfile
liegt aber im Repo-Root. Dependabot bumped nur `ui-app/package.json`, der Root-Lockfile
bleibt stehen → `pnpm install --frozen-lockfile` failt mit
„specifiers in the lockfile don't match" (belegt im Job-Log von PR #275).
Jeder npm-Dependabot-PR ist damit CI-rot, unabhängig vom Inhalt.
**Vorgeschlagener Fix (nicht ausgeführt):** npm-Ecosystem-Eintrag auf `directory: "/"`
umstellen (pnpm-Workspace-Modus), damit Dependabot den Root-Lockfile mitpflegt.

### Offene PRs (6, alle Dependabot)

| PR | Titel (Kurz) | Branch-Alter | Konflikte | Checks | Kategorie | Empfehlung |
|----|--------------|--------------|-----------|--------|-----------|------------|
| #275 | @types/node 25.9.3→26.0.1 (ui-app) | 2026-06-29 | nein | ❌ workspace/UI-Build/JS-Tests/JS-Audit | E (Blocked) | Nicht mergen, bis Lockfile-Problem (s.o.) gelöst; danach `@dependabot recreate`. Major-Bump → mit Node-Version im CI abgleichen |
| #274 | postcss 8.5.15→8.5.16 (ui-app) | 2026-06-29 | nein | ❌ wie #275 | E (Blocked) | Wie #275; Patch-Bump, inhaltlich unkritisch |
| #273 | react-query 5.101.0→5.101.2 (ui-app) | 2026-06-29 | nein | ❌ wie #275 | E (Blocked) | Wie #275; Patch-Bump, inhaltlich unkritisch |
| #245 | eslint 9.39.4→10.5.0 (ui-app) | 2026-06-15, Updates bis 06-29 | nein | ❌ wie #275 | C (Human Review) | **Major-Bump.** UI-Lint wurde bewusst auf ESLint 9 stabilisiert (vgl. Issue #226 / PR #214-Historie). Erst Kompatibilität `eslint-config-next` prüfen |
| #272 | actions/setup-python 6.2.0→6.3.0 | 2026-06-29 | nein | ✅ außer JS-Audit (main-Problem) | A (Fast-Track) | Mergebereit, sobald undici-Audit-Fix da ist; Failure ist nicht PR-verursacht |
| #267 | actions/checkout 6.0.3→7.0.0 | 2026-06-22 | nein | unstable (JS-Audit) | C (Human Review) | **Major-Bump** mit Verhaltensänderung (blockt Fork-PR-Checkout bei `pull_request_target`/`workflow_run`). Workflows kurz gegenprüfen, dann mergebar |

Kein offener PR hat Merge-Konflikte; alle Basen sind nah an `main` (2–12 Commits behind).
Branch-Sync via Rebase ist bei Dependabot-PRs kontraproduktiv (Dependabot rebased selbst
via `@dependabot rebase`); deshalb kein eigener Sync-Commit erstellt.

**[FACT]** Chat-Anker verifiziert: PR #276 (welcome/anti-capture) und PR #277
(recovery governance drafts) sind beide am 2026-07-04 **gemerged** worden — nicht mehr offen.
PR #262 (Branch-Hygiene-Inventar) ist als `38e0c3f` in `main` gemerged.

### Offene Issues (3)

| Issue | Typ | Status | Empfehlung |
|-------|-----|--------|------------|
| #278 „Follow-up: align recovery governance drafts after PR #277" | Documentation/Governance | actionable now | Offen lassen; sauberer Cleanup-PR mit den 5 Checklist-Punkten (Check-Namen, SoT-Pfade, VOID_CLOSED review_ref, bilinguale Claim-Tags, claim_hash für reduced Events). Draft-Status respektieren |
| #240 „Overdue VOIDs: VOID-010, VOID-011" | Governance (auto-generiert) | blocked / needs human decision | Target-Dates (2026-06-01) sind überfällig. Entweder neue Targets in `VOIDMAP.yml` (GOLD-Change) setzen oder VOIDs auf SUSPENDED — Owner-Entscheidung (fleks) |
| #226 „Repo Re-Entry Notes: Wochenend-Audit Nachlauf" | Re-Entry-Marker | stale but valuable, teilweise erledigt | Punkt 1 (#214 schließen) ✅ erledigt (closed, not merged). Punkt 2 (#225) ✅ erledigt (closed, superseded durch #245). Punkt 3 (VOIDMAP-Drift) ✅ mit diesem Pass behoben. Punkte 4–5 (Narrative-Sedimente) offen. Kandidat für Schließen-mit-Kommentar oder Umwandlung in fokussiertes Narrativ-Issue — human decision |

Keine Issues geschlossen, keine neuen Issues erstellt.

### Branch-Hygiene (22 Remote-Branches ohne `main`)

Kategorien: **PR-backed** (offener PR), **superseded** (Inhalt vollständig in `main`),
**stale-unique** (einzigartiger Diff, kein PR), **special-case** (Human decision explizit).

| Branch | Letzter Commit | ahead | Net-Diff vs merge-base | Kategorie | Empfehlung |
|--------|----------------|-------|------------------------|-----------|------------|
| dependabot/…/types/node-26.0.1 | 2026-06-29 | 1 | 1 Datei | PR-backed (#275) | mit PR behandeln |
| dependabot/…/postcss-8.5.16 | 2026-06-29 | 1 | 1 Datei | PR-backed (#274) | mit PR behandeln |
| dependabot/…/react-query-5.101.2 | 2026-06-29 | 1 | 1 Datei | PR-backed (#273) | mit PR behandeln |
| dependabot/…/eslint-10.5.0 | 2026-06-21 | 3 | 1 Datei | PR-backed (#245) | mit PR behandeln |
| dependabot/…/setup-python-6.3.0 | 2026-06-29 | 1 | 9 Dateien | PR-backed (#272) | mit PR behandeln |
| dependabot/…/checkout-7.0.0 | 2026-06-24 | 1 | 13 Dateien | PR-backed (#267) | mit PR behandeln |
| claude/repo-hygiene-audit-ozvzlb | 2026-07-04 | — | — | active (dieser Pass) | — |
| claude/align-coverage-policy | 2026-04-04 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| claude/analyze-repo-essence-LKgK4 | 2026-01-03 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| claude/refactor-codebase-011CV4t3… | 2026-01-03 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| claude/repo-maintenance-consolidation-LA2ek | 2026-01-04 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| codex/update-markdown-file-in-repository | 2025-12-29 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| codex/update-readme-for-deepjump-integration | 2025-12-29 | 0 | ZERO | superseded | Safe-Delete-Kandidat |
| dependabot/…/setup-node-6.4.0 | 2026-05-11 | 0 | ZERO | superseded (PR zu, gemerged) | Safe-Delete-Kandidat |
| claude/sleepy-dirac-sgsjk0 | 2026-06-20 | 3 | ZERO (Commits netto leer) | superseded | Safe-Delete-Kandidat |
| fix/ci-security-pip-audit-171 | 2026-05-11 | 1 | 2 Zeilen (`safety`→`pip-audit` in ci.yml) | superseded — `main` nutzt bereits pip-audit (ci.yml Z.114/118) | Safe-Delete-Kandidat |
| claude/ui-lint-flat-config | 2026-06-16 | 1 | 1 Datei (ui-app/tsconfig.json) | superseded — `main`-tsconfig extends inzwischen `@enta/tsconfig/nextjs.json`; Branch würde regressieren | Close/Delete-Kandidat, kurze Human-Bestätigung |
| codex/beheben-von-fehlern-beim-mergen | 2026-05-31 | 3 | 7 Dateien (ui-app) | superseded — war Head von PR #214 (closed, superseded durch #222–#224 laut Issue #226) | Delete-Kandidat, kurze Human-Bestätigung |
| claude/repo-audit-analysis-oiW6K | 2026-04-06 | 4 | +479/−30 (Audit-Docs u.a. OUT/repo_audit_2026-04-06.md) | stale-unique | Human decision: Docs salvagen oder archivieren |
| claude/repo-maintenance-audit-mnZVm | 2026-05-20 | 2 | +309/−1 (Makefile, voids_backlog-Tooling) | stale-unique | Human decision: prüfen ob Tooling-Delta noch relevant |
| codex/find-more-ways-to-enhance-pipeline-management | 2026-05-30 | 2 | +226/−1 (pipeline_essentials Tool+Test+Doc) | stale-unique | Human decision: Inhalt evtl. noch wertvoll |
| codex/review-open-prs-and-issues-for-merge | 2026-06-11 | 1 | 21 Dateien (Workflow-Umbauten) | stale-unique | Human decision: Workflows haben sich seither weiterbewegt; vermutlich überholt, aber nicht ZERO |
| phase0/foundation-pack | 2026-01-18 | 0 | ZERO | **special-case** | Nicht löschen ohne explizite Entscheidung (Foundation-Anker-Charakter, per Vorgabe) |

**Es wurde kein Branch gelöscht.** Safe-Delete-Kandidaten erfüllen alle Kriterien
(kein offener PR, keine einzigartige Diff, vollständig in `main`, keine junge Aktivität) —
Löschung nur nach explizitem OK.

### WELCOME.md / README.md / Verbindungen

| Prüfpunkt | Ergebnis |
|-----------|----------|
| Links WELCOME.md (4 Markdown-Links) | ✅ alle Ziele existieren |
| Links README.md (32 Markdown-Links) | ✅ alle Ziele existieren |
| README → WELCOME | ✅ vorhanden (Zeile 5, „gentle orientation") |
| WELCOME → README/CLAUDE/Policies/LICENSE_REVIEW/Privacy/Anti-Capture | ✅ vorhanden |
| WELCOME → CONTRIBUTING.md | ⚠️ fehlte → mit diesem Pass ergänzt (1 Zeile) |
| 6 Core Layers | ✅ exakt 6, verständlich, konsistent mit PR #276 |
| „Commercial use and extractive capture are not identical" | ✅ vorhanden (WELCOME Z.124, LICENSE_REVIEW) |
| Claim-Hygiene WELCOME | ✅ „where implemented", „intended", „not a finished product" — keine falsche Implementierungsreife; verifyLedger/Governance Cockpit sind klar als intended/where-exists markiert, inkl. Hinweis „If a path does not exist yet, open a small PR or VOID instead" |
| LICENSE_REVIEW.md | ✅ trennt sauber Option A (OSI/Copyleft), B (source-available/noncommercial), C (Hybrid); „not legal advice"; keine Lizenzentscheidung getroffen |
| Privacy/Security-Überclaims | keine gefunden; PRIVACY_BOUNDARY/GITHUB_USE_POLICY sind als Policy/Governance formuliert |

### Governance / Claim-Hygiene

- **[FACT]** `claim-lint` (Scope index, spec, receipts, tools): keine ungetaggten Claims.
- **[FACT]** VOIDMAP-Drift behoben (siehe Actions Taken): `VOIDMAP.yml` (GOLD, unangetastet)
  wurde am 2026-06-24 um VOID-015/016/017/024–029 erweitert, aber weder
  `docs/voids_backlog.md` (generiert) noch `ui-app/lib/voidmap-parser.ts` (Hand-Mirror)
  waren nachgezogen. Beide Gates (`voids-backlog-check`, `voidmap-ui-drift-check`) waren rot.
- **[FACT]** `data/receipts/` wurde nicht berührt (append-only respektiert).

## Aktionen

- [x] `docs/voids_backlog.md` regeneriert via `python3 tools/voids_backlog_gen.py` (sanktionierter Weg)
- [x] `ui-app/lib/voidmap-parser.ts` mechanisch re-synct: 9 fehlende VOIDs gespiegelt (Wortlaut 1:1 aus `VOIDMAP.yml`), `med`→`medium` bei VOID-021/022, `last_updated` 2026-06-24
- [x] WELCOME.md: 1 Zeile CONTRIBUTING-Link ergänzt
- [x] Dieser Report

Verifikation nach den Änderungen: `make verify` ✅, `make verify-governance` ✅, `make verify-js` ✅.

## Nicht getan

- Keine Branches gelöscht.
- Keine PRs gemerged, geschlossen oder rebased (Dependabot rebased selbst; Root-Cause liegt in dependabot.yml/Lockfile, nicht in den Branches).
- Keine Lizenzentscheidung getroffen; LICENSE_REVIEW.md unverändert.
- Keine Issues geschlossen oder erstellt.
- Keine konzeptuelle Expansion, kein verifyLedger-/Cockpit-/MaterialPointer-Bau.
- Kein Dependency-Upgrade (undici-Fix nur als konkreter Vorschlag dokumentiert).
- `VOIDMAP.yml`, `index/`, `policies/`, Receipts: unangetastet (GOLD/IMMUTABLE).

## Risiken

- **Security:** undici-High-Advisory bleibt offen, bis der Override-Fix gemerged ist; scheduled Security-Audit auf `main` bleibt bis dahin rot.
- **Merge-Risiko Dependabot:** #245 (eslint 10 major) und #267 (checkout v7 major, Fork-PR-Verhalten) brauchen bewusste Review; nicht fast-tracken.
- **Claim/Evidence:** Issue #278-Checkliste beschreibt bekannte Doc-Referenz-Abweichungen aus PR #277 — solange offen, enthält `docs/governance/` einzelne Pfad-/Namens-Inkonsistenzen (als Draft markiert, kein Overclaim).

## Offene Punkte

- [ ] ☐ P0: undici-Override-Fix-PR (`pnpm.overrides` + Lockfile-Regen + `make verify-js`)
- [ ] ☐ P1: dependabot.yml npm-`directory` auf Workspace-Root umstellen, danach `@dependabot recreate` für #273/#274/#275
- [ ] ☐ P1: #272 mergen, sobald Audit grün; #267 nach kurzem `pull_request_target`-Check
- [ ] ☐ P2: Branch-Cleanup der 9 Safe-Delete-Kandidaten nach explizitem OK (phase0/foundation-pack ausgenommen)
- [ ] ☐ P2: Issue #278-Follow-up-PR; Entscheidung zu #240 (Target-Dates) und #226 (schließen mit Verweis?)
- [ ] ☐ P2: verifyLedger / Tamper-Drills / typed Material als separater Code-PR (nur Vorschlag)

## Artefakte

- `OUT/repo_hygiene_report_2026-07-04.md` (dieser Report)
- `docs/voids_backlog.md` (regeneriert)
- `ui-app/lib/voidmap-parser.ts` (re-synct)
- `WELCOME.md` (1 Zeile)

## Final Status

**WARN** — Kern-Verify grün, Repo strukturell sauber, aber: scheduled Security-Audit
auf `main` rot (undici high), Dependabot-npm-PRs strukturell blockiert (Lockfile-Drift),
zwei Major-Bumps warten auf bewusste Review.
