# Branch Protection Setup

## Required Steps (GitHub UI)

Go to: Repository → Settings → Branches → Add branch protection rule

### Branch name pattern
`main`

### Settings to enable

- [x] Require a pull request before merging
  - [x] Require approvals: 1 (or 0 if solo maintainer)
- [x] Require status checks to pass before merging
  - [x] Require branches to be up to date before merging
  - Required checks:
    - `Verify Pointers & Lint (blocking)` (from deepjump-ci.yml)
    - `verify` (from ci.yml)
    - `build` (from ci.yml)
    - `security` (from ci.yml)
    - `Metatron Guard` (from metatron-guard.yml)
- [x] Do not allow bypassing the above settings

### Optional (recommended)
- [x] Require signed commits
- [x] Include administrators

## CLI Alternative (gh)

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Verify Pointers & Lint (blocking)","verify","build","security","Metatron Guard"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field restrictions=null
```

Replace `{owner}/{repo}` with `fleksible/entaENGELment-`.

## Verification

After setting protection:

```bash
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_status_checks.contexts'
```

Expected output: list of all required check names.

## Note

This must be configured manually via GitHub UI or API.
It cannot be set via repository files alone.
