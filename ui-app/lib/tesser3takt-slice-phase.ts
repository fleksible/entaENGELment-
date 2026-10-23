import {
  validateProvenanceRef,
  type ProvenanceRef,
} from './tesser3takt-frame.ts';

export type SliceHandedness = 'LEFT' | 'RIGHT';

interface PhaseReference {
  basisId: string;
  unit: 'turns';
  provenance: ProvenanceRef;
}

export interface SlicePhaseSnapshot extends PhaseReference {
  frameId: string;
  phase: number;
  handedness: SliceHandedness;
}

export interface SlicePhaseTransportReceipt extends PhaseReference {
  sliceId: string;
  sourceFrameId: string;
  targetFrameId: string;
  phaseBefore: number;
  phaseAfter: number;
  handedness: SliceHandedness;
  transformId: string;
}

export interface DeclaredPhaseTransform extends PhaseReference {
  transformId: string;
  deltaTurns: number;
}

export interface SlicePhaseTransportValidationResult {
  valid: boolean;
  errors: string[];
  receipt?: SlicePhaseTransportReceipt;
}

export const SLICE_PHASE_TOLERANCE_TURNS = 1e-10;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function validateString(
  record: Record<string, unknown>,
  field: string,
  path: string,
  errors: string[],
): void {
  if (typeof record[field] !== 'string' || record[field].trim().length === 0) {
    errors.push(`${path}.${field}: expected a non-empty string`);
  }
}

function validatePhase(
  record: Record<string, unknown>,
  field: string,
  path: string,
  errors: string[],
): void {
  const value = record[field];
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value >= 1) {
    errors.push(`${path}.${field}: expected a finite phase in [0, 1) turns`);
  }
}

function validateReference(
  value: unknown,
  path: string,
  stringFields: readonly string[],
  phaseFields: readonly string[],
  hasHandedness: boolean,
  errors: string[],
): void {
  if (!isRecord(value)) {
    errors.push(`${path}: expected an object`);
    return;
  }
  for (const field of ['basisId', ...stringFields]) {
    validateString(value, field, path, errors);
  }
  if (value.unit !== 'turns') {
    errors.push(`${path}.unit: expected turns`);
  }
  for (const field of phaseFields) {
    validatePhase(value, field, path, errors);
  }
  if (hasHandedness && value.handedness !== 'LEFT' && value.handedness !== 'RIGHT') {
    errors.push(`${path}.handedness: expected LEFT or RIGHT`);
  }
  validateProvenanceRef(value.provenance, `${path}.provenance`, errors);
}

function phasesMatch(left: number, right: number): boolean {
  const distance = Math.abs(left - right);
  return Math.min(distance, 1 - distance) <= SLICE_PHASE_TOLERANCE_TURNS;
}

// Contract: docs/annex/SLICE_PHASE_TRANSPORT_v0_1.md.
// Snapshots and the approved transform must come from the caller, not the receipt.
export function validateSlicePhaseTransport(
  receiptInput: unknown,
  sourceInput: unknown,
  targetInput: unknown,
  transformInput: unknown,
): SlicePhaseTransportValidationResult {
  const errors: string[] = [];
  validateReference(
    receiptInput,
    'receipt',
    ['sliceId', 'sourceFrameId', 'targetFrameId', 'transformId'],
    ['phaseBefore', 'phaseAfter'],
    true,
    errors,
  );
  validateReference(sourceInput, 'source', ['frameId'], ['phase'], true, errors);
  validateReference(targetInput, 'target', ['frameId'], ['phase'], true, errors);
  validateReference(transformInput, 'transform', ['transformId'], [], false, errors);
  if (isRecord(transformInput)) {
    const delta = transformInput.deltaTurns;
    if (typeof delta !== 'number' || !Number.isFinite(delta) || Math.abs(delta) > 1) {
      errors.push('transform.deltaTurns: expected a finite offset in [-1, 1] turns');
    }
  }
  if (errors.length > 0) return { valid: false, errors };

  const receipt = receiptInput as SlicePhaseTransportReceipt;
  const source = sourceInput as SlicePhaseSnapshot;
  const target = targetInput as SlicePhaseSnapshot;
  const transform = transformInput as DeclaredPhaseTransform;

  if (receipt.sourceFrameId !== source.frameId) {
    errors.push('receipt.sourceFrameId: does not match source snapshot');
  }
  if (receipt.targetFrameId !== target.frameId) {
    errors.push('receipt.targetFrameId: does not match target snapshot');
  }
  if (source.frameId === target.frameId) {
    errors.push('receipt: source and target frame ids must differ');
  }
  if ([source.basisId, target.basisId, transform.basisId].some(x => x !== receipt.basisId)) {
    errors.push('receipt.basisId: all inputs must use the same declared basis');
  }
  if (source.handedness !== receipt.handedness || target.handedness !== receipt.handedness) {
    errors.push('receipt.handedness: source and target orientation must be preserved');
  }
  if (receipt.transformId !== transform.transformId) {
    errors.push('receipt.transformId: does not match declared transform');
  }
  if (!phasesMatch(receipt.phaseBefore, source.phase)) {
    errors.push('receipt.phaseBefore: does not match source snapshot');
  }
  if (!phasesMatch(receipt.phaseAfter, target.phase)) {
    errors.push('receipt.phaseAfter: does not match target snapshot');
  }
  const expected = ((source.phase + transform.deltaTurns) % 1 + 1) % 1;
  if (!phasesMatch(expected, target.phase)) {
    errors.push('target.phase: does not match declared phase transform');
  }

  return errors.length === 0
    ? { valid: true, errors, receipt }
    : { valid: false, errors };
}
