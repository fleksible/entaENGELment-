# Repo Hygiene Report — 2026-07-04

**Datum:** 2026-07-04
**Fokus:** Repo-Hygiene-Pass (read-mostly)

## Ziel

Vollständiger Hygiene-Pass über offene PRs, offene Issues, Branch-Bestand,
WELCOME.md/README.md-Verbindungen, CI-/Verify-Status und Claim-/Governance-Hygiene.
Konservativ, evidence-first, keine Merges, keine Löschungen, keine konzeptuelle Expansion.

## Scope

- Offene Pull Requests (Klassifikation A–E)
- Offene Issues (Triage)
- Branch-Matrix (ahead/behind, Netto-Diff, Kategorien)
- WELCOME.md / README.md / Policy-Dateien (Links + Claim-Hygiene)
- CI / `make verify` / `make verify-governance`
- Claim-Tags: `[FACT]` = im Repo nachweisbar, `[DRAFT]`/`[SPEC]` = Entwurf/Absicht,
  Einschätzungen sind als solche markiert.

## Environment

| Feld | Wert |
|------|------|
| Repo | `fleksible/entaENGELment-` |
| `main` HEAD | `fe0a4e679aebd32f729ce57ffd9f9c593cad1a80` (docs: add recovery governance drafts, Squash von PR #277) |
| Arbeitsbranch | `claude/hopeful-faraday-m301os` (von `main` @ fe0a4e6) |
| Tools | git (voll, nach `--unshallow`), GitHub-MCP (Auth ✓); kein `gh` CLI verfügbar |
| Verify-Befehl | `make verify` vorhanden und kanonisch [FACT] |
| Hinweis Umgebung | `make install-dev` kollidiert im Container mit Debian-`cryptography` (Workaround: `--ignore-installed cryptography`); `make verify` ruft ein uv-Tool-`pytest` ohne Repo-Deps auf → Phasen einzeln mit `python3 -m pytest` ausgeführt. Umgebungsartefakt, kein Repo-Fehler. |

---

## Findings

### 1. Offene PRs (6 — alle Dependabot)

[FACT] Es gibt genau 6 offene PRs, alle von `dependabot[bot]`. PR #276 (WELCOME/Anti-Capture)
und PR #277 (Recovery-Governance-Drafts) wurden am 2026-07-04 gemerged. PR #262
(Branch-Hygiene-Inventar) ist gemerged (Commit `38e0c3f` in main).

| PR | Inhalt | Alter / Update | Checks | Diff | Kategorie | Empfehlung |
|----|--------|----------------|--------|------|-----------|------------|
| #272 | actions/setup-python 6.2.0→6.3.0 (minor) | 2026-06-29 | grün außer „JS dependency audit (pnpm)" (vorbestehend auf main, s. §5) | 9 Dateien, ±12 | **A** | Mergebereit nach menschlichem OK; 2 Commits behind main → vorher Branch-Update |
| #267 | actions/checkout 6.0.3→7.0.0 (**major**) | 2026-06-22 / 06-24 | grün außer pnpm-audit (vorbestehend) | 13 Dateien, ±21 | **A/B** | v7-Breaking-Change (Block von Fork-PR-Checkout bei `pull_request_target`/`workflow_run`) betrifft dieses Repo nicht — kein Workflow nutzt diese Events [FACT]. Mergebereit nach menschlichem OK; 4 Commits behind → Branch-Update |
| #275 | @types/node 25.9.3→26.0.1 (**major**) | 2026-06-29 | **rot**: workspace, UI Build, JS Tests | 1 Datei (nur `ui-app/package.json`) | **E** | Blockiert durch Lockfile-Problem (s.u.); nach Dependabot-Fix recreaten, dann Major-Bump neu bewerten |
| #274 | postcss 8.5.15→8.5.16 (patch) | 2026-06-29 | **rot**: workspace, UI Build, JS Tests | 1 Datei | **B** | Nach Dependabot-Fix recreaten; Inhalt unkritisch |
| #273 | @tanstack/react-query 5.101.0→5.101.2 (patch) | 2026-06-29 | **rot**: workspace, UI Build, JS Tests | 1 Datei | **B** | Wie #274 |
| #245 | eslint 9.39.4→10.5.0 (**major**, Label `security`) | 2026-06-15 / 06-29 | **rot**: workspace, UI Build, JS Tests | 1 Datei | **E/C** | Doppelt blockiert: Lockfile-Problem **und** UI-Lint wurde bewusst auf ESLint 9 stabilisiert (vgl. Issue #226). Entscheidung nötig: Major ignorieren (`@dependabot ignore this major version`) oder geplanter Umstieg mit `verify-js` |

**Systemische Ursache der 4 roten npm-PRs [FACT]:**
`.github/dependabot.yml` konfiguriert das npm-Ökosystem mit `directory: "/ui-app"`.
Das Repo ist aber ein pnpm-Workspace mit einem einzigen Root-`pnpm-lock.yaml`.
Dependabot ändert daher nur `ui-app/package.json` (je 1 Zeile, ohne Lockfile) —
jeder Job mit `pnpm install --frozen-lockfile` schlägt zwangsläufig fehl.
Kein npm-Dependabot-PR kann in dieser Konfiguration grün werden.

**Empfohlener Fix (separater Mini-PR, nicht in diesem Pass):**
npm-Eintrag in `dependabot.yml` auf `directory: "/"` umstellen (Dependabot
unterstützt pnpm-Workspaces vom Root aus), danach `@dependabot recreate` auf den
offenen npm-PRs.

### 2. Offene Issues (3)

| # | Titel | Kategorie | Status | Empfehlung |
|---|-------|-----------|--------|------------|
| #278 | Follow-up: align recovery governance drafts after PR #277 | Documentation / Governance | **actionable now** — alle referenzierten Dateien existieren in main [FACT] | Als eigener kleiner Cleanup-PR abarbeiten (P2); gut gescopte Checkliste |
| #240 | Overdue VOIDs: VOID-010, VOID-011 | Governance / Backlog | **needs human decision** — beide VOIDs stehen weiterhin auf `IN_PROGRESS` in `VOIDMAP.yml` [FACT], Target 2026-06-01 überschritten | Offen lassen; Owner entscheidet: Re-Dating oder Teilschließung mit Evidence |
| #226 | Repo Re-Entry Notes: Wochenend-Audit Nachlauf | Governance / Notizen | **stale but valuable** — Kernpunkte inzwischen erledigt: #214 ist nicht mehr offen [FACT]; #225 (eslint 10.4.1) ist nicht mehr offen und durch #245 ersetzt (Dependabot-Supersede, Einschätzung); voids_backlog-Drift in diesem Pass behoben; Grimm-2-Narrative weiterhin nur `_template.md` [FACT] | Schließen mit Verweis auf diesen Report (Human OK) oder bewusst als Marker offen lassen |

Keine Issues geschlossen, keine neuen Issues erstellt.

### 3. Branch-Hygiene (22 Remote-Branches außer main)

Vollständige Matrix (ahead = eigene Commits vs. merge-base; „0 Netto-Diff" = Tree
identisch mit merge-base bzw. vollständig in main enthalten):

**Kategorie: superseded / safe-deletion-candidates (nur Vorschlag — nichts gelöscht):**

| Branch | Letzter Commit | Befund |
|--------|----------------|--------|
| `claude/align-coverage-policy` | 2026-04-04 | 0 eigene Commits, vollständig in main |
| `claude/analyze-repo-essence-LKgK4` | 2026-01-03 | dito |
| `claude/refactor-codebase-011CV4t3…` | 2026-01-03 | dito |
| `claude/repo-maintenance-consolidation-LA2ek` | 2026-01-04 | dito |
| `codex/update-markdown-file-in-repository` | 2025-12-29 | dito |
| `codex/update-readme-for-deepjump-integration` | 2025-12-29 | dito |
| `dependabot/github_actions/actions/setup-node-6.4.0` | 2026-05-11 | verwaist: kein offener PR, 0 eigene Commits |
| `claude/sleepy-dirac-sgsjk0` | 2026-06-20 | 3 Commits, aber 0 Netto-Diff vs. merge-base |

**Kategorie: protected/special-case — human decision required:**

| Branch | Befund |
|--------|--------|
| `phase0/foundation-pack` | 0 Netto-Diff vs. merge-base (370 behind), aber Foundation-Anker-Charakter → per Vorgabe **nicht** löschen, separat entscheiden |
| `fix/ci-security-pip-audit-171` | 1 Mini-Commit (±2 Zeilen), 2026-05-11; pip-audit läuft auf main grün → funktional vermutlich überholt (Einschätzung), vor Löschung prüfen |

**Kategorie: stale mit einzigartigem Inhalt (keep bis Review):**

| Branch | Letzter Commit | Netto-Diff |
|--------|----------------|-----------|
| `claude/repo-audit-analysis-oiW6K` | 2026-04-06 | +479/−30 (8 Dateien, Audit-Docs) |
| `claude/repo-maintenance-audit-mnZVm` | 2026-05-20 | +309/−1 (3 Dateien) |
| `claude/ui-lint-flat-config` | 2026-06-16 | +22/−7 (1 Datei) |
| `codex/beheben-von-fehlern-beim-mergen` | 2026-05-31 | +419/−86 (7 Dateien) |
| `codex/find-more-ways-to-enhance-pipeline-management` | 2026-05-30 | +226/−1 (4 Dateien) |
| `codex/review-open-prs-and-issues-for-merge` | 2026-06-11 | +245/−169 (21 Dateien) |

**Kategorie: PR-backed (aktiv):** die 6 Dependabot-Branches (s. §1) sowie
`claude/hopeful-faraday-m301os` (dieser Hygiene-Pass).

[FACT] Kein einziger Nicht-Dependabot-Branch hat einen offenen PR.

### 4. WELCOME.md / README.md / Verbindungshygiene

- [FACT] Alle relativen Links intakt: README.md (32 geprüft), WELCOME.md (4),
  CONTRIBUTING.md, GITHUB_USE_POLICY.md, ANTI_CAPTURE_POLICY.md, PRIVACY_BOUNDARY.md,
  LICENSE_REVIEW.md — keine toten Links.
- [FACT] README.md verweist prominent auf WELCOME.md (Zeile 5); WELCOME verweist
  zurück auf README/CLAUDE.md/Policies.
- [FACT] WELCOME.md hat exakt 6 Core Layers (Governance, Verification, Gläserne
  Agora & Receipt-Ledger, Essence Architecture, Commons & Anti-Capture, Exploration).
- Claim-Hygiene: WELCOME nutzt konsequent „where implemented" / „intended" /
  „If a path does not exist yet…"; verifyLedger ist als *intended* markiert,
  nicht als implementiert. Kein Implementierungs-Überclaim gefunden.
- [FACT] Der Guard-Satz „Commercial use and extractive capture are not identical."
  steht in WELCOME.md (§ Anti-Capture Position) und wird in LICENSE_REVIEW.md
  ausgeführt; Anti-Capture ist explizit als Governance-Position (nicht als
  rechtlich durchsetzbar) deklariert.
- [FACT] LICENSE_REVIEW.md trennt die drei Pfade sauber: (A) OSI/Copyleft (AGPL),
  (B) source-available/noncommercial, (C) Hybrid. Keine Lizenzentscheidung
  getroffen — Dokument empfiehlt selbst dedizierte Legal-Review.
- [FACT] LICENSE ist Apache-2.0; README-Badge und LICENSE_REVIEW konsistent dazu.
- **Ergebnis: keine Änderungen an WELCOME/README nötig — keine vorgenommen.**

### 5. CI / Verify

| Check | Ergebnis | Beleg |
|-------|----------|-------|
| `make verify` (Kern-Membran) | **PASS** lokal auf `fe0a4e6` [FACT] | port-lint OK · pytest **186 passed** · `verify_pointers.py --strict` OK (4 optionale Pfade als WARN) · claim-lint OK |
| `make verify-governance` | **FAIL → teilweise behoben** | workflow-posture: 13/13 PASS · voids-backlog-check: Drift **behoben durch Regeneration in diesem Pass** · voidmap-ui-drift-check: **weiterhin FAIL** [FACT] |
| voidmap-ui-drift Detail | 9 VOIDs (015–017, 024–029) fehlen im UI-Mirror `ui-app/lib/voidmap-parser.ts`; 2 Priority-Drifts (VOID-021/022: `medium` vs. `med`) [FACT] | `tools/voidmap_ui_drift_check.py` |
| CI-Verdrahtung | [FACT] `verify-governance`/`voids_backlog`-Checks sind in **keinem** Workflow unter `.github/workflows/` referenziert — Governance-Drift gated CI nicht | grep über Workflows |
| Security Audit (main) | **FAIL** seit 2026-06-22 (Scheduled Runs 06-22 & 06-29 rot; letzter grüner Lauf 06-16) [FACT] | `pnpm audit --audit-level=high`: 4 Vulns (2 low, 1 moderate, **1 high**) — **undici < 6.27.0**, DoS via Fragment-Count-Bypass (GHSA-vxpw-j846-p89q), transitiv über `electron-builder → app-builder-lib → @electron/rebuild → node-gyp → undici` |
| `ci.yml` verify-Job (Push-Runs) | **FAIL auf main** — die letzten 3 Push-Runs (fe0a4e6 vom 07-04, 9d38d77 vom 07-04, e7e0a08 vom 06-24) sind alle `failure` [FACT] | mypy bricht ab: `numpy/__init__.pyi:737: Type statement is only supported in Python 3.12 and greater` — ungepinnte neueste numpy-Stubs nutzen PEP-695-`type`-Statements, mypy läuft mit `python_version = "3.10"`; der Override `follow_imports = "skip"` (aus PR #271) verhindert das Parsen der Stubs nicht. Der Job läuft nur bei Push-Events (`if: github.event_name != 'pull_request'`) und ist daher auf PR-Checks unsichtbar — **stiller roter Zustand** |
| `make verify-js` | nicht lokal ausgeführt (kein JS in diesem Pass geändert); auf den grünen PRs #267/#272 lief `workspace` erfolgreich → Workspace-Wiring auf main intakt (Einschätzung auf CI-Basis) | ci-js-workspace Checks |
| HMAC-Status | nicht geprüft (kein Secret in dieser Umgebung); Verhalten wie in CLAUDE.md dokumentiert (UNSIGNED-Modus lokal) | — |

---

## Risks

0. **P0/P1 — Push-CI auf main still rot**: der `ci.yml`-verify-Job (ruff+mypy) schlägt
   auf jedem Push fehl (mypy vs. neueste numpy-Stubs, s. §5) und ist auf PRs per
   Design ausgeblendet — Regressionen im Lint/Type-Gate fallen derzeit nicht auf.
   Fix-Kandidaten (separater Mini-PR): numpy in `requirements-dev.txt` pinnen
   **oder** mypy-Override für numpy auf `ignore_errors`/`--exclude` erweitern.
1. **P1 — undici-High-Vuln** hält den Security-Audit-Workflow auf main dauerhaft rot
   und maskiert künftige echte Findings. Fix: `pnpm.overrides` für `undici >= 6.27.0`
   oder electron-builder-Kette aktualisieren (separater, getesteter PR).
2. **P1 — Dependabot/pnpm-Mismatch**: solange `directory: "/ui-app"` konfiguriert
   ist, bleibt jeder npm-Bot-PR rot (Dauerrauschen, Gewöhnung an rote Checks).
3. **P2 — VOIDMAP-UI-Drift**: der VOIDMAP-Explorer zeigt 9 VOIDs nicht an;
   `verify-governance` bleibt rot, ist aber nicht CI-gated → Drift fällt nur
   manuell auf.
4. **P2 — Merge-Risiko Dependabot-Majors** (#245 eslint, #275 @types/node): nicht
   ohne `verify-js` und explizite Notiz mergen; #245 kollidiert mit bewusster
   ESLint-9-Stabilisierung.
5. **Kein Claim/Evidence-Mismatch** in WELCOME/README/Policies gefunden; Lizenz-
   und Anti-Capture-Formulierungen sind korrekt als Governance-Position markiert.

## Actions Taken

- [x] `docs/voids_backlog.md` mit `tools/voids_backlog_gen.py` regeneriert
      (auto-generierte Datei; Quelle `VOIDMAP.yml` unangetastet) → voids-backlog-check grün.
- [x] Diesen Hygiene-Report erstellt (`docs/audit/2026-07-04_repo_hygiene_report.md`).

## Actions Not Taken (bewusst)

- Keine Branches gelöscht (nur Kandidatenliste, §3).
- Keine PRs gemerged, geschlossen oder rebased.
- Keine Issues geschlossen oder erstellt.
- Keine Lizenzentscheidung getroffen.
- Keine Änderungen an WELCOME.md/README.md (nicht nötig).
- Keine Dependency-Upgrades (undici-Fix nur als Empfehlung dokumentiert).
- Kein Fix am UI-Mirror `voidmap-parser.ts` (TS-Code, gehört in eigenen PR mit `verify-js`).
- Keine Dependabot-Konfigurationsänderung (empfohlen als separater Mini-PR).
- Keine konzeptuelle Expansion, kein verifyLedger-/Cockpit-/MaterialPointer-Bau.

## Offene Punkte

- [ ] ☐ Human Decision: Dependabot-npm auf Root-Directory umstellen + PRs recreaten
- [ ] ☐ Human Decision: undici-Override oder electron-builder-Bump (Security, P1)
- [ ] ☐ Human Decision: #267/#272 nach Branch-Update mergen
- [ ] ☐ Human Decision: #245 Major ignorieren oder geplanter ESLint-10-Umstieg
- [ ] ☐ Human Decision: Branch-Löschkandidaten aus §3 bestätigen
- [ ] ☐ Human Decision: `phase0/foundation-pack` Archiv-Strategie (Tag statt Branch?)
- [ ] ☐ UI-Mirror-Sync `voidmap-parser.ts` (eigener PR, `verify-js`)
- [ ] ☐ Issue #278 Checkliste als Cleanup-PR
- [ ] ☐ Optional: verify-governance in CI verdrahten (sonst bleibt Drift unsichtbar)

## Recommended Next Steps

**P0:**
- `ci.yml`-verify-Job (Push) auf main entröten: mypy/numpy-Stub-Konflikt fixen
  (numpy-Pin oder mypy-Override erweitern; Mini-PR). Kern-Membran `make verify`
  ist davon unabhängig und lokal grün — aber ein still roter Push-Gate maskiert
  echte Lint-/Type-Regressionen.

**P1:**
1. Mini-PR: `dependabot.yml` npm-Ökosystem auf `directory: "/"` → 4 npm-PRs recreaten.
2. Mini-PR: `pnpm.overrides` undici ≥ 6.27.0 (mit `verify-js`) → Security-Audit wieder grün.
3. #272 (und nach kurzem Blick #267) Branch aktualisieren und mergen.

**P2:**
4. Branch-Cleanup gemäß §3 nach menschlicher Bestätigung (8 safe candidates).
5. Issue #278 als Cleanup-PR abarbeiten; #226 schließen oder aktualisieren.
6. UI-Mirror-Sync + optional CI-Verdrahtung von `verify-governance`.
7. Danach (separat, wie geplant): verifyLedger / Tamper-Drills / typed Material —
   nur als Vorschlag, nicht Teil dieses Passes.

## Final Status

**WARN** — Kern ist stabil (lokales `make verify` grün, PR-Gating-Workflows grün,
Onboarding-Docs sauber und ohne Überclaims), aber: `ci.yml`-Push-Verify auf main
still rot (mypy/numpy), Security-Audit auf main rot (undici high), 4 Dependabot-PRs
strukturell unmergebar (Konfig-Mismatch), VOIDMAP-UI-Drift offen.
Alles Genannte ist mit kleinen, getrennten PRs behebbar.

## Artefakte

- `docs/audit/2026-07-04_repo_hygiene_report.md` (dieser Report)
- `docs/voids_backlog.md` (regeneriert aus `VOIDMAP.yml`)
