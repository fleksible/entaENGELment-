# Audit: Korpus-Snapshot v10

**Datum:** 2026-10-07
**Fokus:** Korpusstand als öffentlichen Intake-PR bereitstellen
**Status:** DERIVED / REVIEW-PENDING

## Ziel und Umfang

Der [Intake-Snapshot](../intake/raw/2026-10-07/corpus-v10/README.md) macht den
erschlossenen Projektstand, die Matrix und drei Sichtungs-Skills im Repository
prüfbar. GitHub-Veröffentlichung und Merge wurden vom Nutzer beauftragt.

Basis: `99bd8ca81f0b3c12a704105b4d2b1f7b59a3a420` auf `main`.
Änderungen beschränken sich auf `docs/intake/` und diesen Bericht in `docs/audit/`.
GOLD, Runtime, CI-Konfiguration, Receipts und Originalquellen bleiben unverändert.

## Aktionen und Prüfungen

- [x] Quellindex als bestätigte Version 10 materialisiert und SHA-256 festgehalten.
- [x] 63 erfasste Quellen, 11 offene Kandidaten, 192 Punkte, 38 Relationen und
  5 Konflikte als abgeleiteten Snapshot übernommen.
- [x] Private Originale, projektfremde Medienmetadaten und Suchcursor nicht exportiert.
- [x] Alle drei Skill-Pakete einschließlich Referenzen/UI-Dateien bytegleich kopiert.
- [x] JSON-/CSV-Konsistenz, vollständige Übernahme nach dokumentierter Feldreduktion,
  lokale IDs, Skill-Dateien, Manifest-Hashes und relative Links geprüft.
- [x] `make verify`: 665 Tests und 165 Untertests bestanden; Pointer, Ports und
  Claim-Lint bestanden. 104 Warnungen im bestehenden Python-Testlauf.
- [x] `make lint`, `black --check src/ tools/ tests/`, `make type-check` und
  `bandit -c .bandit.yaml -r src/ tools/` bestanden.

Die lokale Umgebung wurde mit der vorgeschriebenen uv-Version 0.12.18 aus dem
bestehenden `uv.lock` installiert. Es wurden keine Lockfiles oder Abhängigkeiten
geändert. Remote-CI und Merge-Ergebnis sind am zugehörigen PR nachzuprüfen; dieser
vorab erstellte Bericht behauptet keinen bereits erfolgten Merge.

## Grenzen und offene Punkte

- [ ] EXPORT-01–03: veraltete interne Versionsmetadaten, abweichender
  Sammelbericht-Zähler und gemischtes Claim-Tag-Vokabular im Quellindex.
- [ ] 5 aktive Teil-Lektüren und 11 Metadatenkandidaten; 2 Research-Radar-Berichte
  bleiben zurückgestellt.
- [ ] Originallektüre, semantischer Readback, wissenschaftliche/Runtime-Validierung
  und Kanonentscheid sind durch die Integrationsprüfungen nicht geleistet.

Die Exportprüfung belegt die dokumentierte Übernahme des Indexstands, nicht die
Korrektheit sämtlicher historischer Lesebehauptungen. Quellen, generierte Reviews
und ihre Kopien erzeugen durch Wiederholung keine unabhängige Evidenz.

## Rückweg

Bei Fehlern den Snapshot durch einen Folge-PR als überholt kennzeichnen und eine
korrigierte Fassung danebenstellen. Öffentliche Kopien lassen sich nicht
zuverlässig zurückrufen. Der private Originalindex wurde nicht verändert.
