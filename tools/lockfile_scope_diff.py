#!/usr/bin/env python3
"""Read two Git-bound pnpm v9 lockfiles; keep inventory and resolution edges separate.

This is an observation utility, not an audit gate or a dependency-safety claim.
Snapshot identifiers and peer suffixes remain opaque; no subtree equivalence is inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json

# Read-only Git object commands use an argv list, never a shell.
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

DEPENDENCY_GROUPS = ("dependencies", "devDependencies", "optionalDependencies")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys rather than silently dropping observations."""

    def construct_mapping(self, node: yaml.Node, deep: bool = False) -> dict[Any, Any]:
        if not isinstance(node, yaml.MappingNode):
            raise ValueError("Expected a YAML mapping")
        result: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("Lockfile mapping keys must be strings")
            if key in result:
                raise ValueError(f"Duplicate lockfile key: {key}")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"Expected string-keyed mapping: {label}")
    return value


def parse_lock(text: str) -> dict[str, Any]:
    loader = UniqueKeyLoader(text)
    try:
        lock = mapping(loader.get_single_data(), "lockfile")
    finally:
        loader.dispose()
    if str(lock.get("lockfileVersion")) != "9.0":
        raise ValueError("Only lockfileVersion 9.0 is supported")
    for section in ("packages", "snapshots", "importers"):
        for key, value in mapping(lock.get(section), section).items():
            mapping(value, f"{section}.{key}")
    try:
        json.dumps(lock, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("Lockfile must contain finite JSON-compatible values") from exc
    return lock


def changes(before: dict[Any, Any], after: dict[Any, Any]) -> list[dict[str, Any]]:
    rows = []
    for key in sorted(before.keys() | after.keys()):
        if key in before and key in after and before[key] == after[key]:
            continue
        rows.append(
            {
                "key": list(key) if isinstance(key, tuple) else key,
                "change": (
                    "added" if key not in before else "removed" if key not in after else "changed"
                ),
                "before": before.get(key),
                "after": after.get(key),
            }
        )
    return rows


def edges(lock: dict[str, Any], section: str) -> dict[tuple[str, str, str], Any]:
    result = {}
    for parent, record in lock[section].items():
        for group in DEPENDENCY_GROUPS:
            for name, reference in mapping(record.get(group, {}), f"{parent}.{group}").items():
                if section == "importers":
                    reference = mapping(reference, f"importers.{parent}.{group}.{name}")
                    if not isinstance(reference.get("version"), str):
                        raise ValueError(f"Missing string version: {parent}.{group}.{name}")
                elif not isinstance(reference, str):
                    raise ValueError(f"Expected string resolution: {parent}.{group}.{name}")
                result[(parent, group, name)] = reference
    return result


def metadata(lock: dict[str, Any], section: str) -> dict[str, Any]:
    return {
        parent: {key: value for key, value in record.items() if key not in DEPENDENCY_GROUPS}
        for parent, record in lock[section].items()
    }


def compare_locks(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    old, new = set(before["packages"]), set(after["packages"])
    added, removed = sorted(new - old), sorted(old - new)
    inventory = {
        "added": added,
        "removed": removed,
        "changed_names": sorted({key.rsplit("@", 1)[0] for key in added + removed}),
        "same_identifier_metadata_changes": changes(
            {key: before["packages"][key] for key in old & new},
            {key: after["packages"][key] for key in old & new},
        ),
    }
    return {
        "package_inventory": inventory,
        "snapshot_identifiers": {
            "added": sorted(set(after["snapshots"]) - set(before["snapshots"])),
            "removed": sorted(set(before["snapshots"]) - set(after["snapshots"])),
        },
        "snapshot_edge_changes": changes(edges(before, "snapshots"), edges(after, "snapshots")),
        "importer_edge_changes": changes(edges(before, "importers"), edges(after, "importers")),
        "snapshot_metadata_changes": changes(
            metadata(before, "snapshots"), metadata(after, "snapshots")
        ),
        "importer_metadata_changes": changes(
            metadata(before, "importers"), metadata(after, "importers")
        ),
        "other_top_level_changes": changes(
            {k: v for k, v in before.items() if k not in {"packages", "snapshots", "importers"}},
            {k: v for k, v in after.items() if k not in {"packages", "snapshots", "importers"}},
        ),
        "limits": [
            "Package identities alone do not detect resolution-edge rewrites.",
            "Full snapshot identifiers, dependency groups and peer suffixes are preserved.",
            "Added/removed snapshot contexts are not silently paired by package name.",
            "Dependency references are observed strings, not verified installed targets.",
            "No reachability, runtime, vulnerability or Next-only subtree claim is inferred.",
            "YAML comments and formatting are outside this structural comparison.",
        ],
    }


def git_bytes(repo: Path, *args: str) -> bytes:
    # Callers choose fixed subcommands; refs are resolved before object reads.
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def build_git_diff(repo: Path, base: str, head: str, path: str) -> dict[str, Any]:
    refs = [
        git_bytes(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
        .decode()
        .strip()
        for ref in (base, head)
    ]
    blobs = [git_bytes(repo, "show", f"{ref}:{path}") for ref in refs]
    result = compare_locks(*(parse_lock(blob.decode("utf-8")) for blob in blobs))
    result["sources"] = {
        "path": path,
        "base": refs[0],
        "head": refs[1],
        "base_blob": git_bytes(repo, "rev-parse", f"{refs[0]}:{path}").decode().strip(),
        "head_blob": git_bytes(repo, "rev-parse", f"{refs[1]}:{path}").decode().strip(),
        "base_sha256": hashlib.sha256(blobs[0]).hexdigest(),
        "head_sha256": hashlib.sha256(blobs[1]).hexdigest(),
        "raw_diff_sha256": hashlib.sha256(
            git_bytes(
                repo,
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--no-color",
                "--no-renames",
                "--unified=3",
                *refs,
                "--",
                path,
            )
        ).hexdigest(),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--path", default="pnpm-lock.yaml")
    args = parser.parse_args()
    try:
        result = build_git_diff(args.repo, args.base, args.head, args.path)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    except (
        ValueError,
        yaml.YAMLError,
        UnicodeError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"lockfile-scope-diff: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
