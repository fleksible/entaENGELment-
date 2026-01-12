# Adiabatic Bandwidth Shaping v0.1

## Overview

Adiabatic bandwidth shaping dynamically adjusts system capacity based on resonance quality and heat accumulation. This approach prevents abrupt transitions (adiabatic = "no sudden heat exchange") while maintaining responsive throttling.

## Core Principles

1. **Gradual Adaptation**: Bandwidth changes smoothly to avoid system shock
2. **Heat-Based Feedback**: Rejections accumulate "heat" that reduces capacity
3. **Quality-Weighted Recovery**: High-quality resonances accelerate cooling
4. **Reversible Throttling**: System can recover to full capacity over time

## Mathematical Model

### Bandwidth Update

```
B_new = B0 + (B_current - B0) * exp(-k * dt) + BW_norm * weights
```

Where:
- `B0`: Baseline bandwidth (initial capacity)
- `B_current`: Current bandwidth capacity
- `k`: Decay/recovery constant
- `dt`: Time delta since last update
- `BW_norm`: Normalized bandwidth metric from current request
- `weights`: Quality-based weighting factors

### Normalized Bandwidth Metric

```
BW_norm = w_omega * omega_norm + w_kenosis * kenosis_norm + w_phi * phi_norm
```

Where:
- `w_omega`, `w_kenosis`, `w_phi`: Weights (sum to 1.0)
- Normalized metrics scaled to [0, 1] range

### Heat Accumulation

```
heat_new = heat_current * exp(-alpha * dt) + heat_injection
```

Where:
- `heat_current`: Current accumulated heat
- `alpha`: Cooling exponent (higher = faster cooling)
- `dt`: Time delta
- `heat_injection`: Heat added by current rejection (if any)

Heat injection rules:
- `REJECTED`: +1.0 heat
- `REFLECTED`: +0.5 heat
- `COOLED`: +0.2 heat
- `TUNNEL_GRANTED`: 0 heat (only natural cooling)

### Capacity Reduction from Heat

```
B_effective = B_current * max(0, 1 - heat / heat_capacity)
```

Where:
- `heat_capacity`: Maximum heat before full throttle (e.g., 10.0)
- Effective bandwidth decreases linearly with heat

## Constants (Policy-Pinned)

Reference values from `receipt_policy_v0_1.yaml`:

```yaml
bandwidth_shaping:
  B0: 1.0                    # Baseline bandwidth
  BW0: 0.5                   # Initial normalized bandwidth
  k: 0.1                     # Decay constant (1/s)
  alpha: 0.05                # Cooling exponent (1/s)
  heat_capacity: 10.0        # Max heat tolerance
  weights:
    w_omega: 0.4
    w_kenosis: 0.3
    w_phi: 0.3
```

## Decision Flow Integration

The bandwidth shaping integrates with gate decisions:

```
1. Compute BW_norm from incoming metrics
2. Update heat based on time + previous decision
3. Compute B_effective from current bandwidth & heat
4. Check: if BW_norm < bandwidth_min -> COOLED
5. Otherwise proceed to policy checks
```

## Privacy & Normalization

- All metrics normalized to [0, 1] before bandwidth computation
- No raw user identifiers included in bandwidth calculations
- Heat and bandwidth state persisted per-session (not per-user)

## Grade 3 Margins

Grade 3 (high-security) operations apply stricter margins:

```yaml
grade3_margins:
  omega_margin: 0.15
  kenosis_margin: 0.10
  phi_margin: 0.10
  bandwidth_margin: 0.20
```

Effective thresholds for grade 3:
- `omega_max_grade3 = omega_max * (1 - omega_margin)`
- `bandwidth_min_grade3 = bandwidth_min * (1 + bandwidth_margin)`

## Implementation Notes

1. **Timestamp Precision**: Use millisecond-resolution timestamps for `dt` calculations
2. **Exponential Decay**: Use `exp()` for smooth transitions
3. **Bounds Checking**: Ensure `B_effective >= 0` and `heat >= 0`
4. **Genesis State**: Initial receipts start with `B0`, `BW0`, `heat=0`

## References

- Receipt Policy v0.1: `docs/specs/receipt_policy_v0_1.yaml`
- Resonance Receipt Schema v1.1: `spec/resonance_receipt_v1_1.schema.json`
- Canonical Serialization: RFC8785 (JCS)
