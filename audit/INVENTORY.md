# Repository Inventory

**Audit Session:** audit-2026-01-18-SDbnU
**Repository:** fleksible/entaENGELment-
**HEAD SHA:** 523e706ab4ebe15b3a93ddbde29cc39f7b8369fe

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Commits | 179 |
| Total Tracked Files | 1,548 |
| Tags | 0 |
| Remote Branches | 10 |
| Local Branches | 2 |
| First Commit | e1f0a1d (Initial commit) |
| Latest Commit | 523e706 (2026-01-17) |

---

## Authors by Commit Count

| Rank | Author | Commits | % |
|------|--------|---------|---|
| 1 | flek | 103 | 57.5% |
| 2 | Claude | 69 | 38.5% |
| 3 | User | 5 | 2.8% |
| 4 | fleksible | 2 | 1.1% |

**Observation:** ~39% of commits are AI-generated (Claude), indicating heavy AI-assisted development.

---

## Hotspot Files (Most Frequently Changed)

| Rank | File | Changes | Risk Level |
|------|------|---------|------------|
| 1 | README.md | 15 | Low |
| 2 | .github/workflows/ci.yml | 13 | **Medium** |
| 3 | docs/masterindex.md | 11 | Low |
| 4 | .gitignore | 7 | Low |
| 5 | tools/port_lint.py | 6 | Medium |
| 6 | tools/mzm/gate_toggle.py | 6 | Medium |
| 7 | pyproject.toml | 6 | Medium |
| 8 | .github/workflows/ci-smoke.yml | 6 | Medium |
| 9 | docs/architecture.md | 5 | Low |
| 10 | REPOSITORY_ESSENZ_ANALYSE.md | 5 | Low |

**Observation:** CI/CD configuration is a high-churn area (19 changes across workflow files).

---

## Largest Files

| Size (bytes) | File | Type |
|--------------|------|------|
| 284,784 | package-lock.json | Lock file |
| 215,490 | ui-app/package-lock.json | Lock file |
| 29,830 | REPOSITORY_ESSENZ_ANALYSE.md | Documentation |
| 18,317 | Fractalsense/tests/unit/test_modular_app_structure.py | Test |
| 17,232 | Fractalsense/tests/unit/test_color_generator.py | Test |
| 16,558 | Fractalsense/tests/unit/test_sound_generator.py | Test |
| 16,260 | Fractalsense/modular_app_structure.py | Source |
| 16,099 | Fractalsense/fractal-visualizer.js | Source |

**Observation:** Lock files dominate size; no large binaries detected.

---

## Branch Overview

### Remote Branches

| Branch | SHA | Date | Author | Status |
|--------|-----|------|--------|--------|
| origin/main | 523e706 | 2026-01-17 | flek | **Canonical** |
| origin/hi | 523e706 | 2026-01-17 | flek | Identical to main |
| origin/fleksible-patch-1 | e327637 | 2026-01-18 | flek | Active |
| origin/claude/update-readme-docs-kf9LE | d2db08d | 2026-01-17 | Claude | Feature |
| origin/codex/add-connectivity-tests-and-enhance-ci | e567981 | 2026-01-15 | flek | Feature |
| origin/claude/repo-maintenance-consolidation-LA2ek | 315e8dc | 2026-01-04 | flek | Stale |
| origin/claude/analyze-repo-essence-LKgK4 | dd28e79 | 2026-01-03 | Claude | Stale |
| origin/claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D | 9fbf1de | 2026-01-03 | Claude | Stale |
| origin/codex/update-markdown-file-in-repository | 68395d7 | 2025-12-29 | flek | Stale |
| origin/codex/update-readme-for-deepjump-integration | 723f8bc | 2025-12-29 | flek | Stale |

### Local Branches (Orphaned)

| Branch | SHA | Note |
|--------|-----|------|
| claude/repo-audit-release-SDbnU | 523e706 | Remote deleted |
| claude/merge-phase-0-zip-fBeQL | 523e706 | Remote deleted |

---

## Risk Commits (Structural Changes)

| SHA | Subject | Type |
|-----|---------|------|
| 87b330a | refactor(structure): complete codebase restructure | **Major restructure** |
| 98ce5de | Masterindex-Struktur implementiert | Reorganization |
| 7e9e026 | Kohärenz-Audit: Broken Links, Pfad-Inkonsistenzen | Cleanup |

---

## Pull Request Activity (gh CLI unavailable)

Unable to fetch PR data - gh CLI not authenticated.

**Known PRs from commit messages:**
- PR #55: claude/audit-branch-structure-YU3Vb (merged 2026-01-17)
- PR #54: claude/fractalsense-ui-integration-UfxBi (merged 2026-01-17)
- PR #53: claude/entaengelment-ui-prototype-VNbAR (merged 2026-01-17)
- PR #52: claude/fix-ci-pipeline-O7uZC (merged 2026-01-17)
- PR #50: claude/fix-commits-workflow-YKETI (merged 2026-01-15)
- PR #49: claude/fix-commits-workflow-YKETI (merged 2026-01-15)
- ... (55 total PRs referenced)

---

## Observations

1. **High AI collaboration:** 39% of commits from Claude agent
2. **No tags/releases:** No version tagging strategy visible
3. **Stale branches:** 5+ branches older than 2 weeks
4. **CI churn:** Workflow files changed frequently (stability concern)
5. **Clean file hygiene:** No large binaries in repo
