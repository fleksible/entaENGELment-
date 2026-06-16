# CI Workflow Map

[FACT] This map documents the repository's GitHub Actions workflows, their minimum token permissions, and their top-level concurrency guard.

## Guard contract

Each workflow should declare explicit `permissions` and a top-level `concurrency` block.

Default read-only template:

```yaml
permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Exception: `release.yml` keeps `contents: write` because it creates GitHub Releases from version tags.

## Workflows

| Workflow file | Purpose | Permissions | Concurrency |
|---------------|---------|-------------|-------------|
| `.github/workflows/ci.yml` | Legacy/advisory CI plus non-PR verify/build/security/gate-policy jobs | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-evidence-bundle.yml` | Evidence bundle generation | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-js-workspace.yml` | JS/TS workspace membrane: frozen pnpm install plus Turbo typecheck/lint/build for UI/package changes | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-policy-lint.yml` | Policy JSON lint | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-smoke.yml` | Python smoke tests | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/deepjump-audit.reusable.yml` | Reusable DeepJump audit core | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/deepjump-ci.yml` | DeepJump verify/lint plus reusable audit call | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/metatron-guard.yml` | FOKUS marker advisory guard for PRs/branch pushes | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/release.yml` | Release gate and GitHub Release creation | `contents: write` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/sbom.yml` | SBOM generation and artifact upload | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/test.yml` | JavaScript, Python, and UI build tests | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/void-sync.yml` | Scheduled VOID deadline monitoring and issue creation | `contents: read`, `issues: write` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |

## Maintenance rule

[FACT] New workflows must document any permission broader than `contents: read` in this file. The reason should be action-specific, not symbolic or implied.

[FACT] `make workflow-posture-check` (`tools/workflow_posture_check.py`) verifies this contract locally: every workflow must declare explicit `permissions` and a `concurrency` block with `cancel-in-progress: true`, and any permission broader than `contents: read` must be named in this file. The check is read-only and deterministic.
