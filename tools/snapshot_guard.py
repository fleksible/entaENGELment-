#!/usr/bin/env python3
"""EntaENGELment Snapshot Guard (Final Hardened)

Zweck: Erstellt Manifest mit SHA-256 Hashes.
Härtung: commonpath-Check, Root-Globbing, Strict-Mode.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Iterable, List


def hash_file(path: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except FileNotFoundError:
        return "MISSING"


def get_repo_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, ".."))


def is_within_root(abs_path: str, repo_root: str) -> bool:
    try:
        return os.path.commonpath([abs_path, repo_root]) == repo_root
    except ValueError:
        return False


def build_file_list(repo_root: str, patterns: Iterable[str]) -> List[str]:
    files_to_process: List[str] = []
    for pattern in patterns:
        search_pattern = pattern if os.path.isabs(pattern) else os.path.join(repo_root, pattern)
        files_to_process.extend(glob.glob(search_pattern, recursive=True))
    return sorted(list(set(files_to_process)))


def create_manifest(repo_root: str, files: Iterable[str]) -> Dict[str, str]:
    manifest_files: Dict[str, str] = {}
    for fpath in files:
        if os.path.isfile(fpath):
            abs_path = os.path.abspath(fpath)
            if not is_within_root(abs_path, repo_root):
                print(f"[WARN] Skipping file outside repo root: {fpath}")
                continue
            rel_path = os.path.relpath(abs_path, start=repo_root).replace("\\", "/")
            manifest_files[rel_path] = hash_file(abs_path)
    return manifest_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_out", help="Path to output manifest.json")
    parser.add_argument("inputs", nargs="+", help="Input patterns (globs)")
    parser.add_argument("--strict", action="store_true", help="Fail if critical seeds are missing")
    args = parser.parse_args()

    repo_root = get_repo_root()
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repo_root_anchor": "REL_TO_ROOT",
        "files": {},
    }

    files_to_process = build_file_list(repo_root, args.inputs)
    manifest["files"] = create_manifest(repo_root, files_to_process)

    has_seeds = any(k.startswith("seeds/") for k in manifest["files"].keys())
    if not has_seeds:
        msg = "[WARN] No seeds/ detected in snapshot! Config drift risk."
        print(msg)
        if args.strict:
            print("[FAIL] Strict mode active. Aborting.")
            sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(args.manifest_out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.manifest_out, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"[SNAPSHOT] Generated at {args.manifest_out} ({len(manifest['files'])} files)")


if __name__ == "__main__":
    main()
