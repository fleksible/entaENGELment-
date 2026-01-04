#!/usr/bin/env python3
"""MZM Gate Toggle - Hard-Gate Policy für entaENGELment Framework.

Implementiert die Gate-Logik basierend auf der MZM-Policy (gate_policy_v1.json).
Das Gate öffnet nur, wenn alle Constraints erfüllt sind:
- Phi >= phi_min
- RCC:EC erfüllt
- Non-Overlap (¬PO)
- ||M||_2 = 1.0
- Psi-Lock gesetzt
"""
from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Any

POLICY_PATH = pathlib.Path(__file__).parents[2] / "policies" / "gate_policy_v1.json"


@dataclass
class Context:
    """Kontext-Datenstruktur für Gate-Evaluierung."""

    phi: float  # Resonanzpotential Φ
    rcc_ec: bool  # RCC:EC erfüllt?
    non_overlap: bool  # ¬PO (Non-Overlap)
    m_norm_l2: float  # ||M||_2 (L2-Norm)
    psi_lock: bool  # Lock gesetzt?


def load_policy(path: pathlib.Path = POLICY_PATH) -> dict[str, Any]:
    """Lädt die Gate-Policy aus JSON-Datei.

    Args:
        path: Pfad zur Policy-Datei

    Returns:
        dict: Geladene Policy-Konfiguration
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def gate_open(ctx: Context, policy: dict[str, Any]) -> bool:
    """Prüft, ob das Gate basierend auf Kontext und Policy geöffnet werden kann.

    Args:
        ctx: Context-Objekt mit aktuellen Werten
        policy: Policy-Dictionary mit Constraints

    Returns:
        bool: True wenn alle Constraints erfüllt sind, sonst False
    """
    c = policy["constraints"]
    checks = [
        ctx.phi >= c["phi_min"],
        (ctx.rcc_ec if c["rcc_ec_required"] else True),
        (ctx.non_overlap if c["non_overlap_required"] else True),
        abs(ctx.m_norm_l2 - c["m_norm_l2"]) < 1e-9,
        (ctx.psi_lock if c["psi_lock_required"] else True),
    ]
    return all(checks)


def main(argv: list[str]) -> int:
    """CLI-Einstiegspunkt für Gate-Toggle.

    Usage:
        mzm_gate_toggle.py <phi> <rcc_ec> <non_overlap> <m_norm_l2> <psi_lock>

    Args:
        argv: Command-line Argumente

    Returns:
        int: Exit-Code (0 für Erfolg, 2 für falsche Argumente)
    """
    if len(argv) != 6:
        print(
            "usage: mzm_gate_toggle.py <phi> <rcc_ec> <non_overlap> <m_norm_l2> <psi_lock>",
            file=sys.stderr,
        )
        return 2

    phi = float(argv[1])

    def parse_bool(s):
        return s.lower() in {"1", "true", "yes", "y", "on"}

    ctx = Context(
        phi=phi,
        rcc_ec=parse_bool(argv[2]),
        non_overlap=parse_bool(argv[3]),
        m_norm_l2=float(argv[4]),
        psi_lock=parse_bool(argv[5]),
    )

    policy = load_policy()
    result = "true" if gate_open(ctx, policy) else "false"
    print(f"GateOpen={result}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
