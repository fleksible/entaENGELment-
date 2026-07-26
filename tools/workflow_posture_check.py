#!/usr/bin/env python3
"""Workflow posture drift check.

Scans `.github/workflows/*.yml` and `.github/workflows/*.yaml` and verifies
that each workflow keeps the CI/CD membrane contract:

- a top-level ``permissions`` block is declared;
- a top-level ``concurrency`` block is declared;
- ``concurrency.cancel-in-progress`` is ``true``;
- any top-level or job-level permission broader than ``contents: read`` exactly
  matches a current machine-readable exception in ``docs/ci/WORKFLOW_MAP.md``;
- external actions are pinned to full 40-character commit SHAs, including
  actions reached through checked-in composite wrappers;
- executable ``run``/``github-script`` bodies do not interpolate Actions
  expressions directly;
- shell commands do not hide failure with ``|| true``;
- reusable calls do not use ``secrets: inherit`` and secrets are not exposed
  through workflow-wide or job-wide environment variables.

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
CONTAINER_IMAGE_DIGEST = re.compile(r"^[^@\s]+@sha256:[0-9a-fA-F]{64}$")
NAMED_SECRET_REFERENCE = re.compile(
    r"""^\$\{\{\s*secrets(?:\.[A-Za-z0-9_]+|\[['"][A-Za-z0-9_]+['"]\])\s*\}\}$"""
)
PERMISSION_CONTRACT = re.compile(
    r"<!-- workflow-posture-permissions\n(?P<yaml>.*?)\n-->",
    re.DOTALL,
)


def iter_action_nodes(doc: dict[str, Any]):
    """Yield reusable-job and step mappings plus whether each is a step."""
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        return
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        if "uses" in job:
            yield job, False
        steps = job.get("steps")
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict):
                    yield step, True


def has_direct_expression(script: object) -> bool:
    """Return whether executable code directly contains an Actions expression."""
    return isinstance(script, str) and "${{" in script


def masks_shell_failure(script: object) -> bool:
    """Return whether a shell body masks a failure with ``|| true``."""
    if not isinstance(script, str):
        return False
    return bool(
        re.search(
            r"\|\|(?:[ \t]|\\\r?\n|\r?\n)*true" r"(?=[ \t]*(?:[;&|)]|#|\r?$))",
            script,
            re.MULTILINE,
        )
    )


def env_contains_secret(env: object) -> bool:
    """Return whether an environment mapping references the secrets context."""
    return isinstance(env, dict) and any(
        isinstance(value, str) and has_actions_context_reference(value, "secrets")
        for value in env.values()
    )


def has_actions_context_reference(value: str, context: str) -> bool:
    """Find an unquoted context token inside an Actions expression.

    The scanner deliberately does not use ``[^}]*`` as an expression boundary:
    braces are valid inside quoted format strings such as ``'{0}'``.
    """
    lowered_value = value.lower()
    lowered_context = context.lower()
    cursor = 0
    while (expression_start := value.find("${{", cursor)) != -1:
        index = expression_start + 3
        quote: str | None = None
        while index < len(value):
            char = value[index]
            if quote is not None:
                if char == quote:
                    if index + 1 < len(value) and value[index + 1] == quote:
                        index += 2
                        continue
                    quote = None
                index += 1
                continue
            if char in {"'", '"'}:
                quote = char
                index += 1
                continue
            if value.startswith("}}", index):
                cursor = index + 2
                break
            if lowered_value.startswith(lowered_context, index):
                before = value[index - 1] if index > expression_start + 3 else ""
                after_index = index + len(lowered_context)
                after = value[after_index] if after_index < len(value) else ""
                if not (before.isalnum() or before == "_") and not (
                    after.isalnum() or after == "_"
                ):
                    return True
            index += 1
        else:
            return False
    return False


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


def container_image_problem(image: object) -> str | None:
    """Return a posture problem for a mutable job or service image."""
    if not isinstance(image, str):
        return "container image is missing or is not a string"
    if CONTAINER_IMAGE_DIGEST.fullmatch(image):
        return None
    return f"container image is not pinned to an immutable sha256 digest: {image}"


def is_github_script_action(uses: object) -> bool:
    """Return whether a step invokes the official github-script action."""
    return isinstance(uses, str) and uses.lower().startswith("actions/github-script@")


def inspect_action_item(
    item: dict[str, Any],
    *,
    root: Path,
    problems: list[str],
    seen_local_actions: set[Path],
    is_step: bool,
    context: str = "",
) -> None:
    """Inspect one reusable job or action step and recurse into local composites."""

    def add_problem(problem: str) -> None:
        problems.append(f"{context}: {problem}" if context else problem)

    uses = item.get("uses")
    if isinstance(uses, str):
        problem = action_reference_problem(uses)
        if problem is not None:
            add_problem(problem)

    run = item.get("run")
    if has_direct_expression(run):
        add_problem(
            "executable 'run' body contains a direct Actions expression; "
            "pass it through a step env variable"
        )
    if masks_shell_failure(run):
        add_problem(
            "shell command masks failure with '|| true'; use an explicit "
            "non-blocking step or handle the exit code"
        )

    with_args = item.get("with")
    script = with_args.get("script") if isinstance(with_args, dict) else None
    if is_github_script_action(uses) and has_direct_expression(script):
        add_problem(
            "github-script body contains a direct Actions expression; "
            "pass it through a step env variable"
        )

    if not (is_step and isinstance(uses, str) and uses.startswith("./")):
        return

    repo_root = root.resolve()
    action_dir = (repo_root / uses[2:]).resolve()
    if not action_dir.is_relative_to(repo_root):
        add_problem(f"local action path escapes the repository: {uses}")
        return

    manifest = next(
        (
            candidate
            for candidate in (action_dir / "action.yml", action_dir / "action.yaml")
            if candidate.is_file()
        ),
        None,
    )
    if manifest is None:
        add_problem(f"local action manifest not found: {uses}")
        return
    if manifest in seen_local_actions:
        return
    seen_local_actions.add(manifest)

    try:
        action_doc = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        add_problem(f"local action manifest has invalid YAML ({manifest}): {exc}")
        return
    if not isinstance(action_doc, dict):
        add_problem(f"local action manifest is not a mapping: {manifest}")
        return

    runs = action_doc.get("runs")
    if not isinstance(runs, dict) or str(runs.get("using")).lower() != "composite":
        return
    steps = runs.get("steps")
    if not isinstance(steps, list):
        add_problem(f"composite action has no valid steps list: {manifest}")
        return

    manifest_context = str(manifest.relative_to(repo_root))
    for step in steps:
        if not isinstance(step, dict):
            problems.append(f"{manifest_context}: composite step is not a mapping")
            continue
        inspect_action_item(
            step,
            root=repo_root,
            problems=problems,
            seen_local_actions=seen_local_actions,
            is_step=True,
            context=manifest_context,
        )


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


def stale_permission_exception_problems(
    workflows: list[Path],
    permission_contract: dict[str, Any],
) -> list[str]:
    """Return exceptions that no longer match a current broad permission."""
    problems: list[str] = []
    workflow_paths = {path.name: path for path in workflows}

    for workflow_name, exception in permission_contract.items():
        path = workflow_paths.get(str(workflow_name))
        if path is None:
            problems.append(f"stale permission exception names missing workflow {workflow_name!r}")
            continue
        if not isinstance(exception, dict):
            problems.append(f"permission exception for {workflow_name!r} is not a mapping")
            continue
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(doc, dict):
            continue

        if "workflow" in exception:
            actual = doc.get("permissions")
            if actual != exception["workflow"] or is_minimal_permissions(actual):
                problems.append(f"stale permission exception for {workflow_name!r} workflow scope")

        jobs_exception = exception.get("jobs")
        if jobs_exception is None:
            continue
        if not isinstance(jobs_exception, dict):
            problems.append(f"permission job exceptions for {workflow_name!r} are not a mapping")
            continue
        jobs = doc.get("jobs")
        for job_name, documented in jobs_exception.items():
            job = jobs.get(job_name) if isinstance(jobs, dict) else None
            actual = job.get("permissions") if isinstance(job, dict) else None
            if actual != documented or is_minimal_permissions(actual):
                problems.append(
                    f"stale permission exception for {workflow_name!r} " f"job {job_name!r}"
                )

    return problems


def check_workflow(path: Path, permission_contract: dict[str, Any]) -> list[str]:
    """Return a list of posture problems for a single workflow file."""
    problems: list[str] = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        return [f"YAML parse error: {exc}"]

    if not isinstance(doc, dict):
        return ["top-level YAML is not a mapping"]

    if env_contains_secret(doc.get("env")):
        problems.append(
            "workflow exposes a secret through workflow-wide env; " "scope it to the consuming step"
        )

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
            job_secrets = job.get("secrets")
            if job_secrets == "inherit":
                problems.append(
                    f"job {job_name!r} uses 'secrets: inherit'; pass only named secrets"
                )
            elif isinstance(job_secrets, dict):
                for secret_name, value in job_secrets.items():
                    if not isinstance(value, str) or not NAMED_SECRET_REFERENCE.fullmatch(value):
                        problems.append(
                            f"job {job_name!r} secret {secret_name!r} is not an "
                            "explicit named secrets reference"
                        )
            elif job_secrets is not None:
                problems.append(
                    f"job {job_name!r} has an invalid secrets mapping; " "pass only named secrets"
                )
            if env_contains_secret(job.get("env")):
                problems.append(
                    f"job {job_name!r} exposes a secret through job-wide env; "
                    "scope it to the consuming step"
                )

            container = job.get("container")
            if container is not None:
                image = container.get("image") if isinstance(container, dict) else container
                problem = container_image_problem(image)
                if problem is not None:
                    problems.append(f"job {job_name!r} {problem}")

            services = job.get("services")
            if isinstance(services, dict):
                for service_name, service in services.items():
                    image = service.get("image") if isinstance(service, dict) else None
                    problem = container_image_problem(image)
                    if problem is not None:
                        problems.append(f"job {job_name!r} service {service_name!r} {problem}")

    root = path.parents[2]
    seen_local_actions: set[Path] = set()
    for item, is_step in iter_action_nodes(doc):
        inspect_action_item(
            item,
            root=root,
            problems=problems,
            seen_local_actions=seen_local_actions,
            is_step=is_step,
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
    contract_problems = stale_permission_exception_problems(
        workflows,
        permission_contract,
    )
    if contract_problems:
        all_ok = False
        lines.append(f"FAIL {WORKFLOW_MAP_REL}")
        for problem in contract_problems:
            lines.append(f"  - {problem}")

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
