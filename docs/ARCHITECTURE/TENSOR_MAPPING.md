# TENSOR_MAPPING (Rosetta Stone)

Diese Datei beschreibt die 3-Achsen-Kodierung zentraler Konzepte:

- **x (Operational):** Layer 0–5 (Governance → Tools → UI → Validation …)
- **y (Epistemological):** L0–L5 (Erleben → Sprache → Methodik → Normativ → Unwissen …)
- **z (Representational):** Helix **L/R** (formal/technisch vs. mythisch/poetisch)

## Warum das wichtig ist
- Verhindert, dass Begriffe nur "poetisch" oder nur "technisch" bleiben.
- Macht **Brücken** (Chiasma) sichtbar: wo zwei Layer gleichzeitig aktiv sind.
- Ermöglicht VOIDs: gezielte "noch nicht benannte" Knoten.

## Minimaler Eintrag
```yaml
- name: "Begriff"
  coordinates:
    x: { layer: 1, component: "...", role: "..." }
    y: { layer: 2, component: "...", role: "..." }
    z: "Helix-L"  # oder Helix-R / Helix-L+R
  rcc_relations:
    - target: "Anderer Begriff"
      relation: "EC"   # RCC-8
      description: "..."
  theta_score: 0.0-1.0
  status: defined|partial|void
```

## Validator
Der Validator (`mapping/tensor_validator.py`) prüft Struktur + RCC-8 + Wertebereiche.
