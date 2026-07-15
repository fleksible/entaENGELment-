# PROJECT_CONSTELLATION_MAP_v0_1

**Status:** [ANNEX] — projektuebergreifende Navigationskarte, keine Kanonisierung  
**Datum:** 2026-07-14  
**Inline-Claim-Tags:** [FACT] [INFERENZ] [VOID] [ANNEX] [CONTEXT]

## 0. Funktion und Grenze

[CONTEXT] Diese Datei zeigt Projektknoten, Funktion, Status, massgebliche Repo-Anker, Abhaengigkeiten, offene Luecken und Review-Stand.

[ANNEX] Sie ist kein neues Atlas-System, keine Source of Truth und kein Ersatz fuer `docs/masterindex.md`, `index/`, `VOIDMAP.yml`, Policies, Specs oder Receipts. Sichtbarkeit ist weder Wahrheit noch Kanonisierung.

### 0.1 Kontrolliertes Statusvokabular

[ANNEX] `repository_status` beschreibt ausschliesslich die Repo-Repraesentation:

- `present-current`
- `present-partial`
- `repository-lagging`
- `intake-only`
- `absent-or-unindexed`
- `archived`

[ANNEX] `repository-lagging` ist nur zulaessig, wenn ein datierter `external_state_pointer` auf ein Intake- oder Receipt-Artefakt den behaupteten reicheren Stand pruefbar macht. Fehlt dieser Pointer, muss der Knoten als `present-partial`, `intake-only` oder `absent-or-unindexed` gefuehrt werden.

[ANNEX] `authority_status` beschreibt die Geltung. Mehrere Werte werden als Liste, nicht als neuer Hybridstatus notiert:

- `gold`
- `governed`
- `annex`
- `draft`
- `intake`
- `receipt-only`
- `unresolved`

[ANNEX] `work_action` beschreibt die naechste Arbeitsbewegung und ist kein Authority- oder Repository-Status:

- `none`
- `clarify`
- `source`
- `formalize`
- `validate`
- `intake`
- `hold`

### 0.2 Claim- und Reviewmechanik

[FACT] Die verwendeten Claim-Tags stammen aus `policies/claim_tags_v0_2.yaml`. Diese Datei verwendet keine unregistrierten Tags wie `[PROPOSAL]` oder `[OPEN]`.

[ANNEX] `review_history` ist append-only zu fuehren. Ein spaeterer Review darf einen frueheren nicht ueberschreiben. Jeder Eintrag nennt mindestens Datum, Instanz, Scope und Ergebnisstatus. Ein uebermittelter Fremdreview wird als `user-relayed` markiert und nicht als direkt vom Repository attestiert ausgegeben.

### 0.3 Privacy-Reduktionsregel

[ANNEX] Strenge Reduktionsregel: Private Stränge duerfen als offene Knoten benannt, aber nicht erzaehlt oder aufgeloest werden. Nicht ins Repo gehoeren biographische Anker, private Symbolketten, persoenliche Bedeutungsprofile oder rekonstruierbare Gespraechspassagen. Fuer jeden uebernommenen Knoten bleibt nur die kleinste fuer Repo-Navigation, Guard oder Pruefung notwendige Struktur.

[FACT] Aktueller Reentry-Abgleich:

- `docs/audit/2026-07-14_tesser3takt_reentry_gap_audit.md` — privacy-reduzierte Delta-Matrix zwischen bestehender Repo-Struktur und aktuellem Arbeitsstand; keine neue Index- oder Kanonisierungsschicht

## 1. Projektknoten

```yaml
- id: ENTAENGELMENT-CORE
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: technischer, ethischer und governance-bezogener Rahmen
  repository_status: present-current
  authority_status: [gold, governed, annex]
  work_action: none
  primary_repo_anchor:
    - README.md
    - index/COMPACT_INDEX_v3.yaml
    - VOIDMAP.yml
    - policies/
    - spec/
  depends_on:
    - claim-hygiene
    - consent-and-gate-rules
    - deepjump-and-receipts
  open_voids:
    - technische und narrative Projektkoerper gemeinsam navigierbar machen
  review_history:
    chatgpt:
      - date: 2026-07-10
        id: architecture-pass-2026-07-10
        scope: project-constellation
        result: annex-pass-candidate
    claude: []
    human:
      - status: pending-content-decision

- id: SOURCE-OF-TRUTH-SPINE
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: Governance-Membran fuer Repo, Runtime, externe Quellen und Mensch
  repository_status: present-current
  authority_status: [draft, intake]
  work_action: clarify
  primary_repo_anchor:
    - docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md
  depends_on:
    - claim-tags
    - intake-first
    - provenance-and-retraction
  open_voids:
    - explizite Review- und Promotion-Entscheidung
  promotion_boundary: primaerer Anker ist keine automatische SoT-Geltung
  review_history: {}

- id: TESSER3TAKT
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: Uebergangs-, Projektions- und Reentry-Navigation
  repository_status: present-current
  authority_status: [annex]
  work_action: clarify
  primary_repo_anchor:
    - docs/tesser3takt/README.md
    - docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md
    - docs/audit/2026-07-14_tesser3takt_reentry_gap_audit.md
  depends_on:
    - source-decoration-guards
    - claim-hygiene
    - reentry
  open_voids:
    - Verhaeltnis zum erweiterten Grimm-Apparat
    - spaetere Pruefung weiterer Assembly-Schichten
    - praemetrische Relation-vor-Koordinate-Reihenfolge pruefen
    - Markov/non-Markov- und Landungsmodi nur als begrenzte Modellkandidaten formalisieren
  review_history:
    chatgpt:
      - date: 2026-07-10
        id: architecture-pass-2026-07-10
        scope: tesser3takt-annex-cluster
        result: annex-pass-candidate
      - date: 2026-07-14
        id: reentry-gap-audit-2026-07-14
        scope: repo-to-current-work-delta
        result: pass-candidate
    claude:
      - date: 2026-07-14
        id: strict-review-user-relayed-2026-07-14
        source: user-relayed
        scope: patch-and-sample-5-of-17-delta-rows
        result: pass-candidate-after-fixes
    human:
      - status: pending-content-decision

- id: GRIMM-APPARAT
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: narrativer Leseraum und maeutische Rezeptionsarchitektur
  repository_status: present-partial
  external_work_status: unanchored-intake
  authority_status: [unresolved, intake]
  work_action: intake
  primary_repo_anchor:
    - docs/narratives/grimm2/README.md
    - docs/narratives/grimm2/_template.md
  external_state_pointer: null
  depends_on:
    - entaengelment-ethics
    - tesser3takt-navigation
    - claim-and-layer-hygiene
  open_voids:
    - Reader-Membran und Schutz vor Fremddeutung
    - aktueller re-entry-faehiger Save-State
    - Aegypten-Griechenland-Bruecke
    - Ra-Skarabaeus-Logos-720-degree-Strang
    - heutige Rolle als adaptiver Muse- und Leseraum
    - mehrschichtige Zeitreise und Hermes-Uebersetzung ohne private Herkunftsoffenlegung
  promotion_boundary: neuere Chat-Synthesen zuerst als datiertes Intake sichern; ohne Pointer kein repository-lagging
  review_history:
    chatgpt:
      - date: 2026-07-10
        id: architecture-pass-2026-07-10
        scope: grimm-repository-representation
        result: intake-needed
      - date: 2026-07-14
        id: reentry-gap-audit-2026-07-14
        scope: privacy-reduced-grimm-delta
        result: hold-for-intake
    claude:
      - date: 2026-07-14
        id: strict-review-user-relayed-2026-07-14
        source: user-relayed
        scope: repository-lagging-proof-burden
        result: status-hardening-required
    human:
      - status: pending-content-decision

- id: ARK-FAMILY
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: technische und evidenzbezogene P4-/Cephalo-/Receipt-Artefaktfamilie
  repository_status: present-partial
  authority_status: [annex, receipt-only, unresolved]
  work_action: clarify
  primary_repo_anchor:
    - ark/p4/P4_TESTPLAN_INDEX.md
    - ark_cephalo_manifest_v2.json
  depends_on:
    - receipt-and-provenance-guards
  open_voids:
    - ein oder mehrere gekoppelte Projektkoerper
    - Beziehung zur aktuellen CephaloCamouflage-Lesart
  promotion_boundary: Receipts sind kein semantischer Kanon
  review_history: {}

- id: RESONANZKIEL
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: Architektur- und Uebergangsknoten zwischen Modellgrammatik, Resonanz und Navigation
  repository_status: absent-or-unindexed
  authority_status: [intake]
  work_action: intake
  primary_repo_anchor: []
  depends_on:
    - tesser3takt
    - grimm-apparat
    - claim-and-layer-hygiene
  open_voids:
    - aktuellen Save-State mit Provenienz als Intake sichern
    - Modell-, Physik-, Metapher- und Spec-Layer trennen
  promotion_boundary: keine Hochstufung durch rueckwirkend erkannte Chat-Kohaerenz
  review_history: {}

- id: FKP
  claim_status:
    repo_anchors: "[FACT]"
    status_assignment: "[INFERENZ]"
    open_questions: "[VOID]"
  role: Flux-Kondensations-Protokoll und claim-hygienische Pruefsynthese
  repository_status: absent-or-unindexed
  authority_status: [intake]
  work_action: intake
  primary_repo_anchor: []
  depends_on:
    - fluxon-thread
    - claim-hygiene
  open_voids:
    - FKP-v0.2 mit Provenienz als Intake sichern
    - strukturierte Energie und Informationsclaims getrennt halten
  promotion_boundary: keine SoT-, Spec- oder VOIDMAP-Integration ohne separaten Review
  review_history: {}
```

## 2. Navigationskette

```text
docs/START_HERE.md
        -> docs/masterindex.md
        -> docs/PROJECT_CONSTELLATION_MAP_v0_1.md
        -> bestehende Index-, VOID-, Governance-, Grimm-, tesser3TAKT- und ARK-Anker
```

[ANNEX] Der Reentry-Gap-Audit ist ein nachgeordneter Evidenzbeleg der Konstellationskarte, kein zusaetzlicher Navigationsknoten.

## 3. Reentry

[ANNEX] Hochstufung setzt Provenienz, Scope, Repo-Anker, Claim-/Layer-Status, offene Voids, Ruecknahmebedingung, menschliche Inhaltspruefung und die vorgesehene Gegenpruefung voraus.

**PASS-KANDIDAT:** projektuebergreifende ANNEX-Navigation und privacy-reduzierter Gap-Audit; gilt nur fuer den Draft-Verbleib bis alle Merge-Checks geschlossen sind  
**HOLD:** Kanonisierung, GOLD-/VOIDMAP-Aenderung und Engel-Operationalisierung  
**LOOP:** user-relayed Claude-/Diogenes-Pruefung ist stichprobenhaft erfolgt; menschliche Inhaltsklaerung und Merge-Entscheidung bleiben offen
