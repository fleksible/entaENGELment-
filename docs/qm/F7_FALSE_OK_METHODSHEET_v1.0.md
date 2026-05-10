---
doc_id: F7_FALSE_OK_METHODSHEET_v1.0
title: "QM-Methodenblatt: Fehlerklasse F7"
subtitle: "False OK despite Missing or Unverified Required Input"
version: "1.0"
status: "exportfähig unter aktuellem Prüfumfang"
internal_reference: "Unmarked VOID under False Safety"
created: "2026-05-10"
claim_status: "[MODELL] auditierbare Fehlerklasse für QM-/Safety-Analysen; kein Rechts- oder Sicherheitsgutachten"
---

# QM-Methodenblatt: Fehlerklasse F7

## False OK despite Missing or Unverified Required Input

**Interne Referenz:** Unmarked VOID under False Safety

## 1. Kurzdefinition

**F7 = Falsches OK trotz fehlender oder ungeprüfter Entscheidungsgrundlage.**

F7 beschreibt einen **Statusvertragsbruch**: Ein System signalisiert OK, Normalität, Vollständigkeit oder Freigabe, obwohl eine dafür erforderliche Information fehlt oder nicht verlässlich geprüft wurde.

Kurzformel:

> **F7 liegt vor, wenn ein System „grün“ meldet, obwohl die Grundlage für „grün“ fehlt oder nicht geprüft wurde.**

## 2. Die drei zwingenden Kriterien

Ein F7-Fehler liegt nur vor, wenn alle drei Bedingungen erfüllt sind:

1. **Defizit**  
   Ein erforderlicher Eingabewert fehlt oder ein erforderliches Prüfmerkmal ist nicht erfüllt.

2. **Unsichtbarkeit**  
   Dieser mangelhafte Zustand wird nicht sichtbar als Problem, Warnung oder Lücke markiert.

3. **Falsche Sicherheit**  
   Das System gibt trotzdem ein OK-, Normal-, Vollständig- oder Freigabesignal aus, zum Beispiel grüner Haken, Prozessfreigabe oder Weiterleitung.

## 3. F7-Typologie

### F7a — Missing Required Input

Ein erforderlicher Wert fehlt vollständig, wird aber nicht als fehlend markiert.

### F7b — Unverified Required Input

Ein Wert liegt vor, ist aber nicht verlässlich geprüft, zum Beispiel wegen fehlendem Zeitstempel, unklarer Quelle, falscher Zuordnung, fehlender Kalibrierung, veralteter Gültigkeit oder unvollständiger Prüfung.

## 4. Ausschluss: Kein F7

F7 liegt nicht vor, wenn:

- der fehlende oder ungeprüfte Wert sichtbar und korrekt als Warnung oder Fehler markiert wurde;
- das System keinen OK-, Normal-, Vollständig- oder Freigabestatus erzeugt hat;
- der betroffene Wert für die konkrete Entscheidung nicht erforderlich war;
- eine Person trotz korrekter und sichtbarer Warnung bewusst weitergehandelt hat;
- ein Defekt vorlag, aber kein falsches Freigabe- oder Normalitätssignal erzeugt wurde.

## 5. Audit- und Prüffragen

Zur Identifikation von F7 in RCA, CIRS, Safety-Audits oder Post-Mortems:

1. Welche Information war laut Regel, Prüfprotokoll, Risikobewertung oder Systemlogik für diese Entscheidung erforderlich?
2. War diese Information zum Zeitpunkt der Freigabe vorhanden?
3. War sie aktuell, gültig, vollständig, korrekt zugeordnet und verlässlich geprüft?
4. Wurde sichtbar angezeigt, wenn sie fehlte oder ungeprüft war?
5. Gab es trotzdem ein OK-, Normal-, Vollständig- oder Freigabesignal?
6. Haben Checklisten, Anzeigen, Routinen oder Hierarchien dieses Signal gestützt?
7. Wurde dadurch eine nachfolgende Fehlentscheidung wahrscheinlicher oder legitimiert?

## 6. Guardrail: Verantwortung nicht auflösen

**F7 entschuldigt lokales Fehlverhalten nicht pauschal.**

F7 verhindert aber, dass lokale Operatoren vorschnell als alleinige Ursache markiert werden. Die Fehlerklasse prüft, ob Systemdesign, Schnittstellen, Routinen oder Organisationskultur eine unvollständige Entscheidungsgrundlage als sicher erscheinen ließen.

## 7. Abgrenzung zu bestehenden Safety-Konzepten

| Konzept | Nähe zu F7 | Unterschied zu F7 |
|---|---|---|
| Latente Bedingungen | versteckte systemische Schwächen | F7 fokussiert speziell auf falsche OK-/Freigabesignale |
| Normalization of Deviance | Abweichungen werden normalisiert | F7 benennt den konkreten Mechanismus der unsichtbaren Unvollständigkeit |
| Swiss-Cheese-Modell | Lücken in Schutzschichten | F7 beschreibt eine spezifische Lücke: System meldet grün trotz fehlender Grundlage |
| Root Cause Analysis | Analyseverfahren für Ursachen | F7 ist eine Fehlerklasse, die in RCA geprüft werden kann |
| Sicherheitskultur | Unsicherheit wird nicht eskaliert | F7 ist enger und auditierbarer |
| Stop-Authority | Stoppen bei Unsicherheit | F7 zeigt, wann Stop-Authority durch falsche Normalmeldung entwertet wird |
| Human Error | lokale Fehlhandlung | F7 fragt zusätzlich, ob die Handlung durch falsche Systemsignale vorbereitet wurde |

## 8. Status

Dieses Methodenblatt ist als **v1.0 exportfähig unter aktuellem Prüfumfang** sedimentiert. Es ist kein abschließendes Sicherheits- oder Rechtsgutachten, sondern ein portables Analysewerkzeug für Situationen, in denen formale Sicherheit angezeigt wird, obwohl erforderliche Entscheidungsdaten fehlen oder ungeprüft sind.
