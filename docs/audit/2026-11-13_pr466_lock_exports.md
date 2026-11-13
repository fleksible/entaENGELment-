# PR #466: Python-Lock und Requirements konsistent nachführen

**Datum:** 2026-11-13 · **Status:** ANNEX / DERIVED · technische Prüfung

**FOKUS:** Den konkreten Dependency-Diff aus #466 konsistent auflösen

## Auftrag, Herkunft und Umfang

Kevin beauftragte am 13. November die Umsetzung der nächsten Aktionen aus dem
Wochenstatus. Der technische Schritt umfasst die Korrektur von #466 und die
erneute CI-Prüfung. Das bestehende Mandat zur sinnvollen, geprüften Übernahme
der Projektarbeit wird für diese begrenzte technische Korrektur verwendet.
Die Modellentscheidung aus #423 und eine Korpus-Kanonisierung sind davon getrennt.

Bot-Ausgangspunkt: `2eac4000c5400065737c30b28f5ec0df1e0b1f4d`.
Basis der Korrektur: `main@d489c2876b18dfe5d620ed08d10481185ea2b112`.
Die manuelle Ersatz-PR folgt dem in `.github/dependabot.yml` und #416
festgehaltenen Verfahren. Der ursprüngliche Bot-Commit bleibt erhalten.

## Reproduzierter Fehler und Korrektur

Der Bot änderte ausschließlich `requirements-test.txt`, `requirements-dev.txt`
und `Fractalsense/requirements-dev.txt`; `uv.lock` blieb unverändert.
`python tools/python_lock.py check` endet am unveränderten Bot-Head mit Exit 1:
`Generated requirements drift` für genau diese drei Exporte.

Der direkt gelesene [Runtime-Job 128960563303](https://github.com/fleksible/entaENGELment-/actions/runs/42555629864/job/128960563303)
zeigt denselben Abbruch auf dem damaligen synthetischen Merge
`d834ea3b6cddaa31c249f4d271941fdb071a1999`. Die Installation erreicht dort
weder Testausführung noch einen erfolgreichen Paket-Audit.

Mit **uv 0.12.18** wurden die sechs gewünschten Versionen zunächst gemeinsam
mit `uv lock --dry-run --upgrade-package` auflösbar nachgewiesen, anschließend
im zentralen Lock aufgelöst. Alle vier Exporte wurden ausschließlich mit
`python tools/python_lock.py export` erzeugt und mit dem unveränderten
`python tools/python_lock.py check` geprüft. Der Runtime-Export bleibt bytegleich.

| Paket | Bisher | Korrektur |
| --- | --- | --- |
| coverage | 7.16.2 | 7.17.2 |
| fonttools | 4.66.1 | 4.68.0 |
| mypy-extensions | 1.1.0 | 1.2.0 |
| platformdirs | 4.12.4 | 4.14.5 |
| python-dateutil | 3.0.0 | 4.0.0 |
| rpds-py | 2026.6.3 | 2026.9.1 |

Der strukturierte TOML-Vergleich zeigt nur diese sechs Versionswechsel,
keine zusätzlichen oder entfernten Paketnamen und unveränderte globale
Lock-Metadaten. Zusätzlich regeneriert uv die unveränderte pytest-cov-Version
7.1.0 mit einer `coverage`-Abhängigkeitskante ohne den bisherigen `toml`-Extra.
Das ist eine generierte Kantenänderung, kein siebtes Paketupdate.
`pyproject.toml`, Python-Floor und Workflow-Gates werden nicht verändert.

Lock-SHA-256: `e9c22ba89d33323a11128dfbe742b6ed0848a870f9e28dacd93e4041a3b17008`.

## Selbst ausgeführte lokale Prüfungen

Linux, Python **3.12.14**, uv **0.12.18**. Jede der folgenden Umgebungen wurde
frisch aus demselben korrigierten Lock installiert: dev, runtime, sbom, audit,
fractalsense und zwei getrennte test-Umgebungen. `sync` prüft jeweils
`uv pip check` und schreibt die passende Lock-Receipt.

| Prüfung | Beobachtung |
| --- | --- |
| Lock und alle vier Exporte | PASS, Exit 0 |
| `make verify` | 1222 bestanden, 193 Subtests bestanden, 2 übersprungen; Exit 0 |
| `make verify-governance` | 16 Workflows und 22 VOIDs synchron; Exit 0 |
| Ruff / Black / mypy | PASS; Black 129 Dateien, mypy 59 Quelldateien |
| Bandit mit bestehender `.bandit.yaml` | Keine Befunde; vorhandene Ausschlüsse bleiben wirksam |
| Fractalsense | 184 bestanden, 235 Warnungen zur wiederholten Colormap-Registrierung; Exit 0 |
| Zwei frische test-Installationen | Vollständige Lock-Receipts identisch |
| CycloneDX gegen frische Runtime | SBOM-Generierung und Receipt-Abgleich bestanden |
| Vollständiger Lock-Audit | 85 Paketversionen geprüft, keine bekannten Schwachstellen; Exit 0 |
| `git diff --check` | PASS |

Die zwei übersprungenen Kernprüfungen benötigen DataLad/git-annex; sie werden
nicht als ausgeführte private Empfangsprüfung gewertet. Vier optionale
Ausgabepointer fehlen im frischen Checkout; alle 47 vorhandenen Kern-/Quellpfade
sind gültig, kein CORE-Pointer fehlt. Lokale Python-3.12-Prüfung ersetzt nicht
die CI-Matrix 3.11 bis 3.14.

## CI-Bedingung, Rückweg und verbleibende Grenze

Vor Merge sind Checks, vollständiger Python-Audit und Review am tatsächlich
veröffentlichten Korrektur-Head erneut zu lesen. Nach der Übernahme ist der
Audit am tatsächlichen main-Commit zu bestätigen. Dieser Bericht nimmt diese
späteren Ergebnisse nicht vorweg.

#416 bleibt offen: Ein manueller erfolgreicher Durchlauf belegt keine dauerhafte
Reparatur des Updaters. Unbekannte Schwachstellen und native Wheel-Bestandteile
ohne passende Advisories sind durch den Audit nicht vollständig erfasst.
Der JS-Audit besitzt seinen eigenen Prüfumfang.

Rücknahmeweg ist ein nachvollziehbarer Revert der technischen Übernahme.
GOLD, NICHTRAUM, bestehende Receipts und private Korpusdaten sind nicht Teil
dieses Diffs. Die Korpus-Review-Karten bleiben getrennt und REVIEW-PENDING.
