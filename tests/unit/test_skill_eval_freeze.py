"""Guard tests for the sealed skill-stack evaluation freeze (commit-reveal).

The freeze records only SHA-256 hashes of the evaluation material (protocol,
rubric, conventional-mode prompt, cases, keys). Public plaintext is revealed
into the repository only after all evaluation runs; hidden plaintext never is.

These tests make the reveal checkable and keep hidden material out of the repo:

- FREEZE.json itself is pinned: changing a frozen hash requires changing this test;
- revealed public files must match their frozen hash, and only a complete reveal passes;
- hidden paths must never exist;
- no frozen content may appear in any file git could commit, outside its reveal path;
- the reveal root holds nothing but the freeze and declared public files.

Scope of the content scan: files listed by ``git ls-files --cached --others
--exclude-standard`` (tracked plus committable untracked files). It detects
byte-identical copies only, not edited or paraphrased ones.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FREEZE_PATH = REPO_ROOT / ".claude" / "skills" / "eval" / "FREEZE.json"

# Pin of FREEZE.json. The freeze is never edited after it is merged; any change
# to a frozen hash therefore also has to change this constant in the same diff.
FREEZE_SHA256 = "fdfbd4dfd364ca448c980794bb55fab3efbab514801bcb73135fc8a8e1640405"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VISIBILITIES = {"public", "hidden"}
SCAN_MAX_BYTES = 5 * 1024 * 1024


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _committable_files() -> list[str]:
    """Repo-relative paths git could commit: tracked plus untracked, not ignored."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("content scan needs a git working tree")
    return [p for p in result.stdout.decode("utf-8").split("\0") if p]


@pytest.fixture(scope="module")
def freeze() -> dict:
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def entries(freeze: dict) -> list[dict]:
    return freeze["entries"]


def test_freeze_file_is_pinned() -> None:
    assert _sha256(FREEZE_PATH) == FREEZE_SHA256, "FREEZE.json changed after the freeze"


def test_freeze_top_level_contract(freeze: dict) -> None:
    assert freeze["schema_version"] == "skill-eval-freeze.v0.1"
    assert freeze["hash_alg"] == "sha256"
    assert freeze["reveal_root"] == ".claude/skills/eval"
    assert freeze["evaluation_kind"].startswith("sealed")
    assert freeze["limitations"], "the sealed-not-blind limitation must stay documented"
    assert "nonce" in freeze["commitment_scheme"]
    assert isinstance(freeze["entries"], list) and freeze["entries"]


def test_entries_are_well_formed(freeze: dict, entries: list[dict]) -> None:
    root = freeze["reveal_root"] + "/"
    ids = [e["id"] for e in entries]
    paths = [e["path"].lower() for e in entries]
    digests = [e["sha256"] for e in entries]
    assert len(ids) == len(set(ids)), "duplicate entry id"
    assert len(paths) == len(set(paths)), "duplicate entry path (case-insensitive)"
    assert len(digests) == len(set(digests)), "duplicate digest: commitments must be distinct"
    for entry in entries:
        assert SHA256_RE.match(entry["sha256"]), entry["id"]
        assert entry["visibility"] in VISIBILITIES, entry["id"]
        assert entry["path"].startswith(root), entry["path"]
        assert ".." not in Path(entry["path"]).parts, entry["path"]
        assert "\\" not in entry["path"], entry["path"]


def test_cases_and_keys_pair_up(entries: list[dict]) -> None:
    by_id = {e["id"]: e for e in entries}
    cases = {i[: -len("_case")] for i in by_id if i.endswith("_case")}
    keys = {i[: -len("_key")] for i in by_id if i.endswith("_key")}
    assert cases, "no cases registered"
    assert cases == keys, f"unpaired cases/keys: {sorted(cases ^ keys)}"
    for stem in cases:
        assert by_id[f"{stem}_case"]["visibility"] == by_id[f"{stem}_key"]["visibility"]
    hidden_cases = [s for s in cases if by_id[f"{s}_case"]["visibility"] == "hidden"]
    assert len(hidden_cases) >= 2, "held-out cases H1/H2 must stay registered"


def test_public_reveal_is_complete_and_matches(entries: list[dict]) -> None:
    public = [e for e in entries if e["visibility"] == "public"]
    present = [e for e in public if (REPO_ROOT / e["path"]).exists()]
    assert len(present) in (0, len(public)), (
        "partial reveal: " f"missing {sorted(e['path'] for e in public if e not in present)}"
    )
    for entry in present:
        assert (
            _sha256(REPO_ROOT / entry["path"]) == entry["sha256"]
        ), f"reveal mismatch: {entry['path']}"


def test_hidden_paths_never_exist(freeze: dict, entries: list[dict]) -> None:
    hidden = {e["path"].lower() for e in entries if e["visibility"] == "hidden"}
    root = REPO_ROOT / freeze["reveal_root"]
    for path in root.rglob("*"):
        rel = path.relative_to(REPO_ROOT).as_posix().lower()
        assert rel not in hidden, f"hidden file present: {rel}"


def test_reveal_root_holds_only_declared_files(freeze: dict, entries: list[dict]) -> None:
    root = freeze["reveal_root"] + "/"
    declared = {e["path"] for e in entries if e["visibility"] == "public"}
    declared.add(FREEZE_PATH.relative_to(REPO_ROOT).as_posix())
    for rel in _committable_files():
        if rel.startswith(root):
            assert rel in declared, f"undeclared file in eval reveal root: {rel}"


def test_frozen_content_does_not_appear_elsewhere(entries: list[dict]) -> None:
    hidden = {e["sha256"] for e in entries if e["visibility"] == "hidden"}
    public = {e["sha256"]: e["path"] for e in entries if e["visibility"] == "public"}
    for rel in _committable_files():
        path = REPO_ROOT / rel
        try:
            if path.is_symlink() or not path.is_file():
                continue
            if path.stat().st_size > SCAN_MAX_BYTES:
                continue
            digest = _sha256(path)
        except OSError:
            continue
        assert digest not in hidden, f"hidden evaluation content found at {rel}"
        if digest in public:
            assert rel == public[digest], f"frozen content outside reveal path: {rel}"
