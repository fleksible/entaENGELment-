---
name: corpus-accumulator
description: Erschließe unsere entaENGELment- und Synthbiosis-Projektdaten schrittweise und führe einen dauerhaften Korpusindex mit Herkunft, Lesefortschritt, neuen Fassungen und offenen Fragen. Nutze den Skill zum Akkumulieren vorhandener Unterlagen, für nächtliche Sammelläufe oder zum Fortsetzen einer Sichtung; kombiniere ihn mit corpus-gate und einer separat eingerichteten geplanten Aufgabe.
---

# Corpus Accumulator v0.2

Sammle Fundstellen, belegte Auszüge, Bearbeitungsstände und revidierbare Ableitungen. Führe einen wiederaufnehmbaren Index als `DERIVED / REVIEW-PENDING`. Bezeichne die Tätigkeit als Erschließung; behaupte dadurch weder Modelltraining noch vollständige Erinnerung an alle Gespräche.

## Lauf und Geltungsbereich

- Führe bei jedem Aufruf genau einen begrenzten Lauf aus. Ein Skill stellt keinen Hintergrundprozess und keinen App-Inaktivitätssensor bereit. Starte Wiederholungen über eine tatsächlich eingerichtete Automation.
- Verwende ausschließlich den in Auftrag/Index festgehaltenen Projektumfang. Standard: native Library-Unterlagen mit nachvollziehbarem Bezug zu entaENGELment oder Synthbiosis sowie ausdrücklich bereitgestellte Chatstellen. Suche anfangs mit `entaENGELment` und `Synthbiosis`; ergänze dokumentierte Projektaliase. Suchergebnisse bilden keine vollständige Inventur.
- Aktiviere Drive, GitHub oder weitere Quellen erst nach einem erfolgreichen Lesezugriff und mit konkretem Projektordner/Repo im Scope. Ein verlinkter Repo-Stand im Save State ist vorerst nur eine berichtete Quelle.
- Behaupte keinen globalen Chatarchiv-Zugriff. Erschließe frühere Chats nur über tatsächlich verfügbare Originalstellen oder Exporte. Bezeichne Zusammenfassungen als Zusammenfassungen. Halte fehlende Archive als Zugangslücke fest.
- Verwende den Library-Skill für Lesen/Speichern und `corpus-gate` für Intake. Suche einen nicht im Katalog sichtbaren persönlichen Skill nach seinem Frontmatter-Namen. Falls corpus-gate fehlt, halte Quellen-ID, Version, gelesenen Umfang, lokale Claim-Tags und HOLD-Gründe fest und melde die fehlende Abhängigkeit.

## Dauerhaften Stand laden

1. Lies den im Auftrag benannten Index über seine gespeicherte Library-ID. Ohne ID suche den Titel `entaENGELment_Korpusindex.md`, bei Nulltreffer einmal vereinfacht. Erzeuge einen neuen Index nur wenn kein bestehender aufgelöst wurde. Bei mehreren plausiblen Indizes melde HOLD und führe sie nicht automatisch zusammen.
2. Verwende das Format aus [references/index-format.md](references/index-format.md). Bewahre vorhandene Einträge und negative Information. Der Auftrag zum Akkumulieren autorisiert das Fortschreiben dieses abgeleiteten Index; er autorisiert keine Änderungen an Quelldokumenten oder Kanonisierung.
3. Speichere IDs und Lesefortschritt dauerhaft im Index. Verlasse dich zwischen Läufen weder auf lokale Dateien noch allein auf die Gesprächserinnerung.

## Ermitteln, lesen, zuordnen

1. Prüfe bekannte Quelldateien auf neue Versionen. Suche begrenzt nach neuen Fundstellen innerhalb des Scope. Übernehme exakte zurückgegebene IDs, Dateinamen und Zeitstempel. Lade höchstens zwei Such-/Inventarseiten pro Lauf; führe Suchcursor und offene Kandidaten weiter. Wenn ein Cursor abgelaufen ist, starte dieselbe Suche neu und dedupliziere anhand der gespeicherten IDs.
2. Bearbeite höchstens 12 Quellen bzw. 24 Leseabschnitte pro Lauf. Reserviere bei vorhandenem Rückstand mindestens zwei Plätze für die ältesten offenen Kandidaten. Bei Zeit-/Kontextgrenze speichere früher einen Teilstand. Kein Rekursionslauf über neu erzeugte Ableitungen.
3. Verwende `source_id + source_version` als Versionsschlüssel. Ohne Versions-ID verwende die tatsächlich zurückgegebenen Änderungszeit/Größe als vorläufigen Marker und markiere `version_reliability: provisional`. Ohne belastbaren Marker lies erneut; behaupte keine unveränderte Fassung. Ein neuer Marker erzeugt einen neuen Eintrag; alte Beobachtungen bleiben erhalten.
4. Behalte teilgelesene Quellen als `PARTIAL`, samt genauen Seiten-/Zeilenbereichen und Fortsetzung. Setze `READ_COMPLETE` nur wenn die Quelle vollständig gelesen wurde. Das bedeutet ausschließlich Lesestand, keine sachliche Validierung. Bei Versionswechsel während des Lesens brich die Zusammenführung ab, markiere HOLD und beginne mit der aktuellen Fassung neu.
5. Erstelle pro gelesener Quelle ein corpus-gate-Receipt. Speichere knappe Projektpunkte mit Belegstellen, eigenen Claim-Tags und den ursprünglichen Tags der Quelle. Übersetze Quelltags nur mit expliziter Mapping-Notiz. Belegte Wiedergabe einer Äußerung und sachlicher Wahrheitsanspruch bleiben verschiedene Aussagen.
6. Verknüpfe ähnliche Stellen als vorgeschlagene Relationen: `possible_duplicate`, `revises`, `contradicts`, `related`. Bestätige inhaltliche Gleichheit nur bei tatsächlichem Vergleich; gleiche Titel reichen nicht. Zwei Zusammenfassungen derselben Quelle zählen nicht als unabhängige Evidenz.
7. Bewahre fehlgeschlagene Reads als `RETRY` mit Fehler und Fortsetzung. Verdränge solche Einträge nicht durch einen globalen Zeitstempel. Steigere einen Claim niemals wegen Wiederholung, Dateimenge oder erfolgreichem Nachtlauf.

## Delta- und Präzisionsfilter

- Suche bei einer vermeintlich neuen Kernregel innerhalb desselben Laufbudgets zuerst passende ältere Projektformulierungen. Lies deren konkrete Passage. Vergleiche Herkunft, Input/Output, Guard, Falsifikator, Verlust und Rücknahme. Entscheide je Aussage REUSE, EXTEND, KEEP_BOTH oder HOLD; keine automatische Ersetzung der Quelle.
- Führe `source_family`, `parent_refs`, `contact_stage` und `independence_basis` aus corpus-gate fort. Gemeinsame Lineage ist eine Beziehung, keine inhaltliche Dublette. Bei unbekannter Herkunft bleibt Unabhängigkeit UNKNOWN.
- Unterscheide `new_file`, `new_version`, `new_wording`, `new_operation_candidate`, `status_drift` und `no_substantive_delta`. Neu importiert heißt nicht neu gedacht. `introduced` bleibt eine lokale Ergänzung, keine bestätigte Emergenz.
- Halte lesbaren Vorschlag, normative Entscheidung, Implementierung und getestetes Verhalten getrennt. Ergänze einen Scope-/Status-Konflikt, wenn ein Save State SPEC oder Code als validierte Runtime wiedergibt. Null Suchtreffer ist keine Abwesenheit.
- Automatisiere sichere Zuordnung und Vorschläge; automatische Löschung, Quellenverschmelzung und Claim-Promotion bleiben ausgeschlossen. UNKNOWN erzeugt eine konkrete Fortsetzung, keine wiederholte Neuformulierung desselben Befunds.
- Erfasse abgeleitete Reviews nur als Wegweiser/Arbeitsartefakte; zähle sie und ihre Kopien nicht als neue Evidenz. Zitiere Originalsätze nicht über immer neue Zusammenfassungen zurück in den Index.
- Speichere additive Felder nur für tatsächlich bearbeitete Einträge. Keine ungeprüfte globale Migration älterer Indexzeilen und keine unbegrenzte Rekursion. Halte einen aktuellen Kopf und eine strukturierte Historie; kopiere nicht bei jedem Lauf den kompletten alten Bericht in den Kopf.

## Speichern und rückmelden

- Schreibe die neuen Beobachtungen und den Fortsetzungsstand gemeinsam in dieselbe Indexdatei. Ersetze deren bestehende Library-ID mit Versionsschutz, soweit verfügbar. Bei Konflikt lies den aktuellen Index und ergänze nur fehlende Einträge; erzwinge kein Überschreiben.
- Werte den Lauf erst nach bestätigtem Speichern als gesichert. Bei Speicherfehler melde `UNSAVED`; behaupte keinen dauerhaften Fortschritt und setze keinen Erfolgscursor. Bei unklarem Speicherausgang lies den Index vor einem erneuten Create/Replace.
- Schließe Index, Akkumulatorberichte und deren Kopien als neue Evidenz aus. Halte die eigene Index-ID im Auftrag und die Rolle `generated_index` im Artefakt fest. Enthält ein Bericht externe Quellen, folge den Originalreferenzen nur innerhalb des Scope.
- Übernimm nur projektbezogene Daten. Fremde private Bilder, intime Inhalte und unverbundene Biographie sind kein Sammelauftrag. Bewahre hier höchstens eine minimale Auslassungsnotiz ohne sensitive Details.
- Liefere kurz: neu/aktualisiert/gelesen/teilgelesen/offen, wichtigster Konflikt und Speicherstatus. Vermeide eine neue Nachricht bei unverändertem Stand, sofern der Task dies erlaubt; melde Zugriffs- und Speicherblocker. Versprich keine Unterdrückung plattformseitiger Benachrichtigungen.
- Führe `RAW`, `DERIVED` und `HOLD` fort. Vorschläge für Kanonisierung bleiben im Review. Autorisiere keinen Merge, kein Löschen und kein Umschreiben einer Quelle aus diesem Workflow.

## Automation einrichten

Prüfe vor Aktivierung alle erforderlichen Quellen durch harmlose Lesezugriffe. Verwende den verfügbaren Automationsdienst mit der Nutzerzeitzone und dem gewählten Rhythmus. Lege den Index samt ID, Scope, Budget und zentralen Guards in den Aufgabenprompt; verlasse dich nicht auf nachträglich verfügbare Skills. Weise bei fehlendem App-Inaktivitätssignal darauf hin und vereinbare den alternativen Start. Teste vor Aktivierung einen kleinen Lauf am realen Material. Melde Installation des Skills, gesicherten Probelauf und Aktivierung des Zeitplans getrennt nach ihrem tatsächlichen Ergebnis.
