import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

import { buildMicroToMesoTrace } from '../lib/tesser3takt-bridge.ts';

const fixture = JSON.parse(
  readFileSync(
    new URL('../fixtures/tesser3takt-micro-meso-bridge-v0.1.json', import.meta.url),
    'utf8',
  ),
);

function request(overrides = {}) {
  return structuredClone({ ...fixture, ...overrides });
}

test('positive synthetic bridge emits a derived meso trace without claim promotion', () => {
  const result = buildMicroToMesoTrace(fixture);

  assert.equal(result.accepted, true);
  assert.equal(result.decision, 'PASS_CANDIDATE');
  assert.deepEqual(result.errors, []);
  assert.equal(result.trace.authorityStatus, 'derived');
  assert.equal(result.trace.sourceFrameId, 'tesser3takt-micro-slice-v0.1');
  assert.equal(result.trace.from.resolutionScale, 'MICRO');
  assert.equal(result.trace.to.resolutionScale, 'MESO');
  assert.deepEqual(result.trace.pairOrder, ['bt-001', 'bt-002']);
  assert.deepEqual(result.trace.eventOrder, [
    { pairId: 'bt-001', half: 'EXIT', stepIndex: 2 },
    { pairId: 'bt-001', half: 'ENTRY', stepIndex: 3 },
    { pairId: 'bt-002', half: 'EXIT', stepIndex: 4 },
    { pairId: 'bt-002', half: 'ENTRY', stepIndex: 5 },
  ]);
  assert.deepEqual(result.trace.connectivity[0], {
    pairId: 'bt-001',
    fromStateId: 'S4:1234',
    toStateId: 'S4:2143',
    fromPosition: [1, 1],
    toPosition: [2, 3],
    exitProvenance: fixture.transitions[0].provenance,
    entryProvenance: fixture.transitions[1].provenance,
  });
  assert.deepEqual(result.trace.connectivity[1], {
    pairId: 'bt-002',
    fromStateId: 'S4:2143',
    toStateId: 'S4:2413',
    fromPosition: [2, 3],
    toPosition: [4, 4],
    exitProvenance: fixture.transitions[2].provenance,
    entryProvenance: fixture.transitions[3].provenance,
  });
  assert.deepEqual(result.trace.origin, fixture.origin);
});

test('bridge metadata below the minimum is rejected as BRIDGE_INCOMPLETE', () => {
  const cases = [
    request({ bridgeId: '' }),
    request({ sourceFrameId: '' }),
    request({ preservedInvariants: [] }),
    request({ measuredOrDeclaredLoss: [] }),
    request({ falsifiers: [] }),
    request({ evidenceRefs: [] }),
    request({ origin: { ...fixture.origin, immutable: false } }),
    request({ from: { ...fixture.from, extentScope: 'TRAVERSAL_SLICE' } }),
  ];

  for (const candidate of cases) {
    const result = buildMicroToMesoTrace(candidate);
    assert.equal(result.accepted, false);
    assert.equal(result.decision, 'REJECT');
    assert.equal(result.code, 'BRIDGE_INCOMPLETE');
    assert.ok(result.errors.length > 0);
  }
});

test('every required preserved invariant and falsifier is mechanically required', () => {
  for (const invariant of fixture.preservedInvariants) {
    const result = buildMicroToMesoTrace(
      request({
        preservedInvariants: fixture.preservedInvariants.filter(
          (candidate) => candidate !== invariant,
        ),
      }),
    );
    assert.equal(result.accepted, false);
    assert.equal(result.code, 'BRIDGE_INCOMPLETE');
    assert.match(result.errors.join('\n'), new RegExp(invariant));
  }

  for (const falsifier of fixture.falsifiers) {
    const result = buildMicroToMesoTrace(
      request({
        falsifiers: fixture.falsifiers.filter((candidate) => candidate !== falsifier),
      }),
    );
    assert.equal(result.accepted, false);
    assert.equal(result.code, 'BRIDGE_INCOMPLETE');
    assert.match(result.errors.join('\n'), new RegExp(falsifier));
  }
});

test('missing or reordered boundary halves falsify the bridge', () => {
  const orphan = buildMicroToMesoTrace(request({ transitions: [fixture.transitions[0]] }));
  assert.equal(orphan.accepted, false);
  assert.equal(orphan.code, 'BRIDGE_FALSIFIED');
  assert.match(orphan.errors.join('\n'), /exactly one EXIT and one ENTRY/);

  const reordered = buildMicroToMesoTrace(
    request({ transitions: [fixture.transitions[1], fixture.transitions[0]] }),
  );
  assert.equal(reordered.accepted, false);
  assert.equal(reordered.code, 'BRIDGE_FALSIFIED');
  assert.match(reordered.errors.join('\n'), /strictly increasing by stepIndex/);
});

test('changed connectivity falsifies the bridge', () => {
  const changedEntry = {
    ...fixture.transitions[1],
    transformedFrom: 'S4:9999',
  };
  const result = buildMicroToMesoTrace(
    request({ transitions: [fixture.transitions[0], changedEntry] }),
  );

  assert.equal(result.accepted, false);
  assert.equal(result.code, 'BRIDGE_FALSIFIED');
  assert.match(result.errors.join('\n'), /transformedFrom must match EXIT stateId/);
});

test('a locally valid pair cannot silently break the traversal chain', () => {
  const disconnectedExit = {
    ...fixture.transitions[2],
    stateId: 'S4:9999',
  };
  const internallyReboundEntry = {
    ...fixture.transitions[3],
    transformedFrom: 'S4:9999',
  };
  const result = buildMicroToMesoTrace(
    request({
      transitions: [
        fixture.transitions[0],
        fixture.transitions[1],
        disconnectedExit,
        internallyReboundEntry,
      ],
    }),
  );

  assert.equal(result.accepted, false);
  assert.equal(result.code, 'BRIDGE_FALSIFIED');
  assert.match(result.errors.join('\n'), /pair chain state continuity broke/);
});

test('complete pairs cannot interleave and masquerade as a sequential traversal', () => {
  const interleaved = [
    { ...fixture.transitions[0], stepIndex: 2 },
    { ...fixture.transitions[2], stepIndex: 3 },
    { ...fixture.transitions[1], stepIndex: 4 },
    { ...fixture.transitions[3], stepIndex: 5 },
  ];
  const result = buildMicroToMesoTrace(request({ transitions: interleaved }));

  assert.equal(result.accepted, false);
  assert.equal(result.code, 'BRIDGE_FALSIFIED');
  assert.match(result.errors.join('\n'), /pair chain event order broke/);
});

test('lost transition provenance rejects the bridge before aggregation', () => {
  const entryWithoutProvenance = { ...fixture.transitions[1] };
  delete entryWithoutProvenance.provenance;

  const result = buildMicroToMesoTrace(
    request({ transitions: [fixture.transitions[0], entryWithoutProvenance] }),
  );

  assert.equal(result.accepted, false);
  assert.equal(result.code, 'BRIDGE_INCOMPLETE');
  assert.match(result.errors.join('\n'), /provenance/);
});

test('claim origin is copied, frozen, and cannot be laundered by the bridge', () => {
  const metaphorOrigin = {
    claimTag: 'METAPHER',
    evidenceRole: 'PROVENANCE_ONLY',
    immutable: true,
  };
  const result = buildMicroToMesoTrace(request({ origin: metaphorOrigin }));

  assert.equal(result.accepted, true);
  assert.deepEqual(result.trace.origin, metaphorOrigin);
  assert.equal(Object.isFrozen(result.trace), true);
  assert.equal(Object.isFrozen(result.trace.origin), true);
  assert.equal(Object.isFrozen(result.trace.connectivity), true);
  assert.equal(Object.isFrozen(result.trace.connectivity[0].exitProvenance), true);
  assert.throws(() => {
    result.trace.origin.claimTag = 'CANON';
  }, TypeError);
  assert.equal(result.trace.origin.claimTag, 'METAPHER');
});

test('malformed and sparse transport inputs fail closed without throwing', () => {
  assert.deepEqual(buildMicroToMesoTrace(null), {
    accepted: false,
    decision: 'REJECT',
    code: 'BRIDGE_INCOMPLETE',
    errors: ['$: expected a bridge request object'],
  });

  const sparse = [fixture.transitions[0]];
  sparse.length = 3;
  sparse[2] = fixture.transitions[1];
  const result = buildMicroToMesoTrace(request({ transitions: sparse }));

  assert.equal(result.accepted, false);
  assert.equal(result.code, 'BRIDGE_INCOMPLETE');
  assert.match(result.errors.join('\n'), /sparse array entries are not allowed/);

  const sparsePosition = [1];
  sparsePosition.length = 2;
  const sparseCoordinate = buildMicroToMesoTrace(
    request({
      transitions: [
        { ...fixture.transitions[0], latticePosition: sparsePosition },
        ...fixture.transitions.slice(1),
      ],
    }),
  );
  assert.equal(sparseCoordinate.accepted, false);
  assert.equal(sparseCoordinate.code, 'BRIDGE_INCOMPLETE');
  assert.match(sparseCoordinate.errors.join('\n'), /two integer global coordinates/);
});
