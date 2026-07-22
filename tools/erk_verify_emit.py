#!/usr/bin/env python3
"""ERK Verify-Emitter — DeepJump-Läufe als replaybare Eventgeschichte.

Zeichnet das Ergebnis eines Verify-Laufs als ``VERIFY_PASS``- bzw.
``VERIFY_PASS_UNSIGNED``-Event (Vokabular aus ``spec/runtime_eventlog_v0_1.json``)
append-only in einen JSONL-Eventstream auf — über die öffentliche
``ledger.event()``-API mit vorhandener Hash-Chain.

Grenzen:
  - Das Event dokumentiert, dass ein Lauf stattfand; es macht kein Ergebnis wahr.
  - Kein Ersatz für ``make status`` (HMAC-Receipt) — nur eine Eventspur.
  - ``event_id`` und ``timestamp`` liegen im Ledger-Envelope; das Payload trägt
    ``actor``, ``scope``, ``commit_sha`` (und bei unsigned einen ``reason``).

Usage:
    python tools/erk_verify_emit.py --scope core --commit <sha>
        [--unsigned --reason "no HMAC secret"]
        [--ledger out/erk/verify_events.jsonl] [--actor role:ci]
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path
from typing import Any

try:
    from src.core.ledger import Ledger
    from tools.erk_paths import ensure_erk_write_path
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.core.ledger import Ledger
    from tools.erk_paths import ensure_erk_write_path

DEFAULT_LEDGER = Path("out") / "erk" / "verify_events.jsonl"


def resolve_commit_sha(explicit: str | None) -> str:
    """Commit-SHA aus Argument, Umgebung oder git ermitteln (fail-closed)."""
    if explicit:
        return explicit
    for env_var in ("ENTA_COMMIT_SHA", "GITHUB_SHA"):
        value = os.environ.get(env_var)
        if value:
            return value
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"[erk-verify-emit] no commit sha available: {exc}") from exc


def build_verify_payload(
    *, scope: str, commit_sha: str, actor: str, unsigned: bool, reason: str | None
) -> tuple[str, dict[str, Any]]:
    """Baut (event_type, payload) für den Verify-Lauf."""
    payload: dict[str, Any] = {"actor": actor, "scope": scope, "commit_sha": commit_sha}
    if unsigned:
        if not reason:
            raise SystemExit("[erk-verify-emit] --unsigned braucht --reason")
        payload["reason"] = reason
        return "VERIFY_PASS_UNSIGNED", payload
    return "VERIFY_PASS", payload


def emit_verify_event(
    *,
    scope: str,
    commit_sha: str,
    actor: str = "role:ci",
    unsigned: bool = False,
    reason: str | None = None,
    ledger_path: Path = DEFAULT_LEDGER,
) -> str:
    """Hängt das Verify-Event append-only an den Eventstream an."""
    event_type, payload = build_verify_payload(
        scope=scope, commit_sha=commit_sha, actor=actor, unsigned=unsigned, reason=reason
    )
    ledger = Ledger(ensure_erk_write_path(ledger_path))
    event = ledger.event(event_type, payload)
    return event.event_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify-Lauf als Ledger-Event aufzeichnen")
    parser.add_argument("--scope", default="core", help="Geltungsbereich, z.B. core")
    parser.add_argument("--commit", default=None, help="Commit-SHA (Default: env oder git)")
    parser.add_argument("--actor", default="role:ci", help="Rollen-Label (nicht authentifiziert)")
    parser.add_argument("--unsigned", action="store_true", help="Als VERIFY_PASS_UNSIGNED taggen")
    parser.add_argument("--reason", default=None, help="Grund bei --unsigned")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER), help="Ziel-JSONL-Eventstream")
    args = parser.parse_args()

    commit_sha = resolve_commit_sha(args.commit)
    event_id = emit_verify_event(
        scope=args.scope,
        commit_sha=commit_sha,
        actor=args.actor,
        unsigned=args.unsigned,
        reason=args.reason,
        ledger_path=Path(args.ledger),
    )
    print(f"[erk-verify-emit] event_id={event_id}")
    print(f"[erk-verify-emit] appended -> {args.ledger}")
    print("[erk-verify-emit] Eventspur, kein Truth-Maker und kein HMAC-Ersatz.")


if __name__ == "__main__":
    main()
