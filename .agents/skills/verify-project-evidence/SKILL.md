---
name: verify-project-evidence
description: Prüfe Abschlussbehauptungen, PR-Freigaben, CI- und Scanner-Ergebnisse gegen passende Quellen, Versionen und tatsächlichen Prüfumfang. Nutze dies vor Aussagen wie fertig, behoben, bestanden oder übernahmefähig sowie bei widersprüchlichen Prüfbelegen. Keine Aufrufpflicht vor jeder Antwort und keine automatische Handlungsfreigabe.
---

# Projektnachweise prüfen

Begründe jede wesentliche Abschlussaussage mit einem passenden Nachweis. Halte
beobachtetes Ergebnis, eigene Schlussfolgerung und erlaubte Handlung auseinander.
Begrenze den Aufwand auf die konkrete Unsicherheit.

## Gegenstand und Herkunft

- Bestimme Auftrag, Zielversion und relevante Umgebung. Löse aktuelle PR-Heads und
  Basen direkt auf. Binde CI und Reviews an den geprüften Commit; prüfe bei Bedarf
  den synthetischen Merge-Stand.
- Unterscheide selbst ausgeführte Befehle, direkt gelesene API-/CI-Datensätze,
  statisch gelesenen Code und zugeschriebene Berichte. Behaupte bei gelesenen Logs
  keinen eigenen Testlauf. Lies benötigte Originalpassagen statt ihrer Titel.
- Notiere Quelle, Version, Prüfumfang und wesentliche Zugangslücken knapp. Nutze
  vorhandene Prüfberichte, statt zusätzliche Register einzuführen.

## Passenden Nachweis wählen

- Bestimme die kleinste Beobachtung oder Gegenprobe, die die konkrete Aussage
  tragen könnte. Lint ersetzt keinen Build; Tests ersetzen keinen Vertragsabgleich.
- Verwende vorhandene Belege weiter, wenn Gegenstand, relevante Voraussetzungen und
  beanspruchter Umfang passen. Eine neue Nachricht allein verlangt keinen Testlauf.
  Prüfe veränderliche Zustände wie PR-Head, Review-Abschluss oder Berechtigungen
  erneut, soweit die Handlung davon abhängt.
- Führe bei relevanten Änderungen, neuen Fehlern oder offenen Fragen neu aus.
  Begründe zusätzliche Testbreite durch die verbleibende Lücke. Benenne bei
  unzugänglichen Fähigkeiten die unbeantwortete Frage.

## Ergebnis tatsächlich lesen

- Lies die entscheidenden vollständigen Prüfprotokolle einschließlich Exit-Code,
  Zusammenfassung, Fehlern, Skips und Abbrüchen. Weise gekürzte oder begrenzte
  Lesestände aus; verallgemeinere sie nicht auf ungelesene Teile.
- Prüfe verdeckte Fehler in Wrappern, Pipelines, Catch- oder Advisory-Modi.
  Ein grüner Sammeljob belegt keine übersprungenen Unterprüfungen.
- Unterscheide fehlgeschlagene Installation, nicht gestartete Tests und tatsächlich
  fehlgeschlagene Tests. Bei Scannern sind ausgeführter Lauf, erfasste Eingaben und
  Befunde getrennte Beobachtungen.
- Bewahre Rohbefund und Begründung. Eine Formatmeldung kann zutreffen, ohne einen
  Funktionsfehler zu belegen. Fehlende Reproduktion allein widerlegt keinen Bug.

## Schlussfolgerung begrenzen

- Prüfe Gegenlesarten: falsche Version, unerreichbarer Nutzungspfad, veraltete
  Spezifikation, vorhandener Schutz, Umgebungsunterschied oder zu breite Behauptung.
  Verwerfe Befunde erst mit passender Gegenbegründung.
- Nutze Teilprüfungen für ausdrücklich begrenzte Aussagen. Fehlende eigene Imports
  schließen transitive Nutzung nicht aus. Zwei Werkzeuge auf derselben Quelle
  sind nicht automatisch zwei unabhängige Evidenzkanäle.
- Erhalte das lokale Statusvokabular. Nicht geprüft beschreibt einen Nachweisstand;
  HOLD kann eine Handlungsentscheidung sein. Erzeuge keine universelle Abbildung
  zwischen Review-, Runtime- und HumanDecision-Zuständen.

## Gedeckte Handlung

- Nutze passende bestehende Aufträge und Delegationen. Trage technische Auswahl
  und Prüflast selbst; verlange keinen stellvertretenden Code-Audit.
- Leite aus Tests, einem Skill, Scanner, Schweigen oder technischer Empfehlung kein
  neues Merge-, Veröffentlichungs- oder Kanonisierungsmandat ab. Beurteile eine
  geäußerte Autorisierung nach ihrem tatsächlichen Umfang.
- Bringe neue Ziele, wesentliche Nebenwirkungen oder überschrittene Grenzen als
  verständliche Wirkungsfrage zurück. Menschliches Abnicken schließt keine
  technische Nachweislücke.

## Verständlich berichten

Nenne zuerst Ergebnis und praktische Bedeutung, dann tragenden Nachweis,
verbleibende Grenze und nächsten gedeckten Schritt. Passe die Länge dem Fall an;
erzwinge weder ein Formular noch eine routinemäßige Rückfrage.
Sichere beauftragte Artefakte im zuständigen Projekt- oder Dateispeicher.

Für entaENGELment und lokale Workflow-Scans lies bei Bedarf
[Projektbezug und Scannergrenzen](references/entaengelment.md).
