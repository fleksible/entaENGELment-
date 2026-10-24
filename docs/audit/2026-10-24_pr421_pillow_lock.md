# #421: Pillow im universellen Lock nachführen

**Datum:** 2026-10-24 · **Status:** ANNEX / DERIVED

**FOKUS:** Pillow-Update mit Python-Matrix erhalten

[FAKT] Der ursprüngliche Bot-Head `e23175910061e0e05eb5bc45c17dcfc754da473a`
ändert nur den FractalSense-Export. Der Lock-Check reproduziert
`Generated requirements drift: Fractalsense/requirements-dev.txt`.

[FAKT] Nach Aufnahme von `main@539e87b` wurde mit uv 0.12.18 ausschließlich
Pillow neu aufgelöst und alle vier Exporte regeneriert. Die universelle
Auflösung erhält Pillow 12.3.0 für Python 3.10 und verwendet 13.0.0 ab Python
3.11. Pillow 13 beendet die Unterstützung von Python 3.10; ein unbedingter
13.0.0-Pin würde die bestehende Runtime-/FractalSense-Matrix verletzen.
Projektanforderung und Matrix werden nicht angehoben. Andere Paketversionen
bleiben gegenüber dieser Basis unverändert.

[FAKT] `python tools/python_lock.py check` besteht. Eine frische
Linux-/Python-3.12.14-FractalSense-Umgebung aus dem Lock installiert Pillow
13.0.0 und besteht `uv pip check`. `make verify`: 741 Tests und 165 Subtests;
`make verify-governance` bestanden. Die separate FractalSense-Suite besteht mit
184 Tests; ihre 235 Warnungen bleiben sichtbar und werden nicht unterdrückt.

[ANNEX] Die universellen Marker sind eine Resolverentscheidung, kein lokaler
Ausführungstest unter Python 3.10. Die aktuelle PR-CI muss die unterstützte
Matrix, frische Reproduzierbarkeit und den SBOM-Abgleich am korrigierten Head
prüfen. Dieser manuelle Abschluss folgt dem Verfahren aus
[#416](https://github.com/fleksible/entaENGELment-/issues/416); die dauerhafte
Bot-Korrektur bleibt offen. Kein Gate wird abgeschwächt.
