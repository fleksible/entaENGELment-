# Repository Structure Map

**Audit Session:** audit-2026-01-18-SDbnU
**Total Files:** 1,548
**Total Directories:** ~60

---

## Directory Taxonomy

### GOLD Tier (Immutable/Protected)

| Directory | Purpose | Files | G-Rule |
|-----------|---------|-------|--------|
| `index/` | Functorial Index v3 - Source of Truth for Claims | ~20 | G1:GOLD |
| `policies/` | Gate policies, codebooks, governance rules | ~10 | G1:GOLD |
| `VOIDMAP.yml` | Gap registry, void tracking | 1 | G1:GOLD |
| `data/receipts/` | HMAC-signed audit receipts (IMMUTABLE) | ~5 | G1:IMMUTABLE |
| `receipts/` | Legacy receipts path | ~5 | G1:IMMUTABLE |
| `spec/` | Specification files (cglg, eci, grammophon) | ~5 | G1:GOLD |
| `seeds/` | Strict seeds for snapshot | ~3 | G1:GOLD |

### ANNEX Tier (Modifiable with Plan)

| Directory | Purpose | Files | Status |
|-----------|---------|-------|--------|
| `src/` | Core Python modules (metrics, ledger, gate logic) | ~30 | Active |
| `src/core/` | Core metrics (eci.py, metrics.py, ledger.py) | ~10 | Active |
| `src/cglg/` | Consensual Gate Logic | ~5 | Active |
| `tools/` | DeepJump tooling (status_emit, port_lint, etc.) | ~15 | Active |
| `tests/` | Test suites (unit, integration, ethics, cpt) | ~40 | Active |
| `docs/` | Documentation (masterindex, specs, guards) | ~50 | Semi-protected |
| `scripts/` | Build/deploy scripts, evidence bundle | ~10 | Active |
| `ui-app/` | Next.js UI application | ~100 | Active |
| `Fractalsense/` | Fractal visualization module | ~30 | Active |
| `__tests__/` | JavaScript Jest tests | ~15 | Active |
| `adapters/` | External adapters (MSI) | ~5 | Active |
| `Plugins/` | Plugin system (SynthosiaCore) | ~10 | Active |
| `bio_spiral_viewer/` | Bio-spiral console viewer | ~5 | Active |
| `dashboard/` | Dashboard UI components | ~5 | Active |
| `lyra/` | Lyra subsystem | ~5 | Active |
| `overlay/` | Overlay modules and pins | ~10 | Active |
| `aggregates/` | Aggregate modules | ~5 | Active |
| `reports/` | Generated audit reports | ~10 | Output |
| `tickets/` | Task tickets | ~5 | Active |
| `schedules/` | Time schedules | ~5 | Active |
| `runbooks/` | Operational runbooks | ~5 | Active |
| `diagrams/` | Architectural diagrams | ~10 | Active |

### Meta/Config Tier

| Directory | Purpose | Files |
|-----------|---------|-------|
| `.claude/` | Claude Code rules and skills | ~10 |
| `.github/workflows/` | CI/CD workflows | ~5 |
| `OUT/` | Generated outputs | ~5 |
| `TASKS/` | Active task definitions | ~3 |
| `audit/` | Audit artifacts (this audit) | ~10 |

---

## Source of Truth Documents

| Document | Path | Purpose |
|----------|------|---------|
| **Primary Index** | `index/COMPACT_INDEX_v3.yaml` | Functorial pointer registry |
| **Void Registry** | `VOIDMAP.yml` | Open gaps tracking |
| **Master Index** | `docs/masterindex.md` | Navigation hub |
| **Gate Policy** | `policies/gate_policy_v1.json` | Governance rules |
| **Port Codebooks** | `policies/port_codebooks.yaml` | Port semantics |
| **README** | `README.md` | Entry point & overview |

---

## Key Architecture Files

### Core Python Package

```
src/
├── core/
│   ├── __init__.py
│   ├── eci.py           # Ethical Consent Index
│   ├── metrics.py       # Core5 metrics implementation
│   └── ledger.py        # Receipt ledger
├── cglg/
│   └── gate.py          # Consensual Gate Logic
├── stability/
│   └── __init__.py      # Stability checks
└── meta_backprop.py     # Policy evolution
```

### DeepJump Tools

```
tools/
├── status_emit.py       # HMAC status emission
├── status_verify.py     # Status verification
├── snapshot_guard.py    # Snapshot integrity
├── port_lint.py         # Port matrix linter
├── claim_lint.py        # Claim validator
├── verify_pointers.py   # Pointer verification
├── metatron_check.py    # Metatron guard check
└── mzm/
    ├── __init__.py
    └── gate_toggle.py   # MZM gate control
```

### UI Application (Next.js)

```
ui-app/
├── app/                 # Next.js app router
├── components/          # React components
│   └── fractalsense/    # Fractalsense UI
├── lib/                 # Shared libraries
├── public/              # Static assets
└── package.json         # Node dependencies
```

---

## File Type Distribution

| Type | Count | Example Extensions |
|------|-------|-------------------|
| Python | ~200 | .py |
| TypeScript/JavaScript | ~150 | .ts, .tsx, .js |
| Markdown | ~100 | .md |
| YAML | ~50 | .yaml, .yml |
| JSON | ~30 | .json |
| Other Config | ~20 | .toml, .cfg |
| Shell | ~10 | .sh |

---

## Cross-Reference Map

### Pointer Chains

```
README.md → index/COMPACT_INDEX_v3.yaml
         → spec/*.spec.json
         → src/core/metrics.py
         → tools/status_emit.py

VOIDMAP.yml → docs/voids/*.md
            → receipts/*_closure.json

index/modules/*.yaml → src/**/*.py
                     → policies/*.json
```

### Dependency Graph (Python)

```
src/core/ledger.py
  └── uses: hashlib, json
  └── imports: src/core/metrics.py

tools/status_emit.py
  └── uses: hmac, hashlib
  └── outputs: receipts/*.json

tools/port_lint.py
  └── reads: policies/port_codebooks.yaml
  └── validates: src/**/*.py
```

---

## Observations

1. **Clear GOLD/ANNEX separation** enforced via CLAUDE.md
2. **Pointer-based architecture** - claims have evidence paths
3. **Multi-language stack** - Python (core) + TypeScript (UI)
4. **Heavy documentation** - ~100 markdown files
5. **Test coverage areas**: unit, integration, ethics, CPT
6. **VOID tracking** - systematic gap management via VOIDMAP.yml
