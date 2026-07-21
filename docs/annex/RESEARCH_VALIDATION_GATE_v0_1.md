# RESEARCH_VALIDATION_GATE_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** none
**Human-Research-Status:** HOLD
**Promotion-Effect:** none
**Human-Decision-Boundary:** required
**Source:** Synthbiosis Systematlas v1.1 / `05_RESEARCH_VALIDATION_GATE.md`
(Bundle-Witness: `INBOX/INTAKE-2026-07-21-synthbiosis-system-atlas-v1_1.md`;
Crosswalk-Einstufung MISSING_REPO_SAFE:
`docs/audit/SYNTHBIOSIS_BUNDLE_CROSSWALK_v0_1.md`)

```yaml
source_relation:
  relation: reduced_public_annex
  source_identity: not_claimed
  semantic_equivalence: not_claimed
  known_loss_required: true

erk_reference:
  pull_request: 314
  state: open_draft
  reviewed_head: ef3393e9b40e6cc2a777c5b464909e5a42b5e7c6
  moving_target: true
  authority_effect: none
```

Dieses Dokument ist ein **methodischer Vertrag, kein Forschungsnachweis**.
Es implementiert nichts, erhebt nichts, rekrutiert niemanden und gibt
nichts frei.

---

## 1. Zweck

Die Kernfunktion von M5 lautet:

> Aus einer Idee wird entweder ein begrenzter Modellkandidat, eine testbare
> Hypothese, ein Simulationsvorhaben, ein Bench-/Feasibility-Plan — oder ein
> bewusster HOLD-Zustand.

M5 ist ausdrücklich **nicht**:

- ein Truth-Maker,
- eine Ethikkommission,
- eine medizinische Zulassung,
- eine automatische Studienfreigabe,
- ein Ersatz für fachliche Zuständigkeit,
- ein statistischer Zaubertrichter,
- ein Instrument, das normative Werte in Biomarker übersetzt.

## 2. Eingangsklassen

Jeder Intake benötigt **genau eine primäre Klasse**. Mehrdeutige Intakes
bleiben `CLASSIFICATION_UNDETERMINED`; es gibt keine automatische Wahl der
stärkeren Klasse.

| Eingangsklasse | Beispiel | zulässiger nächster Schritt | verbotener Kurzschluss |
|---|---|---|---|
| Normativer Wert | Würde, bedingungslose Liebe | Designprinzip, qualitative Prüfung | Wert → Biosignalproxy |
| Modellkandidat | PASS/Π, Resonanzkiel | Schema, Negativtest, Simulation | Modell → Realität |
| Physikalischer Komponentenclaim | Absorber-Transmission | Bench-Plan, Kalibrierung, Unsicherheit | Bauteil → Ethik |
| Human-Messclaim | HRV verändert sich unter Aufgabe X | Airlock, Datenplan, Präregistrierung | Biosignal → innerer Zustand |
| Wirksamkeitsclaim | System verbessert klinische Outcomes | HOLD im aktuellen Reifegrad | Pilot → Wirksamkeit |

## 3. Evidenzleiter

```
ROHSEDIMENT → MODEL → TESTABLE_HYPOTHESIS → SIMULATION_PROXY
    → BENCH_OR_FEASIBILITY → REPLICATED_EVIDENCE
```

**Verbindliche Invariante:**

> Keine Stufe wird durch rhetorische Kohärenz, Quellenmenge, UI-Qualität,
> ein Receipt, einen Hash oder eine menschlich bewegende Erfahrung
> übersprungen.

Zusätzlich gelten die harten Nicht-Gleichungen:

- Simulation Proxy ≠ Bench Evidence
- Bench Evidence ≠ Human Evidence
- Human Measurement ≠ Effectiveness
- Replication ≠ universelle Gültigkeit

### 3.1 ROHSEDIMENT

- **Zulässig:** „Diese Idee/dieser Fund existiert und hat eine Herkunft."
- **Unzulässig:** jede Geltungs-, Wirkungs- oder Messbehauptung.
- **Erforderliche Artefakte:** Herkunftspointer (Intake).
- **Mögliche Falsifier:** noch keine — es gibt noch keinen prüfbaren Satz.
- **Nächster Schritt:** Klasse zuordnen (§2), sonst `CLASSIFICATION_UNDETERMINED`.
- **Rücknahmepfad:** Intake bleibt liegen oder wird als [VOID] markiert; nichts wird gelöscht.

### 3.2 MODEL

- **Zulässig:** „Unter diesen dokumentierten Annahmen beschreibt Struktur X das Phänomen Y."
- **Unzulässig:** „Das Modell ist die Realität"; jede empirische Wirkung.
- **Erforderliche Artefakte:** Annahmenliste, Geltungsbereich, Negativbeispiel.
- **Mögliche Falsifier:** ein Fall im Geltungsbereich, den das Modell nicht abbilden kann.
- **Nächster Schritt:** testbare Hypothese formulieren oder bewusst als Modell parken.
- **Rücknahmepfad:** Modell wird als überholt markiert (append-only), nicht überschrieben.

### 3.3 TESTABLE_HYPOTHESIS

- **Zulässig:** ein präziser, falsifizierbarer Satz mit definierter Messgröße.
- **Unzulässig:** metaphorische Gesamtfragen; Hypothese als Ergebnis ausgeben.
- **Erforderliche Artefakte:** Operationalisierung, Falsifier, erwartetes Nullresultat — **vor** dem Test.
- **Mögliche Falsifier:** explizit benannt, sonst ist es keine Hypothese dieser Stufe.
- **Nächster Schritt:** Simulation oder (für Humanclaims) Airlock §4 — niemals direkt Erhebung.
- **Rücknahmepfad:** Hypothese wird als verworfen/nicht bestätigt dokumentiert; Nullresultate sind berichtenswert.

### 3.4 SIMULATION_PROXY

- **Zulässig:** „Im synthetischen Setting S mit Modellgrenze G zeigt sich Verhalten V."
- **Unzulässig:** synthetischer Erfolg als reale Wirkung; Proxy-Daten als Empirie.
- **Erforderliche Artefakte:** Datensatz-/Modellgrenze, Seed/Parameter, Auswertungsplan.
- **Mögliche Falsifier:** Verhalten verschwindet unter deklarierten Variationen.
- **Nächster Schritt:** Bench-/Feasibility-Plan — mit neuem, eigenem Review.
- **Rücknahmepfad:** Simulation wird als nicht übertragbar markiert; Grenze bleibt dokumentiert.

### 3.5 BENCH_OR_FEASIBILITY

- **Zulässig:** „Unter definierten Bedingungen zeigt Komponente/Pipeline X reproduzierbar Messwert M mit Unsicherheit U."
- **Unzulässig:** Wirksamkeits-, Ethik- oder Governanceaussagen; Feasibility als Ergebnisqualität.
- **Erforderliche Artefakte:** Kalibrierung, Wiederholungen, Unsicherheit, Negativpfad, Rohdaten-Pointer.
- **Mögliche Falsifier:** Nicht-Reproduktion unter denselben Bedingungen; Drift/Degradation.
- **Nächster Schritt:** für Humanfragen ausschließlich Airlock §4; für Komponenten M1-Bridge (semantische Zuordnung separat).
- **Rücknahmepfad:** Messreihe wird mit Befund zurückgezogen; Rohdaten bleiben referenziert.

### 3.6 REPLICATED_EVIDENCE

- **Zulässig:** „Der Effekt wurde im deklarierten Design unabhängig repliziert."
- **Unzulässig:** universelle Gültigkeit; Übertragung auf andere Populationen/Domänen ohne neues Design.
- **Erforderliche Artefakte:** unabhängige Replikation, eingefrorener Analyseplan, vollständige Berichtslage inkl. Nullresultaten.
- **Mögliche Falsifier:** fehlgeschlagene Replikation; Designfehler.
- **Nächster Schritt:** externe fachliche Einordnung; im Repo höchstens scoped [FACT]-Kandidat nach menschlicher Entscheidung.
- **Rücknahmepfad:** Retraction-Semantik — append-only, Historie bleibt.

## 4. Human-Research Airlock

Vor Kontaktaufnahme, Rekrutierung oder Datenerhebung müssen mindestens
vorliegen:

1. **Intended Purpose** — Research, Wellness-Demo, medizinischer Zweck oder
   Enterprise Governance sind getrennt zu benennen.
2. **Präzise Forschungsfrage** — keine metaphorische Gesamtfrage.
3. **Primärer Endpunkt** — vor Beginn operationalisiert.
4. **Beobachtung oder Intervention** — explizit unterschieden.
5. **Sensorvalidität** — Gerät, Messrate, Genauigkeit, Artefaktbehandlung
   und Ausschlussregeln.
6. **Risiko- und Abbruchpfad** — einschließlich unerwarteter Ereignisse und
   Zuständigkeit.
7. **Datenfluss** — Rechtsgrundlage, Zugriff, Pseudonymisierung, Retention
   und Löschung.
8. **Unabhängige Zuständigkeits-/Ethikentscheidung** — das Framework trifft
   sie nicht selbst.
9. **Vorab eingefrorener Analyseplan** — Endpunkte, Ausschlüsse, Statistik,
   Nullresultate und Abweichungsregeln.
10. **Keine Biomarker-Identifikation normativer Begriffe** — Liebe, Würde,
    Resonanz, Zustimmung oder Wahrheit werden nicht durch ein Sensorsignal
    operational identisch.

```yaml
airlock_source_note:
  source_condition_count: 9
  annex_condition_count: 10
  structural_expansion_only: true
  new_substantive_requirement: false
  note: >
    Der Quellkörper fasst Daten- und Risikostruktur enger zusammen; die
    öffentliche Fassung verteilt sie aus Lesbarkeitsgründen auf zehn Zeilen.
```

Humanforschung bleibt bis zum vollständigen und **extern zuständigen**
Review: **HOLD**. „Fast validiert" ist kein zulässiger Status.

## 5. HRV- und Körpersignal-Korrektur

Ausdrücklich erhalten bleibt:

- HRV ist kein Liebesmesser.
- HRV ist kein Resonanzmesser.
- HRV ist kein Wahrheitsmesser.
- LF/HF ist nicht pauschal „Kohärenz".
- Atemfrequenz, Haltung, Tageszeit, Bewegung, Medikamente, Fitness und
  Artefakte sind mögliche Confounder.
- Ein erster Pilot prüft höchstens Pipeline und Feasibility, nicht
  Wirksamkeit.

Eine enge, weiterhin **nur beispielhafte** Forschungsfrage darf lauten:

> Verändert eine klar definierte, nicht-klinische Aufmerksamkeitsaufgabe
> unter kontrollierten Bedingungen ausgewählte, vorab definierte Messgrößen
> gegenüber einer festgelegten Kontrollbedingung?

Diese Formulierung ist **keine** Studienfreigabe, keine Empfehlung und keine
Rekrutierungsaufforderung.

## 6. Phyphox- und Mehrphasen-Grenze (nicht normative Anschlussnotiz)

Phyphox oder eine vergleichbare Sensorinstanz darf später als
`acquisition_layer` dienen und liefern: Rohsignale, Zeitreihen, Geräte- und
Sensormetadaten, berechnete Merkmale, begrenzte Phasenkandidaten.

Sie darf **nicht** liefern: Wahrheit über eine Person, psychologische
Diagnose, Consent, normativen Wert, Liebe oder Resonanz als Messwert,
klinische Wirksamkeit, automatische Forschungsfreigabe.

**Zulässiger Fluss:**

```
Sensorsignal → Observable → Feature → Model Candidate
    → Research Gate → menschliche und fachliche Prüfung
```

**Unzulässiger Fluss:**

```
Sensorsignal → innerer Zustand → Wahrheit → Governancewirkung
```

Ein Phasenlabel wie `BASELINE_CANDIDATE`, `TRANSITION_CANDIDATE` oder
`REENTRY_CANDIDATE` bleibt Modelloutput und darf nicht als Selbstaussage
der Person behandelt werden. Diese Fassung enthält keine `.phyphox`-Datei
und keinen Sensorcode.

## 7. Präzisionswächter

- Keine willkürlichen Resonanzstärken wie „0.9" ohne Messdefinition.
- Ein Θ-Score ist höchstens Priorisierungsheuristik.
- Harte Risiken sind Constraints, keine negativen Gewichte in einer
  Gesamtsumme.
- Mehrere ähnliche oder „hochresonante" Kontexte erzeugen keinen
  Evidenzbonus.
- Falsifikations- und Nullresultate werden vor dem Test festgelegt.
- Missing Data darf nicht automatisch positiv interpretiert werden.
- Messpräzision ist keine semantische Präzision.
- Ein valides Instrument für Merkmal X validiert nicht automatisch die
  Interpretation Y.

## 8. Nicht ausführbares Claim-Review-Template

Dokumentarisches Template — es wird nicht ausgeführt, erzeugt keine
Eventtypen und keine HumanDecision, ist kein neues Policy-Schema und kein
Ersatz für ERK oder M1. Keine dynamischen Scores.

```yaml
research_claim_review:
  claim_id: local_annex_identifier
  input_class: normative_value | model_candidate | component_claim | human_measurement_claim | effectiveness_claim
  intended_purpose:
  research_question:
  primary_endpoint:
  observation_or_intervention:
  measurement_definition:
  instrument_and_version:
  confounders: []
  exclusion_rules: []
  falsifier:
  expected_null_result:
  risk_constraints: []
  data_flow:
  retention_and_deletion:
  ethics_or_authority_status:
  analysis_plan_frozen: false
  current_evidence_stage:
  known_loss: []
  status: HOLD
```

## 9. Verhältnis zu den anderen Modulen

**M5 ↔ M1:** M5 prüft methodische Zulässigkeit; M1 hält die semantische
Übertragung und ihren Verlust sichtbar. Keines ersetzt das andere.

**M5 ↔ M6:** M6 darf einen Komponentenclaim nur über M5 weitergeben:

```
M6 component claim → M5 bench/method review
    → M1 semantic bridge → M4 governance review
```

Kein direkter Hardware-zu-Ethik-Pfad. M6 bleibt bis zur Akzeptanz dieses
Gates HOLD.

**M5 ↔ ERK:** Ein M5-Ergebnis kann später als Material oder
EvidenceRelation in einen ERK-Flow eingehen (Referenzstand:
`erk_reference`, Head `ef3393e9…`). Es kann niemals
`HumanDecision(APPROVE)` synthetisieren, selbstständig retaggen oder
Claim-Wahrheit feststellen.

**M5 ↔ tesser3TAKT:** Das Wort „HOLD" besitzt verschiedene lokale Rollen.
Research-HOLD bedeutet: „Voraussetzungen für methodische oder menschliche
Forschung fehlen." Es ist weder automatisch M2-Navigations-HOLD noch
ERK-Guard-HOLD noch Claim-[VOID]. Keine automatische Übersetzung.

## 10. Externe Forschungsanschlüsse (`methodological_neighbors`)

Diese Anschlüsse sind methodische Nachbarn aus dem Quellkorpus — **keine
Bestätigung des Frameworks**. Kein neuer Literaturreview in diesem Pass;
die Links sind historische Pointer aus dem Bundle (Stand 2026-07-16) und
wurden hier nicht erneut aufgelöst.

| Anschluss | möglicher methodischer Nutzen | Domänen-/Sensor-/Populationsunterschied | Privacy-/Bias-Grenze | historischer Pointer |
|---|---|---|---|---|
| SΩI / O-Information | höherordentliche Synergie-/Redundanzanalyse | Informationstheorie, keine Projekt-Domäne | kein Resonanz- oder Bewusstseinsbeweis | hf.co/papers/2402.05667 |
| CausalDynamics | Benchmarkdesign für dynamische Kausalmodelle | simulierte Benchmarks, keine Domänenvalidierung | Simulation ≠ Empirie | hf.co/papers/2505.16620 |
| DeepPhys | methodischer Nachbar kontaktloser Physiologie | andere Sensorik und Population | Privacy und Bias separat zu prüfen | hf.co/papers/1805.07888 |
| Wearable Foundation Models | Skalierungs-/Repräsentationsforschung | hochsensibler Datenraum, andere Geräteklasse | keine lokale UI-LAB-Freigabe ableitbar | hf.co/papers/2312.05409 |

## 11. Exit-Semantik

M5 besitzt in v0.1 **keinen Runtime-Zustandsautomaten**. Die ANNEX-Fassung
kann nur feststellen: **HOLD** — oder in natürlicher Sprache:

> Die Voraussetzungen sind vollständig genug für eine menschliche und
> fachlich zuständige Prüfung.

Nicht erlaubt ohne externe, zuständige und konkret dokumentierte
Entscheidung: `PASS`, `VALIDATED`, `PROVEN`, `SAFE`, `CLINICALLY_READY`,
`ETHICALLY_APPROVED`.

Der Abschluss des Gates ist keine Forschungsfreigabe, sondern höchstens
**ELIGIBLE_FOR_EXTERNAL_REVIEW** — als beschreibende ANNEX-Formulierung,
nicht als Runtime-Status und nicht als Claim-Tag.

## 12. Known Loss gegenüber dem Quellmodul

Sichtbare Verluste dieser reduzierten Fassung (`known_loss_required: true`):

- Die Kurzprosa und Beispieldichte des Quellmoduls wurden gestrafft;
  einzelne Formulierungen sind nicht wortidentisch (`source_identity:
  not_claimed`).
- Die Airlock-Struktur wurde von neun auf zehn Zeilen verteilt
  (`structural_expansion_only: true`, keine neue materielle Anforderung).
- Die Forschungs-Links wurden nicht erneut aufgelöst und gelten als
  historische Pointer.
- Die Evidenzleiter-Stufenbeschreibungen (§3.1–3.6) sind eine
  ANNEX-Ausarbeitung der knappen Quellleiter; sie erweitern die Leiter
  nicht um neue Stufen.
- Phyphox-Notiz (§6) ist eine Anschlussnotiz dieser Fassung; das
  Quellmodul nennt Phyphox nicht.

## 13. Grenzen

- Keine Runtime, keine Erhebung, keine Rekrutierung, keine Empfehlung.
- Keine medizinische Zweckbestimmung, keine Wirksamkeitsbehauptung.
- Keine Claim-Promotion; jede Statusänderung braucht menschliche
  Entscheidung (bei ERK-Anbindung zusätzlich die dortige
  HumanDecision-Grenze).
- Änderungen am ERK nach Head `ef3393e9…` erfordern einen neuen
  Drift-Check dieses Dokuments.
