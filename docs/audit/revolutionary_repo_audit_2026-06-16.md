# Revolutionary Repository Audit — entaENGELment-

**Datum:** 2026-06-16
**Fokus:** Struktur-/Branch-/Workflow-/Verbindungs-Audit (Read-Only Phase 1)
**Branch:** `claude/great-galileo-h4jnc8`
**HEAD:** `af85bfb`
**Modus:** Phase 1 = Read-Only Systemscan. Keine inhaltlichen Änderungen in dieser Phase.

> Zielformel: „Revolutionäre Modernisierung durch bessere Membranen, nicht durch
> Austausch des Herzens." Dieser Bericht beschreibt, *was ist* — nicht, was sein
> soll. Empfehlungen sind als Vorschläge mit Claim-Status markiert.

---

## 0. Methodik & Claim-Disziplin

Claims in diesem Bericht tragen einen epistemischen Status (vgl.
`EPISTEMIC_HYGIENE.md`):

- **[FAKT]** — verifizierbar aus Code / Build-Output / Dateisystem.
- **[INFERENZ]** — aus Fakten abgeleitet, aber nicht direkt gemessen.
- **[MODELL]** — strukturelle Deutung / Architekturmuster.
- **[HYPOTHESE]** — Erwartung, nicht belegt.
- **[METAPHER]** — symbolisch, nicht-wörtlich.

Durchgeführte Beobachtungs-Operationen (alle read-only, deterministisch):

- Git-Topologie: `git branch -vv`, `git branch -r`, `git log`, `git status`.
- Dateisystem-Scan über getrackte Dateien (`git ls-files`: **476** Dateien).
- Workflow-Posture-Check: `python3 tools/workflow_posture_check.py` → PASS (13/13).
- VOID-Backlog-Drift: `python3 tools/voids_backlog_gen.py --check` → up to date.
- Doku-Graph- und Code-Graph-Survey über zwei Read-Only-Explorationsläufe.

**Nicht ausgeführt / Limitierung:** `pytest` ist in dieser Audit-Umgebung **nicht
installiert**; die Python-Testsuite konnte lokal **nicht** ausgeführt werden.
Aussagen zu Testergebnissen stützen sich auf CI-Konfiguration und Quelltext,
nicht auf einen lokalen Lauf. **[FAKT]** (Limitierung dokumentiert, kein „Looks
good" ohne Beleg — Anti-F7).

---

## 1. Executive Summary

**[INFERENZ]** Das Repository ist **deutlich reifer und disziplinierter** als ein
typisches Forschungs-Repo. Es besitzt eine bewusst gebaute Governance-Membran:
Claim-Lint, Pointer-Verify, Port-Lint, VOID-Registry mit Drift-Check,
HMAC-Receipts, Workflow-Posture-Contract, gepinnte Action-SHAs und explizite,
minimale CI-Permissions. Die symbolische Architektur (NEBEL→MEMBRAN→KRISTALL,
Consent-First, VOIDMAP, Claim-Disziplin) ist **konsistent zwischen Doku und
Werkzeugen** verankert.

Die größten Lücken sind **nicht** strukturelle Fäulnis, sondern **Zukunftsfähigkeits-Gaps**:

1. Fehlende Orientierungs-READMEs in den beiden größten Code-Domänen (`src/`, `tools/`).
2. Kein expliziter **Exchange-/Handoff-Archivraum** für „ehemalige Bezüglichkeit".
3. Keine **Registries** als erste-Klasse-Artefakte (Claim/Term/Evidence/Receipt) —
   die Bausteine existieren verstreut, aber ohne zentrale Indizes.
4. CI deckt Python/JS-Membran gut ab, aber **nicht** Markdown-Links, allgemeine
   YAML-Validität, VOIDMAP-Schema oder Exchange-Index-Konsistenz.
5. Strukturelle Doppeldeutigkeit `docs/audit/` (Singular) vs. im Auftrag
   gewünschtes `docs/audits/` (Plural) — Duplikationsrisiko (siehe §4, §8).

**[MODELL]** Empfehlung: Modernisierung durch *Ergänzung von Membranen*
(Registries, Exchange-Archiv, validierende Checks) statt Umbau des Kerns.

---

## 2. Was ist stabil?

**[FAKT]** Git-/Branch-Hygiene:

- Aktiver Branch: `claude/great-galileo-h4jnc8`, sauberes Working Tree.
- Nur zwei Remote-Branches: `origin/main`, `origin/claude/great-galileo-h4jnc8`.
  **Keine** Zombie-/Wildwuchs-Branches, keine divergierenden Altzweige sichtbar.
- `main` und Arbeitsbranch zeigen aktuell auf denselben Commit (`af85bfb`).
- Branch-Naming folgt erkennbarer Konvention (`claude/**`, `codex/**` in History).

**[FAKT]** CI/CD-Membran:

- 13 Workflows, **alle** erfüllen den Posture-Contract (explizite `permissions`,
  `concurrency` mit `cancel-in-progress: true`).
- Nur zwei Workflows mit Schreibrechten, beide dokumentiert in
  `docs/ci/WORKFLOW_MAP.md`: `release.yml` (`contents: write`, Release-Erstellung)
  und `void-sync.yml` (`issues: write`, VOID-Deadline-Issues).
- Action-Referenzen sind auf **SHA gepinnt** (z. B. `actions/checkout@df4cb1c…`).
- Blockierende Gates auf PRs: `verify_pointers --strict`, `claim_lint --strict`,
  `port_lint`, Tests, Smoke, Policy-Lint, Metatron-Guard (advisory), DeepJump.
- Dependabot aktiv für pip, npm (`/ui-app`), github-actions.

**[FAKT]** Governance-Werkzeuge (Stand: grün):

- `workflow_posture_check.py` → 13/13 PASS.
- `voids_backlog_gen.py --check` → `docs/voids_backlog.md` synchron mit `VOIDMAP.yml`.
- HMAC-Receipt-Pipeline (`status_emit.py`, `snapshot_guard.py`) vorhanden.

**[FAKT]** Build-/Sprach-Setup:

- Python: `pyproject.toml` mit ruff/black/mypy/pytest-Konfig, Coverage-Gate
  `--fail-under=50`, Matrix über Py 3.9–3.12.
- JS/TS: pnpm-Workspace (`ui-app`, `packages/*`), Turbo-Tasks
  (typecheck/lint/build/test), `@enta/types` (type-only), `@enta/tsconfig`.
- Lizenz: Apache-2.0 konsistent in `pyproject.toml`, `LICENSE`, `NOTICE`.

**[INFERENZ]** Essenz-Kohärenz: Framework-Begriffe (VOIDMAP, consent, PASS-Codes)
sind zwischen Code und Doku konsistent verwendet; rein konzeptuelle Begriffe
(tesser3TAKT, RZT, Traversal-Grammar) leben sauber in der Doku-/Spec-Schicht,
ohne unbelegte Code-Behauptungen.

---

## 3. Was ist riskant?

| # | Befund | Status | Risiko |
|---|--------|--------|--------|
| R1 | `pytest` lokal nicht ausführbar in dieser Umgebung; Testgrün nur via CI belegt | [FAKT] | Audit kann Suite nicht unabhängig bestätigen |
| R2 | `src/`, `tools/` ohne README — größte Code-Domänen ohne Einstiegspunkt | [FAKT] | Onboarding-/Drift-Risiko, kein „map of the territory" |
| R3 | Mehrere Tools ohne Tests: `metatron_check.py`, `mzm/gate_toggle.py`, `receipt_lint.py`, `status_verify.py`, `verify_cards.py` | [INFERENZ] | Guard-Werkzeuge selbst ungeprüft (Guard-the-guard-Lücke) |
| R4 | `src/meta_backprop.py`, `src/tools/cauchy_detector.py` scheinen ohne Importer/Tests | [HYPOTHESE] | Mögliche tote Pfade — **NICHT** löschen (G3), nur prüfen |
| R5 | Coverage-Gate bei nur 50 % | [FAKT] | Niedrige Schwelle; akzeptabel als Baseline, aber ausbaufähig |
| R6 | Kein CI-Gate für Markdown-Links / YAML-Validität / VOIDMAP-Schema | [FAKT] | Link-/Schema-Drift wird erst spät entdeckt |

**Wichtig zu R4:** „scheint unreferenziert" ist **[HYPOTHESE]**, nicht [FAKT]. Es
gab historische Commits mit `backprop`-Bezug (`docs/audit/2026-01-24_fix-pointer-traversal_backprop.md`).
Diese Dateien fallen unter **G3 (Deletion-Verbot)** und **SEMANTIC REVIEW** — sie
dürfen nicht automatisch entfernt werden.

---

## 4. Was ist doppelt?

**[FAKT]** Strukturelle Doppeldeutigkeit Audit-Verzeichnis:

- Es existiert `docs/audit/` (**Singular**, 19 Dateien — etablierter Kanon).
- Der Auftrag verlangt Deliverables unter `docs/audits/` (**Plural**).
- Es gibt **keine** Referenz auf `docs/audits/` irgendwo im Repo.

→ Ein neues `docs/audits/` neben `docs/audit/` zu erzeugen, wäre genau die Art von
stiller Duplikation, die dieser Audit aufdecken soll. **Entscheidung (siehe §8 und
ADR-0001):** Deliverables werden in das **bestehende `docs/audit/`** geschrieben;
die Plural-Variante wird **nicht** angelegt.

**[INFERENZ]** Weitere potenzielle, aber **bewusst akzeptierte** Doppelungen
(nicht „echte" Duplikate, sondern Schicht-Trennung):

- `docs/spec/` vs. `docs/specs/` (Singular/Plural koexistieren) — verschiedene
  Inhalte; **Review empfohlen**, aber nicht akut.
- `receipts/` (Top-Level) vs. `data/receipts/` vs. `ark/p4/receipts/` — mehrere
  Receipt-Pfade. **[FAKT]** Alle sind in `EPISTEMIC_HYGIENE.md` als IMMUTABLE
  benannt. Mehrgleisigkeit ist gewollt (Legacy + aktuell + ark), erhöht aber den
  Bedarf an einem **Receipt-Registry-Index** (siehe §7).
- `audit/` (Top-Level) vs. `docs/audit/` — Top-Level `audit/` enthält
  Snapshot-/Seed-Inputs (Makefile `SNAPSHOT_INPUTS`), nicht Audit-Reports;
  Namensgleichheit ist verwirrend, aber funktional getrennt. **Review-Frage.**

---

## 5. Was ist veraltet?

**[INFERENZ]** Wenig harte Fäulnis:

- Keine getrackten Dateien mit Datum vor 2026 gefunden; History beginnt 2026-01.
- `docs/audit/CONNECTIVITY_MAP.md` markiert eine frühere Methodik als
  „(deprecated)" — bewusste Kennzeichnung, kein toter Inhalt.
- TODO-Marker existieren v. a. in Audit-Logs als Audit-Trail (gewollt).
- `ci.yml` ist als „Legacy/advisory" gekennzeichnet; die blockierende Abdeckung
  liegt in dedizierten Workflows (Tests, Smoke, Policy, Metatron, DeepJump).
  **[INFERENZ]** Bewusste Migration, nicht Vergessen — aber zwei CI-Layer
  nebeneinander erhöhen die kognitive Last.

---

## 6. Was ist widersprüchlich?

**[FAKT]** Kein harter Widerspruch in der Claim-Disziplin gefunden. Insbesondere:

- Das in `docs/bridgecards/BC_consent_as_transit.md:9` verwendete Tag **`[FAKT]`**
  ist **kein** Fehler: `[FAKT]` ist Teil der **kanonischen** Claim-Taxonomie des
  Frameworks (siehe Auftrags-Essenzliste Punkt 4 und `EPISTEMIC_HYGIENE.md`).
  Deutsch/Englisch-Varianten koexistieren bewusst; eine erzwungene
  „Normalisierung" wäre eine **unerlaubte semantische Änderung**. → DO NOT TOUCH.

**[INFERENZ]** Latente Spannungen (kein Widerspruch, aber Klärungsbedarf):

- Doppelte Tag-Sprachen (`[FAKT]`/`[FACT]`, `[INFERENZ]`/`[INFERENCE]`) sind
  legitim, aber ohne zentrale **Term-/Claim-Registry** lässt sich Konsistenz nicht
  maschinell prüfen. → Empfehlung: Registry + optionaler `claim_lint`-Modus, der
  *warnt* (nicht blockiert) bei gemischten Sprachvarianten innerhalb einer Datei.
- `make verify` ≠ vollständige Abdeckung: Governance- und JS-Layer sind bewusst
  *nicht* in `verify` verdrahtet (Ergonomie-Entscheidung, im Makefile dokumentiert).
  **[INFERENZ]** Korrekt, aber leicht zu übersehen — Dokumentationswert hoch.

---

## 7. Was fehlt für Zukunftsfähigkeit?

**[MODELL]** Priorisierte Lücken (Vorschläge, keine Behauptung über Notwendigkeit):

| Bereich | Fehlt | Vorgeschlagene Phase |
|---------|-------|----------------------|
| Orientierung | `src/README.md`, `tools/README.md` | SAFE PATCH |
| Exchange / Handoff | `docs/exchange_archive/` (README/INDEX/TEMPLATE) | SAFE PATCH |
| Roadmap | `docs/roadmap/` (Zukunftsarchitektur) | SAFE PATCH |
| Decision Log | ADRs zu Struktur-Entscheidungen (Verzeichnis existiert) | SAFE PATCH |
| Claim Registry | Zentrale Liste kanonischer Claims + Status | REVIEW PATCH |
| Term Registry / Glossary | `docs/glossary/` mit kanonischen Begriffen + Claim-Grenze | REVIEW PATCH |
| Evidence Registry | Index über `evidence/`, `ark/p4/evidence/`, `docs/release/evidence/` | REVIEW PATCH |
| Receipt Registry | Index über `receipts/`, `data/receipts/`, `ark/p4/receipts/` | REVIEW PATCH |
| CI-Gates | Markdown-Linkcheck, YAML-Validity, VOIDMAP-Schema, Exchange-Index | REVIEW PATCH |
| Semantische Wächter | `claim_lint`-Erweiterung, `voidmap_lint`, `exchange_lint` (nur *warnend*) | SEMANTIC REVIEW |
| Canon/Variant-Trennung | Explizite `docs/canon/` vs. Varianten-Markierung | SEMANTIC REVIEW |

**[FAKT]** Bereits vorhanden (nicht neu zu bauen): CHANGELOG.md, SECURITY.md,
CONTRIBUTING.md, CODE_OF_CONDUCT.md, CODEOWNERS, Issue-Templates
(`void.yml`, `claim_correction.yml`), PR-Template, `docs/decisions/`, SBOM-Workflow,
Release-Workflow, `docs/governance/`.

---

## 8. Was darf NICHT automatisch geändert werden?

**DO NOT TOUCH WITHOUT USER CONSENT:**

1. **GOLD-Pfade** (`index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/`) —
   nur nach explizitem OK (G1).
2. **IMMUTABLE Receipts** (`data/receipts/`, `receipts/`, `ark/`) — nur Anhängen,
   nie Modifizieren/Umbenennen (G1).
3. **`docs/negations.md`** (Semi-GOLD, „Negative Theologie") — nur nach Diskussion.
4. **Claim-Tags** wie `[FAKT]`, `[POESIE]`, `[METAPHER]` — keine „Normalisierung"
   deutscher in englische Varianten; beide sind kanonisch.
5. **Poetische / symbolische Kerntexte** (`docs/narratives/`, Grimm-2.0,
   Nektar-Synapsen-Raum, `SYNTHBIOSIS.md`) — keine inhaltliche Umdeutung; keine
   Poesie-als-Beweis-Kollaps-Struktur erzeugen.
6. **Vermeintlich tote Dateien** (R4) — nicht löschen; G3 verlangt Verschieben
   nach `NICHTRAUM/archive/` und nur nach Consent.
7. **Branch-Operationen** — kein Force-Push, kein Branch-Löschen, kein Merge,
   kein Issue-Schließen ohne explizite Anweisung.

---

## 9. Vorschlag für Patch-Phasen

### SAFE PATCH (additiv, reversibel, keine Semantik berührt)
- `src/README.md` + `tools/README.md` (Orientierung, beschreibt vorhandenen Stand).
- `docs/exchange_archive/{README,INDEX,TEMPLATE_exchange_record}.md`.
- `docs/roadmap/revolutionary_forward_architecture_2026-06-16.md`.
- `docs/decisions/ADR-0001…` (Audit-Verzeichnis-Konsolidierung),
  `ADR-0002…` (Exchange-Archiv-Einführung).
- Dieser Auditbericht + Ergebnisbericht in `docs/audit/`.

### REVIEW PATCH (sinnvoll, aber menschlicher Review vor Merge)
- Registries (Claim/Term/Evidence/Receipt) als Index-Dokumente.
- Zusätzliche CI-Gates (Linkcheck, YAML, VOIDMAP-Schema) — als **nicht-blockierend**
  einführen, später härten.
- README-Ergänzung für weitere ANNEX-Ordner.

### SEMANTIC REVIEW REQUIRED (Bedeutung im Spiel)
- Semantische Wächter (`claim_lint`-Erweiterung, `voidmap_lint`, `exchange_lint`) —
  Design ja, Implementierung nur risikoarm und *warnend*.
- Canon/Variant-Verzeichnistrennung.
- Konsolidierung `docs/spec/` vs. `docs/specs/`, Top-Level `audit/` vs. `docs/audit/`.

### DO NOT TOUCH WITHOUT USER CONSENT
- Siehe §8 vollständig.

---

## 10. Offene Review-Fragen (an Kevin/Fleks)

- [ ] ☐ **Audit-Verzeichnis:** Ist die Konsolidierung in `docs/audit/` (statt neuem
  `docs/audits/`) gewünscht? (ADR-0001 trifft diese Annahme.)
- [ ] ☐ **`docs/spec/` vs. `docs/specs/`:** Zusammenführen oder bewusst getrennt?
- [ ] ☐ **Top-Level `audit/`** (Snapshot-Inputs) — umbenennen zur Entwirrung von
  `docs/audit/`? (Berührt Makefile `SNAPSHOT_INPUTS` → SEMANTIC REVIEW.)
- [ ] ☐ **R4 (vermeintlich tote Dateien):** Prüfen, ob `meta_backprop.py` /
  `cauchy_detector.py` archiviert werden sollen (G3: Verschieben, nicht löschen).
- [ ] ☐ **CI-Gates:** Sollen Linkcheck/YAML/VOIDMAP-Schema als blockierend oder
  zunächst nur advisory laufen?

---

## 11. Artefakte (dieser Phase)

- `docs/audit/revolutionary_repo_audit_2026-06-16.md` (dieser Bericht)

*Folge-Artefakte (Phase 2/3) siehe `revolutionary_repo_audit_result_2026-06-16.md`.*
