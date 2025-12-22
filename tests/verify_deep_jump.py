#!/usr/bin/env python3
"""DeepJump verification utility (P9 Runbook reference)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List, Tuple


def load_receipt(path: str) -> Dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Receipt not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def validate_receipt(data: Dict) -> Tuple[str, List[str]]:
    issues: List[str] = []

    status_ok = data.get("status") == "valid"
    if not status_ok:
        issues.append("status not valid")

    proofs = data.get("proofs", {})
    proofs_ok = {"receipt_proof", "context_signature"}.issubset(set(proofs.keys()))
    if not proofs_ok:
        issues.append("missing proofs")

    metrics = data.get("metrics", {})
    required_metrics = {"H", "dmi_score", "phi_integrity", "refractory_ms"}
    metrics_ok = required_metrics.issubset(set(metrics.keys()))
    if metrics_ok:
        numeric_ok = all(isinstance(metrics[k], (int, float)) for k in required_metrics)
        metrics_ok = metrics_ok and numeric_ok
    else:
        issues.append("missing metrics")

    seed_ref = bool(data.get("seed_snapshot"))
    if not seed_ref:
        issues.append("missing seed snapshot reference")

    all_ok = status_ok and proofs_ok and metrics_ok and seed_ref
    verdict = "pass" if all_ok else "fail"
    return verdict, issues


def build_report(data: Dict) -> Dict:
    verdict, issues = validate_receipt(data)
    return {
        "receipt_id": data.get("id"),
        "status": data.get("status"),
        "verdict": verdict,
        "issues": issues,
        "proofs_present": {"receipt_proof", "context_signature"}.issubset(set(data.get("proofs", {}).keys())),
        "metrics_keys": sorted(list(data.get("metrics", {}).keys())),
        "seed_snapshot": data.get("seed_snapshot"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DeepJump verification runner.")
    parser.add_argument("--receipt", required=True, help="Path to receipt JSON")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        data = load_receipt(args.receipt)
    except FileNotFoundError as exc:
        print(f"[FAIL] {exc}")
        sys.exit(1)

    report = build_report(data)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"[REPORT] receipt={report['receipt_id']} verdict={report['verdict']}")
        if report["issues"]:
            print("Issues:", ", ".join(report["issues"]))

    if report["verdict"] != "pass":
        sys.exit(1)


if __name__ == "__main__":
    main()
