from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.validate_grimm_mereotopology_fixtures import (  # noqa: E402
    READER_ACTIONS,
    RELATIONS,
    load_bundle,
    validate_bundle,
)


class GrimmMereotopologyFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_bundle()

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
                self.assertEqual(
                    fixture["frameBridge"]["disposition"], "NO_FRAME_EFFECT"
                )

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

    def test_validator_rejects_collision_from_projected_crossing(self) -> None:
        malformed = copy.deepcopy(self.bundle)
        projected = next(
            fixture
            for fixture in malformed["fixtures"]
            if fixture["crossing"] == "PROJECTED"
        )
        projected["frameBridge"]["expectedCollisionProxy"] = True
        errors = validate_bundle(malformed)
        self.assertTrue(any("only EXACT_STATE_ID" in error for error in errors))

    def test_protected_origin_is_not_publicly_reconstructable(self) -> None:
        protected = next(
            fixture
            for fixture in self.bundle["fixtures"]
            if fixture["provenance"]["sourceVisibility"] == "protected-origin"
        )
        self.assertIsNone(protected["provenance"]["sourcePointer"])
        self.assertFalse(protected["provenance"]["publicReconstructionAllowed"])


if __name__ == "__main__":
    unittest.main()
