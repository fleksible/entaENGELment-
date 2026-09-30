# Python lock introduction baseline

The lock introduction for issue #333 preserves every installed package
name/version from the preceding successful Python 3.11 quality job:
[job 109830467826](https://github.com/fleksible/entaENGELment-/actions/runs/36697992134/job/109830467826).
The job belongs to the coordinated React PR #371; no Python package update
was included there. Its `Successfully installed` inventory was compared with
the fresh Linux CPython 3.11.16 `dev` environment produced by the new lock.

Existing package versions, including the editable `entaengelment==0.1.0`,
are unchanged. The only additional distributions in that environment are
`setuptools==84.0.0` and `wheel==0.48.0`, explicitly installed from the `build`
group so project installation can disable untracked build isolation.

The new audit and SBOM groups also explicitly record their tool dependencies.
The FractalSense group now includes the project's runtime dependencies through
the same installation contract. Those additions are environment composition
changes rather than upgrades to existing runtime/dev packages.

Python/platform forks are deliberate. Python 3.9–3.12 runtime compatibility
is checked independently by the PR matrix. The Python 3.11 baseline comparison
does not establish support for an untested interpreter or operating system.
Requirements files retain the lock's environment markers and wheel hashes.

Refresh review must compare package names, versions and added/removed groups;
the generated export text alone is not a meaningful version-change summary.
