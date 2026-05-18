from __future__ import annotations

from pathlib import Path

from tools import voids_backlog_gen as gen


def test_render_document_is_deterministic_and_groups_statuses() -> None:
    data = {
        "metadata": {"last_updated": "2026-05-18"},
        "voids": [
            {
                "id": "VOID-Z",
                "title": "Older closed",
                "status": "CLOSED",
                "closed": "2026-01-01",
                "evidence": "old.md",
            },
            {
                "id": "VOID-A",
                "title": "Open pipe | escaped",
                "status": "OPEN",
                "priority": "high",
                "owner": "fleks",
                "domain": ["[SYS]", "[AUDIT]"],
                "target_date": "2026-06-01",
                "symptom": "First line\nsecond line ignored",
            },
            {
                "id": "VOID-B",
                "title": "Newer closed",
                "status": "CLOSED",
                "closed": "2026-02-01",
                "evidence": "new.md",
            },
            {
                "id": "VOID-X",
                "title": "Unknown status",
                "status": "REVIEW",
            },
            {
                "id": "VOID-MISSING",
                "title": "Missing optional fields",
                "status": "IN_PROGRESS",
            },
        ],
    }

    first = gen.render_document(data, "VOIDMAP.yml")
    second = gen.render_document(data, "VOIDMAP.yml")

    assert first == second
    assert "| OPEN | 1 |" in first
    assert "| IN_PROGRESS | 1 |" in first
    assert "| CLOSED | 2 |" in first
    assert "| OTHER | 1 |" in first
    assert "Open pipe \\| escaped" in first
    assert "First line" in first
    assert "second line ignored" not in first
    assert "## OTHER (unrecognized status)" in first
    assert "| VOID-MISSING | Missing optional fields | — | — | — | — | — |" in first
    assert first.index("VOID-B") < first.index("VOID-Z")


def test_check_mode_succeeds_and_detects_drift(tmp_path: Path) -> None:
    source = tmp_path / "VOIDMAP.yml"
    out = tmp_path / "voids_backlog.md"
    source.write_text(
        """
metadata:
  last_updated: 2026-05-18
voids:
  - id: VOID-001
    title: Open item
    status: OPEN
    priority: high
    owner: fleks
    domain: "[SYS]"
""".lstrip(),
        encoding="utf-8",
    )

    assert gen.main(["--source", str(source), "--out", str(out)]) == 0
    assert gen.main(["--source", str(source), "--out", str(out), "--check"]) == 0

    out.write_text(out.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")

    assert gen.main(["--source", str(source), "--out", str(out), "--check"]) == 1


def test_load_voidmap_rejects_non_mapping_source(tmp_path: Path) -> None:
    source = tmp_path / "VOIDMAP.yml"
    source.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    try:
        gen.load_voidmap(source)
    except ValueError as exc:
        assert "not a YAML mapping" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected ValueError for non-mapping VOIDMAP source")
