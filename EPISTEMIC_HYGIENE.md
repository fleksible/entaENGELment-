# EPISTEMIC_HYGIENE.md — Naming, Claim-Tagging & Safe Extension

> Rules for keeping the workspace legible and error-free as it grows.
> ANNEX document; subordinate to `CLAUDE.md` and `.claude/rules/*` (guards win).

---

## 1. Claim-Tagging

When documenting an architectural decision (in PRs, ADRs, comments, reports),
tag the *epistemic status* of each non-trivial claim so facts are not confused
with guesses. This mirrors the discipline enforced by `tools/claim_lint.py`.

| Tag | Meaning | Example |
|-----|---------|---------|
| **[FACT]** | Verifiable from code/types/build output | `[FACT] @enta/types is type-only (no runtime exports).` |
| **[MODEL]** | An architectural pattern/decision | `[MODEL] Domain types live once, in @enta/types.` |
| **[HYPOTHESIS]** | A DX/perf expectation, not yet measured | `[HYPOTHESIS] Turbo caching cuts CI typecheck time.` |
| **[METAPHOR]** | Domain symbolism, non-literal | `[METAPHOR] Each package is a sovereign cell.` |

Rule: never let a **[HYPOTHESIS]** or **[METAPHOR]** masquerade as a **[FACT]**
in something that gates a merge.

---

## 2. Naming Conventions

- **Internal packages:** scoped `@enta/*`, `"private": true`, `version` `0.0.0`.
  The scope marks "internal ANNEX building block, never an npm artifact".
- **Package directory = unscoped name** under `packages/` (`packages/types` →
  `@enta/types`). Apps live at their historical paths (`ui-app`).
- **Exports are the contract:** every package declares an explicit `exports`
  map. Consumers import only declared subpaths — never deep relative paths into
  another package's internals.
- **TS files:** `kebab-case.ts` for modules, `PascalCase.tsx` for React
  components (matches existing `ui-app` convention).

---

## 3. TypeScript Baseline

- **[FACT]** The workspace targets **TypeScript 6**, treated as the *stable
  bridge baseline*. TypeScript 6.0 is an official transition release toward
  TS 7 / the native compiler.
- **TS 7 / native-compiler adoption is explicitly OUT OF SCOPE** for the
  monorepo-membrane work. Do not bundle a compiler migration into membrane PRs.
- Shared strictness lives in `tsconfig.base.json`. New packages extend
  `@enta/tsconfig/base.json` and inherit it (including
  `noUncheckedIndexedAccess`).
- **Known deferral:** `ui-app` currently relaxes `noUncheckedIndexedAccess`
  (legacy code predates it) via `@enta/tsconfig/nextjs.json`. Flipping it to
  `true` after migrating ui-app's array accesses is a tracked roadmap item.

---

## 4. Safe Extension — Adding a Package

A checklist that keeps additions error-free and CEI-positive (see
`SYNTHBIOSIS.md` §4):

1. **Justify the boundary.** Does this encode a genuinely shared contract? If it
   only serves one app, it belongs *in* that app.
2. `packages/<name>/package.json`: scoped `@enta/<name>`, `"private": true`,
   explicit `exports`, and scripts matching the Turbo task names you want it to
   participate in (`typecheck`, optionally `build`, `lint`, `test`). A package
   without the matching script is silently skipped by Turbo.
3. Extend `@enta/tsconfig/base.json` (or `nextjs.json` for Next apps).
4. **Keep the graph acyclic and leaf-ward.** Shared packages must not depend on
   apps. No cycles.
5. **Type-only stays type-only** unless you deliberately add runtime values —
   then update consumers' `transpilePackages`.
6. Run `pnpm turbo run typecheck lint build` before committing.

---

## 5. Boundaries That Must Not Be Crossed (recap of guards)

- **GOLD** (`index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/`): read-only.
  `@enta/types` *mirrors* the VOIDMAP schema; it never edits it.
- **IMMUTABLE** receipts (`data/receipts/`, `receipts/`, `ark/`): append-only.
- **Python core**: sovereign; the JS workspace does not gate or rewrite it.
- **Deletion (G3):** move to `NICHTRAUM/archive/` with a reason; never delete.

---

*See also: `SYNTHBIOSIS.md`, `diagrams/monorepo-topology.md`, `CLAUDE.md`.*
