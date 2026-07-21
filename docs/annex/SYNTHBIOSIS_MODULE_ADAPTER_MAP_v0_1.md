# SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** none
**Promotion-Effect:** none
**Human-Decision-Boundary:** required
**Datum:** 2026-07-21
**Quellen:** Synthbiosis Systematlas v1.1 (Bundle-Witness, siehe
`INBOX/INTAKE-2026-07-21-synthbiosis-system-atlas-v1_1.md` und
`docs/audit/SYNTHBIOSIS_BUNDLE_CROSSWALK_v0_1.md`); Evidence Routing Kernel
v0.1a (PR #314, offen — noch nicht main).

---

## 1. Ziel

Diese Map dokumentiert die **kleinste relationale Anschlussform** zwischen den
sechs Bundle-Modulen und dem Evidence Routing Kernel (ERK):

| Kürzel | Modul |
|---|---|
| M1 | Dual-Format Claim Bridge |
| M2 | tesser3TAKT Transition & Reentry |
| M3 | Grimm/Nektar Private UI-LAB |
| M4 | Governance / Receipts / False-Safety |
| M5 | Research & Validation Gate |
| M6 | Photonic/Thermal ROSETTA Airlock |
| ERK | Evidence Routing Kernel v0.1a (PR #314) |

Die Map ist **kein neuer Orchestrator**, kein Runtime-Vertrag und keine
Kopplung. Nichts hierin wird enforced; jede spätere Implementierung benötigt
einen eigenen Plan-first-Checkpoint und eine menschliche Freigabe.

## 2. Verbindliche Unterscheidungen

### 2.1 M1 → ERK (Bridge-Record als Material + Relation)

Mapping-Kandidaten (keine Implementierung):

| M1-Feld (bridge_record) | ERK-Gegenstück | Anmerkung |
|---|---|---|
| `source_pointer` | `MaterialRef` (locator/digest/origin) | Pointer, kein Inhalt |
| `claim_status` / Claim-Satz | `ClaimCandidate` (claim_tag/claim_text) | Text bleibt privat-reduzierbar |
| `preserved_relation` | `EvidenceRelation` | Relationstyp bewusst begrenzt |
| `known_loss` | Adapter-Metadatum / begrenzter Reason-Text | bleibt sichtbar; kein kontrollierter Reason-Code-Slot |
| `falsifier` | Anforderung an M5 (Research Gate) | ERK prüft Struktur, nicht Falsifizierbarkeit |
| `rollback` | Pointer auf `HumanDecision(WITHDRAW)` / `Retraction` | append-only, kein eigenes Rollback-Feld |
| `source_register`, `transferred_property`, `intended_use` | **kein** ERK-Gegenstück | echt neue Bridge-Felder; verbleiben im Adapter |

Dabei gilt:

- `MOTIVATES` und `CONTEXTUALIZES` sind **keine Promotionsbeweise**
  (deckungsgleich mit ERK-Invarianten 3/4 und Reason-Codes
  `METAPHOR_IS_NOT_EVIDENCE`, `PROVENANCE_IS_NOT_EVIDENCE`).
- Bridge-Records dürfen **keine Gleichheit** zwischen Quellen- und
  Zieldomäne behaupten (`no_identity_shortcut`).
- **Known Loss muss sichtbar bleiben:** Ein Adapter, der `known_loss`
  verwirft, ist fehlerhaft.

### 2.2 M2 → ERK (strikte Vokabular-Trennung)

Drei Entscheidungssysteme, die **nicht** ineinander übersetzt werden:

| System | Vokabular | Rolle |
|---|---|---|
| M2 tesser3TAKT | `PASS \| HOLD \| LOOP \| STOP` | lokale Navigations-/Reviewentscheidung |
| ERK Guard | `PROPOSE \| HOLD \| STOP` | strukturelle Durchlassentscheidung |
| ERK Human | `APPROVE \| REJECT \| DEFER \| WITHDRAW` | einzige Retagging-Quelle |

**Kein Adapter darf automatisch übersetzen:**

- `M2 PASS → HumanDecision(APPROVE)` — verboten (Invariante 5:
  M2-PASS ist kein Human-Approve; Invariante 12: HumanDecision bleibt
  menschlich).
- `M2 PASS → CLAIM_RETAGGED` — verboten.
- `M2 HOLD → Claim [VOID]` — verboten (Guard-State ist kein Claim-State).

Zulässig ist höchstens: M2 liefert ein **externes Navigationssignal** oder
einen **Materialpointer** (`MaterialRef` mit `kind: navigation_signal`,
Relation `CONTEXTUALIZES` — und damit per Definition keine Promotion).

### 2.3 M3 → M1/M4 (Angebotsformen, keine Diagnosen)

Grimm-/Nektar-Ausgaben sind:

- offered forms (Angebote, keine Feststellungen),
- narrative bzw. UI-Records,
- mögliche protected-origin Materialien (`visibility: private`),
- **keine Diagnose** und **kein automatischer Claim über eine Person**.

Nicht-Resonanz ist eine **gültige, terminale Rückmeldung** für die konkrete
Lesung und darf nicht umgedeutet werden. Ein M3-Record kann höchstens als
privates `MaterialRef` in M1 eingehen; sein Weg zu M4 führt ausschließlich
über M1-Brücken und menschliche Entscheidung.

### 2.4 M4 → ERK (Receipt-Typen nach Belegfunktion)

Ordnung nach **Belegfunktion**, nicht nach vermeintlicher Wahrheitsstärke:

| Receipt-Typ | ERK-Relationskandidat | proves | does_not_prove |
|---|---|---|---|
| `repo_hmac` | `PROVENANCE_ONLY` | signierte kanonische Payload im Schlüssel-/Toolscope | externe Realität, semantische Wahrheit |
| `p7_sha_chain` | `PROVENANCE_ONLY` | lokale Reihenfolge, manipulationssensitive Inhalte | Identität, unabhängige Verwahrung, HMAC-Vertrauen |
| `review_relay` | `CONTEXTUALIZES` | dass ein Review mit Scope übermittelt wurde | Repository-Attestation, Humanentscheid |
| `status_receipt` | `PROVENANCE_ONLY` | protokollierter Status zu einem Zeitpunkt | vollständige Spezifikation, unabhängige Validierung |
| `empirical_bundle` | `SUPPORTS` \| `CONTRADICTS` — **nur nach M5-Prüfung** | Daten, Protokoll, Auswertung im Design-Scope | Generalisierung außerhalb des Designs |

Jede spätere Implementierung muss `proves` und `does_not_prove` explizit
mitführen (Bundle-Vorschlag `evidence_semantics`; im ERK bewusst nicht
enthalten — Reason-Codes sind Entscheidungsgründe, keine Beweisfelder).

### 2.5 M5 → ERK (methodische Prüfung, keine Wahrheitsentscheidung)

M5 entscheidet **nicht** über Claim-Wahrheit. M5 darf erzeugen:

- „methodisch zulässiger Kandidat",
- `HOLD`,
- „fehlende Voraussetzung",
- Falsifier,
- Messplan,
- Evidenzklasse,
- Daten-/Ethik-/Privacy-Blocker.

M5 darf **keine HumanDecision synthetisieren** (deckungsgleich mit
ERK-Invariante 2). Ein M5-Ergebnis kann höchstens als Material/Relation in
einen `TransitionRequest` eingehen, dessen Guard-Bewertung und menschliche
Entscheidung unverändert dem ERK-Protokoll folgen.

### 2.6 M6 → M5 → M1 → M4 (einziger Hauptpfad)

```
physischer Komponentenbefund
    → M5 methodische Prüfung
    → M1 getrennte semantische Brücke
    → M4 Governancewirkung
```

**Nicht zulässig:** `M6 → direkte Authority`, `M6 → menschlicher Consent`,
`M6 → moralische Wahrheit` (Invariante 7: Hardware ist keine Ethik;
Invariante 8: Simulation ist keine Empirie).

## 3. Contract-Gap-Tabelle

```yaml
- source_module: M1
  target_module: ERK
  current_contract: bridge_record (Bundle 01, YAML-Skizze)
  repo_representation: keine (ERK in PR #314; Bridge-Adapter existiert nicht)
  missing_fields: [source_register, transferred_property, known_loss, falsifier, intended_use]
  prohibited_shortcut: bridge_record als direkter CLAIM_RETAGGED-Auslöser
  failure_mode: Metapher wird über SUPPORTS-Relation als Evidenz eingeschleust
  human_boundary: jede Promotion braucht HumanDecision(APPROVE)
  recommended_phase: 2A

- source_module: M2
  target_module: ERK
  current_contract: tesser_input/tesser_output (Bundle 02)
  repo_representation: tesser3takt-ANNEX-Doku; UI-seitig PR #304/#312 (offen)
  missing_fields: [reason_codes-Abgleich, receipt_pointer-Semantik]
  prohibited_shortcut: PASS->APPROVE, PASS->RETAG, HOLD->VOID (jede Automatik)
  failure_mode: Navigationsentscheidung wird als epistemischer Status gelesen
  human_boundary: M2 liefert höchstens Signale/Pointer; nie Entscheidungen
  recommended_phase: nach 2A, nur als Signal-Adapter

- source_module: M3
  target_module: M1/M4
  current_contract: scene_contract (Bundle 03)
  repo_representation: nur Prinzipien (PRIVACY_BOUNDARY, ANTI_CAPTURE_POLICY)
  missing_fields: [source_freeze_manifest, public_allowlist, namespace_crosswalk]
  prohibited_shortcut: UI-Record als Framework-Beweis oder Personen-Claim
  failure_mode: private Herkunft diffundiert in öffentliche Artefakte
  human_boundary: Consent-State und Nicht-Resonanz sind menschlich, terminal
  recommended_phase: 2D (nur Source-Freeze-Manifest, kein Import)

- source_module: M4
  target_module: ERK
  current_contract: receipt_types + false_safety_check (Bundle 04)
  repo_representation: F7-Methodsheet, Ledger/Receipt-Mechanik (scoped), ERK-Reason-Codes (PR #314)
  missing_fields: [receipt_type, proves, does_not_prove, scope, authority_effect]
  prohibited_shortcut: Receipt-Gültigkeit als Claim-Wahrheit
  failure_mode: F7/FALSE_OK — grün trotz fehlender Grundlage
  human_boundary: Authority ändert nur menschliche Entscheidung
  recommended_phase: nach 2A (evidence_semantics als eigenes Schema-Delta)

- source_module: M5
  target_module: ERK
  current_contract: Eingangsklassen + Airlock (Bundle 05)
  repo_representation: keine (MISSING_REPO_SAFE)
  missing_fields: [gesamtes Gate als ANNEX-Vertrag]
  prohibited_shortcut: normativer Wert als Biomarker; Simulation als Empirie
  failure_mode: HRV o.ä. wird als Resonanz-/Wahrheitsmeter gelesen
  human_boundary: Ethik-/Zuständigkeitsentscheidung liegt außerhalb des Systems
  recommended_phase: 2B

- source_module: M6
  target_module: M5
  current_contract: component_claim (Bundle 06)
  repo_representation: keine (MISSING_REPO_SAFE)
  missing_fields: [Kalibrierung, Unsicherheit, Rohdaten-Pointer, Threat-Model]
  prohibited_shortcut: Hardware->Authority, Hardware->Ethics-PASS
  failure_mode: Bauteileigenschaft und Governancebedeutung im selben Satz
  human_boundary: Semantik-Zuordnung nur als separates M1-Bridge-Record nach Review
  recommended_phase: 2C (erst nach 2B)
```

## 4. Keine erfundene Vollständigkeit

`UNDETERMINED` bleibt ausdrücklich stehen für:

- die Container-Identität des früher beobachteten Bundle-Digests
  (Intake, `bundle_sha256_note`);
- den heutigen Zustand der privaten P7-Gates (privater Korpus liegt dieser
  Prüfung nicht vor);
- die Frage, ob `07_MODULE_CONTRACTS.yaml`-`stops` als typisiertes Schema
  tragfähig sind, bevor Prinzipien, Interpretationsverbote und technische
  Fehler getrennt sind.

Nichts davon wird ästhetisch geschlossen.

## 5. Noch nicht genehmigte Folgephasen (nur Vorschläge, keine Dateien)

| Phase | Inhalt | Voraussetzung | kleinster nächster Schritt |
|---|---|---|---|
| 2A | M1 Bridge-Adapter (`src/core/evidence_bridge_adapter.py` + Tests + ANNEX-Doku) | PR #314 gemergt oder stabiler Adapterzielstand | Feld-Mapping aus §2.1 als Schema-Entwurf reviewen |
| 2B | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` (reduzierte ANNEX-Fassung von Bundle 05) | eigener Plan-first-/Safety-Checkpoint | Freigabeentscheidung |
| 2C | Photonic/Thermal Airlock: nur atomare Komponentenclaims | 2B existiert | ersten Bench-Claim-Text reviewen |
| 2D | Grimm/Nektar Source-Freeze-Manifest (Hash, Purpose, Inventar, Datenfluss, Providergrenzen, Known Limits, Lizenz, Public-Allowlist, private Ausschlüsse) | kein P7-Import | Manifest-Zuschnitt entscheiden |
| 2E | Annex F v0.3: revisionsgebundener Source-Pointer für PR #304-Quellen; Gate-0-Korrekturen als reduzierte ANNEX-Fassung; Rohdaten/Scanner/24-42-H0 bleiben HOLD | Entscheidung zu PR #304 | prüfen, ob ein Source-Pointer genügt |
| 2F | NotebookFM Source Membrane: Rest-Vertrag für Reader/Retrieval, nachdem Privacy Boundary, Claim Mapping und Source Decoration Map den Großteil abdecken | kein Import des biographischen Korpus | Abdeckungslücke präzise benennen |

## 6. Grenzen dieser Map

- Kein Modul wird implementiert, importiert oder gekoppelt.
- Kein zweites Entscheidungssystem, kein dritter Masterindex.
- Formale Werkzeuge (z.B. Wolfram) dürfen später ausschließlich deklarierte
  Graphen/Mengen/Erreichbarkeit/Zyklusfreiheit prüfen — niemals Wahrheit,
  Geltung, Bewusstsein, Biographie oder Resonanzqualität.
- Alle sechzehn Pflichtinvarianten des Stitching-Passes gelten unverändert;
  diese Map macht sie nur relational sichtbar.
