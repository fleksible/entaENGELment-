# SYNTHBIOSIS.md — Architecture Axioms of the EntaENGELment Workspace

> The monorepo as a synthbiotic organism: many sovereign cells, one membrane.
> This document defines the structural axioms of the JS/TS workspace and how it
> coexists with the Python domain and the GOLD governance core.

---

## 0. Relationship to the House Rules

`SYNTHBIOSIS.md` is **ANNEX** (changeable after plan). It does **not** override
`CLAUDE.md` or `.claude/rules/*`. Where this document and the guards (G0–G6)
could appear to conflict, **the guards win**. This file only describes the
*shape* of the workspace; the guards govern *what may change and how*.

---

## 1. The Three Sovereign Domains

The repository is **polyglot**. It is not, and will not be forced into, a single
language tree. Three domains coexist:

| Domain | Paths | Tooling | Status |
|--------|-------|---------|--------|
| **JS/TS membrane** | `ui-app/`, `packages/*` | pnpm + Turborepo + TS | ANNEX |
| **Python core** | `src/`, `tools/`, `tests/`, `bio_spiral_viewer/`, `Fractalsense/*.py` | `pyproject.toml` + uv | ANNEX (sovereign) |
| **Governance GOLD** | `index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/`, receipts | read-only | GOLD / IMMUTABLE |

**Axiom S1 — Sovereignty:** Each domain owns its own toolchain, lockfile, and
test runner. The JS/TS workspace does **not** absorb, rewrite, or gate the
Python core, and neither touches GOLD.

---

## 2. Additive Membrane Principle

**Axiom S2 — Additivity:** The monorepo membrane is introduced *additively*.
Existing directories are not relocated; the workspace is layered over them via
`pnpm-workspace.yaml` globs (`ui-app`, `packages/*`). Restructuring (moving
`ui-app`/`Fractalsense` into `apps/`) is a **future** decision requiring its own
consent, not a precondition of the membrane.

**Axiom S3 — No deletion (G3):** Superseded artifacts (e.g. npm lockfiles) are
moved to `NICHTRAUM/archive/` with a reason, never deleted.

---

## 3. Package Topology & Arché

Each package has an **Arché** — an unchangeable core identity — and communicates
through a calibrated boundary (its `exports`).

| Package | Arché | Boundary |
|---------|-------|----------|
| `@enta/tsconfig` | The shared compiler covenant | `./base.json`, `./nextjs.json` |
| `@enta/types` | Single source of truth for domain types (mirrors `VOIDMAP.yml`) | type-only `.` export |
| `entaengelment-ui` (`ui-app`) | The human-facing window onto the system | a Next.js app (leaf consumer) |

**Axiom S4 — Single source of truth:** Domain types (`Void`, `VoidMap`, `Guard`,
`FocusState`, …) live exactly once, in `@enta/types`. They mirror the GOLD
`VOIDMAP.yml` schema as a **read-only consumer** — editing `@enta/types` never
edits GOLD. UI code imports them via `@/types`, which re-exports the package.

**Axiom S5 — Type-only until proven otherwise:** `@enta/types` carries no runtime
values. If runtime constants/validators are ever added, consumers must declare
`transpilePackages: ["@enta/types"]`. This keeps the boundary cheap and the
coupling minimal.

---

## 4. CEI — Connection Efficiency Index

We replace vague "cohesion" talk with a directional preference, the **CEI**:

> **CEI = (useful shared relations) / (parasitic coupling)** — maximize it.

Concretely:

- **Raise the numerator:** extract genuinely shared contracts (types, configs)
  into leaf packages with explicit `exports`. (Done: `@enta/types`,
  `@enta/tsconfig`.)
- **Lower the denominator:** no deep cross-package relative imports; no app
  importing another app; shared packages stay dependency-light and acyclic.

**Axiom S6 — Acyclic, leaf-heavy graph:** Dependencies flow *toward* leaves
(`ui-app → @enta/types → @enta/tsconfig`). Shared packages must never depend on
apps.

---

## 5. Reproducibility

**Axiom S7 — Tools in the lockfile, not the air:** Build tooling (`turbo`) is a
pinned root devDependency; the package manager is pinned via `packageManager`
(`pnpm@10.33.0`). CI installs with `--frozen-lockfile`. Reproducibility is part
of the receipt chain, not the ambient environment.

**Axiom S8 — One active lockfile:** `pnpm-lock.yaml` at the root is the single
source of dependency truth for the JS/TS domain.

---

## 6. What This Architecture Is Now

A polyglot system with a thin, typed, cache-aware JS/TS **membrane** wrapped
around a sovereign Python core and an untouched GOLD governance center. The
membrane shares one compiler covenant and one type-topology, builds through a
single Turbo graph, and grows by *adding leaves* — never by dissolving the cells
it connects.

---

*See also: `EPISTEMIC_HYGIENE.md` (naming, claim-tagging, safe extension),
`diagrams/monorepo-topology.md` (topology graph), `CLAUDE.md` (the guards).*
