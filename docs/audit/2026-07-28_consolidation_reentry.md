# entaENGELment consolidation and re-entry audit — 2026-07-28

VERIFIED — This report separates repository facts, connected-document classifications,
draft work, and explicit holds. Drive upload dates, internal document dates,
the date of this audit, and canon status are independent fields.

## State matrix

| Category | Element | Current status | Evidence | Action |
|---|---|---|---|---|
| VERIFIED | `main` | `eade3b7726dfa70b9d226f8ba3421aa1012edb2f` | commit `docs: bound security and resonance claims (#331)` | none |
| VERIFIED | PR #321 exact-version thread | implementation accepts only complete npm SemVer 2.0.0 or conservative PyPI PEP 440 public identifiers; target thread resolved after verification | PR #321, commit `325adcfd6d4447b05f4c129749110065da13e9d6` | no code follow-up |
| VERIFIED | PR #334 | open, mergeable, ready for review; 7/7 observed head workflows successful | PR #334, head `76a1a884b1563b60074bec690c436d7247921489` | Owner review; no autonomous merge |
| DRAFT | PR #340 | open draft, unmerged; this consolidation branch | PR #340 | complete CI and human review; no autonomous merge |
| VERIFIED | Dependency PRs #335–#338 | patch updates; expected file scope; 9/9 observed checks successful on each head | PRs #335–#338 | review and merge individually |
| HOLD | Dependency PR #298 | `MAJOR_COMPATIBILITY_HOLD`; TypeScript 7 breaks lint/typecheck compatibility | PR #298 workflow logs | separate compatibility track |
| HOLD | Dependency PR #339 | `MAJOR_COMPATIBILITY_HOLD`; ESLint 10 conflicts with `eslint-plugin-react@7.37.5` | PR #339 workflow logs | separate compatibility track |
| HOLD | Security settings/advisories | repository settings-side CodeQL and Private Vulnerability Reporting posture not exposed by the connected evidence | open issue #332; last audit witness in PR #329 | Owner/settings verification |
| VERIFIED | VOID-027 | `IN_PROGRESS`; stable repo-relative receipt evidence exists, but HUD receipt-link rendering and the remaining declared components stay open | `VOIDMAP.yml` and `receipts/2026-07-28_void027_bridge_view_v0_1.json` | validate in CI; do not close VOID |
| HOLD | VOID-010/011 | overdue and still `IN_PROGRESS` | `VOIDMAP.yml`, issue #311 | scoped evidence review |
| VERIFIED | Notion re-entry mirror | connected mirror records PRs #326–#331 and issues #332/#333; it explicitly defers authority to repo/VOIDMAP | Notion page `3a9a6554-a786-8105-a411-e5745c6319f5` | reference only |
| HOLD | Linear | no matching entaENGELment project or issue was found in the connected workspace | connected Linear search | no issue creation without Owner choice |

## Dependency classification

| Category | PR | Class | Verification |
|---|---:|---|---|
| VERIFIED | #335 | A — `actions/checkout` 7.0.0 → 7.0.1 | expected workflow files; observed checks successful |
| VERIFIED | #336 | A — `@tanstack/react-query` 5.101.2 → 5.101.4 | manifest/lockfile only; observed checks successful |
| VERIFIED | #337 | A — React 19.2.7 → 19.2.8 | manifest/lockfile only; observed checks successful |
| VERIFIED | #338 | A — `@tailwindcss/postcss` 4.3.2 → 4.3.3 | manifest/lockfile only; observed checks successful |
| HOLD | #298 | `MAJOR_COMPATIBILITY_HOLD` — TypeScript 7 | `typescript-estree` crash and failed Next typecheck |
| HOLD | #339 | `MAJOR_COMPATIBILITY_HOLD` — ESLint 10 | `eslint-plugin-react` API incompatibility |

VERIFIED — The current workspace policy includes explicit `pnpm` overrides and
`patches/brace-expansion@5.0.8.patch`. These are compatibility/security
exceptions, not ordinary patch updates. They must remain isolated, documented,
and rollbackable.

### Major compatibility tracks

| Category | Check | PR #298 — TypeScript 7 | PR #339 — ESLint 10 |
|---|---|---|---|
| HOLD | workspace tests | not accepted; required workflow is red | not accepted; required workflow is red |
| HOLD | lint/config/plugins | `@typescript-eslint/typescript-estree@8.60.1` crashes on TS 7 (`Cjs`) | `eslint-plugin-react@7.37.5` calls removed context API |
| HOLD | typecheck | Next build reaches typecheck, then reports the required TypeScript package unavailable | not reached after lint failure |
| HOLD | build/packaging | compile stage alone is insufficient; typecheck/package acceptance absent | build and Electron packaging acceptance absent |
| HOLD | lockfile consistency | changed lockfile is not accepted while compatibility checks fail | changed lockfile is not accepted while compatibility checks fail |
| HOLD | audit result | no successful head-specific audit witness | no successful head-specific audit witness |
| HOLD | breaking changes | demonstrated parser/toolchain incompatibility | demonstrated plugin API incompatibility |
| HOLD | rollback | leave unmerged or close PR; `main` stays unchanged | leave unmerged or close PR; `main` stays unchanged |

## VOID/QDOT re-entry

| Category | Entry / status | Open required parts | Current evidence | Smallest closable part | Blocker | Review boundary |
|---|---|---|---|---|---|---|
| HOLD | VOID-010 / `IN_PROGRESS` | cited CSV and evidence bundle | `docs/voids/VOID-010_taxonomy_and_spectra.md` | sources-first CSV schema with at least five cited sources | overdue 2026-07-15; empirical source binding | physics/literature review |
| HOLD | VOID-011 / `IN_PROGRESS` | deterministic metric export and `SIMULATION_PROXY` receipt | metrics code, toy dataset, unit test, VOID note | one deterministic claim-tagged export/receipt | evidence boundary, not implementation stub | quantitative-method review |
| HOLD | VOID-015 / `OPEN` | lint rules, fixtures, coverage receipt | none | one trigger-term fixture with Reason/Transform/Input binding | target thresholds remain SPEC | claim-hygiene/governance review |
| HOLD | VOID-016 / `OPEN` | τ retention rules, autophagy/V+ interaction, deletion receipts | none | one explicit τ_fast retention rule and negative fixture | “essence” and deletion semantics are not operationally bound | governance/privacy review |
| HOLD | VOID-017 / `OPEN` | Δ components and non-peak tipping tests | none | one negative fixture proving magnitude alone does not tip | threshold/components remain SPEC | math/control review |
| HOLD | VOID-024 / `OPEN` | consent policy, bounds, reason codes, kill-switch, safe-text fallback, receipt | none | consent + STOP fallback schema fixture | heuristic frequency/PLV values lack an evidence path | safety/human review |
| HOLD | VOID-025 / `OPEN` | modality fields, deterministic serialization, hash basis, autophagy invariants, receipt fixtures | none | canonical UTF-8 NFC text fixture | cross-modality identity and heuristics unresolved | governance/cryptographic review |
| HOLD | VOID-026 / `OPEN` | ADR, model, Kraehennest order, tests, receipt | none | ADR invariant: SailObservation precedes KraehennestObservation | runtime/control model not authorized | architecture/governance review |
| VERIFIED | VOID-027 / `IN_PROGRESS` | 1xn slice, Apex, calibrated EFS/MVI, decision bar remain open | HUD/frame code, fixtures/tests, README, new receipt pointer | stable repo-relative receipt pointer | remaining UI/calibration elements are separately unevidenced | Owner/human review before status change |
| HOLD | VOID-028 / `OPEN` | normalized deltas, calibration factors, thresholds, three fixtures, `SIMULATION_PROXY` receipt | none | bind metric definitions before calibrating thresholds | false-precision risk and VOID-011 dependency | math/quantitative review |
| HOLD | VOID-029 / `OPEN` | cross-instance receipt schema/instance and allowed reuse scope | none | one receipt instance with `human_commit_required=true` | source poles/protected-origin scope unresolved | governance/Owner review |
| HOLD | VOID-LOGZN-001 / `OPEN` | tests, metrics/claim tags, receipt or replay witness | two cited RZT/tesser3TAKT documents | one claim-tagged test plus receipt | current evidence is documentary only | math/claim review |

VERIFIED — No additional diagram, calibration, or narrative extension is started by this
change.

HOLD — No separate canonical QDOT registry was verified in the inspected repo
sources. QDOT statements in Drive document
`1wsipMetHXM6y4Lo66amlh7Qph1z72zlt` remain historical reference and do not
close or promote a repo entry.

## Connected Drive classification

| Category | Primary class | Document ID | Internal document date | Drive upload / modified date | Rationale |
|---|---|---|---|---|---|
| VERIFIED | WORKING_DRAFT | `1FakZrgPWLvJgTZevIXfm0rCnlVVROrtFT1taoUTGMlI` | 2026-07-22 | 2026-07-22 created/modified | internal read-only shadow catalog; no authority |
| HISTORICAL_REFERENCE | HISTORICAL_REFERENCE | `1vXrSyu4o--5pA-FulYG46AEGUzVaOmOw` | 2026-05-20 | 2026-07-19 upload | upload map, not current repository state |
| HISTORICAL_REFERENCE | HISTORICAL_REFERENCE | `1bRRzGSm7KXJE0CFviuQyfckkTWfrd1UG` | snapshot at `main@96bbdb9` | 2026-07-19 created/modified | contradicts the current verified main SHA |
| HISTORICAL_REFERENCE | HISTORICAL_REFERENCE | `1wsipMetHXM6y4Lo66amlh7Qph1z72zlt` | snapshot date in document | 2026-07-19 created/modified | VOID/QDOT states are stale against `VOIDMAP.yml` |
| HISTORICAL_REFERENCE | HISTORICAL_REFERENCE | `14TTRVr7zbOdna1Z-cyorweQC4q_Moq3d` | 2026-07-25 | 2026-07-26 created/modified | protected save state, but repo/PR snapshot is stale |
| HISTORICAL_REFERENCE | HISTORICAL_REFERENCE | `1ku9YAmiYjkuk2rZkB9jDzM8xYT-pJce6` | 2026-01-26 | 2026-07-26 created/modified | research indexer snapshot does not represent the current repo |
| HOLD | QUARANTINE_OVERCLAIM_REVIEW | `1GX8xBBudyNK0Im_EU_Rhpw5bBNbRuU-p` | 2025-12-16 | 2026-07-26 upload | quantitative, physical, biological, TRL, and “proof” language lacks a bound repo/lab evidence chain |
| NARRATIVE | NARRATIVE_LAYER | `1lOW9L35WQ2KtWFdBXr_wZfKr7AHrQaAR` | date in document | 2026-07-19 upload | document self-labels model/Rosetta/guard/wordknot/narrative material and disclaims scientific proof |
| NARRATIVE | NARRATIVE_LAYER | `10ySaVb8S2NnagB5L--jQ9V4kifv6EM2Q` | not treated as canon date | 2026-07-26 modified | private Grimm reading surface; not an evidence source |

HOLD — The classification creates no canon. Source-of-Truth admission still requires
technical/content review, Claude/Diogenes review, explicit Owner decision,
documented receipt, and a rollback path.

HOLD — Drive metadata reported `source_visibility_status=access_not_verified`
for these records. The primary class is a content/re-entry classification, not
a sharing or confidentiality guarantee.

## Action-Gate boundary

| Category | Re-entry point | State |
|---|---|---|
| VERIFIED | `PROPOSE != AUTHORIZE` | documented invariant |
| VERIFIED | `PROPOSE != EXECUTE` | documented invariant |
| HOLD | payload limits | separate review and authorization required |
| HOLD | registry signature verification | separate review and authorization required |
| HOLD | consumer authenticity | separate review and authorization required |
| HOLD | executing runtime boundary | no consumer implemented |
| HOLD | ledger or UI coupling | separate adapter decision required |
| HOLD | installation or deployment path | no path implemented |

## Grimm accessibility and protection audit

| Category | Check | Result |
|---|---|---|
| VERIFIED | local/network boundary | no `fetch`, XHR, WebSocket, local/session storage, or dynamic execution found in the connected HTML; CSP has `connect-src 'none'`; referrer policy is `no-referrer` |
| VERIFIED | semantic baseline | `header`, `main`, `footer`, labels, native controls, an `aria-live` copy status, and an `aria-label` on the generated prompt field are present |
| HOLD | reduced motion | `prefers-reduced-motion` handling is absent while repeated animations are present |
| HOLD | focus/keyboard | no explicit `:focus-visible`; some selection semantics are not conveyed with ARIA state |
| HOLD | contrast | several computed foreground/background pairs are below 4.5:1 and require contextual visual review |
| HOLD | screen-reader flow | dynamic receipt-card order and state announcements require assistive-technology testing |
| HOLD | re-identification | local storage boundaries do not establish content anonymity; copied prompts can cross the local boundary |
| HOLD | `HUMAN_REVIEW_HOLD` | keyboard, focus, contrast, reduced-motion, and screen-reader behavior were not interactively verified in a rendered provider artifact |

NARRATIVE — Structural protection is not equivalent to content anonymity. The Grimm
surface remains a narrative reading space and muse, not an evidence instance.

## Authority and rollback

DRAFT — All new code in this change is a non-executing projection. Rollback is a revert
of the introducing commit, together with removal of its VOIDMAP evidence
pointer. No deployment, publication, merge, Source-of-Truth promotion, runtime
consumer, or canon change is performed.
