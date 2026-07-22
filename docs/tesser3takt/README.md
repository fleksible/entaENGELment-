# tesser3TAKT ANNEX Cluster

Claim-Tags: [FACT] [MODEL] [INFERENCE] [HYPOTHESIS] [METAPHOR]
Status: [ANNEX] — Local documentation index, keine Kanonisierung

## 0. Scope

This README indexes the local docs/tesser3takt/ ANNEX cluster.

It provides reading order, document roles, and guardrails for the local tesser3TAKT documentation bundle.

It does not promote any file to GOLD, VOIDMAP, receipt, or canonical status.

It does not modify global documentation indexes.

## 1. Local Reading Order

Recommended local reading order:

1. S4_LOGZN_bridge.md

Purpose:
Existing bridge between S4 and LOG-ZN.

Role:
Discrete reordering and continuous winding memory, without identity claim.

2. SOURCE_DECORATION_MAP_v0_1.md

Purpose:
Claim-hygiene map for external motifs.

Role:
Defines how source forms may become decorative or model roles through Guard and Reentry Question.

3. TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md

Purpose:
Main transition-navigation spec.

Role:
Defines three cubes, projection stack, monadic skin, mast, Schraegstellung, 720-degree reentry, Assembly-Navi operators, and PASS/HOLD/LOOP/STOP.

4. LYRA_STRINGS_COMPLEMENT_v0_1.md

Purpose:
Acoustic complement.

Role:
Defines Lyra as resonance body for POVs, seven strings, fourth string, harmony, disharmony, overtones, Fuehligkeit, and indirect player/source.

5. FUENFTER_KLANG_DEPTH_v0_1.md

Purpose:
Vertical depth module.

Role:
Defines essence, meaning, structure, manifestation, descent/ascent, movement grammar, integration loop, and bio/quantum decoration guards.

6. SANCHO_GUARD_v0_1.md

Purpose:
Fall-tolerant grounding module.

Role:
Defines Don 6, Sancho 5, Sanchos Rueckenpanzer, 5-over-6 beat, landability, and fall-tolerance.

## 2. Cluster Summary

Der tesser3TAKT-Cluster beschreibt Uebergaenge als lokal dokumentierte ANNEX-Navigation: Raum wird geschnitten, Klang wird gestimmt, Tiefe wird geoeffnet, Druck wird gelesen, und Sancho macht das Ideal landefaehig.

## 3. Guardrails

No file in this folder proves tesser3TAKT through physics, mathematics, biology, music, literature, or metaphysics.

No file in this folder claims identity between source domains and framework mechanisms.

External motifs must remain traceable through SOURCE_DECORATION_MAP_v0_1.md.

Every motif requires role, guard, and reentry question.

Future edits should remain ANNEX unless explicitly promoted through the repository process.

## 4. Non-Goals

This README does not update docs/masterindex.md.

This README does not update VOIDMAP.yml.

This README does not create receipts.

This README does not define empirical validation.

This README does not introduce Path Integral, new physics motifs, or additional expansion layers.

## 5. Next Possible Steps

Review the five-file cluster for consistency.

Optionally add a future VOIDMAP proposal in a separate explicit GOLD-change step.

Optionally create a later PATH_INTEGRAL_ASSEMBLY_NOTE only after the local cluster is stable.

Optionally link this README from docs/masterindex.md only after explicit approval.


## Frame Contract v0.2

The UI frame contract is represented by `ui-app/lib/tesser3takt-frame.ts` and the minimal serializable fixture `ui-app/fixtures/tesser3takt-minimal-frame.json`. The v0.2 contract keeps kenograms as UI-local `kenograms`, derives `collisionProxy` from `leftStateId`, `rightStateId`, and `collisionSemantics: EXACT_STATE_ID`, and makes `boundaryTransitions` first-class frame data.

Each boundary pair must contain exactly one ordered `EXIT` and one `ENTRY`, use unique half IDs per pair, link the entry to the exit via `transformedFrom`, and validate the knight move in the explicitly shared `GLOBAL_REENTRY_LATTICE` coordinate space rather than subtracting unrelated quadrant-local coordinates. Every boundary transition and frame-level witness carries a typed `ProvenanceRef` with source, revision, optional `digest`, explicit `digestStatus`, locator, claim layer, and authority status. An unverified pointer uses `digest: null` plus `digestStatus: UNVERIFIED`; it never uses a hash-looking placeholder.

JSON and transport inputs must enter through `validateTesserTickFrame`. The runtime validator checks the complete serialized shape, requires every transition to name `GLOBAL_REENTRY_LATTICE`, verifies the EXIT/ENTRY pair invariant, rejects a supplied `collisionProxy` that disagrees with the state IDs, and enforces the `digest`/`digestStatus` relation. TypeScript annotations alone are not an input boundary.
