"""
src/core/ledger.py

Runtime Ledger for entaENGELment Framework.
Append-only JSONL with hash-chain for auditable runtime events.

Features:
- Append-only JSONL format
- SHA-256 hash chain for integrity
- Span/context support via ContextVars
- Type-safe event emission (gate, metric, span)
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

# Context variable for current span
_current_span: ContextVar[str | None] = ContextVar("current_span", default=None)


@dataclass
class LedgerEvent:
    """Single ledger event with hash-chain support."""

    type: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str | None = None
    prev_hash: str | None = None
    hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        d = {
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "event_id": self.event_id,
        }
        if self.span_id is not None:
            d["span_id"] = self.span_id
        if self.prev_hash is not None:
            d["prev_hash"] = self.prev_hash
        if self.hash is not None:
            d["hash"] = self.hash
        return d

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of event content."""
        content = json.dumps(
            {
                "type": self.type,
                "payload": self.payload,
                "timestamp": self.timestamp,
                "event_id": self.event_id,
                "span_id": self.span_id,
                "prev_hash": self.prev_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


class Ledger:
    """Append-only runtime ledger with hash-chain integrity.

    Usage:
        ledger = Ledger("/path/to/events.jsonl")
        ledger.metric("mzm.phi", 0.85)
        ledger.gate("mzm_gate_v1", passed=True, reason="PASS_ALL_CONSTRAINTS")

        with ledger.span("stability.check"):
            ledger.gate("stability_taxonomy_v1", passed=False, reason="BLOCK_NEED_CONSENT")
    """

    def __init__(
        self,
        path: str | Path | None = None,
        run_id: str | None = None,
        manifest_sha256: str | None = None,
    ):
        """Initialize ledger.

        Args:
            path: Path to JSONL file. If None, events are stored in memory only.
            run_id: Optional run identifier for correlation.
            manifest_sha256: Optional static manifest hash for integrity.
        """
        self.path = Path(path) if path else None
        self.run_id = run_id or os.environ.get("ENTA_RUN_ID") or str(uuid.uuid4())
        self.manifest_sha256 = manifest_sha256 or os.environ.get("ENTA_STATIC_MANIFEST_SHA256")
        self._events: list[LedgerEvent] = []
        self._prev_hash: str | None = None
        self._file: TextIO | None = None

        # Initialize file if path provided
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # Load existing hash chain if file exists
            if self.path.exists():
                self._load_last_hash()

    def _load_last_hash(self) -> None:
        """Load the last hash from existing ledger file."""
        if not self.path or not self.path.exists():
            return

        last_line = None
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last_line = line

        if last_line:
            try:
                event = json.loads(last_line)
                self._prev_hash = event.get("hash")
            except json.JSONDecodeError:
                pass

    def _emit(self, event: LedgerEvent) -> None:
        """Emit event to ledger with hash-chain."""
        # Set span from context if not explicitly set
        if event.span_id is None:
            event.span_id = _current_span.get()

        # Set hash chain
        event.prev_hash = self._prev_hash
        event.hash = event.compute_hash()
        self._prev_hash = event.hash

        # Store in memory
        self._events.append(event)

        # Write to file if path configured
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.to_dict(), separators=(",", ":")) + "\n")

    def metric(self, metric_id: str, value: float, **tags: Any) -> None:
        """Emit a metric event.

        Args:
            metric_id: Metric identifier (e.g., "mzm.phi", "exception.GateBlockedError")
            value: Numeric metric value
            **tags: Additional tags for the metric
        """
        payload = {"metric_id": metric_id, "value": value}
        if tags:
            payload["tags"] = tags

        event = LedgerEvent(type="metric", payload=payload)
        self._emit(event)

    def gate(self, gate_id: str, passed: bool, reason: str | None = None) -> None:
        """Emit a gate decision event.

        Args:
            gate_id: Gate identifier (e.g., "mzm_gate_v1", "stability_taxonomy_v1")
            passed: Whether the gate check passed
            reason: Reason code for the decision
        """
        payload: dict[str, Any] = {"gate_id": gate_id, "passed": passed}
        if reason is not None:
            payload["reason"] = reason

        event = LedgerEvent(type="gate", payload=payload)
        self._emit(event)

    @contextmanager
    def span(self, name: str) -> Iterator[str]:
        """Create a span context for grouping related events.

        Args:
            name: Span name for identification

        Yields:
            The span_id for the created span
        """
        span_id = str(uuid.uuid4())
        parent_span_id = _current_span.get()

        # Emit span start
        start_payload: dict[str, Any] = {"name": name, "span_id": span_id}
        if parent_span_id:
            start_payload["parent_span_id"] = parent_span_id
        start_event = LedgerEvent(type="span_start", payload=start_payload)
        self._emit(start_event)

        # Set current span
        token = _current_span.set(span_id)

        try:
            yield span_id
        finally:
            # Reset span context
            _current_span.reset(token)

            # Emit span end
            end_payload = {"name": name, "span_id": span_id}
            end_event = LedgerEvent(type="span_end", payload=end_payload)
            self._emit(end_event)

    def get_events(self, event_type: str | None = None) -> list[dict[str, Any]]:
        """Get all events, optionally filtered by type.

        Args:
            event_type: Optional filter for event type

        Returns:
            List of event dictionaries
        """
        events = [e.to_dict() for e in self._events]
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        return events

    def verify_chain(self) -> bool:
        """Verify the integrity of the hash chain.

        Returns:
            True if hash chain is valid, False otherwise
        """
        prev_hash = None
        for event in self._events:
            if event.prev_hash != prev_hash:
                return False
            # Verify computed hash matches stored hash
            computed = event.compute_hash()
            if event.hash != computed:
                return False
            prev_hash = event.hash
        return True

    def close(self) -> None:
        """Close the ledger (flush any buffered writes)."""
        # Currently no buffering, but provided for future use
        pass

    def __enter__(self) -> Ledger:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


def load_ledger(path: str | Path) -> list[dict[str, Any]]:
    """Load events from a ledger file.

    Args:
        path: Path to JSONL ledger file

    Returns:
        List of event dictionaries
    """
    events: list[dict[str, Any]] = []
    path = Path(path)
    if not path.exists():
        return events

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return events


def create_ledger_from_env() -> Ledger | None:
    """Create a ledger from environment variables.

    Environment variables:
        ENTA_LEDGER_PATH: Path to ledger file
        ENTA_RUN_ID: Run identifier
        ENTA_STATIC_MANIFEST_SHA256: Manifest hash

    Returns:
        Ledger instance or None if ENTA_LEDGER_PATH not set
    """
    path = os.environ.get("ENTA_LEDGER_PATH")
    if not path:
        return None

    return Ledger(
        path=path,
        run_id=os.environ.get("ENTA_RUN_ID"),
        manifest_sha256=os.environ.get("ENTA_STATIC_MANIFEST_SHA256"),
    )
