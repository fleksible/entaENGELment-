#!/usr/bin/env python3
"""ERK VOID-Resonanz-Report — rein lesende Kompassnadel, kein Entscheider.

Liest ``VOIDMAP.yml`` (GOLD, nur lesen) und einen ERK-Eventstream, replayt den
Stream und berichtet:

  - offene VOIDs nach Status,
  - Claims, die aktuell im Tag ``[VOID]`` stehen,
  - wie viele Evidence-Relationen sich je [VOID]-Claim ansammeln (nach Typ).

Grenzen (Invariante 5: VOID is valid):
  - Es gibt keine automatische Verknüpfung zwischen ``claim_id`` und VOID-IDs;
    der Report stellt beide Seiten nebeneinander, mehr nicht.
  - Der Report schließt nichts, schlägt keine Schließung vor und schreibt
    weder in VOIDMAP.yml noch in den Eventstream.
  - Ansammelnde Relationen sind Hinweise auf menschliche Review-Kandidaten,
    kein Evidenz-Urteil.

Usage:
    python tools/erk_void_resonance.py --stream out/erk/erk_events.jsonl
        [--voidmap VOIDMAP.yml] [--out OUT/erk_void_resonance.md]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

try:
    from src.core.evidence_routing import ReplayState, replay_events
    from tools.erk_paths import ensure_erk_write_path
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.core.evidence_routing import ReplayState, replay_events
    from tools.erk_paths import ensure_erk_write_path

OPENISH_STATUSES = ("OPEN", "IN_PROGRESS", "SUSPENDED")


def load_stream(path: Path) -> list[dict[str, Any]]:
    """JSONL-Eventstream tolerant einlesen (Integritätsfragen klärt der Ledger)."""
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def load_voidmap_summary(path: Path) -> dict[str, Any]:
    """VOIDMAP.yml rein lesend zusammenfassen."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    voids = data.get("voids", []) if isinstance(data, dict) else []
    by_status: Counter[str] = Counter()
    openish: list[dict[str, str]] = []
    for void in voids:
        if not isinstance(void, dict):
            continue
        status = str(void.get("status", "UNKNOWN"))
        by_status[status] += 1
        if status in OPENISH_STATUSES:
            openish.append(
                {
                    "id": str(void.get("id", "?")),
                    "title": str(void.get("title", "?")),
                    "status": status,
                }
            )
    return {"by_status": dict(sorted(by_status.items())), "openish": openish}


def void_claim_resonance(state: ReplayState) -> list[dict[str, Any]]:
    """[VOID]-Claims mit Relationszählung je Typ (reine Beobachtung)."""
    rows: list[dict[str, Any]] = []
    for claim_id, record in sorted(state.claims.items()):
        if record.get("current_tag") != "[VOID]":
            continue
        relation_types: Counter[str] = Counter()
        for relation in state.relations.values():
            if relation.get("claim_id") == claim_id:
                relation_types[str(relation.get("relation_type", "?"))] += 1
        rows.append(
            {
                "claim_id": claim_id,
                "status": record.get("status"),
                "retracted": bool(record.get("retracted", False)),
                "relation_counts": dict(sorted(relation_types.items())),
                "relation_total": sum(relation_types.values()),
            }
        )
    return rows


def render_report(voidmap_summary: dict[str, Any], resonance: list[dict[str, Any]]) -> str:
    """Menschenlesbaren Markdown-Report bauen."""
    lines = [
        "# ERK VOID-Resonanz-Report",
        "",
        "Rein lesende Beobachtung. Kein VOID wird geschlossen, nichts wird",
        "vorgeschlagen; VOID ist ein gültiger Dauerzustand (Invariante 5).",
        "Es besteht keine automatische Verknüpfung zwischen claim_id und VOID-ID.",
        "",
        "## VOIDMAP-Status (read-only)",
        "",
    ]
    for status, count in voidmap_summary["by_status"].items():
        lines.append(f"- {status}: {count}")
    lines += ["", "## Offene VOIDs", ""]
    if voidmap_summary["openish"]:
        for void in voidmap_summary["openish"]:
            lines.append(f"- {void['id']} ({void['status']}): {void['title']}")
    else:
        lines.append("- (keine)")
    lines += ["", "## Claims aktuell in [VOID]", ""]
    if resonance:
        for row in resonance:
            counts = ", ".join(f"{k}={v}" for k, v in row["relation_counts"].items()) or "keine"
            lines.append(
                f"- {row['claim_id']}: {row['relation_total']} Relation(en) ({counts})"
                + (" — RETRACTED" if row["retracted"] else "")
            )
        lines += [
            "",
            "Ansammelnde Relationen sind Kandidaten für menschliche Review,",
            "kein Evidenz-Urteil und keine Schließungsempfehlung.",
        ]
    else:
        lines.append("- (keine Claims in [VOID] im untersuchten Stream)")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="VOID-Resonanz zwischen VOIDMAP und ERK-Stream")
    parser.add_argument("--stream", required=True, help="Pfad zum ERK-JSONL-Eventstream")
    parser.add_argument("--voidmap", default="VOIDMAP.yml", help="Pfad zur VOIDMAP (nur lesen)")
    parser.add_argument("--out", default=None, help="Optionaler Markdown-Zielpfad")
    args = parser.parse_args()

    voidmap_path = Path(args.voidmap)
    if not voidmap_path.is_file():
        raise SystemExit(f"[erk-void] VOIDMAP not found: {voidmap_path}")

    state = replay_events(load_stream(Path(args.stream)))
    report = render_report(load_voidmap_summary(voidmap_path), void_claim_resonance(state))

    if args.out:
        out_path = ensure_erk_write_path(Path(args.out))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"[erk-void] report -> {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
