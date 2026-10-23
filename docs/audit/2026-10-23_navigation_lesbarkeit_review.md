# Navigation und Lesbarkeit — Fortsetzung vom 2026-10-23

**Status:** ANNEX · DERIVED · Audit der Veröffentlichungsvorbereitung

**FOKUS:** getrennte Vorhaben konkretisieren

**Basis:** `main@b8fc884fb9957931f5107a54417b35b97660ec84`

**Arbeitsbranch:** `codex/navigation-lesbarkeit-2026-10-23`

**Prüfzeitpunkt:** vor Erstveröffentlichung dieses Pakets; PR-/Merge-Stand folgt aus der Git-Historie

## 1. Autorisierung und Umfang

[FAKT] Der Nutzer beauftragt die Fortsetzung des ursprünglichen Arbeitsplans unter
Einbeziehung der inzwischen ausgearbeiteten Nuancen. Der bereits gemergte
[Bestandsaudit](2026-10-22_tesser3takt_revision_audit.md) bleibt der getrennte
Beleg der früheren Dokumentkorrekturen. Diese Fortsetzung bereitet neue Vorschläge
vor und erklärt die früheren offenen Herkunftsfragen nicht pauschal für geschlossen.

[ANNEX] Der ursprüngliche Umfang sind vier Dokumententwürfe: gedankliche Navigation,
Architektur der Lesbarkeit, registergetreue Claim-Prüfung und ein lesender
PerspectiveTransitionWitness. Laufzeitcode, installierte Skills, exportierte
Skill-Snapshots, GOLD-Bereiche und bestehende Receipts werden nicht verändert.
Eine neue Pipeline- oder VOID-Liste wird nicht angelegt.

[ANNEX] Auf ausdrücklichen Folgeauftrag wird ein fünfter Annex-Entwurf ergänzt:
Prüfanforderungen zu Adaptivität, Pearson-Blanket, HC/AC, Gemini-Stream-Abbruch und
Qwen-Berechtigungen. Der Umfang umfasst Anforderungen und Harness-Design,
keine Implementierung oder Ausführung dieser Experimente. Die Bestandsmatrix
bleibt unverändert.

## 2. Herkunft und Reduktionsumfang

[ANNEX] Die methodischen Nuancen stammen aus autorisierter privater Arbeitslektüre.
Die öffentliche Prüfbarkeit betrifft ausschließlich die benannten öffentlichen
Repo-Anker und Fachquellen. Eine vollständige öffentlich rekonstruierbare Genealogie
der privaten Begriffsarbeit wird nicht behauptet.

[FAKT] Das vorbereitete Paket enthält keine privaten Quelldateinamen, Zugangs-IDs,
biografisch verknüpften Forumskennungen oder privaten Gesprächszitate. Beispiele
werden als synthetisch ausgewiesen. Ihre Reduktion ist nicht verlustfrei: Die
persönliche Herkunft wird damit gerade nicht vollständig rekonstruierbar.

[ANNEX] Die Prüfung der vorliegenden Reduktion ist paketbezogen; ältere
Exportprüfungen werden nicht geerbt. Die lokale Vorbereitung enthält keine
Veröffentlichungs- oder Kanonisierungsentscheidung. Private Originalpassagen und
offene narrative Ausarbeitungen bleiben außerhalb dieses Repo-Pakets.

## 3. Konkrete Entwürfe

| Dokument | Neues, begrenztes Delta |
| --- | --- |
| [Gedankliche Navigation](../annex/GEDANKLICHE_NAVIGATION_v0_1.md) | Ausgangsform, gedankliche Bewegung und Fachlesart erhalten; direkte Lektüre, Wiedererkennen, erinnerte Absicht und heutige Haltung unterscheiden. |
| [Architektur der Lesbarkeit](../annex/ARCHITEKTUR_DER_LESBARKEIT_v0_1.md) | Schwelle, Projektion und benannte Invariante; Erinnerung und wohlwollende Durchlässigkeit als eigene begriffliche bzw. ethische Fragen. |
| [Registergetreue Claim-Prüfung](../annex/REGISTERGETREUE_CLAIM_PRUEFUNG_v0_1.md) | Sechs synthetische Gegenfälle; Originalaussage und zusätzlich eingeführten Prüfsatz trennen. |
| [PerspectiveTransitionWitness](../annex/PERSPECTIVE_TRANSITION_WITNESS_v0_1.md) | Genau ein Boundary-Paar an fünf Übergabegrößen prüfen; positiver Paarlauf und offene semantische Größen getrennt dokumentieren. |
| [Adaptivität: Prüfanforderungen](../annex/ADAPTIVITAET_PRUEFANFORDERUNGEN_v0_1.md) | Vier getrennte Prüfbereiche mit Quellen, Kontrollfällen und Verwerfungskriterien; alle Experimente NOT_RUN, ursprüngliche HC/AC-Bezeichnung HOLD. |

## 4. Technischer Gegenfall

[FAKT] Am gepinnten Ref trägt `B-Q0-Q1` genau ein EXIT und ein ENTRY. Der
ausgeführte vorhandene Validator liefert `valid: true`, `errors: []`.
Die Paardaten enthalten keinen Slice-Phasenübergang; die HUD-Spezifikation und
`Kη-03` führen diese Bindung weiter als offen. Der Provenienzpointer des Paars
selbst führt `revision: unverified`, `digest: null`, `digestStatus: UNVERIFIED`.

[ANNEX] Der Lauf belegt damit einen gültigen Boundary-Übergang im bestehenden
Vertrag. Er ist kein Nachweis vollständiger Graining-, Phasen-, Blindseiten- oder
Sphärenübergabe. Das Dokument ergänzt keine fehlenden Werte und ändert keinen
Kenogramm-Status.

## 5. Validierung

[FAKT] Die Vorprüfung der unveränderten Basis besteht mit CPython 3.12.14 und dem
gepinnten `uv 0.12.18`: 709 Python-Tests und 165 Subtests, Port-Lint, strikte
Core-Pointer-Prüfung und Claim-Lint. Vier optionale generierte `out/`-Pfade fehlen
bereits an der Basis; kein Core-Pointer fehlt.

[FAKT] Die Standardumgebung konnte zunächst kein `pytest` ausführen; die
vorhandene alte Umgebung war nicht verwendbar. Ein weiterer Start mit dem
runtime-eigenen `uv 0.12.23` wurde von der Versionsbindung abgewiesen. Die erfolgreiche
Vorprüfung nutzt deshalb `uv 0.12.18` und eine separate lokale Prüfumgebung.
Die Projekt-Konfiguration und Lockdateien wurden dafür nicht geändert.

[FAKT] Die Nachprüfung des ursprünglichen Dokumentpakets vor der
Adaptivitäts-Ergänzung besteht:

| Prüfung | Ergebnis und Reichweite |
| --- | --- |
| `make verify` | PASS: 709 Python-Tests und 165 Subtests, Port-Lint, strikte Core-Pointer-Prüfung, Claim-Lint; dieselben vier optionalen `out/`-Pfade fehlen wie an der Basis. |
| `make verify-governance` | PASS: 15 Workflows erfüllen das Posture-Gate; VOID-Backlog aktuell; 22 VOID-Einträge im UI-Spiegel synchron. |
| `git diff --check` | PASS nach Korrektur der Markdown-Zeilenenden. |
| Lokale Linkprüfung | PASS: 21 relative Links und zwei Zielanker lösen im gelesenen Dokumentpaket auf. |
| Diff- und Reduktionsprüfung | Genau fünf zusätzliche Dokumentdateien; keine Laufzeit-, Lock-, GOLD- oder Receipt-Änderung; keine der konkret ausgeschlossenen privaten Quellenkennungen im Paket. |
| Enger Boundary-Lauf | PASS für `B-Q0-Q1`; das sichtbare Node-Modulformat-Warning bleibt bestehen. |

[FAKT] Der bestehende Claim-Lint prüft `index, spec, receipts, tools`, nicht die
neuen Annex-Texte. Deren Claim-Reichweite wurde redaktionell geprüft; die Link- und
Reduktionsprüfung ist ein begrenzter lokaler Dokumentcheck. Für diesen reinen
Dokumentdiff wurde kein vollständiger UI-Build ausgeführt.

[ANNEX] Weder synthetische Beispiele noch technische Gates validieren eine
allgemeine Wirksamkeit der Methode oder ein physikalisches Gesamtmodell. Der
lokale Prüfstand ist kein vorweggenommenes CI-Ergebnis einer veröffentlichten PR.

## 6. Ergänzung: Adaptivitätsanforderungen

[FAKT] Der Folgeauftrag ergänzt vier Prüfbereiche in einem fünften Annex-Entwurf.
Das Paket umfasst damit sechs zusätzliche Dokumentdateien einschließlich dieses
Audits. Der Quellabgleich liest zwei datierte Preprints, den öffentlichen
Gemini-Fehlerbericht und offizielle Release-/Konfigurationsseiten. Frühere
Radar-Zusammenfassungen gelten nicht als unabhängige Bestätigung dieser Quellen.

[ANNEX] Adaptivität wird als angemessene Verhaltensänderung bei bindenden Grenzen
geprüft; Robustheit und Berechtigungstreue bleiben getrennte Prüfsätze. Die
Anforderungen umfassen vorab bestimmte Kontrollfälle, einen ausschließlich
synthetischen Effekt-Ledger und Verwerfung beim ersten Inhalts- oder Metadatenleck.
Direktlesung mit bekanntem Pfad und Suche nach unbekannten Metadaten verwenden
getrennte Fixtures, damit Eingabewissen nicht als Leck fehlgezählt wird.

[UNRESOLVED] Die ursprüngliche Definition von HC/AC bleibt HOLD. Die H/A/F-Matrix
ist als eigener Operationalisierungsvorschlag ausgewiesen. Ein Fehlerbericht zu
Gemini CLI 0.64.0 wird nicht als reproduzierter Befund zu 0.65.0 ausgegeben;
aktuelle Qwen-Dokumentation nicht als gemessene Garantie eines Pre-Releases.

[FAKT] Die erneute lokale Nachprüfung besteht: `make verify` mit 709 Tests und
165 Subtests; `make verify-governance` mit 15 Workflows und 22 synchronen VOIDs;
`git diff --check`; 25 relative Links und zwei Zielanker. Die vier optionalen
generierten Pfade fehlen weiterhin wie an der Basis. Der erste Verify-Start
scheiterte vor pytest, weil der Interpreter-Einstieg der separaten Prüfumgebung
fehlte. Dieser lokale Einstieg wurde wiederhergestellt; der vollständige neue
Verify-Lauf besteht. Repo-Toolchain und Lockdateien wurden nicht verändert.

[ANNEX] Diese Ergebnisse prüfen die bestehende Repo-Membran und die redaktionelle
Einbindung. Sie führen keinen der neuen Modell-, Zusammenarbeits-, Gemini- oder
Qwen-Tests aus. Alle vier Experimente stehen weiterhin auf NOT_RUN. Es wurden
weder ein Qwen-Testprofil noch Produktadapter eingerichtet. Kein Push oder Merge
dieser Ergänzung und keine Kanonpromotion sind erfolgt.

## 7. Abgleich mit der ursprünglichen Reihenfolge

[ANNEX] Auf den erneuten Abgleich wird §7 des Adaptivitätsentwurfs präzisiert:
Dokumentreview mit öffentlichem Umfang, kleiner PR und Merge nach grünen
erforderlichen Prüfungen; danach konkreter Methodenfall samt Gegenfall;
anschließend Phasenübergabe vor Code-Patch und gesonderte Behandlung von Graining,
Blindseite und Sphärenstatus; danach reproduzierbares optisches Modellbeispiel.
Grimm 2.0 bleibt eigenständig, die Szene offen. Die neuen Anforderungen werden
jetzt dokumentiert; ihre vollständige experimentelle Ausführung wird nicht zur
Voraussetzung des Dokument-Merges gemacht. Adapterprüfungen binden die tatsächliche
Nutzung des betreffenden Adapters. Der Publikations- und Ausführungsstand bleibt
unverändert. Dieser Nachtrag ändert ausschließlich Dokumenttext.

## 8. Freigabe der quellenreduzierten Reviewfassung

[FAKT] Der Nutzer beauftragt nach Abgleich der vier Schritte deren Durchführung,
einschließlich öffentlichem PR und Merge nach grünen erforderlichen Prüfungen.
Die Freigabe umfasst das reduzierte ANNEX-Paket. Private Herkunftsbelege und
persönliche Entstehungsgeschichte sind nicht Bestandteil dieser Veröffentlichung.

[ANNEX] Die fünf Entwürfe werden als SPEC-WIP zur öffentlichen Prüfung eingebracht.
HOLD, NOT_RUN und fehlende Laufzeitdurchsetzung bleiben sichtbar. Die Einordnung
ist keine fachliche Validierung oder Kanonpromotion. Der öffentliche Umfang
umfasst genau diese fünf Annex-Dateien und dieses Audit; keine privaten
Quelldateinamen, Zugangs-IDs oder biografisch verknüpften Kennungen werden ergänzt.
