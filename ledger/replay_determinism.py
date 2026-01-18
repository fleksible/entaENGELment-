"""ledger.replay_determinism

Deterministic receipt generation with stable hashing.

Key principle:
- event.* can vary (timestamps, UUIDs)
- deterministic.replay_hash must be identical for same logical input

IMPORTANT PITFALL FIXED:
- replay_hash MUST NOT hash over itself.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import unicodedata
import uuid
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


# Namespace for stable UUIDs (UUIDv5) — keep constant for the project.
NAMESPACE_ENTAENGELMENT = uuid.UUID("12345678-1234-5678-1234-567812345678")


def canonicalize_text(s: str) -> str:
    """Normalize text for deterministic hashing.

    - NFC Unicode normalization (composed form)
    - Newlines: \r\n, \r → \n
    - Strip leading/trailing whitespace
    """
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = unicodedata.normalize("NFC", s)
    return s.strip()


def stable_uuid(name: str, namespace: uuid.UUID = NAMESPACE_ENTAENGELMENT) -> str:
    """Generate deterministic UUID from name (UUIDv5)."""
    return str(uuid.uuid5(namespace, name))


def canonicalize_json(obj: Any) -> str:
    """Canonical JSON representation.

    - Sort keys recursively
    - No whitespace (separators)
    - UTF-8 stable output
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_canonical(obj: Any) -> str:
    """SHA-256 hash of canonical JSON."""
    canonical = canonicalize_json(obj)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class ReplayableReceipt:
    """Receipt with deterministic replay capability."""

    event: Dict[str, Any]
    deterministic: Dict[str, Any]
    input: Dict[str, Any]
    transforms: List[Dict[str, Any]]
    output: Dict[str, Any]
    signatures: Dict[str, Any]

    def compute_replay_hash(self) -> str:
        """Compute deterministic hash over ONLY stable fields.

        Excludes:
          - event.* (timestamps, UUIDs)
          - deterministic.replay_hash (self-reference)

        Includes:
          - deterministic (minus replay_hash)
          - input
          - transforms
          - output
        """
        stable_deterministic = dict(self.deterministic)
        stable_deterministic.pop("replay_hash", None)

        stable_subset = {
            "deterministic": stable_deterministic,
            "input": self.input,
            "transforms": self.transforms,
            "output": self.output,
        }
        return hash_canonical(stable_subset)

    def verify_replay(self) -> bool:
        """Check if stored replay_hash matches computed hash."""
        def _norm_sha256(s: str) -> str:
            """Normalize either 'hex' or 'sha256:hex' to 'hex'."""
            s = (s or "").strip()
            # allow empty
            if not s:
                return ""
            # split only once (e.g. 'sha256:...')
            if ":" in s:
                algo, rest = s.split(":", 1)
                if algo.lower() == "sha256":
                    return rest
            return s

        computed = _norm_sha256(self.compute_replay_hash())
        stored = _norm_sha256(self.deterministic.get("replay_hash", ""))
        return computed == stored

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def create_receipt(
    text: str,
    seed: int,
    config: Dict[str, Any],
    transforms: List[Dict[str, Any]],
    output: Dict[str, Any],
    user_id_hash: str,
    user_consent: str,
    *,
    session_id: str | None = None,
) -> ReplayableReceipt:
    """Create a new receipt with deterministic replay capability."""

    # Canonicalize input
    text_canonical = canonicalize_text(text)

    # Event metadata (non-deterministic)
    event = {
        "receipt_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
        "session_id": session_id or str(uuid.uuid4()),
        "user_id_hash": user_id_hash,
    }

    # Deterministic hashes
    config_hash = hash_canonical(config)
    input_hash = hash_canonical({"text": text_canonical})
    output_hash = hash_canonical(output)

    deterministic = {
        "seed": seed,
        "config_hash": f"sha256:{config_hash}",
        "input_hash": f"sha256:{input_hash}",
        "output_hash": f"sha256:{output_hash}",
        "replay_hash": "",  # filled below
    }

    receipt = ReplayableReceipt(
        event=event,
        deterministic=deterministic,
        input={"text_canonical": text_canonical, "metadata": config},
        transforms=transforms,
        output=output,
        signatures={
            "user_consent": user_consent,
            "system_checksum": "",  # set to replay_hash
        },
    )

    replay_hash = receipt.compute_replay_hash()
    receipt.deterministic["replay_hash"] = f"sha256:{replay_hash}"
    receipt.signatures["system_checksum"] = f"sha256:{replay_hash}"
    return receipt


def verify_receipt_chain(receipts: List[Dict[str, Any]]) -> Dict[str, bool]:
    """Verify a list of receipts (dict form) for replay-hash integrity."""
    results: Dict[str, bool] = {}
    for i, receipt in enumerate(receipts):
        obj = ReplayableReceipt(**receipt)
        results[f"receipt_{i}"] = obj.verify_replay()
    return results
