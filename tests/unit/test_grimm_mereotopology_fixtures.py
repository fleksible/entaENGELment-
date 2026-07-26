from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.validate_grimm_mereotopology_fixtures import (  # noqa: E402
    READER_ACTIONS,
    RELATIONS,
    DuplicateJSONKeyError,
    load_bundle,
    validate_bundle,
)


class GrimmMereotopologyFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_bundle()

    def assert_rejected(self, bundle: Any, message: str | None = None) -> list[str]:
        errors = validate_bundle(bundle)
        self.assertIsInstance(errors, list)
        self.assertTrue(errors, "malformed JSON-shaped input unexpectedly passed")
        if message is not None:
            self.assertTrue(
                any(message in error for error in errors),
                f"{message!r} absent from {errors!r}",
            )
        return errors

    def fixture(self, relation: str) -> dict[str, Any]:
        return next(
            fixture for fixture in self.bundle["fixtures"] if fixture["relation"] == relation
        )

    def mutated_fixture(self, relation: str) -> tuple[dict[str, Any], dict[str, Any]]:
        bundle = copy.deepcopy(self.bundle)
        fixture = next(fixture for fixture in bundle["fixtures"] if fixture["relation"] == relation)
        return bundle, fixture

    def test_bundle_satisfies_all_intake_invariants(self) -> None:
        self.assertEqual(validate_bundle(self.bundle), [])

    def test_six_fixtures_cover_each_relation_exactly_once(self) -> None:
        relations = [fixture["relation"] for fixture in self.bundle["fixtures"]]
        self.assertEqual(len(relations), 6)
        self.assertEqual(set(relations), RELATIONS)
        self.assertEqual(len(relations), len(set(relations)))

    def test_non_exact_crossings_never_create_collision(self) -> None:
        for fixture in self.bundle["fixtures"]:
            if fixture["crossing"] == "EXACT_STATE_ID":
                continue
            with self.subTest(fixture=fixture["id"]):
                self.assertFalse(fixture["frameBridge"]["expectedCollisionProxy"])
                self.assertEqual(fixture["frameBridge"]["disposition"], "NO_FRAME_EFFECT")

    def test_exact_collision_has_frame_owned_witness(self) -> None:
        exact = [
            fixture
            for fixture in self.bundle["fixtures"]
            if fixture["crossing"] == "EXACT_STATE_ID"
        ]
        self.assertEqual(len(exact), 1)
        bridge = exact[0]["frameBridge"]
        self.assertEqual(exact[0]["relation"], "EQ")
        self.assertEqual(bridge["collisionSemantics"], "EXACT_STATE_ID")
        self.assertEqual(bridge["leftStateId"], bridge["rightStateId"])
        self.assertTrue(bridge["expectedCollisionProxy"])

    def test_reader_colorless_motionless_and_narrow_width_contracts(self) -> None:
        self.assertGreaterEqual(self.bundle["invariants"]["minimumViewportCssPx"], 320)
        for fixture in self.bundle["fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(set(fixture["reader"]["actions"]), READER_ACTIONS)
                self.assertFalse(fixture["visualEncoding"]["requiresColorForMeaning"])
                self.assertFalse(fixture["visualEncoding"]["requiresMotionForMeaning"])
                self.assertTrue(fixture["visualEncoding"]["relationLabel"])
                self.assertTrue(fixture["visualEncoding"]["linePattern"])
                self.assertTrue(fixture["visualEncoding"]["staticFallback"])

    def test_validator_is_total_for_json_scalar_and_array_roots(self) -> None:
        for value in (None, False, True, 0, 1, 1.5, "", "bundle", [], [None]):
            with self.subTest(value=value):
                self.assert_rejected(value, "fixture root must be an object")

    def test_validator_rejects_non_array_set_fields_without_raising(self) -> None:
        invalid_values = (None, False, True, 0, 1.5, "DC", {})
        for field in ("relationSet", "readerActions"):
            for value in invalid_values:
                malformed = copy.deepcopy(self.bundle)
                malformed["invariants"][field] = value
                with self.subTest(field=field, value=value):
                    self.assert_rejected(malformed, "must be an array")

        for value in invalid_values:
            malformed, fixture = self.mutated_fixture("DC")
            fixture["reader"]["actions"] = value
            with self.subTest(field="reader.actions", value=value):
                self.assert_rejected(malformed, "must be an array")

    def test_validator_rejects_non_object_nested_values_without_raising(self) -> None:
        invalid_values = (None, False, True, 0, 1.5, "object", [])
        for field in ("provenance", "visualEncoding", "reader", "frameBridge"):
            for value in invalid_values:
                malformed, fixture = self.mutated_fixture("DC")
                fixture[field] = value
                with self.subTest(field=field, value=value):
                    self.assert_rejected(malformed, f"{field} must be an object")

        for value in invalid_values:
            malformed = copy.deepcopy(self.bundle)
            malformed["invariants"] = value
            with self.subTest(field="invariants", value=value):
                self.assert_rejected(malformed, "invariants must be an object")

    def test_validator_rejects_non_object_fixture_members_without_raising(self) -> None:
        for value in (None, False, True, 0, 1.5, "fixture", []):
            malformed = copy.deepcopy(self.bundle)
            malformed["fixtures"][0] = value
            with self.subTest(value=value):
                self.assert_rejected(malformed, "fixture must be an object")

    def test_validator_rejects_non_string_and_duplicate_set_members(self) -> None:
        cases = (
            ("relationSet", [None], "must be a string"),
            ("relationSet", [{}], "must be a string"),
            ("relationSet", ["DC", "DC"], "must not contain duplicates"),
            ("readerActions", [True], "must be a string"),
            ("readerActions", [[]], "must be a string"),
            ("readerActions", ["ACCEPT", "ACCEPT"], "must not contain duplicates"),
        )
        for field, value, expected in cases:
            malformed = copy.deepcopy(self.bundle)
            malformed["invariants"][field] = value
            with self.subTest(field=field, value=value):
                self.assert_rejected(malformed, expected)

        malformed, fixture = self.mutated_fixture("DC")
        fixture["reader"]["actions"] = ["ACCEPT", {}]
        self.assert_rejected(malformed, "must be a string")

    def test_validator_rejects_invalid_scalar_enums_without_raising(self) -> None:
        invalid_values = (None, False, True, 0, 1.5, [], {}, "NOT_VALID")
        fixture_fields = ("relation", "crossing", "direction")
        for field in fixture_fields:
            for value in invalid_values:
                malformed, fixture = self.mutated_fixture("DC")
                fixture[field] = value
                with self.subTest(field=field, value=value):
                    self.assert_rejected(malformed, f"{field} ")

        provenance_fields = ("authorityStatus", "sourceVisibility")
        for field in provenance_fields:
            for value in invalid_values:
                malformed, fixture = self.mutated_fixture("DC")
                fixture["provenance"][field] = value
                with self.subTest(field=field, value=value):
                    self.assert_rejected(malformed, f"provenance.{field}")

    def test_validator_rejects_collision_from_projected_crossing(self) -> None:
        malformed, projected = self.mutated_fixture("DC")
        projected["frameBridge"]["expectedCollisionProxy"] = True
        self.assert_rejected(malformed, "only EXACT_STATE_ID")

    def test_non_exact_crossings_reject_frame_owned_witness_fields(self) -> None:
        mutations = {
            "collisionSemantics": "EXACT_STATE_ID",
            "leftStateId": "S4:1234",
            "rightStateId": "S4:1234",
        }
        for field, value in mutations.items():
            malformed, projected = self.mutated_fixture("DC")
            projected["frameBridge"][field] = value
            with self.subTest(field=field):
                self.assert_rejected(
                    malformed,
                    f"non-exact crossing must set {field} to null",
                )

    def test_non_exact_crossing_may_retain_transition_pair_reference(self) -> None:
        malformed, projected = self.mutated_fixture("DC")
        projected["frameBridge"]["transitionPairId"] = "bt-reference-only"
        self.assertEqual(validate_bundle(malformed), [])

    def test_exact_state_ids_must_be_canonical_non_empty_equal_strings(self) -> None:
        cases = (
            ("leftStateId", None, "non-empty string state IDs"),
            ("leftStateId", 1234, "non-empty string state IDs"),
            ("leftStateId", "   ", "non-empty string state IDs"),
            ("rightStateId", [], "non-empty string state IDs"),
            ("leftStateId", " S4:1234", "must not contain edge whitespace"),
            ("rightStateId", "S4:1234 ", "must not contain edge whitespace"),
            ("rightStateId", "S4:5678", "requires equal state IDs"),
        )
        for field, value, expected in cases:
            malformed, exact = self.mutated_fixture("EQ")
            exact["frameBridge"][field] = value
            with self.subTest(field=field, value=value):
                self.assert_rejected(malformed, expected)

    def test_protected_origin_is_not_publicly_reconstructable(self) -> None:
        protected = next(
            fixture
            for fixture in self.bundle["fixtures"]
            if fixture["provenance"]["sourceVisibility"] == "protected-origin"
        )
        self.assertIsNone(protected["provenance"]["sourcePointer"])
        self.assertFalse(protected["provenance"]["publicReconstructionAllowed"])

    def test_validator_rejects_populated_protected_source_pointer(self) -> None:
        malformed, protected = self.mutated_fixture("NTPP")
        protected["provenance"]["sourcePointer"] = "private/origin.md"
        self.assert_rejected(malformed, "protected-origin must not carry sourcePointer")

    def test_validator_rejects_invalid_reconstruction_flag_types(self) -> None:
        for value in (None, True, 0, 1, "false", [], {}):
            malformed, protected = self.mutated_fixture("NTPP")
            protected["provenance"]["publicReconstructionAllowed"] = value
            with self.subTest(value=value):
                self.assert_rejected(
                    malformed,
                    "publicReconstructionAllowed",
                )

    def test_validator_rejects_shadow_fields_that_bypass_privacy_shape(self) -> None:
        malformed, protected = self.mutated_fixture("NTPP")
        protected["rawBiography"] = "must not pass the public intake"
        self.assert_rejected(malformed, "unknown field 'rawBiography'")

        malformed, protected = self.mutated_fixture("NTPP")
        protected["provenance"]["privateNotes"] = "must not pass provenance"
        self.assert_rejected(malformed, "unknown field 'privateNotes'")

    def test_validator_rejects_unknown_nested_fields(self) -> None:
        for object_name, field in (
            ("visualEncoding", "hiddenMeaning"),
            ("reader", "coerciveDefault"),
            ("frameBridge", "collisionOverride"),
        ):
            malformed, fixture = self.mutated_fixture("DC")
            fixture[object_name][field] = True
            with self.subTest(object_name=object_name, field=field):
                self.assert_rejected(malformed, f"unknown field {field!r}")

    def test_validator_rejects_non_canonical_optional_strings(self) -> None:
        for value in (False, True, 0, 1.5, [], {}, "", "  ", " path.md"):
            malformed, fixture = self.mutated_fixture("DC")
            fixture["provenance"]["sourcePointer"] = value
            with self.subTest(value=value):
                self.assert_rejected(malformed, "canonical non-empty string")

    def test_bundle_authority_metadata_is_enforced(self) -> None:
        for field, value, expected in (
            ("status", "[CANON]", "status must be [ANNEX]"),
            ("status", None, "status must be [ANNEX]"),
            ("claimLayer", "[FACT]", "claimLayer must be [SPEC-WIP]"),
            ("claimLayer", {}, "claimLayer must be [SPEC-WIP]"),
        ):
            malformed = copy.deepcopy(self.bundle)
            malformed[field] = value
            with self.subTest(field=field, value=value):
                self.assert_rejected(malformed, expected)

    def test_loader_rejects_duplicate_json_keys_at_any_depth(self) -> None:
        documents = (
            '{"schemaVersion":"0.1","schemaVersion":"0.2"}',
            '{"outer":{"sourcePointer":null,"sourcePointer":"private.md"}}',
        )
        for document in documents:
            with self.subTest(document=document):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "duplicate.json"
                    path.write_text(document, encoding="utf-8")
                    with self.assertRaises(DuplicateJSONKeyError):
                        load_bundle(path)


if __name__ == "__main__":
    unittest.main()
