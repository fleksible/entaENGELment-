# Report: Rosetta Taxonomy & Philology Stress Slice v0.1

**Datum:** 2026-09-23  
**Fokus:** Rosetta Taxonomy Stress

## Ziel

Den Pre-Implementation-Red-Team-Befund als kleinen ANNEX/Intake-Slice umsetzen,
ohne Rosetta v0.1 still zu migrieren und ohne Runtime-, GOLD-, VOID-, FEP-,
Ledger-, zGWSTN- oder Evidence-Bridge-Promotion.

## Aktionen

- [x] `TransformationDelta` auf `preserved / lost / introduced` reduziert.
- [x] Mapping-Topologie von semantischem Delta getrennt:
      `ONE_TO_ONE / ONE_TO_MANY / MANY_TO_ONE / MANY_TO_MANY` plus Coverage.
- [x] Attribution von beobachtetem Delta getrennt:
      Interpreter, Language Affordance, Historical Path, Editorial Choice,
      Reader Rebinding.
- [x] Kenogramm-Status als dimensionsübergreifendes Legacy-Problem markiert und
      Kandidatenachsen für Epistemik, Mapping, Consent, Policy und Visibility
      beschrieben.
- [x] Fünf Stress-Fixtures angelegt:
      `ousia`, `energeia`, `logos`, `hen/agathon`,
      `universal-harmony-collapse`.
- [x] Pytest-Guards für Question Provenance, Nicht-Promotion,
      Delta/Topology-Trennung, Attribution und Anti-Collapse ergänzt.
- [x] Historische Quellen im Fixture-Paket als Evidence Catalog referenziert;
      sie sind Review-Ziele und keine kanonische Philologie.
- [x] Formatter-Gate iterativ repariert, ohne Fixture-Semantik zu verändern.

## Verifikation

Vollständig grüne PR-CI auf Head
`139adae118fcf3e3d615cde956c7321d5adaa831`:

- CI Pipeline - entaENGELment Framework: SUCCESS
- Metatron Guard: SUCCESS
- Policy Lint: SUCCESS
- Smoke Tests: SUCCESS
- DeepJump CI: SUCCESS
- Tests: SUCCESS
- Python Quality: SUCCESS

## Nicht getan

- Keine Änderung an `docs/spec/tesser3takt_hud_v0_2.md`.
- Keine Änderung am HUD-/Runtime-Schema.
- Keine Änderung an `ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1.md`.
- Kein zGWSTN-Reentry in diesem Slice.
- Kein Umbau von `src/core/evidence_bridge_adapter.py`.
- Kein FEP-/Active-Inference-Mechanismus.
- Kein Ledger-, Merkle-DAG- oder Blockchain-Umbau.
- Keine GOLD-, Policy-, Receipt- oder `VOIDMAP.yml`-Mutation.
- Keine neue VOID-ID.

## Risiken

- Die Taxonomien sind DERIVED/HOLD und noch nicht durch einen unabhängigen
  Human Reader reentered.
- `languageAffordance` bleibt eine Attributionshypothese und darf nicht in
  sprachlichen Determinismus kippen.
- Die philologischen Fixtures testen Transformationsformen; sie sind keine
  abschließende historische Bedeutungsrekonstruktion.
- Ownership und Lifecycle von `known_loss` bleiben weiterhin offen.
- Eine spätere HUD-Migration der Kenogramm-Dimensionen ist ausdrücklich noch
  nicht entschieden.

## Offene Punkte

- [ ] Human Reentry: Sind Transformation, Mapping und Attribution klar getrennt?
- [ ] Prüfen, ob `introduced` für alle Stressfälle akteursneutral genug bleibt.
- [ ] Prüfen, ob `WITHHELD` vollständig aus Consent + Visibility + Scope
      ableitbar ist oder eine eigene UI-Darstellung benötigt.
- [ ] Erst danach Rosetta v0.2 als Contract-Kandidat entwerfen.
- [ ] zGWSTN erst gegen akzeptierte Translation Witnesses reentern.
- [ ] FEP und Ledger nur als spätere Crosswalks prüfen.

## Artefakte

- `docs/intake/raw/ROSETTA_TRANSFORMATION_TAXONOMY_v0_1.md`
- `docs/intake/raw/ROSETTA_MAPPING_TOPOLOGY_v0_1.md`
- `docs/intake/raw/ROSETTA_ATTRIBUTION_TAXONOMY_v0_1.md`
- `docs/intake/raw/KENOGRAM_STATUS_DIMENSIONS_v0_1.md`
- `docs/narratives/grimm2/fixtures/rosetta_philology_stress_fixtures_v0_1.json`
- `tests/unit/test_rosetta_philology_stress_fixtures.py`
