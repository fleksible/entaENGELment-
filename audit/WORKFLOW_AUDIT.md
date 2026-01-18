# Workflow & CI Audit

**Audit Session:** audit-2026-01-18-SDbnU
**Scan Date:** 2026-01-18

---

## Workflow Inventory

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| CI Pipeline | `ci.yml` | push/PR to main, claude/** | Full lint/test/security pipeline |
| DeepJump CI | `deepjump-ci.yml` | push/PR to main, scheduled | DeepJump Protocol v1.2 flow |
| Metatron Guard | `metatron-guard.yml` | PR open/edit/sync, push | FOKUS marker enforcement |
| CI Smoke | `ci-smoke.yml` | push/PR | Quick smoke tests |
| Evidence Bundle | `ci-evidence-bundle.yml` | - | Evidence collection |
| Policy Lint | `ci-policy-lint.yml` | - | Policy validation |
| Test | `test.yml` | - | Test execution |

---

## Workflow Analysis

### ci.yml (Main Pipeline)

**Stages:**
1. **Verify** (4 Python versions: 3.9-3.12)
   - ruff check
   - black --check
   - mypy (continue-on-error: true)

2. **Build** (depends on verify)
   - Unit tests
   - Integration tests
   - Ethics tests
   - Coverage (threshold: 20%)

3. **Security** (depends on build)
   - bandit security linter
   - safety dependency check

4. **Gate Policy** (depends on build)
   - Gate toggle validation tests

**Issues Identified:**
- mypy runs with `continue-on-error: true` (type errors not blocking)
- Coverage threshold is very low (20%)
- Security checks run with `continue-on-error: true`

**Recommendations:**
- [ ] Consider stricter type checking
- [ ] Raise coverage threshold as project matures
- [ ] Make security checks blocking

### deepjump-ci.yml (DeepJump Protocol)

**Phases:**
1. **Verify** - verify_pointers.py, claim_lint.py, pytest
2. **Status** - status_emit.py + status_verify.py (HMAC)
3. **Snapshot** - snapshot_guard.py (manifest generation)
4. **Upload** - Artifact upload to GitHub

**Security Notes:**
- Uses `ENTA_HMAC_SECRET` from secrets
- Falls back to ephemeral secret if not set (with warning)
- Scheduled daily at 03:00 UTC

**Issues Identified:**
- claim_lint runs with `continue-on-error: true`
- Tests run with warning on failure

### metatron-guard.yml (Focus Enforcement)

**Purpose:** Enforce FOKUS marker in PRs and commits

**Features:**
- PR body check for FOKUS: marker
- Commit message check (soft warning)
- Skips merge/squash/fixup commits

**Status:** Working as designed

---

## Actions Version Audit

| Action | Version | Pinning | Status |
|--------|---------|---------|--------|
| actions/checkout | v4 | Tag | ⚠️ Should pin to SHA |
| actions/setup-python | v5 | Tag | ⚠️ Should pin to SHA |
| codecov/codecov-action | v4 | Tag | ⚠️ Should pin to SHA |
| actions/upload-artifact | v4 | Tag | ⚠️ Should pin to SHA |

**Recommendation:** Pin actions to full SHA for security.

---

## Secrets & Permissions

| Secret | Used In | Purpose |
|--------|---------|---------|
| `ENTA_HMAC_SECRET` | deepjump-ci.yml | HMAC signing |
| `CODECOV_TOKEN` | ci.yml | Coverage upload |

**Permissions:** Default (not explicitly restricted)

**Recommendation:** Add explicit `permissions:` block to workflows.

---

## Makefile Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `make verify` | 1 | Full verification (port-lint, test, verify-pointers, claim-lint) |
| `make status` | 2 | Emit HMAC status |
| `make status-verify` | 2 | Emit + verify status |
| `make snapshot` | 3 | Generate snapshot manifest |
| `make deepjump` | All | Full DeepJump flow |

**Local Execution:** Available via Makefile

---

## Test Coverage Areas

| Category | Path | Count |
|----------|------|-------|
| Unit | `tests/unit/` | ~10 files |
| Integration | `tests/integration/` | ~5 files |
| Ethics | `tests/ethics/` | ~5 files |
| CPT | `tests/cpt/` | ~3 files |
| JavaScript | `__tests__/` | ~10 files |
| Fractalsense | `Fractalsense/tests/` | ~10 files |

---

## CI Status Summary

| Check | Status | Notes |
|-------|--------|-------|
| Lint (ruff) | Blocking | Must pass |
| Format (black) | Blocking | Must pass |
| Type (mypy) | Non-blocking | Warnings only |
| Unit Tests | Blocking | Must pass |
| Integration Tests | Blocking | Must pass |
| Ethics Tests | Blocking | Must pass |
| Security (bandit) | Non-blocking | Warnings only |
| Security (safety) | Non-blocking | Warnings only |
| FOKUS (PR) | Blocking | Must have FOKUS marker |
| FOKUS (Commit) | Non-blocking | Soft warning |
