# Architekturskizze (Seed)

## Layer-Architektur

### Policy Layer
Definiert die nicht-verhandelbaren Invarianten und Gate-Logik:
- `gate_policy_v1.json` — Hard-Gate Policy (MZM)
- `schema.json` — JSON Schema für Policy-Validierung

### Spec Layer
Spezifikationen für die Kernkomponenten:
- `grammophon.spec.json` — Slice-Rotation & Polyeder-Klanggeometrie
- `cglg.spec.json` — Consensual Gate Logic & Mutual Perception

### Runtime Layer
Operative Komponenten:
- **Core Metrics** (`src/core/metrics.py`) — ECI, PLV, MI, FD, PF
- **CGLG** (`src/cglg/`) — Gate-Logik und Mutual Perception
- **Tools** (`src/tools/`) — Cauchy-Detector, Throat-Vector
- **Meta-Backpropagation** (`src/meta_backprop.py`) — Policy-Evolution

### Evidence & Receipt Chain
Auditierbare Beweisketten:
- Dual-Receipts (`receipt_proof`, `context_signature`)
- Evidence-Bundling via `scripts/evidence_bundle.sh`

### Canvas-Verknüpfung
Verbindung zu Canvas-Dokumenten für narrative Einordnung und Kontextbezug.
