# Methodenfall: Treffer, Herkunft und Vertrag

**Status:** ANNEX · DERIVED · Review-Kandidat

**FOKUS:** Suchnuancen ohne Geltungsverschiebung prüfen

**Promotion-Effect:** none

## Gelesene Basis

[FAKT] Grundlage ist main@83caf03d6e8039637f147f1313238ca5cab611f6.
Die öffentliche [Suchkarte](corpus_search_aliases_v0_1.json) bindet jede Familie
an Quellpfade dieses Stands. Die beobachteten Zahlen unten sind Dateitreffer
im unterstützten Repo-Text, keine Zählung unabhängiger Bestätigungen.

## Fall 1: Schreibvariante erhält eine Suchspur

[FAKT] Grüneisen findet wörtlich drei Dateien. Die ausdrücklich ergänzte
Schreibvariante Grueneisen erschließt fünf Dateien im benannten Stand.
Die [Source Decoration Map](../tesser3takt/SOURCE_DECORATION_MAP_v0_1.md)
verwendet Grueneisen als begrenzte Sensitivitätsrolle; der
[VOID-Backlog](../voids_backlog.md) benennt die Grüneisen-like EFS/MVI-Achse.

[MODELL] Die Erweiterung erhält Herkunft und Originalschreibweise, während
die Query mehr Bezeichnungen erfasst. Casefold ignoriert Groß-/Kleinschreibung
im Index. Die Nachlese am Original bleibt möglich; damit ist keine gleiche
Bedeutung aller Treffer bewiesen.

[ANNEX] Positiver Kontrollfall: zwei dokumentierte Schreibweisen führen zu ihren
jeweiligen erhaltenen Texten. Gegenfall: Aus einem gemeinsamen Suchcluster wird
eine Identität des physikalischen Parameters und des Repo-Proxys behauptet.
Diese zusätzliche Behauptung trägt der Suchlauf nicht.

[UNRESOLVED] Die genaue erste Übernahmefolge eines Bildes in diese Dateien
benötigt eigene Originalquellen. Ein gegenwärtiger Treffer datiert sie nicht.

## Fall 2: Vorhandene Gruppierung trägt keinen zusätzlichen Mechanismus

[FAKT] Das [Lyra-Komplement §3](../tesser3takt/LYRA_STRINGS_COMPLEMENT_v0_1.md)
erhält sieben Rollen in der Gruppierung 3|1|3. Die
[HUD-Spezifikation §9](../spec/tesser3takt_hud_v0_2.md) fordert sieben
unabhängige Kanäle und einen sichtbaren Adapter für konkrete Abbildungen.

[MODELL] Eine wörtliche Notationssuche erhält die Gruppierung als Textspur.
Ein synthetischer Symboltest prüft separat, dass der Tokenmodus
Bedeutungszeichen nicht unbemerkt zu Zahlen zerlegt.

[ANNEX] Positiver Kontrollfall: Die mittlere Rolle bleibt beim Zählen erhalten.
Gegenfall: Sie wird ausgelassen, während der Prüfer weiterhin sieben Rollen
behauptet. Eine technische Kanalzuordnung oder ein akustischer Transfer muss
gesondert belegt werden; eine korrekt erhaltene Textnotation reicht dafür nicht.

[UNRESOLVED] Eine räumliche Referenzrolle allein legt weder Phasengröße noch
Frequenzen oder eine binaurale Abbildung fest. Sie ist kein Grund,
die fehlende Signaldefinition rückwirkend als vorhandene Absicht auszugeben.

## Fall 3: Anbindung bleibt trotz Worttreffer offen

[FAKT] [Phasenquelle und Zuordnung](PHASENQUELLE_UND_ZUORDNUNG_v0_1.md)
unterscheidet einen vorhandenen synthetischen Producer von seiner ausgewählten
HUD-Rolle. Der [Slice-Vertrag](SLICE_PHASE_TRANSPORT_v0_1.md) hält Graining,
Blindseite und Sphärenstatus jeweils UNRESOLVED und Kη-03 UNBOUND.

[ANNEX] Positiver Kontrollfall: Ein Suchtreffer führt zum Vertrag und seinem
Status. Gegenfall: Ein allgemeiner Provenienzpointer wird als mitgeführte
Graining-Herkunft oder als bestätigte Phasenbindung ausgegeben.

[UNRESOLVED] Welche Prozessbeobachtungen EXIT und ENTRY bezeichnen und welche
Größe dabei erhalten oder transformiert wird, ist eine Modellentscheidung.
Suchhäufigkeit, gleiche Kennungen oder ein bestandener Strukturtest ersetzen
diese Entscheidung nicht.

## Vergleichsreceipt

| Übergang | Erhalten | Hinzugefügt oder begrenzt | Offener Rückweg |
| --- | --- | --- | --- |
| Originaltext → normalisierte Suche | Originaldatei, Ref, Repräsentation und Hash | Groß-/Kleinschreibung im Suchkanal ignoriert; Casefold/NFC erklärt | Originalstelle im richtigen Register nachlesen |
| Schreibvariante → zusätzliche Treffer | Getrennte Texte und Statusdeklarationen | Suchrelation, keine Sachidentität | Beziehung am einzelnen Treffer prüfen |
| Nachbarbegriff → Vergleich | Ausgangsquery und markierte Erweiterung | related_not_equivalent | Quellen-/Bedeutungsübergang bleibt prüfbar und zurücknehmbar |
| Treffer → Modellentscheidung | Vorhandener Vertrag und seine Grenzen | Keine automatische Promotion | Ausdrücklicher menschlicher Bedeutungsentscheid |

[ANNEX] Der Methodenfall prüft begrenzte Darstellungen und erhält Gegenfälle.
Er ist keine allgemeine Wirksamkeitsstudie der Navigationslinse und kein
nachträglicher Wahrheitsbeleg aus Korpuswiederholung.

