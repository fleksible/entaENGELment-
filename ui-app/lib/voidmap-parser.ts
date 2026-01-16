import { Void, VoidMap, VoidStatus, VoidPriority } from '@/types';

// Static VOIDMAP data (in production, this would be fetched from API)
// Parsed from VOIDMAP.yml
export const VOIDMAP_DATA: VoidMap = {
  version: '1.0',
  description: 'Central registry for tracking open voids (gaps) in the entaENGELment framework.',
  metadata: {
    maintainer: 'entaENGELment',
    last_updated: '2026-01-04',
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
      status: 'OPEN',
      priority: 'high',
      owner: null,
      domain: '[DEV]',
      symptom: 'CI does not run full verify/status/snapshot flow',
      closing_path: 'Update deepjump-ci.yml with verify_pointers and claim_lint steps',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[TODO] Needs CI workflow update to include new tools.',
    },
    {
      id: 'VOID-003',
      title: 'Status Emit Receipt Format',
      status: 'OPEN',
      priority: 'medium',
      owner: null,
      domain: '[DEV]',
      symptom: 'status_emit.py does not emit full receipt format per protocol',
      closing_path: 'Update status_emit.py with --claim, --tag, --module options',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[TODO] Protocol specifies receipt format v1.0 with additional fields.',
    },
    {
      id: 'VOID-010',
      title: 'Taxonomie & Spektren (Empirie)',
      status: 'OPEN',
      priority: 'high',
      owner: null,
      domain: '[PHYS]',
      symptom: 'Spektrale Zuordnung ohne belastbare Literatur-/Datenbasis',
      closing_path: 'Literatur-Scan + zitierte Tabelle (CSV) + Evidence-Bundle',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[BIO][PHYS] Empirie-Bridge für MOD_18/Taxonomie.',
    },
    {
      id: 'VOID-011',
      title: 'Metriken der Resonanz (MI, PLV, FD)',
      status: 'OPEN',
      priority: 'high',
      owner: null,
      domain: '[MATH]',
      symptom: 'MI/FD sind aktuell Minimal-Stubs; keine Toy-Simulation als Proof',
      closing_path: 'Option B: toy_resonance_dataset + robuste Implementierung + Tests',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[COMP] Siehe src/tools/toy_resonance_dataset.py',
    },
    {
      id: 'VOID-012',
      title: 'GateProof Checkliste (Governance)',
      status: 'OPEN',
      priority: 'critical',
      owner: null,
      domain: '[DEV]',
      symptom: 'Keine einheitliche, testbare Checkliste für latent→manifest Übergänge',
      closing_path: 'policies/gateproof_v1.yaml + negative ethics tests',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[META] Governance als Judikative.',
    },
    {
      id: 'VOID-013',
      title: 'Sensor-Architektur (BOM & Protokoll)',
      status: 'OPEN',
      priority: 'medium',
      owner: null,
      domain: '[DEV]',
      symptom: 'Kein BOM/Protokoll für Sensorik, falls Messschicht gebaut wird',
      closing_path: 'docs/sensors/bom.md + spec/sensors.spec.json',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[BIO] Nur Komponenten-/Protokollebene.',
    },
    {
      id: 'VOID-014',
      title: 'Protein-Design (in-silico, safety-bounded)',
      status: 'OPEN',
      priority: 'medium',
      owner: null,
      domain: '[BIO]',
      symptom: 'Exploration gewünscht, aber hohes Risiko bei operativen Laboranleitungen',
      closing_path: 'High-level Tool/Literatur-Übersicht + nicht-operative Demos',
      evidence: null,
      created: '2026-01-04',
      closed: null,
      notes: '[SAFETY] Nur computational exploration.',
    },
    {
      id: 'VOID-020',
      title: 'Port-Matrix Suite (K0..K4) fehlt',
      status: 'CLOSED',
      priority: 'high',
      owner: null,
      domain: '[DEV]',
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
      domain: '[DEV]',
      symptom: 'Semantik/Marker nicht zentral dokumentiert',
      closing_path: 'policies/port_codebooks.yaml',
      evidence: 'policies/port_codebooks.yaml',
      created: '2026-01-13',
      closed: '2026-01-13',
      layer: 'GUARD',
    },
    {
      id: 'VOID-022',
      title: 'Flood-Guard Threshold fehlt',
      status: 'CLOSED',
      priority: 'medium',
      owner: null,
      domain: '[DEV]',
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
      status: 'OPEN',
      priority: 'low',
      owner: null,
      domain: '[DEV]',
      symptom: 'Scope-Tags nicht überall konsistent',
      closing_path: null,
      evidence: null,
      created: '2026-01-13',
      closed: null,
      layer: 'EXPLAIN',
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
    closed: voids.filter(v => v.status === 'CLOSED').length,
    critical: voids.filter(v => v.priority === 'critical' && v.status !== 'CLOSED').length,
    high: voids.filter(v => v.priority === 'high' && v.status !== 'CLOSED').length,
  };
}

export function getStatusIcon(status: VoidStatus): string {
  switch (status) {
    case 'OPEN': return '☐';
    case 'IN_PROGRESS': return '🔄';
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
    case 'CLOSED': return 'text-green-500';
  }
}
