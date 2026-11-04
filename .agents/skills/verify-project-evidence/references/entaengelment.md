# Projektbezug und Scannergrenzen

## entaENGELment

Lies die zum geprüften Stand gehörende AGENTS.md. Behandle Runtime-, Receipt- und
Consent-Verträge als eigene Verträge. Dieser Skill ändert sie nicht.
Nutze bestehende Prüfberichte unter docs/audit/ und halte offene Befunde lokal.
Ein beobachteter Review-Kommentar ist keine formale GitHub-Review-Submission.

Persönliche Installation und repo-eigene Kopie können denselben Ablauf anbieten.
Wende ihn pro Prüfung einmal an. Vorhandensein oder Validierung einer SKILL.md
belegt weder automatische Ladung noch technische Durchsetzung.

## Lokaler zizmor-Pilot

Pinne Toolversion und Repository-Stand. Erfasse Workflows, lokale
Action-Definitionen und Dependabot-Konfigurationen (`.github/dependabot.yml`
oder `.yaml`). Übergib bevorzugt den Checkout als Ganzes; dokumentiere bei einer
bewusst engeren Dateiauswahl jede ausgelassene unterstützte Konfiguration.
Führe einen lesenden Offline-Lauf mit strikter Erfassung aus:

```bash
zizmor --offline --strict-collection --format=json-v1 /pfad/zum/checkout
```

Bewahre Ausgabe und ursprünglichen Exit-Code getrennt auf. Verwende keine
Autofix-Option. Prüfe mit einem kleinen kontrollierten Gegenfall, ob die
ausgewählte Regel und Fehlerweitergabe tatsächlich reagieren.
Unterscheide Fortschrittsausgabe auf stderr von Fehlermeldungen. Vergleiche
Befundzahlen nur bei gleichem Repository-Stand und gleichem Erfassungsumfang;
weise nachträglich erweiterte Eingaben separat aus.

Berichte Anzahl und Pfade erfasster Dateien, Parsefehler, ausgelassene
Online-Prüfungen und Findings. Fehlende Findings belegen nur diesen Scope.
Indirekt aufgerufene Shell-Skripte und fachliche Pflicht-/Warnungsabweichungen
brauchen gegebenenfalls eine eigene Prüfung. Übernimm neue CI-Gates erst als
gesonderte überprüfbare Änderung.

## Herkunft der Anregung

Eigenständige projektbezogene Formulierung vom 3. November 2026. Konsultierte
Anregungen, keine eingebundenen Abhängigkeiten oder übernommenen Skill-Pakete:

- https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md
- https://docs.zizmor.sh/usage/
- https://github.com/fleksible/entaENGELment-/pull/451

Erhalte bei späterer Übernahme fremder Dateien deren konkrete Herkunft und Lizenz.
