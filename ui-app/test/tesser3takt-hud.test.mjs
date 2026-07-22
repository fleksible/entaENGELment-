import assert from 'node:assert/strict';
import test from 'node:test';

import {
  buildTesserHudFrame,
  HUD_BOUNDARY_TRANSITIONS,
  KENO_FRINGES,
  PORTAL_DISTINCT_RIGHT_STATE_ID,
  PORTAL_LEFT_STATE_ID,
} from '../lib/tesser3takt-hud.ts';
import {
  validateBoundaryPairs,
  validateTesserTickFrame,
} from '../lib/tesser3takt-frame.ts';

function buildFrame(overrides = {}) {
  return buildTesserHudFrame({
    observerMode: 'OUTER',
    control: -0.34,
    torsion: 0.48,
    zLayer: 4,
    leftStateId: PORTAL_LEFT_STATE_ID,
    rightStateId: PORTAL_DISTINCT_RIGHT_STATE_ID,
    ...overrides,
  });
}

test('portal determinant is derived from exact canonical state ids', () => {
  const distinct = buildFrame();
  assert.equal(distinct.transport.collisionProxy, false);
  assert.equal(distinct.portal.determinantProxy, 1);

  const collision = buildFrame({ rightStateId: PORTAL_LEFT_STATE_ID });
  assert.equal(collision.transport.collisionProxy, true);
  assert.equal(collision.portal.determinantProxy, 0);

  for (const frame of [distinct, collision]) {
    assert.deepEqual(validateTesserTickFrame(frame.transport), {
      valid: true,
      errors: [],
      frame: frame.transport,
    });
  }
});

test('HUD boundary markers are canonical paired transitions', () => {
  assert.equal(HUD_BOUNDARY_TRANSITIONS.length, 6);
  assert.equal(
    new Set(HUD_BOUNDARY_TRANSITIONS.map((transition) => transition.pairId)).size,
    3,
  );
  assert.deepEqual(validateBoundaryPairs(HUD_BOUNDARY_TRANSITIONS), {
    valid: true,
    errors: [],
  });

  for (const pairId of new Set(
    HUD_BOUNDARY_TRANSITIONS.map((transition) => transition.pairId),
  )) {
    const pair = HUD_BOUNDARY_TRANSITIONS.filter(
      (transition) => transition.pairId === pairId,
    );
    assert.deepEqual(
      pair.map((transition) => transition.half).sort(),
      ['ENTRY', 'EXIT'],
    );
  }
});

test('display regime cannot produce a governance guard transition', () => {
  const loosened = buildFrame({ control: 1, torsion: 0 });
  const overwound = buildFrame({ control: -1, torsion: 1 });
  assert.equal(loosened.guardState, 'PASS');
  assert.equal(overwound.guardState, 'PASS');
  assert.notEqual(loosened.regime.state, overwound.regime.state);

  const held = buildFrame({
    control: 1,
    torsion: 0,
    guardInputs: { claimPromotionRequested: true },
  });
  assert.equal(held.guardState, 'HOLD');
});

test('fringe and transport provenance remain structured and explicitly unverified', () => {
  const references = [
    ...KENO_FRINGES.flatMap((fringe) => fringe.provenance),
    ...buildFrame().transport.provenance,
    ...HUD_BOUNDARY_TRANSITIONS.map((transition) => transition.provenance),
  ];

  assert.ok(references.length > 0);
  for (const reference of references) {
    assert.equal(typeof reference, 'object');
    assert.equal(reference.digestStatus, 'UNVERIFIED');
    assert.equal(reference.digest, null);
    assert.ok(reference.source.length > 0);
    assert.ok(reference.locator.length > 0);
  }
});
