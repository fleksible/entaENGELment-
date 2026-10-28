"""
tests/unit/test_ledger_strict_payloads.py

Regression tests for ledger findings B5 and B4.

B5: metric/gate payloads (including nested tags) are validated as strict JSON
before any ledger state changes. A rejected payload leaves ``_prev_hash``,
``_events`` and the file untouched; a following valid event still produces a
verifiable chain.

B4: after reopening an existing file, the in-memory check is anchored at the
loaded last hash. It checks the newly appended section only; the persisted
history is the job of ``verify_chain_from_file``.
"""

import json
import math

import numpy as np
import pytest

from src.core.ledger import Ledger, verify_chain_from_file

INVALID_METRICS = [
    ("mzm.phi", math.nan, {}),
    ("mzm.phi", math.inf, {}),
    ("mzm.phi", -math.inf, {}),
    ("mzm.phi", True, {}),
    ("mzm.phi", "0.9", {}),
    ("mzm.phi", None, {}),
    ("", 1.0, {}),
    ("mzm.phi", 1.0, {"tag": math.nan}),
    ("mzm.phi", 1.0, {"nested": {"deep": [1.0, math.inf]}}),
    ("mzm.phi", 1.0, {"obj": object()}),
]

INVALID_GATES = [
    ("", True, None),
    ("mzm_gate_v1", 1, None),
    ("mzm_gate_v1", "true", None),
    ("mzm_gate_v1", np.bool_(True), None),
    ("mzm_gate_v1", True, 7),
]


def _snapshot(ledger, path):
    content = path.read_text(encoding="utf-8") if path.exists() else None
    return ledger._prev_hash, len(ledger._events), content


@pytest.mark.parametrize("metric_id,value,tags", INVALID_METRICS)
def test_rejected_metric_leaves_state_unchanged(tmp_path, metric_id, value, tags):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.metric("mzm.phi", 0.85)
    before = _snapshot(ledger, path)

    with pytest.raises(ValueError):
        ledger.metric(metric_id, value, **tags)

    assert _snapshot(ledger, path) == before

    ledger.metric("mzm.phi", 0.9)
    assert ledger.verify_chain() is True
    assert verify_chain_from_file(path) is True


@pytest.mark.parametrize("gate_id,passed,reason", INVALID_GATES)
def test_rejected_gate_leaves_state_unchanged(tmp_path, gate_id, passed, reason):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.gate("mzm_gate_v1", passed=True, reason="PASS_ALL_CONSTRAINTS")
    before = _snapshot(ledger, path)

    with pytest.raises(ValueError):
        ledger.gate(gate_id, passed=passed, reason=reason)

    assert _snapshot(ledger, path) == before

    ledger.gate("mzm_gate_v1", passed=False, reason="BLOCK_PHI_BELOW_MIN")
    assert ledger.verify_chain() is True
    assert verify_chain_from_file(path) is True


def test_rejected_event_timestamp_leaves_state_unchanged(tmp_path):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.metric("mzm.phi", 0.85)
    before = _snapshot(ledger, path)

    with pytest.raises(ValueError):
        ledger.event("CLAIM_CREATED", {"claim_id": "c1"}, timestamp=math.inf)

    assert _snapshot(ledger, path) == before


def test_persisted_lines_are_strict_json(tmp_path):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.metric("mzm.phi", np.float64(0.85), source="toy", weights=[0.5, 0.5])
    ledger.metric("count", 3)
    ledger.gate("mzm_gate_v1", passed=True)

    def _reject(token):
        raise ValueError(f"non-standard JSON constant {token}")

    for line in path.read_text(encoding="utf-8").splitlines():
        json.loads(line, parse_constant=_reject)
    assert verify_chain_from_file(path) is True


def test_numpy_scalar_metric_is_stored_as_plain_number(tmp_path):
    ledger = Ledger(tmp_path / "events.jsonl")
    ledger.metric("mzm.phi", np.float32(0.5))
    value = ledger.get_events("metric")[0]["payload"]["value"]
    assert type(value) is float and value == 0.5


def test_reopen_and_append_verifies_new_section(tmp_path):
    path = tmp_path / "events.jsonl"
    first = Ledger(path)
    first.metric("mzm.phi", 0.85)
    first.gate("mzm_gate_v1", passed=True, reason="PASS_ALL_CONSTRAINTS")
    last_hash = first._prev_hash

    reopened = Ledger(path)
    reopened.metric("mzm.phi", 0.9)
    reopened.gate("mzm_gate_v1", passed=False, reason="BLOCK_PHI_BELOW_MIN")

    events = reopened.get_events()
    assert events[0]["prev_hash"] == last_hash
    assert reopened.verify_chain() is True
    assert verify_chain_from_file(path) is True


def test_reopen_anchor_is_not_evidence_of_valid_history(tmp_path):
    """A tampered persisted history is caught by the file check, not the anchor."""
    path = tmp_path / "events.jsonl"
    first = Ledger(path)
    first.metric("mzm.phi", 0.85)
    first.metric("mzm.phi", 0.86)

    lines = path.read_text(encoding="utf-8").splitlines()
    tampered = json.loads(lines[0])
    tampered["payload"]["value"] = 0.99
    lines[0] = json.dumps(tampered, separators=(",", ":"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    reopened = Ledger(path)
    reopened.metric("mzm.phi", 0.9)
    assert reopened.verify_chain() is True  # only the appended section
    assert verify_chain_from_file(path) is False


def test_in_memory_tampering_after_reopen_is_detected(tmp_path):
    path = tmp_path / "events.jsonl"
    Ledger(path).metric("mzm.phi", 0.85)

    reopened = Ledger(path)
    reopened.metric("mzm.phi", 0.9)
    reopened._events[0].prev_hash = None
    assert reopened.verify_chain() is False


def test_fresh_ledger_chain_still_starts_at_none():
    ledger = Ledger()
    ledger.metric("mzm.phi", 0.85)
    assert ledger.get_events()[0].get("prev_hash") is None
    assert ledger.verify_chain() is True
