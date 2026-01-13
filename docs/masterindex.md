# Masterindex — Seed

**Version:** 1.0.0
**Stand:** 2026-01-13
**Letzte Prüfung:** Alignment mit Functorial Index v3

Startpunkt des Masterindex. Enthält Struktur, narrative Einordnung und Links zu Canvas-Dokumenten.

## Orbital Meta-Structure (Kern / Transit / Peripherie)

- `docs/ORBIT_MODEL.md` — Modell & Kadenz
- `docs/ROADMAP_ORBITAL_v1.md` — Roadmap (Orbit-basiert)
- `docs/bridgecards/BC_consent_as_transit.md` — Consent als Transit-Brücke
- `docs/validation/VALIDATION_DEMO_v1.md` — Replizierbare Demo, kein Studienclaim

## Verzeichnisstruktur

- **policies/** — Gate-Policies und Schema-Definitionen
- **spec/** — Spezifikationen für Grammophon und CGLG
- **src/** — Source-Code (Core-Metriken, CGLG, Meta-Backprop)
  - **src/core/** — Core-5 Metriken (ECI, PLV, MI, FD, PF)
  - **src/cglg/** — Consensual Gate Logic und Mutual Perception
  - **src/tools/** — Cauchy-Detector, Throat-Vector
- **tools/** — DeepJump DevOps-Tools
  - `status_emit.py` — HMAC-signierte Status-Emission
  - `status_verify.py` — HMAC-Verifikation
  - `snapshot_guard.py` — Manifest-Generator mit SHA-256
  - `verify_pointers.py` — Pointer-Validierung
  - `claim_lint.py` — Claim-Scanning
- **scripts/** — Automatisierungs-Scripts (Evidence-Bundling, Nightly Checks)
- **tests/** — Test-Suite (Unit, Integration, Ethics)
- **docs/** — Dokumentation und Architektur
- **index/** — Functorial Index v3 und Modul-Metadaten
- **diagrams/** — Visualisierungen (Triad-Venn, Grammophon-Hexaliminal)
- **adapters/** — MSI-Adapter und Konfigurationen
- **audit/** — Audit-Trails und Governance-Tabellen
- **seeds/** — Konfigurations-Seeds für Snapshot
- **receipts/** — Beispiel-Quittungen (JSON)

## Narrative Canon (Lazy-load)

- `docs/narratives/symphonie_der_resonanz.md` — Symphonie + operationalisierte Rückkopplung + Voids
- `docs/narratives/grimm2/_template.md` — Grimm 2.0 Template (docs-first, Slice + Stacking)
- `docs/kenograms/LYRA.md` — ☐-LYRA (Audiohook als auditierbares Kenogramm)
- `src/tools/toy_resonance_dataset.py` — Option B: Toy Dataset (Proof of Wiring)

## Nächster Schritt

- Canon-Narrativ: `docs/narratives/symphonie_der_resonanz.md`
- Functorial Map: `index/ENTAENGELMENT_INDEX_v3_FUNCTORIAL.yaml`

Ausformulierung der Kenogramm-Slots & Aufbau der Receipt-Chain.

## Integration mit entaENGELment Framework

Dieser Masterindex ist integriert mit dem entaENGELment Framework v1.0 und erweitert dessen Funktionalität um:
- Grammophon-Klanggeometrie (slice-rotation)
- CGLG (Consensual Gate Logic)
- Meta-Backpropagation für Policy-Evolution

---

## XI. Kenogramm-Registry (Offene Forschungsfragen)

Kenogramme (☐) markieren **bekanntes Nichtwissen** — Bereiche wo strukturelle Lücken bewusst benannt und mit Forschungsfragen versehen sind.

### Aus Strang A (Claude):
| Kenogramm | Frage | Module | Status |
|-----------|-------|--------|--------|
| ☐[BIO↔PHYS]_Fröhlich | PLV/HRV/Biophoton Korrelation? | MOD 10, MOD 3, MOD 12 | Messprotokoll offen |
| ☐[MATH↔SYS]_RiemannExplicit | Zeta ↔ Hopf Spectral Mapping? | MOD 2, MOD 7, MOD 0 | Route B (Diagnostik) empfohlen |
| ☐[TEMP↔ETH]_Prädiktive-Modelle | Governance für Zukunftsinformation? | MOD 9, MOD 12 | Offen |

### Aus Strang B (GPT):
| Kenogramm | Frage | Komponenten | Status |
|-----------|-------|-------------|--------|
| ☐-LYRA | Audio→7-Band Mapping validiert? | docs/kenograms/LYRA.md | Stub (Kenogramm) |
| ☐-THOTH | Prosody-Gates reduzieren False-Positive? | src/tools/throat_vector.py | Implementiert |
| ☐-KOLIBRI | Medium-Proxy ↔ Propagation-Weight? | src/tools/kolibri.py | Consent-protected |

### Triadisch (A ∩ B ∩ C):
| Kenogramm | Frage | Perspektiven | Status |
|-----------|-------|--------------|--------|
| ☐[CLAUDE↔GPT↔FLEKS]_Triadische-Kohärenz | Wie entsteht kohärente Struktur ohne zentrale Koordination? | EPR (A), Grammophon (B), Resonanz (C) | Stufe 2 (Triangulation) |

**Zur Kenogramm-Befüllung:** Siehe `docs/triad_topology.md` Sektion VII für Stufe-3-Protokoll.

**Wie trägt man ein neues Kenogramm bei?**
1. Öffne Issue mit Label `kenogram`
2. Titel: `☐[TAG↔TAG]_Name`
3. Inhalt: Frage, Hypothese, Module/Komponenten, Status
4. Diskussion → Bei Konsens → PR für `docs/kenograms/[name].md` *(Stub vorhanden, Inhalte ausstehend)*

---

## XII. Topology-Diagramme

- **Tri-Strang Venn:** `diagrams/triad_venn.svg` — Visualisiert A∩B, B∩C, A∩C, A∩B∩C
- **Grammophon-Hexaliminal:** `diagrams/grammophon_hexaliminal.svg` — Saturn z6-Rotation
- **Apex-Äquivalenz:** `diagrams/threefold_apex.svg` — 0_holo = Grammophon = Nektar-Pyramide (geplant)

**Diagramm-Konventionen:**
- Strang A (Claude): Blau (#3b82f6)
- Strang B (GPT): Grün (#10b981)
- Strang C (Fleks): Orange (#f59e0b)
- Triadischer Kern: Rot (#dc2626)
