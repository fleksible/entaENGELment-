#!/usr/bin/env python3
"""Maintain the sole Python lock and verify environment/SBOM receipts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UV_VERSION = "0.12.18"
EXPORTS = {
    "requirements.txt": "runtime",
    "requirements-test.txt": "test",
    "requirements-dev.txt": "dev",
    "Fractalsense/requirements-dev.txt": "fractalsense",
}
HEADER = f"# Generated from uv.lock by uv {UV_VERSION}; run python tools/python_lock.py export.\n"
GROUPS = ("runtime", "test", "dev", "fractalsense", "audit", "sbom", "build")


def canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def uv(args: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        ["uv", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout if capture else ""


def require_uv() -> None:
    if uv(["--version"], capture=True).split()[:2] != ["uv", UV_VERSION]:
        raise ValueError(f"uv {UV_VERSION} is required")


def group_args(group: str) -> list[str]:
    return [] if group == "runtime" else ["--group", group]


def export_text(group: str) -> str:
    return HEADER + uv(
        [
            "export",
            "--locked",
            "--offline",
            "--no-default-groups",
            "--no-emit-project",
            "--no-header",
            "--no-annotate",
            *group_args(group),
        ],
        capture=True,
    )


def check() -> None:
    require_uv()
    uv(["lock", "--check", "--offline"])
    drift = [
        path
        for path, group in EXPORTS.items()
        if not (ROOT / path).is_file()
        or (ROOT / path).read_text(encoding="utf-8") != export_text(group)
    ]
    if drift:
        raise ValueError("Generated requirements drift: " + ", ".join(drift))


def export() -> None:
    require_uv()
    for path, group in EXPORTS.items():
        (ROOT / path).write_text(export_text(group), encoding="utf-8")


def lock_digest() -> str:
    return hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()


def inventory() -> dict:
    packages = {}
    for dist in importlib.metadata.distributions():
        name = canonical_name(dist.metadata["Name"])
        if name in packages:
            raise ValueError("Duplicate installed distribution: " + name)
        packages[name] = dist.version
    return {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "packages": dict(sorted(packages.items())),
    }


def environment_path() -> Path:
    path = Path(os.environ.get("UV_PROJECT_ENVIRONMENT", ".venv"))
    return path if path.is_absolute() else ROOT / path


def environment_python(env: Path) -> Path:
    return env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def environment_inventory(env: Path) -> dict:
    output = subprocess.check_output(
        [str(environment_python(env)), str(Path(__file__).resolve()), "inventory"],
        cwd=ROOT,
        text=True,
    )
    result = json.loads(output)
    if not isinstance(result, dict):
        raise ValueError("Invalid environment inventory")
    return result


def sync(group: str) -> None:
    check()
    common = [
        "sync",
        "--locked",
        "--no-default-groups",
        "--group",
        "build",
        *([] if group == "build" else group_args(group)),
        "--python",
        sys.executable,
    ]
    # Install locked build tools first. Project installation then cannot fetch
    # an untracked build backend in an isolated environment.
    uv([*common, "--no-install-project"])
    uv([*common, "--no-build-isolation"])
    env = environment_path()
    uv(["pip", "check", "--python", str(environment_python(env))])
    receipt = {"lock_digest": lock_digest(), "group": group, **environment_inventory(env)}
    (env / "lock-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def verify_sbom(bom: dict, receipt: dict, installed: dict, digest: str) -> None:
    if not all(isinstance(value, dict) for value in (bom, receipt, installed)):
        raise ValueError("Invalid SBOM/receipt/inventory object")
    if receipt.get("lock_digest") != digest:
        raise ValueError("Environment receipt does not match current uv.lock")
    expected = receipt.get("packages")
    if not isinstance(expected, dict) or not expected or expected != installed.get("packages"):
        raise ValueError("Installed environment drifted from its locked receipt")
    components = bom.get("components")
    if not isinstance(components, list):
        raise ValueError("SBOM has no component inventory")
    found = {}
    for item in components:
        if not isinstance(item, dict) or not item.get("name") or not item.get("version"):
            raise ValueError("SBOM component lacks name/version")
        name = canonical_name(item["name"])
        if name in found:
            raise ValueError("Duplicate SBOM component: " + name)
        found[name] = item["version"]
    # Some CycloneDX renderers place the project in metadata rather than the
    # dependency list. Accept it there only when it is an installed package.
    metadata = bom.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("Invalid SBOM metadata")
    root = metadata.get("component", {})
    if not isinstance(root, dict):
        raise ValueError("Invalid SBOM root component")
    root_name = canonical_name(root.get("name", ""))
    if root_name in expected and root_name not in found:
        found[root_name] = root.get("version")
    if found != expected:
        missing = sorted(set(expected) - set(found))
        extra = sorted(set(found) - set(expected))
        changed = sorted(
            name for name in set(found) & set(expected) if found[name] != expected[name]
        )
        raise ValueError(
            f"SBOM/lock receipt mismatch: missing={missing}, extra={extra}, changed={changed}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "export", "sync", "inventory", "verify-sbom"))
    parser.add_argument("--group", choices=GROUPS, default="runtime")
    parser.add_argument("--sbom", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            check()
        elif args.command == "export":
            export()
        elif args.command == "sync":
            sync(args.group)
        elif args.command == "inventory":
            print(json.dumps(inventory(), sort_keys=True))
        else:
            if args.sbom is None:
                raise ValueError("--sbom is required")
            env = environment_path()
            receipt = json.loads((env / "lock-receipt.json").read_text(encoding="utf-8"))
            bom = json.loads(args.sbom.read_text(encoding="utf-8"))
            verify_sbom(bom, receipt, environment_inventory(env), lock_digest())
            print("PASS: SBOM matches the current locked environment receipt")
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
