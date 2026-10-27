# DataLad-Korpus: Inventarauswahl und fehlende lokale Eingaben

Stand: 27. Oktober 2026 · DERIVED / technischer Nachtrag zu PR #428.
Ausgangshead: `fc1aaec52b9e942266032a0afa564ef39c89e3b1`.

## Auswahlregel sichtbar machen

[FAKT] Import-Records erfassen auch Dotdateien. Extraktion, Inventar und `sources`
lassen Pfade mit einem punktbeginnenden Bestandteil aus. Fehlende Annex-Inhalte
werden ebenfalls nicht gehasht. `rootHashRule` und Runbook benennen jetzt diesen
Umfang: lokale Nicht-Dotdateien, Inhaltshashes einschließlich Wiederholungen,
keine Bindung von Dateinamen oder Ordnerstruktur. Die Hashberechnung selbst ist
unverändert; die erklärende Regel wird genauer.

Eine neue durchgängige Regression importiert zwei Dateien, inventarisiert eine
und zeigt, dass eine Änderung der Dotdatei den Anker unverändert lässt. Der
Import-Record enthält ihren ursprünglichen Hash. Das ist kein Verlust der Quelle.

## Im echten Lauf gefundener Fehler

[FAKT] Nach `git annex drop --force` einer synthetischen Eingabe brachen beide
Wrapper vor dem Skriptstart ab: `datalad run --input inbox` versuchte zunächst,
fehlende Inhalte zu beschaffen. Der reine Skripttest hatte diesen vorgeschalteten
Schritt nicht abgedeckt; eine neue `missing`-Meldung entstand dabei nicht.

Die Wrapper verwenden nun `datalad run --assume-ready inputs`. Sie verarbeiten den
lokalen Bestand und lassen die Skripte fehlenden Inhalt protokollieren. Ein
gezieltes `datalad get` bleibt eine bewusste, getrennte Aktion. Outputs werden
weiter von DataLad vorbereitet und der Befehl samt Ein-/Ausgaben aufgezeichnet.
Ein Exit 0 des Gesamtlaufs bedeutet weiterhin nicht vollständige Eingaben.

## Ausgeführte Prüfung

- Korpus-Suite mit installiertem DataLad/git-annex und pdftotext: 29 bestanden,
  kein übersprungener End-to-End-Test. Python 3.12.14, pytest 9.1.1,
  DataLad 1.7.1, git-annex 10.20261026, pdftotext 24.02.0.
- Vollständiges `make verify`: 770 Tests und 165 Subtests bestanden. Ruff, Black,
  mypy, Bandit, strenger Claim-Lint und Governance-Gates bestanden.
- Für den Vollsuite-Lauf steht der Python-Interpreter der Projektumgebung vor dem
  separaten DataLad-Werkzeugverzeichnis im PATH. Ein erster Lauf mit umgekehrter
  Priorität hatte zwei fehlgeschlagene Pointer-Unterprozessproben wegen dort
  fehlendem PyYAML; mit der korrekten Projektumgebung sind beide grün.
- Neue echte Regression: zwei Eingaben, vollständige Extraktion, eine Annex-Datei
  nur im synthetischen Dataset droppen, erneut extrahieren und inventarisieren.
  Ergebnis: `missing: 1`, `ok: 1`, altes Textderivat als `stale_outputs`, ein
  fehlender Inventareintrag und nur eine angebotene Reentry-Quelle.
- Gemeinsame Probe mit korrigiertem #427: init, Import in einen frischen Klon,
  sechs importierte Dateien, vier inventarisierte Nicht-Dotdateien,
  README im Annex und importierte Git-Steuerdatei inert. Drei gleichnamige Quellen
  werden getrennt signiert gespeichert und verifiziert.
- Extraktions- und Inventarläufe per `datalad rerun` wiederholt: kein neuer Commit.
  `git annex fsck` besteht. Nach dem Drop einer eindeutigen Quelle erreichen beide
  Wrapper ihre Skripte; Extraktion meldet `missing: 1 / ok: 3`, Inventar drei
  vorhandene und eine fehlende Datei.

Es wurden nur synthetische lokale Daten verarbeitet. Keine Projektabhängigkeit,
kein privates Original, kein externer Speicher-Remote und kein öffentlicher Anker
wurde hinzugefügt. Der Testklon verweist nur auf sein lokales synthetisches Original.
Herkunft vor dem Export-Ordner und Bedeutungstreue der Textextraktion bleiben offen.
