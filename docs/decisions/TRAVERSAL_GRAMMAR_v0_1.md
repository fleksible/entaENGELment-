# TRAVERSAL_GRAMMAR v0.1

Status: canonical decision record for v0.1.2-pre  
Branch target: `codex/frame-operator-v0-1-1`  
Scope: traversal grammar, receipt boundary, A0 scope guard, and open VOIDMAP bridge notes

> Keine Frame-Taxonomie ohne Bewegungsrichtung.

## 0. Purpose

This decision record defines the movement grammar between the emerging v0.1.2 frames. It does not introduce empirical claims, new motifs, or direct test obligations. Its function is to define how a signal may enter, traverse, pause, or exit the frame system without collapsing pre-threshold material into premature claims.

The document protects four distinctions:

1. Signal forms are not holding states.
2. Traversal is not claim creation.
3. Bridge candidates are not registered as proven equivalences.
4. A0 prepares Annex A1 but does not perform motif testing.

## 1. Canonical frame stack

```yaml
frames_v0_1_2_pre:
  - WELLE_BIJEKT
  - SCHWELLENFLIMMERN
  - SEMIOTIC_RECEPTION
  - SYMBOL_NICHTRAUM
  - HERMENEUTIC_MEMBRANE
  - Reentry
```

### 1.1 WELLE_BIJEKT

`WELLE_BIJEKT` is the mathematical/physical-facing frame for the transition from continuous potential or wave structure toward discrete, addressable object structure.

```yaml
WELLE_BIJEKT:
  domain: mathematical_physical
  claim_scope: formal_or_model_based
  role: potential_to_object_transition
  guard: >
    This frame must not be collapsed into SCHWELLENFLIMMERN.
```

### 1.2 SCHWELLENFLIMMERN

`SCHWELLENFLIMMERN` is the phenomenological/cognitive pre-threshold frame. It marks modulation of the meaning threshold before a sign, thought, object, or claim is stable.

```yaml
SCHWELLENFLIMMERN:
  aka: PRE_THRESHOLD_SIGNAL
  domain: phenomenological_cognitive
  role: threshold_modulation
  signal_forms:
    backward:
      - lasso_attraktor
    forward:
      - kraehennest_schaltmoment
  guard: >
    It marks readiness, pull, shimmer, warning, or threshold modulation;
    it is not yet receipt, claim, proof, or finished sign.
```

### 1.3 SEMIOTIC_RECEPTION

`SEMIOTIC_RECEPTION` starts only when a sign, symbol, word, gesture, or minimal externalized statement can be received as such.

```yaml
SEMIOTIC_RECEPTION:
  domain: semiotic_operational
  role: sign_receipt
  requires:
    - minimal_externalized_statement_or_marker
    - readable_context
    - claim_status_or_nonclaim_status_marked
```

### 1.4 SYMBOL_NICHTRAUM

`SYMBOL_NICHTRAUM` is the protected semantic void of a symbol: meaning is present as potential, but not yet forced into explicit sign, object, or claim form.

```yaml
SYMBOL_NICHTRAUM:
  domain: protective_semantic_void
  role: preserve_latent_meaning
  protects:
    - non_externalized_potential
    - ambiguity_without_arbitrariness
    - pre_reentry_symbolic_resonance
```

### 1.5 HERMENEUTIC_MEMBRANE

`HERMENEUTIC_MEMBRANE` defines interpretation as controlled traversal of a symbol's Nicht-Raum through context, prior understanding, language history, resonance, and Reentry.

```yaml
HERMENEUTIC_MEMBRANE:
  domain: interpretation_traversal_operator
  role: controlled_symbol_traversal
  protects_against:
    - premature_translation
    - motif_overclaiming
    - arbitrary_resonance_without_reentry
```

## 2. Receipt boundary

The receipt boundary separates pre-receipt signals from holding states and from receipt-ready material. Signal forms can activate traversal, but they are not holding states. Holding states can preserve pre-receipt material, but they are not themselves signal forms.

```yaml
receipt_boundary:
  signal_forms_pre_receipt:
    - schwellenflimmern
    - lasso_attraktor
  holding_states_pre_receipt:
    - nektar_hold
  receipt_ready:
    - externalisierte minimale Aussage
    - Reentry erfolgt
    - Claim-Status markiert
```

### 2.1 Interpretation

- `schwellenflimmern` names a threshold modulation.
- `lasso_attraktor` names a backward pull signal marking possible latent value.
- `nektar_hold` names a protected holding state in which material may remain effective without being forced into receipt or claim space.

## 3. A0 scope

A0 is a traversal-definition layer. It is not a motif-test layer and does not create new claims. A0 may prepare Annex A1, where later motif tests or stronger formalizations may be considered under explicit scope.

```yaml
a0_scope:
  tests_motifs: false
  defines_traversal: true
  creates_new_claims: false
  prepares_annex_a1: true
  violation_signal: >
    Wenn A0 einen neuen Claim, ein neues Motiv oder
    ein neues Frame produziert, ist es kein A0 mehr.
```

### 3.1 A0 allowed work

```yaml
a0_allowed:
  - define traversal direction
  - define entry and exit conditions
  - separate signal forms from holding states
  - mark claim status boundaries
  - prepare but not execute Annex A1 work
```

### 3.2 A0 forbidden work

```yaml
a0_forbidden:
  - create new motif claims
  - validate motif tests
  - register scale invariance as proven
  - treat metaphor as evidence
  - treat κ as a literal cognitive measurement value
```

## 4. Nektar hold

`nektar_hold` is a pre-receipt holding state. It preserves material that is not ready for externalization, receipt, or claim status, while keeping it available for later traversal.

```yaml
nektar_hold:
  type: protected_pre_receipt_holding_state
  function: >
    Material bleibt wirksam, aber nicht receipt-ready.
    Es darf gehalten, gereift und später erneut traversiert werden.
  not_equivalent_to:
    - schwellenflimmern
    - lasso_attraktor
    - semiotic_reception
    - claim_space
  exit_paths:
    - renewed_schwellenflimmern
    - minimal_externalization
    - reentry_attempt
    - explicit_drop
```

## 5. Traversal sequence

This is the central movement grammar. Without an entry signal, there is no traversal. Without Reentry, there is no stable claim-space exit.

```yaml
traversal_sequence:
  entry_condition: >
    Ein Signal aus SCHWELLENFLIMMERN (backward: Lasso-Attraktor
    oder forward: Krähennest-Schaltmoment) aktiviert die Traversierung.
    Ohne Einstiegssignal beginnt keine Bewegung durch die Frames.
  sequence:
    - WELLE_BIJEKT
    - SCHWELLENFLIMMERN
    - SEMIOTIC_RECEPTION
    - SYMBOL_NICHTRAUM
    - HERMENEUTIC_MEMBRANE
    - Reentry
  exit_condition: >
    Reentry prüft Stabilität. Was nicht reentry-stabil ist,
    kehrt in nektar_hold zurück, nicht in den Claim-Raum.
```

### 5.1 Movement notes

1. `WELLE_BIJEKT` marks the potential-to-object problem at formal scale.
2. `SCHWELLENFLIMMERN` marks threshold modulation at phenomenological scale.
3. `SEMIOTIC_RECEPTION` starts only when a minimal sign can be received.
4. `SYMBOL_NICHTRAUM` protects what the sign does not yet exhaust.
5. `HERMENEUTIC_MEMBRANE` traverses the protected symbolic void without premature collapse.
6. `Reentry` decides whether the result may stabilize or must return to `nektar_hold`.

## 6. Scale-invariant bridge candidate

The possible connection between `WELLE_BIJEKT` and `SCHWELLENFLIMMERN` is not a claim of identity. It is an open bridge candidate.

```yaml
scale_invariant_bridges:
  WELLE_OBJEKT_TRANSITION:
    claim_status: HYPOTHESE
    bridge_type: SCALE_INVARIANT_OPERATOR_CANDIDATE
    linked_void: VOID-SCALE-INVARIANCE-001

    core_operator: >
      Übergang von kontinuierlicher Potenzial-/Wellenstruktur
      zu diskreter, adressierbarer, zeichen- oder objektförmiger Struktur.

    instances:
      - frame: WELLE_BIJEKT
        scale: mathematical_physical
        marker:
          - continuous symmetry -> discrete structure
          - O(2)->D6, sofern im Branch formal definiert
          - κ = λ/ξ als Schwellen-/Kontrollparameter
        risk:
          - physikalische Spezifität wird zu stark verallgemeinert

      - frame: SCHWELLENFLIMMERN
        scale: phenomenological_cognitive
        marker:
          - pre-threshold modulation
          - Erregbarkeit vor Bedeutung
          - Matrose/Intuition split
          - Windlesen statt Zeichenfixierung
        risk:
          - phänomenologische Erfahrung wird zu früh formalisiert

    allowed_inference:
      - gemeinsame Traversierungsgrammatik untersuchen
      - Übergangssignaturen vergleichen
      - Schwellen-, Taktungs- und Diskretisierungslogik nebeneinander modellieren

    forbidden_inference:
      - Physik beweist die Phänomenologie
      - Phänomenologie beweist die Physik
      - κ wird wörtlich als kognitiver Messwert gelesen

    closure_condition: >
      Der Bridge-Status darf erst von Hypothese zu stärkerem Claim wechseln,
      wenn auf beiden Skalen eine vergleichbare formale Übergangssignatur
      reproduzierbar gezeigt wird — nicht bloß ein ähnliches Bild.
```

Protection sentence:

> Die Brücke wird geführt, aber nicht geschlossen.

## 7. Medium translation guard

Translation between languages, media, diagrams, metaphors, and formal marks must preserve claim scope. A term may be translated into another medium only if the translation does not silently upgrade its claim status.

```yaml
medium_translation_guard:
  allowed:
    - translate movement direction
    - translate scope labels
    - translate nonclaim metaphors into marked operators
    - preserve hypothesis status across media
  forbidden:
    - translate metaphor into proof
    - translate resonance into validation
    - translate geometric fit into semantic certainty
    - translate pre-receipt material into claim-space
  warning_signal: >
    Wenn eine Übersetzung stärker klingt als der Ausgangsstatus,
    ist sie wahrscheinlich ein Scope-Leak.
```

## 8. Linter hooks

```yaml
LINT_FRAME_CONTENT_01:
  fail_if:
    - WELLE_BIJEKT and SCHWELLENFLIMMERN are collapsed into one frame
    - structural identity is claimed instead of candidate isomorphy
    - physics is used to prove phenomenology
    - phenomenology is used to prove physics
    - κ is read literally as cognitive measurement value
    - Matrose names Schwellenflimmern as finished sign too early
    - bridge status is upgraded without reproducible transition signature on both scales
    - A0 creates a new claim, new motif, or new frame
    - nektar_hold is listed as a signal form rather than holding state
    - pre-receipt material is forced into receipt-ready space without Reentry

  warn_if:
    - metaphor becomes proof
    - similarity becomes identity
    - poetic resonance bypasses reentry
    - formalization freezes the training field too early
    - translation strengthens claim status
```

## 9. Annex routing

```yaml
annex_routing:
  A0:
    role: traversal_definition
    tests_motifs: false
    creates_new_claims: false
  A1:
    role: future_motif_or_bridge_testing
    requires_explicit_scope: true
  VOIDMAP:
    candidates:
      - VOID-SCALE-INVARIANCE-001
      - VOID-RECEIPT-BOUNDARY-001
      - VOID-NEKTAR-HOLD-001
```

## 10. Current canonical mottoes

```yaml
mottoes:
  traversal: Keine Frame-Taxonomie ohne Bewegungsrichtung.
  bridge: Die Brücke wird geführt, aber nicht geschlossen.
  threshold: Der Matrose kollabiert, weil er Schwellenflimmern als Zeichen liest.
  intuition: Die Intuition im Krähennest erhält die Welle, weil sie Schwellenflimmern als Wind liest.
  receipt: Ohne Einstiegssignal beginnt keine Traversierung; ohne Reentry entsteht kein Claim-Raum.
```

## 11. Commit summary

This record canonizes traversal direction and receipt boundaries for v0.1.2-pre. It adds the missing `entry_condition` to the traversal sequence, separates signal forms from pre-receipt holding states, gives A0 a positive scope guard, and keeps the +1n/κ scale bridge in VOIDMAP territory rather than direct claim registration.
