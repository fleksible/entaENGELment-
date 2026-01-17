# Nachträgliche FOKUS-Dokumentation

**Erstellt:** 2026-01-17
**Grund:** G4 Metatron-Regel wurde nachträglich eingeführt

---

## Anmerkung

Die folgenden Commits wurden vor Einführung der Metatron-Regel erstellt
und enthalten keinen FOKUS-Marker. Eine retrospektive Dokumentation
ist optional, da die Regel prospektiv gilt.

**Empfehlung:** Merge-Commits von der FOKUS-Prüfung ausnehmen.

---

## Commits ohne FOKUS (nach Kategorie)

### Merge-Commits (ausnehmen)

- 928601a: Merge pull request #54 (fractalsense-ui-integration)
- 23aca0c: Merge pull request #53 (entaengelment-ui-prototype)
- b4d165a: Merge pull request #52 (fix-ci-pipeline)
- 1ad52f9: Merge pull request #50 (fix-commits-workflow)
- c0e1085: Merge pull request #49 (fix-commits-workflow)
- fa0a749: Merge pull request #47 (port-matrix-update)
- a47ee4b: Merge pull request #46 (orbital-meta-structure)
- c0ce733: Merge pull request #45 (receipt-v1_1-metrics-bands)
- df910b1: Merge pull request #44 (receipt-policy-privacy)
- 36d035a: Merge pull request #43 (apply-patch-validate)

### Feature-Commits (FOKUS rekonstruierbar)

| Hash | Message | FOKUS (rekonstruiert) |
|------|---------|----------------------|
| 32c757a | feat(ui): integrate Fractalsense module | UI-Integration |
| 946223d | Trigger CI rebuild with pygame | CI-Fix |
| 9e2e54b | feat(ui): add EntaENGELment UI prototype | UI-Prototype |
| 929f2a8 | feat: add Claude Code guard artifacts | Guard-Setup |
| f9d8d57 | feat(receipts): resonance receipt v1.1 | Receipt-Schema |

### Fix-Commits

| Hash | Message | FOKUS (rekonstruiert) |
|------|---------|----------------------|
| 650e171 | fix(metatron_check): require question | Metatron-Check-Fix |
| 4a3989c | fix(metatron_check): type hints | Python-3.9-Compat |
| e563076 | fix(port_lint): Python 3.10+ keyword | Python-3.9-Compat |
| 45503ad | fix(workflows): CI/CD cleanup | CI-Workflow-Fix |
| 938dae2 | fix(receipts): REJECTED flow | Receipt-Fix |

---

## Vollständige Liste

Siehe: `audit/metatron_violations.txt` (47 Einträge)

---

## Empfehlung für CI

```yaml
# In .github/workflows/deepjump-ci.yml hinzufügen:

- name: Check FOKUS marker
  run: |
    # Skip merge commits
    if git log -1 --format=%s | grep -q "^Merge"; then
      echo "Merge commit - FOKUS check skipped"
      exit 0
    fi
    
    # Check for FOKUS marker
    if ! git log -1 --format=%B | grep -q "FOKUS:"; then
      echo "::error::Commit muss FOKUS: Marker enthalten"
      exit 1
    fi
```

