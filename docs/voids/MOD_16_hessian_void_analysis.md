# MOD_16: Hessian Void Analysis

**Status:** ✅ IMPLEMENTED
**Version:** 1.0.0
**Depends on:** NumPy
**Used by:** MOD_14 (Guards), MOD_18 (Taxonomy), MOD_19 (Cost)

---

## Übersicht

MOD_16 implementiert Stabilitäts-Klassifizierung via Hessian-Eigenwertanalyse. Der Hessian (Matrix der zweiten Ableitungen) charakterisiert die lokale Krümmung eines Energiefunktionals und ermöglicht die Erkennung von:

- **STABLE**: Lokales Minimum (sicher)
- **FLAT**: Flache Richtung (VOID - Consent erforderlich)
- **UNSTABLE**: Sattelpunkt (unsicher - blockieren)

---

## Mathematische Grundlage

### Energiefunktional (Ginzburg-Landau-Style)

```
E[ψ] = ∫ [α|ψ|² + β|ψ|⁴ + γ|∇ψ|²] dx
```

### Stationarität (1. Variation)

```
δE/δψ* = 0  →  -γ∇²ψ + αψ + 2β|ψ|²ψ = 0
```

### Stabilität (2. Variation = Hessian)

```
H_ij = δ²E / δψ_i δψ_j*

Stabil ⇔ H positive definit ⇔ alle λ(H) > 0
```

---

## Void-Typen (3-Klassen)

| Typ | Eigenwert-Muster | Physikalisch | Governance |
|-----|------------------|--------------|------------|
| **STABLE** | λ > 0 (alle) | Attraktor | ✅ SAFE |
| **FLAT** | λ ≈ 0 (mind. 1) | Neutral, Drift | ⚠️ VOID |
| **UNSTABLE** | λ < 0 (mind. 1) | Repeller | ❌ UNSAFE |

### FLAT als kritischer VOID-Zustand

- **Mathematisch:** Flache Richtung im Energiefunktional
- **Physikalisch:** Goldstone-Mode, spontane Symmetriebrechung
- **Governance:** Unbestimmtheit → Consent/Human-Review nötig

---

## API

### `compute_hessian_numerical(func, point, eps=1e-5)`

Berechnet numerische Hessian-Approximation via finite Differenzen.

```python
from src.stability.hessian_void import compute_hessian_numerical
import numpy as np

def energy(x):
    return x[0]**2 + x[1]**2

H = compute_hessian_numerical(energy, np.array([0.0, 0.0]))
# H ≈ [[2, 0], [0, 2]]
```

### `classify_stability(hessian, threshold=1e-6)`

Klassifiziert Stabilitätstyp und gibt Eigenwerte zurück.

```python
from src.stability.hessian_void import classify_stability

status, eigvals = classify_stability(H)
# status = 'STABLE', eigvals = [2.0, 2.0]
```

### `detect_void_type(hessian)`

Vereinfachte Void-Typ-Erkennung (lowercase).

```python
from src.stability.hessian_void import detect_void_type

void_type = detect_void_type(H)  # 'stable', 'flat', oder 'unstable'
```

---

## Governance-Integration (MOD_14)

### `stability_gate(hessian, consent_available=False)`

Safety-Gate basierend auf Hessian-Stabilität.

```python
from src.core.stability_guard import stability_gate
import numpy as np

# FLAT ohne Consent → blockiert
flat_H = np.array([[1.0, 0.0], [0.0, 1e-8]])
allow, reason = stability_gate(flat_H, consent_available=False)
# allow=False, reason="FLAT: VOID detected, consent required"

# Mit Consent → erlaubt
allow, reason = stability_gate(flat_H, consent_available=True)
# allow=True
```

### Fail-Safe-Logik

```
STABLE  → Proceed (kein Consent nötig)
FLAT    → Block ohne Consent, Proceed mit Consent
UNSTABLE → Block immer (auch mit Consent)
```

---

## Tests

```bash
# Alle MOD_16 Tests
pytest tests/stability/ -v

# Spezifische Tests
pytest tests/stability/test_hessian_void.py -v
pytest tests/stability/test_stability_guard.py -v
```

### Test-Abdeckung

| Test | Funktion | Erwartung |
|------|----------|-----------|
| `test_stable_minimum` | f(x,y) = x² + y² | STABLE |
| `test_flat_direction_void` | f(x,y) = x² | FLAT |
| `test_saddle_unstable` | f(x,y) = x² - y² | UNSTABLE |
| `test_flat_requires_consent` | Governance | Block ohne Consent |

---

## Erweiterungen (Post-MOD_16)

### MOD_18: Spektrale Taxonomie

Erweitert 3-Klassen auf 7-Klassen via detaillierte Eigenwert-Muster.

### MOD_19: Minimum Work Distance

Cost-Metrik via Hessian-Geodäsik.

### Unreal Integration

```cpp
UFUNCTION(BlueprintCallable)
FStabilityStatus AnalyzeHessian(const TArray<float>& HessianFlat);
```

---

## Changelog

- **v1.0.0** (2026-01-04): Initial implementation
  - Numerische Hessian-Berechnung
  - 3-Klassen-Stabilitätsklassifizierung
  - Governance-Integration (Consent-Gate)
