# ADR-0006: Rollenaufteilung und delegierte Technikentscheidungen

- **Status:** Accepted mit dem Merge unter dem Mandat vom 2026-11-04 (siehe D10)
- **Datum:** 2026-11-04
- **Kontext-Fokus:** Abschluss offener Human Decisions aus der Repo-Analyse vom 2026-07-29
- **Herkunft:** Rollenaussage von Kevin/Fleks im Chat mit der Claude-Prüfinstanz (2026-11-03/04);
  Arbeitsvereinbarung [Menschliche Absicht und technische Merge-Prüfung](../annex/MERGE_INTENT_DELEGATION_v0_1.md)
  (PR #451); Prüfung von PR #452; Live-Abfrage der Repository-Einstellungen am 2026-11-04
- **Entscheidung durch:** D1 Kevin/Fleks (eigene Rollenaussage); D2–D8 Claude-Prüfinstanz unter D1;
  D9 bleibt bei Kevin/Fleks; D10 Mandat von Kevin/Fleks

## Context

Die Human Decisions der Repo-Analyse vom 2026-07-29 (HD-REL-1, HD-LOCK-1, HD-MET-1,
HD-EVB-1, HD-WIP-1) wurden nur im Chat geführt; im Repository waren sie bis heute nicht
abgelegt. Mehrere davon waren als Technikfragen formuliert und damit für den Owner nicht
sinnvoll entscheidbar. PR #452 hat zusätzlich drei Entscheidungen gebündelt (blockierender
Fokus-Guard, Dependabot-Folge, gelockerte Verify-Formulierung in CLAUDE.md).

Kevin/Fleks hat seine Rolle so beschrieben: Architektur und Umsetzung liegen bei den
KI-Instanzen; seine Entscheidungen betreffen relationale, ethische und ästhetische
Rückfragen. Technische Fragen soll ihm keine Instanz zur Entscheidung vorlegen.

## Decision

### D1 Rollenaufteilung

Der Rahmen steht in der Arbeitsvereinbarung
[Menschliche Absicht und technische Merge-Prüfung](../annex/MERGE_INTENT_DELEGATION_v0_1.md).
Diese ADR wendet ihn an und wiederholt ihn nicht:

1. Kevin/Fleks entscheidet Fragen der Essenz, des Consent, der geschützten Herkunft
   (inkl. VOID-META-013) sowie relationale, ethische und ästhetische Fragen.
2. Technische Fragen entscheiden die Agenten selbst. Jede solche Entscheidung nennt eine
   Gegenprobe, an der sie scheitern kann. Kevin/Fleks kann jede davon zurücknehmen (G0:
   Consent ist widerrufbar).
3. Agenten dürfen auf PR-Zweige committen. Nach `main` übernehmen sie nur mit einem
   ausdrücklichen, begrenzten Mandat (§3 der Arbeitsvereinbarung). Technisch erzwungen
   ist nur der PR-Weg (0 erforderliche Freigaben, siehe Belege).

### D2 Fokus-Guard blockiert (HD-MET-1)

Der PR-Fokus-Guard lässt fehlende `FOKUS:`-Marker und fehlende Rückfragen scheitern.
Das ist keine neue Wertentscheidung: AGENTS.md (G4) und CLAUDE.md („PR-Body muss
`FOKUS:` tragen") enthielten die Regel bereits; PR #452 bringt den Code in Übereinstimmung.
**Gegenprobe:** Ein PR-Text ohne `FOKUS:` wird rot (Vertragstests in
`tests/test_ci_guard_contracts.py`).

### D3 Dependabot-PRs werden am Titel geprüft (HD-DEP-1)

„Check PR for FOKUS marker" ist ein Pflichtcheck, der auch für Admins gilt. Dependabot
schreibt seinen PR-Text selbst; das konfigurierte Präfix `FOKUS: deps` steht nur im Titel.
Ohne Ausnahme könnte nach dem Blockieren niemand mehr einen Dependabot-PR mergen.
Für PRs von `dependabot[bot]` liest der Guard deshalb den Titel; für alle anderen Autoren
zählt nur der PR-Text. **Gegenprobe:** Der erste Dependabot-PR nach dem Merge besteht den
Guard; ein menschlicher PR mit `FOKUS:` nur im Titel scheitert weiterhin.

### D4 Verify-Formulierung (HD-VERIFY-1)

`make verify` bleibt der Kernprüflauf. Vorhandene Nachweise dürfen weiterverwendet werden,
solange Stand, Voraussetzungen und Aussageumfang passen (CLAUDE.md in PR #452).
**Gegenprobe:** Jede Abschlussaussage nennt geprüften Stand und Umfang
(Skill `verify-project-evidence`).

### D5 Python-Lock (HD-LOCK-1): erledigt

Faktisch umgesetzt: `uv.lock` liegt im Repository-Wurzelverzeichnis, die Workflows
installieren daraus gesperrt. Hier nur nachträglich festgehalten.

### D6 Release-Gate ruht (HD-REL-1)

Auf `origin` existiert kein Tag (Abfrage 2026-11-04); `release.yml` wurde nie ausgelöst.
Seine Prüfliste weicht von `make verify-all` ab. Keine Änderung jetzt.
**Vor dem ersten `v*`-Tag:** Release-Prüfungen an `make verify-all` angleichen.

### D7 Evidence-Bundle bleibt flüchtig (HD-EVB-1)

`ci-evidence-bundle.yml` erzeugt bei jedem Push Prüfsummen und eine Provenienzdatei
(`validation=NOT_ASSERTED`) und bewahrt das Artefakt 14 Tage auf. Es gilt als
CI-Zwischenbeleg, nicht als dauerhafter Nachweis. Keine Änderung.

### D8 Dependabot-Wartezeit zurückgestellt

Die drei zizmor-Hinweise `dependabot-cooldown` bleiben offen und sichtbar. Eine Wartezeit
wird als eigene Änderung geprüft, wenn `.github/dependabot.yml` ohnehin angefasst wird.

### D9 Gewichtung der VOIDs bleibt beim Owner (HD-WIP-1)

Elf VOIDs sind aktiv, zehn davon `high`. Welche Fäden des Frameworks jetzt Vorrang haben,
ist eine Frage der Essenz. Agenten ändern Prioritäten nicht.

### D10 Merge-Mandat vom 2026-11-04

Kevin/Fleks hat die Claude-Prüfinstanz am 2026-11-04 im Chat beauftragt, die offenen PRs
zu mergen, sofern sie in der Essenz passen.

- **Gegenstand:** die an diesem Tag offenen PRs.
- **Grenze „Essenz":** Hausregeln G0–G6, keine Änderung an GOLD, NICHTRAUM oder Receipts
  ohne eigene Freigabe, Claim-Disziplin ohne Statuspromotion, Consent, geschützte Herkunft,
  VOID-META-013.
- **Technische Voraussetzung:** alle fünf Pflichtchecks am aktuellen Head grün, PR mergebar.
- **Nicht umfasst:** Entwürfe, PRs mit roten Prüfungen, offene inhaltliche Modellentscheidungen.

Einstufung zum Zeitpunkt der Entscheidung:

| PR | Einstufung | Grund |
|---|---|---|
| #451, #452, #453, #437, #443 | Übernahme | Grün, ANNEX-/Workflow-Pfade, kein GOLD; Inhalt deckt sich mit den Hausregeln |
| #445–#449 | Übernahme, einzeln nacheinander | Dependabot-Patch-/Minor-Updates (npm), grün |
| #444, #450 | Zurückgestellt | Rot: bekannte Drift der uv-Exporte; laut `.github/dependabot.yml` manuell zu ersetzen |
| #423 | Nicht umfasst | Entwurf mit offener Modellentscheidung |

Jeder Merge-Commit nennt dieses Mandat.

## Belege: Repository-Einstellungen (live_api, 2026-11-04, nur gelesen)

| Einstellung | Wert |
|---|---|
| Branch-Schutz `main` | aktiv (klassisch), `enforce_admins: true`, keine Rulesets |
| Pflichtchecks | `deepjump-audit / deepjump-audit`, `Verify Pointers & Lint (blocking)`, `All Tests Pass`, `Lint · Format · Types · SAST`, `Check PR for FOKUS marker` |
| Aktueller Stand vor Merge erforderlich | nein (`strict: false`) |
| Erforderliche Freigaben | 0 |
| Force-Push / Löschen von `main` | nicht erlaubt |
| CodeQL | Default Setup `configured` seit 2026-07-21, wöchentlich; Sprachen laut API: actions, c-cpp, javascript, javascript-typescript, python, typescript |
| Private Vulnerability Reporting | aktiv |

Damit sind die in der Repo-Analyse vom 2026-07-29 offenen Punkte „Required Checks",
„CodeQL" und „Private Vulnerability Reporting" belegt. Der Code-Scanning-Teil von
ADR-0003 ist über das Default Setup umgesetzt.

## Consequences

- (+) Entscheidungen sind im Repository abgelegt statt nur im Chat.
- (+) Der Owner bekommt nur noch Fragen aus seinem Bereich vorgelegt.
- (+) Jede delegierte Entscheidung hat eine Gegenprobe und ist widerrufbar.
- (−) Mehr Entscheidungsgewicht liegt bei Agenten; ihre Begründungen müssen im PR lesbar sein.
- (−) Die Einstellungen sind ein Stand vom 2026-11-04 und können sich ändern.

## Grenzen

- Die Dependabot-Annahme (D3) ist mit dem echten Text eines Dependabot-Commits von `main`
  geprüft, nicht mit einem echten Dependabot-PR-Text.
- Die Einstellungen wurden über die GitHub-API gelesen; die Oberfläche wurde nicht geprüft.
- Diese ADR ändert keine Workflows. D3 ist in PR #452 umgesetzt.
