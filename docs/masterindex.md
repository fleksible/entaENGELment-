# Masterindex — Seed

Startpunkt des Masterindex. Enthält Struktur, narrative Einordnung und Links zu Canvas-Dokumenten.

## Verzeichnisstruktur

- **policies/** — Gate-Policies und Schema-Definitionen
- **spec/** — Spezifikationen für Grammophon, CGLG und ECI
- **src/** — Source-Code (Core-Metriken inkl. ECI, CGLG, Tools)
- **scripts/** — Automatisierungs-Scripts (Evidence-Bundling, Nightly Checks, Triad-Compare)
- **tests/** — Test-Suite (Unit, Integration, Ethics, CPT)
- **spec/** — Spezifikationen für Grammophon und CGLG
- **src/** — Source-Code (Core-Metriken, CGLG, Tools)
- **scripts/** — Automatisierungs-Scripts (Evidence-Bundling, Nightly Checks)
- **tests/** — Test-Suite (Unit, Integration, Ethics)
- **docs/** — Dokumentation und Architektur
- **reports/** — Test-Reports und Templates (CPT, Triad-Similarity)
- **validation/** — ECI-Validierungs-Artefakte

## Nächster Schritt

Ausformulierung der Kenogramm-Slots & Aufbau der Receipt-Chain.

## Integration mit entaENGELment Framework

Dieser Masterindex ist integriert mit dem entaENGELment Framework v1.0 und erweitert dessen Funktionalität um:
- Grammophon-Klanggeometrie (slice-rotation)
- CGLG (Consensual Gate Logic)
- Meta-Backpropagation für Policy-Evolution
- **ECI (Ethical Consent Index)** — Implementierung mit Bootstrap/Permutation-Tests
- **CPT-Test-Harness** — Charge-Parity-Time Invarianz-Validation
- **Triad-Execution-Kit** — Templates und Vergleichsskripts für 3-Strang-Analyse

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
| ☐-LYRA | Audio→7-Band Mapping validiert? | processors/lyra_mapper.py | UI-Stub vorhanden |
| ☐-THOTH | Prosody-Gates reduzieren False-Positive? | processors/throat_vector.py | A/B-Test ausstehend |
| ☐-KOLIBRI | Medium-Proxy ↔ Propagation-Weight? | processors/kolibri.py | Consent-protected |

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

---

## XIII. Testbare Implementierungen

### ECI (Ethical Consent Index)
- **Spec:** `spec/eci.spec.json` — JSON Schema für ECI-Vektoren und Kalibrierung
- **Implementierung:** `src/core/eci.py` — ECI-Berechnung mit Bootstrap/Permutation
- **Tests:** `tests/unit/test_eci.py` — Unit-Tests für ECI-Funktionen
- **CLI:** `python src/core/eci.py --likert 6 --behavior 0.6 --physio 0.5 --out validation/eci_example.json`

### CPT-Test-Harness
- **Implementierung:** `tests/cpt/test_cpt_harness.py` — Charge-Parity-Time Transformationen
- **Template:** `reports/cpt_test_report_template.json` — Report-Format
- **Tests:** `pytest tests/cpt/test_cpt_harness.py -q`

### Triad-Execution-Kit
- **Template:** `docs/triad_fill_template.md` — Standardisierter Slot für jeden Pol
- **Vergleichsskript:** `scripts/triad_compare.py` — TF-Vektorisierung & Cosine-Similarity
- **Usage:** `python scripts/triad_compare.py claude.md gpt.md fleks.md reports/triad_similarity.json`

**Dependencies:**
```bash
pip install numpy scipy pytest
```
