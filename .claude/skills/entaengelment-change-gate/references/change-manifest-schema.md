# Change-Manifest — Feldschema und Reason-Codes (v0.1)

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** none (nicht in `make verify` oder CI verdrahtet)
**Human-Decision-Boundary:** required
**Promotion-Effect:** none

Dieses Dokument beschreibt ein **lokales Prüf- und Planungsartefakt**. Es ist
keine Source of Truth, kein Claim-Register, kein Policy-Schema und kein
Receipt. Es macht keine Aussage wahr — es macht den Prüfstand einer geplanten
Änderung nachvollziehbar (vgl. `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md`
§5: „SoT macht Claims nicht wahr").

---

## 1. Geschlossenes Feldschema

Unbekannte Felder werden fail-closed abgelehnt (Muster:
`src/core/evidence_routing.py`, geschlossenes Feldschema).

| Feld | Typ | Pflicht | Darf leer sein | Werte |
|---|---|---|---|---|
| `focus` | String | ja | nein | 2–5 Wörter (G4), **geprüft** — s. §2.5 |
| `requested_change` | String | ja | nein | Freitext |
| `change_class` | Liste[String] | ja | nein | s. §2.1 |
| `affected_layers` | Mapping | ja | — | Schlüssel: `gold`, `annex`, `immutable`, `nichtraum`, `untrusted_inputs`; Werte je Liste[String] |
| `existing_sources_of_truth` | Liste[String] | ja | nein | repo-relative Pfade |
| `authority_effect` | Mapping | ja | — | `value` (s. §2.2), `explanation` (String) |
| `claim_effect` | Mapping | ja | — | `value` (s. §2.2), `explanation` (String) |
| `human_decision` | Mapping | ja | — | `required` (Bool), `questions` (Liste[String]) |
| `possible_parallel_system` | Mapping | ja | — | `systems_checked` (Liste[String]), `detected_overlaps` (Liste[String]), `mitigation` (String) — s. §2.6 |
| `known_loss` | Liste[String] | ja | ja¹ | Freitext |
| `falsifiers` | Liste[String] | ja | nein | Freitext |
| `reversibility` | Mapping | ja | — | `value` (s. §2.3), `rollback_path` (String) |
| `allowed_paths` | Liste[String] | ja | nein | repo-relative Pfade |
| `forbidden_paths` | Liste[String] | ja | ja | repo-relative Pfade |
| `verification_commands` | Liste[String] | ja | nein | vorhandene Repo-Kommandos |
| `expected_gate_outcome` | String | ja | nein | s. §2.4 |
| `unresolved_points` | Liste[String] | ja | ja | Freitext |

¹ `known_loss` darf leer bleiben, **außer** bei `GOVERNANCE_ADJACENT` oder bei
nicht leeren `affected_layers.untrusted_inputs`.

## 2. Wertebereiche

### 2.1 `change_class`

`DOCUMENTATION` · `CODE` · `TEST` · `TOOLING` · `WORKFLOW` ·
`GOVERNANCE_ADJACENT` · `CLASSIFICATION_UNDETERMINED`

`CLASSIFICATION_UNDETERMINED` ist der wörtliche Repo-Begriff aus
`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §2: Mehrdeutiges bleibt
unentschieden; es gibt **keine** automatische Wahl der stärkeren Klasse.

### 2.2 `authority_effect.value` / `claim_effect.value`

`none` · `requested`

`none` ist der im Repository attestierte Wert (Kopfblöcke in
`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`).
`requested` drückt einen **Antrag** aus, nie eine Gewährung. Ein Antrag
erzwingt eine menschliche Entscheidung.

### 2.3 `reversibility.value`

`REVERSIBLE` · `IRREVERSIBLE` — `rollback_path` entspricht dem
„Rücknahmepfad" aus `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §3.

Ein **konkreter `rollback_path` ist in beiden Fällen Pflicht** (`CLAUDE.md` G3
„Reversibilität erhalten"; ebd. §3 nennt für jede Stufe einen Rücknahmepfad).
`IRREVERSIBLE` verlangt **zusätzlich** eine konkrete menschliche
Entscheidungsfrage.

Der Validator prüft ausschließlich, **ob** ein Rücknahmepfad konkret deklariert
ist. Er behauptet **nicht**, dass dieser Pfad fachlich funktioniert.

### 2.4 `expected_gate_outcome`

`HOLD` · `ELIGIBLE_FOR_EXTERNAL_REVIEW`

Beide Werte sind bereits im Repository belegt und dort ausdrücklich als
**beschreibende ANNEX-Formulierung, nicht als Runtime-Status und nicht als
Claim-Tag** markiert (`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §11).

**`HOLD` ist hier gate-lokal.** Es ist ausdrücklich *nicht* automatisch
tesser3TAKT-Navigations-HOLD, *nicht* ERK-Guard-HOLD und *nicht* Claim-`[VOID]`
(ebd. §9: „Das Wort HOLD besitzt verschiedene lokale Rollen … Keine
automatische Übersetzung").

### 2.5 `focus` — Wortzahl

Quelle: `.claude/rules/metatron.md` („`FOKUS: <2-5 Wörter die das Ziel
beschreiben>`"). Der Vertrag ist ausführbar: weniger als 2 oder mehr als 5
Wörter → `FOCUS_WORD_COUNT_INVALID`.

Gezählt wird **whitespace-basiert** (`str.split()`): beliebige Whitespace-Folgen
gelten als ein Trenner, zusätzlicher Whitespace verändert das Ergebnis nicht.
Keine linguistische Tokenisierung — `Change-Gate Skill` zählt als **zwei**
Wörter. Ein leerer Fokus wird nur als `EMPTY_REQUIRED_VALUE` gemeldet, nicht
zusätzlich als Wortzahlverletzung.

### 2.6 `possible_parallel_system`

Zwei getrennte Bedeutungen, damit „geprüft" und „gefunden" nicht kollabieren:

| Feld | Bedeutung |
|---|---|
| `systems_checked` | bestehende Systeme, **gegen die geprüft wurde** |
| `detected_overlaps` | **tatsächlich erkannte** Überschneidungen |
| `mitigation` | Gegenmaßnahme; Pflicht, sobald `detected_overlaps` nicht leer ist |

Invarianten:

- `GOVERNANCE_ADJACENT` in `change_class` ⇒ `systems_checked` darf **nicht leer**
  sein. Fail-closed: eine ungeprüfte Behauptung „kein Parallelsystem" ist kein
  Nachweis.
- `detected_overlaps` nicht leer ⇒ `mitigation` darf **nicht leer** sein.
- Ein leeres `detected_overlaps` bedeutet **nur**: keine Überschneidung
  deklariert gefunden. Es bedeutet **nicht**, dass keine Prüfung stattfand —
  diese Aussage trägt allein `systems_checked`.

Die frühere Form (`detected: Bool` plus `overlaps`) ist **nicht** mehr gültig.
Weil das Feldschema geschlossen ist, erzeugt sie `UNKNOWN_FIELD` und
`MISSING_REQUIRED_FIELD` — widersprüchliche Altsemantik (`detected: true` bei
leeren `overlaps`) läuft nicht still durch.

## 3. Nicht-Äquivalenztabelle

Vier Übergangs-/Entscheidungssysteme existieren im Repository und dürfen
**nicht** gleichgesetzt werden (`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §11):

| System | Werte | Quelle | Verhältnis zu diesem Manifest |
|---|---|---|---|
| Claim-Tag-Register | `ROHSEDIMENT` … `[CANON]` | `policies/claim_tags_v0_2.yaml` (GOLD) | nur gelesen/referenziert; das Manifest ändert keinen Tag |
| ERK `GuardDecision` | `PROPOSE` \| `HOLD` \| `STOP` | `src/core/evidence_routing.py` | nicht importiert, nicht dupliziert |
| ERK `HumanDecision` | `APPROVE` \| `REJECT` \| `DEFER` \| `WITHDRAW` | ebd. | der Agent nimmt keinen dieser Werte vorweg |
| tesser3TAKT Assembly-Navi | `PASS` \| `HOLD` \| `LOOP` \| `STOP` | `docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md` §9 | anderes System (Navigation), nicht übersetzt |

Die Reason-Codes in §4 sind **lokale Codes dieses Validators**. Sie sind nicht
die `ReasonCode`-Werte aus `src/core/evidence_routing.py`, werden nie in
Ledger, Receipts oder Events geschrieben und begründen keinen Projektstatus.

## 4. Reason-Codes

Insgesamt **29 Reason-Codes**. Ein Test (`test_every_reason_code_is_documented_in_the_schema`,
`test_documented_reason_code_count_matches_the_code`) hält Code und diese
Tabelle deckungsgleich; Drift wird sichtbar, statt still zu bleiben.

### 4.1 Struktur (8)

| Code | Auslöser |
|---|---|
| `MANIFEST_UNPARSEABLE` | YAML nicht parsebar (`yaml.safe_load`) |
| `MANIFEST_NOT_MAPPING` | Wurzelknoten ist kein Mapping |
| `MISSING_REQUIRED_FIELD` | Pflichtfeld fehlt |
| `UNKNOWN_FIELD` | Feld nicht im geschlossenen Schema |
| `FIELD_TYPE_INVALID` | falscher Typ |
| `EMPTY_REQUIRED_VALUE` | leerer Pflichtwert / leere Pflichtliste |
| `UNKNOWN_ENUM_VALUE` | Wert außerhalb des Wertebereichs |
| `FOCUS_WORD_COUNT_INVALID` | `focus` hat weniger als 2 oder mehr als 5 Wörter (§2.5) |

### 4.2 Selbstautorisierung (2)

| Code | Auslöser |
|---|---|
| `FORBIDDEN_SELF_ATTESTATION` | freistehendes `VALIDATED`, `PROVEN`, `SAFE`, `CANON`, `TRUE`, `CLINICALLY_READY`, `ETHICALLY_APPROVED`, `AUTO_APPROVED`, `SELF_VALIDATED` in einem Manifestwert |
| `FINAL_PASS_NOT_PERMITTED` | freistehendes `PASS` als erwarteter Agentenzustand |

Ein in eckigen Klammern stehender Tag (`[CANON]`) gilt als **Referenz** auf das
Claim-Register und wird nicht als Selbstattestierung gewertet.

### 4.3 Schichtgrenzen (8)

Jede der drei geschützten Schichten hat **zwei** Codes: einen für die fehlende
menschliche Entscheidung und einen für eine Freigabe ohne Deklaration. Ein
geschützter Pfad in `allowed_paths` muss in der zugehörigen
`affected_layers`-Liste stehen — sonst entfiele die HumanDecision-Pflicht
still. Nach korrekter Deklaration greift weiterhin die Pflicht zur konkreten
menschlichen Frage.

| Code | Auslöser |
|---|---|
| `GOLD_PATH_REQUIRES_HUMAN_DECISION` | `affected_layers.gold` nicht leer ohne konkrete menschliche Frage |
| `GOLD_PATH_UNDECLARED` | GOLD-Pfad in `allowed_paths`, aber nicht in `affected_layers.gold` |
| `IMMUTABLE_PATH_REQUIRES_HUMAN_DECISION` | `affected_layers.immutable` nicht leer ohne konkrete Frage |
| `IMMUTABLE_PATH_UNDECLARED` | IMMUTABLE-Pfad (`data/receipts/`, `receipts/`) in `allowed_paths`, aber nicht in `affected_layers.immutable` |
| `NICHTRAUM_PATH_REQUIRES_HUMAN_DECISION` | `affected_layers.nichtraum` nicht leer ohne konkrete Frage |
| `NICHTRAUM_PATH_UNDECLARED` | NICHTRAUM-Pfad in `allowed_paths`, aber nicht in `affected_layers.nichtraum` |
| `PATH_ALLOWLIST_CONFLICT` | Pfad gleichzeitig in `allowed_paths` und `forbidden_paths` (inkl. Unterpfad) |
| `UNTRUSTED_INPUT_WITHOUT_DECLARED_LOSS` | untrusted Eingaben ohne `known_loss` |

### 4.4 Wirkung (6)

| Code | Auslöser |
|---|---|
| `HUMAN_DECISION_WITHOUT_QUESTION` | `required: true` ohne konkrete Frage (Frage muss auf `?` enden) |
| `PROMOTION_WITHOUT_HUMAN_DECISION` | `authority_effect`/`claim_effect` `requested` ohne `human_decision.required: true` |
| `AUTHORITY_EFFECT_UNDERSTATED` | `none` behauptet trotz GOLD-Berührung; oder `none` bei `GOVERNANCE_ADJACENT` **ohne Begründung** (verlangt wird eine Begründung, nicht die Hochstufung auf `requested`) |
| `CLAIM_EFFECT_UNDERSTATED` | `none` behauptet trotz freigegebener Claim-Fläche (`index/`, `policies/`, `spec/`, `seeds/`, `VOIDMAP.*`) |
| `POSSIBLE_PARALLEL_SYSTEM` | `detected_overlaps` nicht leer ohne `mitigation` **oder** `GOVERNANCE_ADJACENT` ohne benannte `systems_checked` (§2.6) |
| `MISSING_KNOWN_LOSS` | `GOVERNANCE_ADJACENT` ohne deklarierten Verlust |

### 4.5 Quellenbindung, Rücknahme (5)

| Code | Auslöser |
|---|---|
| `SOURCE_OF_TRUTH_PATH_MISSING` | genannter Pfad existiert nicht im Repository |
| `SOURCE_OF_TRUTH_PATH_ESCAPES_REPO` | absoluter Pfad oder `..`-Segment |
| `REVERSIBLE_WITHOUT_ROLLBACK` | `REVERSIBLE` ohne konkreten `rollback_path` (§2.3) |
| `IRREVERSIBLE_WITHOUT_ROLLBACK` | `IRREVERSIBLE` ohne konkreten `rollback_path` |
| `IRREVERSIBLE_WITHOUT_HUMAN_DECISION` | `IRREVERSIBLE` ohne konkrete menschliche Frage |

## 5. Ergebnis und Exit-Codes

| Verdikt | Exit | Bedeutung |
|---|---|---|
| `ELIGIBLE_FOR_EXTERNAL_REVIEW` | 0 | keine strukturellen Befunde; das Manifest ist vollständig genug für eine menschliche Prüfung |
| `HOLD` | 1 | mindestens ein Befund, oder selbst deklariertes `HOLD` |
| `HOLD` | 2 | **Eingabefehler**: Datei nicht lesbar oder YAML nicht parsebar |

Exit `2` trennt einen Eingabefehler von einem inhaltlichen Befund. Das Verdikt
bleibt in diesem Fall fail-closed `HOLD` und wird mit dem Befund
`MANIFEST_UNPARSEABLE` ausgegeben — nur der Exit-Code unterscheidet.

Die öffentliche `validate_manifest()`-API kennt keine Exit-Codes; sie liefert
immer ein `ValidationResult`. Die Trennung findet in der CLI statt.

Ein selbst deklariertes `expected_gate_outcome: HOLD` wird respektiert und
**nie** hochgestuft.

`ELIGIBLE_FOR_EXTERNAL_REVIEW` bedeutet ausdrücklich **nicht**: geprüft,
korrekt, sicher, genehmigt oder wahr. Es bedeutet nur, dass das Manifest die
hier beschriebenen Strukturbedingungen erfüllt.

## 6. Determinismus und Grenzen des Validators

- Befunde werden stabil nach `(code, field, detail)` sortiert und dedupliziert;
  identische Eingabe erzeugt identische Ausgabe.
- Keine Zeitstempel, keine Zufallswerte, keine Netzwerkzugriffe, kein
  Prozessstart, keine Schreibzugriffe, keine Ausführung von Manifestinhalten.
- Der einzige Umgebungszugriff ist ein optionaler **Existenz-Check** der
  `existing_sources_of_truth` gegen die Repo-Wurzel (abschaltbar mit
  `--no-path-check`).

**Deklarierte Verluste des Validators selbst:**

- Er prüft **Struktur**, nicht Inhalt. Ein formal vollständiges Manifest kann
  fachlich falsch sein.
- Das Wort `GOLD` wird nicht als Selbstattestierung geprüft, weil es in
  Manifesten legitim als Schichtname vorkommt; GOLD-Wirkung wird ausschließlich
  über Pfadregeln erfasst.
- Ein Manifest, das die Regel „kein endgültiger PASS" wörtlich zitiert, löst
  `FINAL_PASS_NOT_PERMITTED` aus. Der Validator bevorzugt fail-closed einen
  Fehlalarm gegenüber einer stillen Durchlassung.
- Die Pfadklassen sind **Kopien**: GOLD und IMMUTABLE aus
  `.claude/rules/annex.md`, NICHTRAUM aus `CLAUDE.md` (G2 — `annex.md` führt
  diese Schicht nicht). Ein Test belegt die Herkunft jedes Präfixes in seiner
  Quelldatei; Drift wird sichtbar, statt still zu bleiben.
- Der Validator kennt keine VOIDs, keine Receipts, keine Ledger-Events und
  keine Policy-Digests.

**Falsifikatoren dieses Schemas:** Ein Manifest, das eine GOLD-, Claim- oder
Authority-Wirkung erzeugt und dennoch `ELIGIBLE_FOR_EXTERNAL_REVIEW` erhält,
widerlegt das Schema. Ebenso ein Lauf, der bei identischer Eingabe zwei
verschiedene Ergebnisse liefert.

**Rücknahmepfad:** Skill-Verzeichnis nach `NICHTRAUM/archive/` verschieben
(G3: nie löschen). Es besteht keine Kopplung, die dabei bricht — kein Makefile-
Target, kein Workflow und kein Modul importiert den Validator.
