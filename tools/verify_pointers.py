#!/usr/bin/env python3
"""EntaENGELment Verify Pointers (DeepJump Protocol v1.2)

Purpose: Check for dead pointers in index and module definitions.
Rules:
  - OPERATIONAL CORE: must exist → error if missing
  - OPTIONAL: may be missing if marked with "(optional)" or "[OPT]"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


class PointerResult(NamedTuple):
    path: str
    source: str
    exists: bool
    optional: bool


# Directories considered OPERATIONAL CORE (must exist)
OPERATIONAL_CORE = {
    "index",
    "tools",
    ".github/workflows",
    "tests",
}

# Patterns that mark a path as optional
OPTIONAL_MARKERS = [
    r"\(optional\)",
    r"\[OPT\]",
    r"# optional",
    r"# OPT",
]


def get_repo_root() -> Path:
    """Get repository root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent.resolve()


def is_optional_context(text: str) -> bool:
    """Check if the surrounding text marks this as optional."""
    for pattern in OPTIONAL_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def extract_paths_from_yaml(yaml_path: Path, repo_root: Path) -> list[PointerResult]:
    """Extract file paths from a YAML file."""
    results: list[PointerResult] = []

    try:
        with open(yaml_path, encoding="utf-8") as f:
            content = f.read()
            data = yaml.safe_load(content)
    except Exception as e:
        print(f"[WARN] Could not parse {yaml_path}: {e}")
        return results

    if not isinstance(data, dict):
        return results

    # Keys that typically contain file paths

    def clean_path(raw: str) -> str:
        """Clean a path string by removing CLI arguments and whitespace."""
        # Strip CLI arguments (e.g., "tools/foo.py --strict" → "tools/foo.py")
        path = raw.split()[0] if " " in raw else raw
        return path.strip()

    def looks_like_path(s: str) -> bool:
        """Check if string looks like a file path."""
        # Must contain / but not be http
        if "/" not in s or s.startswith("http"):
            return False
        # Skip special values
        if s in ("REL_TO_ROOT", "sha256"):
            return False
        # Skip long descriptions (paths are usually short)
        if len(s) > 100:
            return False
        # Must have a file-like pattern (contains . or ends with /)
        if "." not in s and not s.endswith("/"):
            return False
        # Skip sentences (no spaces before the path portion)
        clean = clean_path(s)
        if " " in clean:
            return False
        return True

    # Extract paths from common keys
    def find_paths(obj, context: str = "", key: str = ""):
        if isinstance(obj, str):
            # Only check strings that look like paths
            if looks_like_path(obj):
                path = clean_path(obj)
                optional = is_optional_context(context)

                # Try both absolute from repo root and relative from source file
                full_path = repo_root / path
                relative_path = yaml_path.parent / path

                # Check if either path exists
                exists = full_path.exists() or relative_path.exists()

                # Use the path that exists, or fall back to absolute
                if relative_path.exists() and not full_path.exists():
                    # Convert to repo-relative path for consistent reporting
                    try:
                        path = str(relative_path.relative_to(repo_root))
                    except ValueError:
                        pass  # Keep original path

                results.append(
                    PointerResult(
                        path=path,
                        source=str(yaml_path.relative_to(repo_root)),
                        exists=exists,
                        optional=optional,
                    )
                )
        elif isinstance(obj, dict):
            for k, v in obj.items():
                find_paths(v, f"{context} {k}", k)
        elif isinstance(obj, list):
            for item in obj:
                find_paths(item, context, key)

    find_paths(data)
    return results


def is_core_path(path: str) -> bool:
    """Check if path is in OPERATIONAL CORE."""
    for core_dir in OPERATIONAL_CORE:
        if path.startswith(core_dir + "/") or path == core_dir:
            return True
    return False


def verify_pointers(repo_root: Path, strict: bool = False) -> bool:
    """Verify all pointers in index and module files."""
    all_results: list[PointerResult] = []

    # Scan index directory
    index_dir = repo_root / "index"
    if index_dir.exists():
        for yaml_file in index_dir.rglob("*.yaml"):
            all_results.extend(extract_paths_from_yaml(yaml_file, repo_root))

    # Also check VOIDMAP.yml if it exists
    voidmap = repo_root / "VOIDMAP.yml"
    if voidmap.exists():
        all_results.extend(extract_paths_from_yaml(voidmap, repo_root))

    # Categorize results
    missing_core: list[PointerResult] = []
    missing_optional: list[PointerResult] = []
    valid_paths: list[PointerResult] = []

    seen: set[str] = set()
    for result in all_results:
        if result.path in seen:
            continue
        seen.add(result.path)

        if result.exists:
            valid_paths.append(result)
        elif result.optional:
            missing_optional.append(result)
        elif is_core_path(result.path):
            missing_core.append(result)
        else:
            # Non-core, non-optional missing paths → warning only
            missing_optional.append(result)

    # Report results
    print("\n=== POINTER VERIFICATION ===")
    print(f"Checked: {len(seen)} unique paths")
    print(f"Valid:   {len(valid_paths)}")
    print(f"Missing (optional): {len(missing_optional)}")
    print(f"Missing (CORE):     {len(missing_core)}")

    if valid_paths:
        print("\n✅ Valid paths:")
        for r in valid_paths[:10]:  # Show first 10
            print(f"   {r.path}")
        if len(valid_paths) > 10:
            print(f"   ... and {len(valid_paths) - 10} more")

    if missing_optional:
        print("\n⚠️  Missing (optional/non-core):")
        for r in missing_optional:
            print(f"   {r.path} (from: {r.source})")

    if missing_core:
        print("\n❌ Missing (OPERATIONAL CORE):")
        for r in missing_core:
            print(f"   {r.path} (from: {r.source})")

    # Determine exit status
    if missing_core:
        print(f"\n[FAIL] {len(missing_core)} dead pointer(s) in OPERATIONAL CORE")
        return False

    if strict and missing_optional:
        print(f"\n[WARN] {len(missing_optional)} optional paths missing (strict mode)")

    print("\n✅ All core pointers valid")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify pointers in index and module definitions")
    parser.add_argument(
        "--strict", action="store_true", help="Also warn about optional missing paths"
    )
    parser.add_argument("--help-extended", action="store_true", help="Show extended help")
    args = parser.parse_args()

    if args.help_extended:
        print(__doc__)
        sys.exit(0)

    repo_root = get_repo_root()
    print(f"[verify_pointers] Scanning from: {repo_root}")

    success = verify_pointers(repo_root, strict=args.strict)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
