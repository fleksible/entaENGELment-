"""Exercise the workflow fragments that decide whether checks can pass."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(shutil.which("bash") is None, reason="Bash is required")


def _steps(workflow: str, job: str) -> list[dict]:
    document = yaml.safe_load((ROOT / ".github/workflows" / workflow).read_text())
    return document["jobs"][job]["steps"]


def _run(script: str, cwd: Path, **values: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, **values}
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )


@pytest.fixture
def metatron_workspace(tmp_path: Path) -> Path:
    (tmp_path / "tools").mkdir()
    shutil.copyfile(ROOT / "tools/metatron_check.py", tmp_path / "tools/metatron_check.py")
    return tmp_path


def _metatron_script() -> str:
    return next(
        step["run"]
        for step in _steps("metatron-guard.yml", "metatron-pr-check")
        if "PR_BODY" in step.get("env", {})
    )


@pytest.mark.parametrize(
    "body",
    [
        "",
        "Documentation update without a focus marker.",
        "FOKUS: Parser\nFOKUS-SWITCH: Parser -> UI\nChanged task.",
        "FOKUS: Parser\nFOKUS-SWITCH: Parser -> UI\nProceed?\n"
        "FOKUS-SWITCH: UI -> Release\nChanged task again.",
        "FOKUS: Parser\nFOKUS-SWITCH 1: Parser -> UI\nChanged task.",
        "FOKUS: Parser\nFOKUS-SWITCH 1: Parser -> UI\n"
        "FOKUS-SWITCH 2: UI -> Release\nProceed with the second switch?",
    ],
    ids=["empty", "missing-focus", "missing-question", "second-switch", "numbered", "borrowed"],
)
def test_pr_guard_rejects_rule_violations(metatron_workspace: Path, body: str) -> None:
    result = _run(_metatron_script(), metatron_workspace, PR_BODY=body)
    assert result.returncode != 0, result.stdout


@pytest.mark.parametrize(
    "body",
    [
        "FOKUS: Parser",
        "FOKUS: Parser\nFOKUS-SWITCH: Parser -> UI\nProceed?",
        "FOKUS: Parser\nFOKUS-SWITCH 1: Parser -> UI\nProceed?\n"
        "FOKUS-SWITCH 2: UI -> Release\nProceed again?",
    ],
)
def test_pr_guard_accepts_documented_focus(metatron_workspace: Path, body: str) -> None:
    result = _run(_metatron_script(), metatron_workspace, PR_BODY=body)
    assert result.returncode == 0, result.stdout + result.stderr


def test_pr_guard_rejects_execution_error(tmp_path: Path) -> None:
    result = _run(_metatron_script(), tmp_path, PR_BODY="FOKUS: Parser")
    assert result.returncode != 0


@pytest.mark.parametrize("job", ["JS_RESULT", "PYTHON_RESULT", "UI_RESULT"])
@pytest.mark.parametrize("outcome", ["failure", "skipped", "cancelled", ""])
def test_test_aggregate_rejects_non_success(tmp_path: Path, job: str, outcome: str) -> None:
    step = _steps("test.yml", "all-tests-pass")[0]
    values = {"JS_RESULT": "success", "PYTHON_RESULT": "success", "UI_RESULT": "success"}
    values[job] = outcome
    assert _run(step["run"], tmp_path, **values).returncode != 0


def test_test_aggregate_accepts_success(tmp_path: Path) -> None:
    step = _steps("test.yml", "all-tests-pass")[0]
    result = _run(
        step["run"], tmp_path, JS_RESULT="success", PYTHON_RESULT="success", UI_RESULT="success"
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("allow_skip", "key", "expected_exit", "expected_output"),
    [
        ("true", "", 0, "available=false\nskip_allowed=true\n"),
        ("false", "", 1, "available=false\nskip_allowed=false\n"),
        ("false", "synthetic-test-key", 0, "available=true\nskip_allowed=false\n"),
    ],
)
def test_hmac_availability_contract(
    tmp_path: Path, allow_skip: str, key: str, expected_exit: int, expected_output: str
) -> None:
    step = next(
        step
        for step in _steps("deepjump-audit.reusable.yml", "deepjump-audit")
        if step.get("id") == "hmac"
    )
    output = tmp_path / "github-output"
    result = _run(
        step["run"],
        tmp_path,
        ALLOW_UNSIGNED_STATUS_SKIP=allow_skip,
        ENTA_HMAC_SECRET=key,
        GITHUB_OUTPUT=str(output),
    )
    assert result.returncode == expected_exit, result.stdout + result.stderr
    assert output.read_text() == expected_output
