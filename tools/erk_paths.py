"""Write-boundary checks shared by ERK command-line adapters."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_PROTECTED_TOP_LEVELS = frozenset({"index", "policies", "nichtraum"})
_PROTECTED_COMPONENTS = frozenset({"receipt", "receipts"})


def ensure_erk_write_path(path: Path, *, repo_root: Path = REPO_ROOT) -> Path:
    """Resolve an output path and reject repository-protected destinations.

    Existing symlink components are resolved before the repository-relative
    check, closing the obvious alias path around the GOLD/NICHTRAUM boundary.
    Paths outside the repository remain available for tests and disposable
    operator output.
    """
    resolved = path.expanduser().resolve(strict=False)
    root = repo_root.expanduser().resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return resolved

    folded_parts = tuple(part.casefold() for part in relative.parts)
    protected = (
        not folded_parts
        or folded_parts[0] in _PROTECTED_TOP_LEVELS
        or "voidmap.yml" == relative.as_posix().casefold()
        or any(part in _PROTECTED_COMPONENTS for part in folded_parts)
    )
    if protected:
        raise ValueError(f"ERK output path is protected: {relative.as_posix() or '.'}")
    return resolved
