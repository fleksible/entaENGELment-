from __future__ import annotations

from pathlib import Path

from tools import pipeline_essentials as pe


def test_build_report_lists_all_essentials(tmp_path: Path) -> None:
    (tmp_path / "Makefile").write_text(
        "\n".join(
            [
                "JS_VERIFY_CMD ?= pnpm turbo run typecheck lint build",
                "verify: verify-core",
                "verify-core: port-lint test verify-pointers claim-lint",
                "voids-backlog-check:",
                "frame-lint: FRAME_LINT_PATHS",
                "status-verify: status tools/status_verify.py",
                "snapshot: --strict",
                "verify-js:",
                "\tpnpm install --frozen-lockfile",
                "\t$(JS_VERIFY_CMD)",
            ]
        ),
        encoding="utf-8",
    )
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "release.yml").write_text("tools/receipt_lint.py", encoding="utf-8")
    (workflows / "ci.yml").write_text(
        "pip-audit\nactions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        encoding="utf-8",
    )
    (workflows / "ci-js-workspace.yml").write_text(
        "node-version: 22\npnpm install --frozen-lockfile\npnpm turbo run typecheck lint build",
        encoding="utf-8",
    )
    (workflows / "test.yml").write_text("node-version: '22'", encoding="utf-8")
    docs_ci = tmp_path / "docs" / "ci"
    docs_ci.mkdir(parents=True)
    (docs_ci / "WORKFLOW_MAP.md").write_text(
        ".github/workflows/ci-js-workspace.yml\nJS/TS workspace membrane",
        encoding="utf-8",
    )

    report = pe.build_report(tmp_path)

    assert "ESS-001" in report
    assert "ESS-008" in report
    assert "Ausbau-Möglichkeiten" in report
    assert "OPEN" not in report


def test_missing_essential_is_reported_open(tmp_path: Path) -> None:
    (tmp_path / "Makefile").write_text("verify: test\n", encoding="utf-8")

    report = pe.build_report(tmp_path)

    assert "ESS-001 | OPEN" in report
    assert "missing:" in report
