import json
import os
import subprocess
import sys


def run_guard(out_path, *patterns):
    cmd = [
        sys.executable,
        "tools/snapshot_guard.py",
        str(out_path),
        *patterns,
        "--strict",
    ]
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def test_snapshot_guard_includes_seeds_and_rel_paths(tmp_path):
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("external")

    manifest_path = tmp_path / "snapshot_manifest.json"
    run_guard(manifest_path, "seeds/*.yaml", "audit/*.yaml", str(outside_file))

    with open(manifest_path) as f:
        manifest = json.load(f)

    assert any(key.startswith("seeds/") for key in manifest["files"].keys())
    assert "seeds/seed_config.yaml" in manifest["files"]
    assert "seeds/seed_extras.yaml" in manifest["files"]
    assert all(not os.path.isabs(key) for key in manifest["files"])
    assert not any("outside.txt" in key for key in manifest["files"])


def test_snapshot_guard_warns_without_seeds(tmp_path):
    manifest_path = tmp_path / "snapshot_manifest.json"
    result = subprocess.run(
        [
            sys.executable,
            "tools/snapshot_guard.py",
            str(manifest_path),
            "audit/*.yaml",
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "No seeds/" in result.stdout or "No seeds/" in result.stderr
