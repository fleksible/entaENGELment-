# Grimm-IR Mereotopology Intake v0.1

**Status:** `[ANNEX]` `[SPEC-WIP]` `[ROSETTA]`  
**Date:** 2026-07-22  
**Scope:** local intake note; no canon promotion

## 1. Purpose

This note records the useful remainder of the Grimm Narrativ 2.0 discussion as a guarded, testable edge grammar. It is a sidecar between Grimm-IR and the tesser3TAKT Frame Contract v0.2, not a replacement for either contract.

The central distinction is:

> A projected crossing is not automatically a contact, an overlap, an identity, or a collision.

Layout may stretch, rotate, reorder, or flatten a scene. The relation, endpoints, direction, guard, reentry question, and provenance must survive those transformations.

## 2. Non-goals

This intake does not:

- assert identity between mythology, private experience, biology, chemistry, mathematics, or physics;
- derive `collisionProxy` from color, proximity, narrative equivalence, or a screen-space crossing;
- reconstruct protected personal material;
- change `TesserTickFrame`, `BoundaryTransition`, or their validation rules;
- update `docs/masterindex.md`, `VOIDMAP.yml`, policies, receipts, or runtime code;
- create a parallel source of truth for tesser3TAKT.

## 3. Minimal Grimm-IR shape

The following is an intake vocabulary, not yet a runtime TypeScript contract.

```ts
type GrimmIRRole =
  | 'SOURCE'
  | 'MOTIF'
  | 'OPERATOR'
  | 'BOUNDARY'
  | 'REENTRY'
  | 'READER';

type MereoRelation = 'DC' | 'EC' | 'PO' | 'TPP' | 'NTPP' | 'EQ';
type EdgeDirection = 'NONE' | 'FORWARD' | 'REVERSE' | 'BIDIRECTIONAL';
type CrossingStatus =
  | 'PROJECTED'
  | 'OVER'
  | 'UNDER'
  | 'TOUCH'
  | 'EXACT_STATE_ID';

interface GrimmSourceRef {
  sourceForm: string;
  sourcePointer: string | null;
  authorityStatus: 'repo-local' | 'external-unverified' | 'derived';
  sourceVisibility: 'public-safe' | 'protected-origin';
}

interface GrimmIRNode {
  nodeId: string;
  role: GrimmIRRole;
  label: string;
  claimLayer: string;
  provenance: GrimmSourceRef;
}

interface GrimmIREdge {
  edgeId: string;
  sourceNodeId: string;
  targetNodeId: string;
  relation: MereoRelation;
  direction: EdgeDirection;
  crossing: CrossingStatus;
  guard: string;
  reentryQuestion: string;
  transitionPairId?: string;
}
```

`GrimmSourceRef` is deliberately separate from the frame-level `ProvenanceRef`. In particular, `protected-origin` describes disclosure handling; it is not a new frame authority status.

## 4. Mereotopological edge grammar

| Code | Reading | Required distinction |
|---|---|---|
| `DC` | disconnected | no contact and no shared interior |
| `EC` | externally connected | boundary contact without shared interior |
| `PO` | partial overlap | shared interior while both retain a remainder |
| `TPP` | tangential proper part | contained and touching the container boundary |
| `NTPP` | non-tangential proper part | contained without touching the container boundary |
| `EQ` | equal region/state description | narrative equality alone is not a collision witness |

Crossing status is orthogonal to the relation:

- `PROJECTED`, `OVER`, `UNDER`, and `TOUCH` are view or scene facts. They never set `collisionProxy`.
- `EXACT_STATE_ID` is permitted only when the frame provides equal left/right state IDs under `collisionSemantics: EXACT_STATE_ID`.
- A Grimm-IR edge with `relation: EQ` but without the exact frame witness remains non-colliding.

An optional `transitionPairId` may point to `BoundaryTransition.pairId`. The frame owns pair validation, ordering, transformed-state checks, lattice checks, provenance checks, and collision semantics. Grimm-IR cannot overwrite them.

## 5. Orthogonal visual channels

Meaning must remain recoverable when color and motion are removed.

| Channel | Carries | Must not carry alone |
|---|---|---|
| line pattern | mereotopological relation | truth or authority |
| text label | explicit relation code and plain-language reading | decorative mood |
| arrow | direction | relation class |
| color | claim/translation layer | identity, collision, or validity |
| opacity | provenance availability/depth | certainty |
| crossing marker | projection/over/under/touch/exact-witness status | contact by appearance |

Every edge therefore has a relation label, line pattern, direction marker, static fallback, guard, and reentry question. Color and animation may enrich the view but are not required to read it.

## 6. Reader membrane

The reader remains an active boundary, not a passive target. Each offered relation supports four reversible actions:

- `ACCEPT` — keep the proposed edge for the current reading;
- `REVISE` — change its relation, wording, or provenance link;
- `REJECT` — remove the proposed edge from the current reading;
- `SILENCE` — leave the edge uncommitted without forcing a decision.

These actions do not diagnose the reader, infer private states, or promote a claim. At narrow width the reading order is fixed as title, relation, endpoints, guard, and reentry question.

## 7. Protected origins

Protected personal material may contribute only a non-reconstructable structural note. The public form records that a boundary, detour, or translation pressure existed; it does not store identifying events, names, quotations, or a reverse path to the origin.

For `sourceVisibility: protected-origin`, `publicReconstructionAllowed` must be `false` in fixtures and later implementations.

## 8. Limited motif roles

| Motif | Limited role | Guard / non-claim |
|---|---|---|
| Förster Hörst | listener and translator at the forest boundary | no authority over another person's inner state |
| Wood Wide Web | distributed-connection motif | no proof of intention, consciousness, or shared qualia |
| spore / mycelium | packet and substrate image | not a biological identity claim for software messages |
| gap junction | selective biological seam | not equivalent to a graph edge, mycorrhiza, or narrative link |
| toroidal garland | phase-sequence image | no quantum-spin assertion |
| absorber inertia | reversible scene memory | no physical continuum between Slater and Pauli |
| cone → lens → jet → Wheeler envelope | scene grammar for direction, wrapping, load, and reentry | Bernoulli and Coandă remain marked metaphors unless independently modelled |
| autopoiesis / qualia | relational description of self-maintaining interpretation | no transfer, measurement, or equivalence of experience |

Each motif remains subject to its source form, limited role, guard, and reentry question.

## 9. Fixtures and promotion gate

The companion fixture bundle contains exactly six qualitative counterexamples, one for each relation. The read-only validator checks:

1. complete relation coverage;
2. collision isolation to an exact frame witness;
3. non-reconstructability of protected origins;
4. plain-language guards and reentry questions;
5. colorless and static fallbacks;
6. the four reader actions and a 320 CSS-pixel content contract.

If a proposed edge type changes neither validation, reader rollback, nor provenance clarity, it is decoration and is not promoted.

Runtime promotion remains blocked until the fixtures pass and an actual Grimm-IR surface has been inspected at 320 CSS pixels with color removed and reduced motion enabled. This ANNEX introduces no such surface.

## 10. Reentry question

Which single relation or reader action would a future implementation make measurably clearer, without converting metaphor into evidence or screen-space overlap into collision?
