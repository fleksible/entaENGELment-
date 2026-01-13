# Start Here

A practical quickstart for newcomers to the entaENGELment Framework.

---

## What is this?

**entaENGELment** is a hardened kernel for embodied human-AI interaction with physically-enforced resonance. It provides:

- **Stability analysis** via Hessian eigenvalue classification
- **Consent-gated actions** with cryptographic audit trails
- **Ethics-first design** with fail-safe mechanisms

If the README feels dense, that's intentional - it's a reference document. This file is your on-ramp.

---

## Quick Setup

```bash
# Clone
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

Expected output: `76 passed` (or more as the project grows).

---

## Project Structure (the essentials)

```
entaENGELment-/
├── src/
│   ├── core/           # Metrics, consent logic, resonance engine
│   └── stability/      # Hessian analysis, spectral taxonomy, gate guards
├── tools/              # CLI utilities (status, snapshot, MZM gate)
├── tests/              # Unit, integration, and ethics tests
├── index/              # Functorial Index (the "source of truth")
└── docs/               # You are here
```

---

## Key Concepts (minimal version)

| Concept | What it means | Where to look |
|---------|---------------|---------------|
| **Stability** | Classifies points as STABLE/FLAT/UNSTABLE via Hessian eigenvalues | `src/stability/` |
| **Consent** | Actions in FLAT zones require explicit consent | `src/core/metrics.py` |
| **Gate** | MOD_14 decides ALLOW/BLOCK based on stability + consent | `src/stability/stability_guard.py` |
| **Receipts** | Every decision is HMAC-signed for audit | `tools/status_emit.py` |

---

## First Steps

1. **Run the tests** to verify your setup works
2. **Read `src/stability/__init__.py`** to see the core exports
3. **Explore `tests/unit/`** to understand expected behavior
4. **Check `docs/masterindex.md`** for the full documentation map

---

## Getting Help

- Open an issue: https://github.com/fleksible/entaENGELment-/issues
- Read the architecture: `docs/architecture.md`
- Browse the voids: `docs/voids/` (design decisions and edge cases)

---

*This document is additive - it doesn't replace the README, just offers a gentler entry point.*

---

## Orbital Meta-Structure
- [Orbital Model](./ORBIT_MODEL.md)
- [Orbital Roadmap](./ROADMAP_ORBITAL_v1.md)
- [BridgeCard — Consent as Transit](./bridgecards/BC_consent_as_transit.md)
- [Validation Demo v1](./validation/VALIDATION_DEMO_v1.md)
