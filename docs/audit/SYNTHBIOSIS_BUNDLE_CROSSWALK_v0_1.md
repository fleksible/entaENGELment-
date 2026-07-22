# SYNTHBIOSIS_BUNDLE_CROSSWALK_v0_1

**Status:** [ANNEX] — `artifact_type: audit/crosswalk` · keine Policy-, Index- oder VOIDMAP-Änderung
**Datum:** 2026-07-21
**Geprüftes Artefakt:** Synthbiosis Systematlas v1.1 (siehe `INBOX/INTAKE-2026-07-21-synthbiosis-system-atlas-v1_1.md`)
**Repo-Referenz der Prüfung:** `main @ 683ea6c079d6099834a5edab44dac1a1ee87cb73`
**Reconciliation-Referenz (append-only):** `main @ d39b9db72dd04d6e1e2cded5a7d08287be76b9b8` (2026-07-22)
**Bundle-Referenz:** `repo_witness.ref = 29390c3d7676a050465568c15dc1caebf62718d8` (historisch)

## 0. Zweck und Grenze

[ANNEX] Dieser Crosswalk ordnet jede Bundle-Datei genau einer Hauptklasse zu
und dokumentiert Repo-Äquivalente, Risiken und kleinste nächste Schritte.
Er verändert keine Authority (Invariante 15), erzeugt keinen dritten
Masterindex (Invariante 16) und promotet nichts.

[FACT] Prüfmethodik: exakte Identität (Name/Hash/Pointer) → umbenannte oder
teilweise Repräsentation (gleiche Funktion/Invarianten) → semantische Nähe
(nur Kandidat, keine Identität) → Authority-/Privacy-Abgleich (ähnlicher
Inhalt ≠ gleiche Rolle). `not found` ≠ `does not exist` (Invariante 10):
Absenzbefunde gelten für den Suchscope `main @ 683ea6c` mit Volltextsuche
über Dateinamen und Kerninhalte.

### Klassifikationsvokabular

`PRESENT_EQUIVALENT` · `PRESENT_PARTIAL` · `MISSING_REPO_SAFE` ·
`PRIVATE_ONLY` · `SUPERSEDED` · `HISTORICAL_WITNESS` · `BROKEN_POINTER` ·
`UNDETERMINED`

### Integritätsbefund (Kurzform)

- [FACT] Alle 10 Manifest-Datei-Hashes verifiziert (2026-07-21), YAML/JSON
  valide, Pfade sicher, keine Duplikate. Der Drive-Container enthält
  12 ZIP-Einträge (1 Verzeichniseintrag, 11 Datei-Einträge); das Manifest
  hasht 10 Dateien und nimmt sich selbst nicht auf
  (`manifest_self_hashed: false`).
- [FACT] Es existieren **zwei verschieden verpackte Container desselben
  Inhalts**: die vom Projektinitiator bereitgestellte Original-Variante
  (`9de320ff…`, 26 043 Bytes, 11 Datei-Einträge, 0 Verzeichniseinträge)
  und die geprüfte Drive-Variante (`3dd76c1f…`, 27 209 Bytes,
  11 Datei-Einträge, 1 Verzeichniseintrag). Verglichen wurden die elf
  normalisierten Dateinamen, die zehn Manifest-Hashes und separat der
  SHA-256 des Receipts selbst (`156e146d…`, beidseitig identisch).
  Disposition: **SAME_INNER_PAYLOAD_DIFFERENT_CONTAINER** (Details:
  Intake, `container_comparison`). Bundle-Integrität bleibt dennoch keine
  semantische Wahrheit (Invariante 1).

### ERK-Referenz dieser Prüfung

```yaml
erk_reference:
  pull_request: 314
  state: open_draft
  reviewed_head: ef3393e9b40e6cc2a777c5b464909e5a42b5e7c6
  moving_target: true
  authority_effect: none
```

[ANNEX] PR #314 ist **kein stabiler Repo-Kanon**. Alle ERK-Bezüge in diesem
Crosswalk gelten für den genannten Head; Änderungen nach diesem Head
benötigen einen neuen Drift-Check.

### Reconciliation-Delta 2026-07-22 (append-only)

[REPO-FACT] Die vorstehenden Aussagen bleiben als historischer Prüf-Witness
unverändert. Für den aktuellen Reentry gilt zusätzlich:

```yaml
reconciliation_delta:
  observed_main: d39b9db72dd04d6e1e2cded5a7d08287be76b9b8
  authority_effect: none
  merged_witnesses:
    research_validation_gate: {pull_request: 316, commit: 51950ae53a5ae5d116129fbd7eb6049ec0077808}
    tesser_tick_frame: {pull_request: 312, commit: a2b5ddf6c20ba268f68daf65472d62cbaf16d6a1}
    evidence_routing_kernel: {pull_request: 314, commit: c81bb202e3b069672b284569523d9c114ba2a2f1}
    tesser_hud: {pull_request: 304, commit: 5cd423f0c40f64e50811ee9392601fb4f99fe48c}
    boundary_array_hardening: {pull_request: 318, commit: d39b9db72dd04d6e1e2cded5a7d08287be76b9b8}
  parallel_open_work:
    pull_request: 319
    state: draft
    relation: outside_reconciliation_scope
    authority_effect: none
```

| Bundle-Datei | Historische Einstufung | Aktueller Overlay-Status |
|---|---|---|
| 01 Dual-Format Claim Bridge | `MISSING_REPO_SAFE` | weiterhin fehlender separater Adapter; nach Merge #314 jetzt `ELIGIBLE_FOR_SPEC` |
| 02 tesser3TAKT Transition Engine | `PRESENT_PARTIAL` | Frame/HUD-Witnesses #312/#304 gemergt; #318 härtet den Runtime-Rand; keine vollständige Engine-Closure |
| 05 Research Validation Gate | `MISSING_REPO_SAFE` | jetzt `PRESENT_PARTIAL` als ANNEX aus #316; Runtime-Enforcement none, Humanforschung HOLD |
| 07 Module Contracts | `MISSING_REPO_SAFE` | weiterhin kein maschinenlesbarer Gesamtvertrag; kein stiller Import |

[GUARD] Dieses Delta überschreibt weder den historischen Suchscope noch die
ursprüngliche Klassifikation. Merge-Status ist kein Authority-Upgrade.
Draft-PR #319 verändert keine der drei Reconciliation-Zieldateien und ist
kein Beleg für VOID-Closure.

---

## 1. Datei-Crosswalk

### 00_SYSTEM_ATLAS.md

```yaml
bundle_file: 00_SYSTEM_ATLAS.md
classification: HISTORICAL_WITNESS   # mit PRESENT_PARTIAL-Anteilen
repo_equivalent:
  - docs/PROJECT_CONSTELLATION_MAP_v0_1.md   # Navigationskarte, Statusvokabular
  - docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md  # Schichten-/Rollenmodell
  - docs/masterindex.md                      # bestehender Navigator
open_pr_overlap: none
preserved_value: >
  Sechs-Körper-Gliederung (M1-M6), Statusleiter E0-E4, Rücktaggung der
  Januar-Aussagen, mereotopologische Schnittstellenordnung, priorisierte
  Umsetzungsliste.
outdated_assumption: >
  Repo-Witness zeigt auf 29390c3d (2026-07-16); seither sind u.a. der
  Evidence Routing Kernel (PR #314, offen) und Dependency-Merges auf main
  hinzugekommen. Der Atlas kennt den ERK nicht.
privacy_risk: >
  Gering im Text selbst; referenziert aber private Save States und
  Drive-Material namentlich. Nicht wörtlich importieren.
authority_risk: >
  Hoch bei Import: Ein "Systematlas" neben Constellation Map und masterindex
  wäre ein dritter Masterindex (verboten, Invariante 16).
recommended_action: nicht importieren; als historische Integrationssicht referenzieren
smallest_next_step: Referenz aus diesem Crosswalk genügt; keine Datei-Übernahme
human_decision: ob einzelne Atlas-Abschnitte je einzeln als ANNEX-Kandidaten intaken werden
```

### 01_DUAL_FORMAT_CLAIM_BRIDGE.md

```yaml
bundle_file: 01_DUAL_FORMAT_CLAIM_BRIDGE.md
classification: MISSING_REPO_SAFE
repo_equivalent: >
  Kein eigenständiges Bridge-Modul auf main. Teilabdeckung durch PR #314
  (offen, nicht main): source_pointer -> MaterialRef; claim/status ->
  ClaimCandidate; preserved_relation -> EvidenceRelation; rollback ->
  HumanDecision(WITHDRAW)/Retraction; Reason-Codes als kontrolliertes
  Vokabular. docs/tesser3takt/SOURCE_DECORATION_MAP_v0_1.md deckt die
  Guard-Seite (kein Identitätskurzschluss) dokumentarisch ab.
open_pr_overlap: "PR #314 (konzeptionell, keine Dateiüberschneidung)"
preserved_value: >
  Echt neue Bridge-Felder: source_register, transferred_property,
  known_loss, falsifier, intended_use; die sechs Brückenfragen; Guards
  no_identity_shortcut, no_score_authority; die vier Minimaltests
  (Josephson-Jesus, 7x9-Yggdrasil, RCC-8-Photonik, Liebe-HRV als
  Pflicht-Negativfall).
outdated_assumption: >
  "rollback: string" ist im ERK inzwischen als append-only
  Withdrawal/Retraction präziser modelliert; ein Bridge-Adapter sollte
  darauf zeigen statt ein eigenes Rollback-Feld zu erfinden.
privacy_risk: gering (Schema-Ebene); protected_origin-Flag ist bereits vorgesehen
authority_risk: >
  Mittel: MOTIVATES/CONTEXTUALIZES dürfen keine Promotionsbeweise werden;
  Bridge-Records dürfen keine Registeridentität behaupten.
recommended_action: >
  Adapterlogik (Bridge-Record -> MaterialRef + EvidenceRelation) gehört in
  einen separaten Adapter, nicht in den ERK-Core. Kandidat für Phase 2A
  nach Merge/Stabilisierung von PR #314.
smallest_next_step: Feld-Mapping-Tabelle in der Adapter-Map (erledigt, siehe dort)
human_decision: Freigabe von Phase 2A und des Adapterziels
```

### 02_TESSER3TAKT_TRANSITION_ENGINE.md

```yaml
bundle_file: 02_TESSER3TAKT_TRANSITION_ENGINE.md
classification: PRESENT_PARTIAL
repo_equivalent:
  - docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md  # Zustands-/Projektionsgrammatik
  - docs/tesser3takt/SOURCE_DECORATION_MAP_v0_1.md      # Motiv-Guards
  - docs/tesser3takt/SANCHO_GUARD_v0_1.md               # Erdungs-Guard
  - docs/qm/F7_FALSE_OK_METHODSHEET_v1.0.md             # FALSE_OK-Anschluss
open_pr_overlap: "PR #304 (HUD/UI), PR #312 (Frame Contract) — beide UI-lokal, offen"
preserved_value: >
  Kompaktes tesser_input/tesser_output-Schema; explizite FALSE_OK-Kriterien
  als Brücke zwischen F7 und PASS/HOLD/LOOP/STOP; die fünf Negativtests
  (PASS ohne Rücknahmepointer usw.).
outdated_assumption: >
  "ausführbare Engine nur [SPEC-WIP]" ist weiter korrekt; die UI-Seite ist
  seit PR #304/#312 konkreter als im Bundle beschrieben.
privacy_risk: gering; verweist auf Regiebuch (privat), erzählt es aber nicht
authority_risk: >
  Hoch bei Doppelbau: Ein zweites PASS/HOLD/LOOP/STOP-System neben der
  Repo-Grammatik und der ERK-Kette PROPOSE/HOLD/STOP ist verboten
  (Invariante 11; Adapter-Map §M2).
recommended_action: >
  Kein Import. Die FALSE_OK-Liste als späteren Prüfanschluss zwischen
  F7-Methodsheet und Guard-Vokabular vormerken (dokumentarisch).
smallest_next_step: keiner in dieser Phase; Abgrenzung in Adapter-Map dokumentiert
human_decision: ob die fünf Negativtests später als Drill-Fälle übernommen werden
```

### 03_GRIMM_NEKTAR_UI_LAB.md

```yaml
bundle_file: 03_GRIMM_NEKTAR_UI_LAB.md
classification: PRIVATE_ONLY
repo_equivalent: >
  Prinzipien teilweise öffentlich vertreten: PRIVACY_BOUNDARY.md
  (private-by-default Datenklassen), ANTI_CAPTURE_POLICY.md (keine
  Fremddeutung/Profiling), Constellation-Map-Privacy-Reduktionsregel.
  Der P7-Quellkörper selbst ist nicht im Repo (korrekt).
open_pr_overlap: none
preserved_value: >
  External Failure Rule; Nicht-Resonanz als gültige, terminale Rückmeldung;
  Szenenvertrag mit consent_state und reversibility; Engineering-Gates-
  Tabelle (Source Freeze, E2E, AuthN/AuthZ, Firebase, Privacy, A11y).
outdated_assumption: >
  Bundle-Stand der P7-Gates (2026-07-16) kann vom heutigen privaten Stand
  abweichen; hier nicht prüfbar (privater Korpus liegt nicht vor) -> insoweit
  UNDETERMINED.
privacy_risk: >
  Hoch bei Import: Providerkonfiguration, UI-Seeds, Firebase-Zweck und
  Datenflüsse sind ungeklärt; private Herkunft ist Konstruktionsmerkmal.
authority_risk: >
  Hoch: Ein privates UI-LAB darf nicht als öffentlicher Frameworkbeweis
  importiert werden (Invariante 4).
recommended_action: >
  Nicht übernehmen. Später genügt ein Source-Freeze-Manifest (Phase 2D):
  Hash, Intended Purpose, Inventar, Datenfluss, Providergrenzen, Known
  Limits, Lizenzstatus, Public-Allowlist, private Ausschlüsse.
smallest_next_step: keiner in dieser Phase
human_decision: Freigabe und Zuschnitt eines Source-Freeze-Manifests (Phase 2D)
```

### 04_GOVERNANCE_RECEIPTS_FALSE_SAFETY.md

```yaml
bundle_file: 04_GOVERNANCE_RECEIPTS_FALSE_SAFETY.md
classification: PRESENT_PARTIAL
repo_equivalent:
  - docs/qm/F7_FALSE_OK_METHODSHEET_v1.0.md            # F7 formal definiert
  - docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md       # Claim-Dialekt-Trennung
  - docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md    # Receipt != Wahrheit
  - src/core/ledger.py + tools/receipt_lint.py         # Receipt-Mechanik (scoped)
open_pr_overlap: "PR #314 (Reason-Codes, PROVENANCE_ONLY-Semantik; keine Dateiüberschneidung)"
preserved_value: >
  Die Receipt-Typen-Tabelle mit expliziten "belegt / belegt nicht"-Spalten
  (repo_hmac, p7_sha_chain, review_relay, status_receipt, empirical_bundle);
  das false_safety_check-Codebook; der Vorschlag einer maschinenlesbaren
  evidence_semantics-Struktur (receipt_type, proves, does_not_prove, scope,
  authority_effect).
outdated_assumption: >
  "Kein neuer universeller Guard" bleibt gültig; die vorgeschlagene
  evidence_semantics-Erweiterung ist durch die ERK-Reason-Codes teilweise,
  aber nicht vollständig abgedeckt (proves/does_not_prove fehlt dort bewusst).
privacy_risk: gering
authority_risk: >
  Mittel: Receipt-Typen dürfen nach Belegfunktion, nicht nach vermeintlicher
  Wahrheitsstärke geordnet werden (Invariante 6: Receipt ist kein
  Evidence- oder Truth-Automat).
recommended_action: >
  Kein Import als Ganzes. Die proves/does_not_prove-Struktur als
  Adapter-Kandidat M4->ERK dokumentieren (erledigt, Adapter-Map §M4).
smallest_next_step: keiner über die Adapter-Map hinaus
human_decision: ob evidence_semantics später ein eigenes Schema-Delta wird
```

### 05_RESEARCH_VALIDATION_GATE.md

```yaml
bundle_file: 05_RESEARCH_VALIDATION_GATE.md
classification: MISSING_REPO_SAFE
repo_equivalent: >
  Kein gleichwertiger Repo-Vertrag gefunden (Suchscope: docs/, spec/,
  policies/ auf main @ 683ea6c; Begriffe: research gate, validation gate,
  HRV, airlock, preregistration). not found != does not exist.
open_pr_overlap: none
preserved_value: >
  Vollständig zu erhalten: Trennung normativer Wert / Modellkandidat /
  Simulation / Komponentenclaim / Humanclaim; Human-Research Airlock
  (9 Voraussetzungen vor jedem Kontakt); "HRV ist kein Liebes- oder
  Resonanzmeter"; harte Risiken sind Constraints, keine verrechenbaren
  Mali; Falsifikations- und Nullresultate werden vor dem Test benannt;
  Evidenzleiter ROHSEDIMENT -> ... -> REPLICATED_EVIDENCE.
outdated_assumption: keine erkannt; der Inhalt ist zeitlos formuliert
privacy_risk: gering (keine personenbezogenen Inhalte)
authority_risk: >
  Gering bei ANNEX-Übernahme; hoch nur, wenn das Gate als bereits
  enforced ausgegeben würde (es ist [SPEC-WIP], Humanforschung HOLD).
recommended_action: >
  Bester Kandidat für eine reduzierte ANNEX-Übernahme in einer eigenen
  Folgephase (Phase 2B: docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md).
smallest_next_step: Phase-2B-Vorschlag im PR (keine Datei in diesem Pass)
human_decision: Freigabe Phase 2B
```

### 06_PHOTONIC_THERMAL_ROSETTA.md

```yaml
bundle_file: 06_PHOTONIC_THERMAL_ROSETTA.md
classification: MISSING_REPO_SAFE   # abhängig von M5 (Research Gate zuerst)
repo_equivalent: >
  Kein Repo-Äquivalent für den Airlock gefunden. Historische
  "materialisierte Ethik"-Sprache existiert in Drive-Material, nicht als
  Repo-Claim (korrekt).
open_pr_overlap: none
preserved_value: >
  Komponentenrealität-vs-Projektzuordnung-Tabelle; die Liste verbotener
  Schlussfolgerungen ("physikbasiert" != "unumgehbar"; Absorber kennt
  keine Zustimmung; Dissipation ist kein moralisches Veto); das atomare
  component_claim-Schema; der empfohlene erste Bench-Claim (Transmission
  T(I) mit Unsicherheit statt "materialisierte Ethik").
outdated_assumption: >
  Historische Gesamtclaims ("materialisierte Ethik", Hardware als
  Sicherheitsbeweis) sind im Bundle selbst bereits zurückgenommen; diese
  Rücknahme ist zu erhalten, nicht rückgängig zu machen.
privacy_risk: gering
authority_risk: >
  Hoch bei falscher Reihenfolge: Kein Pfad Hardware -> Authority,
  Hardware -> Ethics PASS, Simulation -> Public Fact (Invarianten 7/8).
  Zulässig nur M6 -> M5 -> M1 -> M4.
recommended_action: >
  Nicht vor Phase 2B/2C anfassen. Semantische Mappings bleiben strikt
  getrennte Bridge-Records (separate_bridge_record im Schema).
smallest_next_step: keiner in dieser Phase
human_decision: Freigabe Phase 2C erst nach existierendem M5
```

### 07_MODULE_CONTRACTS.yaml

```yaml
bundle_file: 07_MODULE_CONTRACTS.yaml
classification: MISSING_REPO_SAFE   # zugleich HISTORICAL_WITNESS des Bundles
repo_equivalent: >
  Kein maschinenlesbarer Modulvertrag M1-M6 auf main. Teilfunktionen
  existieren verstreut (tesser3takt-Doku für M2, ERK in PR #314 für
  Transition-Proposals, F7 für M4-Prüflogik).
open_pr_overlap: "PR #314 (konzeptionell); keine Dateiüberschneidung"
preserved_value: >
  Weiterhin gültige Flussordnung: narrative_offer M1->M2->M3->M4;
  empirical_claim M1->M5->M4; physical_component M6->M5->M1->M4.
  Die global_invariants decken sich mit heutigen Repo-Prinzipien
  (receipt_is_not_truth, reentry_is_not_identity, human_authority_...).
outdated_assumption: >
  Phantomknoten "M4_authority" in M6.may_not_connect_directly_to: Es gibt
  kein Modul dieses Namens; gemeint ist die Authority-Wirkung von M4.
  Zudem mischt "stops" drei Sorten: Prinzipien (receipt_equals_truth),
  Interpretationsverbote (non_resonance_reinterpretation) und technisch
  beobachtbare Fehler (pass_without_rollback) — für ein validierbares
  Schema müssten diese getrennt typisiert werden.
privacy_risk: gering
authority_risk: >
  Mittel: Die Datei ist Architekturmanifest, kein validierbares
  Runtime-Schema. Keine Runtime-Schema-Implementierung in diesem Pass.
recommended_action: >
  Als historischen Vertragstext bezeugen; Felder, die später in ein
  validierbares Schema überführt werden könnten: modules[].accepts/emits,
  flows[].path/end_condition, getrennt typisierte stops.
smallest_next_step: Contract-Gap-Tabelle in der Adapter-Map (erledigt)
human_decision: ob und wann ein validierbares Schema-Delta beauftragt wird
```

### 08_HISTORICAL_STATUS_CROSSWALK.md

```yaml
bundle_file: 08_HISTORICAL_STATUS_CROSSWALK.md
classification: HISTORICAL_WITNESS
repo_equivalent: >
  Kein Repo-Äquivalent; VOIDMAP.yml ist das einzige kanonische
  VOID-Register (Legacy V-008..V-015 sind dort bewusst NICHT enthalten;
  die VOIDMAP-Reconciliation-Notes dokumentieren bereits frühere
  Legacy-ID-Kollisionen und Remappings).
open_pr_overlap: none
preserved_value: >
  Die Rücktaggungs-Tabelle begrenzt alte starke Aussagen (Isomorphie ->
  Mapping-Kandidat; Resonanzzahlen -> Heuristik; "Liebe -> HRV" ->
  unzulässige Verkürzung). Die Konflikt-Tabelle §5 (PASS/Pi, Resonanz,
  Receipt als Namespace-Konflikte, kein stiller Merge) bleibt wertvoll.
outdated_assumption: >
  V-014 ("Nektar-UI fehlt") ist im Bundle selbst schon als überholt
  markiert; keine weitere Korrektur nötig.
privacy_risk: gering
authority_risk: >
  Hoch bei Import der Legacy-IDs: Gefahr eines zweiten historischen
  VOID-Registers neben VOIDMAP.yml (Invariante 3: historische Herkunft
  nicht durch neue Terminologie überschreiben; Invariante 11).
recommended_action: >
  Nicht importieren. Der Crosswalk soll alte starke Aussagen begrenzen,
  nicht sie erneut verbreiten — genau dafür genügt die Referenz hier.
smallest_next_step: keiner
human_decision: keine erforderlich, solange kein Import erfolgt
```

### 09_SYNTHESIS_RECEIPT.json

```yaml
bundle_file: 09_SYNTHESIS_RECEIPT.json
classification: HISTORICAL_WITNESS
repo_equivalent: >
  Kein direktes Äquivalent; funktional entspricht es im heutigen
  ERK-Vokabular (PR #314) einem Material mit Relation PROVENANCE_ONLY:
  Es belegt Herkunft und Zusammenstellung, niemals Claim-Wahrheit.
open_pr_overlap: none
preserved_value: >
  Datei-Hash-Manifest (10/10 verifiziert), Methoden-Scope-Liste,
  ehrliche limits-Liste, repo_witness mit Ref, authority_effect: none.
outdated_assumption: >
  Scope-Grenzen: Das Receipt hasht sich selbst nicht (korrekt) und deckt
  den äußeren Container nicht ab. Die Container-Frage wurde daher separat
  über den Receipt-Selbsthash (156e146d..., beidseitig identisch) und die
  zehn Manifest-Hashes geklärt: SAME_INNER_PAYLOAD_DIFFERENT_CONTAINER.
privacy_risk: >
  Gering; method_scope nennt private Quellklassen (save states, P7) nur
  als Kategorien, ohne Inhalte.
authority_risk: >
  Gering, solange gilt: Receipt vorhanden != Authority (Invariante 6).
recommended_action: als Bundle-Witness referenzieren; nicht ins Repo kopieren
smallest_next_step: keiner
human_decision: keine erforderlich
```

### README.md

```yaml
bundle_file: README.md
classification: HISTORICAL_WITNESS
repo_equivalent: >
  Kein Bedarf: docs/masterindex.md und PROJECT_CONSTELLATION_MAP sind die
  gegenwärtigen Navigatoren.
open_pr_overlap: none
preserved_value: >
  Belegt die beabsichtigte Paketordnung (Lesereihenfolge 00-08) und die
  "Harten Grenzen" des Bundles; die Ein-Satz-Architektur ist eine gute
  Kurzzusammenfassung der Rollenverteilung.
outdated_assumption: Repo-Witness 29390c3 ist nicht mehr aktueller main
privacy_risk: gering
authority_risk: gering (kein gegenwärtiger Repo-Navigator)
recommended_action: als historische Paketbeschreibung belassen
smallest_next_step: keiner
human_decision: keine erforderlich
```

---

## 2. Zusammenfassung nach Klassen

| Klasse | Bundle-Dateien |
|---|---|
| PRESENT_PARTIAL | 02, 04 |
| MISSING_REPO_SAFE | 01, 05, 06, 07 |
| PRIVATE_ONLY | 03 |
| HISTORICAL_WITNESS | 00, 08, 09, README |
| UNDETERMINED (Teilaspekte) | heutiger P7-Stand (privater Korpus liegt der Prüfung nicht vor) |

[FACT] Die zunächst offene Container-Identität des früheren Digests ist
aufgelöst: `9de320ff…` gehört zur Original-ZIP-Variante des
Projektinitiators; beide Container tragen denselben inneren Inhalt
(`SAME_INNER_PAYLOAD_DIFFERENT_CONTAINER`, siehe Integritätsbefund).

[INFERENZ] Kein Bundle-Modul ist SUPERSEDED im strengen Sinn: Auch die
teilweise repräsentierten Module (02, 04) enthalten Prüfmaterial (Negativtests,
proves/does_not_prove), das im Repo noch fehlt. Kein BROKEN_POINTER: Alle
Bundle-internen Referenzen lösten auf.

## 3. Reentry

**PASS-Kandidat:** Bundle-Witness + Crosswalk als ANNEX-Audit.
**HOLD:** jeder Modul-Import, Legacy-VOID-IDs, P7-Material, Runtime-Schemata.
**LOOP:** Phase 2A/2B als kleinste sinnvolle Folgearbeiten (siehe Adapter-Map §5).
**STOP:** dritter Masterindex, paralleles PASS/HOLD/LOOP/STOP-System,
Receipt-als-Wahrheit-Lesart, Import privater Quellkörper.
