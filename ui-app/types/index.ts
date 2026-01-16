// =============================================================================
// EntaENGELment UI Types
// =============================================================================

// VOIDMAP Types
export type VoidStatus = 'OPEN' | 'IN_PROGRESS' | 'CLOSED';
export type VoidPriority = 'critical' | 'high' | 'medium' | 'med' | 'low';
export type VoidDomain = '[BIO]' | '[MATH]' | '[PHYS]' | '[CHEM]' | '[COMP]' | '[META]' | '[DEV]';

export interface Void {
  id: string;
  title: string;
  status: VoidStatus;
  priority: VoidPriority;
  owner: string | null;
  domain: string;
  symptom: string;
  closing_path: string | null;
  evidence: string | string[] | null;
  created: string;
  closed: string | null;
  notes?: string;
  layer?: string;
}

export interface VoidMap {
  version: string;
  description: string;
  metadata: {
    maintainer: string;
    last_updated: string;
    generated_doc: string;
  };
  voids: Void[];
}

// Guard Types
export type GuardStatus = 'ok' | 'warning' | 'error';

export interface Guard {
  id: string;
  name: string;
  shortRule: string;
  fullRule: string;
  status: GuardStatus;
  lastCheck?: Date;
}

// Metatron Types
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

// Navigation Types
export type NavItem = {
  id: string;
  label: string;
  icon: string;
  href: string;
};

// Filter Types
export interface VoidFilters {
  status: VoidStatus | 'ALL';
  priority: VoidPriority | 'ALL';
  domain: string | 'ALL';
}
