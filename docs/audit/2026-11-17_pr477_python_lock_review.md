# PR #477 — Python-Lock, Messung und Auditpfade

Prüfdatum: 2026-11-17 (Europe/Berlin). Technischer Review durch den Coding-Agenten.
Mandat: Prüfung, notwendige Ausbesserung und Übernahme dieses Dependency-PRs bei
tragfähigen Nachweisen ausdrücklich delegiert.

## Ergebnis

**Lock-Drift repariert und lokal geprüft; Merge bleibt HOLD wegen des aktuellen
repositoryweiten JS-High-Audits.** Die ursprünglichen Python-CI-Fehler sind
Installationsabbrüche vor Beginn der Tests und des Audits, keine nachgewiesene
Coverage-Regression. Der korrigierte Stand benötigt CI am endgültigen Head.

- PR: <https://github.com/fleksible/entaENGELment-/pull/477>.
- Basis: `b4ad2a01a87871457d07704bb12d194c784c2bd4`.
- Ursprünglicher Head: `1ebc01636781575f0c67c9dfa3efa4fb381f0527`.
- Ursprünglicher CI-Merge: `1ded05d33943e56283416883651b96c5dbf1ff30`.
- Korrigierter `uv.lock`, SHA-256:
  `e06261793b9da53e5834def9db52f5f271ea179b603a8f4bb14ccf4fc9f1d41c`.

## Exakter Diff und Reparatur

| Datei im ursprünglichen PR | Änderung der Versionspins |
| --- | --- |
| `requirements-test.txt` | coverage 7.17.2 -> 7.17.3, zugehörige Distributions-Hashes |
| `requirements-dev.txt` | coverage 7.17.2 -> 7.17.3; stevedore 5.9.1 -> 5.10.0; Hashes |
| `Fractalsense/requirements-dev.txt` | coverage 7.17.2 -> 7.17.3, Distributions-Hashes |

`uv.lock` blieb im ursprünglichen PR unverändert. Die zum geprüften Stand
gehörende `tools/python_lock.py` bezeichnet jedoch den Root-Lock als maßgebliche
Quelle und vergleicht alle Requirements-Exporte bytegenau vor jedem Sync.
`requirements.txt` und die Runtime-Paketversionen werden durch #477 nicht geändert.

Der Fehler wurde mit dem vorgeschriebenen uv 0.12.18 lokal reproduziert:

```text
FAIL: Generated requirements drift: requirements-test.txt, requirements-dev.txt, Fractalsense/requirements-dev.txt
```

Anschließend wurde ausschließlich der Root-Lock gezielt aktualisiert:

```sh
uv lock --upgrade-package 'coverage==7.17.3' --upgrade-package 'stevedore==5.10.0'
python tools/python_lock.py export
python tools/python_lock.py check
```

Alle Befehle verwenden uv 0.12.18. Der neue Lock enthält weiterhin 86
Paketdatensätze. Alle anderen Datensätze sowie die Top-Level-Metadaten sind
strukturell exakt gleich. Die neu generierten Requirements sind bytegleich mit
den bereits im PR enthaltenen Exporten. Die notwendige Codekorrektur ist somit
ein zusätzlich geänderter `uv.lock`; daneben kommt nur dieser Auditbericht hinzu.
Die Archivkopie unter `NICHTRAUM/archive/uv.lock` bleibt unangetastet.

## Tatsächliche Nutzung und Wirkungsgrenzen

`coverage` wird transitiv durch pytest-cov 7.1.0 benutzt. Aktive Pfade sind
`make coverage`, Fractalsense-CI mit XML-/HTML-Reports und die vollständige
Legacy-CI mit XML-/Terminal-Report und `coverage report --fail-under=50`.
Die Legacy-Build-Jobs laufen auf PRs nicht; ihr grüner Advisory-Ersatz ist kein
Coverage-Nachweis. `make verify` führt Core-Tests und Guards aus, aktiviert für
sich genommen aber keine Coverage-Messung.

`pyproject.toml` misst `src` und `tools`; im gelesenen Konfigurationsstand sind
Branch-Messung, parallele Messung und zusätzliche `fork`-/`subprocess`-Patches
nicht aktiviert. Es gibt keinen gefundenen Projektkonsumenten von
`coverage.json` oder dessen Funktionsschlüsseln. Subprozesse in Tests allein
belegen keine aktivierte Subprozess-Messung.

Die [Coverage-Änderungshistorie 7.17.3](https://coverage.readthedocs.io/en/7.17.3/changes.html)
nennt veränderte Fork-/Subprozess-Erfassung, JSON-Namensdisambiguierung und den
Umgang mit verschwindenden parallelen Datenfiles. Das sind Änderungen des
Mess-/Reportwerkzeugs. Sie ändern keine Projekt-Governance oder normative
Entscheidung und sind nicht mit zusätzlicher wissenschaftlicher Validierung
gleichzusetzen. Die konkrete JSON-Änderung wurde unten nachgestellt; die hier
nicht konfigurierten Fork-/SIGINT-/Race-Sonderfälle wurden nicht eigens simuliert.

`stevedore` ist über Bandit 1.9.4 in den Dev-/Auditgruppen erreichbar, also für
die Erkennung der Scanner-Plugins relevant. Fehlende eigene Imports wären kein
Ausschluss dieser Nutzung. Die installierte Version 5.10.0 verlangt Python
>=3.11 und passt damit zum vorhandenen Projekt-Floor. Ihr Lauf wurde an Code und
einem kontrollierten positiven Scannerbefund überprüft.

## Eigenständig ausgeführte Nachtests

Umgebung: Linux, CPython 3.11.18, uv 0.12.18; separate aus dem korrigierten Lock
installierte Dev-, Fractalsense- und Audit-Umgebungen. Die Paketprüfungen melden
kompatible Installationen. Diese lokalen Ergebnisse werden nicht als selbst
ausgeführte Python-3.12/3.13/3.14-Tests ausgegeben.

| Prüfung | Beobachtung |
| --- | --- |
| Originaler `python tools/python_lock.py check` | Exit 1, Drift der drei Exportdateien reproduziert |
| Korrigierter Export und `check` | Exit 0; vorhandene PR-Exporte unverändert reproduziert |
| `make verify` | Exit 0; 1285 Tests und 200 Subtests bestanden, 2 DataLad-Integrationstests übersprungen; Port-/Claim-Guards und Core-Pointer gültig, 4 optionale Output-Pointer fehlen |
| Core-Suite zusätzlich mit pytest-cov und XML/HTML/JSON | Exit 0; 1285 Tests und 200 Subtests bestanden, dieselben 2 Skips; 51 erfasste Dateien, 4873/6448 Statements = 75,57 % (Terminal rundet auf 76 %) |
| `coverage report --fail-under=50` | Exit 0; bestehende Schwelle unverändert erfüllt |
| Fractalsense-Suite mit XML/HTML-Coverage | Exit 0; 184 Tests bestanden; 235 Warnungen wegen wiederholter Registrierung von fünf Matplotlib-Colormaps, keine Testfehler |
| Isolierte Getter-/Setter-Probe, coverage 7.17.2 gegen 7.17.3 | Beide messen dieselben 12/12 Statements; JSON ergänzt erwartungsgemäß `Box.value@10`, statt einen gleichnamigen Eintrag zu verlieren; XML/HTML/JSON-Erzeugung jeweils Exit 0 |
| `bandit -c .bandit.yaml -r src/ tools/` | Exit 0; 11672 Codezeilen erfasst, keine Findings oder Scannerfehler; bestehende Skip-Regeln bleiben in Kraft |
| Kontrollierte Scannerprobe mit `eval(input())` | Erwarteter Exit 1, B307 mit mittlerer Schwere/hoher Konfidenz; keine Scannerfehler. Die Probe wird nicht ausgeführt und nicht als Produktcode übernommen |
| `python tools/python_lock.py audit` | Exit 0; alle 85 exportierten gelockten Paketversionen geprüft, keine bekannten Python-Abhängigkeitslücken zum Prüfzeitpunkt |
| `git diff --check` | Exit 0 |

Die Getter-/Setter-Probe belegt den beabsichtigten Report-Unterschied, nicht die
vollständige Gleichheit aller denkbaren Messungen. Der positive Bandit-Gegenfall
begrenzt die Aussage eines ansonsten befundfreien Scannerlaufs. Neue
Environment-Receipts beziehen sich auf den neuen Lock-Digest; vorhandene
unveränderliche Projekt-Receipts und Schwellen wurden nicht verändert.

## CI-/Review-Belege und verbleibender Blocker

Am ursprünglichen Head gab es keine Review-Submission und keine Inline-Threads.
Die angeforderte Review allein ist keine technische Freigabe. Direkt gelesene
Logs zeigen den identischen Export-Drift vor den eigentlichen Arbeitsschritten:

- [Frische Locked-Umgebung](https://github.com/fleksible/entaENGELment-/actions/runs/43797262986/job/133068790269).
- [Python-3.12-Tests](https://github.com/fleksible/entaENGELment-/actions/runs/43797263103/job/133068790175).
- [Python-Audit](https://github.com/fleksible/entaENGELment-/actions/runs/43797262963/job/133068790253).

Der signierte DeepJump- und Legacy-Build-/Security-Pfad waren übersprungen.
CodeQL meldete fehlende Konfigurationen und ist kein belastbarer zusätzlicher
Sicherheitsnachweis. Die neuen Python-Ergebnisse müssen am korrigierten Head
durch die dedizierten CI-Läufe bestätigt werden.

Zusätzlich ist die Aktualität der JS-Prüfung relevant: Der neue Lauf von #475
auf derselben JS-Dependency-Basis scheitert im
[High-Gate](https://github.com/fleksible/entaENGELment-/actions/runs/44144870580/job/134257148477)
an zwei `picomatch`-Befunden. Beide PRs enthalten unverändert `picomatch@2.3.2`
und `picomatch@4.0.7` in Jest-/Packaging-Pfaden.
[GHSA-fc5q-39xc-vjpf](https://github.com/advisories/GHSA-fc5q-39xc-vjpf),
aktualisiert am 17. November 2026, nennt keine gepatchte Version. Das belegt
einen aktuellen repositoryweiten Gate-Blocker; daraus folgt nicht automatisch
eine erreichbare Sicherheitslücke der Produkt-UI.

## Kleinste belastbare Entscheidung

Die gezielte Lock-Reparatur im PR belassen und die CI erneut auswerten. Die
Versionspflege ist technisch von den Mess-/Report- und Scannerwirkungen
unterschieden und passend nachgeprüft. Solange das High-Gate rot bleibt, erfolgt
kein Merge. Eine reparierte Dependency oder eine eigenständig begründete,
ausdrücklich autorisierte Risikoausnahme wäre der nächste erforderliche Schritt;
das Gate wird hier nicht abgeschwächt und keine Ausnahme implizit erteilt.
