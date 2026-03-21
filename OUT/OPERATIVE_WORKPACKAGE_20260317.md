# Operatives GitHub-Arbeitspaket

**Datum:** 2026-03-17
**FOKUS:** Repo-Analyse → Operatives Arbeitspaket
**Autor:** Principal Engineer / Repo-Steward (Claude)
**Branch:** claude/repo-architecture-analysis-0OC44
**Basis:** Vollständige Repository-Analyse (März 2026)
**Claim-Status:** Dieser Report basiert auf belegten Beobachtungen (INFERENZ wo angegeben)

---

## 1. Operativer Kernbefund

### Lageeinschätzung

EntaENGELment ist ein kohärentes, governance-first Forschungsprototyp-Framework mit 179 Commits,
39 % KI-Autorenschaft und einem soliden CI-/Audit-Fundament. Die Governance-Schicht (Guards G0–G6,
HMAC-Receipts, GateProof-Checkliste, Metatron-Guard in CI) ist strukturell vollständig und funktional.
Die Implementierungsschicht hingegen ist systematisch unvollständig: Kernfähigkeiten wie Resonanzmetriken
(MI, PLV, FD), Spektraltaxonomie und Sensor-Integration sind dokumentiert, in Code aber nur als Stubs oder
gar nicht vorhanden. Das Repo liefert exakt das, was es deklariert: einen Prototyp — nicht weniger, aber
auch nicht mehr.

### Was muss geschützt werden

GOLD-Dateien (index/, policies/, VOIDMAP.yml) und IMMUTABLE Receipts (data/receipts/) sind strukturell
intakt und dürfen unter keinen Umständen still migriert oder "aufgeräumt" werden. Ebenso schutzbedürftig:
die Claim-Disziplin (FACT / INFERENZ / HYPOTHESE / METAPHER), das Annex-Prinzip (G1) als
Änderungsschutzschild und die ehrliche Selbstverortung in docs/negations.md. Jede Maßnahme, die
Simulation, Stub oder Aspiration still zu "Evidenz" aufwertet, ist ein Governance-Verstoß.

### Gefährlichste offene Lücke

Die kombinierte Abwesenheit von (a) NICHTRAUM/-Verzeichnis trotz G2-Regel, (b) 59 Dateien ohne G1-
Kategorie und (c) keiner einzigen lauffähigen End-to-End-Demo erzeugt ein strukturelles Onboarding-Risiko:
Ein neuer Contributor (oder zukünftiger Claude-Context) kann die Governance-Regeln nicht aus der Repo-
Struktur ableiten — er muss sie aus Dokumenten rekonstruieren. Wenn diese Diskrepanz zwischen Regel und
Infrastruktur wächst, erodiert die Governance-Schicht von innen.

---

## 2. Priorisierter Issue-Backlog

| Priorität | Issue-Titel | Typ | Warum jetzt | Akzeptanzkriterien | Abhängigkeiten | Labels |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P0 | NICHTRAUM/-Verzeichnis materialisieren | governance | G2-Regel existiert, Zielverzeichnis fehlt — Regel ohne Infrastruktur | `NICHTRAUM/archive/`, `NICHTRAUM/maybe/`, `NICHTRAUM/quarantine/` existieren; `.gitkeep`; CI-Check auf Existenz | keine | `governance` `infra` `G2` |
| P0 | G1-Kategorisierung der 59 UNKNOWN-Dateien | governance | Annex-Prinzip (G1) ist CI-Regel aber ohne Enforcement; 59 Dateien unkategorisiert | Jede Datei hat explizite G1-Kategorie; `tools/annex_check.py` schlägt bei UNKNOWN fehl | keine | `governance` `G1` `tech-debt` |
| P1 | VOID-011: Resonanzmetriken von Stub zu HYPOTHESE heben | research | Überreichste Metrik-Dokumentation, minimalstes Code-Pendant — Mismatch wächst | `toy_resonance_dataset.py` produziert synthetische MI/PLV/FD-Werte; Claim explizit als HYPOTHESE/SIMULATION_PROXY getaggt; Tests existieren | keine | `research` `VOID-011` `claim-hygiene` |
| P1 | VOID-010: Spektraltaxonomie mit Literaturbelegen verankern | research | VOID-010 überfällig (Deadline 2026-03-15); Spektralzuweisungen ohne Quellen = ungedeckte Behauptungen | CSV-Tabelle mit ≥5 zitierten Quellen; `claim_lint.py` akzeptiert Einträge als INFERENZ (nicht FACT); neues Dok in docs/voids/ | VOID-011 | `research` `VOID-010` `docs` |
| P1 | Semver-Tag 0.1.0 erzeugen und Release-Notes schreiben | chore | CHANGELOG nennt 0.1.0, kein Tag existiert — Versioning in der Praxis nicht gestartet | `git tag v0.1.0`; GitHub Release erstellt; Release-Notes aus CHANGELOG extrahiert; CI Release-Workflow läuft durch | G1-Kategorisierung abgeschlossen | `chore` `release` |
| P2 | Metatron-Amnesty formal kodieren (Merge-Commits exemptieren) | governance | 47/50 Commits ohne FOKUS-Marker; AMNESTY-Dok existiert aber nicht in CI konfiguriert | `metatron-guard.yml` exemptiert Merge-Commits via Regex; AMNESTY-Datum in Workflow dokumentiert | keine | `governance` `G4` `ci` |
| P2 | E2E-Demo: Minimaler Receipt-Zyklus (emit → verify → display) | feature | Kein lauffähiger Demo-Pfad trotz vollständiger Tool-Chain — Onboarding-Blocker | `make demo` produziert HMAC-Receipt, verifiziert es, gibt Status aus; in README verlinkt; läuft in CI als Smoke-Test | keine | `feature` `demo` `onboarding` |
| P2 | Python → UI Datenbrücke spezifizieren | tech-debt | Next.js UI und Python-Backend existieren parallel ohne dokumentierten Datenfluss | API-Spec (OpenAPI oder JSON-Schema) in `docs/api/` beschreibt mindestens 2 Endpunkte; als HYPOTHESE markiert wenn unimplementiert | keine | `tech-debt` `ui-app` `docs` |
| P3 | Konfabulations-Risiko-Overlay (T2.4-KONFAB-ACM) abschließen | feature | Ticket in-progress, kein Abschlussdatum sichtbar | Ticket geschlossen oder explizit auf SUSPENDED gesetzt mit Begründung | keine | `feature` `governance` |
| P3 | Externe Hash-Anchor-Exploration (INFERENZ) | research | Idee erwähnt aber nicht verfolgt; Tamper-Proof-Einschränkung in negations.md benannt | ADR (Architecture Decision Record) in `docs/adr/` mit HYPOTHESE-Claim; keine Implementierung | keine | `research` `scope-control` |
| P4 | VOID-014 Protein-Design formal suspendieren | scope-control | Scope "bounded for safety" ohne explizites SUSPENDED-Label — schwebender Scope kostet Aufmerksamkeit | VOID-014 in VOIDMAP.yml als `status: SUSPENDED` mit Begründung; kein Code dazu in `src/` | keine | `scope-control` `VOID-014` |
| P4 | Maintainer-Onboarding-Guide erstellen | docs | 39% Claude-Autorenschaft erhöht Bus-Faktor; kein dedizierter Einstieg für menschliche Maintainer | `docs/MAINTAINER_GUIDE.md` mit ≤500 Wörtern; deckt: lokales Setup, Guard-Übersicht, PR-Checkliste | E2E-Demo vorhanden | `docs` `onboarding` |

---

## 3. Issue-Details (Top 5)

---

### P0-A: NICHTRAUM/-Verzeichnis materialisieren

**Problem**
Guard G2 schützt den `NICHTRAUM/`-Bereich als Auffangzone für Unentschiedenes. Das Verzeichnis mit den
definierten Unterordnern (`archive/`, `maybe/`, `quarantine/`) existiert im Repository nicht. Die Regel ist
dokumentiert, die Infrastruktur fehlt. Jeder Versuch, G2 anzuwenden, würde stillschweigend scheitern oder
ad-hoc-Verzeichnisse erzeugen.

**Evidenz**
- `CLAUDE.md` G2: "NICHTRAUM/ ist ein geschützter Bereich"
- Workspace Layout in `CLAUDE.md` listet `NICHTRAUM/archive/`, `NICHTRAUM/maybe/`, `NICHTRAUM/quarantine/`
- Audit-Befund: "G2 documented but the directory isn't there"
- `security.md` verweist auf `NICHTRAUM/quarantine/` als Quarantine-Ziel

**Ziel**
Infrastruktur mit Governance in Deckung bringen; G2 wird lauffähig statt aspirational.

**Akzeptanzkriterien**
- `NICHTRAUM/archive/.gitkeep`, `NICHTRAUM/maybe/.gitkeep`, `NICHTRAUM/quarantine/.gitkeep` committet
- `NICHTRAUM/quarantine/quarantine_log.md` mit leerem Template (per `security.md` Format) vorhanden
- Optional: `tools/annex_check.py` oder CI-Step prüft Existenz der drei Unterverzeichnisse
- Kein Inhalt verschoben (reine Infrastruktur-PR)

**Nicht-Ziele**
- Kein Inhalt in NICHTRAUM verschieben (separater PR)
- Keine neuen Guards einführen
- Keine Änderungen an GOLD-Dateien

**Risiken**
- NIEDRIG — rein additive Änderung, keine Logik betroffen
- `.gitkeep`-Dateien könnten bei Cleanup-Automatiken versehentlich gelöscht werden → `.gitignore`-Ausnahme prüfen

**Betroffene Pfade**
```
NICHTRAUM/archive/.gitkeep        (neu)
NICHTRAUM/maybe/.gitkeep          (neu)
NICHTRAUM/quarantine/.gitkeep     (neu)
NICHTRAUM/quarantine/quarantine_log.md  (neu, Template)
```

**Labels:** `governance` `G2` `infra` `good-first-issue`

---

### P0-B: G1-Kategorisierung der 59 UNKNOWN-Dateien

**Problem**
Das Annex-Prinzip (G1) unterscheidet GOLD / ANNEX / IMMUTABLE. CI soll UNKNOWN ablehnen. Laut
Deep-Audit-Report sind 59 Dateien ohne explizite Kategorie. `tools/annex_check.py` (oder äquivalent)
erzwingt diese Klassifikation nicht maschinell. Damit ist G1 eine Regel mit Dokumentation aber ohne
Durchsetzung.

**Evidenz**
- `audit/DEEP_AUDIT_REPORT_20260117.md`: "59 files in UNKNOWN category"
- `.claude/rules/annex.md` listet Pfad-Tabelle, kein CI-Enforcement dokumentiert
- `policies/gateproof_v1.yaml` referenziert G1, kein maschinenlesbares Mapping

**Ziel**
Jede Datei im Repo hat eine explizite G1-Kategorie; CI blockiert bei UNKNOWN.

**Akzeptanzkriterien**
- `tools/annex_check.py` liest eine Konfigurationsdatei (`policies/annex_map.yaml` o.ä.) und schlägt bei UNKNOWN-Pfaden fehl
- Alle 59 bisher unkategorisierten Pfade sind in der Map eingetragen
- CI-Workflow führt `annex_check.py` aus und ist blockierend
- GOLD-Dateien dürfen in Map als GOLD markiert sein, müssen aber nicht separat geschützt werden (das ist Reviewer-Aufgabe)

**Nicht-Ziele**
- Keine inhaltlichen Änderungen an GOLD-Dateien
- Kein Refactoring bestehender Kategorien
- Keine neuen Pfad-Konventionen einführen

**Risiken**
- MITTEL — Falsch kategorisierte Dateien könnten CI-Fehler erzeugen, die andere PRs blockieren
- Empfehlung: Erst in warning-mode deployen, nach Review auf blocking setzen

**Betroffene Pfade**
```
policies/annex_map.yaml           (neu)
tools/annex_check.py              (neu oder erweitert)
.github/workflows/ci.yml          (Schritt hinzufügen)
```

**Labels:** `governance` `G1` `tech-debt` `ci`

---

### P1-A: VOID-011 Resonanzmetriken von Stub zu HYPOTHESE heben

**Problem**
Resonanzmetriken (MI = Mutual Information, PLV = Phase-Locking Value, FD = Fractal Dimension) sind
Kernkonzepte der EntaENGELment-Dokumentation und werden in mehreren Docs als Fähigkeit des Frameworks
beschrieben. `src/tools/toy_resonance_dataset.py` existiert, ist aber "minimal" (laut Audit). Es gibt keinen
Hinweis, dass die Implementierung die beschriebene Berechnung tatsächlich liefert. Das erzeugt einen
unmarkierten Claim-Mismatch: Dokumentation impliziert Fähigkeit, Code liefert Stub.

**Evidenz**
- `docs/voids/VOID-011_*`: "MI, PLV, FD are described as stubs"
- Audit: "toy_resonance_dataset.py exists but is minimal"
- VOID-011 als HIGH-Priorität, Deadline 2026-03-15 (überfällig)

**Ziel**
`toy_resonance_dataset.py` produziert synthetische (!) Beispieldaten für MI, PLV, FD mit explizitem
SIMULATION_PROXY-Claim-Tag. Kein Anspruch auf empirische Validität.

**Akzeptanzkriterien**
- Skript generiert bei `python toy_resonance_dataset.py` eine CSV mit Spalten: `t`, `mi_proxy`, `plv_proxy`, `fd_proxy`
- Docstring enthält: `CLAIM: SIMULATION_PROXY — Keine empirischen Daten, synthetisch erzeugt`
- `tests/unit/test_toy_resonance.py` prüft: Output existiert, Spalten vorhanden, Werte im validen Range
- `claim_lint.py` akzeptiert die Datei (kein FACT-Claim ohne Beleg)
- VOID-011 in VOIDMAP.yml auf `status: IN_PROGRESS` gesetzt mit Notiz "toy simulation done, empirical validation pending"

**Nicht-Ziele**
- Keine echten Messdaten verwenden
- Keine ML-Modelle
- Keine Integration in UI in diesem Schritt
- Kein Upgrade zu FACT oder EVIDENZ

**Risiken**
- NIEDRIG — isoliertes Skript, keine Breaking Changes
- Reputationsrisiko wenn SIMULATION_PROXY nicht klar kommuniziert → Claim-Tag ist Pflicht

**Betroffene Pfade**
```
src/tools/toy_resonance_dataset.py    (erweitern)
tests/unit/test_toy_resonance.py      (neu)
VOIDMAP.yml                           (Status-Update, GOLD → Checkpoint nötig)
```

**Labels:** `research` `VOID-011` `claim-hygiene`

---

### P2-A: E2E-Demo: Minimaler Receipt-Zyklus

**Problem**
Die Tool-Chain für HMAC-Receipts (emit → verify) ist vollständig implementiert. Trotzdem existiert kein
dokumentierter, lauffähiger Demo-Pfad. Ein Contributor, der verstehen will, was das Framework *tut*,
findet keine funktionierende Demonstration. `README.md` erwähnt `make verify`, aber kein `make demo`.
Das ist der stärkste Onboarding-Blocker für das sonst stärkste Feature des Repos.

**Evidenz**
- Audit: "No runnable example"; "make verify mentioned but no make demo"
- `tools/status_emit.py` und `tools/status_verify.py` existieren und sind funktional (laut Audit)
- README verspricht reproduzierbare Workflows

**Ziel**
`make demo` führt den vollständigen Receipt-Zyklus durch: Emit → Receipt in data/receipts/ → Verify → Ausgabe auf stdout.

**Akzeptanzkriterien**
- `Makefile`-Target `demo` vorhanden
- Demo läuft in CI als Smoke-Test (separater Workflow-Step oder eigener Job)
- README enthält Demo-Abschnitt mit Beispiel-Output (als Code-Block, FACT)
- Keine neuen Dependencies

**Nicht-Ziele**
- Keine UI-Integration in diesem Schritt
- Kein komplexes Multi-Agent-Szenario
- Keine Änderungen an bestehenden Receipt-Formaten (IMMUTABLE)

**Risiken**
- NIEDRIG für Code
- MITTEL für HMAC-Secret-Handling in CI: Demo darf kein echtes Secret committen → `.env`-Pattern oder Test-Secret dokumentieren

**Betroffene Pfade**
```
Makefile                              (demo-Target, neu oder erweitern)
.github/workflows/smoke.yml           (Demo-Step hinzufügen)
README.md                             (Demo-Abschnitt, ANNEX)
docs/DEMO.md                          (neu, optional)
```

**Labels:** `feature` `demo` `onboarding` `good-first-issue`

---

### P0-C: Semver-Tag 0.1.0 erzeugen

**Problem**
CHANGELOG.md beschreibt Version 0.1.0 als unreleased. Kein git-Tag existiert. Der Release-Workflow in CI
ist implementiert, wird aber nie ausgelöst. Ohne Tag gibt es keine reproduzierbare Referenzversion,
keinen Snapshot-Punkt für Audits und keine offizielle Bestätigung des Reifegrads.

**Evidenz**
- Audit: "0.1.0 only in changelog, no tags"
- CI-Workflow `release.yml` existiert (aus Infrastructure Sprint)
- `CHANGELOG.md` Keep-a-Changelog-Format mit `[0.1.0] - Unreleased`

**Ziel**
`v0.1.0`-Tag auf aktuellem Stand erstellen; Release-Notes aus CHANGELOG generieren; CI Release-Workflow einmalig vollständig durchlaufen.

**Akzeptanzkriterien**
- `git tag v0.1.0` auf main (oder designated branch)
- GitHub Release erstellt mit Release-Notes aus CHANGELOG
- CHANGELOG-Eintrag von `Unreleased` auf Datum gesetzt
- CI Release-Workflow grün

**Nicht-Ziele**
- Keine Feature-Vollständigkeit als Voraussetzung (0.1.0 = "erstes versioniertes Artefakt")
- Kein Breaking-Change-Prozess nötig

**Risiken**
- NIEDRIG bis MITTEL: Release-Workflow möglicherweise nicht vollständig getestet → Dry-Run vor echtem Tag

**Betroffene Pfade**
```
CHANGELOG.md                          (Datum eintragen, ANNEX)
.github/workflows/release.yml         (ausführen)
```

**Labels:** `chore` `release`

---

## 4. Commit- und PR-Reihenfolge

| Reihenfolge | Commit/PR-Titel | Zweck | Größe | Risiko |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `governance: materialize NICHTRAUM/ directory structure` | G2-Infrastruktur erzeugen | XS | Niedrig |
| 2 | `governance: add annex_map.yaml with G1 classifications` | 59 UNKNOWN-Dateien kategorisieren | S | Niedrig-Mittel |
| 3 | `ci: add annex_check step (warning mode)` | G1-Enforcement vorbereiten (non-blocking) | XS | Niedrig |
| 4 | `ci: make annex_check blocking after review` | G1-Enforcement aktivieren | XS | Mittel |
| 5 | `ci: exempt merge commits from metatron-guard` | 47-Commit-Rückstand formal amnestieren | XS | Niedrig |
| 6 | `research(VOID-011): extend toy_resonance_dataset with MI/PLV/FD stubs` | Stub → SIMULATION_PROXY heben | S | Niedrig |
| 7 | `test: add unit tests for toy_resonance_dataset` | Coverage + Claim-Validierung | S | Niedrig |
| 8 | `feat(demo): add make demo target for emit→verify receipt cycle` | Onboarding-Demo | S | Niedrig-Mittel |
| 9 | `ci: add smoke test for make demo` | Demo in CI absichern | XS | Niedrig |
| 10 | `docs(VOID-010): add cited spectral taxonomy table (INFERENZ)` | VOID-010 teilschließen | M | Niedrig |
| 11 | `chore: set CHANGELOG 0.1.0 release date` | Versioning materialisieren | XS | Niedrig |
| 12 | `chore: create v0.1.0 git tag and GitHub release` | Ersten Snapshot erzeugen | XS | Mittel |
| 13 | `scope-control(VOID-014): mark protein-design as SUSPENDED` | Schwebenden Scope schließen | XS | Niedrig |
| 14 | `docs: add Python→UI API spec skeleton (HYPOTHESE)` | Datenbrücke spezifizieren | S | Niedrig |
| 15 | `docs: add MAINTAINER_GUIDE.md` | Onboarding-Risiko reduzieren | S | Niedrig |

**Reihenfolge-Logik:**
- Erst Infrastruktur/Scope-Klarheit (1–5): Guards materialisieren, bevor neuer Code kommt
- Dann Metrik-Substanz (6–7): Stub ehrlich heben, nicht still upgraden
- Dann Datenfluss/Demo (8–9): Einziges lauffähiges Artefakt erzeugen
- Dann Dokumentations-Substanz (10–11): Offene VOIDs sauber behandeln
- Dann Governance-Abschluss (12–15): Versioning, Scope-Freeze, Onboarding

---

## 5. Commit-Vorschläge (Conventional Commits)

```
governance: materialize NICHTRAUM/ dirs with gitkeep and quarantine log template
governance(G1): add annex_map.yaml classifying all repo paths by GOLD/ANNEX/IMMUTABLE
ci(annex): add annex_check.py step in warning mode before enabling block
ci(metatron): exempt merge commits from FOKUS-marker requirement per AMNESTY doc
research(VOID-011): extend toy_resonance_dataset.py with MI/PLV/FD proxies — SIMULATION_PROXY
test(VOID-011): add unit tests for toy_resonance_dataset output shape and value ranges
feat(demo): add Makefile demo target running emit→verify receipt cycle end-to-end
ci(smoke): add demo smoke test to CI pipeline
docs(VOID-010): add spectral taxonomy CSV with ≥5 cited sources, tagged INFERENZ
scope-control(VOID-014): mark protein-design VOID as SUSPENDED with rationale in VOIDMAP
chore(release): set 0.1.0 release date in CHANGELOG and create v0.1.0 git tag
docs(api): add Python-to-UI API spec skeleton in docs/api/ tagged HYPOTHESE
docs(onboarding): add MAINTAINER_GUIDE.md covering setup, guards, PR checklist
governance(G1): switch annex_check CI step from warning to blocking after audit sign-off
fix(metatron): correct workflow regex to properly exempt bot-generated merge commits
```

---

## 6. PR-Vorschläge (erste 3)

---

### PR 1: `governance: materialize NICHTRAUM/ and G1 annex map`

**Titel:** `governance: materialize NICHTRAUM/ dirs and add G1 annex_map.yaml (warning mode)`

**Kurzbeschreibung:**
Zwei rein additive, risikolose Infrastruktur-Maßnahmen in einer PR:
1. `NICHTRAUM/` mit drei Unterverzeichnissen und quarantine_log-Template erzeugen
2. `policies/annex_map.yaml` mit G1-Klassifikation aller bekannten Pfade anlegen
3. `tools/annex_check.py` prüft Map gegen Repo-Pfade, CI-Step in **warning mode** (non-blocking)

**Warum isoliert sinnvoll:**
Beide Maßnahmen sind rein additiv, berühren keine existierende Logik und können unabhängig reviewt werden.
Sie materialisieren dokumentierte Guards ohne inhaltliche Entscheidungen zu erzwingen. Warning-Mode
verhindert, dass ein unentdeckter UNKNOWN-Pfad den CI sofort bricht.

**Welche Risiken sie reduziert:**
- G2-Lücke (Nichtraum-Infrastruktur fehlt)
- G1-Enforcement-Lücke (59 UNKNOWN-Dateien)
- Onboarding-Verwirrung (Regel ohne Infrastruktur)

**Welche Folge-PR sie vorbereitet:**
PR 2 (annex_check auf blocking setzen) und PR 3 (Metatron-Amnesty in CI) können erst sinnvoll
deployed werden, wenn die Map-Grundlage steht.

---

### PR 2: `ci: switch annex_check to blocking + exempt merge commits from metatron-guard`

**Titel:** `ci: enable blocking annex_check and apply metatron merge-commit amnesty`

**Kurzbeschreibung:**
Zwei CI-Hardening-Schritte nach Review von PR 1:
1. `annex_check.py`-Step von warning auf blocking setzen (alle 59 Pfade sind jetzt kategorisiert)
2. `metatron-guard.yml` Regex ergänzen: Merge-Commits werden von FOKUS-Pflicht exemptiert, AMNESTY-Datum wird im Workflow-Kommentar dokumentiert

**Warum isoliert sinnvoll:**
Trennt "Infrastruktur schaffen" (PR 1) von "Infrastruktur durchsetzen" (PR 2). Reviewers können
gezielt auf CI-Impact prüfen. Merge-Commit-Amnesty ist eine 1-Zeilen-Regex-Änderung, die historischen
CI-Rückstand bereinigt.

**Welche Risiken sie reduziert:**
- Zukünftige unbemerkte GOLD-Verletzungen durch UNKNOWN-Dateien
- CI-Failures durch legitime Merge-Commits die kein FOKUS haben können

**Welche Folge-PR sie vorbereitet:**
Nach CI-Härtung kann PR 3 (VOID-011 Resonanzmetriken) ohne Governance-Schulden starten.

---

### PR 3: `research(VOID-011): extend toy resonance dataset + tests`

**Titel:** `research(VOID-011): extend toy_resonance_dataset.py with MI/PLV/FD SIMULATION_PROXY values`

**Kurzbeschreibung:**
`src/tools/toy_resonance_dataset.py` wird erweitert um synthetische Beispieldaten für Mutual Information,
Phase-Locking Value und Fractal Dimension. Explizites SIMULATION_PROXY-Claim-Tag in Docstring und
Ausgabe-CSV-Header. Neue Unit-Tests prüfen Outputform und Wertebereiche. VOID-011 in VOIDMAP.yml von
OPEN auf IN_PROGRESS mit Kommentar "toy simulation done, empirical validation pending".

**Warum isoliert sinnvoll:**
Bereinigt den größten Claim-Mismatch im Repo (Dokumentation verspricht Metriken, Code liefert Stub)
ohne die Wahrheitsbehauptung zu erhöhen. Explizites SIMULATION_PROXY macht den Status für alle sichtbar.

**Welche Risiken sie reduziert:**
- Unmarkierter Stub-to-Evidenz-Drift
- Falscher Eindruck bei externen Lesern der Dokumentation
- VOID-011-Deadline-Überziehung (bereits überfällig)

**Welche Folge-PR sie vorbereitet:**
VOID-010 (Spektraltaxonomie) und die E2E-Demo (PR 4) können auf einem sauber markierten
SIMULATION_PROXY-Fundament aufbauen.

---

## 7. Update- / Changelog-Text

### 7.1 Changelog-Eintrag (Keep-a-Changelog-Format)

```markdown
## [Unreleased]

### Added
- `NICHTRAUM/` directory structure materialized (archive/, maybe/, quarantine/)
  with quarantine_log template — implements G2 guard infrastructure
- `policies/annex_map.yaml`: explicit G1 classification for all repository paths
- `tools/annex_check.py`: CI tool validating path classification against annex_map
- `docs/MAINTAINER_GUIDE.md`: onboarding guide for human contributors
- `Makefile` target `demo`: end-to-end receipt cycle (emit → verify) — first
  runnable artifact, documented as FACT (existing toolchain)
- `src/tools/toy_resonance_dataset.py` extended with MI/PLV/FD proxy outputs
  (SIMULATION_PROXY — synthetic data, no empirical validity claimed)
- `docs/api/`: Python-to-UI API spec skeleton (HYPOTHESE — unimplemented)
- `docs/voids/VOID-010_taxonomy.md` updated with cited spectral table (INFERENZ)

### Changed
- CI `metatron-guard.yml`: merge commits exempted from FOKUS-marker requirement
  per `docs/governance/METATRON_AMNESTY.md`
- CI `annex_check` step: warning mode → blocking (after annex_map review)
- `VOIDMAP.yml`: VOID-011 → IN_PROGRESS, VOID-014 → SUSPENDED
- `CHANGELOG.md`: 0.1.0 release date set

### Fixed
- G2 guard had no materialized infrastructure (NICHTRAUM/ was missing)
- 59 files without explicit G1 category now classified

### Governance
- VOID-014 (Protein Design) formally SUSPENDED — scope explicitly bounded
- Metatron Amnesty applied to historical merge commits
- annex_check enforcement activated

### NOT changed (explicit)
- No receipt files modified (IMMUTABLE)
- No GOLD index files modified
- Resonance metrics remain SIMULATION_PROXY — no empirical upgrade
- API spec remains HYPOTHESE — no implementation included
```

### 7.2 Maintainer-Update (intern)

```
Stand: 2026-03-17

Das Infrastruktur-Sprint-Paket aus Feb 2026 ist abgeschlossen. Aktuelle Prioritäten:

1. Governance-Materialisierung: NICHTRAUM/ und G1-Map existieren noch nicht als
   Code — das ist der einzige strukturelle Widerspruch zwischen Regel und Repo.
   Nächste PR schließt diese Lücke.

2. VOID-011 und VOID-010 sind überfällig. VOID-011 wird mit synthetischen
   Proxy-Daten (SIMULATION_PROXY) teilbedient. VOID-010 braucht Literaturarbeit.
   Kein empirischer Upgrade geplant.

3. v0.1.0-Tag steht aus. Release-Workflow ist bereit. Wir sollten taggen sobald
   annex_check-CI grün ist.

4. VOID-014 (Protein Design) wird formal suspendiert — kostet Aufmerksamkeit
   ohne Mehrwert für den aktuellen Scope.

5. Bus-Faktor: 39% Claude-Autorenschaft. MAINTAINER_GUIDE.md ist überfällig.

Keine größeren Umbauten geplant. Kleine, reviewbare PRs.
```

### 7.3 README / Status-Absatz (1 Absatz)

```
**Projektstatus (März 2026):** EntaENGELment ist ein Forschungsprototyp im Stadium
v0.1.0 (erstes versioniertes Artefakt, noch kein stabiles API). Die Governance-Schicht
(Guards G0–G6, HMAC-Receipts, CI-Enforcement) ist strukturell vollständig. Kernfähigkeiten
wie Resonanzmetriken (MI, PLV, FD) liegen als synthetische SIMULATION_PROXY-Implementierung
vor — keine empirischen Daten, keine produktive Anwendbarkeit beansprucht. Sensor-Integration
(BOM v1.0 spezifiziert) und UI-Datenbrücke befinden sich im HYPOTHESE-Stadium. Das Projekt
ist explizit kein Produkt. Externe Contributions willkommen nach Lektüre von CLAUDE.md und
docs/MAINTAINER_GUIDE.md.
```

---

## 8. Fokus-Entscheidung

### Aktiv weiterbuilden (ACTIVE)

| Bereich | Begründung |
|---------|------------|
| Governance-Infrastruktur (NICHTRAUM/, G1-Map, CI) | Fundament; ohne Materialisierung erodieren alle Guards |
| E2E-Demo (Receipt-Zyklus) | Einziges Feature das vollständig existiert; muss lauffähig sein |
| VOID-011 Resonanzmetriken (SIMULATION_PROXY) | Höchster Claim-Mismatch; günstigste Behebung |
| Semver-Tagging (v0.1.0) | Niedrigster Aufwand, höchster Orienterungswert |

### Suspendieren (SUSPENDED)

| Bereich | Begründung |
|---------|------------|
| VOID-014 Protein Design | Scope explizit "bounded for safety", kein Fortschritt, kostet Aufmerksamkeit |
| Multi-Agent-Minimaldemo | Kein Fundament (keine E2E-Demo existiert noch); zu früh |
| Sensor-Integration (Code-Schicht) | BOM und Spec fertig; Implementation braucht Hardware-Kontext der fehlt |
| Externer Hash-Anchor | Explorativ, kein dringender Bedarf, Tamper-Proof bereits als Nicht-Ziel deklariert |

### Nur dokumentarisch pflegen (MAINTENANCE)

| Bereich | Begründung |
|---------|------------|
| VOID-010 Spektraltaxonomie | Literaturarbeit, kein Code nötig; INFERENZ-Status pflegen reicht |
| docs/ETHICS/ | IRB-Status + Consent-Template sind gut genug; kein aktiver Ausbau nötig |
| Fractalsense / bio_spiral_viewer | Standalone-Module, nicht im kritischen Pfad |
| docs/framework/ (Theoretische Linie) | Dokumentation stabil; keine Updates nötig bis Empirik reift |

---

## 9. Finales Urteil

### Was ist der wahre Kern?

EntaENGELment ist ein **Consent- und Audit-Framework** — nicht mehr, nicht weniger.
Der Kern ist: explizite Zustimmung, kryptografischer Nachweis (HMAC-Receipts), maschinell
durchsetzbare Guards. Alles andere — Resonanzmetriken, Spektraltaxonomie, Sensor-Integration —
ist Erweiterungsraum, der die Glaubwürdigkeit des Kerns stützen oder beschädigen kann.

### Was bedroht diesen Kern aktuell am stärksten?

Die **Diskrepanz zwischen dokumentierten Guards und fehlender Infrastruktur** (NICHTRAUM/ existiert
nicht, G1-Enforcement nicht aktiv, Metatron-Amnesty nicht kodiert). Wenn Regeln konsistent ohne
Infrastruktur existieren, erodieren sie — nicht dramatisch, sondern still. Bei 39 % KI-Autorenschaft
und steigender Komplexität kann eine zukünftige Claude-Session die Guards nicht aus der Repo-Struktur
ableiten, nur aus Dokumenten. Dokumente sind flüchtig, Infrastruktur ist persistent.

### Die 2 Schritte mit dem größten Hebel in 30 Tagen

**Schritt 1:** PR "Governance materialisieren" (NICHTRAUM/ + G1-Map + annex_check in warning mode)
mergen. Kein inhaltlicher Aufwand, rein additiv, sofort reviewbar — und schließt die gefährlichste
strukturelle Lücke.

**Schritt 2:** `make demo` implementieren und in CI absichern. Der Receipt-Zyklus *funktioniert
bereits* — er ist nur nicht demonstrierbar. Ein lauffähiges Artefakt ist der glaubwürdigste Beweis
für den Kern-Claim des Projekts. Alle anderen Maßnahmen sind besser begründbar sobald ein Demo
existiert.

---

*Erstellt: 2026-03-17*
*Claim-Status: Befunde aus Repo-Analyse (INFERENZ wo angegeben). Keine Empfehlungen als FACT markiert.*
*Nächste Überprüfung: nach Merge von PR 1 und PR 2*
