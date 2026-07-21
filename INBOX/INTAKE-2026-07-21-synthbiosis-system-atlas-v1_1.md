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
  bundle_sha256: "3dd76c1ff7aab6e1b65de7c820d1da0da5e5eab9c713c3d3a494471efa61ab88"
  bundle_sha256_note: >
    Verifizierter Digest des tatsächlich geprüften ZIP-Containers
    (Google Drive, Dateiname Synthbiosis_Systematlas_v1_1.zip, 27209 Bytes).
    Ein zuvor extern beobachteter Erwartungswert
    (9de320ff4860b8570490e9775cce47cc70f3462a88e72fa8154f34045e60ba6a)
    wurde NICHT reproduziert. Da alle inneren Receipt-Hashes stimmen,
    ist die plausibelste Lesart eine Container-Diskrepanz (Re-Zip desselben
    Inhalts erzeugt andere Container-Digests); die Identität des damals
    beobachteten Containers bleibt UNDETERMINED. Kein stilles Akzeptieren:
    menschliche Kenntnisnahme erforderlich.
  manifest_file: 09_SYNTHESIS_RECEIPT.json
  manifest_hashes_verified: true
  manifest_hashes_checked: 10
  manifest_hashes_failed: 0
  file_count: 10
  zip_entry_count: 11
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

- [FACT] Das Bundle existierte bereits vollständig: elf ZIP-Einträge
  (ein Verzeichnis, zehn Dateien) unter `work/synthbiosis-system-atlas-v1_1/`,
  Struktur exakt wie erwartet (`00_SYSTEM_ATLAS.md` … `09_SYNTHESIS_RECEIPT.json`,
  `README.md`).
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
- [VOID] Offen bleibt die Container-Identität des früher beobachteten Digests
  (siehe `bundle_sha256_note`).

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
