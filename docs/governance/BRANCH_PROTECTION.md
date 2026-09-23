# Branch Protection Setup

**Status:** proposed settings; live enforcement is UNVERIFIED.
**Reviewed:** 2026-09-23. See `BRANCH_EXPECTED_STATE.yml` and issue #278.

Repository files describe the desired posture; they cannot activate protection.
Check Settings → Branches / Rulesets for `main` before changing configuration.

## Required checks

Use the **published job names**, confirmed on a current pull request. Internal
YAML job IDs and workflow titles are not interchangeable with check contexts.

| Check context | PR coverage |
|---|---|
| `Verify Pointers & Lint (blocking)` | Pointers, claims, ports |
| `deepjump-audit / deepjump-audit` | Reusable verification, receipts, tests, snapshot |
| `All Tests Pass` | JavaScript, Fractalsense Python matrix, UI build |
| `Lint · Format · Types · SAST` | Python quality and Bandit |
| `Check PR for FOKUS marker` | PR focus marker |

[FACT] The legacy `ci.yml` `verify`, `build`, and `security` jobs are skipped on
pull requests. They are not substitutes for the dedicated PR checks above.
Claim and receipt lint are steps within jobs, not separate published contexts.
The signed DeepJump path is intentionally skipped on PRs; it must not be required
as though pull requests receive signing secrets.

## Conditional checks

`workspace`, `JS dependency audit (pnpm)`, and
`Python dependency audit (pip-audit)` run for their workflow path filters.
Require their success whenever they execute. Do not configure them as globally
required contexts while the entire workflow can be skipped by a paths filter;
that can leave unrelated PRs waiting forever. An always-running dispatcher with
an explicit affected/unaffected outcome is a separate implementation step.

## Settings and readback

- Require pull requests and up-to-date checks.
- Choose the review count deliberately (solo maintainer: zero may be appropriate).
- Include administrators and disallow bypass according to the chosen rule.
- If signed commits are required, verify that the actual merge method supports it.
- Re-read the active branch/ruleset settings and compare names to a fresh PR.

Optional read-only verification with an authenticated GitHub CLI:

```bash
gh api repos/fleksible/entaENGELment-/branches/main/protection
gh api repos/fleksible/entaENGELment-/rulesets
```

A 403/404 or unavailable connector action is an unresolved access/setting check,
not evidence that protection is enabled or disabled. This maintenance pass does
not write repository settings.
