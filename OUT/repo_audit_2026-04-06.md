# Report: Repository Audit — EntaENGELment

**Datum:** 2026-04-06  
**Fokus:** Vollständiger Repo-Audit (CI/CD, Deps, Struktur, VOIDs, PRs)  
**Branch:** claude/repo-audit-analysis-oiW6K  
**Autor:** Claude (claude-sonnet-4-6)  
**Basis-Commit:** abc12d5 (HEAD auf `main`)

---

## Executive Summary

EntaENGELment ist ein governance-first Forschungsprototyp mit solider CI-Infrastruktur (11 Workflows,
4-stufige Pipeline, DeepJump Protocol v1.2, HMAC-Receipts). Der aktuelle Zustand zeigt:

- **3 kritische/hohe CI-Blocker**, die vor dem nächsten Merge oder RC-Tag behoben werden sollten
- **5 offene Dependabot-PRs mit MAJOR-Versionssprüngen** (Next.js 14→16, TypeScript 5→6, React 18→19,
  Tailwind 3→4) — keine automatische Mergebarkeit ohne Tests
- **1 ungemergter claude-PR (#150)** mit korrekten Fixes seit 2026-04-04
- **2 VOIDs IN_PROGRESS** (VOID-010, VOID-011) mit realistischen Deadlines (2026-06-01)
- **7 veraltete Remote-Branches** ohne aktive PRs
- **Governance-Layer ist strukturell intakt** — GOLD/IMMUTABLE-Dateien unverändert

Keine Befunde zu Sicherheitslücken in Secrets-Handling oder Injection-Risiken im aktuellen Stand.

---

## Befunde (nach Priorität)

---

### F-01 — `safety check --stdin --json` veraltet

| Feld | Wert |
|------|------|
| **Priorität** | KRITISCH |
| **Status** | OFFEN |
| **Betroffene Datei** | `.github/workflows/ci.yml` (Zeile 131) |
| **Risiko** | CI Security-Stage schlägt fehl bei `safety` v3+ |

**Evidenz:**
```yaml
# ci.yml, Stage 3 (Security):
pip freeze | safety check --stdin --json
```
In `safety` v3+ (aktuell v3.x) wurde `--stdin` entfernt. Der korrekte Befehl lautet:
`safety scan` (mit API-Key oder `--policy-file`). Der `check`-Subcommand ist deprecated.

**Auswirkung:** Der Security-Scan in Stage 3 schlägt fehl → CI blockiert nach `build`. Falls
`continue-on-error` nicht gesetzt ist, werden alle nachgelagerten Stages (gate-policy) nie ausgeführt.
Kein `continue-on-error` in diesem Schritt.

**Empfehlung:**
```yaml
# Option A: safety scan (v3+)
- name: Check dependencies for vulnerabilities
  run: safety scan --policy-file .safety-policy.yaml
  continue-on-error: true  # bis API-Key-Setup

# Option B: pip-audit als Ersatz (kein API-Key nötig)
- name: Check dependencies for vulnerabilities
  run: |
    pip install pip-audit
    pip-audit -r requirements.txt
```

---

### F-02 — test.yml triggert auf nicht-existente Branches (master, develop)

| Feld | Wert |
|------|------|
| **Priorität** | HOCH |
| **Status** | IN ARBEIT (PR #150 offen seit 2026-04-04) |
| **Betroffene Datei** | `.github/workflows/test.yml` (Zeilen 4–7) |
| **Risiko** | Stale-Trigger erzeugen false positives / Verwirrung |

**Evidenz:**
```yaml
# test.yml:
on:
  push:
    branches: [main, master, develop]   # ← master, develop existieren nicht
  pull_request:
    branches: [main, master, develop]   # ← master, develop existieren nicht
```
Aktive Remote-Branches laut `git branch -a`: nur `main` und `claude/*`-Branches.

**Auswirkung:** Keine unmittelbare Blockade, aber die Trigger sind irreführend. Zudem
läuft test.yml mit `Fractalsense/`-Tests, ci.yml mit `tests/unit|integration|ethics/` — zwei
parallele, nicht abgestimmte Test-Suites.

**Empfehlung:** PR #150 (`claude/add-ui-build-check-and-clean-test-triggers`) enthält den
korrekten Fix. Dieser PR sollte zeitnah gemergt werden.

---

### F-03 — Duale Test-Infrastruktur ohne klare Abgrenzung

| Feld | Wert |
|------|------|
| **Priorität** | HOCH |
| **Status** | OFFEN |
| **Betroffene Dateien** | `ci.yml`, `test.yml` |
| **Risiko** | Unklar welche Tests die Coverage-Baseline abdecken |

**Evidenz:**

| Workflow | Python-Tests | Pfad |
|----------|-------------|------|
| `ci.yml` | pytest | `tests/unit/`, `tests/integration/`, `tests/ethics/` |
| `test.yml` | pytest | `Fractalsense/` (anderer requirements-Pfad: `Fractalsense/requirements-dev.txt`) |

Die beiden Pipelines installieren unterschiedliche Dependencies, laufen in unterschiedlichen
Working-Directories, und messen unterschiedliche Coverage. Das Coverage-Badge auf main
reflektiert nur `ci.yml`-Ergebnisse — `test.yml` Coverage wird nicht zusammengeführt.

**Auswirkung:** `Fractalsense/`-Coverage wird in der Gesamtbaseline nicht berücksichtigt.
Entwickler, die nur `test.yml` vertrauen, sehen ein unvollständiges Bild.

**Empfehlung:** Entweder Konsolidierung in eine Workflow-Datei mit separaten Jobs, oder
explizite Dokumentation der Abgrenzung (welche Suite testet was). Ein gemeinsames
`coverage.xml`-Merge-Schritt würde das Problem technisch lösen.

---

### F-04 — 5 MAJOR-Versionssprünge in offenen Dependabot-PRs

| Feld | Wert |
|------|------|
| **Priorität** | HOCH |
| **Status** | OFFEN (PRs #152–156 seit 2026-04-06) |
| **Betroffene Dateien** | `ui-app/package.json` |
| **Risiko** | Breaking Changes bei blindem Merge |

**Offene Dependabot-PRs:**

| PR | Paket | Von → Nach | Art |
|----|-------|-----------|-----|
| #156 | next | 14.2.21 → **16.2.2** | MAJOR (2 Versionen) |
| #155 | typescript | 5.9.3 → **6.0.2** | MAJOR |
| #154 | react-dom + @types/react-dom | 18.3.1 → **19.2.4** | MAJOR |
| #153 | tailwindcss | 3.4.19 → **4.2.2** | MAJOR |
| #152 | eslint-config-next | 16.2.1 → 16.2.2 | PATCH |

**Auswirkung:** Next.js 16 hat Routing-Breaking-Changes (App Router), TypeScript 6 hat
strictness-Änderungen, React 19 hat Breaking API-Changes (concurrent features), Tailwind 4
hat komplett neue Konfigurations-Syntax (kein tailwind.config.js mehr).

**Empfehlung:**
- PR #152 (patch): Kann gemergt werden.
- PRs #153–#156: Require dedicated upgrade branch mit manueller Migration + `npm run build`-Überprüfung.
  Nicht via Dependabot-Auto-Merge. Sequentiell testen (Tailwind vor Next.js, da Next.js-Config Tailwind referenziert).
- PR #150 (ci-fix) **zuerst mergen**, damit test.yml den `ui-build`-Check hat.

---

### F-05 — codecov-action Version-Drift (v5.5.2 in ci.yml, v6.0.0 in PR #151)

| Feld | Wert |
|------|------|
| **Priorität** | MITTEL |
| **Status** | OFFEN (PR #151 seit 2026-04-06) |
| **Betroffene Datei** | `.github/workflows/ci.yml` (Zeile 90) |
| **Risiko** | node24-Inkompatibilität bei v5 in neueren GH-Action-Runner |

**Evidenz:**
```yaml
# ci.yml, aktuell:
uses: codecov/codecov-action@671740ac38dd9b0130fbe1cec585b89eea48d3de  # v5.5.2
```
PR #151 will auf v6.0.0 bumpen. v6.0.0 führt node24-Support ein — das ist ein
Breaking Change für Setups die explizit node20 erwarten.

**Empfehlung:** PR #151 reviewen. Der Schritt hat `continue-on-error: true`, daher kein
unmittelbarer CI-Blocker. Testen nach Merge ob Coverage-Upload noch funktioniert.

---

### F-06 — Kein Branch-Protection auf `main`

| Feld | Wert |
|------|------|
| **Priorität** | MITTEL |
| **Status** | OFFEN |
| **Evidenz** | GitHub API: `"protected": false` für alle Branches inkl. `main` |
| **Risiko** | Direktes Pushen auf main ohne CI möglich |

**Auswirkung:** Die gesamte CI/CD-Governance (DeepJump Protocol, Gate Checks, Metatron Guard)
kann umgangen werden durch direktes `git push origin main`.

**Empfehlung:** Branch Protection Rule auf `main` aktivieren:
- Required status checks: `all-checks-passed` (ci.yml), `metatron-pr-check`
- Require PR reviews: 1 Reviewer
- Restrict who can push: nur @fleksible

---

### F-07 — VOID-014 mit undokumentiertem Status `SUSPENDED`

| Feld | Wert |
|------|------|
| **Priorität** | MITTEL |
| **Status** | HINWEIS |
| **Betroffene Datei** | `VOIDMAP.yml` (VOID-014) |

**Evidenz:**
```yaml
- id: VOID-014
  status: SUSPENDED   # ← nicht im Template definiert (nur OPEN/IN_PROGRESS/CLOSED)
```
Das VOIDMAP-Template kennt nur `OPEN | IN_PROGRESS | CLOSED`. `SUSPENDED` ist
semantisch sinnvoll aber nicht schematisiert.

**Auswirkung:** Der Gate-5-Check in `release.yml` prüft nur `OPEN` und `IN_PROGRESS` auf
Owner-Vollständigkeit. `SUSPENDED` wird nicht validiert. Kein unmittelbares Risiko,
aber mögliche Konsistenzprobleme bei zukünftigen VOIDMAP-Tools.

**Empfehlung:** `SUSPENDED` explizit in den VOIDMAP-Header als gültigen Status aufnehmen:
```yaml
# Status: OPEN | IN_PROGRESS | CLOSED | SUSPENDED
```
VOID-014 hat keinen Owner — prüfen ob das per Design oder Versehen ist.

---

### F-08 — RC Preflight-Checkliste komplett offen

| Feld | Wert |
|------|------|
| **Priorität** | MITTEL |
| **Status** | OFFEN |
| **Betroffene Datei** | `docs/release/RC_PRECHECK_v0.1.0-rc1.md` |

**Evidenz:** Alle Checkboxen in der RC-Preflight-Checkliste sind noch `[ ]`.
Status-Marker: `Draft checklist`.

**Auswirkung:** v0.1.0-rc1 ist offiziell nicht release-ready. Vor dem Taggen sollten
mindestens Punkte B (technische Gate-Checks) vollständig abgehakt sein.

**Empfehlung:** Gate-Checks lokal oder in CI durchlaufen, Checkliste aktualisieren,
CHANGELOG.md `Unreleased`-Sektion für RC befüllen.

---

### F-09 — 7 veraltete Remote-Branches ohne offene PRs

| Feld | Wert |
|------|------|
| **Priorität** | NIEDRIG |
| **Status** | OFFEN |
| **Risiko** | Repo-Hygiene, Orientierungsverlust |

**Veraltete Branches:**

| Branch | Typ | Letzter relevanter Merge |
|--------|-----|--------------------------|
| `claude/align-coverage-policy` | claude | Gemergt als PR #149 |
| `claude/analyze-repo-essence-LKgK4` | claude | Gemergt als PR #141 |
| `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D` | claude | Unklar |
| `claude/repo-maintenance-consolidation-LA2ek` | claude | Unklar |
| `codex/update-markdown-file-in-repository` | codex | Unklar |
| `codex/update-readme-for-deepjump-integration` | codex | Unklar |
| `phase0/foundation-pack` | phase | Historisch |

**Empfehlung:** Nach G3-Prinzip: nicht löschen ohne Verifikation. Prüfen ob jeder Branch
einen zugehörigen gemergten PR hat. Dann via GitHub UI als "deleted" markieren (reversibel).

---

### F-10 — Root-Level-Artefakte (mögliche Legacy-Dateien)

| Feld | Wert |
|------|------|
| **Priorität** | NIEDRIG |
| **Status** | HINWEIS |

**Artefakte ohne klare Zugehörigkeit:**

| Datei | Größe | Indiz |
|-------|-------|-------|
| `Index.html` | 49 KB | Standalone HTML ohne Build-Pfad |
| `main.js` | 605 B | Root-JS neben Next.js ui-app/ |
| `metrics` | 1 B | Leere Datei, kein Verzeichnis |
| `REFACTOR_NOTES.md` | 4.3 KB | Undatiert, kein Verweis in README |
| `hardware_requirements_summary.md` | 7.3 KB | Kein VOID-Bezug erkennbar |
| `REPOSITORY_ESSENZ_ANALYSE.md` | 30 KB | Ältere Analyse, ggf. durch diesen Report überholt |

**Empfehlung:** Keine sofortige Aktion (G3: Deletion-Verbot). Klären ob in VOIDMAP oder
docs/ referenziert. Falls ungenutzt: nach `NICHTRAUM/archive/` verschieben mit ☐-Marker.

---

### F-11 — VOIDMAP.yml last_updated veraltet

| Feld | Wert |
|------|------|
| **Priorität** | NIEDRIG |
| **Status** | HINWEIS |
| **Betroffene Datei** | `VOIDMAP.yml` (Zeile 18) |

**Evidenz:**
```yaml
metadata:
  last_updated: "2026-04-04"   # Heute ist 2026-04-06
```

**Empfehlung:** `last_updated` nach jeder VOIDMAP-Änderung aktualisieren. Kann in einen
pre-commit-Hook oder das Makefile integriert werden.

---

## VOIDs — Aktueller Stand

| VOID | Titel | Status | Owner | Deadline | Einschätzung |
|------|-------|--------|-------|----------|--------------|
| VOID-001 | DeepJump Protocol | CLOSED | claude-code | — | ✅ Abgeschlossen |
| VOID-002 | CI Pipeline | CLOSED | claude-code | — | ✅ Abgeschlossen |
| VOID-003 | Status Emit Receipt Format | CLOSED | claude-code | — | ✅ Abgeschlossen |
| VOID-010 | Taxonomie & Spektren | IN_PROGRESS | fleks | 2026-06-01 | 🟡 Forschungs-VOID, realistisch |
| VOID-011 | Metriken der Resonanz | IN_PROGRESS | fleks | 2026-06-01 | 🟡 Stubs gefixt, toy-Dataset ausstehend |
| VOID-012 | GateProof Checkliste | CLOSED | claude-code | — | ✅ Abgeschlossen |
| VOID-013 | Sensor-Architektur | CLOSED | claude-code | — | ✅ Abgeschlossen |
| VOID-014 | Protein-Design | SUSPENDED | fleks | — | ⚠️ Status undokumentiert, kein Owner |
| VOID-020 | Port-Matrix Suite | CLOSED | — | — | ✅ Abgeschlossen |
| VOID-021 | Port-Codebooks | CLOSED | — | — | ✅ Abgeschlossen |
| VOID-022 | Flood-Guard Threshold | CLOSED | — | — | ✅ Abgeschlossen |
| VOID-023 | MICRO/MESO/MACRO Tagging | CLOSED | claude-code | — | ✅ Abgeschlossen |

**Offene Punkte zu VOIDs:**
- VOID-011: `SIMULATION_PROXY`-Claim-Tagging und toy_resonance_dataset-Erweiterung ausstehend
- VOID-014: `SUSPENDED` in Template dokumentieren; Owner-Feld klären

---

## Branches & PRs — Aktueller Stand

### Offene PRs (7)

| PR | Titel | Branch | Labels | Empfehlung |
|----|-------|--------|--------|------------|
| #156 | bump next 14→16 | dependabot/…/next | dependencies | ⛔ MAJOR — manuelle Migration erforderlich |
| #155 | bump typescript 5→6 | dependabot/…/typescript | dependencies | ⛔ MAJOR — manuelle Migration erforderlich |
| #154 | bump react-dom 18→19 | dependabot/…/multi | dependencies | ⛔ MAJOR — manuelle Migration erforderlich |
| #153 | bump tailwindcss 3→4 | dependabot/…/tailwindcss | dependencies | ⛔ MAJOR — manuelle Migration erforderlich |
| #152 | bump eslint-config-next patch | dependabot/…/eslint-config-next | dependencies | ✅ Sicher zu mergen |
| #151 | bump codecov-action v5→v6 | dependabot/…/codecov | dependencies | 🟡 Testen nach Merge |
| #150 | ci: add ui-build, remove stale triggers | claude/add-ui-build-check... | — | ✅ Priorität: zeitnah mergen |

### Empfohlene Merge-Reihenfolge
1. PR #150 (CI-Fix, keine Breaking Changes)
2. PR #152 (eslint-config-next patch)
3. PR #151 (codecov nach Testing)
4. PRs #153–156 nur nach dedizierter UI-Upgrade-Branch mit vollständigem Build-Test

---

## Nächste sinnvolle Updates

Priorität | Maßnahme | Aufwand
----------|----------|--------
🔴 KRITISCH | F-01: `safety check` ersetzen durch `pip-audit` oder `safety scan` in ci.yml | 5 min
🔴 KRITISCH | F-02: PR #150 mergen (stale triggers + ui-build-check) | review only
🟠 HOCH | F-03: Test-Infrastruktur dokumentieren (ci.yml vs test.yml Scope-Abgrenzung) | 15 min
🟠 HOCH | F-04: Dependabot MAJOR-PRs (#153–156) auf separate Upgrade-Branch auslagern | 2–4h je Paket
🟡 MITTEL | F-06: Branch Protection für `main` aktivieren (GitHub Settings) | 10 min
🟡 MITTEL | F-07: `SUSPENDED` in VOIDMAP-Header dokumentieren | 2 min
🟡 MITTEL | F-08: RC Preflight-Checks durchführen und Checkliste abhaken | 30 min
🟢 NIEDRIG | F-09: Veraltete Branches nach Verifikation schließen | 20 min
🟢 NIEDRIG | F-10: Root-Level-Artefakte per G3-Prozess klären/archivieren | 1h
🟢 NIEDRIG | F-11: VOIDMAP last_updated in Makefile/pre-commit integrieren | 5 min

---

## Kompakttabelle Befunde

| ID | Bereich | Titel | Prio | Status |
|----|---------|-------|------|--------|
| F-01 | CI/Security | `safety check --stdin` deprecated | KRITISCH | OFFEN |
| F-02 | CI/Trigger | test.yml stale branches (master/develop) | HOCH | IN ARBEIT (PR #150) |
| F-03 | CI/Tests | Duale Test-Infrastruktur ohne Abgrenzung | HOCH | OFFEN |
| F-04 | Deps | 5 MAJOR-Versionssprünge in ui-app | HOCH | OFFEN |
| F-05 | CI/Actions | codecov-action v5→v6 (node24) | MITTEL | OFFEN (PR #151) |
| F-06 | Security | Kein Branch-Protection auf main | MITTEL | OFFEN |
| F-07 | Governance | VOID-014 Status `SUSPENDED` undokumentiert | MITTEL | HINWEIS |
| F-08 | Release | RC Preflight komplett offen | MITTEL | OFFEN |
| F-09 | Hygiene | 7 veraltete Remote-Branches | NIEDRIG | OFFEN |
| F-10 | Hygiene | Root-Level Legacy-Artefakte | NIEDRIG | HINWEIS |
| F-11 | Governance | VOIDMAP last_updated veraltet | NIEDRIG | HINWEIS |

---

## Nicht getan

- Kein Ausführen von CI-Tools oder Tests
- Keine Änderung an GOLD-Dateien (index/, policies/, VOIDMAP.yml)
- Keine Änderung an IMMUTABLE-Receipts
- Keine Einschätzung zu Laufzeit-Korrektheit von src/core/metrics.py (VOID-011)
- Kein Vergleich mit vorherigen Audit-Reports aus docs/audit/ (OUT/OPERATIVE_WORKPACKAGE_20260317.md als Vorläufer gesichtet)

## Artefakte

- `OUT/repo_audit_2026-04-06.md` (dieser Report)
- Vorläufer: `OUT/OPERATIVE_WORKPACKAGE_20260317.md` (2026-03-17)

---

*Letzte Aktualisierung: 2026-04-06*
