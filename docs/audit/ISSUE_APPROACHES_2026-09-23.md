# Issue-Ansätze — 2026-09-23

**Status:** DERIVED / Vorschlag; keine VOID-Schließung und keine Kanonisierung.
**Basis:** main `0aa93c53`, offene Issues #278, #305, #311, #332, #333.
**FOKUS:** Evidenzlücken in kleine prüfbare Umsetzungsschritte übersetzen.

## #278 — Recovery-Governance

[FACT] Vier veraltete Dateipointer im SoT-Spine wurden auf tatsächlich vorhandene
ANNEX-Dateien korrigiert. Die bisherige Branch-Protection-Anleitung führt interne
Job-IDs und nur nach Push ausgeführte Jobs als PR-Pflichtchecks auf. Der Entwurf
wird auf beobachtete veröffentlichte PR-Jobnamen korrigiert; Live-Settings bleiben
UNVERIFIED.

[MODEL] Für den verbleibenden GOLD-Draft `spec/runtime_eventlog_v0_1.json`:
`VOID_CLOSED` soll gemeinsame Pflichtfelder plus mindestens einen nichtleeren
`evidence_ref` oder `review_ref` verlangen. Eine explizite Review-Closure darf
keine empirische Bestätigung vortäuschen. `CLAIM_CREATED` braucht getrennte
interne und reduzierte Export-Dialekte; ein Hash allein ist keine Anonymisierung.

[FACT] `src/core/evidence_routing.py` hat bereits einen eigenen Runtime-Vertrag
mit internem `claim_text` und reduziertem, allowlist-basiertem Export. Den alten
Draft einfach umzuschreiben implementiert keine neue Runtime-Unterstützung.
[MODEL] Vor Migration: Roundtrip-/Export-Negativtests, Versionskennung und
Kompatibilitätsmatrix. Bilinguale Tags getrennt von Kurzformen erhalten und
Alias-Bypass-Tests des Evidence-Bridge-Adapters weiter bestehen lassen.

Offen bleiben die explizite GOLD-Freigabe für Policy/Spec und der Review dieser
Vertragsänderung; dieses Wartungspaket ändert die semantischen Policies nicht.

## #305 — Annex F

[FACT] Der Drive-Anhang v0.3 ist auffindbar und lesbar. Die Repo-Datei
`tests/benchmark/test_phasor_replay.py` prüft lediglich Parameter-Serialisierung;
sie ist weder der Textscanner noch ein Beleg der historischen 42/52-Ereignisse.
Scanner und Rohpositionen bleiben UNRESOLVED.

[MODEL] Erster unabhängiger PR: 24 Permutationen mit drei Nachbartranspositionen,
`D=inv/6`, `C=1-D`, explizite Kostenfunktion und normalisierte Übergangsmatrix.
Tests: vollständige Enumeration, Inversionsverteilung, Zeilensummen,
Reproduzierbarkeit, Referenzordnungs-Sensitivität. 24/12/6 nur als unterschiedliche
Identifikationsregeln dokumentieren, nicht als automatische Untergruppenkette.

[INFERENZ] Ein wichtiger zusätzlicher Prüfpunkt: Jeder Nachbartausch wechselt
die Parität. Ein Walk, der immer genau einen Tausch macht, hat Periode 2;
gewöhnliche Konvergenz zur stationären Verteilung darf nicht behauptet werden.
Für Mixing-Auswertung den unveränderten periodischen Kern getrennt ausweisen
und einen explizit benannten lazy-Kern `(I+P)/2` vergleichen. Die stationäre
Verteilung des vorgeschlagenen lokal normalisierten biased Walks nicht
ungeprüft als Gibbs-Verteilung ausgeben.

[MODEL] Zweiter PR erst nach Provenienzschluss: Scanner/Version, eingefrorene
Konfiguration, Rohlisten, mindestens zehn Texte und Längen-/Permutationskontrollen.
H0 als Zähldatenmodell mit Längen-Exposure vorregistrieren; Hold für 7:9, 1/64,
Catalan 42, Kibble-Zurek und physikalische Crosswalks bleibt bestehen.

## #311 — VOID-010 und VOID-011

[FACT] Beide stehen weiter auf IN_PROGRESS mit Datum 2026-07-15. Das Datum ist
kein Nachweis, dass die Forschungslücke geschlossen werden kann.
[MODEL] VOID-010: CSV mit mindestens fünf belastbaren Primärquellen, Einheiten,
Messbedingungen, Unsicherheit, Quelle und Geltungsbereich. Prüfer muss fehlende
Quellen/Einheiten ablehnen; synthetische Beispiele getrennt halten.
[MODEL] VOID-011: vorhandene Toy-Generatoren nutzen, Seed/Konfiguration und
Code-Revision in deterministischen Metrikexport aufnehmen. MI/PLV/FD samt
Null-/Randfällen prüfen. Export ausdrücklich SIMULATION_PROXY; keine Messung
menschlicher Resonanz. Signiertes Receipt nur bei tatsächlich vorhandenem
Secret, ansonsten UNSIGNED ausweisen. VOID-Schließung bleibt Review-Schritt.

## #332 — Security-Settings

[FACT] SECURITY.md nennt noch keinen verifizierten privaten Melde-Endpunkt.
Die verfügbaren GitHub-Aktionen geben keinen Schreibzugriff auf CodeQL-Setup
oder Private Vulnerability Reporting. Kein live aktiviertes Setting behaupten.
[MODEL] Maintainer prüft CodeQL-Sprachen und Trigger, aktiviert den privaten
Meldeweg und testet diesen mit einem harmlosen Bericht. Erst anschließend den
beobachteten Endpunkt in SECURITY.md veröffentlichen; keine vertraulichen
Reportdaten in öffentliche Issues aufnehmen.

## #333 — Python-Lock

[FACT] Runtime-Abhängigkeiten sind in pyproject und requirements doppelt
aufgeführt; Dev-Gruppen unterscheiden sich (z.B. Black-Pin und Security-Tools).
Ein Lock ohne Konsolidierung könnte diesen Drift einfrieren.
[MODEL] Vorschlag: pyproject als Manifest, uv als einziger Lock-Generator,
explizite Runtime-/Dev-/Audit-Gruppen, dokumentiert gepinnte uv-Version.
Den Python-3.9-Vertrag vor Auflösung prüfen; keine stille Anhebung des Floors.
Historische NICHTRAUM-Locks bleiben Provenienz und werden nicht reaktiviert.
[MODEL] Abnahme: zwei frische, gefrorene Installationen pro Python 3.9–3.12,
identische Paketlisten je Plattform/Interpreter, `pip check`, Core-/Fractalsense-
Tests und SBOM-Vergleich. Unterschiedliche Interpreter dürfen begründete Marker-
Auflösungen haben. Danach alle CI-/Release-/SBOM-Installer auf frozen sync
umstellen und einen gezielten, reviewbaren Lock-Refresh dokumentieren.
Dependabot erst nach geprüftem Support auf dieselbe Strategie ausrichten.

## Major-PRs #298 und #339

[FACT] Am 2026-09-23 abgefragte Paketmetadaten:
`eslint-plugin-react@7.37.5` unterstützt ESLint bis `^9.7`, nicht 10;
`typescript-eslint@8.70.1` unterstützt TypeScript `>=4.8.4 <6.1.0`, nicht 7.
`eslint-config-next@16.3.3` hängt weiterhin an dieser Pluginfamilie.
[MODEL] Beide Major-PRs bleiben HOLD bis echte kompatible Releases vorliegen.
Keine Regelabschaltung, Peer-Override oder Force-Installation als Ersatz.
Reentry: explizite Migration, frozen install, Typecheck/Lint/Build/Tests,
Rollback auf die dokumentierte TS6-/ESLint9-Baseline.
