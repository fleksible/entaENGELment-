# ROSETTA_TRANSFORMATION_TAXONOMY_v0_1

**Status:** INTAKE · [SPEC-WIP] · [ROSETTA]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Persistence:** none  
**Promotion-Effect:** none  
**Human-Commit:** required

## 0. Zweck

[INFERENZ] Dieser Intake trennt **beobachtete Transformationsdeltas** von
Mapping-Form, Attribution, Consent/Policy und Provenienz.

Die kleinste v0.1-Form lautet:

```ts
type TransformationDelta = {
  preserved: readonly string[];
  lost: readonly string[];
  introduced: readonly string[];
};
```

Dabei gilt:

- `preserved` — eine benannte Relation/Eigenschaft bleibt im deklarierten Scope lesbar;
- `lost` — eine zuvor relevante Relation/Eigenschaft ist im Ziel nicht mehr erhalten;
- `introduced` — im Ziel erscheint eine relevante Relation/Eigenschaft, die in der
  Quellrepräsentation nicht als solche belegt ist.

## 1. Harte Trennung

```text
observed_delta != known_cause_of_delta
introduced != interpreter_intent
lost != failure
preserved != identity
preserved != truth
```

[FACT] `introduced` ist absichtlich akteursneutral. Eine spätere
Attributionsschicht darf prüfen, ob ein Interpreter, eine Sprachaffordanz, ein
historischer Pfad, eine editorische Entscheidung oder ein späterer Reader zur
Einführung beigetragen hat.

[INFERENZ] `split` und `fusion` sind keine Geschwister von
`preserved/lost/introduced`; sie beschreiben die **Form der Zuordnung** und
gehören in `ROSETTA_MAPPING_TOPOLOGY_v0_1`.

[INFERENZ] `withheld` ist ebenfalls kein Transformationsdelta. Consent,
Visibility und Policy werden separat geführt.

## 2. Scope-Regel

Jedes Delta muss mindestens binden an:

```text
sourceRef
targetRef
questionProvenance
scope
provenance[]
```

[FACT] Fehlt eine belastbare Ursache, bleibt die Ursache `UNKNOWN`; das beobachtete
Delta darf trotzdem als Kandidat sichtbar bleiben.

## 3. Nicht-Entscheidungen

- Kein Runtime-Typ.
- Keine automatische Migration des bestehenden Evidence Bridge Adapters.
- Keine Aussage über universale Übersetzbarkeit.
- Keine automatische Wahrheitspromotion.
- Kein FEP-/Active-Inference-Mechanismus.
- Kein Ledger-/Blockchain-Commit.

**Verdict:** HOLD bis die Stress-Fixtures und ein Human Reentry die Trennung stabil
bestätigen.
