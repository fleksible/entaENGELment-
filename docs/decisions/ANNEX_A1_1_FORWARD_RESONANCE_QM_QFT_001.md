# ANNEX A1.1 Forward Resonance Note — QM/QFT

ID: `A1.1-FRN-QM-QFT-001`  
Status: `nektar_hold`  
Claim status: `HYPOTHESE`  
Placement: Annex A1.1, Section 3 — Traversal Grammar Placement, footnote/side-note only

> Operatorverwandtschaft ja. Identität nein.

## 0. Scope

This note records a forward resonance between the Brackwasser/Mündung motif and quantum-mechanical or quantum-field-theoretic transition language. It is not part of the A1.1 main proof path, not a motif test, not a physics claim, and not a canonical VOIDMAP registration.

A1.1 remains narrow:

```yaml
A1_1_main_question:
  focus: Brackwasser vs. Mündung
  not_focus:
    - Brackwasser/QM/QFT/Gesamtphysik
    - proof_by_physics
    - identity_claim_between_media
```

## 1. Forward resonance note

```yaml
forward_resonance_note:
  id: A1.1-FRN-QM-QFT-001
  status: nektar_hold
  claim_status: HYPOTHESE
  placement: "Annex A1.1, Section 3 — Traversal Grammar Placement, footnote/side-note only"
  observation: >
    Brackwasser/Mündung zeigt eine mögliche Operatorverwandtschaft
    zu quantenmechanischen und quantenfeldtheoretischen Übergangsformen:
    Superposition, Pfadintegral, Komplementarität und Dekohärenz/Messung.
  guard:
    medium_translation: active
    no_identity_claim: true
    no_physics_proof: true
```

## 2. Mapping precision

```yaml
mapping_precision:
  brackwasser:
    operator: gehaltene Koexistenz ohne sofortige Entscheidung
    qm_qft_near_reading:
      - kohärente Möglichkeitsschichtung
      - phasenhaltige Koexistenz
      - pre-decisive transition field

  muendung:
    operator: gerichteter Übergang mit irreversibler oder schwer reversibler Spur
    qm_qft_near_reading:
      - gerichtete Spurwerdung
      - loss_of_observable_coherence_as_image
      - transition_into_classically_readable_trace

  path_integral:
    cautious_reading: >
      Mehrere mögliche Wege tragen formal als Amplitudenbeiträge
      zur Übergangswahrscheinlichkeit bei, mit Gewichtung und Phase.
    avoid: >
      Nicht schreiben: alle Wege koexistieren gleichzeitig.

  superposition:
    cautious_reading: >
      Mehrere Zustandsanteile bleiben kohärent,
      solange keine dekohärente Festlegung dominiert.

  complementarity:
    cautious_reading: >
      Verschiedene Beschreibungsmodi bleiben gültig,
      aber nicht gleichzeitig im selben klassischen Bild totalisierbar.

  decoherence_measurement:
    cautious_reading: >
      Dekohärenz ist hier ein Mündungsbild,
      weil aus kohärenter Schichtung eine stabile Spur
      oder klassisch lesbare Struktur wird.
    guard: >
      Dekohärenz ist nicht automatisch Kollaps im starken Sinn;
      sie beschreibt zunächst den Verlust beobachtbarer Kohärenz
      durch Kopplung an Umgebung/Freiheitsgrade.
```

## 3. Densest formulation

> Brackwasser ist phasenhaltige Koexistenz; Mündung ist gerichtete, spurtragende Lesbarkeit.

Or:

> Brackwasser verhält sich zu Mündung wie kohärente Möglichkeitsschichtung zu gerichteter Spurwerdung — als Traversierungsähnlichkeit, nicht als Medienidentität.

## 4. VOID status

No canonical VOID ID is registered by this note. The bridge remains a candidate until VOIDMAP explicitly accepts it.

```yaml
void_link:
  status: candidate
  proposed_title: "Scale-Invariance Bridge: Brackwasser/Mündung ↔ Superposition/Dekohärenz"
  proposed_priority: P2
  touches_existing:
    - VOID-011 # if measurement grammar / resonance metrics are affected
    - VOID-010 # if taxonomy / spectra / physical assignment are affected
  registry_action: "VOIDMAP entry required before canonical ID"
```

## 5. Linter hooks

```yaml
LINT_FORWARD_RESONANCE_QM_QFT_001:
  fail_if:
    - Brackwasser is claimed to be quantum superposition
    - Mündung is claimed to be physical measurement or collapse
    - path integral is described as literal simultaneous coexistence of all paths
    - decoherence is treated as identical to strong collapse
    - physics is used to prove the motif
    - motif resonance is used to prove physics
    - note is promoted from nektar_hold to canonical claim without VOIDMAP registration

  warn_if:
    - analogy language becomes ontological language
    - medium translation strengthens claim status
    - QM/QFT language displaces the Brackwasser-vs-Mündung main question
    - the side-note starts behaving like a test protocol
```

## 6. A1.1 decision

```yaml
A1_1_decision:
  include_in_main_flow: false
  include_as_side_note: true
  note_role: forward_resonance_for_later_SCALE_INVARIANT_BRIDGE
  current_state: nektar_hold
  next_allowed_action: >
    Only register in VOIDMAP after explicit registry action.
```

## 7. Commit summary

This note preserves the QM/QFT resonance without crowning it. It keeps the Brackwasser/Mündung motif narrow, protects the medium-translation boundary, and stores the possible operator bridge in `nektar_hold` until VOIDMAP registration is explicitly requested.

> Die Intuition wird nicht verloren, aber auch nicht gekrönt.
