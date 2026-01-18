# Action Plan

**Audit Session:** audit-2026-01-18-SDbnU
**Generated:** 2026-01-18
**Status:** Ready for execution

---

## Quick Wins (< 1 hour each)

### QW-1: Pin GitHub Actions to SHA
**Priority:** P1 | **Effort:** 15 min | **Risk:** Low

```yaml
# Replace in all workflow files:
# Before
uses: actions/checkout@v4
# After
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

Files to update:
- [ ] `.github/workflows/ci.yml`
- [ ] `.github/workflows/deepjump-ci.yml`
- [ ] `.github/workflows/metatron-guard.yml`
- [ ] `.github/workflows/ci-smoke.yml`

---

### QW-2: Configure ENTA_HMAC_SECRET
**Priority:** P1 | **Effort:** 5 min | **Risk:** Low

```bash
# Generate secure secret
openssl rand -hex 32

# Add to GitHub:
# Settings → Secrets and variables → Actions → New repository secret
# Name: ENTA_HMAC_SECRET
# Value: <generated hex>
```

---

### QW-3: Raise Coverage Threshold
**Priority:** P2 | **Effort:** 5 min | **Risk:** Low

```yaml
# ci.yml line 97
# Before
coverage report --fail-under=20
# After
coverage report --fail-under=50
```

---

### QW-4: Create docs/voids_backlog.md
**Priority:** P2 | **Effort:** 10 min | **Risk:** Low

```bash
# Add script or manual creation
python3 << 'EOF'
import yaml
with open('VOIDMAP.yml') as f:
    data = yaml.safe_load(f)
# Generate markdown from voids
EOF
```

Or create placeholder:
```markdown
# VOIDs Backlog

Generated from VOIDMAP.yml. See VOIDMAP.yml for authoritative list.
```

---

### QW-5: Add Workflow Status Badges
**Priority:** P3 | **Effort:** 10 min | **Risk:** Low

Add to README.md:
```markdown
![CI](https://github.com/fleksible/entaENGELment-/actions/workflows/ci.yml/badge.svg)
![DeepJump](https://github.com/fleksible/entaENGELment-/actions/workflows/deepjump-ci.yml/badge.svg)
```

---

## Mid-Term (1-3 days)

### MT-1: Make Security Checks Blocking
**Priority:** P2 | **Effort:** 2 hours | **Risk:** Medium

Update `ci.yml`:
```yaml
# Remove continue-on-error from:
- bandit security linter (line 124)
- safety check (line 128)

# Fix any existing issues first
bandit -r src/ tools/
safety check
```

---

### MT-2: Implement Version Tagging
**Priority:** P2 | **Effort:** 4 hours | **Risk:** Low

1. Create `CHANGELOG.md` from commit history
2. Add release workflow:
```yaml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: softprops/action-gh-release@v1
```

3. Create first tag: `git tag v1.0.0 && git push --tags`

---

### MT-3: Branch Cleanup
**Priority:** P2 | **Effort:** 1 hour | **Risk:** Medium

1. Review stale branches:
```bash
git branch -r --sort=-committerdate | head -20
```

2. Delete merged branches via GitHub UI or:
```bash
# For each stale branch
gh pr list --head <branch> --state merged
git push origin --delete <branch>
```

3. Enable auto-delete on merge (Settings → General → Auto-delete head branches)

---

### MT-4: Add Explicit Workflow Permissions
**Priority:** P2 | **Effort:** 30 min | **Risk:** Low

Add to each workflow:
```yaml
permissions:
  contents: read
  pull-requests: write  # if needed
  actions: read
```

---

### MT-5: Create Placeholder Files for Planned Features
**Priority:** P3 | **Effort:** 30 min | **Risk:** Low

Create stub files:
- [ ] `docs/sensors/bom.md` — "# Sensor BOM\n\nPlanned. See VOID-013."
- [ ] `spec/sensors.spec.json` — `{"$schema": "...", "status": "planned"}`
- [ ] `diagrams/threefold_apex.svg` — Placeholder SVG

---

## Strategic (1-4 weeks)

### ST-1: VOID Ownership Assignment
**Priority:** P2 | **Effort:** 2 days | **Risk:** Low

1. Review each OPEN VOID in VOIDMAP.yml
2. Assign owner (person or "claude-code")
3. Set target sprint/date
4. Add accountability tracking

---

### ST-2: Contributor Onboarding Guide
**Priority:** P3 | **Effort:** 1 week | **Risk:** Low

Create `docs/CONTRIBUTING.md` (or enhance existing):
- Development setup
- Architecture overview
- Guard system explanation
- Commit message format
- PR template with FOKUS requirement

---

### ST-3: Architectural Review
**Priority:** P3 | **Effort:** 1 week | **Risk:** Medium

Address complexity concerns:
- Evaluate Fractalsense/Lyra/dashboard consolidation
- Document module boundaries
- Consider monorepo vs multi-repo

---

### ST-4: SBOM Generation
**Priority:** P3 | **Effort:** 2 days | **Risk:** Low

Add to CI:
```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    format: cyclonedx-json
    output-file: sbom.json
```

---

### ST-5: Dependabot Configuration
**Priority:** P3 | **Effort:** 1 hour | **Risk:** Low

Create `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "npm"
    directory: "/ui-app"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Execution Checklist

### Immediate (Today)
- [ ] QW-1: Pin GitHub Actions
- [ ] QW-2: Configure HMAC secret

### This Week
- [ ] QW-3: Raise coverage threshold
- [ ] QW-4: Create voids_backlog.md
- [ ] QW-5: Add status badges
- [ ] MT-4: Add workflow permissions

### Next Sprint
- [ ] MT-1: Blocking security checks
- [ ] MT-2: Version tagging
- [ ] MT-3: Branch cleanup
- [ ] MT-5: Placeholder files

### Backlog
- [ ] ST-1: VOID ownership
- [ ] ST-2: Onboarding guide
- [ ] ST-3: Architectural review
- [ ] ST-4: SBOM generation
- [ ] ST-5: Dependabot

---

## Dependencies

```
QW-1 → (none)
QW-2 → (none)
QW-3 → MT-1 (fix issues first)
MT-1 → (fix bandit/safety findings)
MT-2 → QW-1 (secure release)
ST-1 → (none)
```
