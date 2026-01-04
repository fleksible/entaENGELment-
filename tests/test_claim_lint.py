"""Tests for tools/claim_lint.py"""

import subprocess
import sys


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
