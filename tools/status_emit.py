#!/usr/bin/env python3
"""EntaENGELment Status Emitter (DeepJump Protocol v1.2)

Purpose: Generate HMAC-signed status payloads and receipts.

Modes:
  1. Status mode (--outdir): Emit CI status with metrics
  2. Receipt mode (--claim): Emit protocol v1.2 receipt

Receipt Format v1.0:
  - receipt_version, timestamp, claim, tag, module
  - observer, repo, branch, commit, files_changed
  - hash_alg, canonicalization, state_fingerprint, hmac_signature

Claim Tags:
  [FACT] - Empirically verified
  [HYP]  - Testable hypothesis
  [MET]  - Metaphor/Analogy
  [TODO] - Open task
  [RISK] - Known risk
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

VALID_TAGS = {"[FACT]", "[HYP]", "[MET]", "[TODO]", "[RISK]"}


def get_secret() -> str:
    """Get HMAC secret from environment. Fails if not set."""
    secret = os.environ.get("ENTA_HMAC_SECRET") or os.environ.get("CI_SECRET")
    if not secret:
        if os.environ.get("CI"):
            raise OSError(
                "ENTA_HMAC_SECRET is not set. "
                "Unsigned receipts are not permitted in CI."
            )
        print("WARNING: No ENTA_HMAC_SECRET set. Local-only mode.",
              file=sys.stderr)
        return ""
    return secret


def canonical_json(payload: dict) -> str:
    """Create canonical JSON representation (json_c14n_v1)."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def sign_payload(payload: dict, secret: str) -> str:
    """Create HMAC-SHA256 signature of canonical payload."""
    canonical = canonical_json(payload)
    signature = hmac.new(
        secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return signature


def compute_state_fingerprint(payload: dict) -> str:
    """Compute SHA256 fingerprint of canonical payload."""
    canonical = canonical_json(payload)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def get_git_info() -> tuple[str, str, list[str]]:
    """Get current git branch, commit, and changed files."""
    try:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        branch = "unknown"

    try:
        commit = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        commit = "unknown"

    try:
        # Get staged and unstaged changed files
        status = (
            subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
        files_changed = [line[3:].strip() for line in status.split("\n") if line.strip()]
    except Exception:
        files_changed = []

    return branch, commit, files_changed


def emit_badge(status: str, out_dir: str) -> None:
    """Generate SVG status badge."""
    color = {"PASS": "#4c1", "FAIL": "#e05d44", "WARN": "#dfb317"}.get(status, "#999")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20">'
        f'<rect width="100" height="20" fill="#555"/>'
        f'<rect x="55" width="45" height="20" fill="{color}"/>'
        f'<g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">'
        f'<text x="27.5" y="14">DeepJump</text>'
        f'<text x="77.5" y="14">{status}</text>'
        f"</g>"
        f"</svg>"
    )
    with open(os.path.join(out_dir, "deepjump.svg"), "w") as f:
        f.write(svg)


def build_status_payload(args: argparse.Namespace) -> tuple[dict, str]:
    """Build legacy status payload with metrics."""
    secret = get_secret() or args.secret
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


def build_receipt(args: argparse.Namespace) -> tuple[dict, str]:
    """Build protocol v1.2 receipt."""
    secret = get_secret()
    branch, commit, files_changed = get_git_info()

    # Build receipt payload (without signature fields first)
    receipt = {
        "receipt_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "claim": args.claim,
        "tag": args.tag,
        "module": args.module or "UNSPECIFIED",
        "observer": "Claude-Code",
        "repo": "entaENGELment",
        "branch": branch,
        "commit": commit,
        "files_changed": files_changed[:20],  # Limit to 20 files
        "hash_alg": "sha256",
        "canonicalization": "json_c14n_v1",
    }

    # Compute state fingerprint before adding signature
    receipt["state_fingerprint"] = "0x" + compute_state_fingerprint(receipt)

    # Add HMAC signature
    if secret:
        receipt["hmac_signature"] = "0x" + sign_payload(receipt, secret)
    else:
        receipt["hmac_signature"] = "UNSIGNED"
        receipt["warning"] = "No ENTA_HMAC_SECRET set. Receipt is untrusted."

    return receipt, secret


def emit_status(args: argparse.Namespace) -> None:
    """Emit legacy status payload."""
    status_dir = os.path.join(args.outdir, "status")
    badges_dir = os.path.join(args.outdir, "badges")
    os.makedirs(status_dir, exist_ok=True)
    os.makedirs(badges_dir, exist_ok=True)

    payload, secret = build_status_payload(args)
    json_path = os.path.join(status_dir, "deepjump_status.json")
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    emit_badge(args.status, badges_dir)
    print(f"[STATUS] Emitted (Signed: {bool(secret)})")


def emit_receipt(args: argparse.Namespace) -> None:
    """Emit protocol v1.2 receipt."""
    # Validate tag
    if args.tag not in VALID_TAGS:
        print(f"[ERROR] Invalid tag: {args.tag}")
        print(f"        Valid tags: {', '.join(sorted(VALID_TAGS))}")
        sys.exit(1)

    receipt, secret = build_receipt(args)

    # Determine output path
    output_dir = args.output or "receipts"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # Create safe filename from claim
    claim_slug = args.claim[:30].lower()
    claim_slug = "".join(c if c.isalnum() else "_" for c in claim_slug)
    filename = f"{timestamp}_{claim_slug}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(receipt, f, indent=2)

    signed_status = "✅ Signed" if secret else "⚠️  UNSIGNED"
    print(f"[RECEIPT] {signed_status}")
    print(f"          File: {filepath}")
    print(f"          Claim: {args.claim}")
    print(f"          Tag: {args.tag}")
    print(f"          Module: {args.module or 'UNSPECIFIED'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="EntaENGELment Status Emitter (DeepJump Protocol v1.2)"
    )

    # Receipt mode arguments
    parser.add_argument("--claim", help="Claim description for receipt mode")
    parser.add_argument(
        "--tag",
        choices=["[FACT]", "[HYP]", "[MET]", "[TODO]", "[RISK]"],
        help="Claim tag for receipt mode",
    )
    parser.add_argument("--module", help="Module ID (e.g., MOD_6)")
    parser.add_argument("--output", help="Output directory for receipt (default: receipts/)")

    # Legacy status mode arguments
    parser.add_argument("--outdir", help="Output directory for status mode")
    parser.add_argument("--status", default="PASS")
    parser.add_argument("--secret", help="Optional CLI secret (ENV preferred)", default="")
    parser.add_argument("--H", type=float, default=0.0)
    parser.add_argument("--dmi", type=float, default=0.0)
    parser.add_argument("--phi", type=float, default=0.0)
    parser.add_argument("--refractory", type=int, default=0)

    args = parser.parse_args()

    # Determine mode
    if args.claim:
        # Receipt mode
        if not args.tag:
            print("[ERROR] --tag is required when using --claim")
            sys.exit(1)
        emit_receipt(args)
    elif args.outdir:
        # Legacy status mode
        emit_status(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
