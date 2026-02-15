#!/usr/bin/env python3
"""EntaENGELment Claim Lint (DeepJump Protocol v1.2)

Purpose: Detect untagged claims in core artefacts.
Scope: index/, spec/, receipts/, tools/

Claim Tags (Epistemische Hygiene):
  [FACT] - Empirically verified
  [HYP]  - Testable hypothesis
  [MET]  - Metaphor/Analogy (not to be read literally)
  [TODO] - Open task
  [RISK] - Known risk
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# Valid claim tags
VALID_TAGS = {"[FACT]", "[HYP]", "[MET]", "[TODO]", "[RISK]"}

# Patterns that indicate a claim (assertions about system behavior)
CLAIM_PATTERNS = [
    r"\bmust\b",
    r"\bshall\b",
    r"\bwill\s+(?:always|never)\b",
    r"\bguarantee[sd]?\b",
    r"\bensure[sd]?\b",
    r"\bvalidate[sd]?\b",
    r"\bverif(?:y|ies|ied)\b",
    r"\bprov(?:es?|en|ing)\b",
    r"\bconfirm(?:s|ed)?\b",
    r"\brequire[sd]?\b",
    r"\bimplementat(?:ion|ed)\b",
    r"\btested\b",
    r"\bpassed\b",
    r"\bfailed\b",
    r"\bworking\b",
    r"\bcompleted?\b",
    r"\bfixed\b",
]

# Directories to scan by default
DEFAULT_SCOPE = ["index", "spec", "receipts", "tools"]

# Files/patterns to skip
SKIP_PATTERNS = [
    r"__pycache__",
    r"\.pyc$",
    r"\.git",
    r"node_modules",
    r"\.egg-info",
]

# Inline suppression marker
NOQA_MARKER = "noqa: claim-lint"

# Python code-pattern lines to skip (operational code, not epistemic claims)
PYTHON_CODE_SKIP = [
    r"^\s*(if|elif|else|return|raise|for|while|with|try|except|finally|assert)\b",
    r"^\s*\w+\s*=[^=]",           # variable assignment
    r"^\s*(print|logging|sys\.exit|errors?\.append)\s*\(",
    r"^\s*def\s+",                 # function definition
    r"^\s*class\s+",               # class definition
    r'^\s*"required"\s*:',         # JSON-like "required": in any file
    r"^\s*#",                      # code comments (operational notes)
    r"^\s*\w+\.\w+\(",            # method calls (e.g. ledger.gate(...))
    r'^\s*("""|\'\'\')',           # docstring delimiters
    r'^\s*r["\']',                 # raw string literals (regex patterns)
]


class ClaimResult(NamedTuple):
    file: str
    line_num: int
    line: str
    claim_word: str
    has_tag: bool


def get_repo_root() -> Path:
    """Get repository root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent.resolve()


def should_skip(path: str) -> bool:
    """Check if path should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, path):
            return True
    return False


def has_claim_tag(line: str) -> bool:
    """Check if line contains a valid claim tag."""
    for tag in VALID_TAGS:
        if tag in line:
            return True
    return False


def _is_python_code_line(line: str) -> bool:
    """Check if a Python line is clearly operational code, not an epistemic claim."""
    for pattern in PYTHON_CODE_SKIP:
        if re.search(pattern, line):
            return True
    return False


def find_claims_in_file(filepath: Path, repo_root: Path) -> list[ClaimResult]:
    """Find potential claims in a file."""
    results: list[ClaimResult] = []
    rel_path = str(filepath.relative_to(repo_root))
    is_python = filepath.suffix == ".py"

    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[WARN] Could not read {rel_path}: {e}")
        return results

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip shebangs and encoding markers
        if stripped.startswith("#!") or stripped.startswith("# -*-"):
            continue

        # Skip lines with inline suppression
        if NOQA_MARKER in line:
            continue

        # For Python files: skip lines that are clearly code constructs
        if is_python and _is_python_code_line(stripped):
            continue

        # Check for claim patterns
        for pattern in CLAIM_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                has_tag = has_claim_tag(line)
                # Only report if no tag present
                if not has_tag:
                    results.append(
                        ClaimResult(
                            file=rel_path,
                            line_num=line_num,
                            line=stripped[:80] + ("..." if len(stripped) > 80 else ""),
                            claim_word=match.group(),
                            has_tag=has_tag,
                        )
                    )
                break  # Only report once per line

    return results


def scan_directory(dir_path: Path, repo_root: Path) -> list[ClaimResult]:
    """Scan a directory for claims."""
    results: list[ClaimResult] = []

    if not dir_path.exists():
        print(f"[INFO] Directory not found: {dir_path.relative_to(repo_root)}")
        return results

    # Scan YAML, Markdown, and Python files
    # JSON excluded: schema keywords ("required", "passed") are structural, not claims
    extensions = {".yaml", ".yml", ".md", ".py"}

    for filepath in dir_path.rglob("*"):
        if filepath.is_file() and filepath.suffix in extensions:
            if not should_skip(str(filepath)):
                results.extend(find_claims_in_file(filepath, repo_root))

    return results


def run_claim_lint(repo_root: Path, scope: list[str], strict: bool = False) -> bool:
    """Run claim lint on specified directories."""
    all_results: list[ClaimResult] = []

    print("\n=== CLAIM LINT ===")
    print(f"Scope: {', '.join(scope)}")
    print(f"Valid tags: {', '.join(sorted(VALID_TAGS))}")

    for dir_name in scope:
        dir_path = repo_root / dir_name
        results = scan_directory(dir_path, repo_root)
        all_results.extend(results)

    # Filter to untagged claims only
    untagged = [r for r in all_results if not r.has_tag]

    # Group by file
    by_file: dict[str, list[ClaimResult]] = {}
    for r in untagged:
        by_file.setdefault(r.file, []).append(r)

    # Report results
    if untagged:
        print(f"\n⚠️  Found {len(untagged)} potential untagged claims in {len(by_file)} files:")
        for file, claims in sorted(by_file.items()):
            print(f"\n  {file}:")
            for c in claims[:5]:  # Show first 5 per file
                print(f"    L{c.line_num}: '{c.claim_word}' → {c.line}")
            if len(claims) > 5:
                print(f"    ... and {len(claims) - 5} more")

        if strict:
            print(f"\n[FAIL] {len(untagged)} untagged claims (strict mode)")
            return False
        else:
            print("\n[WARN] Consider adding tags to these claims")
            print("       Add [FACT], [HYP], [MET], [TODO], or [RISK] to document claims")
    else:
        print("\n✅ No untagged claims found in scope")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect untagged claims in core artefacts")
    parser.add_argument(
        "--scope",
        default=",".join(DEFAULT_SCOPE),
        help=f"Comma-separated directories to scan (default: {','.join(DEFAULT_SCOPE)})",
    )
    parser.add_argument(
        "--strict", action="store_true", help="Fail if any untagged claims are found"
    )
    parser.add_argument("--help-extended", action="store_true", help="Show extended help")
    args = parser.parse_args()

    if args.help_extended:
        print(__doc__)
        sys.exit(0)

    repo_root = get_repo_root()
    scope = [s.strip() for s in args.scope.split(",")]

    print(f"[claim_lint] Scanning from: {repo_root}")

    success = run_claim_lint(repo_root, scope, strict=args.strict)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
