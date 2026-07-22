#!/usr/bin/env python3
"""Read-only validation for the Grimm-IR mereotopology intake fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RELATIONS = {"DC", "EC", "PO", "TPP", "NTPP", "EQ"}
CROSSINGS = {"PROJECTED", "OVER", "UNDER", "TOUCH", "EXACT_STATE_ID"}
DIRECTIONS = {"NONE", "FORWARD", "REVERSE", "BIDIRECTIONAL"}
READER_ACTIONS = {"ACCEPT", "REVISE", "REJECT", "SILENCE"}
NARROW_ORDER = ["title", "relation", "endpoints", "guard", "reentryQuestion"]


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


DEFAULT_FIXTURE = (
    _root()
    / "docs"
    / "narratives"
    / "grimm2"
    / "fixtures"
    / "mereotopology_edge_fixtures_v0_1.json"
)


def load_bundle(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError("fixture root must be a JSON object")
    return loaded


def validate_bundle(bundle: dict[str, Any]) -> list[str]:
    """Return all validation errors without mutating the supplied bundle."""

    errors: list[str] = []
    invariants = bundle.get("invariants")
    fixtures = bundle.get("fixtures")

    if bundle.get("schemaVersion") != "0.1":
        errors.append("bundle: schemaVersion must be 0.1")
    if not isinstance(invariants, dict):
        return [*errors, "bundle: invariants must be an object"]
    if not isinstance(fixtures, list):
        return [*errors, "bundle: fixtures must be an array"]

    if set(invariants.get("relationSet", [])) != RELATIONS:
        errors.append("bundle: relationSet must contain DC, EC, PO, TPP, NTPP, and EQ")
    if invariants.get("collisionSource") != "EXACT_STATE_ID":
        errors.append("bundle: collisionSource must be EXACT_STATE_ID")
    if invariants.get("colorCarriesMeaning") is not False:
        errors.append("bundle: colorCarriesMeaning must be false")
    if invariants.get("motionCarriesMeaning") is not False:
        errors.append("bundle: motionCarriesMeaning must be false")
    if set(invariants.get("readerActions", [])) != READER_ACTIONS:
        errors.append("bundle: readerActions must contain ACCEPT, REVISE, REJECT, and SILENCE")
    viewport = invariants.get("minimumViewportCssPx")
    if not isinstance(viewport, int) or isinstance(viewport, bool) or viewport < 320:
        errors.append("bundle: minimumViewportCssPx must be an integer of at least 320")

    if len(fixtures) != 6:
        errors.append("bundle: expected exactly six qualitative fixtures")

    ids: set[str] = set()
    observed_relations: set[str] = set()
    exact_witness_count = 0

    for index, fixture in enumerate(fixtures):
        prefix = f"fixtures[{index}]"
        if not isinstance(fixture, dict):
            errors.append(f"{prefix}: fixture must be an object")
            continue

        fixture_id = fixture.get("id")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
            fixture_id = prefix
        elif fixture_id in ids:
            errors.append(f"{fixture_id}: duplicate fixture id")
        ids.add(fixture_id)
        prefix = fixture_id

        for field in (
            "title",
            "sourceNodeId",
            "targetNodeId",
            "plainLanguage",
            "guard",
            "reentryQuestion",
            "claimLayer",
        ):
            value = fixture.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: {field} must be a non-empty string")

        plain_language = fixture.get("plainLanguage")
        if isinstance(plain_language, str) and len(plain_language) > 180:
            errors.append(f"{prefix}: plainLanguage must be at most 180 characters")

        relation = fixture.get("relation")
        crossing = fixture.get("crossing")
        direction = fixture.get("direction")
        if relation not in RELATIONS:
            errors.append(f"{prefix}: unsupported relation {relation!r}")
        else:
            observed_relations.add(relation)
        if crossing not in CROSSINGS:
            errors.append(f"{prefix}: unsupported crossing {crossing!r}")
        if direction not in DIRECTIONS:
            errors.append(f"{prefix}: unsupported direction {direction!r}")

        provenance = fixture.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{prefix}: provenance must be an object")
        else:
            for field in ("sourceForm", "authorityStatus", "sourceVisibility"):
                value = provenance.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}: provenance.{field} must be a non-empty string")
            if provenance.get("sourceVisibility") == "protected-origin":
                if provenance.get("publicReconstructionAllowed") is not False:
                    errors.append(
                        f"{prefix}: protected-origin must set publicReconstructionAllowed to false"
                    )

        visual = fixture.get("visualEncoding")
        if not isinstance(visual, dict):
            errors.append(f"{prefix}: visualEncoding must be an object")
        else:
            for field in ("linePattern", "relationLabel", "arrow", "staticFallback"):
                value = visual.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}: visualEncoding.{field} must be a non-empty string")
            if visual.get("requiresColorForMeaning") is not False:
                errors.append(f"{prefix}: color may not be required for meaning")
            if visual.get("requiresMotionForMeaning") is not False:
                errors.append(f"{prefix}: motion may not be required for meaning")

        reader = fixture.get("reader")
        if not isinstance(reader, dict):
            errors.append(f"{prefix}: reader must be an object")
        else:
            if set(reader.get("actions", [])) != READER_ACTIONS:
                errors.append(f"{prefix}: reader actions are incomplete")
            if reader.get("orderAtNarrowWidth") != NARROW_ORDER:
                errors.append(f"{prefix}: narrow-width reading order is unstable")

        frame_bridge = fixture.get("frameBridge")
        if not isinstance(frame_bridge, dict):
            errors.append(f"{prefix}: frameBridge must be an object")
            continue

        expected_collision = frame_bridge.get("expectedCollisionProxy")
        if not isinstance(expected_collision, bool):
            errors.append(f"{prefix}: expectedCollisionProxy must be boolean")

        if crossing != "EXACT_STATE_ID":
            if expected_collision is not False:
                errors.append(f"{prefix}: only EXACT_STATE_ID may produce collisionProxy=true")
            if frame_bridge.get("disposition") != "NO_FRAME_EFFECT":
                errors.append(f"{prefix}: non-exact crossings must have NO_FRAME_EFFECT")
        else:
            exact_witness_count += 1
            if relation != "EQ":
                errors.append(f"{prefix}: EXACT_STATE_ID requires relation EQ")
            if frame_bridge.get("collisionSemantics") != "EXACT_STATE_ID":
                errors.append(f"{prefix}: exact witness requires EXACT_STATE_ID semantics")
            left = frame_bridge.get("leftStateId")
            right = frame_bridge.get("rightStateId")
            if not isinstance(left, str) or not left or left != right:
                errors.append(f"{prefix}: exact witness requires equal non-empty state IDs")
            pair_id = frame_bridge.get("transitionPairId")
            if not isinstance(pair_id, str) or not pair_id.strip():
                errors.append(f"{prefix}: exact witness requires transitionPairId")
            if expected_collision is not True:
                errors.append(f"{prefix}: valid exact witness must expect collisionProxy=true")
            if frame_bridge.get("disposition") != "FRAME_WITNESS_REQUIRED":
                errors.append(f"{prefix}: exact crossing must have FRAME_WITNESS_REQUIRED")

    if observed_relations != RELATIONS:
        missing = ", ".join(sorted(RELATIONS - observed_relations)) or "none"
        errors.append(f"bundle: fixture relation coverage incomplete; missing {missing}")
    if exact_witness_count != 1:
        errors.append("bundle: expected exactly one EXACT_STATE_ID frame witness")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_FIXTURE)
    args = parser.parse_args()

    try:
        bundle = load_bundle(args.path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1

    errors = validate_bundle(bundle)
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: 6 Grimm-IR mereotopology fixtures satisfy the intake invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
