# #422: kompatible Updates im Lock und Export nachführen

**Datum:** 2026-10-24 · **Status:** ANNEX / DERIVED

**FOKUS:** Dependency-Lock und Exporte synchronisieren

[FAKT] Der Bot-Head `58f9c326ce5ecd9ec00a8ff4546bed8855e10c6b`
ändert nur `requirements-dev.txt`. `python tools/python_lock.py check` reproduziert
`Generated requirements drift: requirements-dev.txt`; die Installation wird
vor Tests abgebrochen. Der zentrale Lock ist die Auflösungsquelle.

[FAKT] Mit uv 0.12.18 wurden ausdrücklich `certifi==2026.10.19` und
`nltk==3.10.4` im Lock aufgelöst; alle vier Exporte wurden daraus regeneriert.
Der Vergleich mit `a99d55d` zeigt genau diese beiden Versionsänderungen.
Runtime-, Test- und FractalSense-Export bleiben dabei bytegleich zur Basis.

[FAKT] Der zusätzliche Bot-Vorschlag `filelock==4.1.0` ist mit dem vorhandenen
Safety 3.8.1 nicht kompatibel. Dessen installierte Paketmetadaten verlangen
`filelock>=3.16.1,<4.0`. Daher bleibt die vorhandene Version 3.32.7 erhalten;
der Sprung auf 4.1.0 ist **HOLD**, kein erledigtes Security-Update. Eine spätere
Auflösung dieses Konflikts braucht einen gesonderten konsistenten Dependency-Diff.

[FAKT] Eine frische Linux-/Python-3.12.14-Dev-Installation aus dem korrigierten
Lock besteht einschließlich `uv pip check`. `python tools/python_lock.py check`,
`make verify` (731 Tests und 165 Subtests), `make verify-governance`, Lint,
Typprüfung und Black bestehen. Dies prüft den ausführbaren Basisstand des
Bot-Branches; die aktuelle CI prüft zusätzlich dessen Integration mit main,
die unterstützte Python-Matrix, Reproduzierbarkeit und den SBOM-Abgleich.

[ANNEX] Das manuelle Verfahren aus [#416](https://github.com/fleksible/entaENGELment-/issues/416)
bleibt maßgeblich. Ein reparierter Bot-Diff ist kein Nachweis einer dauerhaft
reparierten Bot-Automation. Drift-Gates, Workflow-Rechte und Projekt-Claim-Status
werden nicht geändert. Vor Merge müssen die aktuellen erforderlichen und
betroffenen CI-Prüfungen erfolgreich sein.


## Gemeinsamer Abschlussstand

[FAKT] Nach Übernahme von #417/#419/#420, JS-Fix #424 und Pillow-Fix #421
wurde `main@28b9b4760f8e46a24c342a2bf46b171e79e6ef0e` in den Prüfstand
aufgenommen. Die automatische Lock-Zusammenführung besteht den gepinnten
Lock-/Export-Check; Kernprüfung mit 741 Tests und 165 Subtests sowie Governance
bestehen. Die aktuelle PR-CI prüft diesen gemeinsamen Stand erneut einschließlich
frischer Installation, Matrix, SBOM und unverändertem Security-Gate.
