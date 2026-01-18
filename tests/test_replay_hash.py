"""Tests for deterministic replay hashing."""

import time

from ledger.replay_determinism import (
    canonicalize_text,
    create_receipt,
    hash_canonical,
)


def test_canonicalize_text():
    # Newlines
    assert canonicalize_text("a\r\nb") == canonicalize_text("a\rb") == canonicalize_text("a\nb")

    # Unicode normalization (NFC)
    assert canonicalize_text("\u00e9") == canonicalize_text("\u0065\u0301")

    # Strip
    assert canonicalize_text("  hello  ") == "hello"


def test_hash_canonical_deterministic():
    obj = {"b": 2, "a": 1, "c": [3, 2, 1]}
    hashes = [hash_canonical(obj) for _ in range(100)]
    assert len(set(hashes)) == 1


def test_receipt_100x_identical_replay_hash():
    text = "Das EntaENGELment Framework schwingt..."
    seed = 42
    config = {"segmentation": "sections", "metrics": ["coherence_l2"]}
    transforms = [{"step": 1, "op": "score", "result": {"c": 0.5, "n": 0.3}}]
    output = {"winding": 0.25, "coherence": 0.67}
    user_id = "sha256:abc123"
    consent = "signed:2026-01-18T14:00:00Z"

    receipts = [
        create_receipt(text, seed, config, transforms, output, user_id, consent)
        for _ in range(100)
    ]

    replay_hashes = [r.deterministic["replay_hash"] for r in receipts]
    assert len(set(replay_hashes)) == 1

    for r in receipts:
        assert r.verify_replay()


def test_small_change_different_hash():
    text1 = "Das EntaENGELment Framework..."
    text2 = "Das EntaENGELment Framework."  # one less dot

    seed = 42
    config = {"segmentation": "sections"}
    transforms = []
    output = {}
    user_id = "sha256:abc"
    consent = "signed:now"

    r1 = create_receipt(text1, seed, config, transforms, output, user_id, consent)
    r2 = create_receipt(text2, seed, config, transforms, output, user_id, consent)

    assert r1.deterministic["replay_hash"] != r2.deterministic["replay_hash"]


def test_timestamp_uuid_change_same_hash():
    text = "Test"
    seed = 42
    config = {}
    transforms = []
    output = {}
    user_id = "sha256:xyz"
    consent = "signed:now"

    r1 = create_receipt(text, seed, config, transforms, output, user_id, consent)
    time.sleep(0.01)
    r2 = create_receipt(text, seed, config, transforms, output, user_id, consent)

    assert r1.event["timestamp"] != r2.event["timestamp"]
    assert r1.event["receipt_id"] != r2.event["receipt_id"]

    assert r1.deterministic["replay_hash"] == r2.deterministic["replay_hash"]
