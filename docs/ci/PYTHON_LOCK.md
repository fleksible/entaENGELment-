# Reproducible Python environments

The sole resolution authority for the blocking CI gates and managed local
development environments is `uv.lock`,
generated with **uv 0.12.18** from `pyproject.toml`. Runtime dependencies remain
in `[project.dependencies]`; explicit dependency groups cover `test`, `dev`,
`fractalsense`, `audit`, `sbom` and `build`.

As of 2026-10-23, runtime/test compatibility is validated on Linux with Python
3.10–3.14; the separate FractalSense suite covers Python 3.10–3.12. The project
requires Python >=3.10. Quality and FractalSense groups require >=3.10;
audit/SBOM tools require >=3.11. See the
[runtime matrix](../../.github/workflows/ci-python-runtime.yml) and
[FractalSense matrix](../../.github/workflows/test.yml). Other interpreter/OS
combinations need their own tests before claiming support. The published legacy
`[dev]` extra remains available; it is not the repository's reproducible
installation entry point. The [2026-09-30 baseline](PYTHON_LOCK_BASELINE_2026-09-30.md)
records the earlier Python 3.9–3.12 scope and is retained as historical evidence.

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

## Dependabot: current manual completion procedure

Dependabot targets the **uv** ecosystem at the root, groups version/security
updates, uses the explicit public PyPI registry, and excludes historical
`NICHTRAUM/archive/**` manifests. A bot PR must regenerate the compatibility
exports before it can pass the drift gate; it must not open independent pip PRs
against generated exports.

The current updater does not reliably keep `uv.lock` and all four exports
consistent. In [PR #410](https://github.com/fleksible/entaENGELment-/pull/410),
the original bot diff changed 16 packages in the exports but only Ruff in the
central lock. `Generated requirements drift` correctly blocked installation.
The corrected PR resolved 13 compatible updates in the lock and regenerated
the exports with uv 0.12.18. Three proposals incompatible with Safety 3.8.1 were
kept on HOLD. Its green checks validate that corrected head, not future bot PRs.

The Owner decision recorded on 2026-10-18 remains a manual procedure:

1. Inspect the bot's proposed package versions and resolver conflicts.
2. In a dedicated update branch, resolve only the selected compatible updates
   in `uv.lock` with the pinned uv manager. Do not make the exports independent
   inputs or disable their drift check.
3. Run `python tools/python_lock.py export`, then
   `python tools/python_lock.py check`.
4. Verify a fresh installation, `uv pip check`, tests, the supported runtime
   matrix and SBOM reconciliation. Review direct/transitive version changes and
   current CI at the corrected head before merge.
5. Link the original bot proposal to its reviewed correction or replacement.

[Issue #416](https://github.com/fleksible/entaENGELment-/issues/416) tracks this
remaining updater gap separately from the completed lock introduction in #333.
The successful managed uv run on 2026-10-19 produced a PR; it did not prove
that the generated PR passed the lock/export gate. The earlier relative
`rpds-py` URL failure and the export drift are distinct observations.

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

The monitor installation change merged in
[PR #379](https://github.com/fleksible/entaENGELment-/pull/379) on 2026-10-02.
The later [runtime/reproducibility run](https://github.com/fleksible/entaENGELment-/actions/runs/39395067994)
and [SBOM reconciliation](https://github.com/fleksible/entaENGELment-/actions/runs/39395067869)
on the corrected #410 head passed on 2026-10-20. These are the bounded acceptance
evidence for the lock work in #333; updater work continues in #416. The
[2026-10-23 maintenance review](../audit/2026-10-23_maintenance_acceptance.md)
records the checked revision and remaining limits. A merge or green CI does not
authorize a public release or promote framework claims to Source of Truth.
