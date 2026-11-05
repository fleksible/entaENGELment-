#!/usr/bin/env python3
"""Maintain the sole Python lock and verify environment/SBOM receipts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
COMMANDS = ("check", "export", "sync", "inventory", "verify-sbom", "audit")


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


def audit_problems(report: dict, expected: set[tuple[str, str]]) -> list[str]:
    """Return every reason the pip-audit report fails; an empty list means clean.

    Fails closed: skipped packages, missing report entries and known
    vulnerabilities all count, so a partial audit can never pass as clean.
    """
    deps = report.get("dependencies") if isinstance(report, dict) else None
    if not isinstance(deps, list):
        return ["pip-audit report has no dependency list"]
    problems = []
    audited = set()
    for dep in deps:
        if not isinstance(dep, dict):
            problems.append("pip-audit report has a malformed dependency entry")
            continue
        name = canonical_name(str(dep.get("name", "")))
        version = str(dep.get("version", ""))
        if dep.get("skip_reason"):
            problems.append(f"{name} not audited: {dep['skip_reason']}")
            continue
        audited.add((name, version))
        for vuln in dep.get("vulns") or []:
            fixes = ", ".join(vuln.get("fix_versions") or []) or "none published"
            problems.append(f"{name}=={version}: {vuln.get('id')} (fixed in: {fixes})")
    missing = sorted(expected - audited)
    if missing:
        problems.append("not audited: " + ", ".join(f"{n}=={v}" for n, v in missing))
    return problems


def audit() -> None:
    """Audit every package version in uv.lock, across all groups and markers."""
    try:
        import tomllib
    except ModuleNotFoundError as exc:  # pragma: no cover - only below Python 3.11
        raise ValueError("audit needs Python >= 3.11 (the audit group's floor)") from exc

    check()
    beside = Path(sys.executable).parent / ("pip-audit.exe" if os.name == "nt" else "pip-audit")
    pip_audit = str(beside) if beside.is_file() else shutil.which("pip-audit")
    if pip_audit is None:
        raise ValueError("pip-audit not found; run: python tools/python_lock.py sync --group audit")
    with tempfile.TemporaryDirectory() as tmp:
        lock_dir = Path(tmp) / "lock"
        lock_dir.mkdir()
        pylock = lock_dir / "pylock.toml"
        uv(
            [
                "export",
                "--locked",
                "--offline",
                "--format",
                "pylock.toml",
                "--all-groups",
                "--no-emit-project",
                "--output-file",
                str(pylock),
            ],
            capture=True,
        )
        packages = tomllib.loads(pylock.read_text(encoding="utf-8")).get("packages", [])
        expected = {
            (canonical_name(str(pkg.get("name", ""))), str(pkg.get("version", "")))
            for pkg in packages
        }
        if not expected:
            raise ValueError("uv.lock export contains no packages to audit")
        report_path = Path(tmp) / "pip-audit.json"
        result = subprocess.run(
            [
                pip_audit,
                "--locked",
                str(lock_dir),
                "--format",
                "json",
                "--output",
                str(report_path),
                "--progress-spinner",
                "off",
            ],
            cwd=ROOT,
            check=False,
        )
        if not report_path.is_file():
            raise ValueError(f"pip-audit wrote no report (exit {result.returncode})")
        problems = audit_problems(json.loads(report_path.read_text(encoding="utf-8")), expected)
    if problems:
        raise ValueError(
            f"{len(problems)} audit finding(s) in {len(expected)} locked packages:\n  "
            + "\n  ".join(problems)
        )
    if result.returncode != 0:
        raise ValueError(f"pip-audit exited {result.returncode} without a reported finding")
    print(f"PASS: all {len(expected)} locked package versions audited, no known vulnerabilities")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=COMMANDS)
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
        elif args.command == "audit":
            audit()
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
