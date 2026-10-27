# Phasen-Replay: vorbereitete Review-Fragen

**Status:** ANNEX · DERIVED · Entscheidungsvorbereitung

**FOKUS:** offene Phasenentscheidung konkret lesbar halten

**Anbindung:** HOLD · **Promotion-Effect:** none

## Vorliegender Kandidat

[FAKT] Der öffentliche
[Kandidat aus #423](https://github.com/fleksible/entaENGELment-/blob/af2d092dcff2136d675c10d80c6991d1a3bff714/docs/annex/PHASEN_REPLAY_KANDIDAT_v0_1.md)
schlägt einen SIMULATION_PROXY vor: relative interne Toy-Phase a minus b,
n=256, seed=42, coupling=0.35, Sample 0 als EXIT und Sample 1 als ENTRY eines
synthetischen Testbezugs. RIGHT ist dort eine Testkonvention. Der Text
berichtet drei direkte Rechenproben und drei falsche Seed-Proben; die
zusätzlichen Adapterfälle sind ausdrücklich NOT_RUN.

[ANNEX] Das ist ein prüfbarer Vorschlag, kein aus ursprünglicher Navigation
abgeleiteter Bedeutungszwang. Der aktuelle
[Quellenvertrag](PHASENQUELLE_UND_ZUORDNUNG_v0_1.md) bleibt die Basis.
Dieser Fragenbogen wählt weder eine HUD-Quelle noch eine Boundary-Zuordnung.

## Inhaltliche Entscheidungen am konkreten Fall

| Punkt | Offen zu beschreiben | Was die vorhandene Rechnung schon begrenzt |
| --- | --- | --- |
| Prozess und Größe | Welche Veränderung soll Phase in der betrachteten Szene bezeichnen? | a−b ist die interne Differenz eines Toy-Producers; keine gemessene Phase der verrauschten Ausgänge |
| Übergangsbezug | Welche Beobachtungen gehören zu EXIT, ENTRY und demselben fortgeführten Slice? | Sample 0/1 ist eine vorgeschlagene synthetische Zuordnung, kein beobachteter HUD-Pfad |
| Erhalt und Verlust | Welche Relation muss bei der Rückkehr erkennbar bleiben? Welche Rolle spielt die Windungsinformation? | Modulo 1 erhält die Kreisposition, keine Zahl ganzer Umläufe |
| Basis und Orientierung | Was benennen Nullpunkt, Richtung und Basis im gewählten Fall? | RIGHT ist ein deklariertes Label, kein Nachweis räumlicher Händigkeit |
| Rücknahme | Woran würde die ausgewählte Zuordnung scheitern oder unbrauchbar werden? | Eine intern konsistente Rechenprobe ist noch kein unabhängiger Mechanismusbeleg |

[ANNEX] Antworten dürfen den Kandidaten präzisieren, verändern oder weiter offen
lassen. Eine Zustimmung zu technischen Vorarbeiten setzt keine dieser
Bedeutungen automatisch fest. Eine spätere Entscheidung soll den ausgewählten
Fall, erhaltene Aspekte, Verlust und Geltungsbereich benennen.

## Danach vorbereitbare Adapterprüfung

[ANNEX] Nach der inhaltlichen Auswahl ist der kleinste technische Schritt ein
opt-in Export mit Producer-, Lauf-, Sample-, Frame-, Slice- und Boundary-Herkunft.
Vor einem Lauf sind Einheit/Basis und die zulässige Transformation erklärt.
Der Zielwert darf den Offset nicht nachträglich bestimmen.

[ANNEX] Geplante Gegenfälle: vertauschte Beobachtungen, falscher Boundary-Bezug,
andere Slice-ID, falsche Einheit/Basis, nachträglich angepasster Offset,
PLV als Einzelphase und verdeckter Windungsverlust. Die Such-CLI führt diese
Adapterfälle nicht aus und setzt sie nicht auf bestanden.

[UNRESOLVED] Graining-Herkunft, Blindseite und Sphärenstatus bleiben jeweils offen;
Kη-03 bleibt UNBOUND. Ein späterer bestandener Replay würde diese Grenzen
nicht allein durch sein Bestehen schließen.

