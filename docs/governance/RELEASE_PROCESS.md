# Release Process

## Versioning

EntaENGELment uses [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes to Guard contracts or Receipt schema
- MINOR: New modules, new guards, new workflows
- PATCH: Bug fixes, documentation, non-breaking improvements

## How to Release

1. Ensure all CI checks are green on `main`
2. Update CHANGELOG.md with release notes
3. Tag (Beispiel): `git tag vX.Y.Z -m "EntaENGELment vX.Y.Z"`
4. Push tag: `git push origin vX.Y.Z`
5. Release workflow runs automatically:
   - All gate checks must PASS
   - GitHub Release created with auto-generated notes
6. If any gate fails: delete tag, fix, retag

### Release Candidates (RC)

- RC tags follow SemVer pre-release form, e.g. `v0.1.0-rc1`.
- The existing workflow marks tags containing `-rc` as GitHub pre-release.
- For the first RC path, use `docs/release/RC_PRECHECK_v0.1.0-rc1.md` before tagging.

## Gate Checklist (automated)

The release workflow verifies:
- [ ] Pointer integrity (verify_pointers.py)
- [ ] Claim lint (claim_lint.py)
- [ ] Port lint (port_lint.py)
- [ ] Receipt lint (all receipts)
- [ ] No ownerless VOIDs
- [ ] Tests pass
- [ ] No stub metrics
