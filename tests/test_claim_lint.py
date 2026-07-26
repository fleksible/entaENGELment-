"""Tests for tools/claim_lint.py"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CLAIM_FILES = (
    "Index.html",
    "pyproject.toml",
    "docs/START_HERE.md",
    "docs/triad_topology.md",
    "REPOSITORY_ESSENZ_ANALYSE.md",
)
DISALLOWED_OVERCLAIMS = (
    "physically-enforced resonance",
    "physikalisch erzwungener Resonanz",
    "closes the remote-code-execution surface",
    "messbare nicht-lokale Korrelation",
)


def test_claim_lint_help():
    """Test that claim_lint.py --help works."""
    result = subprocess.run(
        [sys.executable, "tools/claim_lint.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Detect untagged claims" in result.stdout


def test_claim_lint_runs():
    """Test that claim_lint.py runs without errors."""
    result = subprocess.run(
        [sys.executable, "tools/claim_lint.py", "--scope", "index"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLAIM LINT" in result.stdout


def test_claim_lint_shows_valid_tags():
    """Test that claim_lint shows valid tags."""
    result = subprocess.run(
        [sys.executable, "tools/claim_lint.py", "--scope", "index"],
        capture_output=True,
        text=True,
    )
    assert "[FACT]" in result.stdout
    assert "[HYP]" in result.stdout
    assert "[TODO]" in result.stdout


def test_claim_lint_module_import():
    """Test that the claim_lint module can be imported."""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tools.claim_lint import VALID_TAGS; print(VALID_TAGS)",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[FACT]" in result.stdout


def test_claim_lint_empty_scope():
    """Test claim_lint with non-existent directory."""
    result = subprocess.run(
        [sys.executable, "tools/claim_lint.py", "--scope", "nonexistent_dir"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_public_claim_surfaces_exclude_known_overclaims():
    """Keep previously corrected security and physics overclaims from returning."""
    corpus = "\n".join(
        (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in PUBLIC_CLAIM_FILES
    )

    for overclaim in DISALLOWED_OVERCLAIMS:
        assert overclaim not in corpus
