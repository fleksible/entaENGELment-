from __future__ import annotations

from pathlib import Path

from tools import pipeline_essentials as pe


def test_build_report_lists_all_essentials(tmp_path: Path) -> None:
    (tmp_path / "Makefile").write_text(
        "\n".join(
            [
                "verify: port-lint test verify-pointers claim-lint",
                "voids-backlog-check:",
                "frame-lint: FRAME_LINT_PATHS",
                "status-verify: status tools/status_verify.py",
                "snapshot: --strict",
            ]
        ),
        encoding="utf-8",
    )
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "release.yml").write_text("tools/receipt_lint.py", encoding="utf-8")
    (workflows / "ci.yml").write_text(
        "pip-audit\nactions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd",
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
