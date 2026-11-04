---
artifact_role: generated_review
status: DERIVED / REVIEW-PENDING
observed_date: 2026-11-03
promotion_effect: none
evidence_import: excluded_self
---

# Rückschau auf bestehende Verifikationspfade

FOKUS: Abschlussbehauptungen gegen die tatsächlich ausführenden Guards prüfen

## Gegenstand und Ergebnis

Die Rückschau setzt auf den ursprünglichen Pilot-Commit
`cfa5797dfad75758ed80a9ce751e5556ed0ce086` auf; dessen Repository-Basis ist
`05712d827b5558b595438f38a1e3c7fc739a297f`. Geprüft wurden der PR-Fokus-Guard,
der Testsammeljob, die HMAC-Verfügbarkeit, Checkout-Verbraucher sowie zugehörige
Abschlussmeldungen und Dokumentation. Das ist keine vollständige Sicherheitsprüfung
aller Anwendungen und Abhängigkeiten.

Zwei reproduzierte Implementierungslücken sind korrigiert: Der Workflow übersetzte
fehlende FOKUS-Marker und Rückfragen in erfolgreiche Warnungen; der Textprüfer
prüfte nur den ersten unnummerierten Fokuswechsel. Jetzt bleiben Regelverstöße und
Ausführungsfehler Fehler. Jeder dokumentierte, auch nummerierte Wechsel braucht
seine eigene Frage vor dem nächsten Marker, spätestens in fünf Folgezeilen.
Die erneute Codex-Review am Folge-Head fand einen berechtigten Randfall: Das
auskommentierte Wechsel-Beispiel der echten PR-Vorlage wurde mitgeprüft. Die
Gegenprobe reproduzierte dies. HTML-Kommentare werden nun ausgeblendet, ihre
Zeilengrenzen bleiben erhalten; ein Fokuswert muss in derselben Zeile sichtbar sein.

Der Skill ist über AGENTS.md in die Repository-Arbeitsanweisungen eingebunden.
Das schafft eine Arbeitsregel für Agenten, die diese Anweisungen lesen; die
Einhaltung durch jeden Agenten wird dadurch nicht maschinell bewiesen. Die
FOKUS-Textprüfung belegt ihrerseits keine tatsächlich erteilte Zustimmung.

## Belegte Gegenproben

Die neuen Tests führen die echten Shell-Fragmente der Workflows mit Bash
`-e -o pipefail` aus und verwenden den echten Textprüfer. Der erste Lauf gegen den
unveränderten Stand ergab **6 fehlgeschlagene und 20 bestandene Tests**. Nach dem
Fix bestehen alle **26**. Der Fehler wurde damit vor der Korrektur reproduziert.
Sechs weitere Vorlagen-/Kommentar-Fälle ergaben vor dem Nachfix **3 failed,
29 passed**; danach bestehen alle **32** Guard-Vertragstests.

| Pfad | Geprüfte Fälle | Ergebnis |
|---|---|---|
| PR-Fokus-Guard | Sechs Regelverletzungen, drei gültige Texte, fehlender Prüfer, sechs Vorlagen-/Kommentar-Fälle | Ungültig und Ausführungsfehler scheitern; ausgefüllte Vorlage besteht |
| All Tests Pass | Drei Unterjobs, jeweils failure/skipped/cancelled/leeres Ergebnis; alle success | Alle zwölf nicht erfolgreichen Kombinationen scheitern; Erfolg besteht |
| HMAC-Verfügbarkeit | PR-Ausnahme ohne Schlüssel; vertrauenswürdiger Lauf ohne Schlüssel; synthetischer Schlüssel | Expliziter unsigned skip; Fehler; Schlüssel verfügbar |

Der Sammeljob und die HMAC-Verfügbarkeitslogik waren bereits korrekt; sie wurden
nicht gelockert. Die Gegenproben verwenden keinen produktiven Schlüssel und
führen keine Release- oder Issue-Erstellung aus.

Lokal mit frisch eingerichteter, gesperrter dev-Umgebung, uv **0.12.18** und Python
**3.12.14** ausgeführt:

- `make verify verify-governance` nach dem Vorlagen-Nachfix: Exit 0; **1176 passed, 2 skipped,
  169 subtests passed**; 16 Workflow-Verträge und 22 VOID-Spiegel konsistent.
- Ruff, Black, mypy und konfigurierter Bandit-Lauf: Exit 0. Die vorhandenen
  Bandit-Ausschlüsse bleiben erhalten; das ist kein grenzenloser SAST-Nachweis.
- Nach den abschließenden Dokumentations-/Kommentarkorrekturen: gezielte
  Guard-/Pipeline-Tests, Governance-Prüfung, Dokumentverweise und Whitespace.

Die Quelldigests, Befehle und Ergebnisse stehen in der
[Zusammenfassung](evidence/2026-11-03_verification_closure/summary.json).
Remote-CI und Reviews müssen am später veröffentlichten Head gelesen werden;
der ursprüngliche Codex-Kommentar am Pilot-Head bestätigt diese Folgeänderung nicht.

## Echter Desktop-Lauf statt Sammeljob-Schlussfolgerung

Am ersten Folge-Head `e5a3e916aacc84903d1c7ce69830b7866f97b296` bestanden die
fünf Pflichtchecks und die Runtime-Matrix. Der zusätzlich angestoßene
[AppImage-Lauf](https://github.com/fleksible/entaENGELment-/actions/runs/41736357077)
scheiterte trotzdem: Im voreingestellten Node-Debugger-Kontext war
`process.resourcesPath` undefiniert. Paketinstallation, Build und Extraktion
hatten bestanden; die Assertions über den echten Renderer waren noch nicht erreicht.
Das ist ein Fehler des Prüfskripts, kein beobachteter Sandbox-Ausbruch.

Der Nachfix aktiviert die Runtime-Kontextmeldungen und wählt ausdrücklich einen
initialisierten Electron-Hauptprozess-Kontext (`type: browser` mit Ressourcenpfad),
bevor die bestehenden Assertions laufen. Drei JS-Gegenproben prüfen den falschen
Node-/Renderer-Kontext, noch fehlende Initialisierung und einen inzwischen zerstörten
Kontext. Die Sandbox-, Preload-, Prozess- und Navigationsprüfungen bleiben erhalten.
Ein erfolgreicher echter AppImage-Lauf am veröffentlichten Folge-Head ist weiterhin
der notwendige Funktionsnachweis; die kleinen Kontextproben ersetzen ihn nicht.

## Checkout-Härtung und erhaltener Scannerbefund

Alle **25 Checkout-Schritte in 16 Workflows** setzen nun
`persist-credentials: false`. Die gelesenen Workflow-Befehle, aufgerufenen Skripte
und Paket-Einstiegspunkte brauchen nach dem Checkout keine authentifizierten
git-Schreibzugriffe. Release-Erstellung und VOID-Issues nutzen ihre eigenen
begrenzten API-/Action-Credentials. Das separat vorhandene
`scripts/branch_cleanup.sh` wird von diesen Workflows nicht aufgerufen.

Der Vergleichslauf nutzt zizmor **1.32.0**, offline, strikte Erfassung, JSON-v1
und genau dieselben **17 Eingaben** wie der ursprüngliche Pilot:

| Regel | Vorher | Nachher | Entscheidung |
|---|---:|---:|---|
| artipacked | 25 | 0 | Unnötige Persistierung entfernt |
| github-env | 1 | 1 | Befund erhalten; feste lokale venv-Pfadänderung, keine nachgewiesene Angreiferkette |
| self-repository | 15 | 15 | Befunde erhalten; Syntaxmigration braucht eigenen Kompatibilitätsnachweis |
| Gesamt | 41 | 16 | Gleiche Erfassung; Exit 14 bleibt Befundausgabe |

[Erhaltene Befunde](evidence/2026-11-03_verification_closure/findings.json).
Es gibt keine neue Scanner-Unterdrückung und keinen neuen zizmor-Pflichtcheck.
Ein zusätzlicher Scan des ganzen Checkouts erfasst auch Dependabot und liefert
drei weitere `dependabot-cooldown`-Empfehlungen, insgesamt 19 Hinweise. Diese drei
gehören nicht zum Vergleich der 17 Eingaben. Eine pauschale Verzögerung von
Updates wird daraus nicht abgeleitet; das wäre eine eigene Update-Policy-Entscheidung.

Tag-Release und geplanter VOID-Monitor wurden statisch auf die Credential-Nutzung
geprüft. PR-CI kann deren extern schreibende Ereignisse nicht bestätigen; ein
Test-Release oder eine Test-Issue wurde dafür nicht erzeugt.

## Dokumentation und kleinste Entscheidung

Die Workflow-Karte nennt jetzt die tatsächliche Runtime-Matrix Python 3.10–3.14,
den JS/TS-Testschritt, die bereits erfolgte Lock-Umstellung von Release/VOID und
den blockierenden PR-Fokus-Guard. CLAUDE.md unterscheidet ausdrücklich erlaubten
PR-Skip von fehlendem HMAC-Schlüssel in vertrauenswürdigen Läufen. `make all`
meldet nur die ausgeführten Kernprüfungen und den Snapshot. Die mitgegebenen
Statuszahlen sind Beispielwerte; eine gültige HMAC-Signatur macht daraus keine
gemessenen oder fachlich bestätigten Werte.

Kleinste technische Entscheidung: die gezielten Guard-Korrekturen und Härtung
nach erfolgreicher CI am neuen Head übernehmen. Die 16 verbleibenden
Scannerhinweise sind begrenzt eingeordnet und bleiben für gesonderte Prüfung
sichtbar. Eine bestandene Prüfung erteilt kein zusätzliches Merge-Mandat.

## Übermittelte Claude-Gegenprüfung, 4. November 2026

Der Nutzer übermittelte einen Claude-Review des ursprünglichen Pilotstands auf
`main@05712d8`. Er berichtet einen eigenen Werkzeuglauf in einer zweiten Umgebung;
dessen Originalprotokoll liegt dieser Prüfung nicht bei. Die folgende Zuordnung
trennt diesen Bericht vom selbst gelesenen PR-Stand `77cf219` und den anschließend
selbst ausgeführten Scans.

| Hinweis | Abgleich und Korrektur |
|---|---|
| Icon fehlt | Bestätigt: Die portable Kopie enthielt zwei Asset-Verweise ohne Datei. Das bereits vorhandene Icon der persönlichen Fassung ist nun beigefügt. |
| Dependabot fehlt in 17 Eingaben | Bestätigt und bereits als zusätzlicher Scope in der Rückschau benannt. Die Anleitung fordert jetzt auch Dependabot-Konfigurationen und die Offenlegung bewusst ausgelassener Eingaben. |
| stderr muss nicht leer sein | Formulierung auf fehlende Fehlermeldungen begrenzt. Die beiden eigenen Vergleichsläufe hatten tatsächlich null stderr-Bytes; reine Fortschrittsausgabe in einer anderen Umgebung widerspricht dem nicht. |
| Fokus- und HMAC-Widersprüche in CLAUDE.md | Am aktuellen PR-Head bereits korrigiert: Der PR-Fokus-Guard blockiert; PR-Signing-Skip und Abbruch ohne Schlüssel außerhalb eines PRs sind getrennt beschrieben. Der Commit-Hinweis bleibt advisory. |
| Claude lädt `.agents/skills/` nicht als Projekt-Skill | Ein kleiner Einstieg unter `.claude/skills/verify-project-evidence/` verweist nun auf den zentralen Ablauf; CLAUDE.md nennt ihn. Es entsteht keine zweite inhaltliche Fassung. |

Selbst wiederholt mit zizmor 1.32.0, offline und strikter Erfassung: automatische
Erfassung von **18 GitHub-Konfigurationsdateien** ergibt am ursprünglichen
`main@05712d8` **44 Hinweise**, am gehärteten Stand **19 Hinweise**, jeweils
Exit 14. Je drei `dependabot-cooldown`-Hinweise erklären die Differenz zu den
engeren 17-Datei-Läufen mit 41 beziehungsweise 16 Hinweisen. An der Entfernung
der 25 Credential-Persistierungs-Hinweise ändert diese Scope-Erweiterung nichts.

[Vergleichsnachweis und zusätzliche Fundstellen](evidence/2026-11-04_review_followup.json).
Die [offizielle Claude-Code-Dokumentation](https://code.claude.com/docs/en/skills)
beschreibt `.claude/skills/<name>/SKILL.md` als Projektpfad. Geprüft wurden die
Frontmatter-Struktur, alle Verweise und die gemeinsame Quelle. Ein nativer
Claude-Code-Aufruf wurde hier nicht ausgeführt; Auffindbarkeit gemäß Dokumentation
ist keine Garantie tatsächlicher Anwendung in jeder Sitzung.
