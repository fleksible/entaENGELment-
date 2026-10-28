"""
tests/ethics/test_trust_visibility_boundaries.py

Boundary tests for the existing trust normalisation and visibility clamping
(V7 mapping, docs/annex/AGENT_INJECTION_PATTERNS_MAPPING_v0_1.md).

They pin current fail-closed behaviour: unknown or malformed trust is UNTRUSTED,
and a proposal is never more public than its source material. They do not cover
derived material: the repo has no derivation tracking for trust (documented gap).
"""

import itertools

import pytest

from src.core.action_gate import ActionReasonCode, build_action_proposal
from src.core.evidence_routing import (
    GUARD_HOLD,
    TRUST_REVIEWED,
    TRUST_TRUSTED,
    TRUST_UNTRUSTED,
    MaterialRef,
    normalize_trust,
)

VISIBILITY_ORDER = {"private": 0, "reduced": 1, "public": 2}


class _StrSubclass(str):
    pass


def make_material(**overrides):
    data = {
        "material_id": "mat-001",
        "schema_version": "erk.v0.1",
        "kind": "document",
        "source": "external",
        "revision": "r1",
        "locator": "INBOX/setup.md",
        "digest": "sha256:01",
        "origin": "external_untrusted",
        "actor": "origin:external",
        "trust": TRUST_REVIEWED,
        "visibility": "reduced",
        "status": "ACTIVE",
    }
    data.update(overrides)
    return MaterialRef(**data)


def build(material, visibility=None):
    return build_action_proposal(
        action_id="act-001",
        source_material=material,
        proposed_command="install pinned local resource",
        ecosystem="pypi",
        package_or_resource="example-lib",
        requested_version="1.2.3",
        registry_or_origin="pypi.org",
        network_required=False,
        reversibility="reversible",
        verification_status="verified",
        visibility=visibility,
    )


class TestTrustNormalisation:
    @pytest.mark.parametrize("value", [TRUST_TRUSTED, TRUST_REVIEWED, TRUST_UNTRUSTED])
    def test_known_levels_are_kept(self, value):
        assert normalize_trust(value) == value

    @pytest.mark.parametrize(
        "value",
        ["trusted", " TRUSTED", "TRUSTED ", "", "VERIFIED", None, 1, b"TRUSTED", ["TRUSTED"]],
    )
    def test_unknown_or_malformed_trust_is_untrusted(self, value):
        assert normalize_trust(value) == TRUST_UNTRUSTED

    @pytest.mark.parametrize(
        "trust", ["trusted", " REVIEWED", "SOMETHING_NEW", _StrSubclass(TRUST_TRUSTED)]
    )
    def test_action_gate_holds_for_unrecognised_trust(self, trust):
        proposal = build(make_material(trust=trust))
        assert proposal.guard_state == GUARD_HOLD
        assert ActionReasonCode.UNTRUSTED_SOURCE_MATERIAL.value in proposal.reason_codes
        assert proposal.human_approval_required is True

    @pytest.mark.parametrize("trust", [TRUST_TRUSTED, TRUST_REVIEWED])
    def test_recognised_trust_alone_does_not_hold(self, trust):
        proposal = build(make_material(trust=trust))
        assert ActionReasonCode.UNTRUSTED_SOURCE_MATERIAL.value not in proposal.reason_codes


class TestVisibilityClamping:
    @pytest.mark.parametrize("source", ["private", "reduced", "public"])
    def test_none_inherits_source_visibility(self, source):
        assert build(make_material(visibility=source)).visibility == source

    @pytest.mark.parametrize("source", ["cosmic", "", "PUBLIC", None, 1])
    def test_unknown_source_visibility_is_private(self, source):
        for requested in (None, "private", "reduced", "public"):
            assert build(make_material(visibility=source), visibility=requested).visibility == (
                "private"
            )

    def test_proposal_is_never_more_public_than_its_source(self):
        levels = ["private", "reduced", "public"]
        for source, requested in itertools.product(levels, levels):
            result = build(make_material(visibility=source), visibility=requested).visibility
            assert VISIBILITY_ORDER[result] <= VISIBILITY_ORDER[source]
            assert result == min(source, requested, key=VISIBILITY_ORDER.__getitem__)
