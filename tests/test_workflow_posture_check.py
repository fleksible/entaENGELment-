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


def _make_local_action(root: Path, relative_dir: str, body: str) -> None:
    action_dir = root / relative_dir
    action_dir.mkdir(parents=True, exist_ok=True)
    (action_dir / "action.yml").write_text(body, encoding="utf-8")


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
    _make_map(
        tmp_path,
        "<!-- workflow-posture-permissions\n"
        "release.yml:\n"
        "  workflow:\n"
        "    contents: write\n"
        "-->\n",
    )

    ok, lines = wpc.build_results(tmp_path)

    assert ok is True


def test_documented_filename_does_not_allow_a_different_scope(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "contents: read",
        "contents: read\n  issues: write",
    )
    _make_workflow(tmp_path, "release.yml", body)
    _make_map(
        tmp_path,
        "<!-- workflow-posture-permissions\n"
        "release.yml:\n"
        "  workflow:\n"
        "    contents: write\n"
        "-->\n",
    )

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("do not exactly match" in line for line in lines)


def test_job_level_broad_permissions_require_documentation(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "permissions:\n      contents: write\n    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "release.yml", body)
    _make_map(tmp_path, "# map without the workflow\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("job 'noop' has permissions broader" in line for line in lines)


def test_job_level_broad_permissions_match_exact_exception(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "permissions:\n      contents: write\n    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "release.yml", body)
    _make_map(
        tmp_path,
        "<!-- workflow-posture-permissions\n"
        "release.yml:\n"
        "  jobs:\n"
        "    noop:\n"
        "      contents: write\n"
        "-->\n",
    )

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_stale_permission_exception_is_rejected(tmp_path: Path) -> None:
    _make_workflow(tmp_path, "release.yml", GOOD_READ_ONLY)
    _make_map(
        tmp_path,
        "<!-- workflow-posture-permissions\n"
        "release.yml:\n"
        "  workflow:\n"
        "    contents: write\n"
        "-->\n",
    )

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("stale permission exception" in line for line in lines)


def test_external_actions_must_use_full_commit_sha(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: actions/checkout@v7",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("not pinned to a full commit SHA" in line for line in lines)


def test_full_sha_and_local_actions_are_allowed(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0\n"
        "      - uses: ./.github/actions/local",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_local_action(
        tmp_path,
        ".github/actions/local",
        "name: Local\n"
        "description: Local test action\n"
        "runs:\n"
        "  using: composite\n"
        "  steps:\n"
        "    - run: echo local\n"
        "      shell: bash\n",
    )
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_local_composite_actions_cannot_hide_mutable_external_actions(
    tmp_path: Path,
) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: ./.github/actions/wrapper",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_local_action(
        tmp_path,
        ".github/actions/wrapper",
        "name: Wrapper\n"
        "description: Wrapper test action\n"
        "runs:\n"
        "  using: composite\n"
        "  steps:\n"
        "    - uses: actions/checkout@v7\n",
    )
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("not pinned to a full commit SHA" in line for line in lines)


def test_nested_local_composites_are_scanned_recursively(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: ./.github/actions/outer",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_local_action(
        tmp_path,
        ".github/actions/outer",
        "name: Outer\n"
        "description: Outer wrapper\n"
        "runs:\n"
        "  using: composite\n"
        "  steps:\n"
        "    - uses: ./.github/actions/inner\n",
    )
    _make_local_action(
        tmp_path,
        ".github/actions/inner",
        "name: Inner\n"
        "description: Inner wrapper\n"
        "runs:\n"
        "  using: composite\n"
        "  steps:\n"
        "    - uses: actions/checkout@v7\n",
    )
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("not pinned to a full commit SHA" in line for line in lines)


def test_docker_actions_require_immutable_digest(tmp_path: Path) -> None:
    mutable = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: docker://vendor/image:latest",
    )
    _make_workflow(tmp_path, "ci.yml", mutable)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("immutable sha256 digest" in line for line in lines)


def test_digest_pinned_docker_action_is_allowed(tmp_path: Path) -> None:
    digest = "a" * 64
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        f"- uses: docker://vendor/image@sha256:{digest}",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_job_and_service_containers_require_immutable_digests(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "container:\n"
        "      image: vendor/job:latest\n"
        "    services:\n"
        "      database:\n"
        "        image: vendor/database:latest\n"
        "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert sum("immutable sha256 digest" in line for line in lines) == 2


def test_digest_pinned_job_and_service_containers_are_allowed(tmp_path: Path) -> None:
    digest = "b" * 64
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        f"container: vendor/job@sha256:{digest}\n"
        "    services:\n"
        "      database:\n"
        f"        image: vendor/database@sha256:{digest}\n"
        "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_non_action_uses_field_is_ignored(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "env:\n      uses: helper\n    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_executable_expressions_must_pass_through_env(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        '- run: echo "${{ github.event.pull_request.title }}"',
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("direct Actions expression" in line for line in lines)


def test_github_script_expressions_are_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3\n"
        "        with:\n"
        "          script: console.log('${{ github.event.issue.title }}')",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("github-script body" in line for line in lines)


def test_other_actions_may_use_script_as_data_input(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- uses: vendor/custom-action@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
        "        with:\n"
        "          script: ${{ github.event.issue.title }}",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_shell_failure_mask_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace("- run: echo ok", "- run: generate-sbom || true")
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("masks failure" in line for line in lines)


def test_shell_failure_mask_before_separator_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- run: generate-sbom || true; echo done",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("masks failure" in line for line in lines)


def test_shell_failure_mask_before_closing_subshell_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- run: (generate-sbom || true)",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("masks failure" in line for line in lines)


def test_shell_failure_mask_across_newline_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "- run: echo ok",
        "- run: |\n" "          generate-sbom ||\n" "            true\n",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("masks failure" in line for line in lines)


def test_workflow_wide_secret_environment_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "concurrency:",
        "env:\n" "  TOKEN: ${{ secrets.REPO_TOKEN }}\n" "concurrency:",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("workflow-wide env" in line for line in lines)


def test_secret_environment_detection_scans_past_quoted_braces(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "env:\n"
        "      TOKEN: ${{ format('{0}', secrets.REPO_TOKEN) }}\n"
        "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("job-wide env" in line for line in lines)


def test_inherited_and_job_wide_secrets_are_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "secrets: inherit\n"
        "    env:\n"
        "      TOKEN: ${{ secrets.REPO_TOKEN }}\n"
        "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    report = "\n".join(lines)
    assert "secrets: inherit" in report
    assert "job-wide env" in report


def test_reusable_call_secret_mapping_requires_named_secret_reference(
    tmp_path: Path,
) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "secrets:\n" "      ALL_SECRETS: ${{ toJSON(secrets) }}\n" "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("explicit named secrets reference" in line for line in lines)


def test_reusable_call_named_secret_mapping_is_allowed(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "secrets:\n" "      TOKEN: ${{ secrets.REPO_TOKEN }}\n" "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, _ = wpc.build_results(tmp_path)

    assert ok is True


def test_bracketed_job_wide_secret_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "env:\n" "      TOKEN: ${{ secrets['REPO_TOKEN'] }}\n" "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("job-wide env" in line for line in lines)


def test_whole_context_job_wide_secret_is_rejected(tmp_path: Path) -> None:
    body = GOOD_READ_ONLY.replace(
        "runs-on: ubuntu-latest",
        "env:\n" "      ALL_SECRETS: ${{ toJSON(secrets) }}\n" "    runs-on: ubuntu-latest",
    )
    _make_workflow(tmp_path, "ci.yml", body)
    _make_map(tmp_path, "# map\n")

    ok, lines = wpc.build_results(tmp_path)

    assert ok is False
    assert any("job-wide env" in line for line in lines)


def test_no_workflows_is_ok(tmp_path: Path) -> None:
    ok, lines = wpc.build_results(tmp_path)
    assert ok is True
    assert any("No workflow files found" in line for line in lines)


def test_repo_workflows_meet_contract() -> None:
    """The real repository workflows must satisfy the posture contract."""
    ok, lines = wpc.build_results(wpc.REPO_ROOT)
    assert ok is True, "\n".join(lines)
