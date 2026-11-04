---
artifact_role: generated_review
status: DERIVED / REVIEW-PENDING
observed_date: 2026-11-03
promotion_effect: none
evidence_import: excluded_self
---

# Verifikationsskill und lokaler zizmor-Pilot

FOKUS: belastbare Abschlussaussagen und begrenzter Workflow-Scan

Dieser Bericht erhält den ursprünglichen Pilotstand am Commit
`cfa5797dfad75758ed80a9ce751e5556ed0ce086`; seine Aussagen über den damaligen
Änderungsscope sind historisch. Die anschließenden Guard-Korrekturen,
Credential-Härtung und neuen Prüfbelege stehen in der
[Rückschau](2026-11-03_verification_workflow_closure.md).

## Ergebnis

Der eigenständig formulierte Skill `verify-project-evidence` ordnet Nachweise einer
konkreten Version, ihrem Umfang und ihrer Herkunft zu. Er trennt technische
Schlussfolgerung und gedeckte Handlung, erlaubt passende ältere Belege und
begrenzte Teilprüfungen und verlangt keine Aufrufzeremonie vor jeder Antwort.

Die persönliche Fassung wurde validiert und dauerhaft bereitgestellt. Die drei
Dateien unter `.agents/skills/verify-project-evidence/` sind die portable
Repository-Fassung desselben Ablaufs. Eine vorhandene SKILL.md beweist weder
automatische Ladung durch jeden Agenten noch technische Durchsetzung.

Der lokale zizmor-Lauf hat **41 Hinweise aus drei Regeln** geliefert. Das sind
keine 41 nachgewiesenen ausnutzbaren Schwachstellen. Die Hinweise werden nicht
unterdrückt, automatisch behoben oder zu einem neuen CI-Gate gemacht.

## Prüfgegenstand und Reproduzierbarkeit

- Repository: `fleksible/entaENGELment-`.
- Basis: `05712d827b5558b595438f38a1e3c7fc739a297f`.
- zizmor: `1.32.0`, offizielle Veröffentlichung
  https://github.com/zizmorcore/zizmor/releases/tag/v1.32.0.
- 16 Workflows und eine lokale Action explizit als 17 Eingaben übergeben.
- 18 materialisierte Quelldateien einschließlich AGENTS.md gegen ihre Git-Blob-IDs
  geprüft; keine Abweichungen. Pfade und IDs stehen im Snapshot.
- Offline, `--strict-collection`, JSON-v1, reguläre Standardregeln.
- Scanner-Exit-Code: **14**; JSON mit 41 Befunden, keine Fehlermeldungen auf stderr.
  Kein Parseabbruch des Repository-Laufs. Der Exit-Code wird als Befundausgabe erhalten.
- Keine Online-Audits, keine extern referenzierten Skripte, keine installierten
  Abhängigkeiten und keine laufenden GitHub-Jobs durch diesen Scan geprüft.

Laufmuster mit allen 17 expliziten Dateipfaden statt einer impliziten Auswahl:

```bash
uv tool run --offline --from zizmor==1.32.0 zizmor \
  --offline --strict-collection --format=json-v1 <17 Dateipfade>
```

Die Toolbereitstellung fand vor dem eigentlichen Offline-Lauf statt. Im
veröffentlichten JSON wurden ausschließlich absolute `Local.verbatim_path`-Werte
auf den Snapshot relativiert. Quellzeilen sind im JSON nullbasiert; die Tabelle
weiter unten verwendet einsbasierte Zeilen. Der SHA-256 des unveränderten
Scanner-stdout steht in der Zusammenfassung.

[Zusammenfassung](evidence/2026-11-03_zizmor/summary.json) ·
[Snapshot](evidence/2026-11-03_zizmor/snapshot.json) ·
[Befunde](evidence/2026-11-03_zizmor/findings.json)

## Einordnung der drei Muster

| Regel | Anzahl | Tool-Einstufung | Eigene begrenzte Einordnung |
|---|---:|---|---|
| github-env | 1 | High, Low confidence | Die lokale Python-Action erweitert GITHUB_PATH um die virtuelle Umgebung. Eine Pfadänderung ist belegt; eine Angreiferkette ist damit nicht belegt. |
| artipacked | 25 | Medium, Low confidence | Checkout-Schritte lassen persistierte Git-Zugangsdaten eingeschaltet. Das ist ein begründeter Härtungskandidat, kein Nachweis eines Credential-Leaks. |
| self-repository | 15 | Low, High confidence | Lokale Verweise verwenden die Workspace-Syntax. Die neuere Self-Repository-Syntax ist ein begrenzter Verbesserungskandidat mit eigenem Kompatibilitätsnachweis. |

### Pfadänderung

Anker: [.github/actions/python-locked/action.yml:18](../../.github/actions/python-locked/action.yml#L18).

Der gelesene Schritt schreibt `$PWD/.venv/bin` nach GITHUB_PATH, nachdem
`tools/python_lock.py sync` die Umgebung einrichtet. Der Text enthält keine
direkte Übernahme eines Issue-Titels oder PR-Kommentars in diesen Wert.
Unter den 16 gelesenen Workflow-Definitionen sind keine
`pull_request_target`- oder `workflow_run`-Trigger deklariert.

Das reduziert die Aussagekraft des pauschalen High-Hinweises für diesen Stand.
Nicht untersucht wurden alle möglichen späteren Aufrufer, Runner-Innereien oder
ein praktisch ausführbarer Angriff. Deshalb weder pauschaler Entwarnungsbeleg
noch bestätigte ausnutzbare Schwachstelle. Ein Wechsel zu direkten Aufrufen des
Umgebungsinterpreters wäre ein eigener, gezielt zu prüfender Workflow-Fix.

### Persistierte Zugangsdaten

Alle 25 Hinweise sind Low-confidence-Feststellungen zu fehlendem
`persist-credentials: false`. zizmor dokumentiert für Checkout ab v6 die Ablage
unter RUNNER_TEMP statt direkt in .git/config. Ein tatsächlicher Upload dieser
Zugangsdaten wurde hier nicht nachgewiesen.

In den 16 Workflow-Definitionen wurde kein direkter git-push-, git-commit- oder
git-tag-Befehl gefunden. Indirekt ausgeführte Skripte sind damit nicht beurteilt.
Kleinster Folgefix: nur nach Prüfung des jeweiligen Jobs die unnötige
Persistierung abschalten und dessen wirklichen Ablauf gegentesten.

### Lokale Action-Verweise

Die 15 Befunde empfehlen den Wechsel von `./...` zu `$/...`. Laut
zizmor-Dokumentation bindet die neue Form an das Repository statt an den
veränderlichen Workspace und unterstützt GitHubs Pinning-Policy.
Das ist keine Aussage über einen bereits erfolgten Austausch einer Action.
Ein späterer Wechsel braucht einen realen CI-Kompatibilitätslauf.

## Ausgeführte Gegenproben

| Prüfung | Ergebnis | Reichweite |
|---|---|---|
| Skill-Strukturvalidator | erfolgreich | Frontmatter und Grundstruktur; kein universeller Verhaltensnachweis |
| Frischer lesender Agent, drei feste Fälle | 3/3 zentrale Unterscheidungen erhalten | Ein Durchlauf; kleine gezielte Beispiele |
| zizmor, absichtlich gefährliche Texteingabe | Exit 14, template-injection erkannt | Erkennung dieses Kontrollmusters |
| zizmor, syntaktisch defektes YAML | Exit 1 | Strikte Erfassung lässt Parsefehler nicht als sauberen Scan erscheinen |
| zizmor, unauffällige Kontroll-Definition | Exit 0, keine Befunde | Kein generelles Fehlerschlagen jeder Eingabe |

Der frische Agent erhielt nur den Skill und drei kleine Leseartefakte:
einen PR-Abschlussdatensatz, einen abgebrochenen Installationslauf und einen
Whitespace-Befund. Er erhielt keine erwarteten Ergebnisse oder Diagnose.
Seine Antworten trennten jeweils technischen Stand und Mandat, nicht gestartete
und fehlgeschlagene Tests sowie Formatbefund und Funktionsfehler.
Die Ausschnitte ersetzen keine erneute Vollprüfung der zugrunde liegenden PRs.

Es wurde kein neuer vollständiger `make verify`-Lauf lokal ausgeführt. Die
Repository-Änderung enthält ausschließlich Agentenanweisungen und Prüfberichte.
Der Scan ist ein bewusst lokaler Pilot mit erhaltenen Befunden.

## Quellen und Grenzen

- https://docs.zizmor.sh/audits/#github-env
- https://docs.zizmor.sh/audits/#artipacked
- https://docs.zizmor.sh/audits/#self-repository
- https://docs.zizmor.sh/usage/
- Gepinnte Quelldateien und Befundpositionen im beigefügten Snapshot/JSON.

Die drei Regeln und die oben angeführten Dokumentationsteile wurden gelesen.
Toolschweregrad, Vertrauensgrad, eigene Einordnung und menschliche Entscheidung
bleiben getrennt. Der Bericht ist ein generated_review und keine unabhängige
Wiederholungsbestätigung seiner eigenen Quellen.
