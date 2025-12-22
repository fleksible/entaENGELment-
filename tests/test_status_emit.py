import json
import os
import subprocess
import sys


def test_status_emit_and_verify(tmp_path):
    env = os.environ.copy()
    env["CI_SECRET"] = "super-secret"

    out_dir = tmp_path
    status_cmd = [
        sys.executable,
        "tools/status_emit.py",
        "--outdir",
        str(out_dir),
        "--status",
        "PASS",
        "--H",
        "0.85",
        "--dmi",
        "4.8",
        "--phi",
        "0.75",
        "--refractory",
        "120",
    ]
    subprocess.run(status_cmd, check=True, env=env)

    status_path = out_dir / "status" / "deepjump_status.json"
    assert status_path.exists()

    with open(status_path, "r") as f:
        payload = json.load(f)
    assert payload["signatures"]["hmac"] != "UNSIGNED"

    verify_cmd = [
        sys.executable,
        "tools/status_verify.py",
        str(status_path),
    ]
    subprocess.run(verify_cmd, check=True, env=env)
