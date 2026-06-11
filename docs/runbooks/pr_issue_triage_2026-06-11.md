# PR / Issue Triage — 2026-06-11

Feature: pr-issue-integration | Sync-Date: 2026-06-11 (07:41 UTC)

## Scope

- Reviewed open dependency PRs #233–#239 against the DeepJump verifier boundary.
- Reviewed open issues #226 and #240 as re-entry / governance signals.

## Decision

### Accepted into this integration branch

- #233: `next` 16.2.6 → 16.2.7.
- #234: `@types/react` → 19.2.17.
- #235: `actions/checkout` v6 line refresh, preserving existing verifier posture.
- #236: `codecov/codecov-action` digest refresh.
- #237: `@types/node` → 25.9.2.
- #238: `@tanstack/react-query` → 5.101.0.
- #239: `eslint-config-next` 16.2.6 → 16.2.7.

### Explicitly not accepted from the raw PR diffs

Several Dependabot branches were based before the `actions/setup-node@v6` merge and therefore carried a stale `ci-js-workspace.yml` hunk that would downgrade `actions/setup-node@v6` to `actions/setup-node@v4`. That hunk was rejected because it weakens the current verifier/runtime boundary instead of advancing it.

## Issue follow-up

### #226 — Re-entry notes

The previously named blockers are no longer active in the same form: #214 and #225 are closed upstream. The remaining useful action is this small, explicit integration pass rather than a broad speculative docs expansion.

### #240 — Overdue VOID-010 / VOID-011

The overdue marker is valid. The correct merge-compatible action is not to close either VOID prematurely:

- VOID-010 remains an empirical-source boundary and is re-baselined to a sources-first CSV/schema evidence step.
- VOID-011 has code/test evidence, but remains open until the deterministic metrics export/receipt carries the `SIMULATION_PROXY` boundary explicitly.

## Verifier expectation

Run the repository verifier (`make verify`) plus JS workspace lock/type/lint checks after lockfile refresh. Any failure should be treated as a boundary signal, not guessed around.
