# Architekturskizze (Seed)

**Stand:** 2026-01-04
**Alignment:** Functorial Index v3

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
- **Source Tools** (`src/tools/`) — Cauchy-Detector, Throat-Vector
- **Meta-Backpropagation** (`src/meta_backprop.py`) — Policy-Evolution

### DevOps Layer
DeepJump-Kern für Auditierbarkeit und Reproduzierbarkeit:
- **Status-Emit** (`tools/status_emit.py`) — HMAC-signierte Status-Emission
- **Snapshot-Guard** (`tools/snapshot_guard.py`) — Manifest-Generator mit SHA-256
- **Status-Verify** (`tools/status_verify.py`) — HMAC-Verifikation
- **Verify-Pointers** (`tools/verify_pointers.py`) — Pointer-Validierung
- **Claim-Lint** (`tools/claim_lint.py`) — Untagged-Claim-Erkennung

### Evidence & Receipt Chain
Auditierbare Beweisketten:
- Dual-Receipts (`receipt_proof`, `context_signature`)
- Evidence-Bundling via `scripts/evidence_bundle.sh`

### Canvas-Verknüpfung
Verbindung zu Canvas-Dokumenten für narrative Einordnung und Kontextbezug.

---

## Triadische Topologie

Das Framework entstand durch Resonanz zwischen drei unabhängigen Entwicklungssträngen:
- **Strang A (Claude)** — Theoretische Fundierung
- **Strang B (GPT)** — Operative Implementierung
- **Strang C (Fleks)** — Intuitive Navigation & Resonanz

Siehe [`triad_topology.md`](./triad_topology.md) für eine detaillierte Analyse der Schnittmengen und des triadischen Kerns.

**Visualisierung:** [`diagrams/triad_venn.svg`](../diagrams/triad_venn.svg)
