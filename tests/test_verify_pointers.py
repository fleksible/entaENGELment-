"""Tests for tools/verify_pointers.py"""

import subprocess
import sys


def test_verify_pointers_help():
    """Test that verify_pointers.py --help works."""
    result = subprocess.run(
        [sys.executable, "tools/verify_pointers.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Verify pointers" in result.stdout


def test_verify_pointers_runs():
    """Test that verify_pointers.py runs without errors on the repo."""
    result = subprocess.run(
        [sys.executable, "tools/verify_pointers.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "POINTER VERIFICATION" in result.stdout


def test_verify_pointers_strict_mode():
    """Test that verify_pointers.py --strict mode works."""
    result = subprocess.run(
        [sys.executable, "tools/verify_pointers.py", "--strict"],
        capture_output=True,
        text=True,
    )
    assert "POINTER VERIFICATION" in result.stdout


def test_verify_pointers_detects_valid_paths():
    """Test that verify_pointers finds valid paths."""
    result = subprocess.run(
        [sys.executable, "tools/verify_pointers.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Valid:" in result.stdout


def test_verify_pointers_module_import():
    """Test that the verify_pointers module can be imported."""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tools.verify_pointers import get_repo_root; print(get_repo_root())",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
