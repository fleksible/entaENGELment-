# Report: EntaENGELment Change-Gate Skill v0.1 — Abschlussbericht

**Datum:** 2026-07-24
**Fokus:** Change-Gate Skill v0.1
**Planbericht:** [`OUT/entaengelment_change_gate_v0_1_plan.md`](entaengelment_change_gate_v0_1_plan.md)
**Scope-Entscheidung aus Phase 2:** PROCEED_ANNEX_ONLY
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

| Datei | Zeilen | Inhalt |
|---|---|---|
| `.claude/skills/entaengelment-change-gate/SKILL.md` | 226 | Aktivierungsbereich, 5-Schritt-Ablauf, Guard-Semantik §4.1–4.8, Quellenbindungstabelle (21 Repo-Pfade) |
| `.claude/skills/entaengelment-change-gate/references/change-manifest-schema.md` | 176 | geschlossenes Feldschema, 22 Reason-Codes, Nicht-Äquivalenztabelle, deklarierte Verluste, Falsifikatoren |
| `.claude/skills/entaengelment-change-gate/templates/change-manifest.yaml` | 88 | leeres Arbeitstemplate mit Quellenkommentaren |
| `.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py` | 800 | deterministischer, offline, seiteneffektfreier Validator |
| `tests/unit/test_change_gate_manifest.py` | 559 | 62 Tests |

**Alle Änderungen sind additiv.** Keine bestehende Datei wurde geändert,
verschoben oder gelöscht (`git status` zeigt ausschließlich drei neue Pfade).

### Umgesetzte Guard-Semantik

| Anforderung | Umsetzung | Reason-Code(s) |
|---|---|---|
| Keine Selbstautorisierung | Freistehende Endattestierungen im gesamten Manifest werden erkannt; `[CANON]` in Klammern gilt als Registerreferenz, nicht als Attestierung | `FORBIDDEN_SELF_ATTESTATION`, `FINAL_PASS_NOT_PERMITTED` |
| Kein paralleles Governance-System | Keine neue Statusleiter; `GOVERNANCE_ADJACENT` ohne geprüfte Überschneidung ist fail-closed | `POSSIBLE_PARALLEL_SYSTEM` |
| Source-of-Truth-Bindung | `existing_sources_of_truth` ist Pflicht; Pfade werden gegen das Repository geprüft | `SOURCE_OF_TRUTH_PATH_MISSING`, `SOURCE_OF_TRUTH_PATH_ESCAPES_REPO` |
| GOLD-/IMMUTABLE-Schutz | Berührung ohne konkrete menschliche Frage → HOLD; GOLD in `allowed_paths` ohne Deklaration wird erkannt | `GOLD_PATH_REQUIRES_HUMAN_DECISION`, `GOLD_PATH_UNDECLARED`, `IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION`, `NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION` |
| Untrusted bleibt untrusted | `verification_commands` werden als Daten behandelt und nie ausgeführt; untrusted Eingaben verlangen deklarierten Verlust | `UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS` |
| Falsifikation vor Verstärkung | `falsifiers` ist Pflichtliste, `known_loss` bei `GOVERNANCE_ADJACENT` und untrusted Eingaben | `MISSING_KNOWN_LOSS` |
| Reversibilität | `IRREVERSIBLE` verlangt Rücknahmepfad **und** menschliche Frage | `IRREVERSIBLE_WITHOUT_ROLLBACK`, `IRREVERSIBLE_WITHOUT_HUMAN_DECISION` |
| Menschliche Entscheidung | Beantragte Authority-/Claim-Wirkung ohne HumanDecision; `required: true` ohne konkrete Frage | `PROMOTION_WITHOUT_HUMAN_DECISION`, `HUMAN_DECISION_WITHOUT_QUESTION` |
| Fail-closed Schema | geschlossenes Feldschema (Muster: `src/core/evidence_routing.py`) | `UNKNOWN_FIELD`, `UNKNOWN_ENUM_VALUE`, `MISSING_REQUIRED_FIELD`, `FIELD_TYPE_INVALID`, `EMPTY_REQUIRED_VALUE`, `MANIFEST_NOT_MAPPING`, `MANIFEST_UNPARSEABLE` |

---

## 2. Technisch verifiziert

Alle Läufe wurden tatsächlich ausgeführt; die Ergebnisse sind unverändert übernommen.

| Befehl | Ergebnis |
|---|---|
| `make verify` (Baseline **vor** dem Patch) | grün — 290 Tests, Pointer/Claims/Ports OK |
| `make verify-governance` (Baseline **vor** dem Patch) | grün — 14 Workflows, VOID-Backlog, UI-Drift OK |
| `make verify` (**nach** dem Patch) | grün — **352 passed in 2.50s**, „Core verify membrane passed" |
| `make verify-governance` (**nach** dem Patch) | grün — „Governance membrane checked" |
| `pytest tests/unit/test_change_gate_manifest.py -q` | **62 passed** |
| `ruff check src/ tools/ tests/` | „All checks passed!" |
| `black --check src/ tools/ tests/` | „87 files would be left unchanged" |
| `mypy src/ tools/` | „Success: no issues found in 43 source files" |
| `ruff` + `black` + `mypy` auf dem Validator (ausserhalb des Repo-Scope, manuell) | sauber bzw. „Success: no issues found in 1 source file" |
| CLI auf dem leeren Template | `HOLD`, Exit 1, 7 Befunde — das Template ist absichtlich noch kein gültiges Manifest |
| CLI auf dem ausgefüllten Selbst-Manifest dieser Änderung | `ELIGIBLE_FOR_EXTERNAL_REVIEW`, Exit 0 |

### Testabdeckung gegenüber den zwölf geforderten Fällen

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

### Zwei Befunde aus dem eigenen Lauf

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

**Neu (3 Pfade, additiv):**

```
.claude/skills/entaengelment-change-gate/SKILL.md
.claude/skills/entaengelment-change-gate/references/change-manifest-schema.md
.claude/skills/entaengelment-change-gate/templates/change-manifest.yaml
.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py
tests/unit/test_change_gate_manifest.py
OUT/entaengelment_change_gate_v0_1_plan.md
OUT/entaengelment_change_gate_v0_1_audit.md
```

**Geändert:** keine.
**Gelöscht/verschoben:** keine.

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

## 10. Offene Punkte

- [ ] ☐ Menschliche Entscheidungen aus §4.
- [ ] ☐ Folgearbeiten aus §6.
- [ ] ☐ Prüfung auf den CI-Matrix-Legs 3.10/3.12 (§3).

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
