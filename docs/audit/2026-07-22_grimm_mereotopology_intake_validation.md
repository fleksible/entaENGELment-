# Grimm-IR Mereotopology Intake Validation

**Date:** 2026-07-22  
**Status:** `[ANNEX]` `[FACT]`  
**Scope:** read-only fixture and documentation validation

## Outcome

PASS for ANNEX intake. Runtime promotion remains HOLD.

The bundle adds no UI surface and therefore makes no claim that an actual Grimm-IR view has rendered successfully on a phone. It establishes the content and accessibility contract that such a surface must satisfy.

## Commands

```text
python tools/validate_grimm_mereotopology_fixtures.py
PASS: 6 Grimm-IR mereotopology fixtures satisfy the intake invariants

python -m unittest discover -s tests/unit -p 'test_grimm_mereotopology_fixtures.py' -v
Ran 7 tests in 0.001s
OK

python -m py_compile tools/validate_grimm_mereotopology_fixtures.py tests/unit/test_grimm_mereotopology_fixtures.py
PASS (exit 0)
```

## Validation matrix

| Gate | Result | Evidence / limit |
|---|---|---|
| six qualitative relations | PASS | exactly one fixture each for `DC`, `EC`, `PO`, `TPP`, `NTPP`, and `EQ` |
| collision semantics | PASS | `PROJECTED`, `OVER`, `UNDER`, and `TOUCH` fixtures are non-colliding; only the explicit equal-State-ID frame witness is true |
| production boundary | PASS | Grimm-IR may reference `transitionPairId` but cannot replace frame validation |
| plain language | PASS | every fixture has a short German reading, guard, and reentry question |
| reader reversibility | PASS | every fixture exposes `ACCEPT`, `REVISE`, `REJECT`, and `SILENCE` |
| colorless reading | PASS at contract level | relation label, line pattern, arrow, and static fallback remain; color is never required for meaning |
| reduced motion | PASS at contract level | motion is never required for meaning; all fixtures specify a static fallback |
| protected provenance | PASS | protected origin has no source pointer and explicitly forbids public reconstruction |
| 320 CSS-pixel content order | PASS at contract level | minimum width and deterministic narrow reading order are validated |
| actual 320 CSS-pixel Grimm rendering | HOLD | no Grimm-IR runtime surface exists in this change; screenshot and interaction inspection are required before runtime promotion |

## Counterexample check

The test suite mutates the projected `DC` fixture to request `collisionProxy: true`. The validator rejects it because screen-space projection is not `EXACT_STATE_ID` evidence.

## Repository boundary

This change is limited to:

- `docs/narratives/grimm2/`;
- a local pointer in `docs/tesser3takt/README.md`;
- a read-only validator under `tools/`;
- unit tests under `tests/unit/`;
- this audit note.

It does not modify `docs/masterindex.md`, `VOIDMAP.yml`, `index/`, `policies/`, `data/receipts/`, UI runtime code, persistence, telemetry, or guard state.

## Promotion condition

Before any runtime promotion, implement the smallest read-only Grimm edge view and inspect it at 320 CSS pixels with color removed and reduced motion enabled. The visual result must preserve relation, endpoints, direction, guard, reentry question, provenance visibility, and all four reader actions.
