#!/usr/bin/env python3
"""EntaENGELment Status Verifier

Zweck: Prüft HMAC-SHA256 Signatur eines status.json.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from typing import Dict, Tuple


def verify_payload(data: Dict, secret: str) -> Tuple[bool, str]:
    signatures = data.pop("signatures", None)
    if not signatures or "hmac" not in signatures:
        return False, "No signature found"

    target_hmac = signatures["hmac"]
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    computed_hmac = hmac.new(secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()
    if hmac.compare_digest(target_hmac, computed_hmac):
        return True, "OK"
    return False, f"Mismatch: {computed_hmac} != {target_hmac}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Path to deepjump_status.json")
    parser.add_argument("--secret", help="HMAC secret (ENV preferred)")
    args = parser.parse_args()

    secret = os.environ.get("CI_SECRET") or os.environ.get("ENTA_HMAC_SECRET") or args.secret
    if not secret:
        print("[ERR] Cannot verify: No secret provided.")
        sys.exit(2)

    with open(args.json_file, "r") as f:
        data = json.load(f)

    valid, msg = verify_payload(data, secret)
    if valid:
        print(f"[OK] Signature verified for {args.json_file}")
        sys.exit(0)

    print(f"[FAIL] Integrity Check Failed: {msg}")
    sys.exit(1)


if __name__ == "__main__":
    main()
