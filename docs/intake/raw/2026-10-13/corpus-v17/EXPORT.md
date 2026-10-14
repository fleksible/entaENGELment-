# Herkunft und Exportgrenzen

**DERIVED / REVIEW-PENDING · Transfer-Receipt, keine Claim-Promotion**

## Getrennte Quellenanker

| Anker | Rolle | SHA-256 |
|---|---|---|
| v17, 1.333.992 Bytes | eingefrorener Eingang vor dem Writeback | `77e4fab4358240a7674943014f9301f1faade50ed0e6072ec10a37d8c6db45e0` |
| v18, 1.379.469 Bytes | bestätigtes materialisiertes Artefakt nach dem Writeback | `66de61ff3fd63fbb478d8feca991ff81d7e36a042228d79da489c7ef3239c01a` |

Die Hashes beziehen sich auf zwei unterschiedliche Originaldateifassungen.
Kein JSON-/CSV-/Markdown-Export behauptet, selbst diese Bytes zu sein.
Das Manifest hasht die tatsächlich ausgelieferten Exportdateien.
Der v17-Hash wurde beim vorherigen Einlesen festgehalten; ein erneuter historischer
Download war im Folgelauf nicht verfügbar. Der erhaltene geparste v17-Inhalt
trägt den separaten Dateihash `66523d1c0fb341af8a8b90f7307a35a89ea19f04b1d3b6dc13234a575d47053c`.
Die v18-Bytes wurden erneut materialisiert und direkt geprüft.
Ein Hash bestätigt Bytegleichheit, nicht semantische Treue oder wissenschaftliche Gültigkeit.

Welcher dieser Anker in einem Lauf tatsächlich geprüft wurde, ist am Prüfumfang
ablesbar: `verify_counts.py --export-only` prüft ihn nicht und meldet
`PASS_EXPORT_ONLY`, `--input-v18 PATH` prüft Originalbytes und Indexinhalt und
meldet `PASS_WITH_V18_INPUT`. Die v17-Originalbytes sind in keinem der beiden
Umfänge prüfbar; sie bleiben UNOBSERVED und stützen sich auf den festgehaltenen
Hash des vorherigen Einlesens.

## Transformation

1. v10-`corpus-snapshot.json` am Repo-Commit `a7773db68d97dbd8271b0921d011934d2e921170` lesen und dessen Hash prüfen.
2. Den erhaltenen geparsten v17-Inhalt und den einen JSON-Block der v18-Datei lesen.
3. Rekursiv dieselben internen Schlüssel wie beim v10-Export entfernen:
   `file_id`, `input_file_id`, `run_id`, `recorded_before_run`, `writeback`,
   `cursor`, `cursor_used`, `next_cursor`, `page_2_cursor_used`.
   Zusätzlich werden zwei interne `file_`-Verweise im Freitextfeld `reference_contact`
   durch `[interne Datei-ID ausgelassen]` ersetzt. Der Bezug auf Indexversion 15
   bleibt erhalten. Dies ist eine ausdrücklich ausgewiesene Ergänzung zum v10-Filter.
4. `document_id` als `doc-` plus erste zwölf SHA-256-Hexzeichen der UTF-8-`source_id`
   berechnen. Quell-IDs bleiben Herkunftsanker, keine Zugangsberechtigung.
5. Je Übergang vollständige neue Einträge und geänderte alte Einträge übertragen.
   Jeder ersetzte Eintrag trägt den SHA-256 seines vorherigen kanonischen JSON-Werts
   (UTF-8, Schlüssel sortiert, keine Zwischenraum-Separatoren).
   Relationen und Konflikte werden ausschließlich angehängt; historische Präfixe bleiben erhalten.
6. Vorgemerkte Quellen nach exakter `source_id` sammeln, bereits indexierte Quellen
   ausschließen, letzte Metadatenbeobachtung je ID verwenden, nach ID sortieren.
7. Zwei Stände rekonstruieren; aus den Einträgen die folgenden Tabellen berechnen.
   Die CSV enthält 96 Zeilen des v18-Inventars plus v17-Lesestand und v17-Punktzahl.
   Fehlende Felder: `NOT_RECORDED`; unbekannte Versionen: `UNKNOWN`; explizites null: `null`.
   Verschachtelte Werte: JSON; CSV-Formeleinleitungen: vorangestelltes Apostroph.
8. Die privaten Originaldateien und den vollständigen Index nicht übernehmen.
   Alle neuen Paketdateien außer dem Manifest selbst hashen. `INDEX.md` wird nur auf
   die eindeutige neue Intake-Zeile geprüft, damit spätere Anhänge möglich bleiben.

## Nachrechenbare Zähler und Tagmenge

<!-- COUNTS:START -->
| Metric | v10 | v17 | v18 |
|---|---:|---:|---:|
| entries | 63 | 88 | 90 |
| READ_COMPLETE | 56 | 88 | 88 |
| PARTIAL | 7 | 0 | 2 |
| pending_candidates | 11 | 8 | 6 |
| identities | 74 | 96 | 96 |
| points | 192 | 258 | 259 |
| relations | 38 | 66 | 66 |
| conflicts | 5 | 14 | 14 |
| outside_claim_vocabulary | 100 | 93 | 93 |
<!-- COUNTS:END -->

Die sechs Referenztags sind genau: `FAKT`, `MODELL`, `HYPOTHESE`, `METAPHER`, `ANALOGIE`, `UNRESOLVED`.

<!-- TAGS:START -->
| Tag | v10 | v17 | v18 |
|---|---:|---:|---:|
| ARCHITEKTUR | 4 | 4 | 4 |
| AUDIT | 1 | 1 | 1 |
| CLAIM-GUARD | 9 | 8 | 8 |
| FAKT | 19 | 39 | 40 |
| GUARD | 30 | 24 | 24 |
| HYPOTHESE | 2 | 3 | 3 |
| INFERENZ | 1 | 2 | 2 |
| KORPUSBEFUND | 7 | 7 | 7 |
| MODELL | 54 | 101 | 101 |
| POESIE | 1 | 1 | 1 |
| PROVENIENZ | 1 | 1 | 1 |
| REPORTED | 7 | 7 | 7 |
| SPEC | 39 | 38 | 38 |
| UNRESOLVED | 17 | 22 | 22 |
<!-- TAGS:END -->

## Erkannte Befunde und Behandlung

| ID | Befund im Eingang oder Review | Behandlung im Export |
|---|---|---|
| EXPORT-04 | Der Bericht verankert v17; die ausgelieferte Indexdatei ist bereits v18 mit Vergleichsblock. Eingebettete Versionsfelder nennen den Schreib-Eingang. | Beide Originalhashes und Rollen ausweisen; bestätigte Speicherversion separat; Materialisierung nicht mit eingebetteter Metadatenbehauptung verwechseln. |
| EXPORT-05 | Berichtszähler 0 PARTIAL / 258 Punkte gehören zu v17; v18 trägt 2 PARTIAL / 259 Punkte. Vergleich unterschiedlicher Stände wirkte wie Zählerfehler. | Beide Stände aus Einträgen berechnen; v17-Tabelle erhalten; zwei Teillektüren und `next_read` ausschließlich als Folgeschritt führen. |
| EXPORT-06 | Eine Gegenlesung zählt 84 außerhalb einer unbenannten Sechsermenge. | corpus-gate-v0.2-Menge namentlich fixieren; mit dieser Menge sind es 93 in v17 und 93 in v18; keine Umdeutung der Quelltags. |

EXPORT-01 bis EXPORT-03 bleiben als historische Befunde des v10-Exports erhalten.
Die neuen IDs sind lokale Exportbefunde, keine VOID- oder Registry-Kennungen.

## Erhalten, verloren, ungeprüft

Erhalten: Projektpunkte, Beleganker, Claims und Quelltags, Quell-IDs/Fassungsmarker,
Lesebereiche, Fortsetzungen, HOLD-Gründe, Herkunftsfamilien, frühere Beobachtungen,
Relationen, Konflikte und Schutzbedingungen. Ein Update entfernt kein Originaldokument.

Transferverlust: Laufsteuerung, Suchinventare, interne Datei-/Lauf-IDs, Cursor,
globale Laufhistorie, `index_identity` und der globale Vergleichsblock werden nicht publiziert.
Die jeweilige Vergleichsbeobachtung an bearbeiteten Einträgen bleibt erhalten.
Das Paket ist kein wiederanlaufbarer privater Korpusindex.

Quellauslassungen: Originalchats, PDF-/DOCX-Bilder, historische Rohturns und externe
Forschung waren im Index bereits nicht vollständig repräsentiert. Die 12 gezielten
Lesefenster des Vergleichslaufs sind keine neue Volllektüre der 88 Originale.
Der Verifier beweist keine Herkunfts-Unabhängigkeit, Bedeutungsfidelity oder historischen Ereignisse.

## Sichtbarkeit und Rücknahme

Dieser Branch ist ein vorbereiteter Publikationsvorschlag für das öffentliche Repo.
Der Nutzer hat Vergleich und Gegenprüfung beauftragt; dieses Receipt behauptet
keine zusätzliche menschliche Kanonentscheidung oder bereits erfolgte Veröffentlichung.
Es werden nur abgeleitete Projektinformationen exportiert. Quelldokumente,
private Medien und Suchcursor gehören nicht in den Patch.

Ein späterer Nachtrag kann diesen Stand als überholt markieren. Historische
Snapshots bleiben erhalten. Öffentliche Forks und Caches wären nach Veröffentlichung
nicht zuverlässig rückrufbar. Konkrete Falsifikatoren sind falsche Zähler,
veränderte Baseline-/Paketbytes, eine verlorene Fortsetzung oder ein nachgewiesener
Widerspruch zwischen Export und den jeweiligen Originalbytes. Die mechanische
Prüfung hält diese von semantischen Gegenbefunden getrennt.
