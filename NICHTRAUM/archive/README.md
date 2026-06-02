# NICHTRAUM/archive — Archived Artifacts

Per **G3 (Deletion-Verbot)**: nothing is deleted, only moved here with a reason.

## npm lockfiles (archived 2026-06-02)

- `root_package-lock.json` — was `/package-lock.json`
- `ui-app_package-lock.json` — was `/ui-app/package-lock.json`

**Reason:** The repository adopted **pnpm + Turborepo** as the JS/TS workspace
manager (see `SYNTHBIOSIS.md`). These historical npm lockfiles are no longer
active. The single active lockfile is the root **`pnpm-lock.yaml`**, which
Turborepo relies on for reproducible builds and dependency-graph inference.

They are retained here for provenance and reversibility only — do not restore
them while pnpm is the active package manager.
