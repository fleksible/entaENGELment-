# Grimm-IR Mereotopology Intake Validation

**Original date:** 2026-07-22  
**Validation refresh:** 2026-07-26  
**Status:** `[ANNEX]` `[FACT]`  
**Scope:** read-only fixture and documentation validation  
**Input snapshot:** PR #319 head `23b72e8`, reconciled with `main@586fc7a`

## Outcome

The hardened ANNEX intake candidate passes the targeted local validator, negative mutation suite, bytecode compilation, Ruff, and Black checks listed below.

PR merge and runtime promotion remain HOLD until the candidate is committed, GitHub CI completes on that exact remote head, and a human confirms the content-level protected-origin boundary. No Grimm-IR runtime surface exists in this change, so no phone rendering or interaction claim is made.

## Commands

```text
python tools/validate_grimm_mereotopology_fixtures.py
PASS: 6 Grimm-IR mereotopology fixtures satisfy the intake invariants

python -m unittest discover -s tests/unit -p 'test_grimm_mereotopology_fixtures.py' -v
Ran 23 tests in 0.026s
OK

python -m py_compile tools/validate_grimm_mereotopology_fixtures.py tests/unit/test_grimm_mereotopology_fixtures.py
PASS (exit 0)

ruff check tools/validate_grimm_mereotopology_fixtures.py tests/unit/test_grimm_mereotopology_fixtures.py
All checks passed!

black --check tools/validate_grimm_mereotopology_fixtures.py tests/unit/test_grimm_mereotopology_fixtures.py
2 files would be left unchanged.

mypy tools/validate_grimm_mereotopology_fixtures.py
Success: no issues found in 1 source file

make verify
475 passed, 104 warnings, 165 subtests passed
Core verify membrane passed

make verify-governance
14 workflow(s) meet the posture contract
22 VOIDs in sync between VOIDMAP.yml and UI mirror
Governance membrane checked
```

`make verify-js` was attempted with a frozen lockfile and a writable temporary pnpm/XDG store. Installation stopped at pnpm's `ERR_PNPM_IGNORED_BUILDS` for `electron-winstaller@5.4.0` and `unrs-resolver@1.12.2`. The same failure reproduces on an unmodified detached `main@586fc7a` worktree, so it is recorded as a pre-existing JS-workspace/environment HOLD rather than a PASS or a regression caused by this Python/docs patch. GitHub workflow results on the committed head remain the remote integration receipt.

## Validation matrix

| Gate | Result | Evidence / limit |
|---|---|---|
| authority metadata | PASS locally | bundle must remain exactly `[ANNEX]` and `[SPEC-WIP]` |
| six qualitative relations | PASS locally | exactly one fixture each for `DC`, `EC`, `PO`, `TPP`, `NTPP`, and `EQ` |
| JSON input totality | PASS locally | scalar roots, malformed nested values, arrays, objects, and unhashable-shaped JSON members return errors without traceback |
| duplicate JSON names | PASS locally | duplicate member names are rejected during loading rather than accepted with last-key-wins behavior |
| closed versioned shapes | PASS locally | unknown bundle, fixture, provenance, visual, reader, and frame fields are rejected |
| collision semantics | PASS locally | non-exact crossings reject frame-owned witness fields; only the canonical equal-State-ID witness is colliding |
| transition reference boundary | PASS locally | a non-exact edge may retain `transitionPairId`, but cannot introduce frame witness semantics |
| provenance vocabulary | PASS locally | authority and visibility values use closed enums; pointer and reconstruction flag types are checked |
| protected-origin structural protocol | PASS locally | protected origin requires `sourcePointer: null`, `publicReconstructionAllowed: false`, and no undeclared disclosure field |
| protected-origin content privacy | HOLD | structural validation cannot establish semantic anonymity or resistance to re-identification; human review required |
| reader reversibility | PASS locally | every fixture exposes `ACCEPT`, `REVISE`, `REJECT`, and `SILENCE` |
| colorless and reduced-motion contract | PASS locally | labels, line patterns, arrows, and static fallbacks remain; color and motion are not required |
| actual 320 CSS-pixel Grimm rendering | HOLD | no Grimm-IR runtime surface exists; screenshot and interaction inspection are required before runtime promotion |

## Negative mutation coverage

The suite now checks:

- every JSON scalar and array root class;
- malformed `invariants`, fixture, provenance, visual, reader, and frame objects;
- null, scalar, object, unhashable-shaped, duplicate, incomplete, and invented set members;
- invalid relation, crossing, direction, authority, and visibility values;
- populated protected pointers, invalid reconstruction flags, and sibling shadow fields;
- each forbidden non-exact frame witness field independently;
- non-string, blank, padded, and unequal exact State IDs;
- duplicate JSON keys at the root and nested levels;
- attempted ANNEX/SPEC-WIP authority relabelling.

The positive counterexample also preserves an optional non-exact `transitionPairId`, preventing the hardening from silently narrowing the documented frame-reference boundary.

## Repository boundary

This change remains limited to:

- `docs/narratives/grimm2/`;
- the additive local pointer in `docs/tesser3takt/README.md`, reconciled with the newer Micro→Meso section on `main`;
- the read-only validator under `tools/`;
- unit tests under `tests/unit/`;
- this audit note.

It does not modify `docs/masterindex.md`, `VOIDMAP.yml`, `index/`, `policies/`, `data/receipts/`, UI runtime code, persistence, telemetry, or guard state.

## Promotion condition

Before any runtime promotion, implement the smallest read-only Grimm edge view and inspect it at 320 CSS pixels with color removed and reduced motion enabled. The visual result must preserve relation, endpoints, direction, guard, reentry question, provenance visibility, and all four reader actions.
