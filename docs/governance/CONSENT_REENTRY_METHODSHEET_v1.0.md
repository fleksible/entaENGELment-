---
doc_id: CONSENT_REENTRY_METHODSHEET_v1.0
title: "QM-Methodenblatt: Consent-Re-Entry-Schwelle"
subtitle: "Regulierung der Rückführung kontaktgenerierter Information"
version: "1.0"
status: "exportfähig unter aktuellem Prüfumfang"
internal_reference: "R8-Semipermeabilität / RZT-CONSENT-1 / No-Learning-on-Non-Match"
created: "2026-05-10"
claim_status: "[MODELL] Governance-/Systemdesign-Methodenblatt; ersetzt keine DSGVO-/Privacy-Prüfung oder Rechtsberatung"
---

# QM-Methodenblatt: Consent-Re-Entry-Schwelle

## Regulierung der Rückführung kontaktgenerierter Information

## 1. Zweck

Die Consent-Re-Entry-Schwelle prüft den Übergang von flüchtiger Interaktionsinformation zu dauerhafter Systempersistenz.

Das Methodenblatt ersetzt keinen DSGVO-/Privacy-Check. Es ergänzt ihn um eine architektonische Vertrauensprüfung: Nicht nur **„Darf verarbeitet werden?“**, sondern **„Darf diese konkrete situative Interaktionsspur in einen neuen Systemzustand zurückgeführt werden?“**

## 2. Vorprüfung: Legal Basis & Special Category Gate

Vor jeder Re-Entry-Autorisierung ist zu prüfen, ob die betreffende Datenkategorie überhaupt verarbeitet werden darf.

Besonders kritisch sind:

- Gesundheitsdaten und psychische Belastungsdaten;
- Beschäftigtendaten;
- relationale Informationen über Dritte;
- Profiling- oder Scoring-nahe Daten;
- Daten, die in Dashboards, Managemententscheidungen oder Leistungsbewertungen einfließen könnten.

Architektonische Freigabe ersetzt keine Rechtsgrundlage. Fehlt die rechtliche Zulässigkeit, ist Re-Entry gesperrt.

## 3. Re-Entry-Autorisierung

Damit eine Interaktionsspur dauerhaft gespeichert oder systemisch wirksam werden darf, müssen vier Bedingungen erfüllt sein:

### 3.1 Explizitheit

Die Zustimmung erfolgt aktiv, informiert und nachweisbar. Schweigen, Weiternutzung oder emotionale Offenheit reichen nicht aus.

### 3.2 Kontextbindung

Die Freigabe gilt nur für den konkreten Zweck. Jeder Skalenwechsel, etwa Sitzung → Nutzerprofil → Aggregat → Management-Dashboard, benötigt eine neue Prüfung.

### 3.3 Widerrufbarkeit

Persistente Informationen müssen isolierbar, auffindbar und löschbar bleiben. Informationen dürfen nicht in nicht trennbare Modellgewichte oder Blackbox-Speicher eingehen, wenn Widerruf oder Löschung erforderlich sein können.

### 3.4 Zweckbindung

Die Information darf nur für die Funktionen wirksam werden, für die sie freigegeben wurde.

## 4. Fehlerklasse: Unconsented Re-Entry / Shadow Profile Formation

Ein Fehler liegt vor, wenn ein System Informationen aus einer situativen Interaktion in dauerhafte Profil-, Analyse-, Trainings-, Steuerungs- oder Aggregationsstrukturen übernimmt, ohne dass dafür eine zulässige, explizite, zweckgebundene und widerrufbare Freigabe vorliegt.

Typische Folgen:

- verdeckte Profilbildung;
- unerwartete Personalisierung;
- nicht autorisierte Aggregation;
- Zweckwechsel ohne erneute Freigabe;
- Verlust der Nachvollziehbarkeit;
- Vertrauensbruch zwischen Nutzer und System.

## 5. Ausschluss: Kein Re-Entry aus bloßer Resonanz

Persistenter Re-Entry ist unzulässig aus:

- bloßer Passung im Dialogmoment;
- statistischer Vermutung;
- emotionaler Offenheit;
- Krisenkommunikation;
- impliziter Vertrautheit;
- wiederholtem Auftreten ohne explizite Freigabe.

## 6. Anti-Consent-Fatigue

Nicht jede triviale Präferenz erfordert einen harten Consent-Prozess.

Ein Re-Entry-Gate ist insbesondere erforderlich bei Informationen, die:

- personenbezogen oder identitätsnah sind;
- gesundheitsnah oder psychologisch sensibel sind;
- Verhalten, Leistung, Belastung oder Beziehungen betreffen;
- Dritte erwähnen;
- in Profile, Scores, Dashboards oder Organisationsebene einfließen können;
- später proaktiv zur Ansprache, Steuerung oder Bewertung genutzt werden könnten.

## 7. Architekturanforderungen

Ein System, das Consent-Re-Entry kontrollieren soll, benötigt mindestens:

- strikte Trennung von Session-Memory und Long-Term-Memory;
- deterministisches Re-Entry-Gate vor jeder Persistierung;
- Consent-Log mit Zeitpunkt, Zweck, Umfang und Datenkategorie;
- Purpose-Tags an persistierten Daten;
- isolierbare und löschbare Speichereinheiten;
- Audit-Trail für jede spätere Nutzung;
- Sperre gegen Speicherung in nicht löschbare Modellgewichte;
- getrennte Freigabe für Aggregation, Dashboarding oder Weitergabe an Dritte;
- sichtbare Nutzeroberfläche für Einsicht, Widerruf und Löschung.

## 8. DPIA Trigger Check

Bei besonderen Datenkategorien, Beschäftigtenkontext, Profiling, systematischer Auswertung persönlicher Aspekte, Management-Dashboards oder automatisierter Folgewirkung ist zu prüfen, ob eine Datenschutz-Folgenabschätzung erforderlich ist.

## 9. Prüffragen

1. Welche Interaktionsspur soll dauerhaft gespeichert oder systemisch wirksam werden?
2. Welche Datenkategorie liegt vor?
3. Gibt es eine rechtliche Grundlage für diese Verarbeitung?
4. Handelt es sich um besondere Kategorien personenbezogener Daten?
5. Liegt Beschäftigtenkontext oder Machtungleichgewicht vor?
6. Wurde aktiv, informiert, zweckgebunden und nachweisbar zugestimmt?
7. Ist der Zweck identisch mit dem ursprünglichen Interaktionskontext?
8. Gibt es einen Skalenwechsel, etwa Sitzung zu Profil, Profil zu Aggregat oder Aggregat zu Dashboard?
9. Ist Widerruf technisch möglich?
10. Sind die Daten isolierbar und löschbar?
11. Wird verhindert, dass die Daten in nicht trennbare Modellgewichte eingehen?
12. Gibt es ein Consent-Log und einen Audit-Trail?
13. Wird Re-Entry aus bloßer Resonanz, emotionaler Offenheit oder statistischer Vermutung blockiert?
14. Ist eine Datenschutz-Folgenabschätzung erforderlich?

## 10. Guardrail

Kontaktgenerierte Information darf nicht automatisch als frei wiederverwendbare Systemressource behandelt werden.

Eine Interaktionsspur bleibt an Zweck, Kontext, Einwilligung, Widerrufbarkeit und technische Nachvollziehbarkeit gebunden.

## 11. Status

Dieses Methodenblatt ist als **v1.0 exportfähig unter aktuellem Prüfumfang** sedimentiert. Es ist kein Rechtsgutachten und ersetzt keine Datenschutz-Folgenabschätzung, DPO-Prüfung, Betriebsrat-/Compliance-Abstimmung oder domänenspezifische Rechtsprüfung.
