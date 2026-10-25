# Review: quellgebundene Stichwortsuche

**Datum:** 2026-10-25 · **Status:** ANNEX / DERIVED

**FOKUS:** nuancierte Repo- und Korpussuche prüfbar bereitstellen

## Problem und resultierendes Verhalten

[ANNEX] Eine reine Teilstringsuche übersieht Schreibvarianten oder vermischt
Worttreffer mit vorgeschlagener Bedeutungsnähe. Der neue lesende
[CLI-Vertrag](../annex/CORPUS_SEARCH_v0_1.md) erhält Originaltext, Ref und
Repräsentation; Schreibvarianten und semantische Nachbarn sind getrennte Modi.
Ein PR-Scope enthält ausschließlich seine vollständigen geänderten Dateien
gegenüber dem gemeinsamen Vorgänger. Keine Addition zu main.

[ANNEX] Das Paket umfasst CLI, sieben öffentlich quellgebundene Suchfamilien,
synthetische Funktionstests, einen Methodenfall und
[vorbereitete Phasen-Review-Fragen](../annex/PHASEN_REPLAY_REVIEWFRAGEN_v0_1.md).
Die Review-Fragen wählen keine Phasenquelle oder Sample-Zuordnung.

## Gelesene und ausgeführte Basis

[FAKT] Quellbasis vor dem Patch:
83caf03d6e8039637f147f1313238ca5cab611f6.
Für die separate PR-Probe wurde ausschließlich der öffentliche Head
af2d092dcff2136d675c10d80c6991d1a3bff714 gelesen.
Die feste [Referenzdatei](../validation/fixtures/corpus_search_reference_v0_1.json)
führt Codehash, Parameter, Segmentzahlen und fünf Queryproben.

[FAKT] Lokaler Prüfstand: Python 3.12.14 mit den gehashten Dev-Requirements
des gelesenen Stands installiert. make verify besteht mit 761 Tests und
169 Subtests. Davon gehören 20 Tests und vier zusätzliche Subtests zur neuen
Suchsuite. Der bestehende Stand umfasste 741 Tests und 165 Subtests.

[FAKT] Vollständig ausgeführt: ruff check src/ tools/ tests/,
black --check src/ tools/ tests/, mypy src/ tools/,
bandit -c .bandit.yaml -r src/ tools/ und make verify-governance.
Ruff und Black bestehen; Mypy prüft 53 Quelldateien; die Governance-Prüfung
meldet 15 Workflows und 22 synchronisierte VOID-Einträge. Keine neue
JS-/UI-Implementierung gehört zum Patch.

[FAKT] Der zusätzliche strenge Claim-Lint aus dem blocking PR-Gate wurde
ebenfalls ausgeführt. Sein erster Lauf markierte die wörtliche Git-Option
--verify als ungetaggten Claim; die konkrete Optionszeile ist jetzt als
Git-Syntax gekennzeichnet. Die Prüflogik und der Workflow bleiben unverändert.

## Gezielte Gegenfälle

- [FAKT] Ein synthetisches Symbol wird im Tokenmodus zurückgewiesen, wenn
  seine Zerlegung Zeichen verlieren würde.
- [FAKT] Tokenmehrfachheit wird mitgeführt; ein Trefferanker für ein ganzes
  Wort zeigt keinen früheren Teilstring in einem längeren Wort.
- [FAKT] Alias-Erweiterung bleibt opt-in. Ein bloßer Nachbarbegriff expandiert
  nicht automatisch zurück in den gesamten Begriffsknoten.
- [FAKT] Gleichnamige lokale Quellen mit verschiedenen Quellkennungen bleiben
  unterscheidbar; Familien bleiben bei fehlender Herkunft UNKNOWN.
- [FAKT] Ein generated_index wird vor dem Öffnen als Steuerartefakt
  ausgeschlossen; vorhandene Ausgabedateien bleiben erhalten.
- [FAKT] Rename, gelöschter Pfad und Größenlimit werden im Overlaymanifest
  ausgewiesen; zu große Blobs werden nicht in den Textindex eingelesen.
- [FAKT] Abgeschnittene Ergebnislisten sind gekennzeichnet; die Gesamtzahl
  passender Dateien wird nicht auf das Ausgabelimit reduziert.

## Öffentlicher Umfang

[ANNEX] Veröffentlicht werden Programm, synthetische Tests, öffentliche
Quellpfade und begrenzte Referenzzahlen. Private Korpusdateien, lokale
Suchdatenbanken, Auszüge, Zugangskennungen und persönliche Gesprächsrekonstruktionen
gehören nicht zum Diff. Der öffentliche Lauf verwendet kein --corpus.
Die Suchartefakte eines ausdrücklich erweiterten lokalen Laufs können dennoch
private Inhalte enthalten; die CLI ist kein Veröffentlichungsfilter.

## Offene Aussagegrenzen

[UNRESOLVED] Das Paket misst keine semantische Suchgüte und keine
Quellenunabhängigkeit. Originaltext- und Hashnachlese belegen keine vollständige
Genealogie oder Bedeutungsfidelity. Die Keywordkarte ist revidierbar.

[UNRESOLVED] #423 bleibt ein konkreter SIMULATION_PROXY-Kandidat mit offener
Modellwahl. Anbindung HOLD; zusätzliche Adapterfälle NOT_RUN; Kη-03 UNBOUND.
Graining, Blindseite und Sphärenstatus bleiben jeweils UNRESOLVED.

[ANNEX] GOLD, Receipts, VOIDMAP und bestehende Runtime-Verträge sind im
Patch unverändert. Die Dev-Audit-/Dependency-Frage aus #425 bleibt ein
eigenständiger Wartungsanschluss und wird nicht durch einen Suchlauf geschlossen.
