# Missing Files & Broken References Report

**Audit Session:** audit-2026-01-18-SDbnU
**Scan Date:** 2026-01-18

---

## Summary

| Category | Count | Severity |
|----------|-------|----------|
| Broken internal links | 5 | Medium |
| Missing referenced files | 5 | Low-Medium |
| Orphan workflow references | 0 | - |

---

## Broken Internal References

### 1. VOIDMAP.yml

| Line | Reference | Status | Recommendation |
|------|-----------|--------|----------------|
| 19 | `docs/voids_backlog.md` | **MISSING** | Create file or remove reference |
| 130 | `docs/sensors/bom.md` | **MISSING** | Part of VOID-013, create stub |
| 130 | `spec/sensors.spec.json` | **MISSING** | Part of VOID-013, create stub |

**Context:** These references are part of VOID-013 "Sensor-Architektur" which is still OPEN. The closing_path specifies these files should be created.

### 2. docs/masterindex.md

| Line | Reference | Status | Recommendation |
|------|-----------|--------|----------------|
| 79 | `src/tools/kolibri.py` | **MISSING** | Not implemented yet |
| 100 | `diagrams/threefold_apex.svg` | **MISSING** | Marked as "geplant" (planned) |

**Context:** These are forward references to planned features.

---

## Verified Workflow Files

All referenced workflow files exist:

| File | Referenced From | Status |
|------|-----------------|--------|
| `.github/workflows/ci.yml` | Multiple docs | ✓ EXISTS |
| `.github/workflows/ci-smoke.yml` | INVENTORY.md | ✓ EXISTS |
| `.github/workflows/deepjump-ci.yml` | README.md, docs | ✓ EXISTS |
| `.github/workflows/metatron-guard.yml` | metatron_rule.md | ✓ EXISTS |
| `.github/workflows/ci-evidence-bundle.yml` | REPOSITORY_ESSENZ | ✓ EXISTS |
| `.github/workflows/ci-policy-lint.yml` | REPOSITORY_ESSENZ | ✓ EXISTS |
| `.github/workflows/test.yml` | - | ✓ EXISTS |

---

## README.md Link Verification

All 11 links in README.md verified:

| Reference | Status |
|-----------|--------|
| `spec/cglg.spec.json` | ✓ |
| `src/core/metrics.py` | ✓ |
| `index/modules/MOD_6_RECEIPTS_CORE.yaml` | ✓ |
| `tools/status_emit.py` | ✓ |
| `tools/snapshot_guard.py` | ✓ |
| `Makefile` | ✓ |
| `docs/masterindex.md` | ✓ |
| `policies/gate_policy_v1.json` | ✓ |
| `index/COMPACT_INDEX_v3.yaml` | ✓ |
| `LICENSE` | ✓ |
| `CODEOWNERS` | ✓ |

---

## Recommendations

### Quick Fixes (P2)

1. **Create `docs/voids_backlog.md`**
   - Simple auto-generated file from VOIDMAP.yml
   - Or update VOIDMAP.yml to remove this metadata field

2. **Add placeholder for planned items**
   - Create `diagrams/threefold_apex.svg` placeholder
   - Or mark reference clearly as "[PLANNED]" in masterindex.md

### Deferred (P3 - Part of VOID closure)

3. **VOID-013 artifacts** when that void is addressed:
   - `docs/sensors/bom.md`
   - `spec/sensors.spec.json`

4. **KOLIBRI module** when implemented:
   - `src/tools/kolibri.py`

---

## Verification Commands Used

```bash
# Check if file exists
test -f <path> && echo "EXISTS" || echo "MISSING"

# Grep for markdown links
grep -rn '\]\(./' --include="*.md" .

# Grep for yaml paths
grep -rn 'path:' --include="*.yaml" --include="*.yml" .
```
