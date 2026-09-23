# Report: Rosetta-Membran Counterfixtures v0.1

**Datum:** 2026-09-23  
**Fokus:** Rosetta Translation Fixtures

## Ziel

Sieben negative/boundary Counterfixtures für eine kontextabhängige,
semipermeable Rosetta-Übersetzungsmembran als DERIVED/HOLD-Slice anlegen.

## Aktionen

- [x] Intake-Contract ohne Runtime-/Policy-Promotion angelegt.
- [x] Sieben Fixtures modelliert:
  1. gleiches Wort / andere Lore,
  2. verschiedene Wörter / erhaltene Relation,
  3. one-to-many,
  4. Round-trip Loss,
  5. unübersetzter Rest,
  6. Question Shift,
  7. Protected Origin / Public Reduction.
- [x] Pytest-Guards für Inventar, Question Provenance, Known Loss, Rest,
      Asymmetrie und Nicht-Promotion ergänzt.

## Nicht getan

- Keine Änderung an `src/core/evidence_bridge_adapter.py`.
- Keine Änderung an `ZGWSTN_READ_ONLY_FRAME_v0_1.md`.
- Keine Änderung an GOLD, VOIDMAP, Policies oder Receipts.
- Keine Behauptung universaler Übersetzbarkeit.
- Kein Runtime-Writeback.

## Risiken

- Die Fixture-Semantik ist noch nicht durch einen fremden Reader validiert.
- `QuestionProvenance` ist in v0.1 dokumentarisch, noch kein Runtime-Typ.
- Ein späterer Adapter-Crosswalk könnte zeigen, dass einzelne Feldnamen anders
  an den bestehenden BridgeContext anschließen sollten.

## Offene Punkte

- [ ] ☐ Reader-Test: Wird Rest als legitime Differenz statt als Defizit gelesen?
- [ ] ☐ zGWSTN-Reentry: Soll `questionProvenance` vor `sharedNow` gebunden werden?
- [ ] ☐ Bridge-Crosswalk erst nach erfolgreichem Reader-/Fixture-Reentry prüfen.

## Artefakte

- `docs/intake/raw/ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1.md`
- `docs/narratives/grimm2/fixtures/rosetta_membrane_translation_fixtures_v0_1.json`
- `tests/unit/test_rosetta_membrane_fixtures.py`
- `OUT/rosetta_membrane_fixture_pass_2026-09-23.md`
