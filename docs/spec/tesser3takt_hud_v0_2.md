# tesser3TAKT Kenogram HUD v0.2

**Status:** [SPEC-WIP]
**Authority:** ANNEX
**Artifact:** UI-LAB
**Route:** `/tesser3takt`

## 0. Purpose

The HUD is a read-only projection of the current tesser3TAKT / Grimm-Apparat working grammar. It makes relations, transformations, receipts, and unresolved fringes visible without turning the visualization into an ontology, diagnosis, personal telos, or oracle.

## 1. Hard separation: regime vs. guard

This is the principal v0.2 correction.

### Regime state

Derived only from model-display variables:

- `control` — dimensionless Landau control parameter;
- `orderParameter` — local display value `sqrt(abs(control))` for `control < 0`;
- `torsion` — Loosen/Tighten display parameter;
- `state` — `SYMMETRIC | CRITICAL | BROKEN | LOOSENED | OVERWOUND`.

Regime state changes the projection. It does not decide consent, truth, safety, or authority.

### Guard state

Derived only from explicit governance events:

- `consentFailed`;
- `focusSwitchPending`;
- `forbiddenCouplingAttempted`;
- `claimPromotionRequested`;
- `receiptPending`;
- `loopRequested`.

Guard output remains:

- `PASS`;
- `HOLD`;
- `LOOP`;
- `STOP`.

A slider must never produce `STOP` merely because a visual field is highly twisted, cold, hot, critical, or symmetrical.

## 2. Canonical transport and HUD view

`TesserTickFrame` v0.2 is the canonical transport contract defined in `ui-app/lib/tesser3takt-frame.ts`. Its required fields are:

```text
frameId
collisionSemantics
leftStateId
rightStateId
collisionProxy
kenograms
boundaryTransitions
provenance
```

The route-specific `TesserHudFrame` is a view model. It wraps the canonical object in `transport` and adds local display state such as observer mode, regime controls, z-layer, guard display, verification witnesses, and disabled semantic-assist configuration. Those view fields do not redefine the wire contract.

Both objects are serializable JSON. They contain no user identity, hidden interaction trace, inferred biography, or telemetry.

## 3. 7×9 and residual channel

Each local field contains `7 × 9 = 63` addressable cells.

The HUD exposes an additional unoccupied residual marker `X`:

```text
63 + X
```

`X` is not a sixty-fourth ordinary cell. It marks the unresolved or orthogonal channel that must not be silently filled by the renderer.

## 4. Knight graph witness

A standard knight graph on a 9-by-7 rectangular board has the following computed witness values:

```text
vertices: 63
edges: 164
connected: true
bipartite: true
diameter: 6
```

These values are verification witnesses for the formal graph only. They do not prove the narrative or physical layers.

## 5. Boundary half-step invariant

A quadrant-crossing move is one logical pair with exactly one `EXIT` and one `ENTRY` record. Both records share a `pairId` and carry:

```text
pairId
half
stepIndex
stateId
quadrant
coordinateSpace = GLOBAL_REENTRY_LATTICE
latticePosition
transformedFrom (ENTRY only)
provenance
```

The `ENTRY.transformedFrom` value must equal the paired `EXIT.stateId`, `EXIT` must precede `ENTRY`, and the two global lattice coordinates must form a legal knight move. The renderer derives its two visual marks from these canonical records; it does not maintain a second boundary identity.

## 6. S₄ permutation witness

The adjacent-transposition Cayley graph of `S₄` has:

```text
vertices: 24
edges: 36
regular degree: 3
connected: true
bipartite: true
diameter: 6
```

This supplies the reversible ordering space for local permutation operations. It is not identical to the 7×9 knight graph; both remain separate generator families.

## 7. Landau panel

The display potential is:

```text
V(phi) = 1/2 control phi^2 + 1/4 quartic phi^4
```

For `control = -0.34` and `quartic = 1`, the local minima occur at approximately:

```text
phi = +/- 0.583095
Vmin = -0.0289
```

The panel is a regime grammar only. It must be labeled as a model display and must never be described as measuring a person's psychological truth, moral state, coherence, love, or health.

## 8. Hermes / Caduceus / Wheeler / zN

- The orthogonal Hermes mast is an axis role.
- The two Caduceus channels are counter-rotating phase carriers.
- Wheeler slices are discrete projections of a continuous process.
- zN depth stores transformation between slices.

Required transport receipt:

```text
sliceId
sourceFrameId
targetFrameId
phaseBefore
phaseAfter
handedness
provenance
transformId
```

Depth is not inferred from screen distance alone.

## 9. Seven Lyra channels

The HUD carries exactly seven independent channels:

```text
C D E F G A B
```

The channels may map to sound, color, context, or another declared scale. A mapping requires a visible adapter and provenance. The seven channels must not be collapsed into six decorative fibers.

## 10. Portal antisymmetry

Orange and blue represent reversible complementary handedness directions.

The current collision proxy is intentionally narrow:

```text
leftStateId === rightStateId -> collisionProxy = true -> determinantProxy = 0
otherwise                    -> collisionProxy = false -> determinantProxy = 1
```

`collisionProxy` is derived by the canonical frame helper and validated against the two state IDs. The HUD cannot inject a manual collision boolean. A duplicate-row Slater determinant is zero; this witness supports only the formal collision metaphor and does not classify persons, moral positions, identities, or biological states.

Open question `Kη-04`: should collision use exact equality or equality up to an explicitly declared symmetry group?

## 11. Kenogram fringes

A fringe is not a generic error.

Allowed states:

- `UNOBSERVED` — not yet inspected;
- `UNBOUND` — anchors exist, connecting operator missing;
- `CONFLICT` — multiple operators compete;
- `WITHHELD` — relation intentionally not shared;
- `FORBIDDEN` — guard blocks the coupling.

Each fringe carries:

```text
id
status
layer
anchors
missingOperator or competingOperators
provenance
resolutionGate
allowPersistentVoid
```

A fringe may remain unresolved indefinitely.

## 12. Optional semantic assistance

The optional Hugging Face adapter is disabled by default:

```text
provider: hugging-face
modelRef: intfloat/multilingual-e5-small
enabled: false
role: candidate-neighbor-ranking
persistence: none
canResolveKenograms: false
canPromoteClaims: false
```

The adapter may later rank semantically similar existing nodes or receipts. It may not generate authority, close a VOID, infer a person, or write back without explicit review.

The model reference is an implementation candidate, not a dependency of the current route.

## 13. Knowledge-graph export

A future graph export must be flat and many-to-many. It may include cycles and cross-domain edges.

Every node and edge must preserve:

```text
claimLayer
provenance
projectionRole
authorityStatus
```

Graph centrality, visual position, or hub degree must not be interpreted as ontological origin, truth, importance, or personal telos.

## 14. Sierpiński and Assembly

The Sierpiński dimension witness is:

```text
log(3) / log(2) ~= 1.5849625007
```

Assembly depth may record minimal joining steps, reuse, and provenance. It must not be used as a proxy for:

- truth;
- moral value;
- human worth;
- Qualia depth;
- Nordstern proximity.

## 15. Consent and persistence

Current route:

```text
autoplay: false
telemetry: false
persistence: false
claimUpgrade: false
```

Any later persistence requires separate explicit consent for:

- points;
- edges;
- trajectories;
- semantic-neighbor suggestions;
- exports.

Consent must be revocable. No hidden reconstruction of the person is permitted.

## 16. Acceptance criteria

- mobile-first route `/tesser3takt`;
- seven visible Lyra channels;
- regime and guard shown separately;
- sliders affect regime only;
- consent failure produces `STOP`;
- claim-promotion request produces `HOLD`;
- portal collision remains reversible and does not automatically alter the guard;
- boundary halves share one transition ID;
- `63 + X` remains visible;
- backend frame is visible and serializable;
- unresolved kenograms remain visible;
- optional semantic assistance is disabled;
- no third-party runtime visualization dependency;
- build, lint, typecheck, overlap audit, and counterfixtures pass before promotion.

## 17. Hold

No VOIDMAP edit. No new canonical VOID identifier. No telemetry. No policy promotion. No automatic graph writeback. No equation of Landau, Slater, Pauli, Wheeler, Majorana, Sierpiński, Assembly, Kenogrammatics, or the HUD with human interiority.
