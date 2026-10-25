"""tesser3TAKT Save State als RO-Crate 1.2: Erzeugen, Versiegeln, Prüfen (tools/reentry_crate.py)."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from tools import reentry_crate as rc
from tools.verify_cards import validate_card

NOW = "2026-10-25T12:00:00+00:00"


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "corpus").mkdir()
    (tmp_path / "corpus" / "quelle.md").write_text("# Quelle\nInhalt\n", encoding="utf-8")
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "stand.md").write_text("- [DERIVED] Beispielnotiz\n", encoding="utf-8")
    return tmp_path


def _manifest(**overrides: object) -> dict[str, object]:
    manifest: dict[str, object] = {
        "id": "test-state",
        "title": "Test Save State",
        "summary": "Kurzfassung für den Wiedereinstieg.",
        "focus": "Re-Entry testen",
        "authority": "DERIVED",
        "current_status": "GO_conservative_hold_50",
        "frozen_state": ["RO-Crate 1.2 als Paketformat"],
        "floating_problem": "Signatur nur mit Secret",
        "open_points": ["Basic Memory noch nicht eingerichtet"],
        "negative_findings": ["DWB ohne API"],
        "known_losses": ["keine Chat-Transkripte"],
        "next_allowed_action": "verify vor Weiterarbeit",
        "next_actions": [{"id": "A1", "title": "Skill testen", "paths": ["tools/x.py"]}],
        "sources": [
            {"id": "src-local", "path": "corpus/quelle.md", "role": "input"},
            {"id": "src-doi", "uri": "https://doi.org/10.1000/example", "role": "context"},
        ],
        "claims": [
            {
                "text": "Paket ist hashbar",
                "tag": "MODELL",
                "status": "DERIVED",
                "sources": ["src-local"],
            },
            {"text": "Wirkung offen", "tag": "[HYP]", "status": "UNRESOLVED"},
        ],
        "notes": ["notes"],
        "lineage": {
            "nodes": [{"id": "a", "label": "A", "status": "spec_wip"}, {"id": "b", "label": "B"}],
            "edges": [{"source": "a", "target": "b", "relation": "supports"}],
        },
    }
    manifest.update(overrides)
    return manifest


def _save(workspace: Path, secret: str = "", **overrides: object) -> Path:
    return rc.save_state(
        _manifest(**overrides), workspace / "out", base=workspace, secret=secret, now=NOW
    )


def test_save_creates_crate_that_passes_verify(workspace: Path) -> None:
    crate = _save(workspace)
    result = rc.verify_crate(crate)
    assert result.verdict == "PASS", result.errors
    assert result.authenticity == "UNSIGNED"
    for name in (rc.METADATA_FILE, rc.BRIEF_FILE, rc.STATE_FILE, rc.SEAL_FILE, rc.CARD_FILE):
        assert (crate / name).is_file()
    assert (crate / "payload/external/quelle.md").is_file()
    assert (crate / "payload/notes/notes/stand.md").is_file()


def test_metadata_follows_ro_crate_12_minimum(workspace: Path) -> None:
    crate = _save(workspace)
    metadata = json.loads((crate / rc.METADATA_FILE).read_text(encoding="utf-8"))
    graph = {e["@id"]: e for e in metadata["@graph"]}
    assert metadata["@context"] == "https://w3id.org/ro/crate/1.2/context"
    assert graph[rc.METADATA_FILE]["conformsTo"] == {"@id": "https://w3id.org/ro/crate/1.2"}
    root = graph["./"]
    assert root["@type"] == "Dataset"
    assert root["license"] == {"@id": rc.PRIVATE_LICENSE_ID}
    parts = {p["@id"] for p in root["hasPart"]}
    files = {k for k, v in graph.items() if v["@type"] == "File"}
    assert files == parts
    assert graph["https://doi.org/10.1000/example"]["@type"] == "CreativeWork"
    claim = graph["#claim-1"]
    assert claim["@type"] == "Claim"
    assert claim["creativeWorkStatus"] == "DERIVED"
    assert claim["isBasedOn"] == [{"@id": "payload/external/quelle.md"}]
    assert graph["#save-action"]["@type"] == "CreateAction"


def test_state_carries_audit_and_input_hashes(workspace: Path) -> None:
    crate = _save(workspace)
    state = json.loads((crate / rc.STATE_FILE).read_text(encoding="utf-8"))
    assert state["claim_audit"] == {
        "total": 2,
        "by_tag": {"HYP": 1, "MODELL": 1},
        "by_status": {"DERIVED": 1, "UNRESOLVED": 1},
    }
    assert state["input_hashes"]["src-local"] == rc.sha256_file(workspace / "corpus/quelle.md")
    assert state["promotion_status"] == "NO_CANON_PROMOTION"


def test_reentry_card_is_valid_for_verify_cards(workspace: Path) -> None:
    crate = _save(workspace)
    assert validate_card(crate / rc.CARD_FILE) == []


def test_brief_lists_open_points_and_negative_findings(workspace: Path) -> None:
    crate = _save(workspace)
    brief = (crate / rc.BRIEF_FILE).read_text(encoding="utf-8")
    assert "Basic Memory noch nicht eingerichtet" in brief
    assert "DWB ohne API" in brief
    assert "Claim-Audit: 2 Aussagen" in brief


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda c: (c / "payload/external/quelle.md").write_text("x", encoding="utf-8"), "SHA-256"),
        (lambda c: (c / "extra.txt").write_text("x", encoding="utf-8"), "nicht im Siegel"),
        (lambda c: (c / rc.BRIEF_FILE).unlink(), "fehlt"),
    ],
)
def test_tampering_yields_hold(workspace: Path, mutate, message: str) -> None:
    crate = _save(workspace)
    mutate(crate)
    result = rc.verify_crate(crate)
    assert result.verdict == "HOLD"
    assert any(message in error for error in result.errors), result.errors


def test_signed_seal_roundtrip(workspace: Path) -> None:
    crate = _save(workspace, secret="s3cret")
    assert rc.verify_crate(crate, secret="s3cret").authenticity == "SIGNED_VALID"
    wrong = rc.verify_crate(crate, secret="other")
    assert (wrong.verdict, wrong.authenticity) == ("HOLD", "SIGNED_INVALID")
    unchecked = rc.verify_crate(crate)
    assert (unchecked.verdict, unchecked.authenticity) == ("PASS", "SIGNED_UNCHECKED")


def test_require_signed_holds_unsigned(workspace: Path) -> None:
    crate = _save(workspace)
    assert rc.verify_crate(crate, require_signed=True).verdict == "HOLD"


def test_seal_edit_breaks_fingerprint(workspace: Path) -> None:
    crate = _save(workspace)
    seal = json.loads((crate / rc.SEAL_FILE).read_text(encoding="utf-8"))
    seal["commit"] = "forged"
    (crate / rc.SEAL_FILE).write_text(json.dumps(seal), encoding="utf-8")
    result = rc.verify_crate(crate)
    assert result.verdict == "HOLD"
    assert any("state_fingerprint" in e for e in result.errors)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"claims": [{"text": "x", "tag": "BELIEF"}]}, "Vokabular"),
        ({"claims": [{"text": "x", "tag": "FACT", "sources": ["nope"]}]}, "unbekannte Quelle"),
        ({"sources": [{"id": "s", "path": "a", "uri": "https://x"}]}, "genau eines"),
        ({"authority": "TRUE"}, "authority"),
        ({"promotion_status": "CANON"}, "promotion_status"),
        ({"focus": ""}, "focus"),
        ({"open_point": ["Tippfehler"]}, "unbekannte Felder"),
        ({"id": "../escape"}, "id"),
        (
            {"lineage": {"nodes": [{"id": "a"}], "edges": [{"source": "a", "target": "z"}]}},
            "Knoten",
        ),
    ],
)
def test_invalid_manifest_is_rejected(overrides: dict[str, object], message: str) -> None:
    manifest = _manifest(**overrides)
    if "claims" in overrides and "sources" not in overrides:
        manifest["sources"] = []
    with pytest.raises(rc.ManifestError, match=message):
        rc.normalize_manifest(manifest)


def test_existing_crate_is_never_overwritten(workspace: Path) -> None:
    _save(workspace)
    with pytest.raises(rc.ManifestError, match="nie überschrieben"):
        _save(workspace)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_committable_target_requires_publish(workspace: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
    (workspace / ".gitignore").write_text("private/\n", encoding="utf-8")
    with pytest.raises(rc.ManifestError, match="privat per Default"):
        rc.save_state(_manifest(), workspace / "public", base=workspace, secret="", now=NOW)
    ignored = rc.save_state(_manifest(), workspace / "private", base=workspace, secret="", now=NOW)
    assert rc.verify_crate(ignored).verdict == "PASS"
    published = rc.save_state(
        _manifest(id="pub"), workspace / "public", base=workspace, secret="", publish=True, now=NOW
    )
    assert rc.verify_crate(published).verdict == "PASS"


def test_cli_brief_prints_only_after_pass(workspace: Path, capsys, monkeypatch) -> None:
    monkeypatch.delenv("ENTA_HMAC_SECRET", raising=False)
    monkeypatch.delenv("CI_SECRET", raising=False)
    crate = _save(workspace)
    assert rc.main(["brief", "--crate", str(crate)]) == 0
    assert "# Re-Entry: Test Save State" in capsys.readouterr().out
    (crate / "payload/external/quelle.md").write_text("x", encoding="utf-8")
    assert rc.main(["brief", "--crate", str(crate)]) == 1
    out = capsys.readouterr().out
    assert "REENTRY VERIFY: HOLD" in out
    assert "# Re-Entry" not in out


def test_cli_save_refuses_unsigned_in_ci(workspace: Path, monkeypatch, capsys) -> None:
    manifest = workspace / "savestate.yaml"
    manifest.write_text(json.dumps(_manifest()), encoding="utf-8")
    monkeypatch.setenv("CI", "true")
    monkeypatch.delenv("ENTA_HMAC_SECRET", raising=False)
    monkeypatch.delenv("CI_SECRET", raising=False)
    code = rc.main(["save", "--manifest", str(manifest), "--out", str(workspace / "out")])
    assert code == 2
    assert not (workspace / "out").exists()


def test_skill_template_uses_only_known_fields() -> None:
    template = (
        Path(__file__).resolve().parents[2]
        / ".claude/skills/tesser3takt-reentry/templates/savestate.yaml"
    )
    data = rc.load_manifest(template)
    assert set(data) <= rc.MANIFEST_KEYS
    with pytest.raises(rc.ManifestError):
        rc.normalize_manifest(data)  # ungefüllte Vorlage ist absichtlich ungültig
