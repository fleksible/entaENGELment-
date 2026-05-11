# Repository Audit Follow-up — EntaENGELment

**Original audit date:** 2026-04-06  
**Follow-up date:** 2026-05-11  
**Source:** superseded PR #157  
**Purpose:** preserve the useful audit findings as documentation only, without importing the mixed CI/dependency/VOIDMAP/CHANGELOG changes from #157.

---

## Status summary

PR #157 was closed unmerged because it mixed unrelated concerns:

- audit report content
- CI workflow changes
- dependency/requirements changes
- UI build checks
- VOIDMAP updates
- CHANGELOG/release-preflight updates

The findings were split into follow-up issues instead of merging #157 as a whole.

## Follow-up containers

- #169 — tracking issue for splitting #157 safely
- #170 — docs-only audit extraction
- #171 — CI security-scan fix
- #172 — UI build check, without UI major upgrades
- #173 — VOIDMAP/release-doc updates
- #174 — UI major upgrade track superseding #155

## Already completed since the original audit

- #151 merged: `codecov/codecov-action` 5.5.2 → 6.0.0
- #159 merged: `actions/github-script` 8.0.0 → 9.0.0
- #176 merged: documented `SUSPENDED` as an allowed VOIDMAP status
- #177 merged: replaced deprecated `safety check --stdin --json` with `pip-audit -r requirements.txt`
- #171 closed as completed after #177
- #157 closed unmerged as superseded
- #175 closed unmerged as superseded by #177

---

## Findings carried forward

### F-01 — Deprecated `safety check --stdin --json`

**Original status:** open / critical  
**Current status:** completed via #177

The original audit identified this CI command:

```bash
pip freeze | safety check --stdin --json
```

This has been replaced with:

```bash
pip-audit -r requirements.txt
```

The replacement was kept isolated to `.github/workflows/ci.yml` and validated by a successful CI Pipeline, including the Security Scan.

### F-02 — `test.yml` stale branch triggers

**Original status:** open / high  
**Current status:** still open, should be handled separately

The original audit reported that `test.yml` referenced stale branch names such as `master` and `develop`. This should not be folded into an audit-report PR. Handle in a dedicated CI hygiene PR.

### F-03 — Dual test infrastructure without explicit boundary

**Original status:** open / high  
**Current status:** still open, related to #172

There are separate testing surfaces in the repository. The follow-up should clarify which workflow tests which part of the project and avoid mixing UI build coverage with unrelated governance changes.

### F-04 — UI major dependency surface

**Original status:** open / high  
**Current status:** tracked by #174; #155 remains HOLD

#155 should not be treated as a normal Dependabot merge. It is a UI-major upgrade surface and must be split into smaller, testable upgrade steps.

### F-05 — Codecov action drift

**Original status:** open / medium  
**Current status:** completed via #151

`codecov/codecov-action` has been upgraded to v6.0.0. Coverage upload should still be watched in future CI runs, but the dependency PR itself is merged.

### F-06 — Branch protection on `main`

**Original status:** open / medium  
**Current status:** still open; GitHub Settings action required

This cannot be fixed safely by a code PR alone. It requires repository settings work: branch protection, required checks, and review policy.

### F-07 — `SUSPENDED` VOIDMAP status undocumented

**Original status:** hint / medium  
**Current status:** completed via #176

`SUSPENDED` is now listed in the VOIDMAP status header.

### F-08 — RC preflight checklist open

**Original status:** open / medium  
**Current status:** still open; do not mark complete without fresh evidence

Any RC-preflight changes should be separate from dependency, UI, or audit-report work. Do not check boxes merely because the audit report exists.

### F-09 — stale remote branches

**Original status:** open / low  
**Current status:** still open; requires verification before deletion

Follow G3-style deletion discipline: verify whether each branch is merged or obsolete before pruning.

### F-10 — root-level legacy artifacts

**Original status:** hint / low  
**Current status:** still open; archive only after reference checks

Do not delete or move root-level artifacts without verifying references and intended use.

### F-11 — `VOIDMAP.yml` `last_updated`

**Original status:** hint / low  
**Current status:** still open as a policy/process question

#176 intentionally did not update `last_updated`, because it was a minimal header correction. A future VOIDMAP process PR can define when and how this field changes.

---

## Current PR / issue state after follow-up

### Merged

- #151 — codecov-action v6
- #159 — actions/github-script v9
- #176 — VOIDMAP `SUSPENDED` documentation
- #177 — CI security scan uses `pip-audit`

### Closed unmerged / superseded

- #157 — superseded by split issues
- #175 — superseded by #177

### Open / held

- #155 — HOLD; UI-major dependency surface
- #169 — tracking issue
- #170 — this docs-only extraction
- #172 — UI build check
- #173 — remaining VOIDMAP/release-doc follow-up
- #174 — UI major upgrade track

---

## Guardrails for subsequent work

- Keep docs-only changes separate from workflow/dependency changes.
- Keep UI build checks separate from UI major upgrades.
- Keep release-preflight claims evidence-bound.
- Do not merge #155 as a single Dependabot PR.
- Do not revive #157 as a whole.

---

## Closure note

This document preserves the useful audit signal from #157 while recording which findings have already been resolved. It is intentionally documentation-only and should not be treated as a technical migration patch.
