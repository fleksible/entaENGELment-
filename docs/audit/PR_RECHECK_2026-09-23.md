# PR recheck and Dependabot parser repair

Date: 2026-09-23
FOKUS: Review open PRs, inspect failed update runs, repair a reproducible updater blocker.

## Findings

- [FACT] Main `332c0fa76c556340239e8c9ed012bac75b4e9035` already contains #357. All nine runs returned for that commit completed successfully, including Tests, Python Quality, DeepJump, SBOM and Evidence Bundle.
- [FACT] The latest applicable JS workspace and Security Audit runs on the preceding dependency merge `e9046bae30aa5d534a235259ecbee991c469c97b` also succeeded. The documentation-only #357 did not trigger those path-filtered workflows.
- [FACT] #298 and #339 remain open with unchanged heads and merge conflicts. Their failing workspace logs show, respectively, a TypeScript API `Cjs` error and React ESLint rule `getFilename` failure. Registry metadata checked again: typescript-eslint@8.70.1 supports TypeScript >=4.8.4 <6.1.0; eslint-plugin-react@7.37.5 supports ESLint through ^9.7, excluding 10. These major upgrades remain HOLD pending compatible tooling and full green verification.
- [FACT] Dependabot runs 35863034007 (uv/black), 35863034312 (uv/pytest), and 35863033837 (pip/black) all abort while parsing `Fractalsense/web_prototype_requirements.txt`: its prose starts with `// Web-Prototyp`, which is not a Python requirement.
- [FACT] Run 35863036532 targets `NICHTRAUM/archive` and aborts because no active project manifest exists there. Its archived uv.lock is historical evidence, not an active installation source; the protected archive is unchanged.

## Repair

- [FACT] Preserve the complete original web specification byte-for-byte in `Fractalsense/web_prototype_requirements.md`.
- [FACT] Retain the old `.txt` path as a comment-only compatibility pointer. No files or specification content are discarded. Requirement scanners now see zero packages at that path instead of an invalid manifest.
- [FACT] No dependency versions, production code, CI gates, receipts or GOLD files change.

## Validation and limitations

- [FACT] The actual pip parser plus install-requirement constructor accept all four tracked `*requirements*.txt` files after the repair. A byte comparison confirms the Markdown document exactly matches the original committed specification.
- [FACT] Local `make verify` passed before and after the repair: 626 tests and 165 subtests, with 104 existing warnings. Remote PR checks must pass before merging.
- [RISK] This repairs the observed parser failure; it does not establish that Dependabot's next update succeeds or resolves the reported Black/pytest advisories. Active Python dependency/lock consolidation remains tracked in #333. No claim is made that the archived Pygments alert is fixed.

## Evidence

- Main Tests: https://github.com/fleksible/entaENGELment-/actions/runs/35868333677
- Python updater parse failure: https://github.com/fleksible/entaENGELment-/actions/runs/35863033837
- Archived lock updater failure: https://github.com/fleksible/entaENGELment-/actions/runs/35863036532
- TypeScript HOLD: https://github.com/fleksible/entaENGELment-/pull/298
- ESLint HOLD: https://github.com/fleksible/entaENGELment-/pull/339
