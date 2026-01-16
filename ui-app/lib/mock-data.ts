import { AttentionItem, FocusState } from '@/types';

// Mock attention stream items for Metatron HUD
export const MOCK_ATTENTION_ITEMS: AttentionItem[] = [
  {
    id: '1',
    timestamp: new Date(Date.now() - 1000),
    content: 'Reading VOIDMAP.yml structure...',
    type: 'exploration',
  },
  {
    id: '2',
    timestamp: new Date(Date.now() - 2000),
    content: 'Found 12 VOIDs, 3 CLOSED',
    type: 'context',
  },
  {
    id: '3',
    timestamp: new Date(Date.now() - 5000),
    content: 'Checking guard definitions...',
    type: 'exploration',
  },
  {
    id: '4',
    timestamp: new Date(Date.now() - 8000),
    content: 'G4 relevant: Fokus stable',
    type: 'context',
  },
  {
    id: '5',
    timestamp: new Date(Date.now() - 12000),
    content: '⚠️ Potential scope change detected',
    type: 'warning',
  },
];

// Mock focus state
export const MOCK_FOCUS_STATE: FocusState = {
  current: 'UI-Prototyp erstellen',
  since: new Date(Date.now() - 3600000), // 1 hour ago
  switchPending: false,
};

// Generate new attention item (for simulated live stream)
let itemCounter = 100;

const EXPLORATION_ITEMS = [
  'Scanning component structure...',
  'Analyzing data flow...',
  'Checking imports...',
  'Reading documentation...',
  'Exploring dependencies...',
  'Mapping file hierarchy...',
];

const CONTEXT_ITEMS = [
  'Found relevant pattern',
  'Context established',
  'Dependencies resolved',
  'Structure understood',
  'Pattern recognized',
];

const WARNING_ITEMS = [
  '⚠️ Scope boundary reached',
  '⚠️ Consider CHECKPOINT',
  '⚠️ External content detected',
  '⚠️ GOLD file in scope',
];

export function generateAttentionItem(): AttentionItem {
  const rand = Math.random();
  let type: AttentionItem['type'];
  let content: string;

  if (rand < 0.5) {
    type = 'exploration';
    content = EXPLORATION_ITEMS[Math.floor(Math.random() * EXPLORATION_ITEMS.length)];
  } else if (rand < 0.85) {
    type = 'context';
    content = CONTEXT_ITEMS[Math.floor(Math.random() * CONTEXT_ITEMS.length)];
  } else {
    type = 'warning';
    content = WARNING_ITEMS[Math.floor(Math.random() * WARNING_ITEMS.length)];
  }

  return {
    id: String(itemCounter++),
    timestamp: new Date(),
    content,
    type,
  };
}

// Nichtraum mock data
export const NICHTRAUM_ZONES = [
  {
    id: 'archive',
    name: 'Archive',
    description: 'Gelöschte/archivierte Items',
    icon: '📦',
    itemCount: 0,
  },
  {
    id: 'maybe',
    name: 'Maybe',
    description: 'Unentschiedenes',
    icon: '❓',
    itemCount: 0,
  },
  {
    id: 'quarantine',
    name: 'Quarantine',
    description: 'Verdächtige Inhalte',
    icon: '🔒',
    itemCount: 0,
  },
];
