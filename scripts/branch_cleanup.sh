#!/usr/bin/env bash
# branch_cleanup.sh — Remove merged branches (local + remote)
#
# Safety: never deletes main, develop, or protected branches.
# Usage: scripts/branch_cleanup.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
PROTECTED_BRANCHES="main master develop release"

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE ==="
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)

is_protected() {
    local branch="$1"
    for p in $PROTECTED_BRANCHES; do
        if [[ "$branch" == "$p" ]]; then
            return 0
        fi
    done
    return 1
}

echo "=== Branch Cleanup ==="
echo "Current branch: $current_branch"
echo ""

# Fetch latest remote state
git fetch --prune origin 2>/dev/null || true

# Find merged local branches
echo "--- Merged local branches ---"
merged_local=0
while IFS= read -r branch; do
    branch=$(echo "$branch" | xargs)  # trim whitespace
    [ -z "$branch" ] && continue
    if [[ "$branch" == "$current_branch" ]] || is_protected "$branch"; then
        continue
    fi
    merged_local=$((merged_local + 1))
    if $DRY_RUN; then
        echo "  Would delete: $branch"
    else
        echo "  Deleting: $branch"
        git branch -d "$branch" 2>/dev/null || echo "  (skipped: $branch not fully merged)"
    fi
done < <(git branch --merged main 2>/dev/null | grep -v '^\*' || true)

echo ""
echo "Merged local branches processed: $merged_local"
echo "=== Cleanup complete ==="
#!/bin/bash
# Branch Cleanup — Remove stale merged branches
# Usage: ./scripts/branch_cleanup.sh [--dry-run]
# Default: dry-run. Pass --execute to actually delete.

set -euo pipefail

MODE="${1:---dry-run}"
PROTECTED="main|develop|release"

echo "=== Branch Cleanup (Mode: $MODE) ==="

git fetch --prune origin

MERGED=$(git branch -r --merged origin/main | grep -v "HEAD" | grep -vE "$PROTECTED" | sed 's|origin/||')

if [ -z "$MERGED" ]; then
    echo "No stale merged branches found."
    exit 0
fi

echo "Stale merged branches:"
echo "$MERGED" | while read branch; do
    LAST_COMMIT=$(git log -1 --format="%ai %s" "origin/$branch" 2>/dev/null || echo "unknown")
    echo "  - $branch ($LAST_COMMIT)"
done

if [ "$MODE" = "--execute" ]; then
    echo ""
    echo "Deleting..."
    echo "$MERGED" | while read branch; do
        git push origin --delete "$branch" 2>/dev/null && echo "  Deleted: $branch" || echo "  Skip: $branch"
    done
    echo "Done."
else
    echo ""
    echo "Dry run. To delete, run: $0 --execute"
fi
