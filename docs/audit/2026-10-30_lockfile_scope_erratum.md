# Dependency-Scope: Paketidentitäten und Auflösungskanten

**Datum:** 2026-10-30  
**Fokus:** Scope-Erratum an den Quelldaten prüfen  
**Status:** DERIVED / REVIEW-PENDING; Beobachtung im gepinnten Git-Scope

## Gegenstand

Der Bericht `OUT/dependency_review_2026-10-09.md` behauptet einen ausschließlich
Next.js-bezogenen Lockfile-Diff. Ohne Granularitätsangabe ist diese Aussage zu
weit lesbar. Sie ist keine erfundene Paketänderung: Paketidentitäten und
Auflösungskanten tragen unterschiedliche Aussagen.

Quelle ist ausschließlich `pnpm-lock.yaml` zwischen
`a7773db68d97dbd8271b0921d011934d2e921170` und
`84ae92a175a5a9e56b2d547061dcb982f1009403`. Der zweite Commit ist das historische
Next.js-Sicherheitsupdate; nicht der aktuelle Arbeitsstand.

## Beobachtungen

| Ebene | Ergebnis | Grenze |
|---|---|---|
| Paketidentitäten (`packages`, name@version) | 12 Identitäten entfernt, 12 hinzugefügt; 12 Paketnamen aus der Next.js-Familie | Kein Nachweis unveränderter Auflösungskanten |
| Snapshot-Kennungen | 13 entfernt, 13 hinzugefügt | Vollständige Peer-Kontexte bleiben erhalten; keine automatische Paarung nach Paketname |
| Kanten unveränderter Snapshot-Eltern | zwei geänderte Referenzen: ein Versionswechsel und eine Peer-Kontextänderung | Keine Gleichsetzung von Basisversion und vollständiger Referenz |
| Kanten hinzugefügter/entfernter Eltern-Kontexte | je 51 hinzugefügte beziehungsweise entfernte Kanten | Keine 102 unabhängigen fachlichen Änderungen; Kontextwechsel bleiben sichtbar |

Die zwei Referenzänderungen bei unveränderter Elternkennung sind:

- `jest-message-util@30.4.1`, `dependencies.picomatch`: `4.0.5 → 4.0.7`.
- `eslint-import-resolver-typescript@3.10.1(...)`,
  `optionalDependencies.eslint-plugin-import`: Basisversion bleibt `2.32.0`,
  der Peer-Suffix ändert sich. Die vollständigen Zeichenfolgen stehen im JSON.

`picomatch@4.0.5` und `picomatch@4.0.7` sind vor und nach dem Update in `packages`
vorhanden. Die Zahl 13 betrifft hier Snapshot-Kennungen, nicht geänderte Paketnamen.
Eine Klassifikation „außerhalb des Next-Teilbaums genau eine Änderung“ wird nicht
allein aus Namen oder dem Entfernen von Peer-Suffixen abgeleitet.

## Diskriminierende Gegenprobe

Der historische Vektor unterscheidet die beiden Granularitäten:

1. Die Projektion auf Paketidentitäten enthält **keine** picomatch-Änderung. Als
   Detektor der geänderten Jest-Auflösung ist sie damit nachweislich unzureichend.
2. Der Kantenvergleich enthält die konkrete Auflösung `4.0.5 → 4.0.7`.
3. Zusätzlich wurde der Abschnitt `jest-message-util@30.4.1` in den rohen
   Git-Blobtexten zeilenbasiert gelesen, ohne den YAML-Parser oder die Kantenlogik
   des Generators zu verwenden. Er beginnt in beiden Ständen in Zeile 6952; die
   picomatch-Referenzen lauten `4.0.5` beziehungsweise `4.0.7`.
4. Der [ungefilterte Rohdiff](2026-10-30_lockfile_scope_raw.diff) ist separat
   abgelegt. SHA-256:
   `3d97882dc10b90f9bb101d7b86d9e7d27fdf100d61498d6162ad460eae079665`.

Die direkte Textkontrolle bestätigt diesen konkreten Prüffall. Sie beweist nicht
die Vollständigkeit des Parsers für beliebige Lockfiles. Die gemeinsamen
Git-Quellbytes sind sichtbar; die Beobachtungsverfahren sind verschieden.

## Reproduktion

```bash
python tools/lockfile_scope_diff.py \
  --base a7773db68d97dbd8271b0921d011934d2e921170 \
  --head 84ae92a175a5a9e56b2d547061dcb982f1009403
```

Die Ausgabe entspricht [2026-10-30_lockfile_scope_diff.json](2026-10-30_lockfile_scope_diff.json).
Vollständige Quell-SHAs, Blob-IDs, Datei-Hashes und Rohdiff-Hash stehen in `sources`.
Die Git-Historie muss die beiden Commits enthalten; es erfolgt kein automatischer
Netzabruf. Unterstützt ist Lockfile-Version 9.0; doppelte Schlüssel,
fehlende Abschnitte und ungültige Referenzformen werden abgewiesen.

Zehn gezielte Tests prüfen unter anderem die unsichtbare Kantenänderung bei
gleichem Paketbestand, Peer-Kontexte, optionale Kanten, Importer und ungültige
Eingaben. Der Generator ist ein Beobachtungsprogramm, kein Gate und kein
Sicherheits- oder Subtree-Zertifikat. Kommentare und Formatierung werden nur im
Rohdiff erhalten.

## Korrekturrückbindung

Der ursprüngliche Bericht erhält einen Erratum-Hinweis am Einstieg. Die alte
Aussage bleibt lesbar, ihre Reichweite wird ausgewiesen. Das importierte
`docs/intake/raw/2026-10-13/corpus-v17/corpus-delta.json` berichtete die zusätzliche
Zuordnung bereits; dieser Korpuswegweiser ist kein unabhängiger neuer Nachweis.

Der Verweis aus `pnpm-workspace.yaml` gilt der braces-Ausnahme. Deren materielle
Gültigkeit ist nicht Gegenstand dieser Prüfung. Weder Paketlisten noch der
Kantendiff belegen allgemein sichere Abhängigkeiten.

## Konsequenz für den Piloten

- `prevents`: Eine Inventaraussage wird als Aussage über den gesamten
  Auflösungsgraphen oder Änderungsumfang gelesen.
- `escape_detector`: Die bekannte Jest-Kante muss im Vergleich erscheinen und
  an den ungefilterten Quellblobs/Rohdiff unabhängig von der Listenlogik
  überprüfbar sein. Ein Prosaabgleich mit derselben Liste reicht nicht.

Die [vor den weiteren Läufen festgehaltenen Pilotkriterien](2026-10-30_pilot_criteria.md)
trennen Arbeitsstatus, Abschluss und Architekturentscheidung. Eine Übernahme als
Repo-Feld, Check, Gate oder Pflicht müsste diese beiden Angaben unabhängig vom
Intake-Etikett erfüllen. Hier wird keine neue Policy und kein Receipt-Schema
eingeführt.

## Ausgeführte Validierung

- Ausgangsstand: `make verify` mit 1126 bestandenen Tests, zwei Skips und 169
  Subtests. Der erste Versuch stoppte mangels lokal installiertem pytest vor
  der Testsammlung; danach wurde eine isolierte Prüfumgebung verwendet.
- Änderungsstand: `make verify` mit 1136 bestandenen Tests, zwei Skips und 169
  Subtests. Die zehn zusätzlichen Tests betreffen den Lockfile-Vergleich.
- `make verify-governance`: 16 Workflow-Postures bestanden, 22 VOIDs mit dem
  UI-Spiegel synchron. Das prüft keine live geltenden GitHub-Schutzregeln.
- Ruff über `src tools tests`, Black über dieselben Pfade und mypy über
  `src tools` bestanden. Bandit mit der unveränderten CI-Konfiguration
  `.bandit.yaml` über `src tools` bestanden; deren bestehende Ausnahmen sind
  keine neue Bestätigung der allgemeinen Sicherheit von subprocess-Aufrufen.
- Die erneute Erzeugung des gepinnten JSON ist bytegleich. Die bekannte
  picomatch-Kante wurde separat im Rohtext bestätigt.
- Die gezielten Metrikläufe sind in [den Pilotresultaten](2026-10-30_pilot_results.md)
  getrennt vom Scope-Experiment dokumentiert.

Lokal: CPython 3.12.14; bestehende wissenschaftliche Pakete plus isoliert
installierte Prüfabhängigkeiten. Die Lockfiles und die Projektabhängigkeiten
wurden nicht verändert. Das ist ein lokaler Ausführungsnachweis und ersetzt
keinen GitHub-CI-Lauf, keinen menschlichen Readback und keinen Merge-Entscheid.

Die erste GitHub-CI-Runde scheiterte im strikten Claim-Lint am Git-Optionswort
`rev-parse --verify`, nicht an einer fachlichen Aussage. `make verify` nutzt
denselben Claim-Lint ohne `--strict` und hatte den Hinweis nicht blockiert.
Die konkrete Operationszeile ist nun mit dem bereits vorgesehenen
`claim-lint: ignore` samt Begründung markiert; Linter und Workflow bleiben
unverändert. Der strikte CI-Aufruf wurde danach lokal erfolgreich ausgeführt.
