# Security Posture Baseline — entaENGELment-

**Datum:** 2026-06-16
**Fokus:** Security-Posture sichtbar machen (Read-Only Baseline)
**Branch:** `chore/security-posture-baseline`
**Basis-HEAD:** `3fefe82` (main nach PR #252, #253)

> Zielsatz: Dieser PR behauptet keine Sicherheit, sondern macht sichtbar, welche
> Membranen bereits tragen — und welche nur als **offene Toggles außerhalb des
> Repo-Codes** markiert sind. Anti-F7: keine unmarkierte falsche Sicherheit.

---

## 0. Claim-Disziplin

- **[FAKT]** verifizierbar aus Repo-Dateien / CI-Konfiguration.
- **[INFERENZ]** abgeleitet, nicht direkt gemessen.
- **[MODELL]** Deutung / Empfehlung.
- **[HYPOTHESE]** Erwartung, unbelegt.

**Limitierung:** Repo-/Org-**Settings** (Branch-Protection, Secret-Scanning,
Dependabot-Alerts/Security-Updates, „allow auto-merge", Code-Scanning-Aktivierung)
sind **nicht** aus dem Dateibaum verifizierbar und konnten in diesem Read-Only-Lauf
**nicht** bestätigt werden. Sie sind unten als **OFFENER TOGGLE** markiert. **[FAKT]**

---

## 1. Was bereits trägt (dateibasiert verifizierbar)

| # | Mechanismus | Beleg | Status |
|---|-------------|-------|--------|
| S1 | Dependency-Audit (JS+Py), blockierend ab `high` | `.github/workflows/security-audit.yml` (`pnpm audit --audit-level=high`, `pip-audit`) | [FAKT] aktiv |
| S2 | Dependabot Version-Updates (pip, npm `/ui-app`, github-actions) | `.github/dependabot.yml` | [FAKT] konfiguriert |
| S3 | SBOM-Generierung | `.github/workflows/sbom.yml` | [FAKT] aktiv |
| S4 | Static-Security-Lint (Python) | `bandit` in `ci.yml` `security`-Job, `.bandit.yaml` | [FAKT] aktiv |
| S5 | Actions auf **SHA gepinnt** | z. B. `actions/checkout@df4cb1c…`, `setup-node@48b55a…` | [FAKT] durchgehend |
| S6 | Minimale Workflow-Permissions + Concurrency | alle 13 Workflows; `tools/workflow_posture_check.py` (13/13 PASS) | [FAKT] erzwungen lokal |
| S7 | Nur 2 Workflows mit Schreibrecht, dokumentiert | `release.yml` (`contents: write`), `void-sync.yml` (`issues: write`) in `docs/ci/WORKFLOW_MAP.md` | [FAKT] |
| S8 | Pre-commit-Guards | `.githooks/pre-commit`, `make install-hooks` | [FAKT] vorhanden (opt-in) |
| S9 | Security-Policy | `SECURITY.md` | [FAKT] vorhanden |
| S10 | HMAC-signierte Status-Receipts | `tools/status_emit.py`, `tools/status_verify.py` | [FAKT] vorhanden |

**[INFERENZ]** Die dateibasierte Supply-Chain-/CI-Membran ist für ein Repo dieser
Größe überdurchschnittlich gehärtet.

---

## 2. Fehlende dateibasierte Bausteine

| # | Lücke | Wirkung | Empfehlung |
|---|-------|---------|------------|
| G1 | **Kein CodeQL / Code Scanning** | Keine semantische Schwachstellenanalyse (SAST über Datenfluss) | Code Scanning aktivieren — siehe §4 + ADR-0003 |
| G2 | SHA-Pin-Invariante nicht maschinell geprüft | Drift möglich (neue Workflows mit Tag-Pins) | optionaler advisory Lint (Roadmap §4) |

**[FAKT]** Erkannte Sprachen (für Code Scanning relevant): Python (99 `*.py`),
JavaScript/TypeScript (28 `*.ts/tsx`, 18 `*.js/jsx`; Next.js `ui-app`, `packages/*`).
CodeQL-Zielsprachen wären `python` und `javascript-typescript`.

---

## 3. OFFENE TOGGLES — Repo-Settings (NICHT dateibasiert; deine Hand)

> **[FAKT]** Diese Punkte sind **keine** Dateiänderungen und konnten hier **nicht**
> verifiziert werden. Sie müssen in den GitHub-Repo-Settings geprüft/aktiviert
> werden. Status hier = **UNBEKANNT/OFFENER TOGGLE**, nicht „erledigt".

| # | Toggle | Wo | Empfohlener Zielzustand |
|---|--------|----|--------------------------|
| T1 | **Branch Protection / Ruleset für `main`** | Settings → Rules/Branches | keine Force-Pushes; keine Deletion; required status checks; required PR review | 
| T2 | **Required status checks** auf `main` | Ruleset | mind. DeepJump CI, Tests, Smoke, Policy Lint, Metatron Guard |
| T3 | **Secret Scanning** (+ Push Protection) | Settings → Code security | aktiv |
| T4 | **Dependabot Alerts** | Settings → Code security | aktiv (Voraussetzung für T5) |
| T5 | **Dependabot Security Updates** | Settings → Code security | aktiv (öffnet PRs für patchbare Alerts) |
| T6 | **Code Scanning Aktivierung** | Settings → Code security | Default Setup (empfohlen) oder Advanced (ADR-0003) |
| T7 | **Allow auto-merge** | Settings → General | **bewusst NICHT jetzt** (siehe §5) |

**Checkliste zum Abhaken (durch dich):**

- [ ] ☐ T1 Branch-Ruleset `main`: Force-Push aus, Deletion aus
- [ ] ☐ T2 Required checks gesetzt
- [ ] ☐ T3 Secret Scanning + Push Protection aktiv
- [ ] ☐ T4 Dependabot Alerts aktiv
- [ ] ☐ T5 Dependabot Security Updates aktiv
- [ ] ☐ T6 Code Scanning aktiviert (Default Setup oder ADR-0003-Workflow)
- [ ] ☐ T7 Auto-Merge: **bleibt aus** (eigener späterer Entscheid)

---

## 4. Code Scanning — empfohlener Weg

**[MODELL]** Zwei dokumentierte Pfade (Details + Workflow-Vorlage in ADR-0003):

1. **Default Setup (empfohlen, wartungsarm):** in den Repo-Settings aktivieren.
   GitHub wählt Sprachen/Queries automatisch, läuft auf Push/PR + Zeitplan. Kein
   Action-Pinning, keine Workflow-Pflege.
2. **Advanced Setup (versioniert):** committete `.github/workflows/codeql.yml` mit
   minimalen Permissions. Mehr Kontrolle, aber: **`github/codeql-action` muss auf
   einen aktuellen Release-SHA gepinnt** werden, um die Repo-SHA-Pin-Invariante zu
   wahren.

**[FAKT] Bewusste Entscheidung dieses PRs:** Es wird **keine aktive `codeql.yml`
committet**, weil ein aktueller `github/codeql-action`-SHA in dieser Read-Only-
Umgebung **nicht verifizierbar** ist. Einen SHA zu raten wäre falsche Sicherheit
(Anti-F7). Die Advanced-Vorlage liegt in ADR-0003 mit explizitem Pin-Hinweis;
primär empfohlen ist Default Setup (T6).

---

## 5. Auto-Merge — bewusst nicht jetzt

**[FAKT]** Dieser PR aktiviert **kein** Auto-Merge und ändert `dependabot.yml` nicht.
**[MODELL]** Empfehlung für einen späteren, eigenen Entscheid: höchstens
*patch-only* Dependabot-Auto-Merge unter grüner CI, niemals Major/Minor, keine
neuen Dependencies, keine Workflow-/Permission-Änderungen ohne Review.

---

## 6. Offene Risiken

- **[FAKT]** Settings-Toggles (§3) sind unverifiziert — Posture ist nur so stark
  wie deren tatsächlicher Zustand. Dieser Bericht behauptet sie **nicht** als aktiv.
- **[HYPOTHESE]** Ohne Branch-Protection auf `main` sind direkte Pushes/Force-Pushes
  technisch möglich; Auswirkung abhängig vom realen Settings-Stand.
- **[FAKT]** Dependabot meldete beim Push 4 Advisories auf dem Default-Branch
  (2 high, 1 moderate, 1 low) — sichtbar in der GitHub-Security-Übersicht; deren
  Behebung ist ein eigener Vorgang (nicht Teil dieses Baseline-PRs).

---

## 7. Nächste Schritte (separiert)

1. Settings-Toggles §3 durch dich; danach Checkliste abhaken.
2. Code Scanning aktivieren (Default Setup empfohlen).
3. Später eigener PR/Entscheid: Dependabot patch-only Auto-Merge unter grüner CI.
4. Optional: advisory SHA-Pin-Lint (Roadmap).

## 8. Artefakte

- `docs/audit/security_posture_baseline_2026-06-16.md` (dieser Bericht)
- `docs/decisions/ADR-0003-security-baseline-and-code-scanning.md`
