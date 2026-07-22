#!/usr/bin/env python3
"""ERK Intake-Adapter — Calm Intake Layer → MaterialRef (Anschluss an Pattern F).

Liest ein Intake-Artefakt (z.B. unter ``docs/intake/raw/``) und erzeugt daraus
ein ``MATERIAL_REGISTERED``-Event für den Evidence Routing Kernel v0.1a.

Grenzen (bewusst eng):
  - Rein lesend gegenüber dem Intake-Bereich; die Quelldatei bleibt unberührt.
  - Append-only gegenüber dem Ziel-Eventstream (Ledger-Hash-Chain).
  - Trust-Default ist UNTRUSTED (G5: externe Inhalte sind untrusted).
  - Kein Rohinhalt wird in das Event übernommen — nur Pfad, Digest, Metadaten.
  - Keine Kanonisierung, keine Claim-Erzeugung, keine Promotion.

Usage:
    python tools/erk_intake_adapter.py --file docs/intake/raw/2026-07-21/x.md
        [--ledger out/erk/erk_events.jsonl]
        [--visibility private] [--kind document] [--root .]

Ohne ``--ledger`` läuft das Tool als Dry-Run und zeigt nur das Event-Payload.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from src.core.evidence_routing import (
        EVENT_MATERIAL_REGISTERED,
        TRUST_UNTRUSTED,
        MaterialRef,
        model_from_payload,
    )
    from src.core.ledger import Ledger
    from tools.erk_paths import ensure_erk_write_path
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.core.evidence_routing import (
        EVENT_MATERIAL_REGISTERED,
        TRUST_UNTRUSTED,
        MaterialRef,
        model_from_payload,
    )
    from src.core.ledger import Ledger
    from tools.erk_paths import ensure_erk_write_path

_KIND_BY_SUFFIX = {
    ".md": "document",
    ".txt": "note",
    ".json": "data",
    ".jsonl": "data",
    ".yaml": "data",
    ".yml": "data",
}


def build_material_payload(
    file_path: Path,
    *,
    root: Path,
    visibility: str = "private",
    kind: str | None = None,
    source: str = "calm_intake",
) -> dict[str, Any]:
    """Baut ein MaterialRef-Payload aus einer Intake-Datei (rein lesend)."""
    raw = file_path.read_bytes()
    digest_hex = hashlib.sha256(raw).hexdigest()
    try:
        locator = file_path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        locator = file_path.as_posix()

    payload: dict[str, Any] = {
        "material_id": f"mat-intake-{digest_hex[:12]}",
        "schema_version": "erk.v0.1",
        "kind": kind or _KIND_BY_SUFFIX.get(file_path.suffix.lower(), "file"),
        "source": source,
        "revision": "r0",
        "locator": locator,
        "digest": f"sha256:{digest_hex}",
        "origin": "calm_intake",
        "actor": "role:intake",
        # G5: Intake is an acquisition boundary. Trust can only be raised by a
        # separate, review-backed event; this adapter never accepts an upgrade.
        "trust": TRUST_UNTRUSTED,
        "visibility": visibility,
        "status": "ACTIVE",
    }
    # Fail-closed Schema-Check über das geschlossene Modell des Kernels:
    model_from_payload(MaterialRef, payload)
    return payload


def emit_material_event(payload: dict[str, Any], ledger_path: Path) -> str:
    """Hängt das Event append-only an den Ziel-Eventstream an."""
    ledger = Ledger(ensure_erk_write_path(ledger_path))
    event = ledger.event(EVENT_MATERIAL_REGISTERED, payload)
    return event.event_id


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Intake-Artefakt als MATERIAL_REGISTERED-Event erfassen (Dry-Run ohne --ledger)"
    )
    parser.add_argument("--file", required=True, help="Pfad zum Intake-Artefakt (rein lesend)")
    parser.add_argument("--ledger", help="Ziel-JSONL-Eventstream; ohne Angabe: Dry-Run")
    parser.add_argument("--visibility", default="private", help="Sichtbarkeit (Default private)")
    parser.add_argument("--kind", default=None, help="Materialart (Default aus Dateiendung)")
    parser.add_argument("--root", default=".", help="Repository-Root (Default: .)")
    args = parser.parse_args()

    source_file = Path(args.file)
    if not source_file.is_file():
        raise SystemExit(f"[erk-intake] source file not found: {source_file}")

    payload = build_material_payload(
        source_file,
        root=Path(args.root),
        visibility=args.visibility,
        kind=args.kind,
    )

    if args.ledger:
        event_id = emit_material_event(payload, Path(args.ledger))
        print(f"[erk-intake] event_id={event_id}")
        print(f"[erk-intake] appended -> {args.ledger}")
    else:
        print("[erk-intake] dry-run (kein --ledger angegeben):")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("[erk-intake] Quelle unberührt; keine Kanonisierung, keine Promotion.")


if __name__ == "__main__":
    main()
