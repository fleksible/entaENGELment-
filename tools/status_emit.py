#!/usr/bin/env python3
"""EntaENGELment Status Emitter (Final Hardened)

Zweck: Erzeugt status.json mit HMAC-Signatur.
Härtung: ENV-Secrets, Canonical JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from typing import Dict, Tuple


def sign_payload(payload: Dict, secret: str) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    signature = hmac.new(secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature


def emit_badge(status: str, out_dir: str) -> None:
    color = {"PASS": "#4c1", "FAIL": "#e05d44", "WARN": "#dfb317"}.get(status, "#999")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20">'
        f'<rect width="100" height="20" fill="#555"/>'
        f'<rect x="55" width="45" height="20" fill="{color}"/>'
        f'<g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">'
        f'<text x="27.5" y="14">DeepJump</text>'
        f'<text x="77.5" y="14">{status}</text>'
        f'</g>'
        f'</svg>'
    )
    with open(os.path.join(out_dir, "deepjump.svg"), "w") as f:
        f.write(svg)


def build_payload(args: argparse.Namespace) -> Tuple[Dict, str]:
    secret = os.environ.get("CI_SECRET") or os.environ.get("ENTA_HMAC_SECRET") or args.secret
    payload = {
        "system": "EntaENGELment DeepJump",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": args.status,
        "metrics": {
            "H": args.H,
            "dmi_score": args.dmi,
            "phi_integrity": args.phi,
            "refractory_ms": args.refractory,
        },
        "signature_type": "hmac-sha256",
    }

    if secret:
        sig = sign_payload(payload, secret)
        payload["signatures"] = {"hmac": sig, "key_id": "ci-primary"}
    else:
        payload["signatures"] = {
            "hmac": "UNSIGNED",
            "warning": "No secret provided. Untrusted status.",
        }
    return payload, secret


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--status", default="PASS")
    parser.add_argument("--secret", help="Optional CLI secret (ENV preferred)", default="")
    parser.add_argument("--H", type=float, default=0.0)
    parser.add_argument("--dmi", type=float, default=0.0)
    parser.add_argument("--phi", type=float, default=0.0)
    parser.add_argument("--refractory", type=int, default=0)
    args = parser.parse_args()

    status_dir = os.path.join(args.outdir, "status")
    badges_dir = os.path.join(args.outdir, "badges")
    os.makedirs(status_dir, exist_ok=True)
    os.makedirs(badges_dir, exist_ok=True)

    payload, secret = build_payload(args)
    json_path = os.path.join(status_dir, "deepjump_status.json")
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    emit_badge(args.status, badges_dir)
    print(f"[STATUS] Emitted (Signed: {bool(secret)})")


if __name__ == "__main__":
    main()
