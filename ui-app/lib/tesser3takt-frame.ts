export type CollisionSemantics = 'EXACT_STATE_ID';
export type BoundaryHalf = 'EXIT' | 'ENTRY';
export type Quadrant = 'alpha' | 'beta' | 'gamma' | 'delta';
export type BoundaryCoordinateSpace = 'GLOBAL_REENTRY_LATTICE';
export type DigestStatus = 'VERIFIED' | 'UNVERIFIED';

export interface ProvenanceRef {
  kind: 'annex' | 'fixture' | 'calculation' | 'transport';
  source: string;
  revision: string;
  digest: string | null;
  digestStatus: DigestStatus;
  locator: string;
  claimLayer: 'MODEL' | 'SPEC' | 'FIXTURE' | 'RECEIPT';
  authorityStatus: 'repo-local' | 'external-unverified' | 'derived';
}

export interface BoundaryTransition {
  pairId: string;
  half: BoundaryHalf;
  stepIndex: number;
  stateId: string;
  quadrant: Quadrant;
  coordinateSpace: BoundaryCoordinateSpace;
  latticePosition: readonly [number, number];
  transformedFrom?: string;
  provenance: ProvenanceRef;
}

export interface TesserTickFrame {
  frameId: string;
  collisionSemantics: CollisionSemantics;
  leftStateId: string;
  rightStateId: string;
  collisionProxy: boolean;
  kenograms: readonly string[];
  boundaryTransitions: readonly BoundaryTransition[];
  provenance: readonly ProvenanceRef[];
}

export interface BoundaryPairValidationResult {
  valid: boolean;
  errors: string[];
}

export interface TesserTickFrameValidationResult extends BoundaryPairValidationResult {
  frame?: TesserTickFrame;
}

const PROVENANCE_KINDS = new Set<ProvenanceRef['kind']>([
  'annex',
  'fixture',
  'calculation',
  'transport',
]);
const DIGEST_STATUSES = new Set<DigestStatus>(['VERIFIED', 'UNVERIFIED']);
const CLAIM_LAYERS = new Set<ProvenanceRef['claimLayer']>([
  'MODEL',
  'SPEC',
  'FIXTURE',
  'RECEIPT',
]);
const AUTHORITY_STATUSES = new Set<ProvenanceRef['authorityStatus']>([
  'repo-local',
  'external-unverified',
  'derived',
]);
const BOUNDARY_HALVES = new Set<BoundaryHalf>(['EXIT', 'ENTRY']);
const QUADRANTS = new Set<Quadrant>(['alpha', 'beta', 'gamma', 'delta']);

const KNIGHT_DELTAS = new Set([
  '1:2',
  '2:1',
  '1:-2',
  '2:-1',
  '-1:2',
  '-2:1',
  '-1:-2',
  '-2:-1',
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function validateNonEmptyString(
  record: Record<string, unknown>,
  field: string,
  path: string,
  errors: string[],
): void {
  const value = record[field];
  if (typeof value !== 'string' || value.trim().length === 0) {
    errors.push(`${path}.${field}: expected a non-empty string`);
  }
}

function validateProvenanceRef(
  value: unknown,
  path: string,
  errors: string[],
): value is ProvenanceRef {
  const errorCount = errors.length;
  if (!isRecord(value)) {
    errors.push(`${path}: expected a provenance object`);
    return false;
  }

  if (!PROVENANCE_KINDS.has(value.kind as ProvenanceRef['kind'])) {
    errors.push(`${path}.kind: unsupported provenance kind`);
  }
  for (const field of ['source', 'revision', 'locator']) {
    validateNonEmptyString(value, field, path, errors);
  }
  if (!DIGEST_STATUSES.has(value.digestStatus as DigestStatus)) {
    errors.push(`${path}.digestStatus: expected VERIFIED or UNVERIFIED`);
  } else if (value.digestStatus === 'VERIFIED') {
    if (typeof value.digest !== 'string' || value.digest.trim().length === 0) {
      errors.push(`${path}.digest: VERIFIED provenance requires a non-empty digest`);
    }
  } else if (value.digest !== null) {
    errors.push(`${path}.digest: UNVERIFIED provenance requires digest: null`);
  }
  if (!CLAIM_LAYERS.has(value.claimLayer as ProvenanceRef['claimLayer'])) {
    errors.push(`${path}.claimLayer: unsupported claim layer`);
  }
  if (!AUTHORITY_STATUSES.has(value.authorityStatus as ProvenanceRef['authorityStatus'])) {
    errors.push(`${path}.authorityStatus: unsupported authority status`);
  }

  return errors.length === errorCount;
}

function validateBoundaryTransition(
  value: unknown,
  path: string,
  errors: string[],
): value is BoundaryTransition {
  const errorCount = errors.length;
  if (!isRecord(value)) {
    errors.push(`${path}: expected a boundary transition object`);
    return false;
  }

  for (const field of ['pairId', 'stateId']) {
    validateNonEmptyString(value, field, path, errors);
  }
  if (!BOUNDARY_HALVES.has(value.half as BoundaryHalf)) {
    errors.push(`${path}.half: expected EXIT or ENTRY`);
  }
  if (!Number.isInteger(value.stepIndex) || (value.stepIndex as number) < 0) {
    errors.push(`${path}.stepIndex: expected a non-negative integer`);
  }
  if (!QUADRANTS.has(value.quadrant as Quadrant)) {
    errors.push(`${path}.quadrant: unsupported quadrant`);
  }
  if (value.coordinateSpace !== 'GLOBAL_REENTRY_LATTICE') {
    errors.push(`${path}.coordinateSpace: expected GLOBAL_REENTRY_LATTICE`);
  }
  if (
    !Array.isArray(value.latticePosition) ||
    value.latticePosition.length !== 2 ||
    !value.latticePosition.every(Number.isInteger)
  ) {
    errors.push(`${path}.latticePosition: expected two integer global coordinates`);
  }
  if (
    value.transformedFrom !== undefined &&
    (typeof value.transformedFrom !== 'string' || value.transformedFrom.trim().length === 0)
  ) {
    errors.push(`${path}.transformedFrom: expected a non-empty state id when present`);
  }
  validateProvenanceRef(value.provenance, `${path}.provenance`, errors);

  return errors.length === errorCount;
}

export function isSlaterCollision(
  leftStateId: string,
  rightStateId: string,
  semantics: CollisionSemantics = 'EXACT_STATE_ID',
): boolean {
  if (semantics !== 'EXACT_STATE_ID') {
    return false;
  }

  return leftStateId === rightStateId;
}

export function withDerivedCollisionProxy<T extends Omit<TesserTickFrame, 'collisionProxy'>>(
  frame: T,
): T & Pick<TesserTickFrame, 'collisionProxy'> {
  return {
    ...frame,
    collisionProxy: isSlaterCollision(
      frame.leftStateId,
      frame.rightStateId,
      frame.collisionSemantics,
    ),
  };
}

export function validateBoundaryPairs(
  transitions: readonly BoundaryTransition[],
): BoundaryPairValidationResult {
  const errors: string[] = [];
  const pairs = new Map<string, BoundaryTransition[]>();

  transitions.forEach((transition) => {
    if (!pairs.has(transition.pairId)) {
      pairs.set(transition.pairId, []);
    }
    pairs.get(transition.pairId)?.push(transition);
  });

  pairs.forEach((pairTransitions, pairId) => {
    const exits = pairTransitions.filter((transition) => transition.half === 'EXIT');
    const entries = pairTransitions.filter((transition) => transition.half === 'ENTRY');

    if (exits.length !== 1 || entries.length !== 1) {
      errors.push(`${pairId}: expected exactly one EXIT and one ENTRY`);
      return;
    }

    const [exit] = exits;
    const [entry] = entries;

    if (exit.stepIndex >= entry.stepIndex) {
      errors.push(`${pairId}: EXIT must precede ENTRY`);
    }

    if (entry.transformedFrom !== exit.stateId) {
      errors.push(`${pairId}: ENTRY transformedFrom must match EXIT stateId`);
    }

    if (exit.coordinateSpace !== entry.coordinateSpace) {
      errors.push(`${pairId}: EXIT and ENTRY must use the same coordinate space`);
    }
    if (exit.coordinateSpace !== 'GLOBAL_REENTRY_LATTICE') {
      errors.push(`${pairId}: EXIT must use GLOBAL_REENTRY_LATTICE`);
    }
    if (entry.coordinateSpace !== 'GLOBAL_REENTRY_LATTICE') {
      errors.push(`${pairId}: ENTRY must use GLOBAL_REENTRY_LATTICE`);
    }
    if (
      exit.coordinateSpace !== entry.coordinateSpace ||
      exit.coordinateSpace !== 'GLOBAL_REENTRY_LATTICE' ||
      entry.coordinateSpace !== 'GLOBAL_REENTRY_LATTICE'
    ) {
      return;
    }

    const [exitX, exitY] = exit.latticePosition;
    const [entryX, entryY] = entry.latticePosition;
    const delta = `${entryX - exitX}:${entryY - exitY}`;
    if (!KNIGHT_DELTAS.has(delta)) {
      errors.push(`${pairId}: EXIT→ENTRY move is not knight-legal in the global lattice`);
    }
  });

  const uniqueKeys = new Set<string>();
  transitions.forEach((transition) => {
    const key = `${transition.pairId}:${transition.half}`;
    if (uniqueKeys.has(key)) {
      errors.push(`${transition.pairId}: duplicate ${transition.half} half`);
    }
    uniqueKeys.add(key);
  });

  return { valid: errors.length === 0, errors };
}

export function validateTesserTickFrame(input: unknown): TesserTickFrameValidationResult {
  const errors: string[] = [];
  if (!isRecord(input)) {
    return { valid: false, errors: ['$: expected a frame object'] };
  }

  for (const field of ['frameId', 'leftStateId', 'rightStateId']) {
    validateNonEmptyString(input, field, '$', errors);
  }
  if (input.collisionSemantics !== 'EXACT_STATE_ID') {
    errors.push('$.collisionSemantics: expected EXACT_STATE_ID');
  }
  if (typeof input.collisionProxy !== 'boolean') {
    errors.push('$.collisionProxy: expected a boolean');
  } else if (
    typeof input.leftStateId === 'string' &&
    typeof input.rightStateId === 'string' &&
    input.collisionSemantics === 'EXACT_STATE_ID' &&
    input.collisionProxy !==
      isSlaterCollision(input.leftStateId, input.rightStateId, input.collisionSemantics)
  ) {
    errors.push('$.collisionProxy: value does not match the derived collision state');
  }

  if (!Array.isArray(input.kenograms)) {
    errors.push('$.kenograms: expected an array');
  } else {
    input.kenograms.forEach((kenogram, index) => {
      if (typeof kenogram !== 'string' || kenogram.trim().length === 0) {
        errors.push(`$.kenograms[${index}]: expected a non-empty string`);
      }
    });
  }

  const transitions: BoundaryTransition[] = [];
  if (!Array.isArray(input.boundaryTransitions)) {
    errors.push('$.boundaryTransitions: expected an array');
  } else {
    input.boundaryTransitions.forEach((transition, index) => {
      if (
        validateBoundaryTransition(
          transition,
          `$.boundaryTransitions[${index}]`,
          errors,
        )
      ) {
        transitions.push(transition);
      }
    });
    if (transitions.length === input.boundaryTransitions.length) {
      errors.push(...validateBoundaryPairs(transitions).errors);
    }
  }

  if (!Array.isArray(input.provenance)) {
    errors.push('$.provenance: expected an array');
  } else {
    input.provenance.forEach((provenance, index) => {
      validateProvenanceRef(provenance, `$.provenance[${index}]`, errors);
    });
  }

  if (errors.length > 0) {
    return { valid: false, errors };
  }
  return { valid: true, errors, frame: input as unknown as TesserTickFrame };
}
