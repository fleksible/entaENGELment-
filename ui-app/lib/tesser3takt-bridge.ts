import {
  validateBoundaryPairs,
  type BoundaryTransition,
  type ProvenanceRef,
} from './tesser3takt-frame.ts';

export type ResolutionScale = 'MICRO' | 'MESO' | 'MACRO';
export type ExtentScope = 'TRAVERSAL_CELL' | 'TRAVERSAL_SLICE';

export type RegisteredClaimTag =
  | 'ROHSEDIMENT'
  | 'METAPHER'
  | 'HYPOTHESE'
  | 'INFERENZ'
  | 'MODEL'
  | 'FACT'
  | 'SPEC-WIP'
  | 'SPEC'
  | 'CANON'
  | 'VOID'
  | 'ROSETTA'
  | 'ANNEX'
  | 'CONTEXT'
  | 'BRIDGE-WIP'
  | 'UI-LAB'
  | 'SIMULATION_PROXY';

export type OriginEvidenceRole = 'CLAIM_BEARING' | 'PROVENANCE_ONLY';

export interface ImmutableClaimOrigin {
  readonly claimTag: RegisteredClaimTag;
  readonly evidenceRole: OriginEvidenceRole;
  readonly immutable: true;
}

export const REQUIRED_PRESERVED_INVARIANTS = [
  'BOUNDARY_PAIR_IDENTITY',
  'EVENT_ORDER',
  'DIRECTIONAL_CONNECTIVITY',
  'PROVENANCE_BINDING',
  'ORIGIN_CLAIM_LEVEL',
] as const;

export type PreservedInvariant = (typeof REQUIRED_PRESERVED_INVARIANTS)[number];

export const REQUIRED_FALSIFIERS = [
  'MISSING_OR_REORDERED_BOUNDARY_HALF',
  'CHANGED_CONNECTIVITY',
  'LOST_PROVENANCE',
  'LOST_CLAIM_ORIGIN',
] as const;

export type BridgeFalsifier = (typeof REQUIRED_FALSIFIERS)[number];

export interface ScaleAddress {
  readonly resolutionScale: ResolutionScale;
  readonly extentScope: ExtentScope;
}

export interface MicroToMesoBridgeRequest {
  readonly bridgeId: string;
  readonly sourceFrameId: string;
  readonly from: ScaleAddress;
  readonly to: ScaleAddress;
  readonly transitions: readonly BoundaryTransition[];
  readonly preservedInvariants: readonly PreservedInvariant[];
  readonly measuredOrDeclaredLoss: readonly string[];
  readonly falsifiers: readonly BridgeFalsifier[];
  readonly evidenceRefs: readonly ProvenanceRef[];
  readonly origin: ImmutableClaimOrigin;
}

export interface TraceEvent {
  readonly pairId: string;
  readonly half: BoundaryTransition['half'];
  readonly stepIndex: number;
}

export interface TraceConnection {
  readonly pairId: string;
  readonly fromStateId: string;
  readonly toStateId: string;
  readonly fromPosition: readonly [number, number];
  readonly toPosition: readonly [number, number];
  readonly exitProvenance: Readonly<ProvenanceRef>;
  readonly entryProvenance: Readonly<ProvenanceRef>;
}

export interface TransitionTrace {
  readonly traceId: string;
  readonly bridgeId: string;
  readonly sourceFrameId: string;
  readonly authorityStatus: 'derived';
  readonly from: Readonly<ScaleAddress>;
  readonly to: Readonly<ScaleAddress>;
  readonly pairOrder: readonly string[];
  readonly eventOrder: readonly Readonly<TraceEvent>[];
  readonly connectivity: readonly Readonly<TraceConnection>[];
  readonly preservedInvariants: readonly PreservedInvariant[];
  readonly measuredOrDeclaredLoss: readonly string[];
  readonly falsifiers: readonly BridgeFalsifier[];
  readonly evidenceRefs: readonly Readonly<ProvenanceRef>[];
  readonly origin: Readonly<ImmutableClaimOrigin>;
}

export type BridgeRejectCode = 'BRIDGE_INCOMPLETE' | 'BRIDGE_FALSIFIED';

export type BridgeResult =
  | {
      readonly accepted: true;
      readonly decision: 'PASS_CANDIDATE';
      readonly errors: readonly [];
      readonly trace: Readonly<TransitionTrace>;
    }
  | {
      readonly accepted: false;
      readonly decision: 'REJECT';
      readonly code: BridgeRejectCode;
      readonly errors: readonly string[];
    };

const CLAIM_TAGS = new Set<RegisteredClaimTag>([
  'ROHSEDIMENT',
  'METAPHER',
  'HYPOTHESE',
  'INFERENZ',
  'MODEL',
  'FACT',
  'SPEC-WIP',
  'SPEC',
  'CANON',
  'VOID',
  'ROSETTA',
  'ANNEX',
  'CONTEXT',
  'BRIDGE-WIP',
  'UI-LAB',
  'SIMULATION_PROXY',
]);

const EVIDENCE_ROLES = new Set<OriginEvidenceRole>(['CLAIM_BEARING', 'PROVENANCE_ONLY']);
const PROVENANCE_KINDS = new Set<ProvenanceRef['kind']>([
  'annex',
  'fixture',
  'calculation',
  'transport',
]);
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
const QUADRANTS = new Set<BoundaryTransition['quadrant']>([
  'alpha',
  'beta',
  'gamma',
  'delta',
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function validateDenseArray(value: unknown, path: string, errors: string[]): value is unknown[] {
  if (!Array.isArray(value)) {
    errors.push(`${path}: expected an array`);
    return false;
  }

  for (let index = 0; index < value.length; index += 1) {
    if (!(index in value)) {
      errors.push(`${path}[${index}]: sparse array entries are not allowed`);
    }
  }
  return true;
}

function validateNonEmptyStringArray(
  value: unknown,
  path: string,
  errors: string[],
): value is string[] {
  const errorCount = errors.length;
  if (!validateDenseArray(value, path, errors)) {
    return false;
  }
  if (value.length === 0) {
    errors.push(`${path}: expected at least one entry`);
  }
  value.forEach((entry, index) => {
    if (!isNonEmptyString(entry)) {
      errors.push(`${path}[${index}]: expected a non-empty string`);
    }
  });
  return errors.length === errorCount;
}

function validateScaleAddress(
  value: unknown,
  path: string,
  expectedResolution: ResolutionScale,
  expectedExtent: ExtentScope,
  errors: string[],
): value is ScaleAddress {
  const errorCount = errors.length;
  if (!isRecord(value)) {
    errors.push(`${path}: expected a scale address`);
    return false;
  }
  if (value.resolutionScale !== expectedResolution) {
    errors.push(`${path}.resolutionScale: expected ${expectedResolution}`);
  }
  if (value.extentScope !== expectedExtent) {
    errors.push(`${path}.extentScope: expected ${expectedExtent}`);
  }
  return errors.length === errorCount;
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
    if (!isNonEmptyString(value[field])) {
      errors.push(`${path}.${field}: expected a non-empty string`);
    }
  }
  if (value.digestStatus !== 'VERIFIED' && value.digestStatus !== 'UNVERIFIED') {
    errors.push(`${path}.digestStatus: expected VERIFIED or UNVERIFIED`);
  } else if (value.digestStatus === 'VERIFIED' && !isNonEmptyString(value.digest)) {
    errors.push(`${path}.digest: VERIFIED provenance requires a non-empty digest`);
  } else if (value.digestStatus === 'UNVERIFIED' && value.digest !== null) {
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

function validateBoundaryTransitionShape(
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
    if (!isNonEmptyString(value[field])) {
      errors.push(`${path}.${field}: expected a non-empty string`);
    }
  }
  if (value.half !== 'EXIT' && value.half !== 'ENTRY') {
    errors.push(`${path}.half: expected EXIT or ENTRY`);
  }
  if (!Number.isInteger(value.stepIndex) || (value.stepIndex as number) < 0) {
    errors.push(`${path}.stepIndex: expected a non-negative integer`);
  }
  if (!QUADRANTS.has(value.quadrant as BoundaryTransition['quadrant'])) {
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
  if (value.transformedFrom !== undefined && !isNonEmptyString(value.transformedFrom)) {
    errors.push(`${path}.transformedFrom: expected a non-empty state id when present`);
  }
  validateProvenanceRef(value.provenance, `${path}.provenance`, errors);
  return errors.length === errorCount;
}

function validateClaimOrigin(
  value: unknown,
  path: string,
  errors: string[],
): value is ImmutableClaimOrigin {
  const errorCount = errors.length;
  if (!isRecord(value)) {
    errors.push(`${path}: expected an origin object`);
    return false;
  }
  if (!CLAIM_TAGS.has(value.claimTag as RegisteredClaimTag)) {
    errors.push(`${path}.claimTag: expected a registered claim tag`);
  }
  if (!EVIDENCE_ROLES.has(value.evidenceRole as OriginEvidenceRole)) {
    errors.push(`${path}.evidenceRole: expected CLAIM_BEARING or PROVENANCE_ONLY`);
  }
  if (value.immutable !== true) {
    errors.push(`${path}.immutable: expected true`);
  }
  return errors.length === errorCount;
}

function validateRequiredEnumValues<T extends string>(
  value: unknown,
  path: string,
  required: readonly T[],
  errors: string[],
): value is T[] {
  const errorCount = errors.length;
  if (!validateNonEmptyStringArray(value, path, errors)) {
    return false;
  }

  const supported = new Set(required);
  value.forEach((entry, index) => {
    if (!supported.has(entry as T)) {
      errors.push(`${path}[${index}]: unsupported value ${entry}`);
    }
  });
  for (const requiredEntry of required) {
    if (!value.includes(requiredEntry)) {
      errors.push(`${path}: missing required value ${requiredEntry}`);
    }
  }
  if (new Set(value).size !== value.length) {
    errors.push(`${path}: duplicate values are not allowed`);
  }
  return errors.length === errorCount;
}

function reject(code: BridgeRejectCode, errors: string[]): BridgeResult {
  return {
    accepted: false,
    decision: 'REJECT',
    code,
    errors: Object.freeze([...errors]),
  };
}

function frozenProvenance(reference: ProvenanceRef): Readonly<ProvenanceRef> {
  return Object.freeze({ ...reference });
}

function buildFrozenTrace(request: MicroToMesoBridgeRequest): Readonly<TransitionTrace> {
  const pairOrder: string[] = [];
  for (const transition of request.transitions) {
    if (transition.half === 'EXIT') {
      pairOrder.push(transition.pairId);
    }
  }

  const connectivity = pairOrder.map((pairId): Readonly<TraceConnection> => {
    const exit = request.transitions.find(
      (transition) => transition.pairId === pairId && transition.half === 'EXIT',
    );
    const entry = request.transitions.find(
      (transition) => transition.pairId === pairId && transition.half === 'ENTRY',
    );

    if (!exit || !entry) {
      throw new Error(`validated pair ${pairId} became incomplete`);
    }

    return Object.freeze({
      pairId,
      fromStateId: exit.stateId,
      toStateId: entry.stateId,
      fromPosition: Object.freeze([...exit.latticePosition]) as readonly [number, number],
      toPosition: Object.freeze([...entry.latticePosition]) as readonly [number, number],
      exitProvenance: frozenProvenance(exit.provenance),
      entryProvenance: frozenProvenance(entry.provenance),
    });
  });

  const eventOrder = request.transitions.map((transition) =>
    Object.freeze({
      pairId: transition.pairId,
      half: transition.half,
      stepIndex: transition.stepIndex,
    }),
  );

  return Object.freeze({
    traceId: `${request.bridgeId}:trace`,
    bridgeId: request.bridgeId,
    sourceFrameId: request.sourceFrameId,
    authorityStatus: 'derived',
    from: Object.freeze({ ...request.from }),
    to: Object.freeze({ ...request.to }),
    pairOrder: Object.freeze(pairOrder),
    eventOrder: Object.freeze(eventOrder),
    connectivity: Object.freeze(connectivity),
    preservedInvariants: Object.freeze([...request.preservedInvariants]),
    measuredOrDeclaredLoss: Object.freeze([...request.measuredOrDeclaredLoss]),
    falsifiers: Object.freeze([...request.falsifiers]),
    evidenceRefs: Object.freeze(request.evidenceRefs.map(frozenProvenance)),
    origin: Object.freeze({ ...request.origin }),
  });
}

export function buildMicroToMesoTrace(input: unknown): BridgeResult {
  const completenessErrors: string[] = [];
  if (!isRecord(input)) {
    return reject('BRIDGE_INCOMPLETE', ['$: expected a bridge request object']);
  }

  if (!isNonEmptyString(input.bridgeId)) {
    completenessErrors.push('$.bridgeId: expected a non-empty string');
  }
  if (!isNonEmptyString(input.sourceFrameId)) {
    completenessErrors.push('$.sourceFrameId: expected a non-empty string');
  }
  validateScaleAddress(
    input.from,
    '$.from',
    'MICRO',
    'TRAVERSAL_CELL',
    completenessErrors,
  );
  validateScaleAddress(input.to, '$.to', 'MESO', 'TRAVERSAL_SLICE', completenessErrors);
  validateRequiredEnumValues(
    input.preservedInvariants,
    '$.preservedInvariants',
    REQUIRED_PRESERVED_INVARIANTS,
    completenessErrors,
  );
  validateNonEmptyStringArray(
    input.measuredOrDeclaredLoss,
    '$.measuredOrDeclaredLoss',
    completenessErrors,
  );
  validateRequiredEnumValues(
    input.falsifiers,
    '$.falsifiers',
    REQUIRED_FALSIFIERS,
    completenessErrors,
  );
  validateClaimOrigin(input.origin, '$.origin', completenessErrors);

  if (validateDenseArray(input.evidenceRefs, '$.evidenceRefs', completenessErrors)) {
    if (input.evidenceRefs.length === 0) {
      completenessErrors.push('$.evidenceRefs: expected at least one evidence reference');
    }
    input.evidenceRefs.forEach((reference, index) => {
      validateProvenanceRef(reference, `$.evidenceRefs[${index}]`, completenessErrors);
    });
  }

  const transitions: BoundaryTransition[] = [];
  if (validateDenseArray(input.transitions, '$.transitions', completenessErrors)) {
    if (input.transitions.length === 0) {
      completenessErrors.push('$.transitions: expected at least one boundary pair');
    }
    input.transitions.forEach((transition, index) => {
      if (
        validateBoundaryTransitionShape(
          transition,
          `$.transitions[${index}]`,
          completenessErrors,
        )
      ) {
        transitions.push(transition);
      }
    });
  }

  if (completenessErrors.length > 0) {
    return reject('BRIDGE_INCOMPLETE', completenessErrors);
  }

  const falsifierErrors = validateBoundaryPairs(transitions).errors.map(
    (error) => `$.transitions: ${error}`,
  );
  for (let index = 1; index < transitions.length; index += 1) {
    if (transitions[index - 1].stepIndex >= transitions[index].stepIndex) {
      falsifierErrors.push(
        `$.transitions[${index}]: event order must be strictly increasing by stepIndex`,
      );
    }
  }

  if (falsifierErrors.length === 0) {
    const orderedPairs = transitions
      .filter((transition) => transition.half === 'EXIT')
      .map((exit) => ({
        exit,
        entry: transitions.find(
          (transition) => transition.pairId === exit.pairId && transition.half === 'ENTRY',
        ),
      }));

    for (let index = 1; index < orderedPairs.length; index += 1) {
      const previousEntry = orderedPairs[index - 1].entry;
      const currentExit = orderedPairs[index].exit;
      if (!previousEntry) {
        falsifierErrors.push(
          `$.transitions: ${orderedPairs[index - 1].exit.pairId} lost its ENTRY`,
        );
        continue;
      }
      if (previousEntry.stateId !== currentExit.stateId) {
        falsifierErrors.push(
          `$.transitions: pair chain state continuity broke before ${currentExit.pairId}`,
        );
      }
      if (
        previousEntry.latticePosition[0] !== currentExit.latticePosition[0] ||
        previousEntry.latticePosition[1] !== currentExit.latticePosition[1]
      ) {
        falsifierErrors.push(
          `$.transitions: pair chain position continuity broke before ${currentExit.pairId}`,
        );
      }
    }
  }

  if (falsifierErrors.length > 0) {
    return reject('BRIDGE_FALSIFIED', falsifierErrors);
  }

  const request: MicroToMesoBridgeRequest = {
    bridgeId: input.bridgeId as string,
    sourceFrameId: input.sourceFrameId as string,
    from: input.from as unknown as ScaleAddress,
    to: input.to as unknown as ScaleAddress,
    transitions,
    preservedInvariants: input.preservedInvariants as PreservedInvariant[],
    measuredOrDeclaredLoss: input.measuredOrDeclaredLoss as string[],
    falsifiers: input.falsifiers as BridgeFalsifier[],
    evidenceRefs: input.evidenceRefs as ProvenanceRef[],
    origin: input.origin as unknown as ImmutableClaimOrigin,
  };

  return {
    accepted: true,
    decision: 'PASS_CANDIDATE',
    errors: [],
    trace: buildFrozenTrace(request),
  };
}
