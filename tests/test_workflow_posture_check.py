from __future__ import annotations

from pathlib import Path

from tools import workflow_posture_check as wpc


def _make_workflow(root: Path, name: str, body: str) -> None:
    wf_dir = root / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    (wf_dir / name).write_text(body, encoding="utf-8")


def _make_map(root: Path, text: str) -> None:
    map_path = root / "docs" / "ci" / "WORKFLOW_MAP.md"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(text, encoding="utf-8")


GOOD_READ_ONLY = """\
name: Good
on: [push]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  noop:
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
"""


def test_minimal_permissions_helper() -> None:
    assert wpc.is_minimal_permissions({"contents": "read"})
    assert wpc.is_minimal_permissions({"contents": "none"})
    assert not wpc.is_minimal_permissions({"contents": "write"})
    assert not wpc.is_minimal_permissions({"issues": "write", "contents": "read"})
    assert not wpc.is_minimal_permissions("write-all")
    assert not wpc.is_minimal_permissions("read-all")


def test_compliant_workflow_passes(tmp_path: Path) -> None:
    _make_workflow(tmp_path, "ci.yml", GOOD_READ_ONLY)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is True
    report = "\n".join(lines)
    assert "PASS .github/workflows/ci.yml" in report


def test_missing_permissions_fails(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace("permissions:\n  contents: read\n", "")
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("missing top-level 'permissions'" in line for line in lines)


def test_missing_concurrency_fails(tmp_path: Path) -> None:
    body = """\
name: NoConcurrency
on: [push]
permissions:
  contents: read
jobs:
  noop:
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
"""
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("missing top-level 'concurrency'" in line for line in lines)


def test_cancel_in_progress_must_be_true(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace("cancel-in-progress: true", "cancel-in-progress: false")
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("cancel-in-progress" in line for line in lines)


def test_broad_permissions_require_documentation(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace("contents: read", "contents: write")
    _make_workflow(tmp_path, "release.yml", body)
    # Map does NOT mention release.yml.
    _make_map(tmp_path, "# map without the workflow\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("not documented" in line for line in lines)


def test_broad_permissions_pass_when_documented(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace("contents: read", "contents: write")
    _make_workflow(tmp_path, "release.yml", body)
    _make_map(tmp_path, "Exception: `release.yml` keeps `contents: write`.\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is True


def test_no_workflows_is_ok(tmp_path: Path) -> None:
    ok, lines = wpc.build_results(tmp_path)
    assert ok is True
    assert any("No workflow files found" in line for line in lines)


def test_repo_workflows_meet_contract() -> None:
    """The real repository workflows must satisfy the posture contract."""
    ok, lines = wpc.build_results(wpc.REPO_ROOT)
    assert ok is True, "\n".join(lines)
