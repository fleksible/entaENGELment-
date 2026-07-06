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

## uv.lock (archived 2026-07-06)

- `uv.lock` — was `/uv.lock`

**Reason:** The Python domain builds via **setuptools + pip** (`pyproject.toml`,
`requirements*.txt`); no CI/build step references `uv`. The committed `uv.lock`
(~390 KB) was a stale, unused second lockfile that could silently drift from the
active dependency set. Archived for provenance; restore only if the project
formally adopts `uv`.

## Fractalsense build artifacts (archived 2026-07-06)

- `fractalsense/*.zip` (4 files) — were `Fractalsense/*.zip`
- `fractalsense/*.min.js` (5 files) — were `Fractalsense/*.min.js`

**Reason:** The `.zip` files are packaged build outputs and the `.min.js` files
are minified bundles with **zero inbound references** (`Fractalsense/index.html`
loads the non-minified `app.js`; Jest coverage explicitly excludes `*.min.js`).
Generated/minified artifacts do not belong in version control. The
human-readable sources (`*.js`) remain in `Fractalsense/`. Restore only if a
no-build deploy of the minified bundles is reintroduced.
