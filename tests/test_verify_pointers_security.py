"""Security-focused tests for tools/verify_pointers.py

These tests ensure that pointer verification cannot be bypassed via
directory traversal (e.g. "../secrets.json").
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def test_rejects_pointer_escape_repo_root() -> None:
    """Pointers that resolve outside the repo root must be rejected."""
    # Get absolute path to verify_pointers.py in the actual repo
    script_path = Path(__file__).parent.parent / "tools" / "verify_pointers.py"
    # Use system python (not pytest's python) which has PyYAML
    python_exe = shutil.which("python") or "/usr/local/bin/python"

    with TemporaryDirectory() as td:
        td_path = Path(td)
        repo_root = td_path / "repo"
        repo_root.mkdir()
        (repo_root / "index").mkdir()

        # Create a YAML with a pointer that escapes the repo
        # index/../outside.txt resolves to repo/outside.txt (still inside)
        # index/../../outside.txt resolves to /tmp/outside.txt (outside!)
        (repo_root / "index" / "test.yaml").write_text(
            "pointer: ../../outside.txt\n", encoding="utf-8"
        )
        # Create the file outside the repo that would be found by traversal
        (td_path / "outside.txt").write_text("secret\n", encoding="utf-8")

        # Run verify_pointers on this test repo
        result = subprocess.run(
            [python_exe, str(script_path), "--repo-root", str(repo_root)],
            capture_output=True,
            text=True,
        )

        # Should fail due to invalid pointer that escapes root
        assert (
            result.returncode != 0
        ), f"Should reject pointers that escape repo root. Output:\n{result.stdout}"
        assert (
            "Invalid" in result.stdout or "escape" in result.stdout.lower()
        ), f"Expected 'Invalid' or 'escape' in output:\n{result.stdout}"


def test_allows_dotdot_when_it_stays_inside_repo() -> None:
    """Relative paths with .. are OK if they still resolve inside repo root."""
    # Get absolute path to verify_pointers.py in the actual repo
    script_path = Path(__file__).parent.parent / "tools" / "verify_pointers.py"
    # Use system python (not pytest's python) which has PyYAML
    python_exe = shutil.which("python") or "/usr/local/bin/python"

    with TemporaryDirectory() as td:
        td_path = Path(td)
        repo_root = td_path / "repo"
        (repo_root / "index").mkdir(parents=True)
        (repo_root / "README.md").write_text("ok\n", encoding="utf-8")

        # YAML in index/ references ../README.md which stays inside repo
        yaml_path = repo_root / "index" / "sample.yaml"
        yaml_path.write_text("doc: ../README.md\n", encoding="utf-8")

        # Run verify_pointers
        result = subprocess.run(
            [python_exe, str(script_path), "--repo-root", str(repo_root)],
            capture_output=True,
            text=True,
        )

        # Should succeed - the ../ stays within repo root
        assert (
            result.returncode == 0
        ), f"Should allow .. paths that stay in repo. Output:\n{result.stdout}"
        assert "README.md" in result.stdout, f"Expected README.md in output:\n{result.stdout}"
