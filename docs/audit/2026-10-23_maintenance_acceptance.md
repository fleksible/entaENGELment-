# Wartungsabnahme und verbleibende Anschlüsse — 2026-10-23

**Status:** ANNEX · DERIVED · Reviewfassung

**FOKUS:** Wartungsabnahme nachführen

**Gelesene und lokal geprüfte Basis:** `a99d55deeb38bf33564ebabb45841656fd45496a`

## Auftrag und Umfang

[ANNEX] Der Owner beauftragt die übrigen Wartungspunkte während der separat
beauftragten Claude-/Diogenes-Gegenlese. Dieser Diff aktualisiert die bestehende
Lock-Anleitung, ergänzt den privaten Melde-Testablauf und dokumentiert die
Abnahmegrenzen. Die GOLD-Gegenlese aus #407/#408 bleibt ein eigener Auftrag.

## Python-Lock: implementiert, Updater getrennt offen

[FAKT] `uv.lock` ist die gemeinsame Auflösung; `tools/python_lock.py` verlangt
uv 0.12.18, prüft alle vier Exporte, synchronisiert mit `--locked` und prüft die
installierte Umgebung. Release Gate, VOID-Monitor und SBOM verwenden diese
Installation. Das tagbasierte Release-Gate wurde hier nicht ausgelöst.

[FAKT] Die an der Basis gelesene Runtime-Matrix umfasst Linux/Python 3.10–3.14;
die separate FractalSense-Matrix umfasst 3.10–3.12. Die bisherige Lock-Anleitung
nannte noch die frühere Spanne 3.9–3.12 und einen bereits erfüllten Mergevorbehalt.
Der historische Baseline-Bericht bleibt als damaliger Stand erhalten.

[FAKT] Am korrigierten #410-Head besteht die
[Runtime-/Reproduzierbarkeitsprüfung vom 20.10.](https://github.com/fleksible/entaENGELment-/actions/runs/39395067994).
Der Job `118535654683` meldet zwei identische frische Installationsreceipts.
Der [SBOM-Lauf](https://github.com/fleksible/entaENGELment-/actions/runs/39395067869),
Job `118535654014`, bestätigt den Abgleich mit dem aktuellen Lock-Receipt.
Das sind ausgeführte CI-Belege; plattformübergreifende Gleichheit wird nicht behauptet.

[FAKT] Lokal wurde eine neue Dev-Umgebung aus demselben Lock mit uv 0.12.18
installiert; `uv pip check` besteht. Der vorinstallierte uv 0.12.23 wurde nicht
als Generator verwendet: seine Versionsprüfung wies bereits die Einrichtung aus
dem Projektverzeichnis zurück. Ein separates lokales uv-0.12.18-Werkzeug stellt
anschließend den vorgeschriebenen Installer bereit. Lock und Exporte bleiben
byte-identisch zur Basis.

[ANNEX] Der erfüllte Lock-Anteil von #333 wird abgenommen. Das verbleibende
Dependabot-Exportproblem ist als [#416](https://github.com/fleksible/entaENGELment-/issues/416)
abgegrenzt. Der [uv-Updaterlauf vom 19.10.](https://github.com/fleksible/entaENGELment-/actions/runs/39193889979)
erzeugte erfolgreich einen PR; dessen anfängliche Exportdrift blieb ein eigener
Fehler. Das manuelle Verfahren aus der Owner-Entscheidung vom 18.10. bleibt erhalten.

## Security-Meldeweg: Einstieg bestätigt, Empfang offen

[FAKT] Die abgemeldete Browseransicht der öffentlichen
[Advisory-Seite](https://github.com/fleksible/entaENGELment-/security/advisories)
zeigt `Report a vulnerability`. Nach dessen Aufruf erscheint die GitHub-Anmeldung
für das Meldeformular. Es wurde kein Bericht versandt und kein Empfang behauptet.
Der [vorbereitete Runbook-Ablauf](../runbooks/PRIVATE_REPORTING_SMOKE_TEST_v0_1.md)
enthält einen harmlosen Marker und die noch auszuführende Abnahme.

[FAKT] Der [CodeQL-Lauf auf der Basis](https://github.com/fleksible/entaENGELment-/actions/runs/39996214068)
besteht für Python, C/C++, JavaScript/TypeScript und Actions. Er belegt diese
Ausführung. Vollständige administrative Trigger-Einstellungen sind dadurch
nicht ausgelesen. #332 bleibt für diesen Settings-Abgleich und den externen
Empfangstest offen.

## Phasenanbindung: aktuelles HOLD berücksichtigen

[FAKT] Nach dem früheren Freitagsanker wurde [#415](https://github.com/fleksible/entaENGELment-/pull/415)
gemergt. Der vorhandene [Quellenabgleich](../annex/PHASENQUELLE_UND_ZUORDNUNG_v0_1.md)
belegt einen synthetischen Producer, aber noch keine ausgewählte HUD-Größe oder
Sample-/Boundary-/Frame-/Slice-Zuordnung. Ein zweiter Quellenbericht oder ein
Anschluss allein durch Umbenennen bestehender IDs würde diese Lücke nicht schließen.

[ANNEX] Vor einem technischen Replay sind verfolgte Größe, Referenz/Orientierung,
Prozessbeobachtungen, Identitätsbindung und unabhängig deklarierte Transformregel
inhaltlich festzulegen. [Issue #418](https://github.com/fleksible/entaENGELment-/issues/418)
hält diese sechs Setzungen und die anschließenden Gegenfälle als ausführbares
Arbeitspaket fest. Die bestehende Kandidatenskizze kann dafür als SIMULATION_PROXY
dienen; eine HUD-Bedeutung wird damit nicht ausgewählt.
Graining, Blindseite und Sphärenstatus bleiben UNRESOLVED; Kη-03 bleibt UNBOUND.

## Lokale Prüfung

[FAKT] Der Basislauf von `make verify` besteht: 731 Tests und 165 Subtests,
Port-Lint, Core-Pointer und Claim-Lint. Die vier bekannten optionalen generierten
Pfade fehlen weiterhin; kein Core-Pointer fehlt. Die direkt ausgeführten
Frame-/HUD-/Bridge-/Slice-Tests bestehen mit 58 Fällen. Bestehende Node-
Modulformat-Warnungen bleiben sichtbar.

[FAKT] Auch die Nachprüfung des Dokumentdiffs besteht mit 731 Tests und
165 Subtests. `make verify-governance` bestätigt 15 Workflow-Konfigurationen
und 22 zwischen Registry und UI synchronisierte VOIDs. Sechs relative Links
der drei Dokumente lösen auf; die Lock-/Export-Dateien sind unverändert und
`git diff --check` besteht. Der abschließende reine Ergebnisnachtrag ändert
keinen ausführbaren Prüfinhalt. Kein vollständiger UI-Build wurde für diesen
Dokumentdiff benötigt; die 58 gezielten Node-Fälle wurden separat ausgeführt.

[ANNEX] Der Claim-Lint erfasst die neuen Dokumenttexte nicht; deren Reichweite
wurde redaktionell geprüft. Aktuelle PR-CI ist erst am veröffentlichten Head
maßgeblich. Eine Source-of-Truth-Promotion oder öffentliche Release-Freigabe
wird aus diesem Bericht nicht abgeleitet.


## Anschlussreview vom 2026-10-24

[FAKT] Der vollständige Drei-Dateien-Diff wurde erneut gelesen. `make verify`
besteht auf dem unveränderten ausführbaren Basisstand mit 731 Tests und
165 Subtests; `make verify-governance` und `git diff --check` bestehen.
Die relativen Links lösen auf. Lock und alle vier Requirements-Exporte sind
gegenüber `a99d55d` unverändert. Dies ist eine neue lokale Nachprüfung unter
Linux/Python 3.12.14; die früheren 58 Node-Fälle wurden dabei nicht erneut ausgeführt.

[ANNEX] Der aktuelle Owner-Auftrag umfasst die Bearbeitung und Übernahme dieses
Dokumentdiffs. Die Abnahme gilt für die hier beschriebenen Wartungsangaben.
Der externe Meldeempfang aus #332 bleibt NOT_RUN; die Updaterkorrektur aus #416
bleibt gesonderte Arbeit. Eine menschliche Codelektüre, ein historisches GOLD-OK
oder eine kanonische Promotion wird aus dem delegierten Review nicht abgeleitet.
