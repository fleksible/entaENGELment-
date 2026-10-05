"""Guard tests for the sealed skill-stack evaluation freeze (commit-reveal).

The freeze records only SHA-256 hashes of the evaluation material (protocol,
rubric, conventional-mode prompt, cases, keys). Public plaintext is revealed
into the repository only after all evaluation runs; hidden plaintext never is.

These tests make the reveal checkable and keep hidden material out of the repo:

- a revealed public file must match its frozen hash;
- a hidden path must never exist;
- no frozen content may appear anywhere else in the working tree;
- the reveal root holds nothing but the freeze and declared public files.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FREEZE_PATH = REPO_ROOT / ".claude" / "skills" / "eval" / "FREEZE.json"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VISIBILITIES = {"public", "hidden"}
SCAN_SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".turbo",
    ".next",
    "htmlcov",
}
SCAN_MAX_BYTES = 2 * 1024 * 1024


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def freeze() -> dict:
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def entries(freeze: dict) -> list[dict]:
    return freeze["entries"]


def test_freeze_top_level_contract(freeze: dict) -> None:
    assert freeze["schema_version"] == "skill-eval-freeze.v0.1"
    assert freeze["hash_alg"] == "sha256"
    assert freeze["reveal_root"] == ".claude/skills/eval"
    assert freeze["evaluation_kind"].startswith("sealed")
    assert freeze["limitations"], "the sealed-not-blind limitation must stay documented"
    assert isinstance(freeze["entries"], list) and freeze["entries"]


def test_entries_are_well_formed(freeze: dict, entries: list[dict]) -> None:
    root = freeze["reveal_root"] + "/"
    ids = [e["id"] for e in entries]
    paths = [e["path"] for e in entries]
    assert len(ids) == len(set(ids)), "duplicate entry id"
    assert len(paths) == len(set(paths)), "duplicate entry path"
    for entry in entries:
        assert SHA256_RE.match(entry["sha256"]), entry["id"]
        assert entry["visibility"] in VISIBILITIES, entry["id"]
        assert entry["path"].startswith(root), entry["path"]
        assert ".." not in Path(entry["path"]).parts, entry["path"]
        assert "\\" not in entry["path"], entry["path"]


def test_every_case_has_a_key_and_hidden_cases_exist(entries: list[dict]) -> None:
    by_id = {e["id"]: e for e in entries}
    cases = [i for i in by_id if i.endswith("_case")]
    assert cases
    for case_id in cases:
        key_id = case_id[: -len("_case")] + "_key"
        assert key_id in by_id, f"{case_id} has no key"
        assert by_id[key_id]["visibility"] == by_id[case_id]["visibility"]
    hidden_cases = [i for i in cases if by_id[i]["visibility"] == "hidden"]
    assert len(hidden_cases) >= 2, "held-out cases H1/H2 must stay registered"


def test_revealed_public_files_match_frozen_hash(entries: list[dict]) -> None:
    for entry in entries:
        if entry["visibility"] != "public":
            continue
        path = REPO_ROOT / entry["path"]
        if path.exists():
            assert _sha256(path) == entry["sha256"], f"reveal mismatch: {entry['path']}"


def test_hidden_paths_never_exist(entries: list[dict]) -> None:
    for entry in entries:
        if entry["visibility"] == "hidden":
            assert not (REPO_ROOT / entry["path"]).exists(), f"hidden file present: {entry['path']}"


def test_reveal_root_holds_only_declared_files(freeze: dict, entries: list[dict]) -> None:
    root = REPO_ROOT / freeze["reveal_root"]
    declared = {e["path"] for e in entries if e["visibility"] == "public"}
    declared.add(FREEZE_PATH.relative_to(REPO_ROOT).as_posix())
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(REPO_ROOT).as_posix()
            assert rel in declared, f"undeclared file in eval reveal root: {rel}"


def test_frozen_content_does_not_appear_elsewhere(entries: list[dict]) -> None:
    hidden = {e["sha256"] for e in entries if e["visibility"] == "hidden"}
    public = {e["sha256"]: e["path"] for e in entries if e["visibility"] == "public"}
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SCAN_SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink() or path.stat().st_size > SCAN_MAX_BYTES:
                continue
            digest = _sha256(path)
            rel = path.relative_to(REPO_ROOT).as_posix()
            assert digest not in hidden, f"hidden evaluation content found at {rel}"
            if digest in public:
                assert rel == public[digest], f"frozen content outside reveal path: {rel}"
