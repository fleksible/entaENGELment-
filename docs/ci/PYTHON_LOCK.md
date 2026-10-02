# Reproducible Python environments

The sole resolution authority for the blocking CI gates and managed local
development environments is `uv.lock`,
generated with **uv 0.12.18** from `pyproject.toml`. Runtime dependencies remain
in `[project.dependencies]`; explicit dependency groups cover `test`, `dev`,
`fractalsense`, `audit`, `sbom` and `build`.

Runtime/test compatibility is validated on Linux with Python 3.9–3.12. The
quality and FractalSense groups require >=3.10; audit/SBOM tools require >=3.11.
The wider public `requires-python` range is unchanged. Other interpreter/OS
combinations are represented by the universal lock but need their own tests
before claiming support. The published legacy `[dev]` extra remains available;
it is not the repository's reproducible installation entry point.

## Install and verify

```sh
python -m pip install "uv==0.12.18"
python tools/python_lock.py check
python tools/python_lock.py sync --group test
.venv/bin/python -m pytest tests/
uv pip check --python .venv/bin/python
```

`sync` uses `--locked` and rejects source/export drift. It first installs the
locked build tools, then installs the project with build isolation disabled.
The first exact sync clears unrelated dependencies from this dedicated
environment; never point `UV_PROJECT_ENVIRONMENT` at a personal shared venv.
Set that variable to a new directory for a separate test context. Every sync
records the lock SHA-256, selected group, interpreter/platform and installed
name/version inventory in that environment's `lock-receipt.json`.

`requirements*.txt` and `Fractalsense/requirements-dev.txt` are generated,
hashed compatibility exports. They are not independent dependency inputs.
Editing them without re-exporting fails CI. Change the corresponding project
dependency or group in `pyproject.toml` instead.

## Deliberate refresh

```sh
# Keep existing versions whenever compatible with the edited source.
uv lock
python tools/python_lock.py export
python tools/python_lock.py check

# Upgrade a named package explicitly, then regenerate exports.
uv lock --upgrade-package PACKAGE
python tools/python_lock.py export
```

Review direct and transitive name/version changes, Python/platform forks,
hashes and newly introduced packages. Run fresh installs, `uv pip check`, the
supported interpreter matrix, quality gates and SBOM reconciliation. A broad
`uv lock --upgrade` is a separate reviewed dependency update. Never combine
an unreported package upgrade with a lock/governance change.

Dependabot targets the **uv** ecosystem at the root, groups version/security
updates, and excludes historical `NICHTRAUM/archive/**` manifests. A bot PR
must also regenerate the compatibility exports before it can pass the same
drift gate; it must not open independent pip PRs against generated exports.

## SBOM and reproducibility evidence

The SBOM workflow installs its target runtime from the lock. The CycloneDX
generator has a separate environment synced from the same lock's `sbom`
group, so generator dependencies are not reported as runtime dependencies.
The SBOM must exactly match the target's locked installation receipt,
including the deliberately installed build tools and the local project.
Stale lock digests, changed installations, omitted/additional versions and
duplicate components fail closed. Use:

```sh
UV_PROJECT_ENVIRONMENT=.sbom-tools python tools/python_lock.py sync --group sbom
.sbom-tools/bin/cyclonedx-py environment .venv/bin/python \
  --pyproject pyproject.toml --spec-version 1.6 --output-reproducible \
  --output-format JSON --output-file sbom-python.cdx.json
python tools/python_lock.py verify-sbom --sbom sbom-python.cdx.json
```

Two fresh environments of the same group, interpreter and platform must have
identical package inventories and lock digests. Local path names and receipt
timestamps are not dependency versions. CI and this receipt establish the
tested resolution; they do not make claims about conceptual framework status.
The PR runtime workflow checks this using two fresh Python 3.11 test-group
environments; the SBOM reconciliation also runs before merge.

## Automation installation coverage

The initial lock PR left the Release Gate and VOID Deadline Monitor untouched
after automated approval review rejected writes to workflows with existing
release/issue-writing permissions. Those rejected changes were recorded as
pending work, not as implemented coverage.

On 2026-10-02, the maintainer changed the Release Gate to create draft releases.
[PR #378](https://github.com/fleksible/entaENGELment-/pull/378), merged the same
day, replaced its unfrozen installation with the pinned uv manager and locked
`dev` group. All nine observed PR workflow runs succeeded on its final head.
The tag-triggered Release Gate itself was not executed by those PR runs; its
configuration and the shared lock installer were checked without creating a tag.

The VOID Deadline Monitor uses `./.github/actions/python-locked` with the
default `runtime` group, which includes PyYAML. Its schedule, permissions,
deadline logic and issue-writing steps retain their existing behavior. A PR
check does not execute the scheduled monitor or prove an issue was created.

Repository-managed Python installations now use the same lock contract.
The pinned `pip install "uv==0.12.18"` bootstrap installs the lock manager;
project and build dependencies are installed from `uv.lock`. See the baseline
above for the tested Python/platform range and reproducibility limitations.

Before closing #333, confirm that this monitor change has merged and its PR
checks pass. A merge or green CI does not authorize a public release or promote
framework claims to Source of Truth.
