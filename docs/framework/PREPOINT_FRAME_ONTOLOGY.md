# PREPOINT_FRAME_ONTOLOGY

> Operative sidecar to [THEORETICAL_LINEAGE.md](THEORETICAL_LINEAGE.md).
> Claim tags: [MET] metaphor · [HYP] hypothesis · [TEST] testable assertion · [VOID] open / unresolved

---

## 1. Prepoint Field

**Definition:** The prepoint field is the sub-symbolic layer that precedes the
assignment of positional identity to any mark. It is not empty space — it is
the structured *potential* from which discrete positions (kenograms, then signs)
emerge.

[HYP] The prepoint field is always plural: no single prepoint exists in
isolation. Multiplicity is its ground state.

[MET] Analogy: as a dark medium carries wave potentials before any crest
becomes distinguishable, the prepoint field carries positional potential before
any mark is fixed. This analogy is structural, not physical — no claim about
dark energy or cosmological fields is intended.

**Relation to Kaehr's kenogrammatik:**
A kenogram is a prepoint that has been assigned a positional slot but not yet a
value. The prepoint field is therefore logically prior to kenogrammatic space.

---

## 2. Frame

**Definition:** A frame is the experiential threshold at which prepoint
multiplicity temporarily appears as a single coherent point.

[HYP] The frame is not a container. It is an event — a crossing threshold that
produces the *appearance* of unity from underlying plurality.

[MET] "Event horizon" is used here analogically: the frame is the boundary
beyond which the observer cannot see the prepoint structure, not a physical
singularity.

**Properties:**

| Property | Description |
|----------|-------------|
| Threshold character | Frame is a transition, not a region |
| Temporary | Frame coherence is maintained only while alignment holds |
| Observer-relative | What counts as a frame depends on the observing system |
| Re-entrant | Frame outputs can become prepoints for the next frame event |

---

## 3. Point

**Definition:** A point is a local alignment-coherence event. It is not an
atomic origin or smallest indivisible unit — it is a *result* of frame
processing.

[HYP] Points are emergent: they arise when the frame achieves sufficient
coherence across prepoint multiplicity to produce a stable registration.

[TEST] Repo test proxy: a metric that passes the Phi-gate threshold (`phi ≥ 0.618`)
is treated as a "coherent point" in the ECI measurement pipeline. This is a
computational operationalisation, not a direct test of the ontological claim.

**Distinction from classical geometry:**
Classical geometry treats points as primitive. This ontology treats points as
derived — which is why L-vor-T (Latent before Terminal) is architecturally
prior: the system must traverse the prepoint/frame sequence before registering
a terminal value.

---

## 4. PCM Concepts

The following concepts from Polycontextural / Categorical Morphology (PCM) map
directly onto the prepoint/frame/point triad.

### 4.1 Crossing / X

[HYP] A Crossing event is the moment the frame threshold is traversed — the
transition from prepoint multiplicity to point coherence.

**Repo expression:** The `verify → receipt` handoff. The system crosses from
latent state (prepoint field) to terminal assertion (point = signed receipt).

### 4.2 Alignment

[HYP] Alignment is the condition that makes a Crossing possible. Before
alignment, prepoints remain distributed; after alignment, the frame can form.

**Repo expression:** ECI (Energetic Coherence Index) and Kuramoto r-bar measure
degree of alignment. `r_bar ≥ 0.9` [TEST] is used as operational proxy for
alignment sufficient to cross.

### 4.3 Kenogram

[MET] A kenogram is a prepoint that has received positional identity but not
yet value-assignment.

**Repo expression:** The ☐-marker. A ☐-tagged item occupies a kenogrammatic
slot: position is fixed, value is pending (neither true nor false — Günther's
third locus).

### 4.4 Leakage

[HYP] Leakage is the partial collapse of frame coherence: alignment is
insufficient, so prepoint multiplicity bleeds through the frame boundary and
the point-event is degraded or ambiguous.

**Repo expression:** `spearman_rho` values with large negative magnitude
(e.g., `-0.798`, `-0.910` in BP-07/BP-08 metrics) indicate anti-correlation
that may signal leakage between subsystems rather than clean alignment.

[VOID] Whether negative rho systematically indicates leakage vs. inhibitory
coupling requires biological runs. Currently tagged `SIMULATION_PROXY`.

### 4.5 Return-Fenster (Return Window)

[HYP] After a frame event, there is a finite interval during which the system
can re-observe its own point-output as a new prepoint input. This is the
Return-Fenster.

**Repo expression:** The Receipt append-only trail. Each receipt becomes
available as a latent input for the next verify cycle. The window is bounded
by the append timestamp; after that boundary the receipt is IMMUTABLE and
can only be read, not re-processed.

[MET] Luhmann's re-entry of the distinction: the system observes itself
observing, but only within the temporal window before the next cycle closes.

---

## 5. Claim-Tag Summary

| Tag | Meaning in this doc |
|-----|---------------------|
| [MET] | Structural analogy — useful for reasoning, not a physical or empirical claim |
| [HYP] | Theoretical hypothesis — coherent, not yet operationalised in tests |
| [TEST] | Has a repo-level computational proxy — see linked metric or gate |
| [VOID] | Open: requires further evidence or biological runs to resolve |

---

## 6. What This Ontology Does Not Claim

- No physical claim about dark energy, event horizons, or quantum fields.
- No assertion that prepoint/frame/point maps one-to-one to biological
  membrane dynamics (that remains [VOID] pending BETSE runs).
- No claim that simulation proxies (tagged `SIMULATION_PROXY`) constitute
  empirical confirmation of any [HYP] above.

---

## 7. Links

- Lineage background: [THEORETICAL_LINEAGE.md](THEORETICAL_LINEAGE.md)
- ☐-marker usage: `src/core/metrics.py`, claim-lint rules
- Kenogram system: Kaehr references in THEORETICAL_LINEAGE.md §3
- Metrics artefacts: `data/metrics/framework_metrics_v2_populated.csv`

---

*Last updated: 2026-03-06*
