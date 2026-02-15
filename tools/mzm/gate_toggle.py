#!/usr/bin/env python3
"""MZM Gate Toggle - Hard-Gate Policy for entaENGELment Framework.

Implements gate logic based on MZM-Policy (gate_policy_v1.json).
Gate opens only when all constraints are satisfied:
- Phi >= phi_min
- RCC:EC fulfilled
- Non-Overlap (not PO)
- ||M||_2 = 1.0
- Psi-Lock set

Ledger Integration:
- Optional ledger parameter for audit logging
- Metrics: mzm.phi, mzm.m_norm_l2
- Gate events: mzm_gate_v1 with pass/fail reason

Strict-Mode:
- When strict=True and gate fails, raises GateBlockedError
- Exception metric logged to ledger
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.core.ledger import Ledger

POLICY_PATH = pathlib.Path(__file__).parents[2] / "policies" / "gate_policy_v1.json"


class GateBlockedError(Exception):
    """Raised when gate is blocked in strict mode."""

    pass


@dataclass
class Context:
    """Context data structure for gate evaluation."""

    phi: float  # Resonance potential
    rcc_ec: bool  # RCC:EC fulfilled?
    non_overlap: bool  # Non-Overlap (not PO)
    m_norm_l2: float  # ||M||_2 (L2-Norm)
    psi_lock: bool  # Lock set?


def load_policy(path: pathlib.Path = POLICY_PATH) -> dict[str, Any]:
    """Load gate policy from JSON file.

    Args:
        path: Path to policy file

    Returns:
        dict: Loaded policy configuration
    """
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
        return data


def _first_failure_reason(ctx: Context, policy: dict[str, Any]) -> str | None:
    """Determine the first constraint failure reason.

    Args:
        ctx: Context object with current values
        policy: Policy dictionary with constraints

    Returns:
        Reason code string if any constraint fails, None if all pass
    """
    c = policy["constraints"]

    if ctx.phi < c["phi_min"]:
        return "BLOCK_PHI_BELOW_MIN"

    if c["rcc_ec_required"] and not ctx.rcc_ec:
        return "BLOCK_RCC_EC_FAILED"

    if c["non_overlap_required"] and not ctx.non_overlap:
        return "BLOCK_NON_OVERLAP_FAILED"

    if abs(ctx.m_norm_l2 - c["m_norm_l2"]) >= 1e-9:
        return "BLOCK_M_NORM_INVALID"

    if c["psi_lock_required"] and not ctx.psi_lock:
        return "BLOCK_PSI_LOCK_MISSING"

    return None


def gate_open(
    ctx: Context,
    policy: dict[str, Any],
    ledger: Ledger | None = None,
    gate_id: str = "mzm_gate_v1",
    strict: bool = False,
) -> bool:
    """Check if gate can be opened based on context and policy.

    Args:
        ctx: Context object with current values
        policy: Policy dictionary with constraints
        ledger: Optional Ledger instance for audit logging
        gate_id: Gate identifier for ledger events
        strict: If True, raises GateBlockedError on gate failure

    Returns:
        bool: True if all constraints are satisfied, False otherwise

    Raises:
        GateBlockedError: If strict=True and gate check fails
    """
    # Log metrics if ledger provided
    if ledger is not None:
        ledger.metric("mzm.phi", ctx.phi)
        ledger.metric("mzm.m_norm_l2", ctx.m_norm_l2)

    # Determine pass/fail and reason
    reason = _first_failure_reason(ctx, policy)
    passed = reason is None

    if passed:
        reason = "PASS_ALL_CONSTRAINTS"

    # Log gate decision if ledger provided
    if ledger is not None:
        ledger.gate(gate_id, passed=passed, reason=reason)

    # Strict mode: raise on failure
    if strict and not passed:
        if ledger is not None:
            ledger.metric("exception.GateBlockedError", 1.0)
        raise GateBlockedError(reason or "BLOCK_UNKNOWN")

    return passed


def main(argv: list[str]) -> int:
    """CLI entry point for Gate-Toggle.

    Usage:
        mzm_gate_toggle.py <phi> <rcc_ec> <non_overlap> <m_norm_l2> <psi_lock>

    Environment variables:
        ENTA_LEDGER_PATH: Path to ledger file
        ENTA_RUN_ID: Run identifier
        ENTA_STATIC_MANIFEST_SHA256: Manifest hash
        ENTA_GATE_STRICT: Set to "1" or "true" for strict mode

    Args:
        argv: Command-line arguments

    Returns:
        int: Exit code (0 for success, 2 for wrong arguments, 1 for gate blocked)
    """
    if len(argv) != 6:
        print(
            "usage: mzm_gate_toggle.py <phi> <rcc_ec> <non_overlap> <m_norm_l2> <psi_lock>",
            file=sys.stderr,
        )
        return 2

    phi = float(argv[1])

    def parse_bool(s: str) -> bool:
        return s.lower() in {"1", "true", "yes", "y", "on"}

    ctx = Context(
        phi=phi,
        rcc_ec=parse_bool(argv[2]),
        non_overlap=parse_bool(argv[3]),
        m_norm_l2=float(argv[4]),
        psi_lock=parse_bool(argv[5]),
    )

    policy = load_policy()

    # Setup ledger from environment
    ledger = None
    ledger_path = os.environ.get("ENTA_LEDGER_PATH")
    if ledger_path:
        from src.core.ledger import Ledger

        ledger = Ledger(
            path=ledger_path,
            run_id=os.environ.get("ENTA_RUN_ID"),
            manifest_sha256=os.environ.get("ENTA_STATIC_MANIFEST_SHA256"),
        )

    # Check strict mode from environment
    strict = os.environ.get("ENTA_GATE_STRICT", "").lower() in {"1", "true", "yes", "on"}

    try:
        result = gate_open(ctx, policy, ledger=ledger, strict=strict)
        print(f"GateOpen={'true' if result else 'false'}")
        return 0
    except GateBlockedError as e:
        print(f"GateOpen=false (BLOCKED: {e})", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
