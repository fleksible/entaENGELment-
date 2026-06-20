#!/usr/bin/env python3
"""EntaENGELment Intake Shadow-Copy — Claude Code PostToolUse hook (PR #256).

Reads a Claude Code hook payload from stdin and, for document-like files written
or edited during a session, drops a *shadow copy* into the intake briefkasten at
``docs/intake/raw/auto/<YYYY-MM-DD>/`` plus a line in a machine ledger
(``_shadow_log.jsonl``).

Design notes (see docs/intake/README.md):
  - Capture is allowed; interpretation and canonisation are forbidden.
  - Copies only. Source files are never moved or deleted (G3).
  - Writes stay strictly inside docs/intake/raw/auto/. The human-curated
    INDEX.md and records/ are NOT touched by the hook (no vacuum effect).
  - Content-hash dedupe: re-editing the same file does not pile up duplicates.
  - Fail-soft: any error exits 0 so Claude Code is never blocked.

The hook is wired async in .claude/settings.json, so its output is discarded.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

# Document-like extensions worth catching in the briefkasten.
DOC_SUFFIXES = {".md", ".txt", ".docx", ".pdf", ".json", ".yml", ".yaml"}

# Tool names this hook reacts to.
DOC_TOOLS = {"Write", "Edit", "MultiEdit"}

# Path prefixes (repo-relative, posix) that must never be captured.
# Two groups: (a) mechanical noise/build/temp, (b) GOLD/canon that already has a
# home -- intake is for the *un-homed*, so canonical sources are not shadowed.
EXCLUDE_DIR_PREFIXES = (
    # (a) mechanical / build / cache
    "docs/intake/",
    ".git/",
    "node_modules/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    "htmlcov/",
    # (b) GOLD / already-homed canon (never write AND never shadow-capture)
    "index/",
    "spec/",
    "policies/",
    "seeds/",
    "docs/canon/",
    "docs/spec/",
    "docs/specs/",
    "docs/glossary/",
    "docs/roadmap/",
)

# Exact filenames never captured (lockfiles + GOLD registries).
EXCLUDE_FILENAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
    "uv.lock",
    "VOIDMAP.yml",
    "VOIDMAP.yaml",
}

# Destinations the hook must never write to (defence in depth; it only writes
# under docs/intake/raw/auto/ anyway).
FORBIDDEN_DEST_PREFIXES = (
    "docs/canon/",
    "docs/spec/",
    "docs/specs/",
    "docs/glossary/",
    "docs/roadmap/",
)

AUTO_REL = Path("docs/intake/raw/auto")


def _is_temp_name(name: str) -> bool:
    """True for editor/temp scratch filenames."""
    lowered = name.lower()
    return (
        name.startswith("~")
        or name.startswith(".~")
        or lowered.endswith(".tmp")
        or lowered.endswith(".temp")
        or lowered.endswith(".swp")
        or lowered.endswith(".bak")
        or lowered.endswith("~")
    )


def _should_skip(rel_posix: str, name: str, suffix: str) -> bool:
    """Decide whether a repo-relative path is out of scope for shadow copy."""
    if suffix.lower() not in DOC_SUFFIXES:
        return True
    if name in EXCLUDE_FILENAMES or _is_temp_name(name):
        return True
    for prefix in EXCLUDE_DIR_PREFIXES:
        if rel_posix.startswith(prefix):
            return True
    return False


def _safe_dest(auto_dir: Path, src: Path, digest8: str) -> Path:
    """Collision-safe, dedupe-friendly destination name (stem__hash.ext)."""
    return auto_dir / f"{src.stem}__{digest8}{src.suffix}"


def _append_ledger(ledger: Path, entry: dict) -> None:
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run(payload: dict) -> None:
    """Core logic; assumes a parsed hook payload. Raises only on bugs."""
    tool_name = payload.get("tool_name", "")
    if tool_name not in DOC_TOOLS:
        return

    tool_input = payload.get("tool_input") or {}
    raw_path = tool_input.get("file_path")
    if not raw_path:
        return

    root = Path(payload.get("cwd") or os.getcwd()).resolve()
    src = Path(raw_path)
    if not src.is_absolute():
        src = root / src
    src = src.resolve()

    if not src.is_file():
        return

    try:
        rel = src.relative_to(root)
    except ValueError:
        return  # outside the repo -> not our briefkasten

    rel_posix = rel.as_posix()
    if _should_skip(rel_posix, src.name, src.suffix):
        return

    content = src.read_bytes()
    digest8 = hashlib.sha256(content).hexdigest()[:8]

    today = _dt.date.today().isoformat()
    auto_dir = root / AUTO_REL / today

    dest = _safe_dest(auto_dir, src, digest8)
    dest_rel = dest.relative_to(root).as_posix()
    for prefix in FORBIDDEN_DEST_PREFIXES:
        if dest_rel.startswith(prefix):
            return  # never happens by construction, but guard anyway

    if dest.exists():
        return  # identical content already captured today -> idempotent

    auto_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)  # copy, never move/delete (G3)

    entry = {
        "ts": _dt.datetime.now().isoformat(timespec="seconds"),
        "event": "intake_shadow_copy",
        "tool": tool_name,
        "source": rel_posix,
        "shadow": dest_rel,
        "sha256_8": digest8,
        "status": "raw/auto",
    }
    _append_ledger(auto_dir / "_shadow_log.jsonl", entry)


def main() -> None:
    # Fail-soft wrapper: nothing here may block Claude Code.
    try:
        data = sys.stdin.read()
        if not data.strip():
            return
        payload = json.loads(data)
        run(payload)
    except Exception:  # noqa: BLE001 - advisory hook must never raise  # nosec B110
        pass
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
