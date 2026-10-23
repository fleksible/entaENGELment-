# Slice-Phasenübergabe v0.1

**Status:** ANNEX · DERIVED · [SPEC-WIP]

**FOKUS:** deklarierte Phasenübergabe prüfen

**Runtime:** separater Validator für einen ausdrücklich deklarierten Modellvertrag

**Runtime-Enforcement:** opt-in API; keine automatische HUD-Anbindung

**Promotion-Effect:** none

## 1. Ausgangslücke und begrenztes Ziel

[FAKT] [HUD-Spezifikation §8](../spec/tesser3takt_hud_v0_2.md#8-hermes--caduceus--wheeler--zn)
fordert sliceId, sourceFrameId, targetFrameId, phaseBefore, phaseAfter,
handedness, provenance und transformId. Das vorhandene Boundary-Paar führt diese
Phase nicht mit. Der [Methodenfall](METHODENFALL_BOUNDARY_PAIR_v0_1.md)
zeigt den Unterschied an gelesenen Daten und einem Gegenfall.

[ANNEX] Dieser erste Vertrag definiert eine prüfbare einzelne Modellphase.
Er ist ein neuer lokaler Entwurf; seine Einheiten und Orientierungslabels werden
nicht nachträglich der HUD-Spezifikation als bereits bestehende Festlegung
zugeschrieben. Die ursprüngliche Spezifikation wird nicht umgeschrieben.

## 2. Explizite Modellentscheidungen

| Angabe | Entscheidung dieser Fassung |
| --- | --- |
| Phase | Dimensionlose Umläufe, unit = turns; Werte im halboffenen Intervall [0,1). |
| Bezugssystem | Nichtleere basisId muss in Quellzustand, Zielzustand, Receipt und Transformdefinition übereinstimmen. Kein impliziter Basiswechsel. |
| Orientierung | handedness = LEFT oder RIGHT ist ein deklariertes Modelllabel und bleibt in dieser Fassung erhalten. Keine automatische Ableitung aus Portal-Farbe, Hopf- oder Körperbildern. |
| Transformation | Durch transformId benannter additiver Versatz deltaTurns im Bereich [-1,1], modulo 1. Keine ausführbaren fremden Transformfunktionen. |
| Numerik | Kreisabstand höchstens 1e-10 Umläufe. Ungültige, unendliche und nicht normalisierte Phasen werden zurückgewiesen. |
| Frames | sourceFrameId und targetFrameId binden zwei verschiedene, nichtleere Frame-Identitäten. |
| Slice | Beide Snapshots führen dieselbe logische sliceId wie das Receipt. Ein anderes Slice am gleichen Frame-Paar darf die Prüfung nicht bestehen. |
| Evidenz | Quell- und Zielphase kommen zusätzlich zum Receipt als eigene Snapshots; ein Receipt darf seine eigenen Vorher-/Nachher-Werte nicht allein bestätigen. |
| Provenienz | Receipt, beide Snapshots und Transformdefinition tragen den vorhandenen ProvenanceRef-Vertrag. Geprüft wird seine Struktur, kein kryptografischer Inhalt und keine Unabhängigkeit der Quellen. |

[ANNEX] Die beschränkte Transformation behauptet keine vollständige zN-, Lyra-,
Holonomie- oder Spinor-Dynamik. Phasen modulo 1 erhalten insbesondere keine
Windungszahl. Eine volle Umdrehung und Identität können denselben Endwert haben.
Eine andere Einheit, Orientierungstransformation oder Basisabbildung braucht
einen gesondert erklärten Vertrag.

## 3. Eingaben und Prüfreihenfolge

[ANNEX] `validateSlicePhaseTransport(receipt, source, target, transform)`
nimmt vier Laufzeiteingaben vom Typ unknown entgegen und liefert ein gültiges
Receipt nur bei erfolgreicher Prüfung zurück. Der Aufrufer muss vertrauenswürdige
Snapshots und die zugelassene Transformdefinition liefern; sie werden nicht
aus dem Receipt erzeugt oder automatisch als vertrauenswürdig erklärt.

1. Struktur, nichtleere Kennungen, Einheiten, Wertebereiche und Provenienz prüfen.
2. Quell-/Ziel-IDs und Slice-Kennung mit beiden Snapshots abgleichen;
   Selbstübergang zurückweisen.
3. Basis und Orientierung über die Eingaben hinweg abgleichen.
4. transformId mit der übergebenen Transformdefinition abgleichen.
5. phaseBefore gegen den Quellsnapshot, phaseAfter gegen den Zielsnapshot prüfen.
6. Den Zielwert unabhängig aus Quellphase und deklariertem Versatz modulo 1
   berechnen und gegen den tatsächlichen Zielwert prüfen.

[ANNEX] Fehlende Daten sind ein negatives Validatorergebnis, keine Nullphase.
Ein strukturelles PASS belegt die Konsistenz der gelieferten Eingaben. Es belegt
nicht, dass ein realer Producer diese Zustände gemessen oder erzeugt hat.

## 4. Die übrigen Übergabegrößen bleiben sichtbar

| Größe | Ergebnis dieses ersten Phasenvertrags |
| --- | --- |
| Boundary-pairId / Slice-Zuordnung | Bestehende Paaridentität bleibt im Boundary-Vertrag. Eine reale Zuordnung vom Paar zum Slice ist hier nicht hergestellt; stateId und frameId werden nicht gleichgesetzt. |
| Graining | Herkunft, Kantenfärbung und Transformregel bleiben UNRESOLVED; keine Ableitung aus der allgemeinen Receipt-Provenienz. |
| Blindseite | Inhalt und Verschiebung bleiben UNRESOLVED; fehlende Information wird nicht als leere Blindseite ausgegeben. |
| Sphärenstatus | INTRA gegenüber optionalem Hüllendurchbruch bleibt UNRESOLVED; ein Quadrantenwechsel entscheidet dies nicht. |

[ANNEX] Der separate Validator erweitert das vorhandene TesserTickFrame nicht.
Eine spätere Anbindung benötigt einen tatsächlichen Phasenproducer und dessen
Frame-/Slice-Zuordnung. Kη-03 bleibt UNBOUND. Dieser Patch erzeugt keine fiktiven
Phasen für die bestehenden HUD-Daten und erklärt keinen VOID für geschlossen.

## 5. Prüffälle und Anschluss

[ANNEX] Vor der Implementierung festgelegt: Normallauf, positiver und negativer
Umlauf über die Nullgrenze, widersprüchliche Frame- und Transform-IDs,
fehlende oder verschiedene Basis, Einheitenfehler, Orientierungswechsel,
falsche Vorher-/Nachher-Werte, unpassende Transformation, fehlerhafte Provenienz
und unvollständige bzw. nicht endliche Eingaben. Ein gültiges Boundary-Paar ohne
Slice-Receipt muss weiterhin als unzureichend für diese Phasenprüfung erkennbar sein.

[ANNEX] Auf diesem begrenzten Vertrag ist der separate
[Validator](../../ui-app/lib/tesser3takt-slice-phase.ts) implementiert; die
[Testsuite](../../ui-app/test/tesser3takt-slice-phase.test.mjs) enthält die
Gegenfälle einschließlich der numerischen Toleranz an der Nullgrenze.
Der ausgeführte Prüfstand steht im [Audit](../audit/2026-10-23_slice_phase_review.md).
Die neuen Gemini-/Qwen-Anforderungen bleiben gesonderte Adapterprüfungen.
