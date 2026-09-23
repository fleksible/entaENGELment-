# Technical Start Here — Die Werkstatt

Diese Seite beginnt dort, wo du beschlossen hast, das Repository **wirklich lokal auszuführen**.

Wenn du nur lesen, stöbern oder die Grundidee verstehen möchtest, brauchst du nichts von dem hier. Geh einfach zurück zu [`WELCOME.md`](../WELCOME.md).

Wenn du jetzt freiwillig `git clone` lesen möchtest: willkommen in der Werkstatt.

---

## Was ist das hier technisch?

**entaENGELment** ist ein experimentelles Framework mit Consent-Gates, Audit-Mechanismen, Tests, Stabilitätsmodellen und mehreren Forschungs-/UI-Schichten.

Die technischen Modelle sind Implementationen und Forschungsproxies. Sie sind keine Diagnose einer Person und kein empirischer Beweis der symbolischen oder narrativen Schichten.

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

Expected output: the test run finishes without failures. The exact count grows with the project and is not a release guarantee.

---

## Project Structure (the essentials)

```text
entaENGELment-/
├── src/
│   ├── core/           # Metrics, consent logic, resonance engine
│   └── stability/      # Hessian analysis, spectral taxonomy, gate guards
├── tools/              # CLI utilities (status, snapshot, MZM gate)
├── tests/              # Unit, integration, and ethics tests
├── index/              # Functorial Index (protected / GOLD)
└── docs/               # Documentation, specs, audits, intake
```

---

## Key Concepts (minimal version)

| Concept | What it means | Where to look |
|---------|---------------|---------------|
| **Stability** | Classifies model states via Hessian eigenvalue analysis | `src/stability/` |
| **Consent** | Explicit boundary condition for guarded actions | `src/core/` and governance docs |
| **Gate** | Allows, holds or blocks operations under declared rules | `src/stability/`, `src/core/` |
| **Receipts** | Auditable records for selected state transitions and evidence flows | `tools/`, `data/receipts/` |

---

## First Steps

1. **Run the tests** to verify your setup works.
2. **Read `CLAUDE.md`** before structural changes; it contains the repository guards.
3. **Explore `tests/unit/`** to see expected behavior.
4. **Check `docs/masterindex.md`** for the deeper documentation map.
5. **Use `make verify`** before proposing a merge.

---

## If GitHub itself is the unfamiliar part

You do not need to learn every GitHub concept at once.

A useful first approximation:

- **Repository** — the shared place where project files and their history live.
- **Issue** — a place to ask, report or discuss something.
- **Branch** — a temporary line of work that does not have to change the main version yet.
- **Pull Request (PR)** — an invitation to review a proposed change before it is merged.
- **Commit** — a named snapshot of a change.

That is enough vocabulary to begin. The rest can arrive when it becomes useful.

---

## Getting Help

- Open an issue if something is unclear or broken.
- Read [`WELCOME.md`](../WELCOME.md) for the non-technical entrance.
- Read [`docs/masterindex.md`](masterindex.md) for the documentation map.
- Browse [`docs/audit/`](audit/) to see how changes are reviewed.
- Browse the VOID-related docs for deliberately unresolved questions.

A question is a valid contribution even when it does not come with a fix.

---

## Orbital Meta-Structure

- [Orbital Model](./ORBIT_MODEL.md)
- [Orbital Roadmap](./ROADMAP_ORBITAL_v1.md)
- [BridgeCard — Consent as Transit](./bridgecards/BC_consent_as_transit.md)
- [Validation Demo v1](./validation/VALIDATION_DEMO_v1.md)
