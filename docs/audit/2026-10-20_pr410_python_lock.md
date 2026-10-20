# Report: PR #410 — konsistente Python-Abhängigkeiten

**Datum:** 2026-10-20  
**FOKUS:** Python-Lock-Drift in PR #410 beheben  
**Ausgangsbasis:** `6816f4e0c7787c78c09d61bbd8748787a92e3685`  
**Vergleichsbasis main:** `f266f3b7277f6156e0dcfe4a3f2f432fb65f1e4a`

## Befund

[FACT] Der ursprüngliche Dependabot-PR kündigte 16 Updates an. Im zentralen
`uv.lock` war nur Ruff aktualisiert; die übrigen Updates standen ausschließlich
in den generierten Requirements-Dateien. `python tools/python_lock.py check`
reproduzierte den CI-Abbruch:

```text
FAIL: Generated requirements drift: requirements-test.txt, requirements-dev.txt, Fractalsense/requirements-dev.txt
```

Belege: [Python Quality](https://github.com/fleksible/entaENGELment-/actions/runs/39194856260),
[Python Runtime Matrix](https://github.com/fleksible/entaENGELment-/actions/runs/39194856227),
[Security Audit](https://github.com/fleksible/entaENGELment-/actions/runs/39194856320).
Die Installationsschritte blockierten vor den jeweiligen Tests bzw. Audits.

## Behebung

Die vorgesehenen Versionen wurden mit dem festgelegten **uv 0.12.18** über
gezielte `uv lock --upgrade-package NAME==VERSION`-Argumente aufgelöst.
Anschließend wurden alle Exporte mit `python tools/python_lock.py export`
regeneriert. Der unveränderte Drift-Check besteht danach.

13 Updates sind gegenüber `main` tatsächlich im Lock enthalten:

| Paket | Vorher | Nachher |
|---|---|---|
| ast-serialize | 0.11.2 | 0.13.0 |
| authlib | 1.8.0 | 1.9.1 |
| cryptography | 50.0.1 | 50.0.2 |
| iniconfig | 2.3.0 | 2.3.1 |
| markupsafe | 3.0.3 | 3.0.4 |
| platformdirs | 4.12.2 | 4.12.4 |
| pluggy | 1.6.0 | 1.7.0 |
| pycparser | 3.0 | 3.11 |
| pydantic | 2.13.5 | 2.14.1 |
| pydantic-core | 2.46.5 | 2.50.1 |
| ruff | 0.17.0 | 0.17.1 |
| tenacity | 9.1.4 | 9.2.1 |
| truststore | 0.10.4 | 0.10.5 |

Keine zusätzlichen Paketnamen, Änderungen an unveränderten Paketversionen oder
Änderungen der Lock-Metadaten gegenüber `main`. `pyproject.toml` bleibt unverändert.

## Zurückgestellt: drei inkompatible Vorschläge

[FACT] Der Resolver weist folgende Zielversionen wegen der Abhängigkeiten von
Safety 3.8.1 zurück. Die Grenzen wurden zusätzlich aus den Metadaten des frisch
installierten Safety-Pakets gelesen.

| Paket | Vorschlag | Beibehalten | Safety-Anforderung |
|---|---|---|---|
| filelock | 4.1.0 | 3.32.7 | `>=3.16.1,<4.0` |
| safety-schemas | 0.0.21 | 0.0.16 | `==0.0.16` |
| typer | 0.27.3 | 0.25.1 | `>=0.16.0,<0.26.0` |

Diese drei Updates sind **HOLD**, nicht umgesetzt. Der Python-Kompatibilitätsbereich
wurde nicht eingeschränkt und Safety nicht entfernt, um eine Auflösung zu erzwingen.

## Prüfung

Lokal: Linux, Python 3.12.14, uv 0.12.18; separate frische Umgebungen für `dev`
und `fractalsense`, jeweils einschließlich `uv pip check` und Lock-Receipt.

| Prüfung | Ergebnis |
|---|---|
| Ausgangsfehler `python tools/python_lock.py check` | vor Änderung reproduziert |
| `python tools/python_lock.py export` / `check` | PASS nach Regenerierung |
| `python tools/python_lock.py sync --group dev` | PASS, 70 kompatible installierte Pakete |
| `python tools/python_lock.py sync --group fractalsense` | PASS in separater Umgebung |
| `make verify` | PASS: 709 Tests, 165 Subtests; Ports, Core-Pointer und Claim-Lint |
| Fractalsense `python -m pytest -q` | 184 PASS; 235 Warnungen, unter anderem Colormap-Neuregistrierung |
| Ruff / Black / mypy / Bandit | PASS; keine Bandit-Befunde |
| `git diff --check` | PASS |

Die lokalen Prüfungen decken Python 3.12 ab. Die PR-CI prüft zusätzlich die
Runtime-Matrix 3.10–3.14, Fractalsense 3.10–3.12, Reproduzierbarkeit, SBOM und
Security-Audit. Deren Ergebnis muss am veröffentlichten Commit gelesen werden;
dieser Bericht behauptet keinen vorweggenommenen CI-PASS.

## Grenzen und Reversibilität

Der Fix erhält `uv.lock` als einzige Auflösungsautorität sowie die blockierenden
Drift-, Integritäts- und Sicherheitsprüfungen. Keine Änderungen an Workflows,
Guards, GOLD, Receipts, NICHTRAUM oder fachlichen Modellen. Keine Kanonisierung.
Der Korrekturcommit ist separat revertierbar; ein Revert stellt allerdings auch
den bekannten inkonsistenten PR-Zustand wieder her.

Der dokumentierte manuelle Umgang mit Dependabot-uv-Updates bleibt bestehen.
Dieser Fix repariert den vorhandenen PR; er automatisiert künftige Bot-Korrekturen
nicht. Die drei HOLD-Updates benötigen eine spätere kompatible Auflösung.
