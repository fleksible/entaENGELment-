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

Exception: `release.yml` keeps top-level `contents: read`; only its
`create-release` job receives `contents: write`, because that job creates a
GitHub Release from a version tag.

The checker reads the following exact exception contract. A filename mention
outside this block does not authorize a broader or different scope.

<!-- workflow-posture-permissions
release.yml:
  jobs:
    create-release:
      contents: write
void-sync.yml:
  workflow:
    contents: read
    issues: write
-->

## Workflows

| Workflow file | Purpose | Permissions | Concurrency |
|---------------|---------|-------------|-------------|
| `.github/workflows/ci.yml` | Legacy/advisory CI plus non-PR verify/build/security/gate-policy jobs | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-evidence-bundle.yml` | Evidence bundle generation | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-js-workspace.yml` | JS/TS workspace membrane: frozen pnpm install plus Turbo typecheck/lint/build for UI/package changes | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-policy-lint.yml` | Policy JSON lint | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/ci-smoke.yml` | Python smoke tests | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/deepjump-audit.reusable.yml` | Reusable DeepJump audit core; HMAC secret is step-scoped and missing keys fail trusted runs | `contents: read` | literal `deepjump-audit-reusable-${{ github.ref }}`, cancel in progress |
| `.github/workflows/deepjump-ci.yml` | DeepJump verify/lint plus separate reusable audit calls: PRs pass no secrets mapping; trusted events pass only `ENTA_HMAC_SECRET` | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/metatron-guard.yml` | FOKUS marker advisory guard for PRs/branch pushes | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/release.yml` | Release gate and GitHub Release creation | top-level `contents: read`; `create-release` job: `contents: write` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/sbom.yml` | Fail-closed Python environment SBOM generation and artifact upload | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/test.yml` | JavaScript, Python, and UI build tests | `contents: read` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |
| `.github/workflows/void-sync.yml` | Scheduled VOID deadline monitoring and issue creation | `contents: read`, `issues: write` | `${{ github.workflow }}-${{ github.ref }}`, cancel in progress |

## Maintenance rule

[FACT] New workflows must document any permission broader than `contents: read`
in the machine-readable exception contract above. The exact workflow/job scope
and permission mapping must match; a filename mention alone grants nothing.
Exceptions without a currently matching broad permission are rejected as stale.

[FACT] `make workflow-posture-check` (`tools/workflow_posture_check.py`) verifies
this contract locally. Every workflow must declare explicit `permissions` and
`concurrency` with `cancel-in-progress: true`; broader top-level or job
permissions must be named here. External actions must use full commit SHAs.
Checked-in composite actions are followed recursively so they cannot hide a
mutable external reference. Executable shell bodies and the official
`actions/github-script` action may not interpolate Actions expressions directly
or hide failure with `|| true`, including before another shell separator or a
closing subshell. Reusable calls must pass named secrets, and secrets may not
live in a workflow-wide or job-wide environment. A reusable-call secret mapping
must reference one explicit `secrets.NAME`, never the whole context. Docker
actions plus job and service container images require an immutable `sha256`
digest; only reusable-job and step `uses` nodes are interpreted as actions.
The check is read-only and deterministic.
