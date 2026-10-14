#!/usr/bin/env python3
"""Automated cases for verify_counts.py.

Standard library only, so the cases run in any environment that can run the
verifier itself:

    python3 docs/intake/raw/2026-10-13/corpus-v17/test_verify_counts.py

Each case copies the files the verifier reads into a temporary root and tampers
with exactly one thing. Scope selection, the linked intake row and both success
statuses are covered alongside the counter, CSV, manifest, identity and
continuation guards.

The v18 scope is exercised against a synthetic index rebuilt from the committed
delta, with the expected original hash repointed at that synthetic file. That
proves the code path, it does not re-run the comparison against the real private
original. Set ENTA_V18_INPUT to the real materialized v18 index to add that run.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BUNDLE_REL = "docs/intake/raw/2026-10-13/corpus-v17"
BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parents[4]
INDEX_REL = "docs/intake/INDEX.md"
MANIFEST_REL = f"{BUNDLE_REL}/MANIFEST.json"


def _verifier():
    spec = importlib.util.spec_from_file_location("verify_counts", BUNDLE / "verify_counts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VC = _verifier()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def regenerate_manifest(root):
    """Rehash every declared package file; the manifest never hashes itself."""
    bundle = root / BUNDLE_REL
    payload = read_json(bundle / "corpus-delta.json")
    manifest = read_json(bundle / "MANIFEST.json")
    manifest["files"] = [
        {"path": rel, "bytes": (root / rel).stat().st_size, "sha256": digest(root / rel)}
        for rel in payload["manifest_files"]
    ]
    write_json(bundle / "MANIFEST.json", manifest)


def build_root(target):
    payload = read_json(BUNDLE / "corpus-delta.json")
    wanted = [*payload["manifest_files"], payload["baseline"]["path"], INDEX_REL, MANIFEST_REL]
    for rel in dict.fromkeys(wanted):
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, destination)
    return target


def rebuild_state18(root):
    bundle = root / BUNDLE_REL
    payload = VC.load_json(bundle / "corpus-delta.json")
    base = VC.load_json(root / payload["baseline"]["path"])
    keys = ("entries", "pending_candidates", "relations", "conflicts")
    state = {key: base[key] for key in keys}
    state = VC.apply_delta(state, payload["delta_v10_v17"])
    return VC.apply_delta(state, payload["followup_v17_v18"])


def synthetic_v18(root, mutate=None):
    """Write a synthetic v18 index and repoint the expected original hash at it."""
    state = rebuild_state18(root)
    index = {
        "entries": state["entries"],
        "discovery": [{"pending_candidates": state["pending_candidates"]}],
        "relations": state["relations"],
        "conflicts": state["conflicts"],
    }
    if mutate is not None:
        mutate(index)
    path = root / "synthetic-v18-index.md"
    body = json.dumps(index, ensure_ascii=False)
    path.write_text(f"# synthetic v18\n\n```json\n{body}\n```\n", encoding="utf-8")
    bundle = root / BUNDLE_REL
    previous = read_json(bundle / "corpus-delta.json")["provenance"]["materialized_v18"]["sha256"]
    current = digest(path)
    for name in ("corpus-delta.json", "README.md", "EXPORT.md"):
        document = bundle / name
        document.write_text(
            document.read_text(encoding="utf-8").replace(previous, current), encoding="utf-8"
        )
    regenerate_manifest(root)
    return path


class VerifierCase(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = build_root(Path(self._temporary.name))

    def run_verifier(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                str(self.root / BUNDLE_REL / "verify_counts.py"),
                "--root",
                str(self.root),
                "--bundle",
                str(self.root / BUNDLE_REL),
                *arguments,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def assertPasses(self, status, *arguments):
        result = self.run_verifier(*arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], status)
        return report

    def assertFails(self, fragment, *arguments, returncode=1):
        result = self.run_verifier(*arguments)
        self.assertEqual(result.returncode, returncode, result.stdout)
        self.assertIn(fragment, result.stdout + result.stderr)
        self.assertNotIn('"status"', result.stdout)
        return result

    def edit_payload(self, change):
        path = self.root / BUNDLE_REL / "corpus-delta.json"
        payload = read_json(path)
        change(payload)
        write_json(path, payload)
        regenerate_manifest(self.root)

    def index_text(self):
        return (self.root / INDEX_REL).read_text(encoding="utf-8")

    def write_index(self, text):
        (self.root / INDEX_REL).write_text(text, encoding="utf-8")

    def intake_line(self):
        identifier = read_json(self.root / BUNDLE_REL / "corpus-delta.json")["intake"]["id"]
        lines = [line for line in self.index_text().splitlines() if identifier in line]
        self.assertEqual(len(lines), 1)
        return lines[0]


class ScopeSelection(VerifierCase):
    def test_export_only_scope_passes_and_names_its_limit(self):
        report = self.assertPasses("PASS_EXPORT_ONLY", "--export-only")
        self.assertFalse(report["input_v18_checked"])
        self.assertTrue(any("original bytes" in entry for entry in report["not_checked"]))
        self.assertEqual(report["metrics"]["v18"]["points"], 259)
        self.assertEqual(report["metrics"]["v17"]["points"], 258)

    def test_no_scope_is_a_cli_error(self):
        result = self.run_verifier()
        self.assertEqual(result.returncode, 2)
        self.assertIn("--export-only", result.stderr)

    def test_both_scopes_are_a_cli_error(self):
        result = self.run_verifier("--export-only", "--input-v18", str(self.root / "any.md"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("not allowed with argument", result.stderr)

    def test_missing_input_never_falls_back_to_export_scope(self):
        self.assertFails("missing or not a file", "--input-v18", str(self.root / "absent.md"))

    def test_wrong_input_hash_fails(self):
        other = self.root / "other.md"
        other.write_text("not the index\n", encoding="utf-8")
        self.assertFails("byte hash mismatch", "--input-v18", str(other))

    def test_synthetic_v18_scope_passes_with_its_own_status(self):
        path = synthetic_v18(self.root)
        report = self.assertPasses("PASS_WITH_V18_INPUT", "--input-v18", str(path))
        self.assertTrue(report["input_v18_checked"])

    def test_matching_hash_but_differing_content_fails(self):
        def drop_a_relation(index):
            index["relations"] = index["relations"][:-1]

        path = synthetic_v18(self.root, mutate=drop_a_relation)
        self.assertFails("differs from the direct v18 index", "--input-v18", str(path))

    @unittest.skipUnless(os.environ.get("ENTA_V18_INPUT"), "real v18 original not supplied")
    def test_real_v18_original_when_supplied(self):
        report = self.assertPasses(
            "PASS_WITH_V18_INPUT", "--input-v18", os.environ["ENTA_V18_INPUT"]
        )
        self.assertTrue(report["input_v18_checked"])


class IntakeRow(VerifierCase):
    def test_linked_row_is_counted_once(self):
        identifier = read_json(self.root / BUNDLE_REL / "corpus-delta.json")["intake"]["id"]
        self.assertEqual(self.index_text().count(identifier), 2)
        self.assertPasses("PASS_EXPORT_ONLY", "--export-only")

    def test_two_real_rows_fail(self):
        self.write_index(self.index_text() + self.intake_line() + "\n")
        self.assertFails("found 2", "--export-only")

    def test_second_id_header_fails(self):
        self.write_index(self.index_text() + "\n| ID | Note |\n| --- | --- |\n")
        self.assertFails("intake table header, found 2", "--export-only")

    def test_duplicate_with_missing_cell_fails(self):
        line = self.intake_line()
        shorter = "|".join(line.split("|")[:-2]) + "|"
        self.write_index(self.index_text().replace(line, line + "\n" + shorter, 1))
        self.assertFails("has 6 cells; expected 7", "--export-only")

    def test_duplicate_with_extra_cell_fails(self):
        line = self.intake_line()
        self.write_index(self.index_text().replace(line, line + "\n" + line + " extra |", 1))
        self.assertFails("has 8 cells; expected 7", "--export-only")

    def test_duplicate_with_optional_outer_pipes_fails(self):
        original = self.index_text()
        line = self.intake_line()
        for variant in (line[:-1], line[1:], line[1:-1]):
            with self.subTest(row=variant):
                self.write_index(original.replace(line, line + "\n" + variant, 1))
                self.assertFails("found 2", "--export-only")

    def test_single_row_with_optional_outer_pipes_passes(self):
        original = self.index_text()
        line = self.intake_line()
        for variant in (line[:-1], line[1:], line[1:-1]):
            with self.subTest(row=variant):
                self.write_index(original.replace(line, variant, 1))
                self.assertPasses("PASS_EXPORT_ONLY", "--export-only")

    def test_unlinked_identifier_cell_fails(self):
        line = self.intake_line()
        identifier = read_json(self.root / BUNDLE_REL / "corpus-delta.json")["intake"]["id"]
        plain = line.replace(f"[{identifier}](records/{identifier}.md)", identifier, 1)
        self.write_index(self.index_text().replace(line, plain))
        self.assertFails("is not a link", "--export-only")

    def test_wrong_record_target_fails(self):
        line = self.intake_line()
        self.write_index(self.index_text().replace(line, line.replace("records/", "record/", 1)))
        self.assertFails("must link to", "--export-only")

    def test_missing_overview_link_fails(self):
        line = self.intake_line()
        broken = line.replace(
            "[Korpus v17 mit v18-Folgestand](", "Korpus v17 mit v18-Folgestand(", 1
        )
        self.write_index(self.index_text().replace(line, broken))
        self.assertFails("does not link to", "--export-only")

    def test_removing_a_declared_file_fails_at_the_manifest_first(self):
        """Both link targets are declared package files, so the manifest guards them earlier."""
        record = read_json(self.root / BUNDLE_REL / "corpus-delta.json")["intake"]["record"]
        (self.root / record).unlink()
        self.assertFails("No such file", "--export-only")

    def test_link_target_existence_is_checked_directly(self):
        """The row check is defence in depth behind the manifest, so call it on its own."""
        bundle = self.root / BUNDLE_REL
        payload = read_json(bundle / "corpus-delta.json")
        (self.root / payload["intake"]["record"]).unlink()
        with self.assertRaises(ValueError) as caught:
            VC.check_intake_row(self.root, bundle, payload)
        self.assertIn("link target missing", str(caught.exception))

    def test_changed_intake_status_fails(self):
        line = self.intake_line()
        self.write_index(self.index_text().replace(line, line.replace("| raw |", "| triaged |", 1)))
        self.assertFails("must stay raw", "--export-only")


class PayloadGuards(VerifierCase):
    def test_counter_tampering_fails(self):
        self.edit_payload(lambda payload: payload["metrics"]["v18"].__setitem__("points", 258))
        self.assertFails("counters or tag totals disagree", "--export-only")

    def test_baseline_tampering_fails(self):
        baseline = self.root / read_json(BUNDLE / "corpus-delta.json")["baseline"]["path"]
        baseline.write_bytes(baseline.read_bytes() + b"\n")
        self.assertFails("Baseline hash mismatch", "--export-only")

    def test_duplicate_new_entry_fails(self):
        def duplicate(payload):
            entries = payload["delta_v10_v17"]["new_entries"]
            entries.append(copy.deepcopy(entries[0]))

        self.edit_payload(duplicate)
        self.assertFails("already exists", "--export-only")

    def test_partial_without_continuation_fails(self):
        def drop_continuation(payload):
            for entry in payload["followup_v17_v18"]["new_entries"]:
                if entry.get("read_state") == "PARTIAL":
                    entry["next_read"] = None
                    return
            raise AssertionError("no PARTIAL follow-up entry to tamper with")

        self.edit_payload(drop_continuation)
        self.assertFails("PARTIAL without continuation", "--export-only")

    def test_csv_tampering_fails(self):
        matrix = self.root / BUNDLE_REL / "corpus-matrix.csv"
        matrix.write_text(matrix.read_text(encoding="utf-8") + "extra\n", encoding="utf-8")
        regenerate_manifest(self.root)
        self.assertFails("CSV matrix differs", "--export-only")

    def test_manifest_tampering_fails(self):
        path = self.root / MANIFEST_REL
        manifest = read_json(path)
        manifest["files"][0]["bytes"] += 1
        write_json(path, manifest)
        self.assertFails("Manifest integrity failure", "--export-only")

    def test_manifest_cardinality_mismatch_fails(self):
        path = self.root / MANIFEST_REL
        manifest = read_json(path)
        manifest["files"] = manifest["files"][:-1]
        write_json(path, manifest)
        self.assertFails("Manifest cardinality mismatch", "--export-only")


if __name__ == "__main__":
    unittest.main(verbosity=2)
