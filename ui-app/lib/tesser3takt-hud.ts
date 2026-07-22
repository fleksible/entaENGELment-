import {
  validateTesserTickFrame,
  withDerivedCollisionProxy,
  type BoundaryTransition,
  type ProvenanceRef,
  type TesserTickFrame as CanonicalTesserTickFrame,
} from './tesser3takt-frame.ts';

export type ClaimLayer =
  | 'FACT'
  | 'FORMAL'
  | 'MODEL'
  | 'METAPHOR'
  | 'POETRY'
  | 'GUARD';

export type KenoStatus =
  | 'UNOBSERVED'
  | 'UNBOUND'
  | 'CONFLICT'
  | 'WITHHELD'
  | 'FORBIDDEN';

export type GuardState = 'PASS' | 'HOLD' | 'LOOP' | 'STOP';

export type RegimeState =
  | 'SYMMETRIC'
  | 'CRITICAL'
  | 'BROKEN'
  | 'LOOSENED'
  | 'OVERWOUND';

export type ObserverMode = 'OUTER' | 'INNER' | 'INVERSE';

export interface HudAnchor {
  id: string;
  label: string;
  x: number;
  y: number;
  layer: ClaimLayer;
}

export interface ResolutionGate {
  needsHumanCommit: boolean;
  needsCounterfixture: boolean;
  needsClaimAudit: boolean;
  needsConsent: boolean;
}

export interface KenoFringe {
  id: `Kη-${string}`;
  label: string;
  status: KenoStatus;
  layer: ClaimLayer;
  anchors: string[];
  missingOperator?: string;
  competingOperators?: string[];
  provenance: readonly ProvenanceRef[];
  resolutionGate: ResolutionGate;
  allowPersistentVoid: true;
}

export interface KnightStep {
  id: string;
  quadrant: 0 | 1 | 2 | 3;
  column: number;
  row: number;
}

export interface GuardInputs {
  consentFailed?: boolean;
  focusSwitchPending?: boolean;
  forbiddenCouplingAttempted?: boolean;
  claimPromotionRequested?: boolean;
  receiptPending?: boolean;
  loopRequested?: boolean;
}

export interface SemanticAssistConfig {
  enabled: false;
  provider: 'hugging-face';
  modelRef: string;
  role: 'candidate-neighbor-ranking';
  canResolveKenograms: false;
  canPromoteClaims: false;
  persistence: 'none';
}

export interface VerificationWitnesses {
  knightGraph: {
    vertices: 63;
    edges: 164;
    connected: true;
    bipartite: true;
    diameter: 6;
  };
  s4AdjacentSwapGraph: {
    vertices: 24;
    edges: 36;
    regularDegree: 3;
    connected: true;
    bipartite: true;
    diameter: 6;
  };
  sierpinskiDimension: number;
  slaterDuplicateRowsDeterminant: 0;
}

export interface TesserHudFrame {
  schemaVersion: '0.2';
  authorityStatus: 'annex';
  artifactType: 'ui-lab';
  projectionOnly: true;
  transport: CanonicalTesserTickFrame;
  observerMode: ObserverMode;
  regime: {
    control: number;
    orderParameter: number;
    torsion: number;
    state: RegimeState;
  };
  zLayer: number;
  guardState: GuardState;
  portal: {
    left: 'ORANGE';
    right: 'BLUE';
    leftStateId: string;
    rightStateId: string;
    handednessPreserved: true;
    determinantProxy: 0 | 1;
  };
  quadrants: {
    count: 4;
    rows: 7;
    columns: 9;
    addressableCells: 63;
    residualChannel: 'X';
    boundaryRule: 'ONE_TRANSITION_TWO_PROJECTIONS';
  };
  lyraChannels: 7;
  kenograms: readonly KenoFringe[];
  semanticAssist: SemanticAssistConfig;
  verification: VerificationWitnesses;
  constraints: {
    autoplay: false;
    telemetry: false;
    claimUpgrade: false;
    persistentVoidAllowed: true;
    humanCommitRequiredForPromotion: true;
  };
}

export const LYRA_CHANNELS = [
  { id: 'L1', note: 'C' },
  { id: 'L2', note: 'D' },
  { id: 'L3', note: 'E' },
  { id: 'L4', note: 'F' },
  { id: 'L5', note: 'G' },
  { id: 'L6', note: 'A' },
  { id: 'L7', note: 'B' },
] as const;

export const LYRA_NOTES = LYRA_CHANNELS.map((channel) => channel.note);

function provenanceRef(reference: string): ProvenanceRef {
  const separator = reference.indexOf(':');
  const namespace = separator === -1 ? 'repo' : reference.slice(0, separator);
  const locator = separator === -1 ? reference : reference.slice(separator + 1);

  const source =
    namespace === 'repo'
      ? 'fleksible/entaENGELment-'
      : namespace === 'drive'
        ? 'Google Drive annex'
        : namespace === 'wolfram'
          ? 'Wolfram Language calculation'
          : 'conversation transport';

  return {
    kind:
      namespace === 'wolfram'
        ? 'calculation'
        : namespace === 'chat'
          ? 'transport'
          : 'annex',
    source,
    revision: 'unverified',
    digest: null,
    digestStatus: 'UNVERIFIED',
    locator,
    claimLayer: namespace === 'repo' ? 'SPEC' : 'MODEL',
    authorityStatus:
      namespace === 'wolfram'
        ? 'derived'
        : namespace === 'repo'
          ? 'repo-local'
          : 'external-unverified',
  };
}

function provenanceRefs(...references: string[]): readonly ProvenanceRef[] {
  return references.map(provenanceRef);
}

export const PORTAL_LEFT_STATE_ID = 'S4:1234';
export const PORTAL_DISTINCT_RIGHT_STATE_ID = 'S4:2143';

const BOUNDARY_PROVENANCE = provenanceRef(
  'repo:docs/spec/tesser3takt_hud_v0_2.md#5-boundary-half-step-invariant',
);

export const HUD_BOUNDARY_TRANSITIONS: readonly BoundaryTransition[] = [
  {
    pairId: 'B-Q0-Q1',
    half: 'EXIT',
    stepIndex: 4,
    stateId: 'hud:N04',
    quadrant: 'alpha',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [8, 5],
    provenance: BOUNDARY_PROVENANCE,
  },
  {
    pairId: 'B-Q0-Q1',
    half: 'ENTRY',
    stepIndex: 5,
    stateId: 'hud:N05',
    quadrant: 'beta',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [9, 7],
    transformedFrom: 'hud:N04',
    provenance: BOUNDARY_PROVENANCE,
  },
  {
    pairId: 'B-Q1-Q3',
    half: 'EXIT',
    stepIndex: 9,
    stateId: 'hud:N09',
    quadrant: 'beta',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [17, 7],
    provenance: BOUNDARY_PROVENANCE,
  },
  {
    pairId: 'B-Q1-Q3',
    half: 'ENTRY',
    stepIndex: 10,
    stateId: 'hud:N10',
    quadrant: 'delta',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [19, 8],
    transformedFrom: 'hud:N09',
    provenance: BOUNDARY_PROVENANCE,
  },
  {
    pairId: 'B-Q3-Q2',
    half: 'EXIT',
    stepIndex: 14,
    stateId: 'hud:N14',
    quadrant: 'delta',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [19, 14],
    provenance: BOUNDARY_PROVENANCE,
  },
  {
    pairId: 'B-Q3-Q2',
    half: 'ENTRY',
    stepIndex: 15,
    stateId: 'hud:N15',
    quadrant: 'gamma',
    coordinateSpace: 'GLOBAL_REENTRY_LATTICE',
    latticePosition: [18, 16],
    transformedFrom: 'hud:N14',
    provenance: BOUNDARY_PROVENANCE,
  },
];

const HUD_FRAME_PROVENANCE = provenanceRefs(
  'repo:docs/spec/tesser3takt_hud_v0_2.md',
  'drive:Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_2.docx',
  'wolfram:knight-graph-7x9-and-s4-adjacent-transpositions',
);

export const KNIGHT_TRAJECTORY: KnightStep[] = [
  { id: 'N00', quadrant: 0, column: 0, row: 5 },
  { id: 'N01', quadrant: 0, column: 2, row: 4 },
  { id: 'N02', quadrant: 0, column: 4, row: 5 },
  { id: 'N03', quadrant: 0, column: 6, row: 4 },
  { id: 'N04', quadrant: 0, column: 8, row: 5 },
  { id: 'N05', quadrant: 1, column: 0, row: 1 },
  { id: 'N06', quadrant: 1, column: 2, row: 0 },
  { id: 'N07', quadrant: 1, column: 4, row: 1 },
  { id: 'N08', quadrant: 1, column: 6, row: 0 },
  { id: 'N09', quadrant: 1, column: 8, row: 1 },
  { id: 'N10', quadrant: 3, column: 7, row: 5 },
  { id: 'N11', quadrant: 3, column: 5, row: 6 },
  { id: 'N12', quadrant: 3, column: 3, row: 5 },
  { id: 'N13', quadrant: 3, column: 1, row: 6 },
  { id: 'N14', quadrant: 3, column: 0, row: 4 },
  { id: 'N15', quadrant: 2, column: 8, row: 1 },
  { id: 'N16', quadrant: 2, column: 6, row: 2 },
  { id: 'N17', quadrant: 2, column: 4, row: 1 },
  { id: 'N18', quadrant: 2, column: 2, row: 2 },
  { id: 'N19', quadrant: 2, column: 0, row: 1 },
];

export const KENO_FRINGES: KenoFringe[] = [
  {
    id: 'Kη-01',
    label: 'Landau-Übersetzung',
    status: 'UNBOUND',
    layer: 'MODEL',
    anchors: ['landau-control', 'hud-regime'],
    missingOperator: 'dimensionless-regime-calibration',
    provenance: provenanceRefs('drive:ANNEX_F', 'wolfram:quartic-witness'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-02',
    label: 'Vortex–Bifröst-Projektion',
    status: 'UNOBSERVED',
    layer: 'MODEL',
    anchors: ['vortex-inner', 'wheeler-outer'],
    missingOperator: 'continuous-to-sliced-projection',
    provenance: provenanceRefs('chat:caduceus-bifrost'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-03',
    label: 'Wheeler-Transport',
    status: 'UNBOUND',
    layer: 'FORMAL',
    anchors: ['phase', 'provenance', 'holonomy'],
    missingOperator: 'slice-transport-receipt',
    provenance: provenanceRefs('chat:wheeler-slices'),
    resolutionGate: {
      needsHumanCommit: false,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-04',
    label: 'Portal-Antisymmetrie',
    status: 'CONFLICT',
    layer: 'FORMAL',
    anchors: ['orange-portal', 'blue-portal', 'slater'],
    competingOperators: ['exact-state-equality', 'equivalence-up-to-symmetry'],
    provenance: provenanceRefs('wolfram:duplicate-row-determinant-zero'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-05',
    label: 'Majorana/Fermi-Inversion',
    status: 'UNOBSERVED',
    layer: 'METAPHOR',
    anchors: ['majorana-void', 'fermi-outside'],
    missingOperator: 'perspective-invariant-map',
    provenance: provenanceRefs('chat:inverse-pov'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-06',
    label: 'Curie–ADR-Extremachse',
    status: 'UNBOUND',
    layer: 'MODEL',
    anchors: ['curie', 'adiabatic-demagnetization'],
    missingOperator: 'dimensionless-extreme-axis',
    provenance: provenanceRefs('chat:curie-adr-axis'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-07',
    label: '7×9-Grenzsprung',
    status: 'UNBOUND',
    layer: 'FORMAL',
    anchors: ['knight-path', 'quadrant-boundary'],
    missingOperator: 'shared-boundary-transition-id',
    provenance: provenanceRefs('wolfram:knight-graph-7x9', 'drive:ANNEX_F'),
    resolutionGate: {
      needsHumanCommit: false,
      needsCounterfixture: true,
      needsClaimAudit: false,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-08',
    label: 'zN-Tiefe',
    status: 'UNOBSERVED',
    layer: 'MODEL',
    anchors: ['zn-stack', 'stored-transform'],
    missingOperator: 'depth-composition-law',
    provenance: provenanceRefs('chat:zn-depth'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-09',
    label: 'Nicht-Raum / Not-at-ion',
    status: 'UNBOUND',
    layer: 'METAPHOR',
    anchors: ['latex-ast', 'chemical-notation', 'assembly-ledger'],
    missingOperator: 'typed-notation-to-assembly-bridge',
    provenance: provenanceRefs('chat:not-at-ion'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-10',
    label: 'Consent-Telemetrie',
    status: 'WITHHELD',
    layer: 'GUARD',
    anchors: ['crank', 'slice', 'breadcrumb'],
    missingOperator: 'explicit-granular-consent',
    provenance: provenanceRefs('repo:G0-consent-boundary'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: true,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-11',
    label: 'Claim-Migration',
    status: 'FORBIDDEN',
    layer: 'GUARD',
    anchors: ['poetry', 'model', 'claim-registry'],
    missingOperator: 'human-reviewed-promotion-receipt',
    provenance: provenanceRefs('repo:claim-tag-runtime-mapping'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
  {
    id: 'Kη-12',
    label: 'Kenogrammstatus',
    status: 'CONFLICT',
    layer: 'FORMAL',
    anchors: ['unobserved', 'unbound', 'conflict', 'withheld', 'forbidden'],
    competingOperators: ['workflow-status', 'epistemic-status', 'authority-status'],
    provenance: provenanceRefs('repo:voidmap', 'repo:claim-tag-runtime-mapping'),
    resolutionGate: {
      needsHumanCommit: true,
      needsCounterfixture: true,
      needsClaimAudit: true,
      needsConsent: false,
    },
    allowPersistentVoid: true,
  },
];

export const SEMANTIC_ASSIST: SemanticAssistConfig = {
  enabled: false,
  provider: 'hugging-face',
  modelRef: 'intfloat/multilingual-e5-small',
  role: 'candidate-neighbor-ranking',
  canResolveKenograms: false,
  canPromoteClaims: false,
  persistence: 'none',
};

export const VERIFICATION_WITNESSES: VerificationWitnesses = {
  knightGraph: {
    vertices: 63,
    edges: 164,
    connected: true,
    bipartite: true,
    diameter: 6,
  },
  s4AdjacentSwapGraph: {
    vertices: 24,
    edges: 36,
    regularDegree: 3,
    connected: true,
    bipartite: true,
    diameter: 6,
  },
  sierpinskiDimension: 1.584962500721156,
  slaterDuplicateRowsDeterminant: 0,
};

export function landauPotential(
  phi: number,
  control: number,
  quartic = 1,
): number {
  return 0.5 * control * phi * phi + 0.25 * quartic * phi ** 4;
}

export function deriveOrderParameter(control: number, quartic = 1): number {
  if (control >= 0 || quartic <= 0) return 0;
  return Math.sqrt(Math.abs(control) / quartic);
}

export function deriveRegimeState(
  control: number,
  torsion: number,
): RegimeState {
  if (torsion > 0.88) return 'OVERWOUND';
  if (torsion < 0.12) return 'LOOSENED';
  if (Math.abs(control) < 0.08) return 'CRITICAL';
  return control < 0 ? 'BROKEN' : 'SYMMETRIC';
}

export function deriveGuardState(inputs: GuardInputs = {}): GuardState {
  if (
    inputs.consentFailed ||
    inputs.focusSwitchPending ||
    inputs.forbiddenCouplingAttempted
  ) {
    return 'STOP';
  }

  if (inputs.claimPromotionRequested || inputs.receiptPending) {
    return 'HOLD';
  }

  if (inputs.loopRequested) return 'LOOP';
  return 'PASS';
}

export function buildTesserHudFrame(input: {
  observerMode: ObserverMode;
  control: number;
  torsion: number;
  zLayer: number;
  leftStateId: string;
  rightStateId: string;
  guardInputs?: GuardInputs;
}): TesserHudFrame {
  const transport = withDerivedCollisionProxy({
    frameId: 'tesser3takt-hud-v0.2',
    collisionSemantics: 'EXACT_STATE_ID' as const,
    leftStateId: input.leftStateId,
    rightStateId: input.rightStateId,
    kenograms: KENO_FRINGES.map((fringe) => fringe.id),
    boundaryTransitions: HUD_BOUNDARY_TRANSITIONS,
    provenance: HUD_FRAME_PROVENANCE,
  });
  const validation = validateTesserTickFrame(transport);
  if (!validation.valid) {
    throw new Error(`Invalid tesser3TAKT transport: ${validation.errors.join('; ')}`);
  }

  return {
    schemaVersion: '0.2',
    authorityStatus: 'annex',
    artifactType: 'ui-lab',
    projectionOnly: true,
    transport,
    observerMode: input.observerMode,
    regime: {
      control: input.control,
      orderParameter: deriveOrderParameter(input.control),
      torsion: input.torsion,
      state: deriveRegimeState(input.control, input.torsion),
    },
    zLayer: input.zLayer,
    guardState: deriveGuardState(input.guardInputs),
    portal: {
      left: 'ORANGE',
      right: 'BLUE',
      leftStateId: transport.leftStateId,
      rightStateId: transport.rightStateId,
      handednessPreserved: true,
      determinantProxy: transport.collisionProxy ? 0 : 1,
    },
    quadrants: {
      count: 4,
      rows: 7,
      columns: 9,
      addressableCells: 63,
      residualChannel: 'X',
      boundaryRule: 'ONE_TRANSITION_TWO_PROJECTIONS',
    },
    lyraChannels: 7,
    kenograms: KENO_FRINGES,
    semanticAssist: SEMANTIC_ASSIST,
    verification: VERIFICATION_WITNESSES,
    constraints: {
      autoplay: false,
      telemetry: false,
      claimUpgrade: false,
      persistentVoidAllowed: true,
      humanCommitRequiredForPromotion: true,
    },
  };
}
