# Release Process

## Versioning

EntaENGELment uses [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes to Guard contracts or Receipt schema
- MINOR: New modules, new guards, new workflows
- PATCH: Bug fixes, documentation, non-breaking improvements

## How to Release

1. Ensure all CI checks are green on `main`
2. Update CHANGELOG.md with release notes
3. Tag: `git tag v0.1.0 -m "EntaENGELment v0.1.0"`
4. Push tag: `git push origin v0.1.0`
5. Release workflow runs automatically:
   - All gate checks must PASS
   - GitHub Release created with auto-generated notes
6. If any gate fails: delete tag, fix, retag

## Gate Checklist (automated)

The release workflow verifies:
- [ ] Pointer integrity (verify_pointers.py)
- [ ] Claim lint (claim_lint.py)
- [ ] Port lint (port_lint.py)
- [ ] Receipt lint (all receipts)
- [ ] No ownerless VOIDs
- [ ] Tests pass
- [ ] No stub metrics
