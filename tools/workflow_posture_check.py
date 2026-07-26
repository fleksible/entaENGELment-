#!/usr/bin/env python3
"""Workflow posture drift check.

Scans `.github/workflows/*.yml` and `.github/workflows/*.yaml` and verifies
that each workflow keeps the CI/CD membrane contract:

- a top-level ``permissions`` block is declared;
- a top-level ``concurrency`` block is declared;
- ``concurrency.cancel-in-progress`` is ``true``;
- any top-level or job-level permission broader than ``contents: read`` exactly
  matches a machine-readable exception in ``docs/ci/WORKFLOW_MAP.md``;
- external actions are pinned to full 40-character commit SHAs;
- executable ``run``/``github-script`` bodies do not interpolate Actions
  expressions directly;
- shell commands do not hide failure with ``|| true``;
- reusable calls do not use ``secrets: inherit`` and secrets are not exposed
  through job-wide environment variables.

The check is read-only, deterministic, and needs no network access. It
prints a PASS/FAIL summary and exits non-zero on drift.

Usage:
    python3 tools/workflow_posture_check.py [--root .]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_GLOBS = ("*.yml", "*.yaml")
WORKFLOW_MAP_REL = "docs/ci/WORKFLOW_MAP.md"
FULL_COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
DOCKER_ACTION_DIGEST = re.compile(r"^docker://[^@\s]+@sha256:[0-9a-fA-F]{64}$")
SECRET_EXPRESSION = re.compile(r"\$\{\{[^}]*\bsecrets\b")
PERMISSION_CONTRACT = re.compile(
    r"<!-- workflow-posture-permissions\n(?P<yaml>.*?)\n-->",
    re.DOTALL,
)


def iter_action_nodes(doc: dict[str, Any]):
    """Yield only reusable-job and step mappings where ``uses`` is meaningful."""
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        return
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        if "uses" in job:
            yield job
        steps = job.get("steps")
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict):
                    yield step


def has_direct_expression(script: object) -> bool:
    """Return whether executable code directly contains an Actions expression."""
    return isinstance(script, str) and "${{" in script


def masks_shell_failure(script: object) -> bool:
    """Return whether a shell body masks a failure with ``|| true``."""
    if not isinstance(script, str):
        return False
    return any(
        re.search(r"\|\|\s*true(?:\s*(?:[;&|]|#)|\s*$)", line) for line in script.splitlines()
    )


def load_permission_contract(workflow_map_text: str) -> dict[str, Any]:
    """Load exact broad-permission exceptions from the workflow map."""
    match = PERMISSION_CONTRACT.search(workflow_map_text)
    if match is None:
        return {}
    try:
        contract = yaml.safe_load(match.group("yaml"))
    except yaml.YAMLError:
        return {}
    return contract if isinstance(contract, dict) else {}


def permission_is_documented(
    contract: dict[str, Any],
    workflow_name: str,
    permissions: Any,
    *,
    job_name: str | None = None,
) -> bool:
    """Return whether a broad permission mapping matches its exact exception."""
    workflow = contract.get(workflow_name)
    if not isinstance(workflow, dict):
        return False
    if job_name is None:
        documented = workflow.get("workflow")
    else:
        jobs = workflow.get("jobs")
        documented = jobs.get(job_name) if isinstance(jobs, dict) else None
    return bool(documented == permissions)


def action_reference_problem(uses: str) -> str | None:
    """Return a posture problem for a mutable external action reference."""
    if uses.startswith("./"):
        return None
    if uses.startswith("docker://"):
        if DOCKER_ACTION_DIGEST.fullmatch(uses):
            return None
        return f"Docker action is not pinned to an immutable sha256 digest: {uses}"
    _, separator, ref = uses.rpartition("@")
    if not separator or not FULL_COMMIT_SHA.fullmatch(ref):
        return f"external action is not pinned to a full commit SHA: {uses}"
    return None


def find_workflows(root: Path) -> list[Path]:
    """Return workflow files under ``.github/workflows`` sorted by name."""
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return []
    files: set[Path] = set()
    for pattern in WORKFLOW_GLOBS:
        files.update(wf_dir.glob(pattern))
    return sorted(files, key=lambda p: p.name)


def is_minimal_permissions(permissions: Any) -> bool:
    """True if permissions are no broader than ``contents: read``.

    A mapping is minimal when every entry is ``contents`` set to ``read`` (or
    ``none``). Any extra scope, any ``write`` value, or a broad string form
    such as ``write-all`` counts as broader and must be documented.
    """
    if isinstance(permissions, dict):
        for scope, level in permissions.items():
            if str(scope).strip().lower() != "contents":
                return False
            if str(level).strip().lower() not in ("read", "none"):
                return False
        return True
    # String forms ("read-all", "write-all") or anything else are not minimal.
    return False


def check_workflow(path: Path, permission_contract: dict[str, Any]) -> list[str]:
    """Return a list of posture problems for a single workflow file."""
    problems: list[str] = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        return [f"YAML parse error: {exc}"]

    if not isinstance(doc, dict):
        return ["top-level YAML is not a mapping"]

    # permissions
    if "permissions" not in doc:
        problems.append("missing top-level 'permissions'")
    elif not is_minimal_permissions(doc["permissions"]):
        if not permission_is_documented(
            permission_contract,
            path.name,
            doc["permissions"],
        ):
            problems.append(
                "permissions broader than 'contents: read' are not documented "
                f"or do not exactly match the exception in {WORKFLOW_MAP_REL}"
            )

    jobs = doc.get("jobs")
    if isinstance(jobs, dict):
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            job_permissions = job.get("permissions")
            if job_permissions is not None and not is_minimal_permissions(job_permissions):
                if not permission_is_documented(
                    permission_contract,
                    path.name,
                    job_permissions,
                    job_name=str(job_name),
                ):
                    problems.append(
                        f"job {job_name!r} has permissions broader than "
                        f"'contents: read' that do not exactly match the exception "
                        f"in {WORKFLOW_MAP_REL}"
                    )
            if job.get("secrets") == "inherit":
                problems.append(
                    f"job {job_name!r} uses 'secrets: inherit'; pass only named secrets"
                )
            job_env = job.get("env")
            if isinstance(job_env, dict) and any(
                isinstance(value, str) and SECRET_EXPRESSION.search(value)
                for value in job_env.values()
            ):
                problems.append(
                    f"job {job_name!r} exposes a secret through job-wide env; "
                    "scope it to the consuming step"
                )

    for item in iter_action_nodes(doc):
        uses = item.get("uses")
        if isinstance(uses, str):
            problem = action_reference_problem(uses)
            if problem is not None:
                problems.append(problem)

        run = item.get("run")
        if has_direct_expression(run):
            problems.append(
                "executable 'run' body contains a direct Actions expression; "
                "pass it through a step env variable"
            )
        if masks_shell_failure(run):
            problems.append(
                "shell command masks failure with '|| true'; use an explicit "
                "non-blocking step or handle the exit code"
            )

        with_args = item.get("with")
        script = with_args.get("script") if isinstance(with_args, dict) else None
        if has_direct_expression(script):
            problems.append(
                "github-script body contains a direct Actions expression; "
                "pass it through a step env variable"
            )

    # concurrency
    concurrency = doc.get("concurrency")
    if "concurrency" not in doc:
        problems.append("missing top-level 'concurrency'")
    elif not isinstance(concurrency, dict):
        problems.append("'concurrency' is not a mapping")
    elif concurrency.get("cancel-in-progress") is not True:
        problems.append("'concurrency.cancel-in-progress' is not true")

    return problems


def build_results(root: Path) -> tuple[bool, list[str]]:
    """Run the check and return (ok, report_lines)."""
    workflows = find_workflows(root)
    map_path = root / WORKFLOW_MAP_REL
    workflow_map_text = map_path.read_text(encoding="utf-8") if map_path.exists() else ""
    permission_contract = load_permission_contract(workflow_map_text)

    lines: list[str] = ["# Workflow Posture Check", ""]
    if not workflows:
        lines.append("No workflow files found under .github/workflows/.")
        return True, lines

    all_ok = True
    for wf in workflows:
        problems = check_workflow(wf, permission_contract)
        rel = wf.relative_to(root) if wf.is_relative_to(root) else wf
        if problems:
            all_ok = False
            lines.append(f"FAIL {rel}")
            for problem in problems:
                lines.append(f"  - {problem}")
        else:
            lines.append(f"PASS {rel}")

    lines.append("")
    if all_ok:
        lines.append(f"PASS: {len(workflows)} workflow(s) meet the posture contract.")
    else:
        lines.append("FAIL: workflow posture drift detected. See items above.")
    return all_ok, lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify GitHub Actions workflows declare permissions and "
        "concurrency guards (deterministic, read-only).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=f"Repository root to scan (default: {REPO_ROOT}).",
    )
    args = parser.parse_args(argv)

    ok, lines = build_results(args.root)
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
