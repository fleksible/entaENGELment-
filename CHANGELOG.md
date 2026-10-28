# Changelog

All notable changes to EntaENGELment will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Release Prep
- Added a concrete RC preflight checklist for `v0.1.0-rc1` in `docs/release/RC_PRECHECK_v0.1.0-rc1.md`.
- Clarified release process documentation for RC tags (`-rc`) and pre-release behavior.

### Added
- Release workflow with integrated gate checks (INF-4)
- Dependabot for automated dependency monitoring (INF-2)
- SBOM generation workflow (INF-3)
- NOTICE file for Apache-2.0 compliance (INF-3)
- VOID→Issue sync workflow (INF-7)
- Benchmark-replay target for reproducible validation (P2-A)
- Metatron pre-protocol amnesty documentation (P1-B)

### Changed
- `make demo` reports "UNSIGNED … signature not verified" when no `ENTA_HMAC_SECRET`/`CI_SECRET`
  is set instead of claiming a verified receipt (B8, checkup 2026-10-28).
- Documentation: module claims in `src/README.md` separate implementation from empirical meaning
  (B6); the exact `uv 0.12.18` requirement of `make install-dev` is documented (B7);
  "non-repudiable" wording for HMAC receipts corrected in `.claude/rules/annex.md`.
- Concept notes (no implementation): `docs/annex/ACTION_SCOPE_TRANSITIONS_v0_1.md`,
  `AGENT_INJECTION_PATTERNS_MAPPING_v0_1.md`, `SIGNED_BYTES_DECISION_NOTE_v0_1.md`,
  `CONSENT_RECORD_MAPPING_v0_1.md`, `TRANSPARENCY_AND_REVOCATION_NOTE_v0_1.md`.
- Security checks now blocking (no more continue-on-error) (INF-1)
- Coverage threshold raised from 20% to 50% (P0-B)
- VOID-012/013 reset to IN_PROGRESS (honest DRAFT status) (P1-A)

### Fixed
- Fail-closed fixes from `docs/audit/2026-10-28_repo_checkup.md` (behaviour changes):
  - B1: MZM gate blocks non-finite or non-real `phi`/`m_norm_l2` (`BLOCK_PHI_BELOW_MIN`,
    `BLOCK_M_NORM_INVALID`) and accepts only bool `True` for its boolean constraints; the
    decision no longer depends on logging the raw metrics, and non-finite values are not logged.
  - B5: `Ledger.metric`/`Ledger.gate` validate payloads (incl. nested tags) as strict JSON before
    any state change; rejected events leave `_prev_hash`, `_events` and the file untouched.
    The persisted-file verifier also rejects non-finite JSON constants and numbers that
    overflow its float decoder, even if the stored hash matches.
  - B2: negative curvature takes precedence over flat directions in `classify_stability`;
    degenerate saddles block with consent; invalid, non-symmetric or non-finite matrices block.
    Both stability guards accept only bool `True` as consent.
  - B4: `Ledger.verify_chain()` after reopening checks the appended section from the loaded
    anchor; the persisted history remains the job of `verify_chain_from_file`.
  - B3: `eci.permutation_test` now raises `NotImplementedError` (test design not specified);
    `bootstrap_ci` gains a `seed`, validates input and no longer returns `(0, 0)` for empty data.
    Resampling and percentile interpolation are scaled to keep finite extreme inputs finite.
  - B9 (partial fix): `compute_hessian_numerical` returns an `EstimatedHessian` (central
    differences, default step `ε^(1/4)·max(1, |x|)`). A classification based on an estimate
    needs a declared error bound (`fourth_derivative_bound`, `evaluation_error`). Otherwise
    the new status `UNRESOLVED` blocks, even with consent. MOD_18 maps `UNRESOLVED` to
    `UNDEFINED`/`BLOCK_UNDEFINED_STATE`. Matrix-only access and false declarations remain
    open (`docs/annex/STABILITY_NUMERICS_v0_1.md`).
  - B9 follow-up: the declared error bound is now computed exactly and rounded upward, so
    intermediate underflow such as `(h_i+h_j)⁴` can no longer erase it and cause a false
    STABLE. Non-normal denominators or a non-representable bound give `UNRESOLVED`, no
    longer a too-small bound or an exception. The eigenvalue uncertainty uses scaled norms.
    The exploratory Richardson value is `None` when the doubled stencil cannot be evaluated;
    previously that error discarded the primary estimate.
- All VOIDs assigned owners and target dates (P1-D)
- VOID-002 closed: full verify/lint in CI pipeline (P2-B)
- HMAC secret now persistent (P0-C, manual)

## [0.1.0] — 2026-02-15

> Note: This entry documents planned/reported `0.1.0` contents. In this repository clone, no `v0.1.0` git tag is present.

Documented 0.1.0 release baseline after hardening sprint (tag/publication status must be verified against the canonical remote).

### Foundation
- DR-KERNEL v1.5 governance framework
- DeepJump Protocol v1.2 (Verify → Status → Snapshot → Upload)
- Guard system G0–G8
- HMAC-signed receipt chain
- VOIDMAP-as-Code with ownership tracking
- 15-module architecture (MOD 0–15)
- Phasor/BETSE empirical bridge
- Claim-tagging system (FACT/INFERENZ/HYPOTHESE/METAPHER)
- Ethics test suite (consent expiry, boundary guards)
- Kenogramm Rubrik v0.5
