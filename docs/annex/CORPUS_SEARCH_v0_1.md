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

## Ergebnis und Zähleinheit

[ANNEX] Jeder Bau erzeugt lokal search.sqlite3, manifest.json, statistics.json,
aliases.json und word-frequency.csv. Das Manifest führt Ref, Repo-Identität,
Dateipfad, Repräsentationshash, Suchrepräsentation und Ausschlüsse. Der Suchlauf
öffnet SQLite im Lesemodus. Bei unbekannter Repo-Identität wird kein GitHub-Link
erfunden. Deklarierte Statuszeilen behalten ihre Position; verschachtelte
Statuswerte werden nicht zu einem Status der gesamten Datei verschmolzen.

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
Outputschutz sowie Overlay- und Ausschlussverhalten.

[ANNEX] Der [Methodenfall](METHODENFALL_CORPUS_SEARCH_v0_1.md) trennt
Suchtreffer, Herkunft und Geltung. Die [Review-Fragen zum Phasenkandidaten](PHASEN_REPLAY_REVIEWFRAGEN_v0_1.md)
bereiten eine spätere Entscheidung vor; die Suche wählt keine HUD-Phase.

[UNRESOLVED] Vollständige Originalgenealogie, semantische Suchgüte und Nutzen
einer Suchoberfläche werden durch diese Funktionstests nicht nachgewiesen.

