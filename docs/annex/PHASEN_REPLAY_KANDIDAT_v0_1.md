# Begrenzter Phasen-Replay: ausgefüllter Kandidat v0.1

**Status:** ANNEX / DERIVED / SPEC-WIP · Review-Kandidat

**FOKUS:** Phasenbindung konkret zur Entscheidung vorlegen

**Anbindung:** HOLD · kein HUD-Adapter und kein Kη-03-BINDING

## Zweck und Entscheidungspunkt

[ANNEX] Anschluss an [#418](https://github.com/fleksible/entaENGELment-/issues/418):
Die vorhandene Quellenprüfung wird wiederverwendet. Dieser Entwurf füllt die
Vorlage für einen kleinen synthetischen Replay aus. Der
[vorhandene Validator](../../ui-app/lib/tesser3takt-slice-phase.ts) bleibt die
technische Prüfstelle. Der Text erzeugt keine neuen HUD-Zustände.

[MODELL] Kandidat ist die relative interne Toy-Phase a minus b als
SIMULATION_PROXY. Ihre Auswahl und die vorgeschlagene Sample-/Boundary-Zuordnung
sind als konkrete Modellentscheidung offen. Auch eine Übernahme für diesen
Test würde keine endgültige HUD-Bedeutung oder Lyra-Deutung festlegen.

## Ausgefüllter Anschlussvertrag

| Angabe | Vorschlag für den begrenzten Replay |
| --- | --- |
| Producer | `generate_mycel_signals`, `src/tools/toy_resonance_dataset.py`; Quellbindung unten. |
| Größe / Claim | `ToyDataset.phases[i]`: gewrappte interne Differenz a − b in Radiant. SIMULATION_PROXY; keine aus den verrauschten Ausgangssignalen gemessene Phase, keine sieben Lyra-Phasen. |
| Parameter | n=256, seed=42, coupling=0.35. Interne Drift-/Rauschparameter gehören zur gepinnten Producer-Version. |
| Zwei Beobachtungen | Samples 0 und 1 desselben Laufs. t=0 und t=1/255 sind normierte Samplekoordinaten, keine Sekunden. |
| Einheit / Nullpunkt | `turns=(radians/(2π)) mod 1`. Null ist Gleichphase modulo 2π; die Richtung stammt aus der gesetzten Differenz a − b. |
| Basis / Orientierung | Kandidat `basisId=toy-relative-a-minus-b-v1`, durchgehend `handedness=RIGHT` als Testkonvention. Kein Nachweis räumlicher Händigkeit oder Spinor-Dynamik. |
| Laufidentität | Deterministischer Digest aus Producer-Quellhash, Parameterobjekt und Schemafassung; keine zufällige ID als Herkunftsersatz. |
| Frames / Slice | Zwei Replay-Snapshots mit Sampleindex in ihrer Identität; gemeinsame Slice-ID des relativen Toy-Verlaufs. Bestehende HUD-frameId und stateId werden nicht umbenannt. |
| Boundary-Zuordnung | Kandidat: Sample 0 → EXIT, Sample 1 → ENTRY des Testbezugs B-Q0-Q1. Das ist eine neu vorgeschlagene synthetische Zuordnung, kein im bisherigen HUD beobachteter Producer-Pfad. Ohne bestätigte Zuordnung bleibt die Anbindung HOLD. |
| Transformation | Vorab erklärte Ein-Schritt-Regel des gepinnten Producers; Offset aus Quellphase, Parametern und passendem RNG-Schritt bestimmen. Zielphase erst zum Vergleich lesen; keinen Offset aus beiden Endwerten anpassen. |
| Evidenz | Zwei separat aus dem Producer-Verlauf gelieferte Samples, zusätzlich Receipt und Transformdefinition. Das Receipt bestätigt sich nicht selbst. |
| Erhalt | Deklarierter Lauf, Samplefolge, logischer Slice, Basis und Orientierung; Konsistenz der Kreisposition innerhalb bestehender Validator-Toleranz. |
| Verlust / offene Größen | Modulo 1 erhält keine Windungszahl. Graining-Herkunft, Blindseite und Sphärenstatus bleiben jeweils UNRESOLVED. |

## Quellbindung und ausgeführte Rechenprobe

[FAKT] Gelesener Stand: `539e87bd3e900930d029f6fdd59d444637cf6425`.
Producer-Blob: `f7bd8c58cbfae298ae727688215f6d92b5913e77`.
SHA-256 der Producer-Datei:
`002d3857301225e8075fe2999f1a28d27ba67e5d781fb9ba174386ef8df5dc28`.
Der Hash bindet Codebytes, weder Modellbedeutung noch reale Kopplung.

[MODELL] Mit relativer Quellphase φ, Kopplung c und den beiden nächsten
Phasenrauschwerten ηa/ηb lautet die Ein-Schritt-Vorhersage:

```text
d = -0.02 + ηa - ηb
deltaRadians = d - c * 0.02 * sin(φ + d)
deltaTurns = deltaRadians / (2π)
predictedTarget = (sourceTurns + deltaTurns) mod 1
```

[FAKT] Pro Sample verbraucht diese Fassung fünf RNG-Werte: zwei für Phase,
zwei für Ausgangsrauschen und einen für den Consent-Proxy. Die Vorhersage
benutzt Quellwert und Laufparameter; der Zielwert bestimmt den Offset nicht.
Geänderte Reihenfolge oder Parameter benötigen eine neue Quellprüfung.

| Seed | Quellphase / Umläufe | Zielphase / Umläufe | vorhergesagter Offset / Umläufe |
| --- | ---: | ---: | ---: |
| 7 | 0.9973859514942129 | 0.9952159793239636 | -0.002169972170249363 |
| 42 | 0.9987812395239011 | 0.9949478544744789 | -0.003833385049422233 |
| 123 | 0.996729111799163 | 0.9920169270668622 | -0.004712184732300852 |

[FAKT] Drei direkte Vergleiche unter Python 3.12.14 bestehen; größter
Kreisabstand etwa 1.11e-16 Umläufe. Drei Gegenproben mit falschem Transform-Seed
werden bei Toleranz 1e-10 zurückgewiesen. Das ist eine ausgeführte Rechenprobe,
kein implementierter Adapter, kein neuer CI-Test und keine unabhängige
Modellherleitung. Producer und Vorhersage teilen ihre Modellannahmen.

## Späterer Patch und offene Setzung

[ANNEX] Nach der konkreten Auswahl kann ein opt-in Export die beiden Samples
mit Producer-/Lauf-/Sample-Herkunft und der erklärten Boundary-/Slice-Bindung
an die bestehende API reichen. Der erste Scope bleibt dieser Replay.

[ANNEX] Zusätzliche Adapter-Gegenfälle: falscher Sample-/Boundary-Bezug,
vertauschte Reihenfolge, falsche Einheit/Basis, andere Slice-ID, nachträglich
angepasster Offset, PLV als Einzelphase und verdeckter Windungsverlust.
Diese Adapterfälle sind NOT_RUN; die drei falschen Seed-Proben ersetzen sie nicht.

[UNRESOLVED] Welche Größe die HUD-Phase bezeichnen soll und ob die oben
vorgeschlagene synthetische Zuordnung gewählt wird, bleibt eine inhaltliche
Festlegung. Eine andere Größe oder Zuordnung ist ein gültiger Ausgang.
