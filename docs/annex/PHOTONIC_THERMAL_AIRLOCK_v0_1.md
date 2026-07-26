# PHOTONIC_THERMAL_AIRLOCK_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** none
**Bench-Measurement-Status:** HOLD
**Promotion-Effect:** none
**Human-Decision-Boundary:** required
**Source:** Synthbiosis Systematlas v1.1 / `06_PHOTONIC_THERMAL_ROSETTA.md`
(Bundle-Witness: `INBOX/INTAKE-2026-07-21-synthbiosis-system-atlas-v1_1.md`;
Crosswalk-Einstufung MISSING_REPO_SAFE, abhängig von M5:
`docs/audit/SYNTHBIOSIS_BUNDLE_CROSSWALK_v0_1.md`)

```yaml
source_relation:
  relation: reduced_public_annex
  source_identity: not_claimed
  semantic_equivalence: not_claimed
  known_loss_required: true

gate_dependency:
  requires: docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md
  relation: M6_enters_only_through_M5
  status_without_M5: HOLD
```

Dieses Dokument beschreibt eine **Reihenfolge und ein Dokumentationsschema**.
Es enthält keinen Messaufbau, keine Stückliste, keinen Schaltplan, keine
Messdaten und keine Hardwarefreigabe. Es macht kein Bauteil zu einer Ethik-
oder Governanceaussage.

---

## 1. Zweck und Nicht-Ziel

[ANNEX] M6 ist die Schleuse, durch die physische Befunde in das Projekt
eintreten können — einzeln, gemessen, mit Unsicherheit, und **ohne
Bedeutungsaufladung**.

M6 ist ausdrücklich **nicht**:

- ein Nachweis, dass ein Gesamtsystem existiert oder funktioniert,
- eine Begründung für „materialisierte Ethik",
- ein Sicherheitsversprechen („physikbasiert" heißt nicht „unumgehbar"),
- ein Weg, Governance an Hardware zu delegieren,
- ein Ersatz für M5 (methodische Prüfung) oder M1 (semantische Brücke).

[CONTEXT] Der Quellkorpus hat die historischen Gesamtclaims bereits selbst
zurückgenommen. Diese Rücknahme wird hier bewahrt, nicht rückgängig gemacht.

## 2. Architekturidee (als Forschungsarchitektur, nicht als Schaltplan)

[MODEL] Der Quellkorpus trennt vier Schichten sinnvoll voneinander:

1. photonische Kern-/Rechenschicht,
2. analoge Überwachung und Sonifikation,
3. digitale Governance/Audit,
4. thermische Metamaterialien und Transportmodelle.

[FACT] Diese Trennung stammt aus einem Navigationsartefakt (Mindmap). Ein
Navigationsartefakt ist kein Schaltplan, keine Stückliste, kein Tape-out und
kein Bench-Receipt.

## 3. Komponentenrealität vs. Projektzuordnung

[ROSETTA] Die folgende Tabelle hält zwei Spalten getrennt, die im historischen
Material oft in einem Satz standen: was ein Bauteil **ist** und welche Rolle
das Projekt ihm **zuschreibt**. Die Liste ist beispielhaft, nicht vollständig.

| Objekt | reale Fachklasse | Projektzuordnung (nur Zuschreibung) | heutiger Status |
|---|---|---|---|
| MZI-Mesh, Wellenleiter, photonische Kristalle | integrierte Photonik | Funktoren / VMM / Pattern Engine | Komponente real; Systemmapping [HYPOTHESE] |
| Sättigungsabsorber | nichtlineare Optik | „Confidence-Guard" | Übertragungsfunktion prüfbar; Confidence-Semantik unkalibriert |
| Ring-/Sektordetektoren | Photodetektion | Monitoring / Sonifikation | plausibler Komponentenpfad; End-to-End offen |
| FPGA / Controller | digitale Steuerung | Consent, Audit, Kill-Switch | digitale Governance möglich; **nicht** durch Photonik legitimiert |
| PCM / Memristor / Delay Line | Speicher- und Dynamikbauteile | Zustands-/Gewichtsspeicher | Forschungsoption, keine integrierte Spec |
| thermo-optischer Resonator | zeitabhängiger optischer Schalter | „Refraktärzeit" | Zeitkonstante messbar; psychologische Lesart bleibt [METAPHER] |
| topologischer Isolator | topologische Photonik | Kohärenzprüfung | Projektmapping spekulativ; kein Modulnachweis |
| Piezo / PDLC | Transduktion, Sichtbarkeit | Interface-Brücke | Komponenten real; Ethik-/Resonanzsemantik offen |

[INFERENZ] Die rechte Spalte ist in keinem Fall durch die linke belegt. Eine
Zuschreibung wird erst dann prüfbar, wenn sie als atomarer Komponentenclaim
(§5) formuliert und über M5 geführt wird.

## 4. Befund zur historischen Hardware-Tabelle

[FACT] Die Hardware-Tabelle des Quellkorpus enthält rund zehn Architekturzeilen
und etwa 59 Quellenverweise. Drei Eigenschaften verhindern eine
Validierungsfunktion:

1. Die Quellen sind heterogen: Fachpaper, Reviews, Aggregatoren, interne
   Dokumente, eigene Specs und Präsentationen stehen nebeneinander.
2. Einzelne Zeilen referenzieren sehr viele Quellen, ohne zu zeigen, welche
   Quelle welchen Parameter trägt.
3. Bauteileigenschaft und Governancebedeutung werden im selben Satz gekoppelt.

[INFERENZ] Folge: Die Tabelle bleibt ein `component_and_claim_inventory` —
eine Literatur- und Komponentenlandkarte. Für eine Prüfung muss sie in atomare
Claims zerlegt werden. Viele Quellen in einer Zelle ersetzen keine Kalibrierung
und keine unabhängige Replikation.

## 5. Atomarer Komponentenclaim (Dokumentationsschema)

Ein Teilclaim ist erst dann prüfbar, wenn dieses Dossier vollständig ist. Das
Schema wird **nicht ausgeführt**, erzeugt keine Events und ist kein
Policy-Schema.

```yaml
component_claim:
  claim_id: local_annex_identifier
  physical_component:
  measurable_quantity:
  units:
  operating_conditions:
  calibration_curve:
  uncertainty:
  repetitions:
  failure_modes: []
  degradation_and_drift:
  threat_model:
  negative_path:
  raw_data_pointer:
  analysis_code_pointer:
  evidence_modality: bench | simulation # kein Receipt-Typ; Einordnung siehe §7
  receipt_type: repo_hmac | p7_sha_chain | review_relay | status_receipt | empirical_bundle | null
  # empirical_bundle nur für bench nach M5; andere M4-Typen belegen
  # ausschließlich ihre Provenienz-/Kontextfunktion
  semantic_mapping: separate_bridge_record
  known_loss: []
  status: HOLD
```

[ANNEX] `semantic_mapping` bleibt bewusst leer und verweist auf ein
**separates** M1-Bridge-Record. Erst nach dem Komponentenclaim darf gefragt
werden, ob und wie eine Messgröße eine Governancefunktion repräsentiert — und
diese Frage wird an anderer Stelle beantwortet, nicht hier.

## 6. Empfohlener erster Bench-Claim

[HYPOTHESE] Nicht „materialisierte Ethik", sondern der engste zulässige
Anspruch:

> Unter definierten Wellenlängen-, Leistungs-, Temperatur- und
> Kopplungsbedingungen zeigt Komponente X eine reproduzierbare Transmission
> `T(I)` mit angegebener Unsicherheit und Erholungszeit.

Benötigt werden: Datenblatt oder Herstellungsweg, optischer Aufbau, Rohdaten,
Kalibrierung, Wiederholungen, Temperaturabhängigkeit, Degradation, Drift und
ein Negativpfad. Erst danach darf der Befund in M5 eingereicht und — nur bei
dort festgestellter methodischer Eignung — über eine getrennte M1-Brücke einem
M4-Governance-Review vorgelegt werden. Sobald daraus Claim-Status oder
Authority folgen sollen, ist eine ausdrücklich **menschliche** Entscheidung
Pflicht. Policy darf syntaktische Übergänge und nicht-authority-verändernde
Verarbeitung wie Analyse oder Visualisierung steuern; sie entscheidet weder
Bedeutung noch Claim-Wahrheit.

[CONTEXT] Dieser Satz ist ein Formulierungsbeispiel für den engsten Anspruch.
Er ist keine Messankündigung, keine Beschaffungsempfehlung und keine
Terminzusage.

## 7. Verhältnis zu den anderen Modulen

**Einziger zulässiger Hauptpfad für Claim-/Authority-Wirkung:**

```
physischer Komponentenbefund
    → M5 methodische Prüfung
    → M1 getrennte semantische Brücke
    → M4 Governance-Review
```

**Nicht zulässig:** `M6 → Authority`, `M6 → menschlicher Consent`,
`M6 → moralische Wahrheit`, `M6 → M4` direkt mit Claim-/Authority-Wirkung.
Analyse, Visualisierung und andere Verarbeitung ohne Authority-Änderung dürfen
innerhalb ihres dokumentierten Scopes policy-gesteuert bleiben.

**M6 ↔ M5:** M6 liefert Komponentenbefunde; M5 prüft methodische Prüfbarkeit,
Voraussetzungen und externe Review-Reife
(`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`). Ein Komponentenclaim ist in
der M5-Evidenzleiter höchstens `BENCH_OR_FEASIBILITY` — niemals
`REPLICATED_EVIDENCE` allein durch Wiederholung im selben Aufbau.

**M6 ↔ M4 (Receipt-Einordnung):** Dieser ANNEX führt **kein eigenes
Receipt-Vokabular** ein. `bench | simulation` ist ausschließlich die
`evidence_modality`. `receipt_type` verwendet die bestehende M4-Typologie
(`docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md` §2.4): Ein
Bench-Ergebnis kann dort höchstens **nach** M5-Prüfung als
`empirical_bundle` mit Relation `SUPPORTS` oder `CONTRADICTS` erscheinen.
Vor M5 und für Simulationen bleiben `repo_hmac`, `p7_sha_chain`,
`review_relay` und `status_receipt` für genau ihre dort definierte
Provenienz-/Kontextfunktion zulässig; `null` bedeutet, dass keine solche
Receipt-Funktion vorliegt. Eine Simulation darf niemals `empirical_bundle`
tragen und wird nicht durch Signatur, Status oder Review zu Empirie.

**M6 ↔ ERK:** Ein Komponentenbefund kann später als `MaterialRef` mit einer
`EvidenceRelation` in einen ERK-Flow eingehen
(`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`). Er kann niemals eine
`HumanDecision` synthetisieren, selbstständig retaggen oder Claim-Wahrheit
feststellen. Ein Bauteil hat keine Zustimmung zu geben.

**Zwei Airlocks, nicht einer:** Der M6-Airlock betrifft **Bauteile**; der
Human-Research Airlock in M5 §4 betrifft **Menschen**. Sie haben getrennte
Voraussetzungen und werden nicht zusammengezogen. Ein erfüllter M6-Pfad sagt
nichts über Humanforschung aus.

## 8. Verbotene Schlussfolgerungen

- „Physikbasiert" bedeutet nicht automatisch „unumgehbar".
- Ein Absorber kennt keine Zustimmung und keine Ethik; er realisiert eine
  Transferfunktion.
- Thermodynamische Dissipation ist kein moralisches Veto.
- Ein optischer Korrelator beweist weder Plagiat noch wechselseitige
  Information ohne definiertes Daten- und Kodierungsmodell.
- Spinor- oder Topologiesprache beweist keine Systemkohärenz.
- Ein Receipt mit synthetischen Zielwerten ist kein Hardware-Messreceipt.
- Simulation ist keine Empirie; Bench-Evidenz ist keine Humanevidenz.
- Viele Quellen in einer Zelle ersetzen keine Kalibrierung.

## 9. Externe Forschungsanschlüsse (`methodological_neighbors`)

[CONTEXT] Interpretable inverse design und generative Materialmodelle können
spätere Material- oder Strukturvariation unterstützen. Sie validieren **kein**
gebautes System und belegen keine Governanceeigenschaft. Der historische
Pointer aus dem Quellkorpus (Stand 2026-07-16) lautet
`hf.co/papers/2401.00003`; er wurde hier nicht erneut aufgelöst und gilt als
historischer Verweis, nicht als Bestätigung.

## 10. Known Loss gegenüber dem Quellmodul

Sichtbare Verluste dieser reduzierten Fassung (`known_loss_required: true`):

- Die Komponententabelle ist gekürzt; einzelne Formulierungen sind nicht
  wortidentisch (`source_identity: not_claimed`).
- Die Bauteilliste ist beispielhaft, nicht vollständig.
- Der externe Forschungspointer wurde nicht erneut aufgelöst.
- Das `component_claim`-Schema wurde gegenüber der Quelle um
  `repetitions`, `degradation_and_drift`, `negative_path`, `known_loss` und
  `status` ergänzt sowie um `evidence_modality` von der bestehenden
  M4-`receipt_type`-Typologie getrennt — als Strukturschärfung, nicht als neue
  inhaltliche Anforderung; die Quelle nennt diese Punkte im Fließtext.
- Kein Messaufbau, keine Stückliste, kein Schaltplan, keine Rohdaten.

## 11. Exit-Semantik

M6 besitzt in v0.1 **keinen Runtime-Zustandsautomaten** und keinen Check in
`make verify`. Solange kein vollständiges Komponentendossier (§5) und keine
M5-Prüfung vorliegen, gilt: **HOLD**.

Der bestmögliche Zustand dieses ANNEX ist eine beschreibende Feststellung —
„Die Voraussetzungen sind vollständig genug für eine menschliche und fachlich
zuständige Prüfung" (`ELIGIBLE_FOR_EXTERNAL_REVIEW` im Sinne von
`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §11). Nicht erlaubt ohne externe,
zuständige und dokumentierte Entscheidung: `VALIDATED`, `PROVEN`, `SAFE`,
`ETHICALLY_APPROVED` oder ein endgültiges Durchlassurteil.

## 12. Grenzen und Rücknahme

- Keine Runtime, keine Messung, keine Beschaffung, keine Empfehlung.
- Keine Authority-, Promotion- oder Consent-Wirkung.
- Kein neues Statussystem, kein neuer Claim-Tag, keine neue Entscheidungsleiter.
- Rücknahme: Diese Datei nach `NICHTRAUM/archive/` verschieben und die
  Begründung im Commit dokumentieren (G3). Kein Modul, kein Make-Target und
  kein Workflow importiert sie.

## 13. Offene Punkte

- [ ] ☐ Ob je eine Bench-Messung stattfindet, bleibt offen und folgt nicht aus
      diesem Dokument.
- [ ] ☐ Die fachliche Zuständigkeit für optische Messungen ist nicht benannt.
- [ ] ☐ Der Übergang M6 → M1 (semantische Bridge) bleibt bis zu einer eigenen
      Phase unimplementiert.
