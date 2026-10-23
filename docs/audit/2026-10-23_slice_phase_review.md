# Methodenfall und erster Slice-Phasenvertrag — 2026-10-23

**Status:** ANNEX · DERIVED · Reviewfassung

**FOKUS:** deklarierte Phasenübergabe prüfen

**Basis:** `fc35b35a63091383249bc3448d3ae3119f1f5570`

## 1. Auftrag und Vorgänger

[FAKT] Der Nutzer beauftragt die Durchführung der abgestimmten vier Schritte.
Das reduzierte Dokumentpaket wurde mit [PR #412](https://github.com/fleksible/entaENGELment-/pull/412)
nach erfolgreichen PR-Workflows und abgeschlossenem automatischem Review ohne
Befunde gemergt. Der Merge-Commit ist die oben benannte Basis dieses Folgepakets.
Die persönliche Entstehungsgeschichte gehört weiterhin nicht zum öffentlichen Diff.

## 2. Konkreter Methodenfall

[FAKT] Der [Methodenfall](../annex/METHODENFALL_BOUNDARY_PAIR_v0_1.md) wurde an
`B-Q0-Q1` ausgeführt: zwei Records, gültiges Paar, keine Phasenfelder. Eine
synthetisch falsche Herkunftsidentität wird zurückgewiesen. Quellfassung,
Dateihashes, zusätzlicher Prüfsatz und Wiederholungsbefehl sind dokumentiert.

[ANNEX] Erhalten bleibt die enge Ausgangsaussage. Die weiter gehende Verbindung
zwischen Paar-PASS und vollständiger Slice-Phase scheitert. Dieser Gegenfall ist
keine Widerlegung des engeren Paarvertrags und kein unabhängiger Methodentest.
Eine autobiografische Szene wurde dafür nicht ausgewählt.

## 3. Vertrag vor Code

[ANNEX] Der neue [Slice-Vertrag](../annex/SLICE_PHASE_TRANSPORT_v0_1.md) benennt
zuerst Einheiten, Bezugssystem, Orientierung, Transformation, separat übergebene
Eingabesnapshots und Gegenfälle. Anschließend wird ein separater Runtime-Validator
implementiert. Der vorhandene Provenienzvalidator wird dafür mit unveränderter
Logik exportiert; eine zweite Provenienzdefinition wird nicht eingeführt.

[ANNEX] Das lokale Modell beschränkt sich auf eine einzelne Phase in Umläufen
modulo 1 und einen begrenzten additiven Versatz. Eine Basis- oder Orientierungsänderung
wird zurückgewiesen. Phasenwerte und zeitliche Verläufe werden dem HUD nicht
hinzuerfunden. Der Aufrufer bleibt für die Herkunft der Snapshots und die zugelassene
Transformdefinition verantwortlich. Strukturprüfung ist keine kryptografische
Prüfung oder Bestätigung der Quellunabhängigkeit.

[UNRESOLVED] Der tatsächliche Phasenproducer und die Boundary-/Frame-/Slice-Zuordnung
fehlen weiter. Graining, Blindseite und Sphärenstatus werden im Vertrag jeweils
ausdrücklich als offene eigene Größen geführt. `Kη-03` bleibt `UNBOUND`.
Dieser Patch schließt weder einen VOID noch den gesamten Transportvertrag.

## 4. Prüfung und Reichweite

[FAKT] Die gezielte neue Suite und die vollständigen lokalen Gates bestehen:

| Prüfung | Ergebnis |
| --- | --- |
| Neue Slice-Phasenfälle | 35 Node-Tests; unter anderem Vorher-/Nachher-Abgleich, Frame-/Slice-/Basis-/Transformkonflikte, Umlauf und numerische Toleranz, fehlende Daten, Provenienz und Negativfall des gültigen Boundary-Paars. |
| `make verify` | 709 Tests und 165 Subtests; Port-Lint, Core-Pointer und Claim-Lint PASS. Dieselben vier optionalen generierten Pfade fehlen wie an der Basis. |
| `make verify-governance` | 15 Workflows und 22 VOID-Einträge konsistent. |
| `make verify-js` | Typprüfung, Lint, Produktionsbuild und Tests mit eingefrorener Lockdatei PASS; 58 Node-Tests sowie sechs Canvas-Tests. |
| Dokument- und Diffprüfung | Relative Links und Anker, Quellen-/Publikationsumfang und `git diff --check` geprüft; nur die sechs genannten Dateien betroffen. |

[FAKT] Die lokale JS-Prüfung verwendet die projektgebundene pnpm-Version 10.33.0
und Node 24.19.0; die CI prüft die JS-Membran mit Node 22. Bestehende
MODULE_TYPELESS_PACKAGE_JSON-Warnungen und Hinweise auf nicht ausgeführte
optionale Installationsskripte bleiben sichtbar. Lockdatei und Paketkonfiguration
werden nicht geändert. Turbo kann unveränderte Teilprüfungen aus dem lokalen
Cache wiederverwenden; der neue Testinhalt wird ausgeführt.

[FAKT] Ein erster UI-Prüflauf wurde von der automatischen Freigabeprüfung wegen
möglicher Telemetrieübertragung an Vercel abgewiesen. Er wird nicht als vollständiger
Prüfbeleg verwendet. Der erfolgreiche neue Lauf deaktiviert die Telemetrie über
`NEXT_TELEMETRY_DISABLED=1`, `TURBO_TELEMETRY_DISABLED=1` und `DO_NOT_TRACK=1`.
Eine globale Konfiguration wird dafür nicht geändert.

[FAKT] Die verwendeten Opt-out-Variablen sind in den offiziellen
[Next.js-Hinweisen](https://nextjs.org/telemetry) und der
[Turbo-Dokumentation](https://v2-8-9.turborepo.dev/docs/telemetry) beschrieben.

[ANNEX] Die Gates prüfen den begrenzten Codevertrag und Regressionen. Sie
belegen keine tatsächliche Phase des HUD, keine physikalische Übertragungsleistung
und keine allgemeine Wirksamkeit der Interpretationsmethode. Der Claim-Lint
deckt die neuen Annex-Texte nicht ab; deren Reichweite wurde redaktionell geprüft.

## 5. Optisches Beispiel und weiterer Anschluss

[UNRESOLVED] Für den vierten Schritt liegt ein reduzierter Material-/Umwelt-Fallplan
vor, der einen früheren optischen Modelllauf berichtet, aber weder sein Skript
noch Parameter und Laufbeleg enthält. Die gezielte Suche hat keine ausreichend
gebundene Codequelle geliefert. Das ist keine Behauptung, dass sie andernorts
nicht existiert. Der frühere Lauf wird hier nicht als reproduziert ausgegeben.

[ANNEX] Der Status bleibt HOLD bis zum ursprünglichen Skript oder einer konkreten
Fundstelle mit Modellannahmen und Parametern. Ein neu erfundenes optisches Modell
wird nicht als Wiederholung dieses Laufs eingesetzt. Nach Bindung der Quelle
folgen sauberer Lauf, benannte Annahmen und ein Gegenfall. Private Quellenbezüge
werden auch dann gesondert auf den öffentlichen Umfang geprüft.

[ANNEX] Grimm 2.0 bleibt unabhängig; eine Szene wird nicht vorgegeben. Die
Pearson-/HC/AC-, Gemini- und Qwen-Experimente aus dem vorherigen Paket sind durch
diesen Phasenpatch nicht ausgeführt. Insbesondere ist kein Qwen-Profil eingerichtet.

## 6. Review-Gegenfall: falsche Slice-Kennung

[FAKT] Das automatische Review von PR #413 fand an `e84231a464` eine fehlende
Bindung: Gleiche Frames, Phasen und Transformation konnten ein Receipt mit
abweichender Slice-Kennung bestehen lassen. Der Gegenfall wurde vor der Korrektur
mit `valid: true` reproduziert. Das war ein Fehler des neuen Validators.

[FAKT] Die korrigierte Fassung fordert sliceId in beiden Snapshots und gleicht
beide mit dem Receipt ab. Derselbe Gegenfall liefert danach `valid: false`.
Drei zusätzliche Regressionen prüfen umetikettiertes Receipt sowie eine jeweils
abweichende Quell- und Zielslice-Kennung. Die ursprüngliche unzureichende Fassung
bleibt in der PR-Historie nachvollziehbar; ihr PASS wird nicht als erfolgreicher
Identitätsnachweis übernommen.
