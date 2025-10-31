"""Command line interface for the Bio Spiral Viewer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import indent

from .loader import load_manifest, load_viewer_state
from .viewer import format_viewer_state

DEFAULT_STATE_PATH = Path("data/state/bio_spiral_state.json")
DEFAULT_MANIFEST_PATH = Path("data/manifest/bio_spiral_manifest.json")


def _print_section(title: str, payload: dict) -> None:
    print(f"\n== {title} ==")
    for key, value in payload.items():
        if isinstance(value, dict):
            print(f"- {key}:")
            for line in json.dumps(value, indent=2).splitlines():
                print(indent(line, "  "))
        else:
            print(f"- {key}: {value}")


def run(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Bio Spiral Viewer console")
    parser.add_argument(
        "--state",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help="Path to the viewer state JSON payload.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="Path to the manifest JSON payload.",
    )
    args = parser.parse_args(argv)

    state = load_viewer_state(args.state)
    manifest = load_manifest(args.manifest)
    formatted = format_viewer_state(state)

    print("Bio Spiral Viewer Snapshot")
    print("===========================")

    _print_section("Body field", formatted["body"])
    _print_section("Spiral topology", formatted["spiral"])
    _print_section("Governance", formatted["governance"])

    print("\nManifest references:")
    for index in manifest.indices:
        print(f"- {index.identifier}: {index.description}")
        if index.artifacts:
            for artifact in index.artifacts:
                print(f"    · {artifact}")
        if index.sub_indices:
            for sub in index.sub_indices:
                print(f"    ↳ {sub.identifier}: {sub.description}")

    if manifest.seeds:
        print("\nSeed checkpoints:")
        for seed in manifest.seeds:
            print(f"- {seed.name} ({seed.path}) — {seed.summary}")

    if manifest.governance_artifacts:
        print("\nGovernance artifacts:")
        for artifact in manifest.governance_artifacts:
            print(f"- {artifact}")

    if manifest.konfab_artifacts:
        print("\nKONFAB ACM overlays:")
        for artifact in manifest.konfab_artifacts:
            print(f"- {artifact}")

    if manifest.lyra_artifacts:
        print("\nLyra T1.1 bundle:")
        for artifact in manifest.lyra_artifacts:
            print(f"- {artifact}")

    if manifest.overlay_artifacts:
        print("\nExplain overlays:")
        for artifact in manifest.overlay_artifacts:
            print(f"- {artifact}")


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    run()
