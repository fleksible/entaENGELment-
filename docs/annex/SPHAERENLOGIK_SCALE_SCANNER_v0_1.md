# SPHAERENLOGIK_SCALE_SCANNER_v0_1

**Status:** [SPEC-WIP]  
**Authority-Status:** ANNEX · DERIVED  
**Runtime:** none  
**Persistence:** none  
**Human-Commit:** required

## 0. Zweck und Grenze

[FAKT] `ui-app/lib/tesser3takt-bridge.ts` kennt bereits die Auflösungsskala
`MICRO | MESO | MACRO`, implementiert aber bewusst nur eine
`MICRO -> MESO`-Brücke.

[FAKT] `ui-app/lib/tesser3takt-hud.ts` führt mit
`OUTER | INNER | INVERSE` eine separate projektive Observer-Achse.

[INFERENZ] Für den heutigen Theorie-Delta fehlt damit kein neuer ontologischer Layer,
sondern ein kleiner lesender Sidecar, der Skala, Traversalrichtung und Beobachterrolle
explizit auseinanderhält.

[FAKT] Dieser Sidecar ersetzt weder `MICRO_MESO_BRIDGE_v0_1`, tesser3TAKT,
Grimm-IR, Evidence Routing Kernel noch VOIDMAP.

[FAKT] Dieser Sidecar erzeugt keine Claim-Promotion, keinen Receipt, keinen Runtime-
Writeback und keine neue VOID-ID.

## 1. Minimaler Scan-Contract

```ts
type ScanScale = 'MICRO' | 'MESO' | 'MACRO';

type ScanDirection =
  | 'BOTTOM_UP'
  | 'TOP_DOWN'
  | 'BIDIRECTIONAL';

type ScanObserver =
  | 'EMBEDDED'
  | 'LIMINAL'
  | 'SPECTATOR_READ_ONLY';

type MesoRole =
  | 'compare'
  | 'contextualize'
  | 'translate'
  | 'route_candidate';

type ScanVerdict = 'PASS' | 'HOLD';

type UnresolvedState =
  | 'NONE'
  | 'CONFLICT'
  | 'MECHANISM_DIVERGENCE'
  | 'PROJECTED_ONLY'
  | 'OPEN_KENOGRAM';

interface ScaleScanCandidate {
  candidateStatus: 'candidate relation';
  sourceScale: ScanScale;
  targetScale: ScanScale;
  direction: ScanDirection;
  observer: ScanObserver;
  mesoRoles: readonly MesoRole[];
  provenance: readonly ProvenanceRef[];
  unresolvedState: UnresolvedState;
  verdict: ScanVerdict;
  humanCommitRequired: true;
}
```

[FAKT] `MesoRole` ist eine Verarbeitungsrolle, kein ontologischer Mittelbereich.

[INFERENZ] Meso kann dadurch Relationen vergleichen, kontextualisieren, übersetzen und
als Kandidaten routen, ohne Mikro oder Makro zu einer gemeinsamen Ursache zu erklären.

## 2. Harte Guards

[FAKT] Der Scanner trägt folgende Invarianten wörtlich:

```text
scale_shift != mechanism_identity
perspective_shift != ontic_change
overlap != collision
resonance != authority
observer != sovereign
```

[FAKT] Daraus folgen für den Scanner:

- [FAKT] Formähnlichkeit ist kein Nachweis gleicher Mechanismen.
- [FAKT] Perspektivwechsel ändert die Projektion, nicht automatisch den Gegenstand.
- [FAKT] Projektive Überlagerung ist kein Kontakt- oder Collision-Witness.
- [FAKT] Resonanz darf Kandidaten priorisieren, aber keine Authority erzeugen.
- [FAKT] Ein Beobachtermodus erzeugt keine Souveränität über beobachtete Perspektiven.

[FAKT] Mikro/Meso/Makro sind in diesem Sidecar Adressen einer Leseskala und keine
ontologische Hierarchie.

[FAKT] IIT ist, falls später referenziert, ausschließlich als inspirierte
Integrations-/Exclusion-Linse zulässig und nicht als Bewusstseinsbeweis.

[FAKT] Grimm Narration 2.0 bleibt Meaning Infrastructure, nicht Meaning Prescription.

[FAKT] entaENGELment koppelt souveräne Perspektiven; der Scanner besitzt sie nicht.

[FAKT] tesser3TAKT darf Traversierungen anbieten; daraus folgt kein persönlicher Telos.

## 3. PASS/HOLD-Guard

[FAKT] Ein lokales `PASS` ist ausschließlich dann zulässig, wenn alle vier
Reentry-Bedingungen für dieselbe Kandidatenrelation belegt sind:

```text
B1 = Resonanz
B2 = Persistenz
B3 = topologische Distinktheit
B4 = Stabilität nach Reentry
PASS <=> B1 && B2 && B3 && B4
otherwise HOLD
```

[FAKT] `PASS` bedeutet hier nur: Der Kandidat darf als weiterhin prüfbarer
`candidate relation` ausgegeben werden.

[FAKT] `PASS` bedeutet ausdrücklich keine CANON-, GOLD-, Runtime-, Claim- oder
VOID-Promotion.

[INFERENZ] Hohe interne Kohärenz ohne einen der vier Witnesses bleibt `HOLD`.

## 4. Observer-Semantik

[FAKT] `EMBEDDED` bezeichnet eine Leseposition innerhalb der aktiven
Traversal-Konfiguration.

[FAKT] `LIMINAL` bezeichnet eine Leseposition an einer noch nicht aufgelösten
Grenze zwischen Adressen oder Kontexten.

[FAKT] `SPECTATOR_READ_ONLY` bezeichnet eine Projektion, die Relationen lesen darf,
aber keine Zustände mutiert, Claims promotet oder Teilnehmerpositionen zusammenführt.

[INFERENZ] Diese drei Rollen sind nicht identisch mit dem bestehenden
HUD-`ObserverMode = OUTER | INNER | INVERSE`; ein späterer Adapter müsste die
Relation zwischen beiden Typen explizit dokumentieren.

## 5. Negative Fixtures

### Fixture N1 — ähnliche Form, verschiedene Mechanismen

[FAKT] Input:

```yaml
sourceScale: MICRO
targetScale: MACRO
direction: BOTTOM_UP
shapeSimilarity: high
microMechanism: reaction_diffusion
macroMechanism: constrained_transport
evidenceForMechanismIdentity: none
```

[FAKT] Erwartung:

```yaml
candidateStatus: candidate relation
unresolvedState: MECHANISM_DIVERGENCE
verdict: HOLD
promotion: forbidden
```

[FAKT] Guard: `scale_shift != mechanism_identity`.

### Fixture N2 — projektive Linienkreuzung

[FAKT] Input:

```yaml
observer: SPECTATOR_READ_ONLY
screenProjection: lines_cross
topologicalWitness: absent
exactStateIdentityWitness: absent
```

[FAKT] Erwartung:

```yaml
collisionClaim: false
unresolvedState: PROJECTED_ONLY
verdict: HOLD
promotion: forbidden
```

[FAKT] Guard: `overlap != collision`.

### Fixture N3 — Makromuster passt, Mikrodaten widersprechen

[FAKT] Input:

```yaml
macroPatternFit: true
microEvidence: contradicts
direction: BIDIRECTIONAL
```

[FAKT] Erwartung:

```yaml
candidateStatus: candidate relation
unresolvedState: CONFLICT
verdict: HOLD
promotion: forbidden
```

[FAKT] Der Makro-Fit darf den Mikro-Widerspruch nicht überschreiben.

### Fixture N4 — unzureichende Evidenz

[FAKT] Input:

```yaml
shapeSimilarity: plausible
provenance: partial
B1: true
B2: false
B3: unknown
B4: false
```

[FAKT] Erwartung:

```yaml
candidateStatus: candidate relation
unresolvedState: OPEN_KENOGRAM
verdict: HOLD
humanCommitRequired: true
promotion: forbidden
```

[FAKT] Es wird keine neue VOID-ID erzeugt; der offene Zustand bleibt Kenogramm, solange
eine bestehende Registry-/Kenogrammposition ausreicht.

## 6. Provenienzbindungen

[FAKT] Dieser Sidecar wurde gegen folgende bestehende Repo-Knoten gelesen:

- [FAKT] `docs/annex/MICRO_MESO_BRIDGE_v0_1.md` — Mikro→Meso, Verlust und Provenienz.
- [FAKT] `docs/spec/tesser3takt_hud_v0_2.md` — Projektions-/Collision-/Kenogramm-Guards.
- [FAKT] `docs/decisions/TRAVERSAL_GRAMMAR_v0_1.md` — Traversal ist keine Claim-Erzeugung.
- [FAKT] `docs/narratives/grimm2/GRIMM_IR_MEREOTOPOLOGY_INTAKE_v0_1.md` — Crossing ist nicht automatisch Kontakt/Overlap/Collision.
- [FAKT] `docs/spec/ruecknahme_operator.md` — Release statt versteckter Bindung.
- [FAKT] `ui-app/lib/tesser3takt-bridge.ts` — vorhandene Scale-Typen und Mikro→Meso-Vertrag.
- [FAKT] `ui-app/lib/tesser3takt-hud.ts` — bestehende Observer- und Kenogramm-Typen.
- [FAKT] `WELCOME.md` — User-Souveränität und Anti-Capture.

## 7. Nicht-Entscheidungen

[HYPOTHESE] Ein späterer Runtime-Adapter könnte ScaleDirection und ScanObserver als
read-only Metadaten neben bestehende Tesser-Frames legen.

[FAKT] Dieser v0.1-Sidecar entscheidet nicht, ob ein solcher Adapter nötig ist.

[FAKT] Dieser v0.1-Sidecar entscheidet nicht, ob `TOP_DOWN` oder
`BIDIRECTIONAL` jemals Runtime-Semantik erhalten.

[FAKT] Dieser v0.1-Sidecar entscheidet keine neue VOID-ID.

[FAKT] Jede Übernahme über ANNEX-WIP hinaus erfordert menschlichen Commit.
