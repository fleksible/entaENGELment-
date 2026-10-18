# Report: GOLD-Änderungen VOIDMAP und Runtime-Spec

**Datum:** 2026-10-18
**Fokus:** GOLD-Punkte #311 und #278

## Ziel
Die offenen GOLD-Punkte aus #311 (überfällige VOIDs) und #278 (Runtime-Vertrag) nach dem
Annex-Prozess umsetzen. Ablauf: Owner-Auftrag „auf zum Gold“, Plan als Checkpoint,
Owner-Auswahl am 2026-10-18, dann minimal-invasive Änderung mit `GOLD-CHANGE:`-Commits.

## Aktionen
- [x] PR #404 auf Owner-OK nach `main` gemergt (alle 42 Checks grün)
- [x] **VOID-011 → CLOSED** (`VOIDMAP.yml`)
  - `tools/void011_metrics_export.py` erzeugt `data/metrics/void011_resonance_metrics.csv` + `.meta.json`:
    - ECI/PLV/MI/FD/PF, Seeds 7/42 × Kopplung 0.1/0.35/0.8
    - jede Zeile `SIMULATION_PROXY`
    - `csv_sha256` im Meta, kein Zeitstempel [FACT]
  - Drift-Check `--check` und `tests/unit/test_void011_metrics_export.py` (5 Tests) [FACT]
  - **Bug gefunden und behoben** [FACT]:
    - `fd()` normierte die Higuchi-Kurvenlänge mit 1/k statt 1/k². Die Steigung war um −1 verschoben und klemmte fast immer auf 1.0.
    - Weißes Rauschen ergab 1.0 statt ≈ 2.0, ein Random Walk 1.0 statt ≈ 1.5.
    - Zwei Referenztests ergänzt: ohne Fix rot, mit Fix grün.
- [x] **VOID-010:**
  - `target_date` 2026-07-15 → 2027-01-31, Begründung in `notes`
  - Gerüst `data/spectra/`: CSV nur mit Kopfzeile, Schema `[SPEC-WIP]`, README
  - `tools/spectra_table_lint.py` (Quellenpflicht) mit 11 Tests [FACT]
  - Status bleibt `IN_PROGRESS`, keine Daten erfunden
- [x] **`spec/runtime_eventlog_v0_1.json`** (bleibt `draft`/`[SPEC-WIP]`):
  - `VOID_CLOSED`: `required_one_of [evidence_ref, review_ref]`
  - `CLAIM_CREATED`: `required_one_of [claim_text, claim_hash, claim_ref]` + `reduced_forbidden_fields [claim_text]`
  - `field_rules` erklärt die Semantik und schließt Laufzeit-Erzwingung ausdrücklich aus
  - `tools/eventlog_spec_check.py` mit 11 Tests; alle CLAIM_CREATED-Events der ERK-Fixtures erfüllen den Vertrag [FACT]
- [x] **Claim-Tags:** Owner-Entscheid „Status quo bestätigen“ in `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md` dokumentiert
- [x] Nachgezogen: UI-Spiegel `ui-app/lib/voidmap-parser.ts`, `docs/voids_backlog.md`, VOID-Dokus, Spine-Doku
- [x] Folgefehler aus #404 behoben: black-`target-version` nur `py310`. Mit py314 warnte Black unter älterem Python.

## Nicht getan
- **`policies/claim_tags_v0_2.yaml` bleibt byte-identisch.** Ein Eintrag des Entscheids dort brach
  16 ERK-Tests: Guard-Entscheidungen binden den `policy_digest` der Datei, jede Byte-Änderung
  macht sie ungültig [FACT]. Der Entscheid verlangt keine Logikänderung, deshalb steht er in der Audit-Doku.
- Kein ERK-Umbau für Hash-only-Claims. Der ERK protokolliert privat mit `claim_text`, und
  `reduce_public_export` entfernt den Text bereits (Invariante 11).
- Kein Literatur-Scan für VOID-010. Forschungsarbeit mit ≥ 5 begutachteten Quellen bleibt beim Owner.
- Label `GOLD-CHANGE` existiert im Repo nicht. Der PR trägt die Kennzeichnung im Titel und das Label `governance`.

## Risiken
- [RISK] Der FD-Fix ändert alle FD-Werte, typischerweise um +1 gegenüber vorher. Wer frühere FD-Ausgaben
  verglichen hat, sah die geklemmte Untergrenze. Im Repo nutzt außer dem Toy-Datensatz niemand FD.
- [RISK] Die Deny-/Ask-Regeln greifen nur bei Claude-Code-Dateiwerkzeugen. Die VOID-010-Änderung lief per
  Skript und löste darum keine Rückfrage aus; die Freigabe lag vorher explizit vor.

## Offene Punkte
- [ ] ☐ #311 nach Merge schließen (VOID-011 geschlossen, VOID-010 nicht mehr überfällig); der PR verlinkt es mit `Closes`
- [ ] ☐ #278 nach Merge schließen (alle fünf Punkte erledigt); der PR verlinkt es mit `Closes`
- [ ] ☐ VOID-010: Literatur-Scan, Tabelle füllen und mit dem Lint prüfen
- [ ] ☐ VOID-028 kann jetzt auf den SIMULATION_PROXY-Export von VOID-011 verweisen
- [ ] ☐ Label `GOLD-CHANGE` anlegen, falls gewünscht (`annex.md` sieht es vor)

## Artefakte
- `VOIDMAP.yml`, `spec/runtime_eventlog_v0_1.json`
- `data/metrics/void011_resonance_metrics.csv`, `data/metrics/void011_resonance_metrics.meta.json`
- `data/spectra/spectra_sources.csv`, `data/spectra/spectra_sources.schema.json`, `data/spectra/README.md`
- `tools/void011_metrics_export.py`, `tools/spectra_table_lint.py`, `tools/eventlog_spec_check.py`
- `tests/unit/test_void011_metrics_export.py`, `tests/unit/test_spectra_table_lint.py`, `tests/unit/test_eventlog_spec_check.py`, `tests/unit/test_core5_metrics.py`
- `src/core/metrics.py`, `src/tools/toy_resonance_dataset.py`, `ui-app/lib/voidmap-parser.ts`
- `docs/voids_backlog.md`, `docs/voids/VOID-010_taxonomy_and_spectra.md`, `docs/voids/VOID-011_resonance_metrics.md`
- `docs/governance/RUNTIME_EVENTLOG_SPINE_v0_1.md`, `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md`
