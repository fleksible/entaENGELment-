# Prüfbericht: Suchreparatur für Originalbytes, Datensatzidentität und Trefferausschnitt

**Datum:** 2026-11-13 · **Status:** ANNEX / DERIVED · Review-Kandidat

**FOKUS:** Suchtreffer an Originalquelle binden

**Promotion-Effect:** none

## Auftrag und Grenze

[ANNEX] Begrenzter Umsetzungsauftrag A0–A3 für die
[quellgebundene Stichwortsuche](../annex/CORPUS_SEARCH_v0_1.md): drei
nachgestellte Fehlerfamilien reparieren, Regressionen ergänzen, Ergebnis
prüfbar liefern. Geändert sind `tools/corpus_search.py`,
`tests/unit/test_corpus_search.py`, der Suchvertrag und dieser Bericht.
GOLD, Policies, Seeds, VOIDMAP, Receipts, Ledger und JS-/UI-Dateien sind
unverändert. Kein Merge, keine Kanon- oder Statuspromotion, keine privaten
Quellen im Diff.

## Basis, Head und Umgebung

| Gegenstand | Stand |
| --- | --- |
| Basis `main`, am 13.11.2026 neu aufgelöst | `8a159f277b375745547e1ab229b04a89929c55e5` |
| Suchcode vorher | Blob `f92da8bb35b64b2f2fe52900b0a6685f5b74e442`, SHA-256 `41b9844f4a1a8e1bda7563a1bac999665cd74e38276c3688657fa44e0ea7c8e5` |
| Reparatur-Commit | `58362ba18ef4325d4d85a65810c0aa7d8d510bf9` |
| Geprüfter Code-Commit, mit einem zusätzlichen Test | `51e0325e2152196e556d036234ec2c85d461ec6e` |
| Suchcode nachher | Blob `fd481017f972ba9b8b180f9c768a7ce7929f20b9`, SHA-256 `31e423c03dd33427bd75ebfcaf3cdfff8ca8dc5ccb1e860f0443d9bb8fc0b2df` |
| PR #423, neu aufgelöst | Head `af2d092dcff2136d675c10d80c6991d1a3bff714`, unverändert, hier nicht bearbeitet |

[FAKT] Basis, Blob und Hash stimmen mit dem übergebenen Startanker überein;
die drei Fehlerfamilien waren am aufgelösten Stand nicht bereits behoben.

[FAKT] Umgebung: Linux, Python 3.13.18 mit Unicode-Daten 15.1.0, Abhängigkeiten
über `make install-dev` aus `uv.lock` mit uv 0.12.18 in einer Umgebung außerhalb
des Repos, pytest 9.1.1. Die Suchsuite lief zusätzlich mit Python 3.11.16
(Unicode 14.0.0, die CI-Version) und 3.12.14 (Unicode 15.0.0, die Version der
Übergabe). Die Vollsuite lief nur unter 3.13.18.

[ANNEX] Dieser Bericht und sein Verweis im Suchvertrag kommen in einem
Folgecommit hinzu, der keinen Code und keinen Test ändert. Die Bindung der
Prüfungen an den endgültigen Head steht in der PR-Beschreibung.

## Vorher und nachher

[FAKT] Dieselben zehn synthetischen Proben wie in der übergebenen Reproduktion,
je einmal gegen den alten und den neuen Suchcode ausgeführt:

| Probe | Alter Code | Neuer Code |
| --- | --- | --- |
| Import mit LF | Bytes und Hash stimmen | unverändert |
| Import mit CRLF | Original zu LF verändert, Hash weicht vom Git-Hash ab | Original, Manifest-Hash und Git-Hash entsprechen den gelieferten Bytes |
| Import mit CR | wie CRLF | wie CRLF |
| Gleiche Bytes, Startzeile 10 und 100 | Bau bricht ab, Exit 2, `UNIQUE constraint failed: docs.id` | Exit 0, zwei Datensätze, zwei Kennungen, ein Inhaltshash |
| Gleiche Bytes, zwei Repräsentationen | wie zuvor, Exit 2 | Exit 0, zwei Datensätze, zwei Kennungen, ein Inhaltshash |
| Lange Vorzeile, literal | Zeile 2 gemeldet, Suchwort nicht im Ausschnitt | Zeile 2, Suchwort im Ausschnitt |
| Später Treffer auf langer Zeile, literal | Zeile 1 gemeldet, Suchwort nicht im Ausschnitt | Zeile 1, Suchwort im Ausschnitt |
| Später Treffer, tokens | wie zuvor | wie zuvor behoben |
| Kombinierter Umlaut, expanded | wie zuvor | Ausschnitt zeigt die kombinierte Originalschreibung |
| Kurzer Kontext | 38 Zeichen, Vor- und Folgezeile | identisch |

[FAKT] Zusammengefasst: alter Code acht verletzte und zwei eingehaltene
Verträge, neuer Code null verletzte und zehn eingehaltene; beide Läufe Exit 0.

[FAKT] Die übergebene Reproduktion selbst erwartet den alten Fehlerzustand.
Am alten Code endet sie mit Exit 0, am neuen mit Exit 1 an ihrer ersten
Fehlererwartung. Keiner dieser beiden Exit-Codes ist der Fix-Nachweis; den
führen die Vertragsproben oben und die Regressionstests unten.

## Was geändert wurde und welche Gegenprobe es trägt

[ANNEX] **Originalbytes.** Der lokale Import liest Bytes und dekodiert sie
ohne Umwandlung der Zeilenenden. Fehlerhafte UTF-8-Bytes brechen wie bisher mit
Exit 2 und benannter Meldung ab; ein eigener Test belegt das. Normalisiert wird weiterhin nur das Suchfeld. Der Hash gilt für die
gelieferte Textrepräsentation; aus einem Extrakt-Hash wird kein Hash des
ursprünglichen DOCX oder PDF.

[ANNEX] **Datensatzidentität.** Wirksame Repräsentation und wirksame Startzeile
werden an die bisherigen Bestandteile der Kennung angehängt. Die Regel gilt
einheitlich für alle Scopes; dadurch ändert sich jede Kennung gegenüber älteren
Indizes. Am öffentlichen Repo-Stand: 797 Dokumente, 797 gleiche Inhaltshashes,
keine gleiche Kennung, 797 eindeutige neue Kennungen. Die nach Inhalt
bereinigte Zählung hängt weiter nur am Inhaltshash.

[ANNEX] **Verbleibende Dublette.** Ein vollständig identischer zweiter Eintrag
bricht den Bau weiterhin mit Exit 2 ab, jetzt mit einer benannten Meldung statt
der SQLite-Meldung. Es wird nichts verschmolzen. Ein `start_line`-Wert, der
keine ganze Zahl ist, wird beim Bau benannt abgewiesen; vorher wäre er erst bei
der Suche als unbehandelter Fehler aufgefallen.

[ANNEX] **Trefferausschnitt.** Der Ausschnitt wird aus dem Originaltext um die
Fundstelle geschnitten. Normalisierte Positionen werden nicht zum Schneiden
benutzt: Gesucht wird der kleinste Originalabschnitt aus ganzen Zeichen, dessen
Suchform den Treffer enthält; er wird vor der Ausgabe erneut verglichen, sonst
gilt die ganze Zeile. Die Grenze von 1.800 Zeichen bleibt. Drei neue
Ausgabefelder machen Lage und Vollständigkeit lesbar: `excerpt_match`,
`match_span_in_excerpt`, `excerpt_clipped`. Zeilenanker und `anchor_kind`
sind unverändert; ein Dokumentanker bleibt Dokumentanker.

[FAKT] Gegenprobe der Tests selbst: Sechs gezielte Rückbauten des neuen Codes
in einer Wegwerfkopie lassen jeweils die zuständigen Tests fehlschlagen.

| Rückbau | Fehlschlagende Tests |
| --- | --- |
| Zeilenenden wieder umwandeln | Bytes/Hash, Zeilenanker bei CRLF und CR |
| Startzeile aus der Kennung nehmen | zwei Positionen |
| Repräsentation aus der Kennung nehmen | zwei Repräsentationen |
| Ausschnitt wieder am Kontextanfang beginnen | lange Vorzeile, später Treffer, Schreibvarianten, Tokenspanne, Zeichengrenzen |
| Normalisierte Positionen direkt am Original verwenden | Schreibvarianten, kombinierte Zeichen, Selbstprüfung der Rückabbildung |
| Teiltreffer als vollständig ausgeben | Kennzeichnung langer Treffer |

[FAKT] Gegenprobe gegen unbeabsichtigte Verhaltensänderung: Index des
öffentlichen Repo-Stands `8a159f2` mit altem und neuem Code in zwei neue
Ordner gebaut. `statistics.json` und `word-frequency.csv` sind bytegleich
(797 Dokumente, 593.223 lexikalische Einheiten). 13 Anfragen in allen drei
Modi ergeben 2.745 Treffer mit gleichen Dokumenten, Zeilen, Ankerarten und
Statusangaben. Von 2.727 Treffern, deren alter Ausschnitt nicht an der Grenze
lag, ist der neue Ausschnitt in allen Fällen textgleich. 18 alte Ausschnitte
lagen an der Grenze. 128 Treffer sind Dokumentanker, einer ist ein Tokentreffer
mit einer Spanne über 1.800 Zeichen und entsprechend gekennzeichnet.

## Ausgeführte Prüfungen am Code-Commit

| Prüfung | Ergebnis | Exit |
| --- | --- | --- |
| Suchsuite, Python 3.13.18 | 36 bestanden, 28 Subtests; vorher 20 und 4 | 0 |
| Suchsuite, Python 3.11.16 und 3.12.14 | je 36 bestanden | 0 |
| `make verify` | 1.222 bestanden, 2 übersprungen, 193 Subtests; Ports, Pointer und Claim-Lint bestanden | 0 |
| `make verify` an der Basis, gleiche Umgebung | 1.206 bestanden, 2 übersprungen, 169 Subtests | 0 |
| `make verify-governance` | 16 Workflows, 22 VOID-Einträge synchron | 0 |
| `ruff check src/ tools/ tests/` | bestanden | 0 |
| `black --check src/ tools/ tests/` | 129 Dateien unverändert | 0 |
| `mypy src/ tools/` | 59 Quelldateien ohne Befund | 0 |
| `bandit -c .bandit.yaml -r src/ tools/` | ohne Befund | 0 |
| `claim_lint.py --scope index,spec,receipts,tools --strict` | ohne Befund | 0 |
| `git diff --check` | ohne Befund | 0 |

[FAKT] Die zwei übersprungenen Tests gehören zu `test_corpus_datalad.py` und
verlangen DataLad und git-annex, die in dieser Umgebung fehlen. Sie sind an
Basis und Head gleich übersprungen und betreffen den Suchcode nicht.

[FAKT] Der Diff wurde auf private Kennungen und Übergabepfade durchsucht; kein
Fund. Alle neuen Testquellen sind synthetisch und im Test selbst erzeugt.

## Auslassungen und Grenzen

- [ANNEX] NOT_RUN: `make verify-js`. Der Diff berührt keine UI-, Package- oder
  Workspace-Datei.
- [ANNEX] NOT_RUN zum Berichtszeitpunkt: CI am PR-Head. Lokale Läufe ersetzen
  sie nicht.
- [ANNEX] NOT_RUN: DataLad-End-to-End-Tests, siehe oben.
- [ANNEX] Kein Lauf mit privatem Korpus, kein Neubau bestehender privater
  Indizes. Alte Indizes und die
  [Referenzmessung](../validation/fixtures/corpus_search_reference_v0_1.json)
  sind nicht verändert; die Referenz bleibt an ihre damalige CLI-Fassung
  gebunden.
- [ANNEX] Kosten: Die Rückabbildung rechnet nur auf der ersten Trefferzeile
  eines Dokuments. Bei einer einzelnen Zeile von 3,7 MB mit Umlauten stieg eine
  wörtliche Suche von 0,3 auf 1,2 Sekunden. Am öffentlichen Repo-Stand lagen
  alle 13 Anfragen unter einer Sekunde.
- [ANNEX] Folge der erhaltenen Zeilenenden: Eine wörtliche Anfrage, die selbst
  einen Zeilenumbruch enthält, muss bei lokalen CRLF- oder CR-Quellen deren
  Zeilenende treffen. Für Git-Dateien galt das bereits; das Suchfeld
  normalisiert weiterhin nur NFC und Groß-/Kleinschreibung.
- [ANNEX] Beobachtet und nicht geändert, weil außerhalb der drei
  Fehlerfamilien: Die Steuerdateien für `--corpus` und `--aliases` werden mit
  der Standardkodierung der Plattform gelesen. Ein abgebrochener Bau hinterlässt
  einen angefangenen Ausgabeordner. Korpuseinträge ohne Angabe erhalten die
  Repräsentationsbezeichnung `tracked_raw_utf8`. Bei einem Dokumentanker zeigt
  der Ausschnitt weiterhin den Dokumentanfang; neu ist nur seine Kennzeichnung.

[UNRESOLVED] Semantische Suchgüte, Wiederauffindbarkeit an echten
Wiedereinstiegsfragen und Quellenunabhängigkeit sind nicht gemessen. Ein
Suchtreffer mit korrektem Hash und sichtbarer Fundstelle belegt weder Lektüre
noch Bedeutung noch Freigabe. Der Code setzt kein READ_COMPLETE, keine
menschliche Entscheidung, keinen Kanonstatus, keine Kη-Bindung und schließt
kein VOID.

## Rückweg

[ANNEX] Den Code-Commit zurücknehmen und einen eigenen Index in einem neuen
Ordner bauen. Das Tabellenschema ist unverändert; geprüft wurde, dass der neue
Suchcode einen alten Index und der alte Suchcode einen neuen Index liest.
Kennungen aus Indizes vor und nach der Reparatur sind nicht vergleichbar.
Lokale Korpuseinträge mit CRLF oder CR erhalten beim Neubau einen anderen,
jetzt zu den Bytes passenden Hash; ältere Aufzeichnungen dieses Hashes werden
dadurch nicht rückwirkend korrigiert. Es ist keine Quelldatenmigration nötig.
