import json
import math

import pytest

from src.core.ledger import Ledger, LedgerEvent, verify_chain_from_file


def _write_single_event(tmp_path):
    path = tmp_path / "events.jsonl"
    ledger = Ledger(path)
    ledger.metric("mzm.phi", 0.85)
    return path


def test_valid_persisted_chain_passes(tmp_path):
    path = _write_single_event(tmp_path)

    assert verify_chain_from_file(path) is True


def test_malformed_json_line_fails_closed(tmp_path):
    path = _write_single_event(tmp_path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"truncated":\n')

    assert verify_chain_from_file(path) is False


def test_extra_unhashed_field_is_rejected(tmp_path):
    path = _write_single_event(tmp_path)
    event = json.loads(path.read_text(encoding="utf-8"))
    event["untrusted_note"] = "not covered by the original hash"
    path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    assert verify_chain_from_file(path) is False


def test_missing_required_field_is_rejected(tmp_path):
    path = _write_single_event(tmp_path)
    event = json.loads(path.read_text(encoding="utf-8"))
    del event["event_id"]
    path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    assert verify_chain_from_file(path) is False


def test_modified_payload_is_rejected(tmp_path):
    path = _write_single_event(tmp_path)
    event = json.loads(path.read_text(encoding="utf-8"))
    event["payload"]["value"] = 0.99
    path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    assert verify_chain_from_file(path) is False


def test_non_object_json_record_is_rejected(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text("[]\n", encoding="utf-8")

    assert verify_chain_from_file(path) is False


@pytest.mark.parametrize(
    "token,value",
    [
        ("NaN", math.nan),
        ("Infinity", math.inf),
        ("-Infinity", -math.inf),
        ("1e999", math.inf),
        ("-1e999", -math.inf),
    ],
)
def test_non_finite_json_numbers_fail_even_with_matching_hash(tmp_path, token, value):
    # Reproduce a legacy/non-standard record, not a hash mismatch. Also cover
    # JSON exponents which are legal syntax but overflow the decoder's float.
    event = LedgerEvent(type="metric", payload={"metric_id": "x", "value": value})
    event.hash = event.compute_hash()
    line = json.dumps(event.to_dict())
    original = "NaN" if math.isnan(value) else ("Infinity" if value > 0 else "-Infinity")
    line = line.replace(original, token)
    path = tmp_path / "events.jsonl"
    path.write_text(line + "\n", encoding="utf-8")

    assert verify_chain_from_file(path) is False


def test_non_finite_token_names_inside_strings_remain_valid(tmp_path):
    path = tmp_path / "events.jsonl"
    Ledger(path).metric("x", 1.0, description="NaN Infinity -Infinity 1e999")
    assert verify_chain_from_file(path) is True
