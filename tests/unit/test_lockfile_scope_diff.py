"""Discriminate inventory equality from dependency-resolution equality."""

import copy

import pytest
import yaml

from tools.lockfile_scope_diff import compare_locks, parse_lock


def lock():
    return {
        "lockfileVersion": "9.0",
        "packages": {"jest-message-util@30.4.1": {}, "picomatch@4.0.5": {}, "picomatch@4.0.7": {}},
        "snapshots": {"jest-message-util@30.4.1": {"dependencies": {"picomatch": "4.0.5"}}},
        "importers": {},
    }


def test_inventory_projection_misses_existing_version_rebinding():
    before = lock()
    after = copy.deepcopy(before)
    after["snapshots"]["jest-message-util@30.4.1"]["dependencies"]["picomatch"] = "4.0.7"
    result = compare_locks(before, after)
    assert result["package_inventory"]["added"] == []
    assert result["package_inventory"]["removed"] == []
    assert result["snapshot_edge_changes"] == [
        {
            "key": ["jest-message-util@30.4.1", "dependencies", "picomatch"],
            "change": "changed",
            "before": "4.0.5",
            "after": "4.0.7",
        }
    ]


def test_peer_context_rewrite_preserves_full_reference():
    before = lock()
    before["snapshots"]["jest-message-util@30.4.1"]["dependencies"]["picomatch"] = "4.0.5(peer@1)"
    after = copy.deepcopy(before)
    after["snapshots"]["jest-message-util@30.4.1"]["dependencies"]["picomatch"] = "4.0.5(peer@2)"
    row = compare_locks(before, after)["snapshot_edge_changes"][0]
    assert row["before"] == "4.0.5(peer@1)"
    assert row["after"] == "4.0.5(peer@2)"


def test_optional_and_required_edges_are_not_collapsed():
    before = lock()
    after = copy.deepcopy(before)
    after["snapshots"]["jest-message-util@30.4.1"] = {
        "optionalDependencies": {"picomatch": "4.0.5"}
    }
    rows = compare_locks(before, after)["snapshot_edge_changes"]
    assert {tuple(row["key"]) for row in rows} == {
        ("jest-message-util@30.4.1", "dependencies", "picomatch"),
        ("jest-message-util@30.4.1", "optionalDependencies", "picomatch"),
    }


def test_importer_resolution_and_declaration_changes_are_preserved():
    before = lock()
    before["importers"] = {
        "ui": {"dependencies": {"picomatch": {"specifier": "^4", "version": "4.0.5"}}}
    }
    after = copy.deepcopy(before)
    after["importers"]["ui"]["dependencies"]["picomatch"]["version"] = "4.0.7"
    assert compare_locks(before, after)["importer_edge_changes"][0]["after"] == {
        "specifier": "^4",
        "version": "4.0.7",
    }


def test_added_and_removed_snapshot_contexts_are_not_paired():
    before = lock()
    before["snapshots"] = {"x@1(peer@1)": {"dependencies": {"picomatch": "4.0.5"}}}
    after = copy.deepcopy(before)
    after["snapshots"] = {"x@1(peer@2)": {"dependencies": {"picomatch": "4.0.5"}}}
    result = compare_locks(before, after)
    assert result["snapshot_identifiers"] == {"added": ["x@1(peer@2)"], "removed": ["x@1(peer@1)"]}
    assert {row["change"] for row in result["snapshot_edge_changes"]} == {"added", "removed"}


def test_package_metadata_change_is_reported_without_identity_change():
    before = lock()
    after = copy.deepcopy(before)
    after["packages"]["picomatch@4.0.5"]["resolution"] = {"integrity": "changed"}
    result = compare_locks(before, after)
    assert result["package_inventory"]["changed_names"] == []
    assert (
        result["package_inventory"]["same_identifier_metadata_changes"][0]["key"]
        == "picomatch@4.0.5"
    )


@pytest.mark.parametrize(
    "text",
    [
        "lockfileVersion: '8.0'\npackages: {}\nsnapshots: {}\nimporters: {}\n",
        "lockfileVersion: '9.0'\npackages: {}\npackages: {}\nsnapshots: {}\nimporters: {}\n",
        "lockfileVersion: '9.0'\npackages: []\nsnapshots: {}\nimporters: {}\n",
    ],
)
def test_unsupported_or_ambiguous_input_is_rejected(text):
    with pytest.raises(ValueError):
        parse_lock(text)


def test_python_object_tags_are_not_constructed():
    with pytest.raises(yaml.constructor.ConstructorError):
        parse_lock("!!python/object/apply:builtins.str [untrusted]")
