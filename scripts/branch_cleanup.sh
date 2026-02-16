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
