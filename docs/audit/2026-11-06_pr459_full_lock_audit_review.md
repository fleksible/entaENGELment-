# PR #459: Abnahme des vollständigen Python-Lock-Audits

FOKUS: CI-Sicherheitsprüfung auf alle Paketlisten ausweiten

**Status:** ANNEX / DERIVED, technische Abnahme; keine Claim-Promotion.
**Datum:** 2026-11-06.

## Auftrag und geprüfter Stand

Kevin beauftragte am 06.11.2026 die Ausführung der Aufgaben aus dem
Wochenstatus. Dessen technischer Schritt 2 umfasst die abschließende Abnahme
von #459, die geprüfte Übernahme und die Bestätigung des Vollaudits auf main.
Dieses begrenzte Mandat trägt ausschließlich diese technische Übernahme;
Leserkreis, Toy-Modellentscheidung und geschützte Herkunft bleiben getrennt.
Es ersetzt für diesen Schritt den früheren Vorbehalt im PR-Text
„Merge bleibt bei Kevin“ vom 05.11., nicht den übrigen Delegationsrahmen.

Ausgangspunkt: PR-Head `a85d56ac924d5f1bc6dfbb10e0a42d4fa15e05a3`.
Aktuelle main-Basis `867e41c10c3c80349dc93a9cce7303793483101c`
wurde ohne Konflikt integriert; lokaler Merge-Stand
`c4f994ca88f702cd652cb88bcd06be9c968fbd47`.
Darauf kommen ausschließlich die acht CLI-Gegenfixtures und dieser Bericht.
Lock-SHA-256: `c3403e979f63c0ce669e1a6d447e68065d581fd7d889e9fd0ebdabc3f23c1821`.

## Ergebnis und Gegenproben

Der neue Auditpfad exportiert alle Gruppen und Markerzweige als pylock.toml,
prüft sie mit dem gelockten pip-audit und vergleicht die Report-Abdeckung
gegen jede exportierte Paketversion. Beide Workflow-Aufrufer verwenden
diesen Pfad. Der Fehlerstatus des Scanners wird nach dem Reportvergleich
zusätzlich geprüft, sodass ein sauberer Report einen Fehler-Exit nicht verdeckt.

Die bestehenden neun Prüffälle decken Befunde, übersprungene und fehlende
Pakete, falsche Versionen sowie fehlerhafte Report-Einträge ab. Acht ergänzte
CLI-Prüffälle üben den realen `main()`/`audit()`-Kontrollfluss mit kontrollierten
UV-/Scanner-Ausgaben: sauber, Fehler-Exit 7, Signal-Exit -9, kein Report,
ungültiges JSON, Teilreport, übersprungenes Paket und Befund trotz Exit 0.
Diese Fixtures sind keine echten Netzwerk- oder Prozessabbruchversuche.

| Selbst lokal ausgeführte Prüfung | Ergebnis |
| --- | --- |
| Audit-Testdatei | 17 bestanden |
| `make verify` | 1206 Tests und 169 Subtests bestanden, 2 übersprungen; Exit 0 |
| `make verify-governance` | 16 Workflow-Verträge und 22 synchronisierte VOIDs; Exit 0 |
| Ruff und Black für Auditcode und Testdatei | PASS |
| mypy für `tools/python_lock.py` | PASS |
| Echter Vollaudit mit uv 0.12.18 und pip-audit 2.10.1 | 85 Paketversionen, keine bekannten Befunde |
| `git diff --check` | PASS |

Umgebung: Linux, Python 3.12.14; getrennte frisch synchronisierte dev- und
audit-Umgebungen aus dem unveränderten Lock. Ein erster Lauf verwendete
versehentlich den Bootstrap-Interpreter ohne PyYAML für Unterprozesse;
zwei Pointertests scheiterten deshalb. Nach korrigierter PATH-Reihenfolge
bestand derselbe Code vollständig. Vier optionale Ausgabepointer fehlen
im frischen Checkout; alle Kernpointer sind gültig.

## CI-Herkunft und Merge-Bedingung

Direkt gelesene GitHub-Protokolle des Ausgangsheads:
[Python-Audit, Job 127932665607](https://github.com/fleksible/entaENGELment-/actions/runs/42229855196/job/127932665607)
und [Security Scan, Job 127933292506](https://github.com/fleksible/entaENGELment-/actions/runs/42229846531/job/127933292506).
Beide führen den neuen Audit aus und melden 85 vollständig geprüfte Versionen.
Der erste lief auf dem synthetischen Merge `68bd92ee0283654c2776e7fd6161b8d28d069865`.
Die fünf Pflichtchecks des Ausgangsheads sind erfolgreich; das Codex-Review
ohne Befunde bezog sich auf `1667000`, nicht auf spätere Commits.

Vor Übernahme ist deshalb die CI am veröffentlichten neuen Head erneut
direkt aufzulösen. Merge nur bei grünen Pflichtchecks und erfolgreichem
Python-Vollaudit. Nach Übernahme den Audit auf dem tatsächlichen main-Commit
bestätigen; dieser Bericht nimmt diesen späteren Nachweis nicht vorweg.

## Grenzen und Rücknahme

Keine neue Branch-Protection-Einstellung: der separate Python-Audit wird
hierdurch kein Required Check. Ein Ausfall der Schwachstellendatenbank
lässt den Lauf scheitern. Nicht erfasst sind unveröffentlichte Lücken und
native Wheel-Bestandteile ohne zugehörige Python-Paket-Advisory; JS besitzt
seinen eigenen Auditpfad. Die beiden Python-Jobs teilen Scanner und Datenbank
und sind keine unabhängigen Sicherheitsquellen.

Keine Änderungen an GOLD, NICHTRAUM, bestehenden Receipts, HUD oder privaten
Quellen. Revert des späteren Merge-Commits ist der technische Rücknahmeweg;
er würde die kleinere alte Audit-Abdeckung wiederherstellen.
