// =============================================================================
// @enta/types — EntaENGELment Domain Types (Single Source of Truth)
// =============================================================================
//
// Arché: the shared type-topology of the system. These types mirror the GOLD
// `VOIDMAP.yml` schema and the CLAUDE.md guard model as a *read-only consumer* —
// editing this file never edits GOLD. Keep this package strictly type-only; if
// runtime values are ever added, consumers (e.g. ui-app) must declare
// `transpilePackages: ["@enta/types"]` in their Next config.
// =============================================================================

// -----------------------------------------------------------------------------
// VOIDMAP Types (mirror of VOIDMAP.yml)
// -----------------------------------------------------------------------------
export type VoidStatus = 'OPEN' | 'IN_PROGRESS' | 'SUSPENDED' | 'CLOSED';
export type VoidPriority = 'critical' | 'high' | 'medium' | 'med' | 'low';
export type VoidDomain = '[BIO]' | '[MATH]' | '[PHYS]' | '[CHEM]' | '[COMP]' | '[META]' | '[DEV]';

export interface Void {
  id: string;
  title: string;
  status: VoidStatus;
  priority: VoidPriority;
  owner: string | null;
  target_date?: string | null;
  domain: string;
  layer?: string;
  legacy_id?: string;
  legacy_source?: string;
  symptom: string;
  closing_path: string | null;
  evidence: string | string[] | null;
  created: string;
  closed: string | null;
  notes?: string;
}

export interface VoidMap {
  version: string;
  description: string;
  metadata: {
    maintainer: string;
    last_updated: string;
    generated_doc: string;
    reconciliation_notes?: string;
  };
  voids: Void[];
}

// -----------------------------------------------------------------------------
// Guard Types (mirror of CLAUDE.md G0–G6)
// -----------------------------------------------------------------------------
export type GuardStatus = 'ok' | 'warning' | 'error';

export interface Guard {
  id: string;
  name: string;
  shortRule: string;
  fullRule: string;
  status: GuardStatus;
  lastCheck?: Date;
}

// -----------------------------------------------------------------------------
// Metatron Types (G4 — Fokus vs. Aufmerksamkeit)
// -----------------------------------------------------------------------------
export type AttentionType = 'exploration' | 'context' | 'warning' | 'switch';

export interface AttentionItem {
  id: string;
  timestamp: Date;
  content: string;
  type: AttentionType;
}

export interface FocusState {
  current: string;
  since: Date;
  switchPending: boolean;
  proposedSwitch?: string;
}

// -----------------------------------------------------------------------------
// Navigation Types
// -----------------------------------------------------------------------------
export type NavItem = {
  id: string;
  label: string;
  icon: string;
  href: string;
};

// -----------------------------------------------------------------------------
// Filter Types
// -----------------------------------------------------------------------------
export interface VoidFilters {
  status: VoidStatus | 'ALL';
  priority: VoidPriority | 'ALL';
  domain: string | 'ALL';
}
