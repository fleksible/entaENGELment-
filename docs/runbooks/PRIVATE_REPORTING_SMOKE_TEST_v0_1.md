# Privaten Security-Meldeweg prüfen v0.1

**Status:** ANNEX · DERIVED · vorbereiteter Testablauf

**Datum:** 2026-10-23

**FOKUS:** privaten Meldeempfang prüfen

**Ausführung:** Einstieg geprüft; Versand und Empfang NOT_RUN

## Beobachteter Einstieg

[FAKT] Die öffentliche [Advisory-Seite](https://github.com/fleksible/entaENGELment-/security/advisories)
zeigt in der abgemeldeten Ansicht den Link `Report a vulnerability`. Sein Aufruf
führt zur GitHub-Anmeldung für das private Meldeformular. Das bestätigt einen
erreichbaren Einstieg, noch keinen Versand oder Empfang. Im verwendeten Browser
ist kein Reporter-Konto angemeldet.

[ANNEX] Für die noch offene Abnahme in [#332](https://github.com/fleksible/entaENGELment-/issues/332)
braucht es einen autorisierten Reporter ohne Maintainer-Zugriff auf dieses Repo
und anschließend die Empfangsbestätigung des Maintainers. Ein vom Owner selbst
angelegter Advisory-Entwurf würde diesen externen Zugangsweg nicht prüfen.

## Ein harmloser Testbericht

[ANNEX] Einmaligen Marker verwenden: `ENTA-REPORTING-SMOKE-20261023`.
Der folgende Text enthält ausschließlich synthetische Testdaten:

```text
Titel: TEST ONLY — ENTA-REPORTING-SMOKE-20261023 — keine Schwachstelle

Dies ist ein vereinbarter Funktionstest des privaten Meldewegs für Issue #332.
Es liegt kein Sicherheitsbefund vor. Der Bericht enthält keine Exploit-Schritte,
Secrets, personenbezogenen Daten oder privaten Projektunterlagen.

Bitte den Empfang dieses Markers privat bestätigen. Es werden keine CVE,
öffentliche Advisory-Veröffentlichung oder Änderungen am Projekt angefordert.
```

## Ablauf und Abnahme

1. Der autorisierte Reporter öffnet die Advisory-Seite mit seinem eigenen
   GitHub-Konto und folgt `Report a vulnerability`. Zugangsdaten bleiben im
   jeweiligen Anmeldeweg.
2. Nur den obigen Testtext übermitteln. Optionale Angaben zu betroffenen Paketen,
   Versionen, CWE oder Schweregrad leer lassen. Falls Pflichtfelder eine echte
   Schwachstelle voraussetzen, abbrechen und den Formularkonflikt quittieren;
   keine Schwachstelle oder Schwere erfinden.
3. Der Maintainer bestätigt den Marker im privaten Bericht. Die normale
   Maintainer-Ansicht darf den Bericht erkennen; fehlende öffentliche Sichtbarkeit
   allein beweist keine vollständige Vertraulichkeit.
4. In #332 nur Datum, Marker, Reporter-Rolle, beobachteten Zugangsweg und
   bestätigten Empfang vermerken. Private Berichtsadresse, Kontoidentität und
   Benachrichtigungsinhalte bleiben im privaten Kanal.
5. Den Testbericht nicht veröffentlichen oder als reale Schwachstelle behandeln.
   Seine weitere Behandlung dem Maintainer überlassen; keine automatische Löschung.

[UNRESOLVED] Versand und Empfang bleiben bis zur tatsächlichen Ausführung offen.
Außerdem verlangt #332 weiterhin den vollständigen beobachteten CodeQL-Trigger-
und Settings-Abgleich. Ein erfolgreicher Meldetest allein schließt dieses Issue
deshalb nicht automatisch.
