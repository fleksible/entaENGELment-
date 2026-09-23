# ROSETTA_MAPPING_TOPOLOGY_v0_1

**Status:** INTAKE · [SPEC-WIP] · [ROSETTA]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Promotion-Effect:** none

## 0. Zweck

[INFERENZ] Dieser Intake beschreibt nur die **Form einer dokumentierten
Zuordnung**. Er erklärt nicht, warum die Form entstanden ist und behauptet keine
semantische Identität.

```ts
type MappingCardinality =
  | 'ONE_TO_ONE'
  | 'ONE_TO_MANY'
  | 'MANY_TO_ONE'
  | 'MANY_TO_MANY';

type MappingCoverage =
  | 'TOTAL_WITHIN_SCOPE'
  | 'PARTIAL_WITHIN_SCOPE'
  | 'NO_MAPPING_FOUND_WITHIN_SCOPE';

type MappingTopology = {
  cardinality: MappingCardinality;
  coverage: MappingCoverage;
  sourceRefs: readonly string[];
  targetRefs: readonly string[];
};
```

## 1. Leseregeln

- **Split** ist ein Alias für `ONE_TO_MANY`.
- **Fusion** ist ein Alias für `MANY_TO_ONE`.
- `PARTIAL_WITHIN_SCOPE` bedeutet nur, dass nicht alle relevanten Elemente im
  deklarierten Scope abgedeckt sind.
- `NO_MAPPING_FOUND_WITHIN_SCOPE` ist **keine** Behauptung metaphysischer
  Irreduzibilität.

```text
mapping_cardinality != semantic_equivalence
one_to_one != identity
one_to_many != loss_by_itself
many_to_one != proof_of_fusion_cause
no_mapping_found != impossible_to_translate
```

## 2. Verhältnis zum Transformationsdelta

[INFERENZ] Eine `ONE_TO_MANY`-Zuordnung kann zugleich Verlust, Erhalt und
Einführung enthalten. Mapping-Topologie und Transformationsdelta sind daher
orthogonale Beschreibungen desselben Übergangs.

## 3. Nicht-Entscheidungen

- Kein Graph-Isomorphismus wird behauptet.
- Keine Kategorientheorie oder Ontologie wird vorausgesetzt.
- Kein Runtime-Adapter wird erzeugt.

**Verdict:** HOLD.
