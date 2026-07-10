# PROJECT_CONSTELLATION_MAP_v0_1

**Status:** [ANNEX] — projektuebergreifende Navigationskarte, keine Kanonisierung  
**Datum:** 2026-07-10  
**Claim-Tags:** [FACT] [INFERENCE] [PROPOSAL] [OPEN]  
**Fokus:** Vorhandene Projektkoerper, Repo-Anker und sichtbare Luecken auffindbar machen

## 0. Scope

Diese Datei ist eine duenne, projektuebergreifende Sicht auf bereits vorhandene Repo-Schichten.

Sie ist:

- kein neues Atlas-System,
- keine Source of Truth,
- kein Ersatz fuer `docs/masterindex.md`, `index/`, `VOIDMAP.yml` oder Governance-Dokumente,
- keine automatische Hochstufung von Chat-Synthesen, Intake-Material oder ANNEX-Dateien,
- keine Behauptung, dass sichtbare Projektknoten bereits vollstaendig oder widerspruchsfrei sind.

Die Karte trennt zwei Fragen:

1. **Repository-Status:** Wie und wie vollstaendig ist ein Projektknoten im Repo vertreten?
2. **Authority-Status:** Welche Geltung besitzt die gefundene Repraesentation?

Sichtbarkeit ist weder Wahrheit noch Kanonisierung.

## 1. Statusvokabular

### Repository-Status

- `present-current` — aktueller, auffindbarer Repo-Anker vorhanden
- `present-partial` — nur Teile oder eine fruehere Ausbaustufe vorhanden
- `repository-lagging` — der aktuelle Arbeitsstand ist reicher als seine Repo-Repraesentation
- `intake-only` — nur als Intake-Kandidat oder Rohsediment vertreten
- `absent-or-unindexed` — kein belastbarer direkter Repo-Anker gefunden
- `archived` — nur historisch oder archiviert vorhanden

### Authority-Status

- `gold` — geschuetzte/kanonische Repo-Schicht gemaess Governance
- `governed` — durch explizite Regeln oder Policies kontrolliert
- `annex` — erweiterbar, aber nicht kanonisch
- `draft` — ausgearbeiteter Entwurf ohne Hochstufung
- `intake` — Review- und Einordnungsbedarf
- `receipt-only` — Evidenz-/Audit-Artefakt, kein semantischer Kanon
- `unresolved` — Geltungsgrenze noch nicht ausreichend geklaert

## 2. Konstellationsknoten

### ENTAENGELMENT-CORE

- **Rolle:** technischer, ethischer und governance-bezogener Rahmen des Repositories
- **Repository-Status:** `present-current`
- **Authority-Status:** `mixed: gold / governed / annex`
- **Primaere Repo-Anker:**
  - `README.md`
  - `index/COMPACT_INDEX_v3.yaml`
  - `VOIDMAP.yml`
  - `policies/`
  - `spec/`
- **Abhaengigkeiten:**
  - Claim-Hygiene
  - Consent- und Gate-Regeln
  - DeepJump-/Receipt-Infrastruktur
- **Offene Punkte:**
  - globale Projektzusammenhaenge im bisherigen Masterindex nur teilweise sichtbar
  - technische und narrative Schichten nicht durchgehend gemeinsam navigierbar
- **Review:**
  - ChatGPT: architecture-pass 2026-07-10
  - Claude/Diogenes: pending
  - Mensch: standing-by fuer Inhaltsfragen

### SOURCE-OF-TRUTH-SPINE

- **Rolle:** Governance-Membran fuer kontrollierte Kopplung von Repo, Runtime, externen Quellen und Mensch
- **Repository-Status:** `present-current`
- **Authority-Status:** `draft / intake`
- **Primaerer Repo-Anker:**
  - `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md`
- **Abhaengigkeiten:**
  - Claim-Tags
  - Intake-first
  - Provenienz und Ruecknahmebedingungen
- **Offene Punkte:**
  - explizite Review- und Promotion-Entscheidung ausstehend
- **Promotion-Boundary:**
  - wichtigste vorhandene Membran, aber keine automatische SoT-Geltung

### TESSER3TAKT

- **Rolle:** Uebergangs-, Projektions- und Reentry-Navigationsarchitektur
- **Repository-Status:** `present-current`
- **Authority-Status:** `annex`
- **Primaere Repo-Anker:**
  - `docs/tesser3takt/README.md`
  - `docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md`
- **Unterstuetzende Anker:**
  - `docs/tesser3takt/SOURCE_DECORATION_MAP_v0_1.md`
  - `docs/tesser3takt/S4_LOGZN_bridge.md`
  - `docs/tesser3takt/LYRA_STRINGS_COMPLEMENT_v0_1.md`
  - `docs/tesser3takt/FUENFTER_KLANG_DEPTH_v0_1.md`
  - `docs/tesser3takt/SANCHO_GUARD_v0_1.md`
- **Abhaengigkeiten:**
  - Source-Decoration-Guards
  - Claim-Hygiene
  - Reentry und PASS/HOLD/LOOP/STOP
- **Offene Punkte:**
  - globale Einbindung in den Masterindex
  - explizites Verhaeltnis zum erweiterten Grimm-Apparat
  - spaetere Pruefung moeglicher Path-Integral-Erweiterungen
- **Promotion-Boundary:**
  - bleibt ANNEX, bis ein separater Review eine andere Einstufung begruendet

### GRIMM-APPARAT

- **Rolle:** narrativer Leseraum, maieutische Rezeptionsarchitektur und symbolische Adaptionsmembran
- **Repository-Status:** `repository-lagging`
- **Authority-Status:** `unresolved / intake`
- **Primaerer Repo-Anker:**
  - `docs/narratives/grimm2/README.md`
- **Unterstuetzender Anker:**
  - `docs/narratives/grimm2/_template.md`
- **Im Repo bereits sichtbar:**
  - RAW -> EXTRACT -> SYNTH
  - Moral als offene Slice-Zone
  - Stacking als Invarianten-Suche
- **Aktuelle sichtbare Luecken:**
  - Reader-Membran und Schutz vor Fremddeutung
  - aktueller re-entry-faehiger Save-State
  - Aegypten-Griechenland-Bruecke
  - Ra-/Skarabaeus-/Logos-/720-Grad-Strang
  - Lustmolch-/Trickster-Differenzierung
  - heutige Rolle als adaptiver Muse- und Leseraum
- **Abhaengigkeiten:**
  - entaENGELment-Ethik
  - tesser3TAKT-Navigation
  - Claim- und Layer-Hygiene
- **Promotion-Boundary:**
  - neuere Chat-Synthesen zuerst als Intake; keine direkte Ueberschreibung des vorhandenen Grimm-Workflows

### ARK-FAMILY

- **Rolle:** technische und evidenzbezogene Artefaktfamilie mit P4-, Cephalo- und Receipt-Schichten
- **Repository-Status:** `present-partial`
- **Authority-Status:** `mixed: annex / receipt-only / unresolved`
- **Primaere Repo-Anker:**
  - `ark/p4/P4_TESTPLAN_INDEX.md`
  - `ark_cephalo_manifest_v2.json`
- **Unterstuetzende Anker:**
  - `ark/p4/receipts/`
- **Offene Punkte:**
  - klaeren, ob ARK-P4, ARK-Cephalo und Governance-Bruecken ein Projektkoerper oder mehrere gekoppelte Koerper sind
  - Receipts nicht als semantischen Kanon lesen
  - Verbindung zur aktuellen CephaloCamouflage-/Physics-Based-Compliance-Lesart pruefen
- **Promotion-Boundary:**
  - keine Zusammenziehung zu einem einheitlichen Kanon ohne Provenienz- und Rollenpruefung

### RESONANZKIEL

- **Rolle:** vermuteter Architektur- und Uebergangsknoten zwischen physischer Modellgrammatik, Resonanz und Navigation
- **Repository-Status:** `absent-or-unindexed`
- **Authority-Status:** `intake`
- **Primaerer Repo-Anker:** keiner belastbar identifiziert
- **Offene Punkte:**
  - aktuellen Save-State als Intake-Artefakt sichern
  - Modell-, Physik-, Metapher- und Spec-Layer trennen
  - Beziehung zu tesser3TAKT und Grimm-Apparat pruefen
- **Promotion-Boundary:**
  - kein Repo-Knoten allein aufgrund nachtraeglich erkannter Chat-Kohaerenz

### FKP

- **Rolle:** Flux-Kondensations-Protokoll; Pruefsynthese fuer strukturierte Energie und vorsichtig getrennte Informationsclaims
- **Repository-Status:** `absent-or-unindexed`
- **Authority-Status:** `intake`
- **Primaerer Repo-Anker:** keiner belastbar identifiziert
- **Offene Punkte:**
  - FKP v0.2 als Intake-Kandidat mit Provenienz sichern
  - Stufen 3-5 und Stufe 6 claim-hygienisch getrennt halten
  - Claude-Pruefung als Provenienz, nicht als Wahrheitsstempel dokumentieren
- **Promotion-Boundary:**
  - keine Integration in SoT, Spec oder VOIDMAP ohne separaten Review

## 3. Navigationskette

```text
docs/START_HERE.md
        -> docs/masterindex.md
        -> docs/PROJECT_CONSTELLATION_MAP_v0_1.md
        -> bestehende Index-, VOID-, Governance-, Grimm-, tesser3TAKT- und ARK-Anker
```

Die Konstellationskarte zeigt den gegenwaertigen Lagezusammenhang. Der Masterindex bleibt das Navigationszentrum; `index/`, Policies, Specs, VOIDMAP und Receipts behalten ihre jeweils eigene Governance-Rolle.

## 4. Review- und Reentry-Regel

Ein Knoten darf nur von `repository-lagging`, `intake` oder `unresolved` hochgestuft werden, wenn mindestens geklaert sind:

1. Provenienz und aktueller Scope
2. massgebliche Repo-Anker
3. Claim- und Layer-Status
4. Abhaengigkeiten und offene Voids
5. Ruecknahme- oder Reentry-Bedingung
6. menschliche Inhaltspruefung
7. unabhaengige Gegenpruefung, sofern fuer den Knoten vorgesehen

## 5. Nicht getan

- `docs/START_HERE.md` nicht veraendert
- `index/` nicht veraendert
- `VOIDMAP.yml` nicht veraendert
- Policies und Specs nicht veraendert
- Receipts nicht veraendert
- SoT-Spine nicht hochgestuft
- Grimm-Apparat nicht inhaltlich neu geschrieben
- Resonanzkiel und FKP nicht als vorhandene Repo-Module ausgegeben

## 6. Aktueller Entscheidungsstatus

**HOLD fuer Kanonisierung.**  
**PASS fuer projektuebergreifende ANNEX-Navigation.**  
**LOOP fuer Claude-/Diogenes-Pruefung und menschliche Inhaltsklaerung.**
