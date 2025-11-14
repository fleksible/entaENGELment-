# Masterindex — Seed

Startpunkt des Masterindex. Enthält Struktur, narrative Einordnung und Links zu Canvas-Dokumenten.

## Verzeichnisstruktur

- **policy/** — Gate-Policies und Schema-Definitionen
- **spec/** — Spezifikationen für Grammophon und CGLG
- **src/** — Source-Code (Core-Metriken, CGLG, Tools)
- **scripts/** — Automatisierungs-Scripts (Evidence-Bundling, Nightly Checks)
- **tests/** — Test-Suite (Unit, Integration, Ethics)
- **docs/** — Dokumentation und Architektur

## Nächster Schritt

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
4. Diskussion → Bei Konsens → PR für `docs/kenograms/[name].md`

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
