import { Void, VoidMap, VoidStatus, VoidPriority } from '@/types';

// =============================================================================
// Static VOIDMAP mirror.
//
// ⚠️ SOURCE OF TRUTH IS `VOIDMAP.yml` (repo root, GOLD).
//
// This file is a hand-synced, read-only copy of `VOIDMAP.yml` so the UI can be
// rendered without a build-time YAML parse. It MUST be kept in sync with
// `VOIDMAP.yml` — never edit a VOID's meaning here, only mirror what the GOLD
// file already says.
//
// Drift in the verbatim-mirrored fields (`status`, `priority`, `title`) is
// detected by `tools/voidmap_ui_drift_check.py` (run via
// `make voidmap-ui-drift-check`). The free-form `notes` field is intentionally
// abridged here for display and is NOT byte-compared. If the check fails,
// re-sync the affected fields below to match `VOIDMAP.yml`.
// =============================================================================
export const VOIDMAP_DATA: VoidMap = {
  version: '1.0',
  description: 'Central registry for tracking open voids (gaps) in the entaENGELment framework.',
  metadata: {
    maintainer: 'entaENGELment',
    last_updated: '2026-06-24',
    generated_doc: 'docs/voids_backlog.md',
  },
  voids: [
    {
      id: 'VOID-001',
      title: 'DeepJump Protocol Implementation',
      status: 'CLOSED',
      priority: 'critical',
      owner: 'claude-code',
      domain: '[DEV]',
      symptom: 'No standardized verification flow for changes',
      closing_path: 'Implement verify_pointers.py, claim_lint.py, and update Makefile',
      evidence: null,
      created: '2026-01-04',
      closed: '2026-01-04',
      notes: '[FACT] Implemented as part of DeepJump Protocol v1.2 setup.',
    },
    {
      id: 'VOID-002',
      title: 'CI Pipeline Integration',
      status: 'CLOSED',
      priority: 'high',
      owner: 'claude-code',
      domain: '[DEV]',
      symptom: 'CI does not run full verify/status/snapshot flow',
      closing_path: 'Update deepjump-ci.yml with verify_pointers and claim_lint steps',
      evidence: '.github/workflows/deepjump-ci.yml',
      created: '2026-01-04',
      closed: '2026-02-15',
      notes: '[CLOSED 2026-02-15] verify_pointers, claim_lint, port_lint now run as blocking CI steps in deepjump-ci.yml (no continue-on-error).',
    },
    {
      id: 'VOID-003',
      title: 'Status Emit Receipt Format',
      status: 'CLOSED',
      priority: 'medium',
      owner: 'claude-code',
      domain: '[DEV]',
      symptom: 'status_emit.py does not emit full receipt format per protocol',
      closing_path: 'Update status_emit.py with --claim, --tag, --module options',
      evidence: 'tools/status_emit.py',
      created: '2026-01-04',
      closed: '2026-03-06',
      notes: '[FACT] tools/status_emit.py implements full receipt format v1.0 with --claim, --tag, --module options (tests/test_status_emit.py).',
    },
    {
      id: 'VOID-010',
      title: 'Taxonomie & Spektren (Empirie)',
      status: 'IN_PROGRESS',
      priority: 'high',
      owner: 'fleks',
      domain: '[PHYS]',
      symptom: 'Spektrale Zuordnung ohne belastbare Literatur-/Datenbasis',
      closing_path: 'Literatur-Scan + zitierte Tabelle (CSV) + Evidence-Bundle',
      evidence: ['docs/voids/VOID-010_taxonomy_and_spectra.md'],
      created: '2026-01-04',
      closed: null,
      notes: '[BIO][PHYS] Empirie-Bridge für MOD_18/Taxonomie. [2026-06-11] Re-baselined after issue #240: next verifier boundary is a sources-first CSV/schema bundle.',
    },
    {
      id: 'VOID-011',
      title: 'Metriken der Resonanz (MI, PLV, FD)',
      status: 'IN_PROGRESS',
      priority: 'high',
      owner: 'fleks',
      domain: '[MATH]',
      symptom: 'MI/FD implementation exists; evidence boundary needs simulation receipt and claim-tagged metric export',
      closing_path: 'Option B: toy_resonance_dataset + robust implementation + tests + SIMULATION_PROXY evidence receipt',
      evidence: [
        'src/core/metrics.py',
        'src/tools/toy_resonance_dataset.py',
        'tests/unit/test_toy_resonance_dataset.py',
        'docs/voids/VOID-011_resonance_metrics.md',
      ],
      created: '2026-01-04',
      closed: null,
      notes: '[COMP] MI (histogram) und FD (Higuchi) implementiert in src/core/metrics.py. [2026-06-11] Do not close until a deterministic metrics export/receipt carries the SIMULATION_PROXY boundary explicitly.',
    },
    {
      id: 'VOID-012',
      title: 'GateProof Checkliste (Governance)',
      status: 'CLOSED',
      priority: 'critical',
      owner: 'claude-code',
      domain: '[DEV]',
      symptom: 'Keine einheitliche, testbare Checkliste für latent→manifest Übergänge',
      closing_path: 'policies/gateproof_v1.yaml + negative ethics tests',
      evidence: ['policies/gateproof_v1.yaml', 'tests/ethics/test_fail_safe_expired_consent.py'],
      created: '2026-01-04',
      closed: '2026-03-06',
      notes: '[META] Governance als Judikative. [CLOSED 2026-03-06] DRAFT-Status entfernt, alle Checks mit Verifikationspfad.',
    },
    {
      id: 'VOID-013',
      title: 'Sensor-Architektur (BOM & Protokoll)',
      status: 'CLOSED',
      priority: 'medium',
      owner: 'claude-code',
      domain: '[DEV]',
      symptom: 'Kein BOM/Protokoll für Sensorik, falls Messschicht gebaut wird',
      closing_path: 'docs/sensors/bom.md + spec/sensors.spec.json',
      evidence: ['docs/sensors/bom.md', 'spec/sensors.spec.json'],
      created: '2026-01-04',
      closed: '2026-03-06',
      notes: '[BIO] Nur Komponenten-/Protokollebene, keine riskanten Anleitungen. [CLOSED 2026-03-06] DRAFT-Status entfernt, Specs finalisiert.',
    },
    {
      id: 'VOID-014',
      title: 'Protein-Design (in-silico, safety-bounded)',
      status: 'SUSPENDED',
      priority: 'medium',
      owner: 'fleks',
      domain: '[BIO]',
      symptom: 'Exploration gewünscht, aber hohes Risiko bei operativen Laboranleitungen',
      closing_path: 'High-level Tool/Literatur-Übersicht + nicht-operative Demos',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[SAFETY] Nur computational exploration; keine Nasslabor-Protokolle. [2026-04-04] Status auf SUSPENDED gesetzt. Kann bei Bedarf auf OPEN zurückgesetzt werden.',
    },
    {
      id: 'VOID-015',
      title: 'Explain-Overlay Lint',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[META][DEV]',
      symptom:
        'Narrative overlays can replace rather than supplement reasoning unless trigger terms are tied back to Reason/Transform/Input and context tags.',
      closing_path:
        'Implement explain-overlay lint rules for trigger keywords, reason-code density, bridge-tag presence, and pseudo-physics guards; add tests and a receipt showing coverage.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-016',
      title: 'Prozess-Erhalt ohne Zeit-Archiv (τ-Kernel)',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[META][COMP]',
      symptom:
        'Surprise in the present must be preserved while reconstructable essence survives and non-essential details remain autophagic.',
      closing_path:
        'Specify τ_fast/τ_mid/τ_long retention rules, autophagy extraction, V+ sediment interaction, and receipts proving detail deletion without essence loss.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-017',
      title: 'Kippung-statt-Peak Operator (Δ-Detektor)',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[MATH][META]',
      symptom:
        'Events risk being misread as maxima or peaks rather than frame changes / tipping transitions.',
      closing_path:
        'Specify semantic drift, interference-field activation, polycontext expansion, and torus-cycle completion as Δ-components; test that a tipping event is not triggered by quantitative increase alone.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-020',
      title: 'Port-Matrix Suite (K0..K4) fehlt',
      status: 'CLOSED',
      priority: 'high',
      owner: null,
      domain: '',
      symptom: 'Kein Port-Linter / keine Marker-Operationalisierung',
      closing_path: 'tools/port_lint.py',
      evidence: ['tools/port_lint.py', 'tests/test_port_lint.py'],
      created: '2026-01-13',
      closed: '2026-01-13',
      layer: 'GUARD',
    },
    {
      id: 'VOID-021',
      title: 'Port-Codebooks fehlen',
      status: 'CLOSED',
      priority: 'medium',
      owner: null,
      domain: '',
      symptom: 'Semantik/Marker nicht zentral dokumentiert',
      closing_path: 'policies/port_codebooks.yaml',
      evidence: 'policies/port_codebooks.yaml',
      created: '2026-01-13',
      closed: '2026-01-13',
      layer: 'GUARD',
    },
    {
      id: 'VOID-022',
      title: 'Flood-Guard Threshold fehlt (MAX_CLAIMS_PER_RECEIPT)',
      status: 'CLOSED',
      priority: 'medium',
      owner: null,
      domain: '',
      symptom: 'Keine harte Grenze gegen Receipt-Überflutung',
      closing_path: 'tools/port_lint.py',
      evidence: 'tools/port_lint.py',
      created: '2026-01-13',
      closed: '2026-01-13',
      layer: 'GUARD',
    },
    {
      id: 'VOID-023',
      title: 'MICRO/MESO/MACRO Tagging konsistent ausrollen',
      status: 'CLOSED',
      priority: 'low',
      owner: 'claude-code',
      domain: '',
      symptom: 'Scope-Tags nicht überall konsistent',
      closing_path: 'policies/port_codebooks.yaml scope_tags section',
      evidence: 'policies/port_codebooks.yaml',
      created: '2026-01-13',
      closed: '2026-03-06',
      layer: 'EXPLAIN',
      notes: '[FACT] Scope-Tag-Definitionen [MICRO]/[MESO]/[MACRO] in policies/port_codebooks.yaml. [CLOSED 2026-03-06] Formale Definition etabliert.',
    },
    {
      id: 'VOID-024',
      title: 'Audio-Bridge-Policy',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[DEV][META]',
      symptom:
        'Audio output needs a consent-bound, explainable, parameterized policy to prevent hidden influence or pseudo-physiological claims.',
      closing_path:
        'Implement an audio-bridge policy document and lint/receipt checks for consent, parameter bounds, reason codes, kill-switch behavior, and safe text fallback.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-025',
      title: 'Multi-Media Canonicalization',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[DEV][META]',
      symptom:
        'Text, image, and audio artifacts need stable receipts despite modality shifts and autophagic detail loss.',
      closing_path:
        'Define canonical fields for text/image/audio, deterministic graph serialization, multimedia hash bases, autophagy-compatible invariants, and receipt fixtures.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-026',
      title: 'tesser3TAKT Core Layout / SailObservation Gate',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[COMP][META]',
      symptom:
        'tesser3TAKT lacks a canonical core layout and indirect sail-observation gate; the process manager risks direct truth-claiming without a SailObservation boundary.',
      closing_path:
        'ADR + src/tesser3takt/models.py + kraehennest.py + tests + receipt; SailObservation must precede KraehennestObservation.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-027',
      title: 'tesser3TAKT HUD Projection Layer',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[COMP][META]',
      symptom:
        'Matrix, 1xn slice, Multiwaygraph, SailObservation, GitHub artifacts, and Airtable status need a read-only HUD projection without turning the UI into an oracle.',
      closing_path:
        'Implement a read-only HUD fixture and UI demo that renders a TesserTickFrame with 7x9 matrix, 1xn slice, Apex marker, periphery, EFS/MVI axis, decision bar, and receipt link, with explicit projection labels.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-028',
      title: 'EFS/MVI Grüneisen-Axis Calibration',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[MATH][COMP]',
      symptom:
        'The proposed Grüneisen-like x-axis between ΔEFS and ΔMVI risks false precision unless both metrics are normalized and fixture-tested.',
      closing_path:
        'Define normalized delta metrics, calibration factors, thresholds, three minimal fixtures (EFS-high/MVI-low, MVI-high/EFS-low, both-high), and a SIMULATION_PROXY receipt linked to VOID-011.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-029',
      title: 'Cross-Instance Receipt for tesser3TAKT HUD Work',
      status: 'OPEN',
      priority: 'medium',
      owner: 'fleks',
      domain: '[META][DEV]',
      symptom:
        'tesser3TAKT HUD and HOLD-transformation material includes cross-instance contributions that need explicit receipt scope and human-commit marking.',
      closing_path:
        'Add a cross-instance receipt template/instance recording source poles, imported claims, protected-origin notes, human_commit_required=true, and allowed reuse scope for ADR and code skeleton work.',
      evidence: null,
      created: '2026-06-24',
      closed: null,
    },
    {
      id: 'VOID-LOGZN-001',
      title: 'LOG-ZN Orbit als Windungs-Gedächtnisoperator',
      status: 'OPEN',
      priority: 'high',
      owner: 'fleks',
      domain: '[MATH][META]',
      symptom: 'Der entwickelte Winkel / log(z)-Orbit ist als neuer RZT-Operator erkannt, aber noch nicht in Tests, Metrics oder Receipts verankert.',
      closing_path: 'docs/rzt/LOG_ZN_ORBIT_001.md + docs/tesser3takt/S4_LOGZN_bridge.md + Claim-Tags + optionaler Visual-/Replay-Test',
      evidence: ['docs/rzt/LOG_ZN_ORBIT_001.md', 'docs/tesser3takt/S4_LOGZN_bridge.md'],
      created: '2026-05-17',
      closed: null,
      notes: '[MODEL] Sichtbare Wiederkehr modulo 2π ist nicht identisch mit entwickelter Windungsgeschichte. [INFERENCE] Anschluss an RZT-0/Nektar-Maturation/A4-Reentry/tesser3TAKT-S4 ist prüfbar, aber nicht als Identitätsbehauptung zu lesen.',
    },
  ],
};

// Helper functions
export function getVoids(): Void[] {
  return VOIDMAP_DATA.voids;
}

export function getVoidById(id: string): Void | undefined {
  return VOIDMAP_DATA.voids.find(v => v.id === id);
}

export function getVoidsByStatus(status: VoidStatus): Void[] {
  return VOIDMAP_DATA.voids.filter(v => v.status === status);
}

export function getVoidsByPriority(priority: VoidPriority): Void[] {
  return VOIDMAP_DATA.voids.filter(v => v.priority === priority);
}

export function getVoidsByDomain(domain: string): Void[] {
  return VOIDMAP_DATA.voids.filter(v => v.domain.includes(domain));
}

export function getVoidStats() {
  const voids = VOIDMAP_DATA.voids;
  return {
    total: voids.length,
    open: voids.filter(v => v.status === 'OPEN').length,
    inProgress: voids.filter(v => v.status === 'IN_PROGRESS').length,
    suspended: voids.filter(v => v.status === 'SUSPENDED').length,
    closed: voids.filter(v => v.status === 'CLOSED').length,
    critical: voids.filter(v => v.priority === 'critical' && v.status !== 'CLOSED').length,
    high: voids.filter(v => v.priority === 'high' && v.status !== 'CLOSED').length,
  };
}

export function getStatusIcon(status: VoidStatus): string {
  switch (status) {
    case 'OPEN': return '☐';
    case 'IN_PROGRESS': return '🔄';
    case 'SUSPENDED': return '⏸';
    case 'CLOSED': return '✓';
  }
}

export function getPriorityColor(priority: VoidPriority): string {
  switch (priority) {
    case 'critical': return 'text-red-500';
    case 'high': return 'text-amber-500';
    case 'medium':
    case 'med': return 'text-blue-500';
    case 'low': return 'text-zinc-400';
  }
}

export function getStatusColor(status: VoidStatus): string {
  switch (status) {
    case 'OPEN': return 'text-amber-400';
    case 'IN_PROGRESS': return 'text-blue-500';
    case 'SUSPENDED': return 'text-violet-400';
    case 'CLOSED': return 'text-green-500';
  }
}
