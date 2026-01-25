# CONNECTIVITY FIX LIST - Prioritized Action Items
**Audit Date:** 2026-01-24
**Total Issues:** 10 (2 critical, 3 high, 5 medium)
**Estimated Total Effort:** 4-6 hours

---

## Priority 1: CRITICAL (Runtime Blockers) - 30 min

### Issue #1.1: Dead Module Import in test_resonance.py
**File:** `Fractalsense/test_resonance.py:26-28`
**Severity:** CRITICAL (ModuleNotFoundError)
**Impact:** Test file cannot run
**Effort:** 15 minutes

**Current Code:**
```python
from modules.resonance_enhancer import ResonanceEnhancerModule
from modules.resonance_enhancer.sound_generator import SoundGenerator
from modules.resonance_enhancer.color_generator import ColorGenerator
```

**Problem:** `modules/` directory doesn't exist

**Fix Option A (Quick - Remove unused imports):**
```python
# Remove these lines if ResonanceEnhancerModule is not actually used
from sound_generator import SoundGenerator
from color_generator import ColorGenerator
```

**Fix Option B (Proper - Create module structure):**
```bash
# If the module structure is needed:
mkdir -p Fractalsense/modules/resonance_enhancer
touch Fractalsense/modules/__init__.py
touch Fractalsense/modules/resonance_enhancer/__init__.py
# Then move/create appropriate files
```

**Verification:**
```bash
python -c "import sys; sys.path.insert(0, 'Fractalsense'); import test_resonance"
```

**Rollback:** Git revert commit

---

### Issue #1.2: Directory-Dependent Import in test_sound_generator.py
**File:** `Fractalsense/tests/unit/test_sound_generator.py:26`
**Severity:** CRITICAL (Context-dependent failure)
**Impact:** Tests break depending on how pytest is invoked
**Effort:** 15 minutes

**Current Code:**
```python
from tests.conftest import get_dominant_frequency
```

**Problem:** Only works when pytest run from specific directory

**Fix:**
```python
# Replace absolute import with relative import
from ..conftest import get_dominant_frequency
```

**Verification:**
```bash
cd Fractalsense
python -m pytest tests/unit/test_sound_generator.py -v
```

**Rollback:** Git revert commit

---

## Priority 2: HIGH (Governance Blockers) - 2-4 hours

### Issue #2.1: Missing GateProof Governance File
**File:** `policies/gateproof_v1.yaml` (MISSING)
**Severity:** HIGH (Blocks VOID-012 closure)
**Impact:** Governance checklist incomplete, no testable gate transition criteria
**Effort:** 2-3 hours (requires design + review)

**Referenced By:**
- `VOIDMAP.yml:116` (VOID-012 closing path)

**What It Should Contain:**
Based on VOID-012 description: "Keine einheitliche, testbare Checkliste für latent→manifest Übergänge"

```yaml
version: "1.0"
description: "GateProof Checklist for latent→manifest transitions"

checklist:
  governance:
    - id: GP-001
      check: "Consent obtained and documented"
      required: true
      evidence: "receipt with consent_timestamp"

    - id: GP-002
      check: "HMAC signature valid"
      required: true
      verification: "tools/status_verify.py"

    - id: GP-003
      check: "All pointers verified"
      required: true
      verification: "make verify-pointers"

    - id: GP-004
      check: "Claim lint passes"
      required: true
      verification: "make claim-lint"

    - id: GP-005
      check: "Port-Matrix K0..K4 validated"
      required: true
      verification: "make port-lint"

  ethics:
    - id: GP-E01
      check: "Negative ethics tests pass"
      required: true
      test_path: "tests/ethics/"

    - id: GP-E02
      check: "No expired consent used"
      required: true
      test_file: "tests/ethics/T3_fail_safe_expired_consent.py"

  technical:
    - id: GP-T01
      check: "Snapshot manifest generated"
      required: true
      artifact: "out/snapshot_manifest.json"

    - id: GP-T02
      check: "Status receipt valid"
      required: true
      artifact: "out/status/deepjump_status.json"

transitions:
  latent_to_manifest:
    trigger: "User consent + context validation"
    guards:
      - "All governance checks pass"
      - "All ethics checks pass"
      - "All technical checks pass"
    outcome:
      success: "Transition allowed, receipt generated"
      failure: "Transition blocked, log reason"
```

**Creation Steps:**
1. Review VOID-012 requirements in VOIDMAP.yml
2. Draft gateproof_v1.yaml based on template above
3. Add tests in `tests/ethics/` to validate checklist
4. Update VOIDMAP.yml evidence field
5. Run `make verify` to test integration

**Verification:**
```bash
# Validate YAML
python -m yaml policies/gateproof_v1.yaml

# Update VOIDMAP.yml:
# evidence: "policies/gateproof_v1.yaml"

# Verify pointer
python tools/verify_pointers.py --strict
```

**Rollback:** Delete file, revert VOIDMAP.yml changes

---

### Issue #2.2: Missing Sensor Architecture Documentation
**Files:**
- `docs/sensors/bom.md` (MISSING)
- `spec/sensors.spec.json` (MISSING)

**Severity:** HIGH (Blocks VOID-013 closure)
**Impact:** Sensor architecture void cannot be closed
**Effort:** 1-2 hours (requires research + documentation)

**Referenced By:**
- `VOIDMAP.yml:130` (VOID-013 closing path)

**What They Should Contain:**

**docs/sensors/bom.md** (Bill of Materials):
```markdown
# Sensor Architecture - Bill of Materials

> **Safety Notice:** This is a components-level overview only.
> No operational lab instructions or risky assembly procedures.

## Overview
Component specifications for potential sensor layer implementation.

## Core Components

### 1. Biosignal Acquisition
- **Component:** OpenBCI Cyton Board or similar
- **Specs:** 8-channel EEG, 250Hz sampling
- **Interface:** USB/Bluetooth
- **Rationale:** Open-source, research-grade biosignal capture

### 2. Environmental Sensors
- **Component:** BME680 (Bosch)
- **Specs:** Temperature, humidity, pressure, gas
- **Interface:** I2C
- **Rationale:** Multi-modal environmental context

### 3. Processing Unit
- **Component:** Raspberry Pi 4 or equivalent
- **Specs:** 4GB RAM minimum
- **Interface:** GPIO, USB, Ethernet
- **Rationale:** Edge processing, Python support

## Integration Protocol
See `spec/sensors.spec.json` for data format and communication protocol.

## References
- OpenBCI Documentation: https://docs.openbci.com
- BME680 Datasheet: (Bosch official)
```

**spec/sensors.spec.json** (Specification):
```json
{
  "version": "1.0",
  "title": "Sensor Layer Specification",
  "description": "Communication protocol and data format for sensor layer",
  "protocol": {
    "transport": "MQTT or HTTP/REST",
    "encoding": "JSON",
    "rate": "1Hz baseline, 250Hz for biosignals"
  },
  "data_format": {
    "sensor_reading": {
      "timestamp": "ISO8601 string",
      "sensor_id": "string (unique identifier)",
      "modality": "string (eeg|environmental|motion)",
      "values": "object (modality-specific)",
      "metadata": {
        "sampling_rate": "number (Hz)",
        "units": "object (key: channel, value: unit string)"
      }
    }
  },
  "biosignal_channels": {
    "eeg": ["Fp1", "Fp2", "C3", "C4", "P3", "P4", "O1", "O2"],
    "sampling_rate": 250
  },
  "environmental": {
    "temperature": {"unit": "celsius", "range": [0, 50]},
    "humidity": {"unit": "percent", "range": [0, 100]},
    "pressure": {"unit": "hPa", "range": [300, 1100]}
  },
  "safety": {
    "note": "This is a data specification only. Hardware assembly requires qualified supervision."
  }
}
```

**Creation Steps:**
1. Create `docs/sensors/` directory
2. Write `bom.md` with component-level overview
3. Write `spec/sensors.spec.json` with data format
4. Update VOIDMAP.yml evidence field
5. Verify with `make verify-pointers`

**Verification:**
```bash
mkdir -p docs/sensors
# Create files as above
python tools/verify_pointers.py --strict
python -m json.tool spec/sensors.spec.json  # Validate JSON
```

**Rollback:** Delete directory and files, revert VOIDMAP.yml

---

## Priority 3: MEDIUM (Code Quality) - 1-2 hours

### Issue #3.1: Implicit Relative Imports in Fractalsense
**Files:**
- `Fractalsense/__init__.py:25`
- `Fractalsense/integration.py:13, 87, 107, 136, 164`

**Severity:** MEDIUM (Deprecated style, potential future breakage)
**Impact:** PEP 8 non-compliance, implicit behavior
**Effort:** 30 minutes

**Current Pattern:**
```python
from modular_app_structure import ModuleInterface
```

**Fix:**
```python
from .modular_app_structure import ModuleInterface
```

**Bulk Fix Script:**
```bash
# In Fractalsense/ directory
sed -i 's/^from modular_app_structure/from .modular_app_structure/g' __init__.py integration.py
```

**Verification:**
```bash
cd Fractalsense
python -c "import __init__"
python -c "import integration"
```

**Files to Update:**
1. `Fractalsense/__init__.py` (1 occurrence)
2. `Fractalsense/integration.py` (5 occurrences)

**Rollback:** Git revert commit

---

### Issue #3.2: sys.path Manipulation in Tests
**Files:**
- `Fractalsense/tests/conftest.py`
- `Fractalsense/tests/unit/test_color_generator.py`
- `Fractalsense/tests/unit/test_modular_app_structure.py`

**Severity:** MEDIUM (Fragile, environment-dependent)
**Impact:** Tests may break in CI or different environments
**Effort:** 30-60 minutes

**Current Pattern:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from color_generator import ColorGenerator
```

**Fix (Option A - Relative imports):**
```python
from ...color_generator import ColorGenerator
```

**Fix (Option B - Package installation):**
```bash
# Install Fractalsense as editable package
pip install -e .
# Then use absolute imports
from Fractalsense.color_generator import ColorGenerator
```

**Recommended:** Option A (simpler, no install needed)

**Files to Update:**
- `Fractalsense/tests/conftest.py`
- `Fractalsense/tests/unit/test_color_generator.py`
- `Fractalsense/tests/unit/test_modular_app_structure.py`

**Verification:**
```bash
cd Fractalsense
python -m pytest tests/ -v
```

**Rollback:** Git revert commit

---

### Issue #3.3: Directory Name with Space
**Directory:** `pdf canvas/`
**Severity:** MEDIUM (Potential shell script breakage)
**Impact:** Scripts that don't quote paths may fail
**Effort:** 5 minutes

**Current Name:** `pdf canvas/`
**Proposed Name:** `pdf_canvas/` or `pdf-canvas/`

**Fix:**
```bash
# Rename directory
mv "pdf canvas" pdf_canvas

# Update any references (if any)
grep -r "pdf canvas" --include="*.py" --include="*.md" --include="*.sh"
# (If references found, update them)
```

**Verification:**
```bash
# Ensure directory accessible without quotes
ls pdf_canvas/
```

**References to Check:**
- Likely none (directory appears to be standalone)
- But verify with grep first

**Rollback:** `mv pdf_canvas "pdf canvas"`

---

## Priority 4: LOW (Future Improvements) - Optional

### Issue #4.1: Add Import Linting to CI
**Severity:** LOW (Preventive)
**Impact:** Catch future import issues early
**Effort:** 30 minutes

**Add to `.github/workflows/ci.yml`:**
```yaml
- name: Lint JavaScript imports
  run: |
    cd ui-app
    npm install eslint eslint-plugin-import --save-dev
    npx eslint --ext .ts,.tsx --plugin import .
```

**Add to `pyproject.toml`:**
```toml
[tool.ruff.lint]
select = [
  "E", "W", "F", "I", "B", "C4", "UP",
  "TID",  # flake8-tidy-imports (add this)
]
```

---

### Issue #4.2: Document Connectivity Expectations
**Severity:** LOW (Documentation)
**Impact:** Help contributors maintain connectivity
**Effort:** 1 hour

**Add section to `CONTRIBUTING.md`:**
```markdown
## Connectivity Guidelines

When adding new files:
1. Update relevant index files (index/COMPACT_INDEX_v3.yaml)
2. Add links from documentation (README.md, docs/)
3. Verify pointers with `make verify-pointers`
4. Use relative imports in Python packages
5. Use `@/` path alias in TypeScript (ui-app)
```

---

## Summary Table

| Priority | Issue | File(s) | Effort | Impact | Verification |
|----------|-------|---------|--------|--------|--------------|
| **P1** | Dead module import | test_resonance.py | 15m | Runtime error | `python -c "import test_resonance"` |
| **P1** | Directory-dependent import | test_sound_generator.py | 15m | Test failure | `pytest tests/unit/test_sound_generator.py` |
| **P2** | Missing gateproof | policies/gateproof_v1.yaml | 2-3h | VOID-012 blocked | `make verify-pointers` |
| **P2** | Missing sensor docs | docs/sensors/*.md, spec/*.json | 1-2h | VOID-013 blocked | `make verify-pointers` |
| **P3** | Implicit imports | Fractalsense/*.py (6 files) | 30m | PEP 8 compliance | `python -c "import Fractalsense"` |
| **P3** | sys.path manipulation | Fractalsense/tests/*.py (3 files) | 30-60m | Test fragility | `pytest Fractalsense/tests/` |
| **P3** | Directory name with space | pdf canvas/ | 5m | Script compatibility | `ls pdf_canvas/` |
| **P4** | Import linting | CI config | 30m | Prevention | CI passes |
| **P4** | Connectivity docs | CONTRIBUTING.md | 1h | Guidance | N/A |

---

## Recommended Execution Order

### Week 1 (Critical + High Priority)
1. **Day 1:** Fix Python import breakages (30m)
   - Issue #1.1: test_resonance.py
   - Issue #1.2: test_sound_generator.py
   - Run `pytest` to verify

2. **Day 2-3:** Create missing governance files (3-4h)
   - Issue #2.1: policies/gateproof_v1.yaml
   - Issue #2.2: docs/sensors/* + spec/sensors.spec.json
   - Update VOIDMAP.yml evidence fields
   - Run `make verify-pointers`

### Week 2 (Medium Priority)
3. **Day 1:** Fix import style issues (1-1.5h)
   - Issue #3.1: Implicit relative imports
   - Issue #3.2: sys.path manipulation
   - Issue #3.3: Rename directory
   - Run full test suite

### Week 3+ (Optional)
4. **Ongoing:** Add preventive measures
   - Issue #4.1: Import linting in CI
   - Issue #4.2: Documentation updates

---

## Verification Checklist

After completing all fixes:

```bash
# 1. Verify Python imports
cd Fractalsense
python -m pytest tests/ -v

# 2. Verify pointers
cd ..
make verify-pointers

# 3. Run full test suite
make test

# 4. Verify VOIDMAP integrity
python tools/verify_pointers.py --strict

# 5. Check CI simulation
make all  # Full DeepJump flow

# 6. Verify JavaScript (if ui-app touched)
cd ui-app
npm run build
npm run test
```

---

## Risk Mitigation

### Before Starting
1. Create feature branch: `git checkout -b audit/connectivity-fixes`
2. Commit after each fix (atomic commits)
3. Run verification after each commit

### During Work
- Test each fix independently
- Don't batch multiple fixes in one commit
- Keep rollback plan ready (git revert)

### After Completion
- Run full test suite
- Check CI passes
- Create PR with detailed changelog
- Request review before merging

---

**Total Estimated Effort:** 4-6 hours (P1 + P2 + P3)
**Critical Path:** 30 minutes (P1 only)
**High-Value Path:** 3-4 hours (P1 + P2)
