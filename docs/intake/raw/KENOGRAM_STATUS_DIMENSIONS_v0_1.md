# KENOGRAM_STATUS_DIMENSIONS_v0_1

**Status:** INTAKE · [SPEC-WIP] · [ROSETTA]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Migration:** none  
**Promotion-Effect:** none

## 0. Problem

[FACT] Der bestehende HUD führt `UNOBSERVED | UNBOUND | CONFLICT | WITHHELD |
FORBIDDEN` als eine Statusliste.

[INFERENZ] Diese Werte mischen verschiedene Dimensionen: epistemischen Zustand,
Mapping-Zustand, Consent/Visibility und Policy. Dieser Intake schlägt eine
**dimensionale Lesart** vor, ohne den HUD oder sein Schema in v0.1 zu ändern.

## 1. Kandidatendimensionen

```ts
type EpistemicState =
  | 'UNOBSERVED'
  | 'UNKNOWN'
  | 'UNDERDETERMINED'
  | 'CONTESTED'
  | 'RESOLVED_WITHIN_SCOPE';

type MappingState =
  | 'UNBOUND'
  | 'PARTIAL'
  | 'MAPPED'
  | 'NO_MAPPING_FOUND_WITHIN_SCOPE';

type ConsentState =
  | 'UNASKED'
  | 'PENDING'
  | 'ACCEPTED'
  | 'DECLINED'
  | 'WITHDRAWN';

type PolicyState =
  | 'ALLOWED'
  | 'RESTRICTED'
  | 'FORBIDDEN';

type VisibilityState =
  | 'UNSPECIFIED'
  | 'PRIVATE'
  | 'REDUCED'
  | 'SHARED';
```

## 2. Legacy-Crosswalk

```text
UNOBSERVED -> epistemicState = UNOBSERVED
UNBOUND    -> mappingState = UNBOUND
CONFLICT   -> epistemicState = CONTESTED (plus competing operators)
WITHHELD   -> no primitive target; derive from consent + visibility + scope
FORBIDDEN  -> policyState = FORBIDDEN
```

[INFERENZ] `WITHHELD` darf nicht automatisch bedeuten, dass ein Inhalt unbekannt
oder falsch ist. Es kann bedeuten, dass ein bekannter Inhalt privat bleibt oder
nicht geteilt werden soll.

[INFERENZ] `NO_MAPPING_FOUND_WITHIN_SCOPE` ersetzt **nicht** den stärkeren Begriff
`IRREDUCIBLE`. Irreduzibilität wäre ein eigener Claim und braucht Evidenz.

## 3. Guards

```text
unknown != withheld
withheld != forbidden
declined != false
unbound != unknowable
contested != majority_vote
visibility != truth_status
```

## 4. Nicht-Entscheidungen

- Keine Änderung an `docs/spec/tesser3takt_hud_v0_2.md`.
- Keine Änderung am UI-Schema.
- Keine neue VOID-ID.
- Keine automatische Migration bestehender Kenogramme.

**Verdict:** HOLD bis Fixtures und Human Reentry zeigen, dass die Achsen praktikabel
und nicht unnötig redundant sind.
