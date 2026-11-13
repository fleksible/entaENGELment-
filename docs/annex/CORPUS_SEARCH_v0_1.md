# Quellgebundene Stichwortsuche v0.1

**Status:** ANNEX · DERIVED · Review-Kandidat

**FOKUS:** nuancierte Repo- und Korpussuche prüfbar bereitstellen

**Promotion-Effect:** none

## Zweck

[ANNEX] Die CLI [corpus_search.py](../../tools/corpus_search.py) macht Wortlaut,
Schreibvarianten und vorgeschlagene Nachbarn getrennt auffindbar. Sie liest
Git-Objekte an vollständigen Commit-Refs; zusätzliche lokale Textrepräsentationen
sind explizit wählbar. Getrackte Dateien werden nicht verändert oder ausgeführt.

[ANNEX] Sieben Suchfamilien in [der öffentlichen Suchkarte](corpus_search_aliases_v0_1.json)
sind aus benannten öffentlichen Repo-Pfaden abgeleitet. Die Karte ist ein
revidierbarer Suchvorschlag. Die Reihenfolge und Häufigkeit ihrer Treffer ist
kein Wahrheits- oder Relevanzrang. Private Interpretationen werden nicht aus
ihren öffentlichen Bezeichnungen rekonstruiert.

## Benutzung

[ANNEX] Ein öffentlicher Repo-Lauf braucht keinen Zugriff auf private Korpora.
Der Ausgabeordner muss außerhalb des untersuchten Repos liegen und neu oder leer sein.

~~~bash
python3 tools/corpus_search.py build --repo . \
  --ref 83caf03d6e8039637f147f1313238ca5cab611f6 \
  --aliases docs/annex/corpus_search_aliases_v0_1.json \
  --out /tmp/enta-search-example

python3 tools/corpus_search.py search /tmp/enta-search-example/search.sqlite3 \
  Grüneisen --mode literal --scope main

python3 tools/corpus_search.py search /tmp/enta-search-example/search.sqlite3 \
  Grüneisen --mode expanded --scope main

python3 tools/corpus_search.py search /tmp/enta-search-example/search.sqlite3 \
  Mast --mode tokens --scope main
~~~

[ANNEX] Für einen PR dessen aktuellen Head direkt auflösen und zum Bau
--overlay pr-NUMMER=VOLLSTAENDIGER_HEAD_SHA ergänzen. Das Overlay enthält nur die
vollständigen geänderten Dateien gegenüber dem gemeinsamen Vorgänger mit dem
gewählten main-Stand. Es ist weder der Vollbestand des PR-Branches noch eine
Anzahl neu hinzugefügter Wörter. Löschungen und Renames bleiben im Manifest
sichtbar; PR-Zahlen werden main nicht hinzuaddiert.

## Modi und Verlustgrenzen

| Modus | Tatsächliche Operation | Grenze |
| --- | --- | --- |
| literal | NFC-/Casefold-Teilstring im erhaltenen Dokument | Mast findet auch master; keine automatische Wortgrenze |
| tokens | Vollständige lexikalische Token, einschließlich geforderter Mehrfachheit | Reihenfolge und Nachbarschaft sind nicht gefordert; Bindestrichwörter sind zusammengesetzte Token |
| expanded | Original plus dokumentierte Schreibvarianten | Ein Begriff, der nur Nachbar ist, wird nicht still zur Ausgangsform |
| expanded mit --related | Zusätzliche markierte Nachbarqueries | related_not_equivalent erklärt ausdrücklich keine Bedeutungsidentität |

[ANNEX] Symbolqueries werden im Tokenmodus abgewiesen, wenn die Zerlegung
Nicht-Leerraumzeichen verlieren würde. Ein Symbol bleibt wörtlich suchbar.
Insbesondere muss 3|1|3 wörtlich gesucht werden; aus der Notation folgt kein
akustischer Adapter. Leere Queries und nichtpositive Trefferlimits werden
zurückgewiesen. Begrenzte Ausgaben nennen returned_documents und truncated;
die Dateitrefferzahlen beziehen sich auf den gesamten ausgewählten Suchscope.

[ANNEX] Normalisierung verändert nur den Suchindex. Der Originaltext bleibt
erhalten. Eine Rückreferenz erlaubt Textnachlese, belegt aber keine verlustfreie
semantische Übersetzung. Ein passender Token-Zeilenanker wird mit derselben
Tokenregel gesucht; ein dokumentweiter Mehrworttreffer ohne gemeinsame Zeile
wird als Dokumentanker ausgewiesen.

## Trefferausschnitt

[ANNEX] Der Ausschnitt wird aus dem erhaltenen Originaltext geschnitten und ist
höchstens 1.800 Zeichen lang. Passen Vorzeile, Trefferzeile und zwei Folgezeilen
in diese Grenze, erscheinen sie vollständig und mit ihren ursprünglichen
Zeilenenden. Andernfalls hat die Fundstelle Vorrang vor dem Kontext: Der freie
Platz wird vor und hinter ihr verteilt, und excerpt_clipped zeigt den Beschnitt an.

[ANNEX] Die Fundstelle wird im Original bestimmt, nicht in der Suchform.
NFC und Casefold verschieben Positionen: ß wird zu ss, Grundbuchstabe plus
kombinierendes Zeichen wird ein Zeichen. Die Suche ermittelt deshalb den
kleinsten Originalabschnitt aus ganzen Zeichen, dessen Suchform den Treffer
enthält, und vergleicht ihn vor der Ausgabe erneut. match_span_in_excerpt nennt
Anfang und Ende dieser Stelle innerhalb von excerpt. Die Anfrage strasse zeigt
so die Schreibung Straße, die Anfrage Grüneisen auch eine kombiniert kodierte
Fassung. Schlägt der Vergleich bei seltenen Zeichenfolgen fehl, gilt die ganze
Zeile als Fundstelle; ein Abschnitt, dessen Suchform den Treffer nicht enthält,
wird nicht ausgegeben.

[ANNEX] Im Tokenmodus reicht die Fundstelle vom ersten bis zum letzten
benötigten Token der Trefferzeile, bestimmt mit derselben Tokenregel. Text
zwischen diesen Token gehört zur Spanne, ist aber selbst kein Treffer.

| excerpt_match | Bedeutung |
| --- | --- |
| complete | Die Fundstelle liegt vollständig im Ausschnitt. |
| partial_match_exceeds_excerpt | Die Fundstelle ist länger als 1.800 Zeichen. Der Ausschnitt beginnt an ihrem Anfang und endet vor ihrem Ende. |
| not_located_document_level | Dokumentanker ohne gemeinsame Trefferzeile. Der Ausschnitt zeigt den Dokumentanfang, match_span_in_excerpt ist leer. |

[ANNEX] Vollständige Sichtbarkeit jeder Fundstelle wird damit nicht zugesagt.
Zugesagt ist, dass ein Zeilentreffer mit seinem Anfang im Ausschnitt steht und
dass eine unvollständige oder fehlende Anzeige ausdrücklich gekennzeichnet ist.
Ein Dokumentanker wird nicht zu einem Zeilentreffer umetikettiert.

## Ergebnis und Zähleinheit

[ANNEX] Jeder Bau erzeugt lokal search.sqlite3, manifest.json, statistics.json,
aliases.json und word-frequency.csv. Das Manifest führt Ref, Repo-Identität,
Dateipfad, Repräsentationshash, Suchrepräsentation und Ausschlüsse. Der Suchlauf
öffnet SQLite im Lesemodus. Bei unbekannter Repo-Identität wird kein GitHub-Link
erfunden. Deklarierte Statuszeilen behalten ihre Position; verschachtelte
Statuswerte werden nicht zu einem Status der gesamten Datei verschmolzen.

[ANNEX] Die Datensatzkennung entsteht aus Scope, Ref, Quellenkennung, Titel
beziehungsweise Pfad, Inhaltshash, wirksamer Repräsentation und wirksamer
Startzeile. Zwei Ausschnitte derselben Quellfassung mit gleichen Bytes, aber
anderer Position oder Repräsentation bleiben zwei Datensätze mit demselben
Inhaltshash. Datensatzidentität und Inhaltsgleichheit sind verschiedene Größen:
Die nach Inhalt bereinigte Zählung zählt solche Bytes weiterhin einmal.
Kennungen aus Indizes vor dieser Regel sind mit neuen nicht vergleichbar.

[ANNEX] Einheiten sind lexikalische Wort-/Codeeinheiten, keine Modelltoken.
Die offengelegte Regex zählt auch Bezeichner und Zahlen. Tokenvorkommen,
Dokumenthäufigkeit und nach identischen vollständigen Inhalten bereinigte
Vorkommen sind verschiedene Maße. Die Bereinigung kennt keine semantische
Dublettengleichheit und begründet keine Quellenunabhängigkeit.

[ANNEX] Code, Dokumente, Konfiguration, Audit-/Review-Pfade und importierte
Snapshots werden nach transparenten Pfad-/Dateitypregeln segmentiert. Das ist
keine semantische oder normative Klassifizierung. Locks/Requirements-Exporte,
nicht unterstützte Formate, Symlinks, Binärdaten, Nicht-UTF-8 und Texte über
4 MiB werden ausgewiesen. Der Größencheck erfolgt vor dem Blobabruf.
Quellmarkup und JSON-Escapes bleiben Rohtext; PDF-/Bild- und Archivpayloads
werden nicht inhaltlich erschlossen.

## Lokales Korpus nur ausdrücklich hinzunehmen

[ANNEX] --corpus akzeptiert eine lokale JSON-Liste mit local_path, title,
source_id, source_version, source_kind, source_family, representation,
read_state, start_line, claim_status und provenance_url, soweit bekannt.
Dies ist ein freiwilliger Zusatz zum öffentlichen Repo-Lauf. Unknown-Werte
bleiben unknown; maschinelles Indexieren ist keine vollständige Lektüre.

[ANNEX] Lokale Dateien werden als Bytes gelesen und ohne Umwandlung der
Zeilenenden als UTF-8 dekodiert. Der gespeicherte Originaltext entspricht damit
für LF, CRLF und CR den gelieferten Bytes, und sein SHA-256 gleicht dem Hash
derselben Bytes als Git-Blob. Der Hash gilt für die gelieferte
Textrepräsentation: Der Hash eines Extrakts bleibt der Hash des Extrakts und
wird nicht zum Hash des ursprünglichen DOCX oder PDF.

[ANNEX] Ein vollständig identischer zweiter Eintrag, also gleiche Quelle,
Fassung, Titel, Bytes, Repräsentation und Startzeile, bricht den Bau mit einer
benannten Dublettenmeldung ab. Er wird weder still verschmolzen noch doppelt
geführt. Ein start_line-Wert, der keine ganze Zahl ist, wird ebenfalls benannt abgewiesen.

[ANNEX] Gleichnamige Quellen behalten ihre Quellenkennungen. Die abgeleitete
Zeilenreferenz gilt für die angegebene Textrepräsentation, nicht automatisch
für Roh-MIME oder PDF-Seiten. Ein generated_index wird als Steuerartefakt
ausgeschlossen, bevor seine Bytes gelesen werden. Reviews bleiben Wegweiser
und keine unabhängigen Originalbelege.

[RISK] SQLite, Ausschnitte und Manifeste eines lokalen Korpuslaufs können private
Originaltexte, Titel oder Quellenkennungen enthalten. Der Ausgabeort außerhalb
des Repos verhindert keinen späteren manuellen Upload. Diese Dateien gehören
nicht automatisch in einen öffentlichen PR. Die Grenze steht in der
[GitHub Use Policy](../../GITHUB_USE_POLICY.md).

## Prüfung und Rückweg

[FAKT] Die [öffentliche Referenzmessung](../validation/fixtures/corpus_search_reference_v0_1.json)
bindet CLI-Quellhash, main@83caf03 und einen PR-Head. Am gepinnten main wurden
698 unterstützte Texte mit 506.322 lexikalischen Einheiten indexiert. Der
Referenzfall verwendet keinen privaten lokalen Korpus. Seine Zahlen sind kein
Sollwert für künftige Heads.

[ANNEX] [Die Funktionstests](../../tests/unit/test_corpus_search.py) verwenden
isolierte synthetische Repositories. Sie prüfen Symbolschutz, Wortgrenzen,
Tokenmehrfachheit, Aliasgrenzen, Original-/Quellenidentität, Ref-Pinning,
Outputschutz sowie Overlay- und Ausschlussverhalten. Seit dem 13.11.2026 prüfen
sie zusätzlich Zeilenenden und Hashbindung lokaler Importe, getrennte
Datensätze bei anderer Position oder Repräsentation sowie Lage, Originalschreibung
und Kennzeichnung der Fundstelle im Ausschnitt. Der zugehörige
[Prüfbericht](../audit/2026-11-13_corpus_search_originalspan_repair.md) führt
Basis, Vorher/Nachher und Auslassungen. Die Referenzmessung oben bleibt an ihre
damalige CLI-Fassung gebunden und wurde nicht rückwirkend angepasst.

[ANNEX] Der [Methodenfall](METHODENFALL_CORPUS_SEARCH_v0_1.md) trennt
Suchtreffer, Herkunft und Geltung. Die [Review-Fragen zum Phasenkandidaten](PHASEN_REPLAY_REVIEWFRAGEN_v0_1.md)
bereiten eine spätere Entscheidung vor; die Suche wählt keine HUD-Phase.

[UNRESOLVED] Vollständige Originalgenealogie, semantische Suchgüte und Nutzen
einer Suchoberfläche werden durch diese Funktionstests nicht nachgewiesen.

