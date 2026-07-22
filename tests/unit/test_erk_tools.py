"""Unit-Tests für die ERK-Anschlusswerkzeuge (Intake, Verify-Emitter, VOID-Resonanz, Drill)."""

import hashlib
import json
from pathlib import Path

import pytest

from src.core.evidence_routing import replay_events
from src.core.ledger import verify_chain_from_file
from tools import erk_drill, erk_intake_adapter, erk_verify_emit, erk_void_resonance
from tools.erk_paths import ensure_erk_write_path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "erk"


class TestIntakeAdapter:
    def _make_source(self, tmp_path):
        source = tmp_path / "docs" / "intake" / "raw" / "2026-07-21" / "wrapup.md"
        source.parent.mkdir(parents=True)
        source.write_text("Intake-Notiz (untrusted, G5).\n", encoding="utf-8")
        return source

    def test_payload_defaults_to_untrusted_and_keeps_no_raw_content(self, tmp_path):
        source = self._make_source(tmp_path)
        payload = erk_intake_adapter.build_material_payload(source, root=tmp_path)
        assert payload["trust"] == "UNTRUSTED"
        assert payload["origin"] == "calm_intake"
        assert payload["kind"] == "document"
        assert payload["locator"] == "docs/intake/raw/2026-07-21/wrapup.md"
        expected = hashlib.sha256(source.read_bytes()).hexdigest()
        assert payload["digest"] == f"sha256:{expected}"
        # Kein Rohinhalt im Event:
        assert "Intake-Notiz" not in json.dumps(payload)

    def test_intake_cannot_request_a_trust_upgrade(self, tmp_path):
        source = self._make_source(tmp_path)
        with pytest.raises(TypeError):
            erk_intake_adapter.build_material_payload(source, root=tmp_path, trust="REVIEWED")

    def test_emitted_event_lands_in_valid_chain_and_replays(self, tmp_path):
        source = self._make_source(tmp_path)
        ledger_path = tmp_path / "out" / "erk_events.jsonl"
        payload = erk_intake_adapter.build_material_payload(source, root=tmp_path)
        erk_intake_adapter.emit_material_event(payload, ledger_path)

        assert verify_chain_from_file(ledger_path) is True
        events = [
            json.loads(line)
            for line in ledger_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        state = replay_events(events)
        assert payload["material_id"] in state.materials
        # Quelle bleibt unberührt (rein lesend):
        assert source.read_text(encoding="utf-8") == "Intake-Notiz (untrusted, G5).\n"


class TestVerifyEmit:
    def test_pass_event_written_with_valid_chain(self, tmp_path):
        ledger_path = tmp_path / "verify_events.jsonl"
        erk_verify_emit.emit_verify_event(
            scope="core", commit_sha="deadbeef", ledger_path=ledger_path
        )
        assert verify_chain_from_file(ledger_path) is True
        event = json.loads(ledger_path.read_text(encoding="utf-8").splitlines()[0])
        assert event["type"] == "VERIFY_PASS"
        assert event["payload"] == {
            "actor": "role:ci",
            "scope": "core",
            "commit_sha": "deadbeef",
        }

    def test_unsigned_needs_reason(self, tmp_path):
        with pytest.raises(SystemExit):
            erk_verify_emit.build_verify_payload(
                scope="core", commit_sha="deadbeef", actor="role:ci", unsigned=True, reason=None
            )
        event_type, payload = erk_verify_emit.build_verify_payload(
            scope="core",
            commit_sha="deadbeef",
            actor="role:ci",
            unsigned=True,
            reason="no HMAC secret",
        )
        assert event_type == "VERIFY_PASS_UNSIGNED"
        assert payload["reason"] == "no HMAC secret"


class TestVoidResonance:
    def _make_voidmap(self, tmp_path):
        voidmap = tmp_path / "VOIDMAP.yml"
        voidmap.write_text(
            "voids:\n"
            "  - id: VOID-901\n"
            "    title: Beispiel offen\n"
            "    status: OPEN\n"
            "  - id: VOID-902\n"
            "    title: Beispiel zu\n"
            "    status: CLOSED\n",
            encoding="utf-8",
        )
        return voidmap

    def _make_stream(self, tmp_path):
        events = []
        with (FIXTURES / "allowed_proposal.jsonl").open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    events.append(json.loads(line))
        # Claim in [VOID] setzen, damit Resonanz sichtbar wird:
        for event in events:
            if event["type"] == "CLAIM_CREATED":
                event["payload"]["claim_tag"] = "[VOID]"
            if event["type"] == "TRANSITION_REQUESTED":
                event["payload"]["from_tag"] = "[VOID]"
                event["payload"]["to_tag"] = "[HYPOTHESE]"
        stream = tmp_path / "stream.jsonl"
        stream.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        return stream

    def test_report_lists_voids_and_void_claims_read_only(self, tmp_path):
        voidmap = self._make_voidmap(tmp_path)
        stream = self._make_stream(tmp_path)
        before = voidmap.read_text(encoding="utf-8")

        state = replay_events(erk_void_resonance.load_stream(stream))
        summary = erk_void_resonance.load_voidmap_summary(voidmap)
        report = erk_void_resonance.render_report(
            summary, erk_void_resonance.void_claim_resonance(state)
        )

        assert "VOID-901" in report
        assert "VOID-902" not in report.split("## Offene VOIDs")[1].split("##")[0]
        assert "clm-001" in report
        assert "SUPPORTS=1" in report
        # Read-only: VOIDMAP unverändert, keine Schließungssprache:
        assert voidmap.read_text(encoding="utf-8") == before
        assert "schließt nichts" in report or "Kein VOID wird geschlossen" in report


class TestDrill:
    def test_all_fixture_drills_hold(self, capsys):
        assert erk_drill.run_drills(FIXTURES) is True
        output = capsys.readouterr().out
        assert output.count("HÄLT") == 5
        assert "BRUCH" not in output

    def test_missing_fixture_reports_break(self, tmp_path, capsys):
        assert erk_drill.run_drills(tmp_path) is False
        assert "FEHLT" in capsys.readouterr().out


class TestWriteBoundary:
    @pytest.mark.parametrize(
        "path",
        [
            REPO_ROOT / "index" / "erk.jsonl",
            REPO_ROOT / "policies" / "erk.jsonl",
            REPO_ROOT / "NICHTRAUM" / "erk.jsonl",
            REPO_ROOT / "receipts" / "erk.jsonl",
            REPO_ROOT / "data" / "receipts" / "erk.jsonl",
            REPO_ROOT / "VOIDMAP.yml",
        ],
    )
    def test_protected_repository_paths_are_rejected(self, path):
        with pytest.raises(ValueError, match="protected"):
            ensure_erk_write_path(path)

    def test_disposable_external_output_remains_available(self, tmp_path):
        path = tmp_path / "erk" / "events.jsonl"
        assert ensure_erk_write_path(path) == path.resolve()
