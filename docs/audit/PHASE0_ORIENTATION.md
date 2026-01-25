# PHASE 0: ORIENTATION REPORT
**Audit Date:** 2026-01-24
**Auditor:** Claude Code (Senior Staff Engineer)
**Repo:** entaENGELment- (fleksible/entaENGELment-)
**Branch:** claude/repo-audit-improvements-wMcLO
**Focus:** Connectivity, Performance, Ergonomics

---

## Executive Summary

**EntaENGELment** is a hardened kernel framework for human-AI interaction with cryptographic audit trails. It implements a "DeepJump Protocol" with HMAC-signed receipts, pointer verification, and strict snapshot validation.

**Languages:** Mixed Python/JavaScript (86 .py files, 45 .js/.ts files)
**Build System:** Make-based with pytest/jest
**CI/CD:** GitHub Actions (8 workflows)
**Core Principle:** "Index = Gold, Code = Annex" (pointer-based architecture)

---

## 1. Repository Map

### 1.1 Top-Level Structure (38 directories)

```
entaENGELment-/
├── .claude/                    # House rules (CLAUDE.md enforcement)
├── .github/workflows/          # CI: 8 YAML workflows
├── Fractalsense/               # Python visualization module (584K)
├── docs/audit/                 # Versioned audit reports and outputs
├── Plugins/                    # Plugin system
├── TASKS/                      # Task definitions
├── __tests__/                  # Jest JavaScript tests
├── adapters/                   # Adapter layer (MSI, etc.)
├── aggregates/                 # Aggregate modules
├── ark/                        # Ark subsystem
├── audit/                      # Audit trails & reports (100K)
├── bio_spiral_viewer/          # Console bio-spiral visualization
├── dashboard/                  # Dashboard UI
├── data/                       # Data files
├── diagrams/                   # Architecture diagrams
├── docs/                       # Documentation (161K, largest doc dir)
├── index/                      # GOLD: Master index (Functorial v3)
├── ledger/                     # Ledger subsystem
├── lyra/                       # Lyra subsystem
├── mapping/                    # Tensor mapping YAMLs
├── overlay/                    # Overlay modules
├── pdf canvas/                 # PDF canvas rendering (225K)
├── policies/                   # GOLD: Policy definitions
├── receipts/                   # IMMUTABLE: Signed receipts
├── reports/                    # Generated reports
├── runbooks/                   # Operational runbooks
├── schedules/                  # Scheduling configs
├── scripts/                    # Build/deploy scripts
├── seeds/                      # GOLD: Seed files for snapshot
├── spec/                       # GOLD: Spec files (JSON schemas)
├── src/                        # Python source code (57K)
├── tests/                      # Pytest tests (86K)
├── tickets/                    # Ticket tracking
├── tools/                      # DeepJump tools (58K)
├── ui-app/                     # Next.js UI app (389K)
└── VOIDMAP.yml                 # GOLD: Void registry
```

### 1.2 Language Breakdown

| Language | Files | Key Dirs |
|----------|-------|----------|
| **Python** | 86 | `src/`, `tools/`, `tests/`, `Fractalsense/` |
| **JavaScript/TypeScript** | 45 | `ui-app/`, `__tests__/`, `bio_spiral_viewer/` |
| **YAML/JSON** | ~60 | `index/`, `policies/`, `spec/`, `.github/workflows/` |
| **Markdown** | ~50 | `docs/`, `audit/`, `runbooks/` |

### 1.3 Entry Points

| Type | File/Command | Purpose |
|------|--------------|---------|
| **Build** | `Makefile` | 20+ targets (install, test, lint, verify, deepjump) |
| **Python** | `pyproject.toml` | Package metadata, pytest/black/ruff config |
| **Node** | `package.json` | Jest tests, Electron app |
| **Setup** | `setup.py` | Legacy Python setup (minimal) |
| **CI Main** | `.github/workflows/ci.yml` | Main CI pipeline (5194 bytes, largest) |

---

## 2. Build & Test Commands

### 2.1 Makefile Targets (Verified)

```makefile
# Setup
make install           # pip install -e .
make install-dev       # pip install dev deps + package

# Testing
make test              # pytest -v
make test-unit         # pytest tests/unit/ -v
make test-integration  # pytest tests/integration/ -v
make test-ethics       # pytest tests/ethics/ -v
make coverage          # pytest --cov --cov-report=html

# Code Quality
make lint              # ruff check src/ tools/ tests/
make port-lint         # python3 tools/port_lint.py (K0..K4)
make format            # black src/ tools/ tests/
make type-check        # mypy src/ tools/

# DeepJump Protocol v1.2 (CORE VERIFICATION)
make verify            # port-lint + test + verify-pointers + claim-lint
make verify-pointers   # python3 tools/verify_pointers.py --strict
make claim-lint        # python3 tools/claim_lint.py --scope index,spec,receipts,tools
make status            # python3 tools/status_emit.py (HMAC receipt)
make snapshot          # python3 tools/snapshot_guard.py (strict manifest)
make all               # verify + test + snapshot (FULL FLOW)
make deepjump          # alias for 'make all'

# Gate Policy
make gate-test         # Test gate toggle with various inputs

# Cleanup
make clean             # Remove build artifacts
```

### 2.2 NPM Scripts (package.json)

```json
"test": "npm run test:js && npm run test:py"
"test:js": "jest"
"test:js:watch": "jest --watch"
"test:js:coverage": "jest --coverage"
"test:py": "cd Fractalsense && python -m pytest"
"test:py:coverage": "cd Fractalsense && python -m pytest --cov"
"start": "electron ."
"dist": "electron-builder"
```

---

## 3. CI/CD Workflows (.github/workflows/)

| Workflow | Lines | Purpose |
|----------|-------|---------|
| **ci.yml** | 5194 | Main CI pipeline |
| **metatron-guard.yml** | 4528 | Metatron G4 focus-switch detection |
| **deepjump-audit.reusable.yml** | 2557 | Reusable deepjump audit |
| **test.yml** | 2346 | Test runner |
| **ci-smoke.yml** | 864 | Smoke tests |
| **deepjump-ci.yml** | 445 | DeepJump CI integration |
| **ci-policy-lint.yml** | 378 | Policy linting |
| **ci-evidence-bundle.yml** | 281 | Evidence bundling |

**Total:** 8 workflows, ~16KB of CI code

---

## 4. Existing Guardrails

### 4.1 DeepJump Protocol Tools (tools/)

| Tool | Purpose | Status |
|------|---------|--------|
| `verify_pointers.py` | Check dead pointers in index/modules | ✓ Active |
| `claim_lint.py` | Detect untagged claims in artifacts | ✓ Active |
| `status_emit.py` | Emit HMAC-signed status receipt | ✓ Active |
| `status_verify.py` | Verify HMAC status receipt | ✓ Active |
| `snapshot_guard.py` | Generate strict snapshot manifest | ✓ Active |
| `port_lint.py` | Port-Matrix linter (K0..K4) | ✓ Active |

### 4.2 Linters & Formatters

- **Python:** ruff (check), black (format), mypy (type check)
- **Config:** pyproject.toml (line-length=100, target=py39+)
- **JavaScript:** jest (test framework)

### 4.3 House Rules (CLAUDE.md)

| Guard | Rule | Enforcement |
|-------|------|-------------|
| **G0** | Consent & Boundary | Plan-first workflow |
| **G1** | Annex Principle | GOLD (index/, policies/, VOIDMAP.yml) read-only |
| **G2** | Nichtraum Protection | Don't optimize NICHTRAUM/ |
| **G3** | Deletion Prohibition | Move to NICHTRAUM/archive/, never delete |
| **G4** | Metatron Rule | Focus ≠ Attention, detect focus-switch |
| **G5** | Prompt Injection Defense | External content = untrusted |
| **G6** | Verify Before Merge | Tests must pass, report to docs/audit/ |

**CI Integration:** metatron-guard.yml workflow enforces G4

---

## 5. Core vs Annex Classification

### 5.1 GOLD (Immutable without explicit permission)

```
index/                          # Functorial Index v3
  ├── COMPACT_INDEX_v3.yaml
  ├── ENTAENGELMENT_INDEX_v3_FUNCTORIAL.yaml
  └── modules/*.yaml

policies/                       # Policy definitions
spec/                          # JSON schemas
seeds/                         # Snapshot seeds
VOIDMAP.yml                    # Void registry
```

### 5.2 IMMUTABLE (Never modify)

```
receipts/                      # HMAC-signed receipts
data/receipts/                 # (if exists)
```

### 5.3 ANNEX (Modifiable after plan)

```
src/                           # Python source
tools/                         # Utility scripts
tests/                         # Test code
docs/                          # Documentation (except negations.md)
ui-app/                        # Next.js UI
Fractalsense/                  # Visualization module
scripts/                       # Build/deploy scripts
adapters/                      # Adapter layer
aggregates/                    # Aggregate modules
... (all other dirs)
```

---

## 6. VOIDMAP Analysis (Open Gaps)

| ID | Title | Status | Priority | Domain |
|----|-------|--------|----------|--------|
| VOID-002 | CI Pipeline Integration | OPEN | high | [DEV] |
| VOID-003 | Status Emit Receipt Format | OPEN | medium | [DEV] |
| VOID-010 | Taxonomie & Spektren | OPEN | high | [PHYS] |
| VOID-011 | Resonanz Metrics (MI, PLV, FD) | OPEN | high | [MATH] |
| VOID-012 | GateProof Checkliste | OPEN | critical | [DEV] |
| VOID-013 | Sensor-Architektur | OPEN | medium | [DEV] |
| VOID-014 | Protein-Design | OPEN | medium | [BIO] |
| VOID-023 | MICRO/MESO/MACRO Tagging | OPEN | low | [EXPLAIN] |

**Closed:** VOID-001, VOID-020, VOID-021, VOID-022 (DeepJump + Port-Matrix suite)

---

## 7. Previous Audit Artifacts (audit/)

Existing audit reports found (100K total):
- `DEEP_AUDIT_REPORT_20260117.md`
- `STRUCTURE_MAP.md`
- `WORKFLOW_AUDIT.md`
- `VERIFY_MATRIX.md`
- `INVENTORY.md`
- `MISSING_FILES.md`
- `DUPLICATES.md`
- `METATRON_COMPLIANCE_BACKLOG.md`
- `dependency_audit_2026-01-05.md`
- `port_matrix_audit_2026-01-13.md`

**Note:** Repo has been audited multiple times; build on existing findings.

---

## 8. Key Risks & Observations

### 8.1 Strengths
- ✅ Well-defined governance (CLAUDE.md house rules)
- ✅ DeepJump Protocol with verification tools
- ✅ HMAC-signed audit trail
- ✅ Comprehensive Makefile with clear targets
- ✅ Mixed language support (Python/JS)
- ✅ CI/CD integration (8 workflows)

### 8.2 Potential Issues (To investigate in Phase 1-3)
- ⚠️ Directory name with space: `pdf canvas/` (breaks shell scripts)
- ⚠️ VOID-002: CI pipeline doesn't run full verify/status/snapshot
- ⚠️ Multiple index files: `COMPACT_INDEX_v3.yaml` vs `ENTAENGELMENT_INDEX_v3_FUNCTORIAL.yaml`
- ⚠️ Legacy files: `setup.py` (minimal), `requirements.txt` vs `pyproject.toml`
- ⚠️ No `NICHTRAUM/` directory visible (referenced in G2, G3)
- ⚠️ `metrics` file is 1 byte (empty?)
- ⚠️ Large npm lockfile (279K)

---

## 9. Next Steps (Phase 1)

**FOCUS:** Connectivity Matrix (MUST DO)

1. **Markdown Links:** Check all internal file links, anchors, relative paths
2. **YAML/JSON Pointers:** Validate in-repo references (index/, policies/, spec/)
3. **Python Imports:** Dead modules, circular imports, missing __init__.py
4. **JavaScript Imports:** ES6/CommonJS import validity
5. **CI Wiring:** Workflows referencing moved/missing scripts/paths
6. **Docs ↔ Code:** Commands in docs that no longer exist

**Deliverables:**
- `docs/audit/CONNECTIVITY_MAP.md` (graph + breakages)
- `docs/audit/CONNECTIVITY_FIXLIST.md` (ranked by impact)

---

**Phase 0 Complete.** Ready for deep connectivity analysis.
