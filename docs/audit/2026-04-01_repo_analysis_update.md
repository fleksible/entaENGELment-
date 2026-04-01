# Repository-Analyse & Wartungsbericht

**Datum:** 2026-04-01
**FOKUS:** Repo-Analyse → Befunde aktualisieren
**Autor:** Claude (Repository-Analyse-Agent)
**Branch:** `claude/analyze-github-repo-Zu9yf`
**Basis:** Vollständiger Repository-Scan (April 2026)
**Vorgänger-Audits:** `docs/audit/AUDIT_SUMMARY.md` (2026-01-24), `OUT/OPERATIVE_WORKPACKAGE_20260317.md` (2026-03-17)
**Claim-Status:** Alle Befunde basieren auf belegten Beobachtungen. Unsicherheiten explizit markiert.

---

## Executive Summary

Das Repository ist ein reifer Forschungsprototyp mit starker Governance-Schicht (Guards G0–G6, HMAC-Receipts, DeepJump-Protokoll). Seit dem letzten Audit (Jan 2026) und dem Operativen Arbeitspaket (März 2026) wurden **wesentliche Fortschritte** erzielt:

**Erledigt:**
- MI/FD-Metriken implementiert (nicht mehr Stubs) — Commit `d213e97`
- 8 VOIDs geschlossen (001–003, 012–013, 020–023)
- CI-Actions SHA-gepinnt und Versionen aktualisiert — Commit `333c634`
- HMAC-Secret fail-fast erzwungen (kein ephemeral Fallback mehr) — Commit `007566b`
- Dependabot aktiv für pip, npm, github-actions
- Pre-Commit-Hook eingerichtet — Commit `878f12c`
- Release-Workflow mit 7 Gates implementiert
- SBOM-Workflow hinzugefügt
- `pdf canvas/` Verzeichnis bereinigt

**Weiterhin offen (kritisch):**
- `NICHTRAUM/` existiert immer noch nicht (G2 nicht durchsetzbar)
- 59 Dateien ohne G1-Kategorie, kein `annex_check.py`
- Kein einziger Git-Tag/Release (v0.1.0 nur in CHANGELOG)
- Coverage-Widerspruch: CONTRIBUTING.md sagt 70%, CI erzwingt 50%

**Neu identifiziert:**
- Next.js Major-Upgrade 14 zu 16 ohne Build-Check in CI
- @types/node Major-Upgrade 20 zu 25
- adapters/ weiterhin Stub-only

---

## 1. Befunde-Tabelle (Kompakt)

| # | Befund | Prio | Status | Evidenz | Empfehlung |
|---|--------|------|--------|---------|------------|
| F-01 | NICHTRAUM/ nicht materialisiert | P0 | **offen** | `ls NICHTRAUM/` nicht vorhanden; G2 in CLAUDE.md definiert | Verzeichnisse + .gitkeep erstellen |
| F-02 | 59 Dateien ohne G1-Kategorie | P0 | **offen** | Kein `policies/annex_map.yaml`, kein `tools/annex_check.py` | annex_map.yaml + CI-Check erstellen |
| F-03 | Coverage-Widerspruch (70% vs 50%) | P1 | **offen** | CONTRIBUTING.md:40 sagt >=70%; ci.yml:100 `--fail-under=50` | Angleichen auf einheitlichen Wert |
| F-04 | Kein Git-Tag/Release v0.1.0 | P1 | **offen** | `git tag -l` leer; CHANGELOG nennt 0.1.0 als Unreleased | Tag erstellen, Release-Workflow testen |
| F-05 | VOID-010 ueberfaellig | P1 | **offen** | target_date: 2026-03-15, status: OPEN | Literaturbelege oder Deadline verlaengern |
| F-06 | VOID-011 Metriken teilweise umgesetzt | P1 | **in Arbeit** | MI/FD implementiert (d213e97), toy_resonance_dataset minimal | toy_resonance_dataset erweitern, Tests |
| F-07 | Metatron-Amnesty nicht in CI kodiert | P2 | **offen** | metatron-guard.yml prueft FOKUS, keine Merge-Commit-Exemption | Regex-Exemption fuer Merge-Commits |
| F-08 | Keine E2E-Demo (make demo) | P2 | **offen** | Kein `demo`-Target in Makefile | make demo Target erstellen |
| F-09 | Python zu UI Datenbruecke undokumentiert | P2 | **offen** | ui-app/ und src/ parallel ohne API-Spec | API-Spec in docs/api/ erstellen |
| F-10 | VOID-014 schwebt ohne SUSPENDED | P4 | **offen** | VOIDMAP: status OPEN, "safety-bounded" | Als SUSPENDED markieren |
| F-11 | Stub-Metriken (return 0.5) beseitigt | - | **erledigt** | src/core/metrics.py: MI=Histogram, FD=Higuchi, PLV=Einheitskreis | - |
| F-12 | HMAC ephemeral Fallback entfernt | - | **erledigt** | Commit 007566b: fail-fast in CI, Warning nur lokal | - |
| F-13 | CI-Actions SHA-Pinning | - | **erledigt** | ci.yml: checkout@de0fac2e, setup-python, codecov | - |
| F-14 | Dependabot konfiguriert | - | **erledigt** | .github/dependabot.yml: pip+npm+actions, weekly Monday | - |
| F-15 | VOID-012/013 geschlossen | - | **erledigt** | gateproof_v1.yaml, docs/sensors/bom.md, spec/sensors.spec.json | - |
| F-16 | Release-Workflow implementiert | - | **erledigt** | .github/workflows/release.yml mit 7 Gate-Checks | Noch nie ausgeloest (s. F-04) |
| F-17 | Pre-Commit-Hook eingerichtet | - | **erledigt** | Commit 878f12c: .githooks/ mit receipt-lint + claim-lint | - |
| F-18 | pdf canvas/ Verzeichnis bereinigt | - | **erledigt** | Verzeichnis nicht mehr vorhanden | - |
| F-19 | ENTA_HMAC_SECRET in CI | P2 | **unklar** | deepjump-audit.reusable.yml nutzt secrets.ENTA_HMAC_SECRET; ob konfiguriert: nicht pruefbar | Secret-Existenz in GitHub Settings verifizieren |

---

## 2. Detail-Befunde (Top 5 offen)

### F-01: NICHTRAUM/ nicht materialisiert (P0, offen)

**Evidenz:**
- `CLAUDE.md` G2: "NICHTRAUM/ ist ein geschuetzter Bereich fuer Unentschiedenes"
- `.claude/rules/security.md` Quarantine-Prozess verweist auf `NICHTRAUM/quarantine/`
- Workspace Layout in `CLAUDE.md` listet archive/, maybe/, quarantine/
- Filesystem: Verzeichnis existiert nicht

**Auswirkung:**
- G2-Regel ist unausfuehrbar
- Quarantine-Prozess (G5) hat kein Ziel-Verzeichnis
- Governance-Regel ohne Infrastruktur = aspirational, nicht operativ

**Empfehlung:**
```
NICHTRAUM/archive/.gitkeep                    (neu)
NICHTRAUM/maybe/.gitkeep                      (neu)
NICHTRAUM/quarantine/.gitkeep                 (neu)
NICHTRAUM/quarantine/quarantine_log.md        (neu, leeres Template)
```

**Aufwand:** 15 Minuten, rein additiv, kein Risiko
**Seit:** Audit Jan 2026, Workpackage P0-A

---

### F-02: 59 Dateien ohne G1-Kategorie (P0, offen)

**Evidenz:**
- Kein `policies/annex_map.yaml` vorhanden
- Kein `tools/annex_check.py` vorhanden
- `.claude/rules/annex.md` listet Pfad-Tabellen, aber kein maschinenlesbares Mapping
- Deep-Audit Jan 2026: "59 files in UNKNOWN category"

**Auswirkung:**
- G1-Enforcement in CI nicht moeglich
- Neue Contributors koennen Schutzstatus nicht ableiten
- Wachsende Diskrepanz zwischen Regel und Praxis

**Empfehlung:**
1. `policies/annex_map.yaml` mit vollstaendiger Pfad-Kategorie-Zuordnung erstellen
2. `tools/annex_check.py` als CI-Schritt (erst warning-mode, nach Review blocking)
3. Alle existierenden Verzeichnisse klassifizieren

**Aufwand:** 2-3 Stunden
**Seit:** Deep-Audit Jan 2026, Workpackage P0-B

---

### F-03: Coverage-Widerspruch (P1, offen)

**Evidenz:**
- `CONTRIBUTING.md` Zeile 40: "Coverage >= 70% sein"
- `.github/workflows/ci.yml` Zeile 100: `coverage report --fail-under=50`
- `jest.config.js`: Threshold 60% (branches=50%, functions/lines/statements=60%)

**Auswirkung:**
- Inkonsistente Erwartung an Contributors
- CI laesst niedrigere Coverage durch als Docs versprechen
- Vertrauensverlust in Dokumentation

**Empfehlung:**
- Entweder CI auf 70% anheben (wenn realistisch)
- Oder CONTRIBUTING.md auf 50% korrigieren (ehrlicher Ist-Zustand)
- Alle drei Stellen (CONTRIBUTING.md, ci.yml, jest.config.js) synchronisieren

**Aufwand:** 5 Minuten

---

### F-04: Kein Git-Tag/Release (P1, offen)

**Evidenz:**
- `git tag -l` liefert keine Ergebnisse
- `CHANGELOG.md` listet `[0.1.0]` als Unreleased
- `release.yml` existiert mit 7-Gate-Checks, wurde nie ausgeloest
- `docs/governance/RELEASE_PROCESS.md` beschreibt vollstaendigen Prozess

**Auswirkung:**
- Keine reproduzierbare Referenzversion
- Release-Workflow ungetestet (potenzielle Fehler bei erstem Einsatz)
- Kein offizieller Snapshot-Punkt fuer Audits

**Empfehlung:**
1. Zuerst G1-Kategorisierung (F-02) abschliessen
2. v0.1.0-rc1 als Dry-Run-Tag erstellen
3. Release-Workflow einmal vollstaendig durchlaufen lassen
4. Bei Erfolg: v0.1.0 final taggen, CHANGELOG-Datum setzen

**Aufwand:** 30 Minuten (nach F-02)

---

### F-05: VOID-010 ueberfaellig (P1, offen)

**Evidenz:**
- VOIDMAP.yml: VOID-010 "Taxonomie & Spektren (Empirie)", target_date: 2026-03-15, status: OPEN
- void-sync.yml (Montags-Schedule) sollte GitHub Issue als ueberfaellig erstellt haben
- Keine Literaturbelege fuer Spektralzuweisungen vorhanden

**Auswirkung:**
- Ungedeckte Behauptungen im Spektralbereich
- Claim-Hygiene-Verletzung wenn nicht als HYPOTHESE getaggt

**Empfehlung:**
- Option A: Literaturbelege in docs/voids/ ergaenzen (CSV-Tabelle mit min. 5 Quellen)
- Option B: Deadline bewusst verlaengern mit Begruendung in VOIDMAP.yml
- In beiden Faellen: Status auf IN_PROGRESS setzen

---

## 3. Neue Befunde (seit Maerz 2026)

### N-01: Next.js Major-Upgrade 14 zu 16 (P2)

**Evidenz:** Commit `1364c6d` — next von 14.2.21 auf 16.1.6 via Dependabot

**Auswirkung:** Major-Version-Sprung mit potenziellen Breaking Changes (App Router, Middleware, API Routes). Kein `next build` Check in CI (s. N-03).

**Empfehlung:** Smoke-Test (`next build`) in CI hinzufuegen; Breaking Changes pruefen.

---

### N-02: @types/node Major-Upgrade 20 zu 25 (P2)

**Evidenz:** Commit `7adf634` — @types/node von 20.19.30 auf 25.2.3

**Auswirkung:** Potenziell inkompatible Type-Definitionen, insbesondere wenn Node.js Runtime noch auf v20 laeuft.

**Empfehlung:** TypeScript-Kompatibilitaet pruefen; test.yml nutzt Node 20 — Version-Mismatch.

---

### N-03: Kein ui-app CI-Test fuer Next.js Build (P2)

**Evidenz:** `.github/workflows/test.yml` testet JavaScript via Jest, fuehrt aber keinen `next build` aus.

**Auswirkung:** Build-Fehler in ui-app/ werden nicht erkannt, besonders kritisch nach Major-Upgrade (N-01).

**Empfehlung:**
```yaml
# In test.yml, nach Jest-Tests:
- name: Build Next.js app
  working-directory: ui-app
  run: npm run build
```

---

### N-04: adapters/ ist Stub (P3)

**Evidenz:** `adapters/msi_adapter_v1.yaml` ist einzige Datei, keine Implementierung.

**Empfehlung:** Als HYPOTHESE dokumentieren oder VOID erstellen wenn Implementierung geplant.

---

## 4. Workflow-Analyse (11 Workflows)

| Workflow | Status | Befund |
|----------|--------|--------|
| ci.yml | OK | 4-Stage Pipeline funktional; SHA-gepinnt; Coverage 50% (s. F-03) |
| ci-smoke.yml | OK | Lightweight Validation |
| ci-policy-lint.yml | OK | JSON-Validierung fuer gate_policy |
| ci-evidence-bundle.yml | OK | Evidence Collection |
| deepjump-ci.yml | OK | Hauptpipeline mit reusable Workflow; daily 3 AM UTC |
| deepjump-audit.reusable.yml | OK | HMAC-Masking korrekt; Secret-Verfuegbarkeit unklar (F-19) |
| metatron-guard.yml | WARN | Soft enforcement OK, aber keine Merge-Commit-Exemption (F-07) |
| release.yml | UNTESTED | 7-Gate-Checks definiert, nie ausgeloest (F-04) |
| sbom.yml | OK | CycloneDX, 90-Tage-Retention |
| test.yml | WARN | Jest + Pytest OK; kein `next build` (N-03) |
| void-sync.yml | OK | Montags-Schedule; VOID-010 sollte als ueberfaellig gemeldet sein |

**Keine Duplikate oder Widersprueche zwischen Workflows erkannt.** Zustaendigkeiten sind klar getrennt.

---

## 5. Sicherheits-Bewertung

| Aspekt | Status | Detail |
|--------|--------|--------|
| Secrets in Code | CLEAN | Kein hardcoded Secret gefunden |
| HMAC-Handling | VERBESSERT | Ephemeral Fallback entfernt (007566b); fail-fast in CI |
| CI-Action-Pinning | OK | SHA-Hashes in ci.yml; Dependabot aktualisiert Actions |
| Bandit-Config | OK | Justified Skips: B105=SVG-Farben, B311=Demo-Random, B404/603/607=Git-Ops |
| Dependency-Scanning | OK | Dependabot weekly fuer pip/npm/actions |
| SBOM | OK | CycloneDX-Generierung bei Release und Push auf main |
| Subprocess-Usage | OK | Nur in tools/ fuer hardcoded Git-Operationen (bandit-justified) |

---

## 6. VOIDMAP-Status

| VOID | Titel | Status | Bemerkung |
|------|-------|--------|-----------|
| VOID-001 | DeepJump Protocol | CLOSED | Seit 2026-01-04 |
| VOID-002 | CI Pipeline Integration | CLOSED | Seit 2026-02-15 |
| VOID-003 | Status Emit Receipt | CLOSED | Seit 2026-03-06 |
| VOID-010 | Taxonomie & Spektren | **OPEN** | Ueberfaellig (target: 2026-03-15) |
| VOID-011 | Metriken der Resonanz | **OPEN** | MI/FD implementiert, toy_resonance minimal |
| VOID-012 | GateProof Checkliste | CLOSED | Seit 2026-03-06 |
| VOID-013 | Sensor-Architektur | CLOSED | Seit 2026-03-06 |
| VOID-014 | Protein-Design | **OPEN** | Kein Code, kein SUSPENDED-Label |
| VOID-020-023 | Port-Matrix Suite | CLOSED | Alle seit 2026-01-13 |

---

## 7. Vergleich mit Vorgaenger-Audits

### Audit Jan 2026 (AUDIT_SUMMARY.md) — Was wurde umgesetzt?

| Empfehlung | Status April 2026 |
|------------|-------------------|
| Q1: Fix Python Imports (Fractalsense) | Teilweise: optional deps non-blocking (34817b6) |
| Q2: Compile Regex Patterns | Nicht umgesetzt |
| Q3: Create Missing Governance Files | **Erledigt**: gateproof_v1.yaml, sensors.spec.json, bom.md |
| Q4: Optimize Directory Traversal | Nicht umgesetzt |
| Q5: Fix Import Style | Nicht umgesetzt |
| S1: Import Linting in CI | Nicht umgesetzt |
| S2: Rename pdf canvas/ | **Erledigt**: Verzeichnis nicht mehr vorhanden |

### Workpackage Maerz 2026 — Was wurde umgesetzt?

| Issue | Status April 2026 |
|-------|-------------------|
| P0-A: NICHTRAUM materialisieren | **Offen** |
| P0-B: G1-Kategorisierung | **Offen** |
| P1-A: VOID-011 Stubs heben | **Teilweise**: MI/FD implementiert |
| P1-B: VOID-010 Literatur | **Offen** (ueberfaellig) |
| P1-C: Semver-Tag 0.1.0 | **Offen** |
| P2-A: Metatron-Amnesty | **Offen** |
| P2-B: E2E-Demo | **Offen** |
| P2-C: Python-UI Datenbruecke | **Offen** |

---

## 8. Naechste sinnvolle Updates (priorisiert)

1. **P0: NICHTRAUM/ materialisieren** — 15min, rein additiv, kein Risiko
2. **P0: annex_map.yaml + annex_check.py** — 2-3h, G1-Enforcement
3. **P1: Coverage-Widerspruch aufloesen** — 5min, CI oder Docs anpassen
4. **P1: v0.1.0-rc1 Dry-Run** — 30min, Release-Workflow erstmals testen
5. **P1: VOID-010 Deadline-Entscheidung** — Verlaengern oder Literatur ergaenzen
6. **P2: Metatron Merge-Commit-Exemption** — 15min, Regex in metatron-guard.yml
7. **P2: Next.js Build-Check in CI** — 15min, `next build` Step in test.yml
8. **P2: make demo Target** — 1h, emit-verify Zyklus
9. **P2: Regex-Compilation in tools/** — 30min, Performance-Quick-Win (aus Jan-Audit)
10. **P4: VOID-014 als SUSPENDED markieren** — 5min, VOIDMAP.yml Update

---

## Artefakte

- `docs/audit/2026-04-01_repo_analysis_update.md` (dieser Report)

## Referenzen

- `docs/audit/AUDIT_SUMMARY.md` (2026-01-24)
- `docs/audit/IMPROVEMENT_RECOMMENDATIONS.md` (2026-01-24)
- `OUT/OPERATIVE_WORKPACKAGE_20260317.md` (2026-03-17)
- `VOIDMAP.yml` (zuletzt aktualisiert 2026-03-06)
- `CLAUDE.md` (Guards G0-G6)
- `.claude/rules/annex.md` (G1 Annex-Prinzip)
