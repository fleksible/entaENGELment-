"""Counterfixtures: the full-lock audit must fail closed on partial or dirty reports."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import python_lock
from tools.python_lock import COMMANDS, audit_problems

EXPECTED = {("pillow", "13.0.0"), ("pyyaml", "6.0.3")}


def report(*deps):
    return {"dependencies": list(deps)}


def clean(name, version):
    return {"name": name, "version": version, "vulns": []}


def test_clean_report_covering_every_locked_package_passes():
    assert (
        audit_problems(report(clean("Pillow", "13.0.0"), clean("PyYAML", "6.0.3")), EXPECTED) == []
    )


def test_known_vulnerability_is_reported_with_fix_version():
    dirty = {
        "name": "pillow",
        "version": "13.0.0",
        "vulns": [{"id": "PYSEC-X", "fix_versions": ["13.0.1"]}],
    }
    problems = audit_problems(report(dirty, clean("pyyaml", "6.0.3")), EXPECTED)
    assert problems == ["pillow==13.0.0: PYSEC-X (fixed in: 13.0.1)"]


def test_vulnerability_without_published_fix_still_fails():
    dirty = {"name": "pyyaml", "version": "6.0.3", "vulns": [{"id": "GHSA-Y", "fix_versions": []}]}
    problems = audit_problems(report(clean("pillow", "13.0.0"), dirty), EXPECTED)
    assert problems == ["pyyaml==6.0.3: GHSA-Y (fixed in: none published)"]


@pytest.mark.parametrize(
    "mutation",
    ["skipped", "missing", "wrong_version", "no_list", "malformed_entry"],
)
def test_partial_audit_fails_closed(mutation):
    deps = [clean("pillow", "13.0.0"), clean("pyyaml", "6.0.3")]
    if mutation == "skipped":
        deps[1] = {"name": "pyyaml", "skip_reason": "Dependency not found on PyPI"}
    elif mutation == "missing":
        deps.pop()
    elif mutation == "wrong_version":
        deps[1] = clean("pyyaml", "6.0.2")
    elif mutation == "malformed_entry":
        deps.append("pyyaml==6.0.3")
    data = {"dependencies": "broken"} if mutation == "no_list" else report(*deps)
    assert audit_problems(data, EXPECTED)


def test_audit_is_a_cli_command():
    assert "audit" in COMMANDS


@pytest.mark.parametrize(
    ("returncode", "payload", "expected_exit", "diagnostic"),
    [
        (0, "clean", 0, "PASS: all 2 locked package versions audited"),
        (7, "clean", 1, "pip-audit exited 7 without a reported finding"),
        (-9, "clean", 1, "pip-audit exited -9 without a reported finding"),
        (0, "absent", 1, "pip-audit wrote no report"),
        (0, "invalid_json", 1, "FAIL:"),
        (0, "partial", 1, "not audited: pyyaml==6.0.3"),
        (0, "skipped", 1, "pyyaml not audited:"),
        (0, "vulnerable", 1, "PYSEC-X"),
    ],
)
def test_audit_cli_preserves_scanner_failure_and_coverage(
    monkeypatch, capsys, returncode, payload, expected_exit, diagnostic
):
    """Exercise the CLI boundary with controlled external-tool outputs."""

    def export_lock(args, *, capture=False):
        output = Path(args[args.index("--output-file") + 1])
        output.write_text(
            '[[packages]]\nname = "pillow"\nversion = "13.0.0"\n'
            '[[packages]]\nname = "pyyaml"\nversion = "6.0.3"\n',
            encoding="utf-8",
        )
        return ""

    def run_scanner(args, **kwargs):
        data = report(clean("pillow", "13.0.0"), clean("pyyaml", "6.0.3"))
        if payload == "partial":
            data["dependencies"].pop()
        elif payload == "skipped":
            data["dependencies"][1] = {"name": "pyyaml", "skip_reason": "unavailable"}
        elif payload == "vulnerable":
            data["dependencies"][0]["vulns"] = [{"id": "PYSEC-X", "fix_versions": []}]
        if payload != "absent":
            output = Path(args[args.index("--output") + 1])
            output.write_text(
                "{" if payload == "invalid_json" else json.dumps(data), encoding="utf-8"
            )
        return subprocess.CompletedProcess(args, returncode)

    monkeypatch.setattr(python_lock, "check", lambda: None)
    monkeypatch.setattr(python_lock, "uv", export_lock)
    monkeypatch.setattr(python_lock.shutil, "which", lambda name: "pip-audit")
    monkeypatch.setattr(python_lock.subprocess, "run", run_scanner)
    monkeypatch.setattr(sys, "argv", ["python_lock.py", "audit"])

    assert python_lock.main() == expected_exit
    output = capsys.readouterr()
    assert diagnostic in output.out + output.err
    if expected_exit:
        assert "PASS:" not in output.out
