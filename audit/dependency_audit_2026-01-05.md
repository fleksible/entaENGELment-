# Dependency Audit Report

**Date:** 2026-01-05
**Repository:** entaENGELment-
**Auditor:** Claude Code

---

## Executive Summary

| Category | Status | Issues Found |
|----------|--------|--------------|
| Outdated Packages | ⚠️ Minor | 1 package has available update |
| Security Vulnerabilities | ✅ None | Project deps have no known CVEs |
| Bloat/Unnecessary Deps | ⚠️ Moderate | Potential optimization available |
| Configuration Issues | 🔴 Critical | Duplicate/inconsistent version specs |

---

## 1. Configuration Issues (Critical)

### 1.1 Duplicate numpy specification in requirements.txt

**File:** `requirements.txt:3-4`
```
numpy>=1.24.0
numpy>=1.20      # <-- DUPLICATE with different version
```

**Impact:** Confusing, pip uses the last specification, but this is poor practice.

**Fix:** Remove duplicate line.

### 1.2 Inconsistent numpy versions across files

| File | numpy Version |
|------|---------------|
| requirements.txt | `>=1.24.0` (and duplicate `>=1.20`) |
| pyproject.toml | `>=1.21.0` |

**Recommendation:** Align to `>=1.21.0` (supports Python 3.9 per pyproject.toml) or `>=1.24.0` if Python 3.9 support isn't required.

---

## 2. Package Usage Analysis

### 2.1 numpy (REQUIRED - Heavy Usage)

**Usage:** 8 files

| File | Import |
|------|--------|
| `src/core/eci.py` | `import numpy as np` |
| `src/core/stability_guard.py` | `import numpy as np` |
| `src/stability/hessian_void.py` | `import numpy as np` |
| `src/stability/spectral_void.py` | `import numpy as np` |
| `tests/cpt/test_cpt_harness.py` | `import numpy as np` |
| `tests/stability/test_*.py` (3 files) | `import numpy as np` |

**Verdict:** ✅ Essential dependency, heavy usage throughout core modules.

### 2.2 scipy (QUESTIONABLE - Minimal Usage)

**Usage:** 1 file only

| File | Import | Function Used |
|------|--------|---------------|
| `tests/cpt/test_cpt_harness.py:11` | `from scipy.spatial.distance import cosine` | `cosine()` |

**Analysis:** SciPy is a large package (~40MB installed) used only for a single `cosine` distance function in one test file.

**Recommendation:** Consider replacing with numpy-only implementation:
```python
def cosine_distance(u, v):
    return 1 - np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
```

**Verdict:** ⚠️ Candidate for removal - significant size reduction possible.

### 2.3 pyyaml (REQUIRED - Light Usage)

**Usage:** 1 file

| File | Import |
|------|--------|
| `tools/verify_pointers.py:19` | `import yaml` (conditional) |

**Analysis:** Used to parse YAML index files for pointer verification. Given the project's heavy use of YAML configuration files (`index/`, `adapters/`, `seeds/`), keeping this dependency is justified.

**Verdict:** ✅ Justified - YAML parsing is core functionality.

---

## 3. Security Vulnerability Scan

### 3.1 Project Dependencies

| Package | Version Required | Known CVEs |
|---------|-----------------|------------|
| numpy | >=1.21.0 | None |
| scipy | >=1.7.0 | None |
| pyyaml | >=6.0 | None |

**Status:** ✅ No vulnerabilities in project dependencies.

### 3.2 Development Dependencies

| Package | Version Required | Known CVEs |
|---------|-----------------|------------|
| pytest | >=7.0 | None |
| pytest-cov | >=4.0 | None |
| black | >=23.0 | None |
| ruff | >=0.1.0 | None |
| mypy | >=1.0 | None |

**Status:** ✅ No vulnerabilities in dev dependencies.

### 3.3 System/Build Dependencies (Not project-specific)

Found vulnerabilities in system packages (not directly declared by project):
- `cryptography 41.0.7`: 4 CVEs (fix: upgrade to 43.0.1+)
- `pip 24.0`: CVE-2025-8869 (fix: upgrade to 25.3)
- `setuptools 68.1.2`: 2 CVEs (fix: upgrade to 78.1.1+)

**Recommendation:** Update system packages in CI/production environments.

---

## 4. Outdated Packages

| Package | Current | Latest | Priority |
|---------|---------|--------|----------|
| PyYAML | 6.0.1 | 6.0.3 | Low (patch release) |

---

## 5. Recommendations

### Immediate Actions (P0)

1. **Fix duplicate numpy in requirements.txt**
   - Remove line 4 (`numpy>=1.20`)

2. **Align numpy versions**
   - Use `>=1.21.0` consistently across all files

### Short-term (P1)

3. **Consider removing scipy**
   - Replace with 3-line numpy implementation
   - Saves ~40MB in dependencies
   - Reduces attack surface

4. **Update PyYAML version spec**
   - Change `>=6.0` to `>=6.0.1` for minor security fixes

### Long-term (P2)

5. **Pin exact versions for reproducibility**
   - Consider using `pip-compile` to generate locked requirements

6. **Add pre-commit hook for dependency auditing**
   - `pip-audit` integration in CI

---

## 6. Dependency Tree Summary

```
entaengelment
├── numpy>=1.21.0       [REQUIRED - core math operations]
├── scipy>=1.7.0        [OPTIONAL - can be removed]
└── pyyaml>=6.0         [REQUIRED - YAML parsing]

[dev]
├── pytest>=7.0
├── pytest-cov>=4.0
├── black>=23.0
├── ruff>=0.1.0
└── mypy>=1.0
```

---

## Appendix: Files Changed

- `requirements.txt` - Remove duplicate numpy, update versions
- `tests/cpt/test_cpt_harness.py` - (Optional) Replace scipy usage
