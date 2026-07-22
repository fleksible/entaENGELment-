import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

import {
  isSlaterCollision,
  validateBoundaryPairs,
  validateTesserTickFrame,
  withDerivedCollisionProxy,
} from '../lib/tesser3takt-frame.ts';

const fixture = JSON.parse(
  readFileSync(new URL('../fixtures/tesser3takt-minimal-frame.json', import.meta.url), 'utf8'),
);

const exit = fixture.boundaryTransitions[0];
const entry = fixture.boundaryTransitions[1];

test('collision proxy uses exact state-id equality in production code', () => {
  assert.equal(isSlaterCollision('S4:1234', 'S4:1234'), true);
  assert.equal(isSlaterCollision('S4:1234', 'S4:2143'), false);

  const frame = withDerivedCollisionProxy({
    ...fixture,
    leftStateId: 'S4:1234',
    rightStateId: 'S4:2143',
  });
  assert.equal(frame.collisionProxy, false);
});

test('valid boundary pair uses one global coordinate space and a knight move', () => {
  assert.deepEqual(validateBoundaryPairs([exit, entry]), { valid: true, errors: [] });
});

test('the serialized fixture passes full runtime validation', () => {
  const result = validateTesserTickFrame(fixture);
  assert.equal(result.valid, true);
  assert.deepEqual(result.errors, []);
  assert.equal(result.frame, fixture);
});

test('boundary validation rejects orphan, duplicate, id mismatch, coordinate mismatch, and non-knight transforms', () => {
  assert.match(
    validateBoundaryPairs([exit]).errors.join('\n'),
    /expected exactly one EXIT and one ENTRY/,
  );
  assert.match(
    validateBoundaryPairs([exit, { ...exit }]).errors.join('\n'),
    /duplicate EXIT/,
  );
  assert.match(
    validateBoundaryPairs([
      { ...exit, stepIndex: 4 },
      { ...entry, stepIndex: 3 },
    ]).errors.join('\\n'),
    /EXIT must precede ENTRY/,
  );
  assert.match(
    validateBoundaryPairs([exit, { ...entry, transformedFrom: 'S4:9999' }]).errors.join('\n'),
    /transformedFrom must match/,
  );
  assert.match(
    validateBoundaryPairs([
      exit,
      { ...entry, coordinateSpace: 'OTHER_LOCAL_SPACE' },
    ]).errors.join('\n'),
    /same coordinate space/,
  );
  assert.match(
    validateBoundaryPairs([
      { ...exit, coordinateSpace: 'OTHER_LOCAL_SPACE' },
      { ...entry, coordinateSpace: 'OTHER_LOCAL_SPACE' },
    ]).errors.join('\n'),
    /must use GLOBAL_REENTRY_LATTICE/,
  );
  assert.match(
    validateBoundaryPairs([exit, { ...entry, latticePosition: [2, 2] }]).errors.join('\n'),
    /not knight-legal in the global lattice/,
  );
});

test('unverified provenance uses null digest rather than a hash-looking placeholder', () => {
  for (const transition of fixture.boundaryTransitions) {
    assert.equal(transition.provenance.digest, null);
    assert.equal(transition.provenance.digestStatus, 'UNVERIFIED');
  }
  for (const provenance of fixture.provenance) {
    assert.equal(provenance.digest, null);
    assert.equal(provenance.digestStatus, 'UNVERIFIED');
  }
});

test('runtime validation rejects a supplied collision value that contradicts state ids', () => {
  const result = validateTesserTickFrame({
    ...fixture,
    rightStateId: 'S4:2143',
    collisionProxy: true,
  });
  assert.equal(result.valid, false);
  assert.match(result.errors.join('\n'), /does not match the derived collision state/);
});

test('runtime validation enforces digest and digest-status consistency', () => {
  const verifiedWithoutDigest = {
    ...fixture.provenance[0],
    digestStatus: 'VERIFIED',
    digest: null,
  };
  const unverifiedWithDigest = {
    ...fixture.provenance[0],
    digestStatus: 'UNVERIFIED',
    digest: 'sha256:not-a-witness',
  };

  assert.match(
    validateTesserTickFrame({ ...fixture, provenance: [verifiedWithoutDigest] }).errors.join(
      '\n',
    ),
    /VERIFIED provenance requires a non-empty digest/,
  );
  assert.match(
    validateTesserTickFrame({ ...fixture, provenance: [unverifiedWithDigest] }).errors.join(
      '\n',
    ),
    /UNVERIFIED provenance requires digest: null/,
  );
});

test('runtime validation rejects malformed JSON without throwing', () => {
  const result = validateTesserTickFrame({
    ...fixture,
    boundaryTransitions: [
      {
        ...exit,
        stepIndex: '2',
        latticePosition: [1],
        coordinateSpace: 'OTHER_LOCAL_SPACE',
      },
      entry,
    ],
  });

  assert.equal(result.valid, false);
  assert.match(result.errors.join('\n'), /stepIndex/);
  assert.match(result.errors.join('\n'), /latticePosition/);
  assert.match(result.errors.join('\n'), /GLOBAL_REENTRY_LATTICE/);
});

test('runtime validation rejects sparse boundary transition arrays', () => {
  const sparseTransitions = [exit];
  sparseTransitions.length = 3;
  sparseTransitions[2] = entry;

  const result = validateTesserTickFrame({
    ...fixture,
    boundaryTransitions: sparseTransitions,
  });

  assert.equal(result.valid, false);
  assert.match(
    result.errors.join('\n'),
    /\$\.boundaryTransitions\[1\]: expected a boundary transition object/,
  );
});
