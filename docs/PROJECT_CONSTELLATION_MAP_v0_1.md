# PROJECT_CONSTELLATION_MAP_v0_1

**Status:** [ANNEX] — projektuebergreifende Navigationskarte, keine Kanonisierung  
**Datum:** 2026-07-14  
**Claim-Tags:** [FACT] [INFERENCE] [PROPOSAL] [OPEN]

## 0. Funktion und Grenze

Diese Datei zeigt Projektknoten, Funktion, Status, massgebliche Repo-Anker, Abhaengigkeiten, offene Luecken und Review-Stand.

Sie ist kein neues Atlas-System, keine Source of Truth und kein Ersatz fuer `docs/masterindex.md`, `index/`, `VOIDMAP.yml`, Policies, Specs oder Receipts. Sichtbarkeit ist weder Wahrheit noch Kanonisierung.

`repository_status` beschreibt die Repo-Repraesentation: `present-current`, `present-partial`, `repository-lagging`, `intake-only`, `absent-or-unindexed`, `archived`.

`authority_status` beschreibt die Geltung: `gold`, `governed`, `annex`, `draft`, `intake`, `receipt-only`, `unresolved`.

Aktueller Reentry-Abgleich:

- `docs/audit/2026-07-14_tesser3takt_reentry_gap_audit.md` — privacy-reduzierte Delta-Matrix zwischen bestehender Repo-Struktur und aktuellem Arbeitsstand; keine neue Index- oder Kanonisierungsschicht

## 1. Projektknoten

```yaml
- id: ENTAENGELMENT-CORE
  role: technischer, ethischer und governance-bezogener Rahmen
  repository_status: present-current
  authority_status: mixed-gold-governed-annex
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
  review:
    chatgpt: architecture-pass-2026-07-14
    claude: pending
    human: standing-by-for-content-questions

- id: SOURCE-OF-TRUTH-SPINE
  role: Governance-Membran fuer Repo, Runtime, externe Quellen und Mensch
  repository_status: present-current
  authority_status: draft-intake
  primary_repo_anchor:
    - docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md
  depends_on:
    - claim-tags
    - intake-first
    - provenance-and-retraction
  open_voids:
    - explizite Review- und Promotion-Entscheidung
  promotion_boundary: primaerer Anker ist keine automatische SoT-Geltung

- id: TESSER3TAKT
  role: Uebergangs-, Projektions- und Reentry-Navigation
  repository_status: present-current
  authority_status: annex
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
  review:
    chatgpt: reentry-gap-audit-2026-07-14
    claude: pending

- id: GRIMM-APPARAT
  role: narrativer Leseraum und maeutische Rezeptionsarchitektur
  repository_status: repository-lagging
  authority_status: unresolved-intake
  primary_repo_anchor:
    - docs/narratives/grimm2/README.md
    - docs/narratives/grimm2/_template.md
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
  promotion_boundary: neuere Chat-Synthesen zuerst als Intake
  review:
    chatgpt: reentry-gap-audit-2026-07-14
    claude: pending
    human: standing-by-for-content-questions

- id: ARK-FAMILY
  role: technische und evidenzbezogene P4-/Cephalo-/Receipt-Artefaktfamilie
  repository_status: present-partial
  authority_status: mixed-annex-receipt-unresolved
  primary_repo_anchor:
    - ark/p4/P4_TESTPLAN_INDEX.md
    - ark_cephalo_manifest_v2.json
  depends_on:
    - receipt-and-provenance-guards
  open_voids:
    - ein oder mehrere gekoppelte Projektkoerper
    - Beziehung zur aktuellen CephaloCamouflage-Lesart
  promotion_boundary: Receipts sind kein semantischer Kanon

- id: RESONANZKIEL
  role: Architektur- und Uebergangsknoten zwischen Modellgrammatik, Resonanz und Navigation
  repository_status: absent-or-unindexed
  authority_status: intake
  primary_repo_anchor: []
  depends_on:
    - tesser3takt
    - grimm-apparat
    - claim-and-layer-hygiene
  open_voids:
    - aktuellen Save-State mit Provenienz als Intake sichern
    - Modell-, Physik-, Metapher- und Spec-Layer trennen
  promotion_boundary: keine Hochstufung durch rueckwirkend erkannte Chat-Kohaerenz

- id: FKP
  role: Flux-Kondensations-Protokoll und claim-hygienische Pruefsynthese
  repository_status: absent-or-unindexed
  authority_status: intake
  primary_repo_anchor: []
  depends_on:
    - fluxon-thread
    - claim-hygiene
  open_voids:
    - FKP-v0.2 mit Provenienz als Intake sichern
    - strukturierte Energie und Informationsclaims getrennt halten
  promotion_boundary: keine SoT-, Spec- oder VOIDMAP-Integration ohne separaten Review
```

## 2. Navigationskette

```text
docs/START_HERE.md
        -> docs/masterindex.md
        -> docs/PROJECT_CONSTELLATION_MAP_v0_1.md
        -> bestehende Index-, VOID-, Governance-, Grimm-, tesser3TAKT- und ARK-Anker
```

Der Reentry-Gap-Audit ist ein nachgeordneter Evidenzbeleg der Konstellationskarte, kein zusaetzlicher Navigationsknoten.

## 3. Reentry

Hochstufung setzt Provenienz, Scope, Repo-Anker, Claim-/Layer-Status, offene Voids, Ruecknahmebedingung, menschliche Inhaltspruefung und die vorgesehene Gegenpruefung voraus.

**PASS:** projektuebergreifende ANNEX-Navigation und privacy-reduzierter Gap-Audit  
**HOLD:** Kanonisierung, GOLD-/VOIDMAP-Aenderung und Engel-Operationalisierung  
**LOOP:** Claude-/Diogenes-Pruefung und menschliche Inhaltsklaerung
