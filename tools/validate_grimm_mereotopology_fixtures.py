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
AUTHORITY_STATUSES = {"repo-local", "external-unverified", "derived"}
SOURCE_VISIBILITIES = {"public-safe", "protected-origin"}
NARROW_ORDER = ["title", "relation", "endpoints", "guard", "reentryQuestion"]

BUNDLE_KEYS = {
    "schemaVersion",
    "status",
    "claimLayer",
    "purpose",
    "invariants",
    "fixtures",
}
INVARIANT_KEYS = {
    "relationSet",
    "collisionSource",
    "colorCarriesMeaning",
    "motionCarriesMeaning",
    "readerActions",
    "minimumViewportCssPx",
}
FIXTURE_KEYS = {
    "id",
    "title",
    "relation",
    "crossing",
    "direction",
    "sourceNodeId",
    "targetNodeId",
    "plainLanguage",
    "guard",
    "reentryQuestion",
    "claimLayer",
    "provenance",
    "visualEncoding",
    "reader",
    "frameBridge",
}
PROVENANCE_KEYS = {
    "sourceForm",
    "sourcePointer",
    "authorityStatus",
    "sourceVisibility",
    "publicReconstructionAllowed",
}
VISUAL_KEYS = {
    "color",
    "linePattern",
    "relationLabel",
    "arrow",
    "staticFallback",
    "requiresColorForMeaning",
    "requiresMotionForMeaning",
}
READER_KEYS = {"actions", "orderAtNarrowWidth"}
FRAME_BRIDGE_KEYS = {
    "transitionPairId",
    "collisionSemantics",
    "leftStateId",
    "rightStateId",
    "expectedCollisionProxy",
    "disposition",
}


class DuplicateJSONKeyError(ValueError):
    """Raised when a JSON object contains a repeated member name."""


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


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for key, value in pairs:
        if key in loaded:
            raise DuplicateJSONKeyError(f"duplicate JSON key: {key!r}")
        loaded[key] = value
    return loaded


def load_bundle(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        loaded = json.load(handle, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(loaded, dict):
        raise ValueError("fixture root must be a JSON object")
    return loaded


def _reject_unknown_keys(
    value: dict[str, Any],
    allowed: set[str],
    prefix: str,
    errors: list[str],
) -> None:
    unknown_keys = [key for key in value if key not in allowed]
    for key in sorted(unknown_keys, key=repr):
        errors.append(f"{prefix}: unknown field {key!r}")


def _validate_exact_string_array(
    value: Any,
    expected: set[str],
    prefix: str,
    errors: list[str],
) -> set[str]:
    if not isinstance(value, list):
        errors.append(f"{prefix} must be an array")
        return set()

    observed: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{prefix}[{index}] must be a string")
            continue
        if item not in expected:
            errors.append(f"{prefix}[{index}] has unsupported value {item!r}")
        observed.append(item)

    if len(observed) != len(set(observed)):
        errors.append(f"{prefix} must not contain duplicates")
    if len(value) != len(expected) or set(observed) != expected:
        expected_text = ", ".join(sorted(expected))
        errors.append(f"{prefix} must contain exactly {expected_text}")
    return set(observed)


def _validate_enum(
    value: Any,
    expected: set[str],
    prefix: str,
    errors: list[str],
) -> str | None:
    if not isinstance(value, str):
        errors.append(f"{prefix} must be a string")
        return None
    if value not in expected:
        errors.append(f"{prefix} has unsupported value {value!r}")
        return None
    return value


def _validate_optional_string(
    value: Any,
    prefix: str,
    errors: list[str],
) -> None:
    if value is not None and (
        not isinstance(value, str) or not value.strip() or value != value.strip()
    ):
        errors.append(f"{prefix} must be null or a canonical non-empty string")


def validate_bundle(bundle: Any) -> list[str]:
    """Return all validation errors without mutating the supplied bundle."""

    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["bundle: fixture root must be an object"]

    _reject_unknown_keys(bundle, BUNDLE_KEYS, "bundle", errors)
    invariants = bundle.get("invariants")
    fixtures = bundle.get("fixtures")

    if bundle.get("schemaVersion") != "0.1":
        errors.append("bundle: schemaVersion must be 0.1")
    if bundle.get("status") != "[ANNEX]":
        errors.append("bundle: status must be [ANNEX]")
    if bundle.get("claimLayer") != "[SPEC-WIP]":
        errors.append("bundle: claimLayer must be [SPEC-WIP]")
    purpose = bundle.get("purpose")
    if not isinstance(purpose, str) or not purpose.strip():
        errors.append("bundle: purpose must be a non-empty string")

    if not isinstance(invariants, dict):
        errors.append("bundle: invariants must be an object")
    else:
        _reject_unknown_keys(invariants, INVARIANT_KEYS, "bundle.invariants", errors)
        _validate_exact_string_array(
            invariants.get("relationSet"),
            RELATIONS,
            "bundle: relationSet",
            errors,
        )
        if invariants.get("collisionSource") != "EXACT_STATE_ID":
            errors.append("bundle: collisionSource must be EXACT_STATE_ID")
        if invariants.get("colorCarriesMeaning") is not False:
            errors.append("bundle: colorCarriesMeaning must be false")
        if invariants.get("motionCarriesMeaning") is not False:
            errors.append("bundle: motionCarriesMeaning must be false")
        _validate_exact_string_array(
            invariants.get("readerActions"),
            READER_ACTIONS,
            "bundle: readerActions",
            errors,
        )
        viewport = invariants.get("minimumViewportCssPx")
        if not isinstance(viewport, int) or isinstance(viewport, bool) or viewport < 320:
            errors.append("bundle: minimumViewportCssPx must be an integer of at least 320")

    if not isinstance(fixtures, list):
        errors.append("bundle: fixtures must be an array")
        return errors
    if len(fixtures) != 6:
        errors.append("bundle: expected exactly six qualitative fixtures")

    ids: set[str] = set()
    observed_relations: set[str] = set()
    exact_witness_count = 0

    for index, fixture in enumerate(fixtures):
        index_prefix = f"fixtures[{index}]"
        if not isinstance(fixture, dict):
            errors.append(f"{index_prefix}: fixture must be an object")
            continue

        _reject_unknown_keys(fixture, FIXTURE_KEYS, index_prefix, errors)
        fixture_id = fixture.get("id")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            errors.append(f"{index_prefix}: id must be a non-empty string")
            prefix = index_prefix
        else:
            prefix = fixture_id
            if fixture_id in ids:
                errors.append(f"{prefix}: duplicate fixture id")
            ids.add(fixture_id)

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

        relation = _validate_enum(
            fixture.get("relation"),
            RELATIONS,
            f"{prefix}: relation",
            errors,
        )
        crossing = _validate_enum(
            fixture.get("crossing"),
            CROSSINGS,
            f"{prefix}: crossing",
            errors,
        )
        _validate_enum(
            fixture.get("direction"),
            DIRECTIONS,
            f"{prefix}: direction",
            errors,
        )
        if relation is not None:
            observed_relations.add(relation)

        provenance = fixture.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{prefix}: provenance must be an object")
        else:
            _reject_unknown_keys(
                provenance,
                PROVENANCE_KEYS,
                f"{prefix}: provenance",
                errors,
            )
            source_form = provenance.get("sourceForm")
            if not isinstance(source_form, str) or not source_form.strip():
                errors.append(f"{prefix}: provenance.sourceForm must be a non-empty string")
            authority = _validate_enum(
                provenance.get("authorityStatus"),
                AUTHORITY_STATUSES,
                f"{prefix}: provenance.authorityStatus",
                errors,
            )
            visibility = _validate_enum(
                provenance.get("sourceVisibility"),
                SOURCE_VISIBILITIES,
                f"{prefix}: provenance.sourceVisibility",
                errors,
            )
            source_pointer = provenance.get("sourcePointer")
            _validate_optional_string(
                source_pointer,
                f"{prefix}: provenance.sourcePointer",
                errors,
            )
            reconstruction = provenance.get("publicReconstructionAllowed")
            if not isinstance(reconstruction, bool):
                errors.append(f"{prefix}: provenance.publicReconstructionAllowed must be boolean")
            if visibility == "protected-origin":
                if source_pointer is not None:
                    errors.append(f"{prefix}: protected-origin must not carry sourcePointer")
                if reconstruction is not False:
                    errors.append(
                        f"{prefix}: protected-origin must set "
                        "publicReconstructionAllowed to false"
                    )
            if authority == "repo-local" and (
                not isinstance(source_pointer, str) or not source_pointer.strip()
            ):
                errors.append(f"{prefix}: repo-local provenance requires sourcePointer")

        visual = fixture.get("visualEncoding")
        if not isinstance(visual, dict):
            errors.append(f"{prefix}: visualEncoding must be an object")
        else:
            _reject_unknown_keys(
                visual,
                VISUAL_KEYS,
                f"{prefix}: visualEncoding",
                errors,
            )
            for field in (
                "color",
                "linePattern",
                "relationLabel",
                "arrow",
                "staticFallback",
            ):
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
            _reject_unknown_keys(reader, READER_KEYS, f"{prefix}: reader", errors)
            _validate_exact_string_array(
                reader.get("actions"),
                READER_ACTIONS,
                f"{prefix}: reader.actions",
                errors,
            )
            narrow_order = reader.get("orderAtNarrowWidth")
            if not isinstance(narrow_order, list) or narrow_order != NARROW_ORDER:
                errors.append(f"{prefix}: narrow-width reading order is unstable")

        frame_bridge = fixture.get("frameBridge")
        if not isinstance(frame_bridge, dict):
            errors.append(f"{prefix}: frameBridge must be an object")
            continue
        _reject_unknown_keys(
            frame_bridge,
            FRAME_BRIDGE_KEYS,
            f"{prefix}: frameBridge",
            errors,
        )

        expected_collision = frame_bridge.get("expectedCollisionProxy")
        if not isinstance(expected_collision, bool):
            errors.append(f"{prefix}: expectedCollisionProxy must be boolean")
        _validate_optional_string(
            frame_bridge.get("transitionPairId"),
            f"{prefix}: frameBridge.transitionPairId",
            errors,
        )

        if crossing != "EXACT_STATE_ID":
            if expected_collision is not False:
                errors.append(f"{prefix}: only EXACT_STATE_ID may produce collisionProxy=true")
            if frame_bridge.get("disposition") != "NO_FRAME_EFFECT":
                errors.append(f"{prefix}: non-exact crossings must have NO_FRAME_EFFECT")
            for field in ("collisionSemantics", "leftStateId", "rightStateId"):
                if frame_bridge.get(field) is not None:
                    errors.append(f"{prefix}: non-exact crossing must set {field} to null")
        else:
            exact_witness_count += 1
            if relation != "EQ":
                errors.append(f"{prefix}: EXACT_STATE_ID requires relation EQ")
            if frame_bridge.get("collisionSemantics") != "EXACT_STATE_ID":
                errors.append(f"{prefix}: exact witness requires EXACT_STATE_ID semantics")
            left = frame_bridge.get("leftStateId")
            right = frame_bridge.get("rightStateId")
            if (
                not isinstance(left, str)
                or not isinstance(right, str)
                or not left.strip()
                or not right.strip()
            ):
                errors.append(f"{prefix}: exact witness requires non-empty string state IDs")
            elif left != left.strip() or right != right.strip():
                errors.append(f"{prefix}: exact witness state IDs must not contain edge whitespace")
            elif left != right:
                errors.append(f"{prefix}: exact witness requires equal state IDs")
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
