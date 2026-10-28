# PR #435: konsistenter Python-Lock

FOKUS: Fehlgeschlagene Dependency-PR technisch korrigieren

Status: DERIVED. Bot-Ausgangsstand `06c691a7edebeaaa1912248c2a1656442d147592`;
integrierte Basis `main@995450d3f1552d160b6dbfca4c6bad656f9323dc`.

## Ursache und kleinste Korrektur

Der Bot änderte zwei generierte Exporte, aber nicht `uv.lock`. Die Logs der
Pointer-Prüfung (Job 121381435515), Reproduzierbarkeit (121381434823) und des
Audits (121381434242) brechen vor Installation und Tests mit
`Generated requirements drift` ab. Der Fehler wurde lokal mit uv 0.12.18
reproduziert. Ein abgebrochener Audit-Start ist kein ausgeführter Audit.

Mit dem festgelegten uv **0.12.18** wurden vier kompatible Updates gezielt im
Lock aufgelöst; danach wurden alle vier Requirements-Exporte über
`tools/python_lock.py export` erzeugt und mit dem unveränderten `check` geprüft.

| Paket | Bisher | Korrigiert |
|---|---|---|
| ast-serialize | 0.13.0 | 0.13.1 |
| joserfc | 1.7.5 | 1.7.7 |
| python-dateutil | 2.9.0.post0 | 3.0.0 |
| tomlkit | 0.15.1 | 0.15.2 |

Der strukturierte TOML-Vergleich zeigt ausschließlich diese vier Versionswechsel:
gleiche Paketnamen, gleiche übrige Paketmetadaten und gleiche Lock-Metadaten.
`pyproject.toml`, Python-Floor, Runtime- und Test-Export bleiben unverändert.

## Drei belegte Konflikte bleiben HOLD

Drei getrennte Resolver-Proben (`uv lock --dry-run --upgrade-package`)
scheitern an den Anforderungen von Safety. Die installierten Metadaten von
Safety 3.8.1 bestätigen dieselben Grenzen:

| Vorschlag | Beibehalten | Safety-Anforderung |
|---|---|---|
| filelock 4.1.0 | 3.32.7 | `>=3.16.1,<4.0` |
| safety-schemas 0.0.21 | 0.0.16 | `==0.0.16` |
| typer 0.27.3 | 0.25.1 | `>=0.16.0,<0.26.0` |

Safety bleibt installiert, seine Grenzen werden nicht überschrieben. Der
universelle Python-Bereich wird nicht verkleinert, um die Vorschläge zu erzwingen.
Der korrigierte PR enthält vier Updates, nicht die ursprünglich angekündigten sieben.

## Abnahme

Linux, Python 3.12.14, uv 0.12.18. Frische getrennte Umgebungen für `dev`
(70 Pakete), `fractalsense`, Runtime und SBOM; jeweils `uv pip check` und
Lock-Receipt. Lock-SHA-256:
`55447f1dfddb85b1c1a6e73144ac92103e14dda602a3cce9204cd74acbc4c058`.

| Lokal geprüft | Ergebnis |
|---|---|
| Lock-/Export-Check nach Regenerierung | PASS |
| `make verify` | 859 Tests und 169 Subtests bestanden |
| Fractalsense | 184 Tests bestanden; 235 bestehende Warnungen |
| Governance, Ruff, Black, mypy | PASS |
| Bandit `-ll` | PASS; keine Befunde ab mittlerer Schwere |
| CycloneDX gegen frische Runtime-Receipt | PASS |

Die am veröffentlichten Head laufende CI muss zusätzlich vor Merge gelesen
werden; lokale Python-3.12-Tests ersetzen die Matrix 3.10–3.14 nicht.
Der am 27.10. unterbrochene Sammelupload hatte keine Branch-Änderung bewirkt;
die Wiederaufnahme lädt getrennte Blobs und vergleicht den fertigen Git-Tree.

## Rest

Dies repariert den konkreten Bot-Diff. #416 bleibt für die dauerhafte
Updater-/Export-Integration offen; die drei Konfliktversionen bleiben HOLD.
Keine Änderungen an Guards, GOLD, bestehenden Receipts, versiegelten Save States
oder privaten Korpusdaten. Die Korrektur bleibt in der PR-Historie nachvollziehbar.
