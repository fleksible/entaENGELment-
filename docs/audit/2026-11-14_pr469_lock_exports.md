# PR #469: Click und Markdown-Parser konsistent im Python-Lock aktualisieren

**Datum:** 2026-11-14 · **Status:** ANNEX / DERIVED · technische Prüfung

**FOKUS:** Die beiden Paketupdates aus #469 im kanonischen Lock und seinem
Dev-Export zusammenführen und den bisherigen Setup-Abbruch prüfen.

## Auftrag, Ausgangsbefund und Herkunft

Kevin beauftragte die Ausführung der nächsten Schritte aus der technischen
Review von #469. Diese Korrektur wird als eigener Draft-PR bereitgestellt.
Das Mandat umfasst die Implementierung und Prüfung, keinen Merge.

Bot-Head: `c5117879e9d93d7703c3f945896ea4aebb6f3296`.
Basis der Korrektur: `main@c27ddef02949da16db491e9e7a04ec620aff2713`.
Der ursprüngliche Bot-Commit bleibt erhalten.

Der Bot änderte nur `requirements-dev.txt`. Im unveränderten `uv.lock`
standen weiterhin click 8.5.0 und markdown-it-py 4.2.0. Die produktive Prüfung
`python tools/python_lock.py check` scheiterte am Bot-Head mit Exit 1:
`Generated requirements drift: requirements-dev.txt`. Auch `sync --group test`
brach vor der Installation ab. Die Basisprüfung bestand mit demselben uv.
Diese Gegenprobe stammt aus der unmittelbar vorausgehenden Review.

Die direkt gelesenen CI-Logs am synthetischen Merge
`229048df38f3ccf9109f7fd7ca719cae89b5fa70` bestätigten den identischen Abbruch:
elf Setup-Jobs scheiterten am Drift, ein Sammeljob folgte. Tests und Audit
wurden dort nicht erreicht. Der erfolgreiche Advisory-Workflow und die
Code-Owner-Anfrage waren keine technische Freigabe.

## Konkrete Korrektur

Mit dem vorgeschriebenen **uv 0.12.18** wurden ausschließlich die beiden
gewünschten Versionen aktualisiert:

```sh
uv lock --upgrade-package click==8.5.1 --upgrade-package markdown-it-py==4.3.0
python tools/python_lock.py export
python tools/python_lock.py check
```

| Paket | Vorher | Nachher |
| --- | --- | --- |
| click | 8.5.0 | 8.5.1 |
| markdown-it-py | 4.2.0 | 4.3.0 |

Der strukturierte TOML-Abgleich zeigt 86 Lock-Einträge vor und nach der
Änderung: genau diese zwei Versionswechsel, 84 unveränderte weitere
Paketdatensätze und unveränderte globale Lock-Metadaten. Nur `uv.lock` und
`requirements-dev.txt` ändern sich technisch; dieser Bericht ergänzt den Diff.

Alle vier Exporte wurden über das vorhandene Werkzeug regeneriert.
Runtime-, Test- und Fractalsense-Export bleiben bytegleich. Der neue Dev-Export
ist bytegleich mit dem in #469 vorgeschlagenen Export
(`f126b661835ee9bad4cd475db55db5e9c53c559e` als Git-Blob).
Auflösung, Paketquellen und Hashes stammen aus uv, nicht aus manueller Bearbeitung.

Lock-SHA-256:
`f1786b27b3c66bf1ef30d2254191ec3e597a27747a9d097ea16068317722967d`.

## Selbst ausgeführte Prüfungen

Linux, CPython **3.12.14**, uv **0.12.18**. Dev- und Audit-Umgebung wurden
frisch aus dem korrigierten Lock installiert. Beide produktiven Sync-Läufe
bestanden einschließlich `uv pip check` und Lock-Receipt.

Die installierte Dev-Umgebung enthält nach direkter Metadatenprüfung
click **8.5.1**, markdown-it-py **4.3.0**, Rich **15.0.0**, Black **26.10.1**
und Bandit **1.9.4**. Ihr Receipt-Digest stimmt mit dem korrigierten Lock überein.

| Prüfung | Beobachtung |
| --- | --- |
| Konsistenzcheck auf aktuellem main vor der Änderung | Exit 0 |
| Korrigierter Lock und alle vier Exporte | Exit 0 |
| `sync --group dev` / `sync --group audit` | Beide Exit 0; kompatible Installationen |
| `make verify` | 1285 Tests und 200 Subtests bestanden, 2 übersprungen; Exit 0 |
| `ruff check src/ tools/ tests/` | Exit 0 |
| `black --check src/ tools/ tests/` | 130 Dateien unverändert; Exit 0 |
| `mypy src/ tools/` | 59 Quelldateien ohne Befund; Exit 0 |
| `bandit -c .bandit.yaml -r src/ tools/` | Keine Befunde bei bestehender Konfiguration; Exit 0 |
| `python tools/python_lock.py audit` | Alle 85 gesperrten externen Paketversionen geprüft, keine bekannten Schwachstellen; Exit 0 |
| `git diff --check` | Exit 0 |

Die zwei ausgelassenen Kernprüfungen betreffen DataLad/git-annex und werden
nicht als ausgeführte Empfangsprüfung gewertet. Vier optionale Ausgabepointer
fehlen im frischen Checkout; die Kernpointer sind gültig. Bandit verwendet
unverändert die vorhandenen Ausschlüsse. Der vollständige Lock-Audit prüft
auch die Versionszweige anderer Python-/Plattformmarker; er ist keine
Ausführung der Tests auf diesen Plattformen.

## Verhalten, CI-Grenze und Rücknahme

Click wird über Black eingebunden, markdown-it-py über Rich in den
Bandit-/pip-audit-Werkzeugumgebungen. Die vorausgehende Review fand in 161
aktiven versionierten Python-Dateien keine direkten Imports dieser Pakete.
Transitive Einbindung belegt allein keinen projektseitigen Markdown-Eingang.

Upstream beschreibt für markdown-it-py 4.3.0 behobene quadratische Parsing-Pfade
und weitere Änderungen an CommonMark-Randfällen und Erweiterungsverträgen.
Die Werkzeugprüfungen oben verwenden tatsächlich die neue Paketversion.
Eine eigene Reproduktion der Upstream-DoS-Fälle wird damit nicht behauptet.

Die vorhandenen CI-Jobs werden am veröffentlichten Draft-Head ausgewertet:
Python Quality, Runtime 3.11–3.14, frische Reproduzierbarkeit, Tests/Smoke,
DeepJump, vollständiger Python-Audit und SBOM. Dieser Commit-Bericht enthält
die lokalen Ergebnisse; die anschließenden CI-Nachweise gehören an den
exakten veröffentlichten Head in der PR-Beschreibung. Er nimmt sie nicht vorweg.

Unbekannte Schwachstellen und nicht durch Advisories abgedeckte native
Bestandteile bleiben außerhalb der Aussage des Paket-Audits. Die bekannte
Dependabot-Grenze in #416 wird durch diese manuelle Korrektur nicht behoben.

Rücknahmeweg: ein nachvollziehbarer Revert des technischen Commits mit Lock
und Export zusammen. Projektlogik, Tests, Workflow-Gates, GOLD, NICHTRAUM und
bestehende Receipts werden durch diese Korrektur nicht verändert.
