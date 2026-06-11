# PR / Issue Triage — 2026-06-11

Feature: review-open-prs-and-issues-for-merge | Sync-Date: 2026-06-11 (16:08 UTC)

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

## Post-merge closure protocol

After this integration PR is merged, do **not** merge the original Dependabot PRs individually. They are superseded by this reviewed integration boundary and should be closed with an explicit comment:

> Superseded by the reviewed integration PR that merged the accepted dependency/workflow update while preserving `actions/setup-node@v6`. Closing to avoid replaying stale branch hunks.

Apply that superseded closure to #233, #234, #235, #236, #237, #238, and #239.

Close issue #240 separately with the governance wording:

> Rebaseline erledigt: the overdue marker is resolved by the integration PR. VOID-010 and VOID-011 remain open as substantive evidence boundaries; they were not closed or marked complete.

This keeps the GitHub queue clean without creating an F7/False-OK signal: the automation tickets are complete, but the underlying VOIDs remain intentionally open until their verifier-facing evidence exists.

## Verifier expectation

Run the repository verifier (`make verify`) plus JS workspace lock/type/lint checks after lockfile refresh. Any failure should be treated as a boundary signal, not guessed around.
