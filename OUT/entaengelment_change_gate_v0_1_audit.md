# Report: EntaENGELment Change-Gate Skill v0.1 — Abschlussbericht

**Datum:** 2026-07-24 (Runde 1) · 2026-07-25 (Runde 2: Review-Nachbesserung)
**Fokus:** Change-Gate Skill v0.1
**Planbericht:** [`OUT/entaengelment_change_gate_v0_1_plan.md`](entaengelment_change_gate_v0_1_plan.md)
**Scope-Entscheidung aus Phase 2:** PROCEED_ANNEX_ONLY
**PR:** #323 (Draft)
**Abschlussstatus:** **ELIGIBLE_FOR_EXTERNAL_REVIEW**

> Der Abschlussstatus verwendet den bereits im Repository belegten Begriff aus
> `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §11 und entspricht dem im
> Auftrag genannten „PASS_CANDIDATE". Er ist **kein endgültiger PASS**, keine
> Freigabe, kein Claim-Status und kein Governance-Status. Er besagt nur: die
> Arbeit ist vollständig genug für eine menschliche Prüfung.
> Begründung der Wortwahl: §2.3 des Planberichts (`PASS_CANDIDATE` hat 0
> Repo-Treffer und wäre ein neuer Statuswert).

## Ziel

Einen ersten operativen Claude-Skill anlegen, der vor nichttrivialen Änderungen
**vorhandene** Repo-Regeln operationalisiert — ohne neue Source of Truth, ohne
Governance-Instanz, ohne semantische Autorität, ohne Ersatz für menschliche
Entscheidungen und ohne automatische Kanonisierung.

---

## 1. Technisch umgesetzt

Alle Zahlen unten sind mit `wc -l`, `pytest --collect-only` und einem
Konstanten-Scan über den Validator-Quelltext gegen den tatsächlichen Patch
geprüft (Stand: Runde 2).

| Datei | Zeilen | Inhalt |
|---|---|---|
| `.claude/skills/entaengelment-change-gate/SKILL.md` | 281 | Aktivierungsbereich, 5-Schritt-Ablauf, Guard-Semantik §4.1–4.8, Quellenbindungstabelle (21 Repo-Pfade) |
| `.claude/skills/entaengelment-change-gate/references/change-manifest-schema.md` | 271 | geschlossenes Feldschema, **29 Reason-Codes**, Nicht-Äquivalenztabelle, deklarierte Verluste, Falsifikatoren |
| `.claude/skills/entaengelment-change-gate/templates/change-manifest.yaml` | 93 | leeres Arbeitstemplate mit Quellenkommentaren |
| `.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py` | 924 | deterministischer, offline, seiteneffektfreier Validator |
| `tests/unit/test_change_gate_manifest.py` | 865 | **92 Tests** in 15 Testklassen |
| `OUT/entaengelment_change_gate_v0_1_plan.md` | 220 | Planbericht (Phase 2) |
| `OUT/entaengelment_change_gate_v0_1_audit.md` | dieses Dokument | Abschlussbericht |

**Alle Änderungen sind additiv.** Keine bestehende Datei wurde geändert,
verschoben oder gelöscht — `git diff origin/main --name-only` listet genau
**7 neue Dateien in 3 Bereichen** (`.claude/skills/…`, `tests/unit/`, `OUT/`).

### 1.1 Runde 2 — Review-Nachbesserung (Kohärenz Vertrag ↔ Code ↔ Tests)

Die konzeptionelle Architektur ist unverändert: kein neuer Source of Truth,
keine Governance-/Claim-Autorität, keine CI-/Make-Verdrahtung, keine
automatische Freigabe, additiv und reversibel.

| # | Befund | Umsetzung |
|---|---|---|
| 1 | Undeklarierte IMMUTABLE-/NICHTRAUM-Pfade liefen still durch (Finding nur für `gold`) | Neue Codes `IMMUTABLE_PATH_UNDECLARED`, `NICHTRAUM_PATH_UNDECLARED`; die drei geschützten Schichten liegen jetzt in einer Tabelle `PROTECTED_LAYERS` und werden symmetrisch geprüft |
| 2 | Fokus-Vertrag „2–5 Wörter" war dokumentiert, aber nicht ausführbar | `count_focus_words()` (whitespace-basiert, dokumentiert) + `FOCUS_WORD_COUNT_INVALID`; leerer Fokus bleibt reiner `EMPTY_REQUIRED_VALUE` |
| 3 | `REVERSIBLE` konnte ohne benannten Rücknahmepfad ein positives Verdikt erhalten | `REVERSIBLE_WITHOUT_ROLLBACK`; ein konkreter `rollback_path` ist in **beiden** Fällen Pflicht, `IRREVERSIBLE` zusätzlich mit HumanDecision |
| 4 | Doku nannte Exit 2 für Parsefehler, CLI gab 1 zurück | CLI trennt Eingabefehler vom Befund: Parsefehler → Exit **2** (Verdikt bleibt fail-closed `HOLD`); Docstring, Schema §5 und SKILL.md §Schritt 3 nennen dieselbe Semantik |
| 5 | `possible_parallel_system` erlaubte widersprüchliche Kombinationen | Aufteilung in `systems_checked` (wogegen geprüft) und `detected_overlaps` (was gefunden); `GOVERNANCE_ADJACENT` verlangt `systems_checked`, erkannte Überschneidung verlangt `mitigation`; die Altform erzeugt `UNKNOWN_FIELD` + `MISSING_REQUIRED_FIELD` und läuft nicht still durch |
| 6 | Audit sagte „3 Pfade", listete 7 Dateien | korrigiert; **alle** Strukturzahlen neu gegen den Patch geprüft (s. §1 und §5) |

Zusätzlich als Drift-Schutz eingezogen: `test_every_reason_code_is_documented_in_the_schema`
und `test_documented_reason_code_count_matches_the_code` — ein neuer Reason-Code
ohne Tabelleneintrag bricht die Suite, statt die Doku still veralten zu lassen.

### Umgesetzte Guard-Semantik

| Anforderung | Umsetzung | Reason-Code(s) |
|---|---|---|
| Keine Selbstautorisierung | Freistehende Endattestierungen im gesamten Manifest werden erkannt; `[CANON]` in Klammern gilt als Registerreferenz, nicht als Attestierung | `FORBIDDEN_SELF_ATTESTATION`, `FINAL_PASS_NOT_PERMITTED` |
| Kein paralleles Governance-System | Keine neue Statusleiter; `GOVERNANCE_ADJACENT` ohne benannte `systems_checked` ist fail-closed; erkannte Überschneidung verlangt `mitigation` | `POSSIBLE_PARALLEL_SYSTEM` |
| Source-of-Truth-Bindung | `existing_sources_of_truth` ist Pflicht; Pfade werden gegen das Repository geprüft | `SOURCE_OF_TRUTH_PATH_MISSING`, `SOURCE_OF_TRUTH_PATH_ESCAPES_REPO` |
| GOLD-/IMMUTABLE-/NICHTRAUM-Schutz | Berührung ohne konkrete menschliche Frage → HOLD; **jede** der drei Schichten wird zusätzlich auf undeklarierte Freigabe in `allowed_paths` geprüft | `GOLD_PATH_REQUIRES_HUMAN_DECISION`, `GOLD_PATH_UNDECLARED`, `IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION`, `IMMUTABLE_PATH_UNDECLARED`, `NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION`, `NICHTRAUM_PATH_UNDECLARED` |
| Untrusted bleibt untrusted | `verification_commands` werden als Daten behandelt und nie ausgeführt; untrusted Eingaben verlangen deklarierten Verlust | `UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS` |
| Falsifikation vor Verstärkung | `falsifiers` ist Pflichtliste, `known_loss` bei `GOVERNANCE_ADJACENT` und untrusted Eingaben | `MISSING_KNOWN_LOSS` |
| Reversibilität | Ein konkreter Rücknahmepfad ist in **beiden** Fällen Pflicht; `IRREVERSIBLE` zusätzlich mit konkreter menschlicher Frage | `REVERSIBLE_WITHOUT_ROLLBACK`, `IRREVERSIBLE_WITHOUT_ROLLBACK`, `IRREVERSIBLE_WITHOUT_HUMAN_DECISION` |
| Fokus-Bindung (G4) | Fokus-Vertrag 2–5 Wörter ist ausführbar, whitespace-basiert gezählt | `FOCUS_WORD_COUNT_INVALID` |
| Menschliche Entscheidung | Beantragte Authority-/Claim-Wirkung ohne HumanDecision; `required: true` ohne konkrete Frage | `PROMOTION_WITHOUT_HUMAN_DECISION`, `HUMAN_DECISION_WITHOUT_QUESTION` |
| Fail-closed Schema | geschlossenes Feldschema (Muster: `src/core/evidence_routing.py`) | `UNKNOWN_FIELD`, `UNKNOWN_ENUM_VALUE`, `MISSING_REQUIRED_FIELD`, `FIELD_TYPE_INVALID`, `EMPTY_REQUIRED_VALUE`, `MANIFEST_NOT_MAPPING`, `MANIFEST_UNPARSEABLE` |

---

## 2. Technisch verifiziert

Alle Läufe wurden tatsächlich ausgeführt; die Ergebnisse sind unverändert übernommen.

| Befehl | Ergebnis (Runde 2, tatsächlich ausgeführt) |
|---|---|
| `make verify` (Baseline **vor** dem Patch) | grün — 290 Tests, Pointer/Claims/Ports OK |
| `make verify-governance` (Baseline **vor** dem Patch) | grün — 14 Workflows, VOID-Backlog, UI-Drift OK |
| `make verify` (**nach** Runde 2) | grün — **382 passed in 9.16s**, „Core verify membrane passed" |
| `make verify-governance` (**nach** Runde 2) | grün — „Governance membrane checked", 22 VOIDs in sync |
| `pytest tests/unit/test_change_gate_manifest.py -q` | **92 passed** (Runde 1: 62) |
| `ruff check src/ tools/ tests/` | „All checks passed!" |
| `black --check src/ tools/ tests/` | „87 files would be left unchanged" |
| `mypy src/ tools/` | „Success: no issues found in 43 source files" |
| `ruff` + `black` + `mypy` auf dem Validator (ausserhalb des Repo-Lint-Scope, manuell) | sauber bzw. „Success: no issues found in 1 source file" |

382 = 290 Baseline + 92 neue Tests. Die Differenz ist vollständig durch diesen
Patch erklärt; keine bestehende Testdatei wurde angefasst.

### Dogfooding (fünf geforderte Fälle, alle ausgeführt)

| Fall | Erwartet | Tatsächlich |
|---|---|---|
| leeres Template | `HOLD` | `HOLD`, Exit 1, 7 Befunde (`EMPTY_REQUIRED_VALUE`) |
| korrekt ausgefülltes ANNEX-Manifest | `ELIGIBLE_FOR_EXTERNAL_REVIEW` | `ELIGIBLE_FOR_EXTERNAL_REVIEW`, Exit 0, keine Befunde |
| undeklarierter IMMUTABLE-Pfad (`data/receipts/…`) | `HOLD` | `HOLD`, Exit 1, `IMMUTABLE_PATH_UNDECLARED` |
| undeklarierter NICHTRAUM-Pfad | `HOLD` | `HOLD`, Exit 1, `NICHTRAUM_PATH_UNDECLARED` |
| ungültiges YAML | Exit `2` | Exit **2**, Verdikt `HOLD`, `MANIFEST_UNPARSEABLE` |

### Testabdeckung gegenüber den zwölf geforderten Fällen (Runde 1)

| # | Geforderter Fall | Testklasse | Status |
|---|---|---|---|
| 1 | valides minimales ANNEX-Manifest | `TestMinimalAnnexManifest` | abgedeckt |
| 2 | fehlendes Pflichtfeld | `TestMissingRequiredField` | abgedeckt |
| 3 | unbekannter Enum-Wert | `TestUnknownValues` | abgedeckt |
| 4 | GOLD-Änderung ohne HumanDecision | `TestGoldBoundary` | abgedeckt |
| 5 | HumanDecision ohne konkrete Frage | `TestHumanDecisionQuestions` | abgedeckt |
| 6 | endgültige Selbstattestierung | `TestSelfAttestation` | abgedeckt |
| 7 | endgültiger `PASS` | `TestFinalPass` | abgedeckt |
| 8 | mögliches paralleles Statussystem | `TestParallelSystem` | abgedeckt |
| 9 | widersprüchliche Pfadfreigaben | `TestPathConflicts` | abgedeckt |
| 10 | Determinismus | `TestDeterminism` | abgedeckt (inkl. Schlüsselreihenfolge) |
| 11 | keine Netzwerk-/Prozess-/Write-Nebenwirkungen | `TestNoSideEffects` | abgedeckt (Import-Scan, Write-Sperre, leeres tmp-Verzeichnis) |
| 12 | Source-of-Truth-Pfade werden verlangt/geprüft | `TestSourceOfTruthBinding` | abgedeckt (inkl. Drift-Check der Pfadklassen) |

### Zusätzliche Testabdeckung aus Runde 2

| Befund | Testklasse / Tests |
|---|---|
| undeklarierte geschützte Pfade | `TestUndeclaredProtectedPaths` (6 Tests: `data/receipts/…`, `receipts/…`, `NICHTRAUM/…`, korrekt deklariert ohne HumanDecision je Schicht, deklariert + Frage, Layer-Tabellen-Drift) |
| Fokus-Wortzahl | `TestFocusWordCount` (4 Grenzfälle 1/2/5/6 Wörter, Whitespace-Idempotenz, leerer Fokus, Zählfunktion) |
| Rücknahmepfad | `TestSourceOfTruthBinding` (5 Tests: `REVERSIBLE` leer/gefüllt, `IRREVERSIBLE` ohne/mit Pfad, keine Funktionsbehauptung) |
| Exit-Codes | `TestTemplateAndCli` (0 / 1 bei Finding / 1 bei selbst deklariertem HOLD / 2 bei kaputtem YAML / 2 bei fehlender Datei, JSON-Determinismus, Docstring-Abgleich) |
| `possible_parallel_system` | `TestParallelSystem` (geprüft ohne Überschneidung, Überschneidung ohne/mit Mitigation, Altform, widersprüchliche Altform) |
| Doku-Drift | `test_every_reason_code_is_documented_in_the_schema`, `test_documented_reason_code_count_matches_the_code` |

### Zwei Befunde aus dem eigenen Lauf (Runde 1)

1. **Drift sichtbar gemacht:** Der Herkunftstest schlug zunächst fehl, weil
   `NICHTRAUM/` **nicht** in `.claude/rules/annex.md` steht, sondern in
   `CLAUDE.md` (G2). Korrigiert wurde die Quellenangabe im Validator, nicht die
   Assertion. `annex.md` blieb unverändert.
2. **Dokumentierter Fehlalarm bestätigt:** Das Selbst-Manifest dieser Änderung
   erhielt zunächst `HOLD` mit `FINAL_PASS_NOT_PERMITTED`, weil ein
   `known_loss`-Eintrag die Verbotsregel **wörtlich zitierte**. Das ist das im
   Schema §6 deklarierte Verhalten (fail-closed vor stiller Durchlassung).
   Geändert wurde die Formulierung des Zitats, nicht die Regel.

---

## 3. Nicht verifiziert

- **`make verify-js`** wurde **nicht** ausgeführt und ist für diesen Patch
  nicht einschlägig: keine der Dateien liegt im `paths`-Filter von
  `ci-js-workspace.yml` (`ui-app/`, `packages/`, `pnpm-lock.yaml`,
  `pnpm-workspace.yaml`, `package.json`, `turbo.json`, `tsconfig.base.json`).
- **`make status` / `make snapshot` / `make all`** wurden nicht ausgeführt.
  Kein HMAC-Secret gesetzt; der Patch erzeugt keine Receipts und keine Seeds.
- **Python 3.9/3.10/3.12** wurden nicht geprüft. Verfügbar war nur Python
  3.11.15. Der Code nutzt `from __future__ import annotations` und keine
  Syntax jenseits von 3.9, ist auf diesen Legs aber **nicht ausgeführt** worden.
- **Verhalten in einer echten Claude-Session** (Aktivierungstreffsicherheit der
  `description`) ist nicht gemessen. Der Skill wurde als Skill registriert, aber
  keine Trigger-Evaluation durchgeführt.
- **Inhaltliche Richtigkeit** eines Manifests wird vom Validator grundsätzlich
  nicht geprüft — nur Struktur (deklarierter Verlust).
- **Funktionsfähigkeit eines `rollback_path`** wird nicht geprüft. Der Validator
  stellt nur fest, **dass** ein Pfad konkret deklariert ist.
- **Semantische Qualität von `systems_checked`/`detected_overlaps`** wird nicht
  geprüft. Ob die genannten Systeme die *richtigen* sind, bleibt menschliche
  Review-Arbeit; der Validator zählt nur, ob etwas benannt wurde.
- **CI-Ergebnis auf PR #323** für Runde 2 lag zum Zeitpunkt dieses Berichts
  noch nicht vor (Push erfolgt mit diesem Commit).

---

## 4. Menschlich zu entscheiden

- [ ] ☐ Soll `.claude/` in `.claude/rules/annex.md` explizit klassifiziert
      werden? Es ist derzeit weder GOLD noch ANNEX noch IMMUTABLE noch
      NICHTRAUM. Behandlung in diesem Patch: additiv-ANNEX auf ausdrückliche
      Anweisung, rein additiv, ohne Änderung an einer Regeldatei.
- [ ] ☐ Ist `ELIGIBLE_FOR_EXTERNAL_REVIEW` als gate-lokale Formulierung
      bestätigt, oder soll ein anderer bestehender Begriff verwendet werden?
- [ ] ☐ Ist die Wiederverwendung des Wortes `HOLD` in gate-lokaler Rolle
      akzeptabel (analog zur Mehrfachbelegung in M5/ERK/tesser3TAKT)?
- [ ] ☐ Soll der Validator später advisory in ein Make-Target oder eine
      CI-Stufe wandern? Dann greift `docs/governance/GUARD_CHECK_CONTRACT_v0_1.md`.
- [ ] ☐ Soll der Skill in `docs/masterindex.md` oder `tools/README.md`
      verlinkt werden?
- [ ] ☐ Ist der Wertebereich `none | requested` für `authority_effect` und
      `claim_effect` richtig gewählt? Nur `none` war im Repository attestiert.
- [ ] ☐ **(Runde 2)** Sind die Fokus-Grenzen 2–5 Wörter als *harte* Schranke
      gewollt? `.claude/rules/metatron.md` nennt „2-5 Wörter"; der Gate setzt
      das jetzt durchsetzend um. Ein längerer Fokus ist damit HOLD, nicht nur
      unschön.
- [ ] ☐ **(Runde 2)** Soll ein konkreter `rollback_path` auch bei `REVERSIBLE`
      Pflicht bleiben? Der Vertrag ist damit strenger als der frühere Code,
      aber deckungsgleich mit `SKILL.md` §4.6/§4.7 und G3.
- [ ] ☐ **(Runde 2)** Ist die Aufteilung `systems_checked` /
      `detected_overlaps` die gewünschte Form? Die frühere Form
      (`detected`/`overlaps`) ist damit ungültig — v0.1 ist Draft und nicht
      extern verdrahtet, ein Kompatibilitätspfad wurde bewusst nicht gebaut.

---

## 5. Bewusst nicht getan

- **Keine Migration** von `.claude/skills/witness_mode.md` (Folgearbeit, §6).
- **Keine Änderung** an GOLD (`index/`, `policies/`, `spec/`, `seeds/`,
  `VOIDMAP.yml`), IMMUTABLE (`data/receipts/`, `receipts/`), `NICHTRAUM/`,
  `.claude/rules/*`, `CLAUDE.md`, `Makefile`, `.github/workflows/`, `tools/`.
- **Keine Verdrahtung** in `make verify` oder CI — eine Guard-Regel ohne
  stabilisierten Check darf nicht als live enforced gelten
  (`GUARD_CHECK_CONTRACT_v0_1.md`).
- **Keine neuen** Claim-Tags, globalen Statuswerte, Authority-Klassen oder
  VOID-Einträge.
- **Kein Eintrag** in `tools/README.md`: der Validator ist bewusst **keine**
  Governance-Membran und liegt deshalb nicht unter `tools/`.
- **Keine Löschung, keine Verschiebung, keine stille Migration.**
- **Kein Merge, kein Release, keine Statuspromotion.**
- Manifeste werden **nicht** automatisch persistiert; das Selbst-Manifest
  dieser Änderung blieb Arbeitsartefakt ausserhalb des Repos.

---

## 6. Erkannte Folgearbeit (nur dokumentiert, nicht umgesetzt)

1. **Witness-Skill-Migration:** `.claude/skills/witness_mode.md` in die
   Verzeichnisform mit `SKILL.md` überführen. Berührt eine bestehende Datei →
   eigener Patch, eigene Entscheidung.
2. **`.claude/`-Klassifikation** in `.claude/rules/annex.md` ergänzen.
3. **Gemeinsame Pfadklassen-Quelle:** GOLD/IMMUTABLE/NICHTRAUM stehen heute in
   zwei Regeldateien und als Kopie im Validator. Eine maschinenlesbare Quelle
   würde die Kopie überflüssig machen — das wäre allerdings eine
   GOLD-nahe Strukturentscheidung.
4. **Advisory-Verdrahtung** des Validators nach Stabilisierung.
5. **Fehlende Guard-the-Guard-Tests** für `metatron_check.py`,
   `receipt_lint.py`, `status_verify.py`, `verify_cards.py`,
   `mzm/gate_toggle.py` (bereits in `tools/README.md` als offen vermerkt) —
   ausserhalb dieses Fokus, kein Fokus-Switch vorgenommen.

---

## 7. Cloud-Umgebungseinschränkungen

| Einschränkung | Auswirkung | Umgang |
|---|---|---|
| `pip install -r requirements-dev.txt` brach beim Paket `safety` ab (System-`cryptography` ohne RECORD-Datei nicht deinstallierbar) | `safety` fehlt; `jsonschema` musste separat installiert werden | `safety` wird von `make verify`/`verify-governance` nicht benötigt; `jsonschema` nachinstalliert |
| Auf `PATH` lag ein uv-verwaltetes `pytest` ohne die Projekt-Dependencies; `make test` schlug dadurch mit `INTERNALERROR` fehl | betrifft die Umgebung, nicht das Repository | Alle Läufe mit `PATH=/usr/local/bin:$PATH`, damit das pip-installierte `pytest` greift. Die Baseline wurde unter denselben Bedingungen erhoben. |
| Nur Python 3.11.15 verfügbar | CI-Matrix-Legs 3.10/3.12 nicht lokal reproduzierbar | in §3 als nicht verifiziert ausgewiesen |
| pnpm/Turbo nicht ausgeführt | `make verify-js` nicht gelaufen | für diesen Patch nicht einschlägig (§3) |

Alle Arbeiten fanden ausschließlich im bereitgestellten Repository-Workspace
statt. Keine Secrets gelesen, keine globalen Pakete/MCP-Server/Systemabhängigkeiten
installiert, keine Repository-Einstellungen, Branch-Protection-Regeln oder
externen Dienste verändert. Netzwerk nur für die repo-definierte
Dependency-Installation.

---

## 8. Veränderte Dateien

**Neu: 7 Dateien in 3 Bereichen, vollständig additiv.**
Quelle der Zahl: `git diff origin/main --name-only` (7 Einträge).

```
.claude/skills/entaengelment-change-gate/SKILL.md                          (281 Zeilen)
.claude/skills/entaengelment-change-gate/references/change-manifest-schema.md  (271)
.claude/skills/entaengelment-change-gate/templates/change-manifest.yaml     (93)
.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py (924)
tests/unit/test_change_gate_manifest.py                                    (865)
OUT/entaengelment_change_gate_v0_1_plan.md                                 (220)
OUT/entaengelment_change_gate_v0_1_audit.md                                (dieses Dokument)
```

In Runde 2 geändert wurden ausschließlich Dateien aus dieser Liste:
`scripts/validate_change_manifest.py`, `references/change-manifest-schema.md`,
`templates/change-manifest.yaml`, `SKILL.md`,
`tests/unit/test_change_gate_manifest.py`, dieser Bericht.

**Bestehende Dateien geändert:** keine.
**Gelöscht/verschoben:** keine.

### Geprüfte Strukturzahlen (gegen den tatsächlichen Patch)

| Größe | Wert | Ermittelt durch |
|---|---|---|
| neue Dateien | 7 (in 3 Bereichen) | `git diff origin/main --name-only` |
| geänderte bestehende Dateien | 0 | ebd. |
| Reason-Codes | 29 | Konstanten-Scan über den Validator-Quelltext |
| Tests in der Suite | 92 | `pytest --collect-only -q` |
| Testklassen | 15 | `grep -c "^class Test"` |
| Tests gesamt in `make verify` | 382 (= 290 Baseline + 92) | Testlauf |
| geforderte Fälle Runde 1 | 12, alle abgedeckt | §2 |
| geforderte Fälle Runde 2 | 6 Befunde, alle abgedeckt | §1.1 |
| Zeilenzahlen | s. Liste oben | `wc -l` |

---

## 9. Risiken

- **[RISK]** Die Pfadklassen im Validator sind Kopien aus `annex.md` bzw.
  `CLAUDE.md`. Gegenmaßnahme: zwei Herkunftstests; Drift wird sichtbar.
- **[RISK]** `ELIGIBLE_FOR_EXTERNAL_REVIEW` und `HOLD` stammen aus einem
  Forschungs-Gate. Gegenmaßnahme: ausdrückliche gate-lokale Scoping-Notiz in
  `SKILL.md` §4.2 und im Schema §2.4, analog zur HOLD-Regel in M5 §9.
- **[RISK]** Der Validator liegt ausserhalb des CI-Lint-Scope
  (`src/ tools/ tests/`). Gegenmaßnahme: `ruff`/`black`/`mypy` manuell sauber;
  die Tests laufen in `make verify` mit.
- **[RISK]** Ein strukturell vollständiges Manifest kann fachlich falsch sein.
  Das ist deklarierter Verlust, kein behobener Mangel.

---

## 10. Verbleibende bekannte Verluste

Diese Verluste sind **deklariert, nicht behoben** — sie stehen so auch in
`references/change-manifest-schema.md` §6:

1. Der Validator prüft **Struktur, nicht Inhalt**. Ein formal vollständiges
   Manifest kann fachlich falsch sein.
2. Das Wort `GOLD` wird **nicht** als Selbstattestierung geprüft, weil es in
   Manifesten legitim als Schichtname vorkommt. GOLD-Wirkung wird ausschließlich
   über die Pfadregeln erfasst.
3. Ein Manifest, das die Verbotsregel zum Endzustand **wörtlich zitiert**, löst
   `FINAL_PASS_NOT_PERMITTED` aus. Fail-closed vor stiller Durchlassung.
4. Die Pfadklassen sind **Kopien** aus `.claude/rules/annex.md` (GOLD,
   IMMUTABLE) bzw. `CLAUDE.md` (NICHTRAUM). Es gibt keine gemeinsame
   maschinenlesbare Quelle; zwei Tests machen Drift sichtbar.
5. Der Validator liegt **außerhalb** des CI-Lint-Scope (`src/ tools/ tests/`);
   `ruff`/`black`/`mypy` laufen dort nur manuell.
6. Die Wortzählung im Fokus ist **rein whitespace-basiert**. `Change-Gate Skill`
   zählt als zwei Wörter; Komposita, Bindestriche und Abkürzungen werden nicht
   analysiert.
7. Ein deklarierter `rollback_path` wird **nicht auf Funktionsfähigkeit**
   geprüft — nur auf Vorhandensein.
8. `systems_checked` wird **nicht auf Vollständigkeit oder Eignung** geprüft.
   Der Gate erkennt „nichts benannt", nicht „das Falsche benannt".
9. Der Validator kennt weiterhin **keine** VOIDs, Receipts, Ledger-Events oder
   Policy-Digests.

---

## 11. Offene Punkte

- [ ] ☐ Menschliche Entscheidungen aus §4 (inkl. drei neue aus Runde 2).
- [ ] ☐ Folgearbeiten aus §6.
- [ ] ☐ Prüfung auf den CI-Matrix-Legs 3.10/3.12 (§3).
- [ ] ☐ CI-Ergebnis von PR #323 nach dem Runde-2-Push.

---

## Artefakte

- `.claude/skills/entaengelment-change-gate/` (4 Dateien)
- `tests/unit/test_change_gate_manifest.py`
- `OUT/entaengelment_change_gate_v0_1_plan.md`
- `OUT/entaengelment_change_gate_v0_1_audit.md`

---

*Abschlussstatus: **ELIGIBLE_FOR_EXTERNAL_REVIEW** — kein endgültiger PASS,
keine Freigabe, kein Claim-Status. Ein technisch erfolgreicher Lauf ist ein
begrenzter technischer Befund und ersetzt keine menschliche Entscheidung.*
