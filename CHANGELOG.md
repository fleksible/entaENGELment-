# Changelog

All notable changes to EntaENGELment will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Release workflow with integrated gate checks (INF-4)
- Dependabot for automated dependency monitoring (INF-2)
- SBOM generation workflow (INF-3)
- NOTICE file for Apache-2.0 compliance (INF-3)
- VOID→Issue sync workflow (INF-7)
- Benchmark-replay target for reproducible validation (P2-A)
- Metatron pre-protocol amnesty documentation (P1-B)

### Changed
- Security checks now blocking (no more continue-on-error) (INF-1)
- Coverage threshold raised from 20% to 50% (P0-B)
- VOID-012/013 reset to IN_PROGRESS (honest DRAFT status) (P1-A)

### Fixed
- All VOIDs assigned owners and target dates (P1-D)
- VOID-002 closed: full verify/lint in CI pipeline (P2-B)
- HMAC secret now persistent (P0-C, manual)

## [0.1.0] — 2026-02-15

Initial tagged release after hardening sprint.

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
