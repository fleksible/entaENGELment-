# Security & Compliance Audit Notes

**Audit Session:** audit-2026-01-18-SDbnU
**Scan Date:** 2026-01-18
**Scope:** Light audit (pattern-based, no dynamic analysis)

---

## Summary

| Category | Status | Risk Level |
|----------|--------|------------|
| Hardcoded Secrets | ✅ None found | Low |
| Dangerous Functions | ✅ Clean | Low |
| License Compliance | ✅ Apache-2.0 | Low |
| Dependency Security | ⚠️ Needs review | Medium |
| CI Security | ⚠️ Actions not pinned | Medium |

---

## Secrets & Credentials Scan

### Environment Variables (Proper Usage)

| Variable | Used In | Status |
|----------|---------|--------|
| `ENTA_HMAC_SECRET` | tools/status_emit.py, status_verify.py | ✅ Env-based |
| `CI_SECRET` | tools/status_emit.py, status_verify.py | ✅ Env-based |
| `CODECOV_TOKEN` | .github/workflows/ci.yml | ✅ GitHub Secrets |

**Verdict:** No hardcoded secrets found. All sensitive values read from environment.

### Sensitive File Patterns

| Pattern | Files Found | Risk |
|---------|-------------|------|
| `.env` | 0 | ✅ None |
| `credentials*` | 0 | ✅ None |
| `*.pem` / `*.key` | 0 | ✅ None |
| `*secret*` | 0 (excluding env refs) | ✅ None |

---

## Dangerous Code Patterns

### eval() / exec()

```
Search: eval(
Result: 0 occurrences
Status: ✅ Clean
```

### Shell Execution

```
Search: subprocess, os.system, exec(
Result: Found in test files only
Location: tests/test_claim_lint.py, tests/test_snapshot_guard.py, tests/test_verify_pointers.py
Status: ✅ Acceptable (test harness)
```

### Command Injection Risk

| File | Usage | Risk |
|------|-------|------|
| tests/*.py | subprocess.run with static args | ✅ Low |

**Note:** All subprocess usage is in test files with controlled inputs.

---

## License Compliance

### Main License

| Field | Value |
|-------|-------|
| License | Apache License 2.0 |
| File | `LICENSE` |
| Status | ✅ Valid |

### License Obligations

- ✅ License file present
- ✅ Copyright notice preserved
- ⚠️ NOTICE file not present (optional for Apache-2.0)

### Third-Party Dependencies

| Package | License | Status |
|---------|---------|--------|
| pyyaml | MIT | ✅ Compatible |
| numpy | BSD | ✅ Compatible |
| scipy | BSD | ✅ Compatible |
| pytest | MIT | ✅ Compatible |
| black | MIT | ✅ Compatible |
| ruff | MIT | ✅ Compatible |

**Verdict:** All dependencies have Apache-2.0 compatible licenses.

---

## CI/CD Security

### GitHub Actions

| Issue | Severity | Recommendation |
|-------|----------|----------------|
| Actions not SHA-pinned | Medium | Pin to commit SHA |
| No permissions block | Low | Add explicit permissions |
| HMAC fallback to ephemeral | Low | Set proper secret |

### Secrets Management

| Secret | Configured? | Notes |
|--------|-------------|-------|
| `ENTA_HMAC_SECRET` | ⚠️ Unknown | Fallback warns if missing |
| `CODECOV_TOKEN` | ⚠️ Unknown | Uses continue-on-error |

---

## OWASP Top 10 Quick Check

| Risk | Status | Notes |
|------|--------|-------|
| A01: Broken Access Control | N/A | No auth system |
| A02: Cryptographic Failures | ⚠️ | HMAC properly used |
| A03: Injection | ✅ | No user input to shell |
| A04: Insecure Design | ✅ | Guard system in place |
| A05: Security Misconfiguration | ⚠️ | CI could be stricter |
| A06: Vulnerable Components | ⚠️ | Need `safety` scan |
| A07: Auth Failures | N/A | No auth system |
| A08: Software Integrity | ⚠️ | Actions not pinned |
| A09: Logging Failures | ✅ | Receipt logging present |
| A10: SSRF | N/A | No external requests |

---

## Recommendations

### P1 - High Priority

1. **Pin GitHub Actions to SHA**
   ```yaml
   # Before
   uses: actions/checkout@v4
   # After
   uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
   ```

2. **Configure ENTA_HMAC_SECRET**
   - Go to Settings → Secrets → Actions
   - Add `ENTA_HMAC_SECRET` with secure random value

### P2 - Medium Priority

3. **Add explicit permissions**
   ```yaml
   permissions:
     contents: read
     pull-requests: write
   ```

4. **Run `safety check` regularly**
   - Already in CI but non-blocking
   - Consider making it blocking

### P3 - Low Priority

5. **Add NOTICE file** (Apache-2.0 best practice)
6. **Enable Dependabot** for dependency updates
7. **Add security policy** (SECURITY.md)

---

## Verification Commands

```bash
# Check for secrets in git history (requires git-secrets or similar)
git log -p | grep -E "(api_key|secret|password)" | head -20

# Run bandit security linter
bandit -r src/ tools/ -f json

# Check dependencies for vulnerabilities
safety check

# Verify HMAC secret is set in CI
gh secret list
```
