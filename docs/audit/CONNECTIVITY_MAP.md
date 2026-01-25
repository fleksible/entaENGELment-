# CONNECTIVITY MAP - EntaENGELment Repository
**Audit Date:** 2026-01-24
**Phase:** 1 - Connectivity Matrix Analysis
**Status:** COMPLETE

---

## Executive Summary

**Overall Connectivity Health: 93% (GOOD)**

| Category | Total | Valid | Broken | Warning | Health |
|----------|-------|-------|--------|---------|--------|
| **Markdown Links** | 66+ | 66 | 0 | 0 | 100% ✓ |
| **YAML/JSON Pointers** | 47 | 40 | 3 | 4 | 85% ⚠ |
| **Python Imports** | ~150 | ~143 | 2 | 5 | 95% ⚠ |
| **JavaScript Imports** | 32+ | 32 | 0 | 0 | 100% ✓ |
| **CI Wiring** | 8 workflows | 8 | 0 | 0 | 100% ✓ |
| **Docs ↔ Code** | ~30 | ~30 | 0 | 0 | 100% ✓ |

**Critical Issues:** 5 (2 runtime blockers, 3 missing governance files)
**Warnings:** 9 (mostly import style consistency)

---

## 1. Markdown Internal Links (100% Valid)

### Summary
- **Total Files Analyzed:** 97 markdown files
- **Total Links Found:** 66+
- **Broken Links:** 0 ✓
- **Valid Links:** 66 (100%)
- **Suspicious Patterns:** 0 ✓

### Link Distribution

| Source File | Links | Status | Notes |
|-------------|-------|--------|-------|
| `README.md` | 14 | ✓ ALL VALID | Core implementation pointers |
| `CLAUDE.md` | 4 | ✓ ALL VALID | House rules references |
| `docs/canvas_links.md` | 16 | ✓ ALL VALID | Master link registry |
| `docs/START_HERE.md` | 4 | ✓ ALL VALID | Orbital model docs |
| `docs/bio_spiral_viewer.md` | 3 | ✓ ALL VALID | Viewer docs |
| `Fractalsense/user_manual.md` | 7 anchors | ✓ ALL VALID | Internal navigation |
| `Fractalsense/presentation_guide.md` | 5 anchors | ✓ ALL VALID | Internal navigation |
| Other docs | 13+ | ✓ ALL VALID | Various references |

### Key Link Hubs (High Connectivity)

1. **README.md** → Central navigation point
   - Links to 14 core implementation files
   - All spec/, src/, docs/ references valid

2. **docs/canvas_links.md** → Comprehensive link registry
   - 16 architecture/roadmap docs
   - All index/, spec/ references valid

3. **CLAUDE.md** → House rules documentation
   - 4 guard/rule files in `.claude/rules/`
   - All references valid

### Connectivity Graph

```
README.md
  ├─→ docs/masterindex.md ✓
  ├─→ spec/cglg.spec.json ✓
  ├─→ spec/eci.spec.json ✓
  ├─→ src/core/eci.py ✓
  ├─→ tests/cpt/test_cpt_harness.py ✓
  └─→ (10 more valid links)

CLAUDE.md
  ├─→ .claude/rules/annex.md ✓
  ├─→ .claude/rules/metatron.md ✓
  ├─→ .claude/rules/security.md ✓
  └─→ .claude/skills/witness_mode.md ✓

docs/canvas_links.md
  ├─→ index/COMPACT_INDEX_v3.yaml ✓
  ├─→ index/modules/MOD_6_RECEIPTS_CORE.yaml ✓
  └─→ (14 more valid links)
```

**Conclusion:** Markdown linking is healthy. No action required.

---

## 2. YAML/JSON Pointer References (85% Valid)

### Summary
- **Total References:** 47 unique path references
- **Valid (existing):** 40 (85%)
- **Dead Pointers:** 3 (6%) ⚠
- **Generated Outputs:** 4 (9%)

### 2.1 Dead Pointers (3 CRITICAL)

| Pointer | Source | Line | Severity | Impact |
|---------|--------|------|----------|--------|
| `policies/gateproof_v1.yaml` | VOIDMAP.yml | 116 | **HIGH** | VOID-012 governance checklist missing |
| `docs/sensors/bom.md` | VOIDMAP.yml | 130 | MEDIUM | VOID-013 closure path incomplete |
| `spec/sensors.spec.json` | VOIDMAP.yml | 130 | MEDIUM | VOID-013 closure path incomplete |

### 2.2 Generated Outputs (4 - Expected)

These are runtime artifacts created by CI/tools:
- `out/status/deepjump_status.json` (created by `tools/status_emit.py`)
- `out/badges/deepjump.svg` (created by CI workflow)
- `out/verify.json` (created by `tests/verify_deep_jump.py`)
- `out/snapshot_manifest.json` (created by `tools/snapshot_guard.py`)

**Status:** ✓ Expected behavior, no action needed

### 2.3 Valid References by Category

| Category | Count | Files |
|----------|-------|-------|
| **Tools** | 8 | All exist in `tools/` |
| **Tests** | 3 | All exist in `tests/` |
| **Scripts** | 1 | `scripts/evidence_bundle.sh` exists |
| **Index Modules** | 6 | All exist in `index/modules/` |
| **Policies** | 2 | gate_policy_v1.json (✓), gateproof_v1.yaml (✗) |
| **Specs** | 5 | All exist except sensors.spec.json |
| **Seeds** | 2 | Both seed files exist |
| **Audit** | 2 | Both audit files exist |
| **Docs** | 3 | voids_backlog.md (✓), sensors/bom.md (✗) |
| **Receipts** | 2 | Sample receipt + directory exist |
| **Workflows** | 1 | Reusable workflow exists |

### 2.4 Cross-Reference Map

```
VOIDMAP.yml (GOLD)
  ├─→ tools/port_lint.py ✓
  ├─→ policies/port_codebooks.yaml ✓
  ├─→ policies/gateproof_v1.yaml ✗ MISSING
  ├─→ docs/sensors/bom.md ✗ MISSING
  └─→ spec/sensors.spec.json ✗ MISSING

index/COMPACT_INDEX_v3.yaml (GOLD)
  ├─→ modules/MOD_6_RECEIPTS_CORE.yaml ✓
  ├─→ modules/MOD_15_STATS_TESTS.yaml ✓
  └─→ ENTAENGELMENT_INDEX_v3_FUNCTORIAL.yaml ✓

index/modules/MOD_15_STATS_TESTS.yaml
  ├─→ tools/status_emit.py ✓
  ├─→ tools/status_verify.py ✓
  └─→ tests/verify_deep_jump.py ✓

index/modules/MOD_6_RECEIPTS_CORE.yaml
  ├─→ tools/snapshot_guard.py ✓
  ├─→ receipts/arc_sample.json ✓
  ├─→ seeds/seed_config.yaml ✓
  └─→ seeds/seed_extras.yaml ✓

.github/workflows/*.yml (8 files)
  ├─→ All tool references valid ✓
  ├─→ All script references valid ✓
  └─→ Reusable workflow reference valid ✓
```

**Conclusion:** 3 missing files block VOID closures. See CONNECTIVITY_FIXLIST.md for remediation.

---

## 3. Python Import Structure (95% Valid)

### Summary
- **Files Analyzed:** ~60 Python files
- **Critical Issues:** 2 (runtime blockers)
- **Style Inconsistencies:** 5 (code quality)
- **Circular Imports:** 0 ✓
- **Missing __init__.py:** 0 ✓

### 3.1 Critical Import Breakages (2 RUNTIME ERRORS)

#### Issue #1: Dead Module Import (CRITICAL)
**File:** `Fractalsense/test_resonance.py:26-28`
```python
from modules.resonance_enhancer import ResonanceEnhancerModule
from modules.resonance_enhancer.sound_generator import SoundGenerator
from modules.resonance_enhancer.color_generator import ColorGenerator
```
**Problem:** `modules/` directory doesn't exist
**Impact:** `ModuleNotFoundError` on import
**What exists instead:**
- `Fractalsense/sound_generator.py` ✓
- `Fractalsense/color_generator.py` ✓

**Fix:** Replace with direct imports or restructure

---

#### Issue #2: Directory-Dependent Import (HIGH)
**File:** `Fractalsense/tests/unit/test_sound_generator.py:26`
```python
from tests.conftest import get_dominant_frequency
```
**Problem:** Only works when pytest run from specific directories
**Impact:** Tests break depending on invocation method
**Fix:** Use relative import: `from ..conftest import get_dominant_frequency`

---

### 3.2 Import Style Inconsistencies (5 files)

#### Pattern 1: Implicit Relative Imports (MEDIUM)
**Files:**
- `Fractalsense/__init__.py:25`
- `Fractalsense/integration.py:13, 87, 107, 136, 164`

**Current (deprecated):**
```python
from modular_app_structure import ModuleInterface
```

**Should be (PEP 8 explicit):**
```python
from .modular_app_structure import ModuleInterface
```

---

#### Pattern 2: sys.path Manipulation (MEDIUM)
**Files:**
- `Fractalsense/tests/conftest.py`
- `Fractalsense/tests/unit/test_color_generator.py`
- `Fractalsense/tests/unit/test_modular_app_structure.py`

**Current pattern:**
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from color_generator import ColorGenerator
```

**Better approach:**
```python
from ...color_generator import ColorGenerator
```

**Impact:** Makes tests fragile and environment-dependent

---

### 3.3 Valid Import Patterns (✓)

**src/** (Core Package):
- All imports use absolute paths
- Proper package structure
- External modules import correctly:
  - `ledger.replay_determinism` ✓
  - `mapping.tensor_validator` ✓

**tools/** (Utility Scripts):
- Consistent absolute imports
- No circular dependencies
- All tool references resolve

**tests/** (Test Suite):
- Pytest discovery works correctly
- Proper test module structure
- __init__.py files present where needed (16 checked)

---

### 3.4 Import Dependency Graph

```
src/
  └─→ ledger.replay_determinism ✓
  └─→ mapping.tensor_validator ✓

tools/
  ├─→ src.core.metrics ✓
  └─→ yaml, json (stdlib) ✓

tests/
  ├─→ src.* (all valid) ✓
  └─→ pytest fixtures ✓

Fractalsense/
  ├─→ modules.* ✗ BROKEN
  ├─→ modular_app_structure ⚠ IMPLICIT
  └─→ tests.conftest ⚠ FRAGILE
```

**Conclusion:** 2 critical fixes required. 5 style improvements recommended.

---

## 4. JavaScript/TypeScript Imports (100% Valid)

### Summary
- **Files Analyzed:** 31 JS/TS files
- **Total Imports:** 32+ using `@/` alias
- **Broken Imports:** 0 ✓
- **Missing Modules:** 0 ✓
- **Path Mapping Issues:** 0 ✓

### 4.1 ui-app/ (Next.js/TypeScript) - HEALTHY

**Configuration:** `tsconfig.json`
```json
"paths": { "@/*": ["./*"] }
"moduleResolution": "bundler"
```

**All imports verified:**
- ✓ `@/types` → `/ui-app/types/index.ts` (11 exports)
- ✓ `@/lib/colormaps` → `/ui-app/lib/colormaps.ts`
- ✓ `@/lib/guard-definitions` → `/ui-app/lib/guard-definitions.ts`
- ✓ `@/lib/voidmap-parser` → `/ui-app/lib/voidmap-parser.ts`
- ✓ `@/lib/mock-data` → `/ui-app/lib/mock-data.ts`
- ✓ `@/components/fractalsense` → Barrel export valid
- ✓ `@/components/guards/*` → All components exist
- ✓ `@/components/voidmap/*` → All components exist
- ✓ `@/components/metatron/*` → All components exist

**NPM Dependencies:** All valid (react, next, tailwindcss verified)

---

### 4.2 __tests__/ (Jest/CommonJS) - HEALTHY

**Configuration:** `jest.config.js`
```javascript
moduleNameMapper: { '^@/(.*)$': '<rootDir>/Fractalsense/$1' }
```

**Files:**
- ✓ `setup.js` → `require('@testing-library/jest-dom')`
- ✓ `__mocks__/canvas.js` → All exports valid
- ✓ `__mocks__/web-audio.js` → 9 exports valid
- ✓ `unit/fractal-math.test.js` → Relative imports valid

---

### 4.3 Module System Consistency

| Location | System | Consistency | Status |
|----------|--------|-------------|--------|
| ui-app/ | ES6 modules | 100% ES6 `import` | ✓ |
| __tests__/ | CommonJS | 100% `require` | ✓ |
| Fractalsense/ | Vanilla JS | No module syntax | ✓ |
| main.js | CommonJS | 100% `require` | ✓ |

**No mixing detected** ✓

---

### 4.4 TypeScript Path Resolution

**Verification:** All 32 `@/` imports resolve correctly
- 32 scanned
- 32 valid (100%)
- 0 dead imports

**Conclusion:** JavaScript/TypeScript import structure is excellent. No fixes required.

---

## 5. CI Workflow Wiring (100% Valid)

### Summary
- **Workflows Analyzed:** 8 YAML files
- **Script References:** 11 total
- **Valid References:** 11 (100%) ✓
- **Broken References:** 0 ✓

### 5.1 Workflow → Tool/Script Mapping

| Workflow | Referenced Scripts | Status |
|----------|-------------------|--------|
| **ci.yml** | requirements-dev.txt, requirements.txt | ✓ EXIST |
| **ci-evidence-bundle.yml** | scripts/evidence_bundle.sh | ✓ EXISTS |
| **ci-policy-lint.yml** | policies/gate_policy_v1.json | ✓ EXISTS |
| **deepjump-ci.yml** | deepjump-audit.reusable.yml | ✓ EXISTS |
| **deepjump-audit.reusable.yml** | tools/verify_pointers.py, tools/receipt_lint.py, tools/claim_lint.py | ✓ ALL EXIST |
| **metatron-guard.yml** | tools/metatron_check.py, docs/guards/metatron_rule.md | ✓ BOTH EXIST |
| **test.yml** | Fractalsense/requirements-dev.txt, npm scripts | ✓ ALL EXIST |
| **ci-smoke.yml** | requirements-dev.txt | ✓ EXISTS |

### 5.2 Tool Dependency Verification

**All 11 tool references valid:**
- ✓ `tools/verify_pointers.py`
- ✓ `tools/receipt_lint.py`
- ✓ `tools/claim_lint.py`
- ✓ `tools/metatron_check.py`
- ✓ `tools/status_emit.py` (via make target)
- ✓ `tools/status_verify.py` (via make target)
- ✓ `tools/snapshot_guard.py` (via make target)
- ✓ `scripts/evidence_bundle.sh`
- ✓ `policies/gate_policy_v1.json`
- ✓ `docs/guards/metatron_rule.md`
- ✓ `.github/workflows/deepjump-audit.reusable.yml`

### 5.3 Makefile Integration

**CI workflows reference Makefile targets:**
- `make verify` → Valid (runs port-lint, test, verify-pointers, claim-lint)
- `make test` → Valid (runs pytest -v)
- `make lint` → Valid (runs ruff check)

**All Makefile targets verified in PHASE0_ORIENTATION.md**

**Conclusion:** CI wiring is solid. No breakages detected.

---

## 6. Docs ↔ Code References (100% Valid)

### Summary
- **Docs Checked:** ~30 files with command references
- **Commands Referenced:** ~30
- **Broken Commands:** 0 ✓
- **Outdated Commands:** 0 ✓

### 6.1 Command Reference Validation

| Doc File | Commands | Status |
|----------|----------|--------|
| `README.md` | `./scripts/nightly.sh`, `make verify` | ✓ EXIST |
| `docs/devops_tooling_kit.md` | `make verify-json`, `python tools/snapshot_guard.py` | ✓ EXIST |
| `docs/devops_tooling_kit_annex.md` | `make verify-json` | ✓ EXIST |
| `docs/bio_spiral_viewer.md` | `python -m bio_spiral_viewer` | ✓ VALID |
| `docs/START_HERE.md` | `pytest` | ✓ VALID |
| `docs/voids/MOD_16_hessian_void_analysis.md` | `pytest tests/stability/ -v` | ✓ VALID |

### 6.2 Script Existence Check

**Referenced in docs:**
- ✓ `scripts/nightly.sh` (exists, simple pytest wrapper)
- ✓ `tools/snapshot_guard.py` (exists)
- ✓ `tools/status_emit.py` (exists)
- ✓ `tools/verify_pointers.py` (exists)

### 6.3 Makefile Target References

**All documented make targets exist:**
- ✓ `make verify`
- ✓ `make verify-json`
- ✓ `make test`
- ✓ `make all`
- ✓ `make deepjump`

**Conclusion:** Documentation accurately reflects codebase commands.

---

## 7. Overall Connectivity Graph

### High-Level Architecture

```
GOLD Layer (index/, policies/, VOIDMAP.yml)
  │
  ├─→ VOIDMAP.yml
  │    ├─→ policies/gateproof_v1.yaml ✗ MISSING
  │    ├─→ docs/sensors/* ✗ MISSING (2 files)
  │    └─→ tools/port_lint.py ✓
  │
  ├─→ index/COMPACT_INDEX_v3.yaml
  │    ├─→ modules/MOD_6_RECEIPTS_CORE.yaml ✓
  │    └─→ modules/MOD_15_STATS_TESTS.yaml ✓
  │
  └─→ policies/
       ├─→ gate_policy_v1.json ✓
       └─→ port_codebooks.yaml ✓

ANNEX Layer (src/, tools/, tests/)
  │
  ├─→ src/ → All imports valid ✓
  │
  ├─→ tools/ (8 DeepJump tools)
  │    └─→ All CI references valid ✓
  │
  ├─→ tests/ → Mostly valid
  │    └─→ Fractalsense/test_resonance.py ✗ BROKEN
  │
  └─→ ui-app/ → All imports valid ✓

CI/CD Layer (.github/workflows/)
  │
  └─→ 8 workflows → All references valid ✓

Documentation Layer (docs/, README.md)
  │
  ├─→ 66+ markdown links → All valid ✓
  └─→ Command references → All valid ✓
```

---

## 8. Risk Assessment

### Critical Risks (Immediate Action Required)

1. **Python Import Failures (2)**
   - `Fractalsense/test_resonance.py` → ModuleNotFoundError
   - `Fractalsense/tests/unit/test_sound_generator.py` → Context-dependent failure
   - **Impact:** Tests will fail, code won't run
   - **Severity:** HIGH
   - **Effort to fix:** 30 minutes

2. **Missing Governance Files (3)**
   - `policies/gateproof_v1.yaml` → VOID-012 blocked
   - `docs/sensors/bom.md` → VOID-013 blocked
   - `spec/sensors.spec.json` → VOID-013 blocked
   - **Impact:** VOIDMAP integrity, governance incomplete
   - **Severity:** MEDIUM-HIGH
   - **Effort to fix:** 2-4 hours (requires design)

### Medium Risks (Should Fix)

3. **Import Style Inconsistencies (5 files)**
   - Implicit relative imports in Fractalsense
   - sys.path manipulation in tests
   - **Impact:** Code fragility, maintainability
   - **Severity:** MEDIUM
   - **Effort to fix:** 1 hour

### Low Risks (Nice to Have)

4. **Directory Name with Space**
   - `pdf canvas/` → Can break shell scripts
   - **Impact:** Script compatibility
   - **Severity:** LOW
   - **Effort to fix:** 5 minutes (rename + update references)

---

## 9. Connectivity Metrics

### Pointer Density (References per file)

| File Type | Avg Pointers/File | Max Pointers | Most Connected File |
|-----------|-------------------|--------------|---------------------|
| YAML (index) | 5.2 | 14 | index/ENTAENGELMENT_INDEX_v3_FUNCTORIAL.yaml |
| Markdown (docs) | 2.3 | 16 | docs/canvas_links.md |
| Python (src) | 4.1 | 12 | src/core/metrics.py |
| Workflows (.github) | 3.8 | 8 | .github/workflows/ci.yml |

### Reference Depth (How many hops to reach a file)

| File | Depth | Incoming References |
|------|-------|---------------------|
| `VOIDMAP.yml` | 0 (root) | 3 references |
| `index/COMPACT_INDEX_v3.yaml` | 0 (root) | 4 references |
| `tools/verify_pointers.py` | 1 | 6 references (most referenced tool) |
| `docs/masterindex.md` | 1 | 4 references |

**Average reference depth:** 1.4 hops (GOOD - shallow hierarchy)

---

## 10. Recommendations

### Immediate (This Week)
1. **Fix Python import breakages** (2 critical issues)
2. **Create missing governance files** (3 files)
3. **Verify test suite passes** after fixes

### Short-Term (This Month)
4. **Refactor Fractalsense imports** (5 files with style issues)
5. **Consider renaming `pdf canvas/`** to `pdf-canvas` or `pdf_canvas`
6. **Add import linting** to CI (eslint-plugin-import for JS)

### Long-Term (This Quarter)
7. **Document connectivity expectations** in CONTRIBUTING.md
8. **Add pointer validation** to pre-commit hooks
9. **Create connectivity dashboard** (visualize reference graph)

---

**Phase 1 Complete.** See `CONNECTIVITY_FIXLIST.md` for prioritized action items.
