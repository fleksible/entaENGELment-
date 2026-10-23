# Phasenquelle und Zuordnung v0.1

**Status:** ANNEX · DERIVED · [SPEC-WIP]

**FOKUS:** Phasenquelle und Zuordnung prüfen

**Gelesene Basis:** `e173790d4d883f1098fd37d6813dab7e608d2b96`

**Anbindung:** HOLD · keine ausgewählte HUD-Phasenquelle

**Promotion-Effect:** none

## 1. Ergebnis der Quellprüfung

[FAKT] Der [Slice-Prüfer](../../ui-app/lib/tesser3takt-slice-phase.ts) prüft
deklarierte Werte. Der gelesene HUD-Ablauf erzeugt dafür weder Phasensnapshots
noch ein Slice-Receipt. Die fehlende Anbindung ist nicht durch Import und Aufruf
dieses Prüfers allein geschlossen. Die ausgeführten Gegenläufe und Quellhashes
stehen im [Audit](../audit/2026-10-23_phase_source_binding_review.md).

[FAKT] Es gibt bereits einen ausführbaren synthetischen Phasengenerator im Repo.
Die Aussage, es existiere überhaupt kein Producer, wäre deshalb zu weitgehend.
Ungebunden sind seine fachliche Auswahl für das HUD und die Zuordnung seiner
Samples zu Boundary, Frame und Slice. Die Prüfung umfasst die unten benannten
Quellen und ihre gelesenen Aufrufer, keine vollständige Sichtung privater Korpora.

## 2. Kandidaten und ihre Grenzen

| Kandidat | Tatsächlich gelesene Größe | Fehlender Anschluss |
| --- | --- | --- |
| [HUD-Faserzeichnung](../../ui-app/components/tesser3takt/Tesser3TaktHudV2.tsx), `fiberPath` | Eine räumliche Kurve aus Laufparameter t, Kanalindex und torsion; der Sinusterm enthält eine zeichnerische Phase. | Kein zeitlicher Sample-Verlauf und keine exportierten Phasensnapshots. Der Kurvenparameter ist keine belegte Prozesszeit. |
| [HUD-Regime und zLayer](../../ui-app/lib/tesser3takt-hud.ts), `buildTesserHudFrame` | Regime aus control/torsion; separat übergebene Ansichts-/Tiefeneinstellung. | Geänderte Einstellungen liefern im ausgeführten Gegenlauf denselben Transport. zLayer ist dort kein gespeicherter Transformationsverlauf. |
| [Toy-Generator](../../src/tools/toy_resonance_dataset.py), `generate_mycel_signals` | Gewrappte relative Phase der internen Variablen phase_a − phase_b in Radiant, mit Seed reproduzierbar. | SIMULATION_PROXY; keine zwei einzelnen exportierten Phasen, keine sieben Lyra-Phasen und keine HUD-IDs. Die Phase ist nicht aus den gefilterten, verrauschten Ausgangssignalen gemessen. |
| [PLV und Metrikexport](../../src/core/metrics.py), [Export](../../tools/void011_metrics_export.py) | Aggregierte Kennzahlen; der aktuelle Export führt keine rohen Phasensamples oder Frame-/Slice-Zuordnung. | Ein gleicher PLV-Wert kann aus verschiedenen Phasen folgen. Er kann die fehlenden Einzelwerte nicht eindeutig ersetzen. |
| [LOG-ZN-Test](../../tests/unit/test_logzn_orbit.py) | Mathematische Gegenfälle zu Branch Cut und entwickelter Phase. | Ausführbare Substratprüfung, kein angebundener HUD-Producer. Der bestehende Slice-Vertrag erhält keine Windungszahl. |

[FAKT] Die beiden Fractalsense-Treffer für `log_zn` in der
[Canvas-Komponente](../../ui-app/components/fractalsense/FractalCanvas.tsx) und im
[Visualizer](../../Fractalsense/fractal-visualizer.js) berechnen logarithmische
Farbglättung. Sie binden nicht den LOG-ZN-Windungsoperator an den Slice-Transport.

## 3. Identitäten nicht durch Namensnähe ersetzen

| Angabe | Vorhandene Rolle | Noch zu erklären |
| --- | --- | --- |
| frameId | Der HUD-Builder setzt fest `tesser3takt-hud-v0.2`. Unterschiedliche Ansichten im Gegenlauf behalten diese Kennung. | Zwei Prozessbeobachtungen benötigen für den bestehenden Phasenvertrag verschiedene Quell-/Ziel-Frame-IDs. Eine Ansichtsversion allein stellt diese Bindung nicht her. |
| stateId | Adressiert im Boundary-Paar etwa hud:N04 und hud:N05. | Kein stilles Umbenennen zu einem Frame- oder Sample-Identifier. |
| pairId | Bindet genau ein EXIT und ENTRY mit Reihenfolge, Herkunftsidentität und legalem Lattice-Schritt. | Welche Prozessbeobachtungen gehören zu diesen beiden Hälften? |
| sliceId | Im neuen Phasenvertrag dieselbe logische Kennung in Receipt und beiden Snapshots. | Welches fortgeführte Objekt oder welcher Schnitt wird damit verfolgt? zLayer und pairId beantworten das nicht von selbst. |
| sourceFrameId der Mikro–Meso-Brücke | Bindet den Eingang einer räumlichen Zusammenfassung. | Der [Bridge-Trace](../../ui-app/lib/tesser3takt-bridge.ts) führt Ereignisreihenfolge weiter, aber keine neue zeitliche Phasenquelle. |

[ANNEX] Die feste HUD-Kennung ist als solche kein nachgewiesener Fehler des
bestehenden Ansichtsvertrags. Für den neuen zeitlichen Vertrag fehlt eine weitere
Identitätsbindung. Künstlich verschiedene Zeichenketten ohne zugehörige
Beobachtungen würden nur das Formatkriterium erfüllen.

## 4. Bedeutung und Verlust vor einer Umrechnung festlegen

[MODELL] Für eine ausgewählte relative Modellphase wäre die rechnerische
Konversion `turns = (radians / (2π)) mod 1` möglich. Der ausgeführte Toy-Lauf
bestätigt Werte im Bereich [0,1). Diese Umrechnung wählt noch keine HUD-Quelle,
keinen Nullpunkt und keine Bedeutung der Phase aus.

[ANNEX] Vor der Anbindung braucht der Vorschlag eine ausdrückliche Beschreibung:

1. Welcher Prozess und welche Größe werden verfolgt: einzelne Phase, relative
   Phase oder ein Verlauf mit zusätzlich erhaltener Windungsinformation?
2. Welche Funktion, Version und Modellparameter erzeugen die Beobachtungen?
3. Welcher Bezug und welche Orientierung gelten; welche Einheit wird übernommen?
4. Wie werden Lauf, Sample-Reihenfolge, Quell-/Ziel-Frame, Slice und Boundary-Paar
   nachvollziehbar miteinander verbunden?
5. Welche Transformation ist vorab zugelassen? Ein erst aus den beiden Endwerten
   errechneter Versatz bestätigt für sich genommen keine unabhängige Transformregel.
6. Welche Information geht verloren, und welcher Claim-Status bleibt erhalten?

[ANNEX] Ein modulo-1-Wert bewahrt die Kreisposition, aber keine Anzahl ganzer
Umdrehungen. Der [LOG-ZN-Anschluss](../tesser3takt/S4_LOGZN_bridge.md) hält diese
Unterscheidung bereits als eigene Modellfrage fest. Soll Windung mitgeführt
werden, benötigt sie einen ergänzenden Vertrag und Gegenfälle; sie darf nicht
nachträglich aus dem vorhandenen Phasenwert behauptet werden.

## 5. Prüffähiger Anschlussvorschlag

[ANNEX] Ein begrenzter technischer Replay könnte den vorhandenen Toy-Generator
als ausdrücklich ausgewählten SIMULATION_PROXY verwenden. Dann wären dessen
relative interne Phasen die gewählte Testgröße. Ein solcher Replay würde den
Transportweg prüfen; seine Übernahme als Bedeutung der tesser3TAKT-Phase bleibt
eine gesonderte Modellentscheidung.

[ANNEX] Mindestumfang des anschließenden Patches: versionierte Producer-Referenz,
stabile Lauf-/Sample-Zuordnung zu zwei tatsächlichen Snapshots, explizite
Boundary-/Slice-Bindung, dokumentierte Einheitenkonversion und ein deklarierter
Transformvertrag. Zufällige neue Frame-IDs oder nachträglich passende Versätze
sind kein Ersatz für diese Herkunft.

[ANNEX] Erforderliche Gegenfälle: falscher Sample- oder Boundary-Bezug; gleiche
Frame-Kennung für zwei verlangte Snapshots; Radiant ohne Einheitenkonversion;
PLV als Ersatz für die Einzelphase; vertauschte Reihenfolge; falscher
Transformbezug; scheinbar gleiche Endphase bei unterschiedlicher Windung.
Es wird hier noch kein Producer, Adapter oder Replay implementiert.

## 6. Gesonderte offene Größen

| Größe | Erhaltener Status |
| --- | --- |
| Graining/Kantenfärbung | UNRESOLVED: Ausleseoperator, Bezug und Transformation fehlen weiterhin. |
| Blindseite | UNRESOLVED: Die ausgeblendeten Größen und ihre Verschiebung sind gesondert zu benennen. |
| Sphärenstatus | UNRESOLVED: INTRA oder optionaler Hüllendurchbruch wird nicht aus Quadrant, zLayer oder Phase abgeleitet. |

[ANNEX] Kη-03 bleibt UNBOUND. Die Prüfung ändert weder HUD-Laufzeit noch
Kenogrammstatus oder VOIDMAP. Ihre konkrete neue Information ist die eingegrenzte
Quellenlage samt Gegenfällen und der vor einem Anbindungspatch fehlenden Setzung.
