# FractalSense ab Python 3.11: Pillow-Restbefund schließen

**Datum:** 2026-11-05 · **Status:** ANNEX / DERIVED

**FOKUS:** Pillow-Restbefund im Python-3.10-Zweig schließen

[FAKT] Ausgangslage auf `main@5380a0a`: Die Gruppe `fractalsense` exportiert für
Python 3.10 `pillow==12.3.0` (über `matplotlib`). `pip-audit` 2.10.1 über alle 95
aus `uv.lock` exportierten Paket-/Versionspaare (runtime, test, dev, fractalsense,
audit, sbom, build) meldet dafür 39 Schwachstellen, Exit-Code 1, keine Skips,
keine weiteren Befunde. Einzige Fixversion ist 13.0.0.

[FAKT] Pillow 13.0.0 verlangt Python >=3.11; seit 12.3.0 (2026-07-01) gibt es
keine 12.x-Veröffentlichung mehr. Für Python 3.10 existiert damit keine
befundfreie Pillow-Version. PEP 619 sieht das Lebensende von Python 3.10 für
Oktober 2026 vor.

[FAKT] Änderung: `tool.uv.dependency-groups.fractalsense` verlangt jetzt
Python >=3.11 (wie bereits `audit` und `sbom`). Das FractalSense-Matrix-Leg 3.10
in `test.yml` entfällt. Die Projektanforderung `requires-python = ">=3.10"` und
alle Kern-Matrizen (`ci.yml`, `ci-python-runtime.yml`, `ci-python-quality.yml`)
bleiben unverändert.

[FAKT] Neuauflösung mit uv 0.12.18 entfernt ausschließlich die 3.10-Zweige von
`pillow` 12.3.0, `matplotlib` 3.10.9, `contourpy` 1.3.2 und `fonttools` 4.65.0
(96 → 92 Pakete). Keine überlebende Version ändert sich.

## Gegenprobe

- `python tools/python_lock.py check` besteht; Exporte regeneriert, kein Drift.
- `pip-audit` über alle 91 exportierten Paare: **keine Befunde**, keine Skips, Exit 0.
- FractalSense-Sync unter Python 3.11.18 aus dem Lock: Pillow 13.0.0,
  `uv pip check` grün, 184 Tests bestanden (235 Warnungen sichtbar, nicht unterdrückt).
- FractalSense-Sync unter Python 3.10.21 bricht laut ab (Gruppenanforderung >=3.11),
  statt still eine Teilumgebung zu installieren.
- Kern unter Python 3.10.21 (Gruppe `dev`): Sync grün, 1189 Tests bestanden.
- `make verify` und `make verify-governance` bestanden.
- Required Check bleibt `All Tests Pass`; die einzelnen Matrix-Legs sind nicht
  als Required Check eingetragen (Branch-Protection per API gelesen).

[ANNEX] Diese Notiz revidiert die Festlegung aus
[2026-10-24_pr421_pillow_lock.md](2026-10-24_pr421_pillow_lock.md), die
FractalSense-Matrix nicht anzuheben. Weil für Python 3.10 keine befundfreie
Pillow-Version existiert und keine mehr erscheinen wird, hieße Festhalten an 3.10
einen dauerhaft offenen Sicherheitsbefund in Kauf nehmen.

## Bewusst offen

- Ob der Kern Python 3.10 nach dessen Lebensende weiter unterstützt, ist eine
  eigene Entscheidung und hier nicht berührt.
- Der CI-Sicherheitslauf (`security-audit.yml`) prüft weiterhin nur
  `requirements.txt`; der hier verwendete Vollaudit über alle Gruppen ist ein
  lokaler Lauf, kein CI-Gate.
