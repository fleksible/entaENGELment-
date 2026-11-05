"""Counterfixtures: the full-lock audit must fail closed on partial or dirty reports."""

import pytest

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
