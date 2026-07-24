# MICRO_MESO_BRIDGE_v0_1

**Status:** Draft

**Claim-Status:** [BRIDGE-WIP]

**Authority-Status:** ANNEX · DERIVED

**Datum:** 2026-07-24

**Runtime:** `ui-app/lib/tesser3takt-bridge.ts`

## 0. Zweck und Grenze

[SPEC-WIP] Dieser Annex definiert den ersten schmalen, falsifizierbaren
Mikro→Meso-Vertical-Slice für tesser3TAKT. Er aggregiert bereits validierbare
  `BoundaryTransition`-Paare zu einem abgeleiteten `TransitionTrace`. Der
  positive Fixture enthält zwei verkettete Paare, damit die Meso-Aggregation
  nicht auf einer trivialen Einpaar-Abbildung beruht.

Der Bridge-Layer:

- erzeugt keine neue Root-Authority,
- bewertet keine Evidenz semantisch,
- promotet keinen Claim,
- identifiziert Mikro- und Meso-Readout nicht miteinander,
- ersetzt weder ERK noch tesser3TAKT-Frame-Vertrag,
- schreibt nicht in GOLD, Receipts oder VOIDMAP.

Ein erfolgreicher Lauf heißt deshalb `PASS_CANDIDATE`, nicht `PASS`.

## 1. Eingangs- und Ausgangsadressen

| Seite | `resolutionScale` | `extentScope` | Form |
|---|---|---|---|
| Eingang | `MICRO` | `TRAVERSAL_CELL` | geordnete `BoundaryTransition[]` |
| Ausgang | `MESO` | `TRAVERSAL_SLICE` | abgeleiteter `TransitionTrace` |

Die beiden Achsen bleiben getrennt. Eine Änderung der Auflösung impliziert
nicht stillschweigend eine Änderung des räumlichen oder prozessualen Umfangs.

## 2. Mechanisch verlangte Mindestfelder

Jeder Request muss enthalten:

- nichtleere `bridgeId`,
- nichtleere `sourceFrameId` als Bindung an den Eingangsframe,
- explizite Mikro-/Meso-Skalenadressen,
- mindestens ein vollständiges EXIT/ENTRY-Paar,
- alle fünf erhaltenen Invarianten,
- eine nichtleere Verlustdeklaration,
- alle vier Falsifikatoren,
- mindestens eine Evidenzreferenz,
- einen registrierten Claim-Ursprung mit `immutable: true`.

Fehlt ein Element, lautet das Ergebnis:

```text
REJECT(BRIDGE_INCOMPLETE)
```

## 3. Erhaltene Invarianten

Die v0.1-Brücke verlangt:

1. `BOUNDARY_PAIR_IDENTITY`
2. `EVENT_ORDER`
3. `DIRECTIONAL_CONNECTIVITY`
4. `PROVENANCE_BINDING`
5. `ORIGIN_CLAIM_LEVEL`

Der Ausgang führt Paarreihenfolge, Ereignisreihenfolge, gerichtete
State-Verbindungen sowie EXIT-/ENTRY-Provenienz explizit weiter. Zwischen
aufeinanderfolgenden Paaren müssen State-ID und globale Lattice-Position des
vorherigen ENTRY mit dem nächsten EXIT übereinstimmen.

## 4. Verlust und Restdifferenz

[MODEL] Mikro und Meso werden verbunden, aber nicht gleichgesetzt. Der positive
Fixture deklariert deshalb mindestens:

- Verlust roher Timingdetails jenseits von `stepIndex`,
- Verlust von Per-Cell-Zustandsdetails, die nicht Teil eines
  `BoundaryTransition` sind.

Die Liste ist Teil des Trace und darf nicht leer sein. Sie ist keine Messung,
solange der Eintrag nicht ausdrücklich eine Messmethode und Einheit nennt.

## 5. Falsifikatoren

Die Brücke wird verworfen, wenn:

- eine EXIT-/ENTRY-Hälfte fehlt oder die Ereignisfolge umgeordnet wurde,
- `transformedFrom` die gerichtete Verbindung nicht bindet,
- Transition- oder Bridge-Provenienz fehlt,
- der Claim-Ursprung fehlt oder nicht als immutable deklariert ist.

Strukturell vollständige, aber relationell gebrochene Eingaben ergeben:

```text
REJECT(BRIDGE_FALSIFIED)
```

## 6. Claim- und Provenienzrollen

`origin.claimTag` verwendet die im
`docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md` inventarisierten Claim-Tags.
`PROVENANCE_ONLY` wird nicht als zusätzlicher Claim-Tag eingeführt, sondern als
separates `origin.evidenceRole` geführt.

Der Trace kopiert den Ursprung unverändert und friert ihn zur Laufzeit ein.
Ein Ursprung `METAPHER` kann durch die Brücke daher nicht zu `FACT` oder
`CANON` gewaschen werden.

## 7. Fixture und Tests

Positiver Fixture:

- `ui-app/fixtures/tesser3takt-micro-meso-bridge-v0.1.json`

Negativtests:

- fehlende Mindestfelder,
- fehlende einzelne Invarianten,
- fehlende einzelne Falsifikatoren,
- verwaiste Boundary-Hälfte,
- umgeordnete Ereignisse,
- gebrochene Konnektivität,
- lokal gültige, aber untereinander diskontinuierliche Paare,
- verlorene Provenienz,
- lösch- beziehungsweise überschreibbarer Ursprung,
- sparse oder malformed Transportdaten.

## 8. Nicht entschieden

[VOID] Diese v0.1 entscheidet nicht:

- ob das spätere Switchboard Verbindungen persistent speichert,
- ob mehrere Traversal-Slices zu einem größeren Meso-Graphen aggregiert werden,
- wie HumanDecision authentisiert wird,
- ob ein Bridge-Trace jemals Receipt-Status erhalten darf,
- ob `PASS_CANDIDATE` später einen eigenen ERK-Adapter bekommt.

Diese Fragen benötigen getrennte Reviews und dürfen nicht aus dem positiven
Fixture abgeleitet werden.
