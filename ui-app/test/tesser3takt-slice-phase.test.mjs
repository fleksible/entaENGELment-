import assert from 'node:assert/strict';
import test from 'node:test';

import { validateBoundaryPairs } from '../lib/tesser3takt-frame.ts';
import { HUD_BOUNDARY_TRANSITIONS } from '../lib/tesser3takt-hud.ts';
import {
  SLICE_PHASE_TOLERANCE_TURNS,
  validateSlicePhaseTransport,
} from '../lib/tesser3takt-slice-phase.ts';

function fixture(sourcePhase = 0.125, deltaTurns = 0.25) {
  const provenance = {
    kind: 'fixture',
    source: 'repo:ui-app/test/tesser3takt-slice-phase.test.mjs',
    revision: 'fixture:v0.1',
    digest: null,
    digestStatus: 'UNVERIFIED',
    locator: 'synthetic-phase-fixture',
    claimLayer: 'FIXTURE',
    authorityStatus: 'derived',
  };
  const reference = { basisId: 'fixture:phase-basis', unit: 'turns', provenance };
  const targetPhase = ((sourcePhase + deltaTurns) % 1 + 1) % 1;
  return {
    receipt: {
      ...reference,
      sliceId: 'fixture:slice-1',
      sourceFrameId: 'fixture:frame-a',
      targetFrameId: 'fixture:frame-b',
      phaseBefore: sourcePhase,
      phaseAfter: targetPhase,
      handedness: 'LEFT',
      transformId: 'fixture:offset',
    },
    source: {
      ...reference, frameId: 'fixture:frame-a', sliceId: 'fixture:slice-1', phase: sourcePhase, handedness: 'LEFT',
    },
    target: {
      ...reference, frameId: 'fixture:frame-b', sliceId: 'fixture:slice-1', phase: targetPhase, handedness: 'LEFT',
    },
    transform: { ...reference, transformId: 'fixture:offset', deltaTurns },
  };
}

function validate(f) {
  return validateSlicePhaseTransport(f.receipt, f.source, f.target, f.transform);
}

test('declared receipt matches independently supplied snapshots and transform after JSON roundtrip', () => {
  const f = JSON.parse(JSON.stringify(fixture()));
  assert.deepEqual(validate(f), { valid: true, errors: [], receipt: f.receipt });
  assert.equal(f.receipt.provenance.digestStatus, 'UNVERIFIED');
});

test('positive and negative offsets wrap at the phase boundary', () => {
  for (const [source, delta, expected] of [[0.875, 0.25, 0.125], [0.125, -0.25, 0.875]]) {
    const f = fixture(source, delta);
    assert.equal(f.target.phase, expected);
    assert.equal(validate(f).valid, true);
  }
});

test('right orientation and identity are supported without deriving a handedness change', () => {
  const f = fixture(0.25, 0);
  for (const value of [f.receipt, f.source, f.target]) value.handedness = 'RIGHT';
  assert.equal(validate(f).valid, true);
});

test('declared numerical tolerance applies across zero but rejects larger drift', () => {
  const epsilon = SLICE_PHASE_TOLERANCE_TURNS;
  for (const phase of [epsilon / 2, 1 - epsilon / 2]) {
    const f = fixture(0.875, 0.125);
    f.target.phase = f.receipt.phaseAfter = phase;
    assert.equal(validate(f).valid, true);
  }
  const drift = fixture(0.875, 0.125);
  drift.target.phase = drift.receipt.phaseAfter = epsilon * 2;
  assert.equal(validate(drift).valid, false);
});

const inconsistencies = [
  ['source frame mismatch', f => { f.receipt.sourceFrameId = 'other'; }, /sourceFrameId/],
  ['target frame mismatch', f => { f.receipt.targetFrameId = 'other'; }, /targetFrameId/],
  ['retagged receipt slice', f => { f.receipt.sliceId = 'other'; }, /sliceId: must match both/],
  ['source slice mismatch', f => { f.source.sliceId = 'other'; }, /sliceId: must match both/],
  ['target slice mismatch', f => { f.target.sliceId = 'other'; }, /sliceId: must match both/],
  ['self transition', f => { f.target.frameId = f.source.frameId; f.receipt.targetFrameId = f.source.frameId; }, /must differ/],
  ['source basis mismatch', f => { f.source.basisId = 'other'; }, /same declared basis/],
  ['target basis mismatch', f => { f.target.basisId = 'other'; }, /same declared basis/],
  ['transform basis mismatch', f => { f.transform.basisId = 'other'; }, /same declared basis/],
  ['unknown transform id', f => { f.receipt.transformId = 'other'; }, /transformId/],
  ['source phase mismatch', f => { f.receipt.phaseBefore = 0.5; }, /phaseBefore/],
  ['target phase mismatch', f => { f.receipt.phaseAfter = 0.5; }, /phaseAfter/],
  ['self-consistent receipt with wrong target', f => { f.receipt.phaseAfter = f.target.phase = 0.5; }, /declared phase transform/],
  ['wrong declared offset', f => { f.transform.deltaTurns = 0.5; }, /declared phase transform/],
  ['orientation flip', f => { f.target.handedness = 'RIGHT'; }, /orientation must be preserved/],
  ['undefined orientation convention', f => { f.receipt.handedness = 'CLOCKWISE'; }, /expected LEFT or RIGHT/],
  ['wrong unit', f => { f.source.unit = 'radians'; }, /unit: expected turns/],
  ['missing basis', f => { delete f.receipt.basisId; }, /basisId/],
  ['blank slice identity', f => { f.receipt.sliceId = ' '; }, /sliceId/],
  ['missing phase', f => { delete f.receipt.phaseBefore; }, /phaseBefore/],
  ['non-finite source phase', f => { f.source.phase = NaN; }, /source.phase/],
  ['non-finite target phase', f => { f.target.phase = Infinity; }, /target.phase/],
  ['non-normalized receipt phase', f => { f.receipt.phaseAfter = 1; }, /phaseAfter/],
  ['negative phase', f => { f.receipt.phaseBefore = -0.1; }, /phaseBefore/],
  ['unbounded transform', f => { f.transform.deltaTurns = 2; }, /deltaTurns/],
  ['non-finite transform', f => { f.transform.deltaTurns = Infinity; }, /deltaTurns/],
  ['missing provenance', f => { delete f.target.provenance; }, /target.provenance/],
  ['contradictory digest status', f => { f.receipt.provenance = { ...f.receipt.provenance, digestStatus: 'VERIFIED' }; }, /VERIFIED provenance requires/],
];

for (const [name, mutate, pattern] of inconsistencies) {
  test(`phase transport rejects ${name}`, () => {
    const f = fixture();
    mutate(f);
    const result = validate(f);
    assert.equal(result.valid, false);
    assert.equal(result.receipt, undefined);
    assert.match(result.errors.join('\n'), pattern);
  });
}

test('incomplete non-object inputs return errors without throwing', () => {
  for (const bad of [undefined, null, [], 0, 'phase']) {
    const f = fixture();
    for (const field of ['receipt', 'source', 'target', 'transform']) {
      const result = validate({ ...f, [field]: bad });
      assert.equal(result.valid, false);
      assert.equal(result.receipt, undefined);
    }
  }
});

test('a valid boundary pair alone does not pass the separate slice-phase contract', () => {
  const pair = HUD_BOUNDARY_TRANSITIONS.filter(x => x.pairId === 'B-Q0-Q1');
  assert.equal(validateBoundaryPairs(pair).valid, true);
  assert.equal(validateSlicePhaseTransport(pair, undefined, undefined, undefined).valid, false);
});

test('phase values modulo one do not distinguish identity from a complete turn', () => {
  const identity = fixture(0.25, 0);
  const fullTurn = fixture(0.25, 1);
  assert.equal(validate(identity).valid, true);
  assert.equal(validate(fullTurn).valid, true);
  assert.equal(identity.target.phase, fullTurn.target.phase);
  assert.notEqual(identity.transform.deltaTurns, fullTurn.transform.deltaTurns);
});
