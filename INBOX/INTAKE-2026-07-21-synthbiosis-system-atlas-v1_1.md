# INTAKE-2026-07-21 — Synthbiosis Systematlas v1.1 (Bundle-Witness)

**Status:** ROHSEDIMENT — Intake-Dokument, keine Kanonisierung
**Claim-Tags dieser Datei:** [FACT] [INFERENZ] [VOID] [CONTEXT]

```yaml
artifact:
  title: Synthbiosis Systematlas v1.1
  artifact_type: historical_internal_bundle
  status: ROHSEDIMENT
  authority_effect: none
  promotion_effect: none
  human_decision_required: true

integrity:
  archive:
    zip_file_entry_count: 11
    zip_directory_entry_count: 1
    zip_total_entry_count: 12
    manifest_hashed_file_count: 10
    manifest_self_hashed: false
    total_expected_files:
      - 00_SYSTEM_ATLAS.md
      - 01_DUAL_FORMAT_CLAIM_BRIDGE.md
      - 02_TESSER3TAKT_TRANSITION_ENGINE.md
      - 03_GRIMM_NEKTAR_UI_LAB.md
      - 04_GOVERNANCE_RECEIPTS_FALSE_SAFETY.md
      - 05_RESEARCH_VALIDATION_GATE.md
      - 06_PHOTONIC_THERMAL_ROSETTA.md
      - 07_MODULE_CONTRACTS.yaml
      - 08_HISTORICAL_STATUS_CROSSWALK.md
      - 09_SYNTHESIS_RECEIPT.json
      - README.md
  container_variant_drive:
    sha256: "3dd76c1ff7aab6e1b65de7c820d1da0da5e5eab9c713c3d3a494471efa61ab88"
    size_bytes: 27209
    source: Google Drive (Synthbiosis_Systematlas_v1_1.zip)
    file_entry_count: 11
    directory_entry_count: 1
    receipt_self_sha256: "156e146dc0993ef45087cf93cfb765c8eeb90a2bfa545f42331ebaf95a5c18f5"
  container_variant_original:
    sha256: "9de320ff4860b8570490e9775cce47cc70f3462a88e72fa8154f34045e60ba6a"
    size_bytes: 26043
    source: vom Projektinitiator bereitgestellte ZIP-Datei
    file_entry_count: 11
    directory_entry_count: 0
    receipt_self_sha256: "156e146dc0993ef45087cf93cfb765c8eeb90a2bfa545f42331ebaf95a5c18f5"
  container_comparison:
    normalized_file_names_match: true   # elf identische Dateinamen beidseitig
    manifest_hashes_match: true         # zehn Manifest-Hashes im Drive-Container verifiziert
    receipt_self_hash_match: true       # 156e146d... beidseitig identisch
    disposition: SAME_INNER_PAYLOAD_DIFFERENT_CONTAINER
    note: >
      Es existieren zwei verschieden verpackte ZIP-Container desselben
      Inhalts. Der frühere Digest 9de320ff... gehört zur vom
      Projektinitiator bereitgestellten Original-Variante (26043 Bytes,
      elf Datei-Einträge, kein Verzeichniseintrag); der Drive-Container
      (27209 Bytes) trägt zusätzlich einen Verzeichniseintrag und andere
      ZIP-Metadaten. Alle elf inneren Dateien stimmen überein: die zehn
      Manifest-Hashes wurden am Drive-Container direkt verifiziert, und
      das byte-identische Receipt (Selbsthash beidseitig gleich) bindet
      dieselben zehn Hashes; die Original-Seite ging über die vom
      Projektinitiator gelieferten Referenzwerte ein.
  manifest_file: 09_SYNTHESIS_RECEIPT.json
  manifest_hashes_verified: true
  manifest_hashes_checked: 10
  manifest_hashes_failed: 0
  yaml_syntax_valid: true
  json_syntax_valid: true
  path_safety_verified: true
  duplicate_filenames: none
  verification_date: 2026-07-21

provenance:
  historical_repo_ref: 29390c3d7676a050465568c15dc1caebf62718d8
  current_repo_ref: 683ea6c079d6099834a5edab44dac1a1ee87cb73
  source_container: user-supplied ZIP (Google Drive)
  bundle_created_at: "2026-07-16T01:24:28+02:00"
  protected_origin_present: true
  public_safe_reduction_required: true
```

## Befund (privacy-reduziert)

- [FACT] Das Bundle existierte bereits vollständig: Der Drive-Container
  enthält zwölf ZIP-Einträge — einen Verzeichniseintrag und **elf
  Datei-Einträge** unter `work/synthbiosis-system-atlas-v1_1/` — mit exakt
  der erwarteten Struktur (`00_SYSTEM_ATLAS.md` … `09_SYNTHESIS_RECEIPT.json`
  plus `README.md`; per `ZipInfo.is_dir()` gemessen, nicht aus Pfadpräfixen
  abgeleitet).
- [FACT] `07_MODULE_CONTRACTS.yaml` war **nicht verloren**, sondern im Bundle
  verborgen: Das Problem war Container-/Discovery-Verlust, kein Datenverlust.
  Die Datei ist syntaktisch valides YAML mit Modulverträgen M1–M6, Flüssen und
  globalen Invarianten.
- [FACT] `09_SYNTHESIS_RECEIPT.json` war ein bislang unsichtbarer
  Bundle-Witness: Es belegt die Bundle-Zusammenstellung (Datum, Methoden-Scope,
  Repo-Witness-Ref) und die Dateiintegrität **innerhalb seines Scopes** —
  alle zehn SHA-256-Dateihashes wurden am 2026-07-21 verifiziert.
- [CONTEXT] Das Receipt nimmt sich selbst nicht in die Hash-Liste auf
  (korrekt, sonst zirkulär) und deckt den äußeren ZIP-Container nicht ab.
- [FACT] Das Receipt belegt **keine** Wahrheit, Authority oder externe
  Validierung: `authority_effect: none`, `public_promotion: none` stehen im
  Receipt selbst; die `limits`-Liste nennt u.a. eine nicht analysierbare
  Null-Byte-Quelle und heterogene Hardware-Quellen.
- [INFERENZ] Einzelne Bundle-Dateien waren bereits separat in Drive sichtbar;
  der Paketkontext (Lesereihenfolge, Modulzusammenhang, Receipt-Bindung) war
  dabei nicht zuverlässig rekonstruierbar. Erst der Container macht den
  Verteilerkasten als Ganzes prüfbar.
- [CONTEXT] Das Bundle wird als **historischer Integrationskörper** intaken,
  nicht als neuer Masterindex. Es referenziert den damaligen Repo-Stand
  `29390c3d…`; der heutige `main` ist `683ea6c…`. Älter ≠ falsch,
  neuer ≠ automatisch überlegen — Abgleich siehe Crosswalk.
- [FACT] Die Container-Frage ist aufgelöst: Der früher beobachtete Digest
  `9de320ff…` gehört zur vom Projektinitiator bereitgestellten
  Original-ZIP-Variante. Beide Container tragen denselben inneren Inhalt
  (Disposition `SAME_INNER_PAYLOAD_DIFFERENT_CONTAINER`, siehe
  `container_comparison`). Außenhash-Differenz erklärt sich durch
  Verpackung (Verzeichniseintrag, ZIP-Metadaten), nicht durch Inhalt.

## Grenzen dieses Intakes

- Das ZIP selbst wird **nicht** ins öffentliche Repository übernommen;
  geprüft wurde in einem temporären lokalen Pfad.
- Keine privaten Namen, Szenen, Gesprächsauszüge oder autobiographischen
  Details wurden übernommen (`protected_origin_present: true` →
  `public_safe_reduction_required: true`).
- Bundle vorhanden ≠ Repo-repräsentiert. Hash stimmt ≠ Inhalt ist wahr.
  Receipt vorhanden ≠ Authority.
- Jede Kanonisierung, Promotion oder Modulübernahme benötigt eine eigene
  menschliche Entscheidung.

## Weiterführend

- Gegenprüfung je Bundle-Datei: `docs/audit/SYNTHBIOSIS_BUNDLE_CROSSWALK_v0_1.md`
- Anschlussplanung ohne Kopplung: `docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md`
