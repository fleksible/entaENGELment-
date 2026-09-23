# ROSETTA_ATTRIBUTION_TAXONOMY_v0_1

**Status:** INTAKE · [SPEC-WIP] · [ROSETTA]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Promotion-Effect:** none

## 0. Zweck

[INFERENZ] Dieser Intake trennt ein beobachtetes Transformationsdelta von der
Frage, **wem oder welcher Bedingung es zugerechnet werden darf**.

```ts
type AttributionFactor =
  | 'INTERPRETER'
  | 'LANGUAGE_AFFORDANCE'
  | 'HISTORICAL_PATH'
  | 'EDITORIAL_CHOICE'
  | 'READER_REBINDING';

type AttributionStatus =
  | 'SUPPORTED'
  | 'PARTIAL'
  | 'CONTESTED'
  | 'UNKNOWN';

type AttributionCandidate = {
  deltaRef: string;
  factor: AttributionFactor;
  actorOrContextRef?: string;
  status: AttributionStatus;
  evidenceRefs: readonly string[];
  counterevidenceRefs: readonly string[];
};
```

## 1. Harte Guards

```text
observed_delta != known_cause_of_delta
language_affordance != linguistic_determinism
interpreter_contribution != source_content
historical_path != truth_inheritance
reader_rebinding != source_intention
agreement_density != evidence_of_origin
```

[INFERENZ] `LANGUAGE_AFFORDANCE` darf nur als Kandidat geführt werden: Eine
Zielsprache kann bestimmte Unterscheidungen oder Wortbildungen erleichtern, ohne
dadurch eine philosophische Entwicklung kausal zu erklären.

[INFERENZ] Ein `READER_REBINDING`, das die Rolle eines Ausdrucks verändert, ist
selbst ein **neues Transformationsereignis** und darf die historische Quellfassung
nicht überschreiben.

## 2. Historischer Pfad

Ein Pfad kann Relationen wie diese dokumentieren:

```text
TRANSLATES
COMMENTS_ON
READS_THROUGH
SYNTHESIZES
CRITICIZES
ATTRIBUTES_TO
REVISES
```

[FACT] Ein vorhandener Pfad erzeugt keine Wahrheitsvererbung.

```text
path_exists != truth_inherits
```

## 3. Nicht-Entscheidungen

- Kein Score für Attribution.
- Kein automatisches Schließen von `UNKNOWN`.
- Kein Personenprofil.
- Kein Ledger-/Blockchain-Schema.

**Verdict:** HOLD.
