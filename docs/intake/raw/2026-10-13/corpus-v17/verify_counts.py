#!/usr/bin/env python3
"""Read-only verifier for the v10 -> frozen v17 -> materialized v18 intake.

No dependencies beyond Python's standard library. This is a structural and
byte-integrity check, not validation of historical reading or corpus claims.

Exactly one scope has to be chosen; there is no default and no silent fallback:

    verify_counts.py --export-only
    verify_counts.py --input-v18 /pfad/entaENGELment_Korpusindex.md

Both successful scopes exit 0 but report different machine-readable statuses,
``PASS_EXPORT_ONLY`` and ``PASS_WITH_V18_INPUT``. Neither status asserts
scientific validity, complete reading of the originals, a green repository CI
run or merge approval.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

CLAIM_TAGS = ("FAKT", "MODELL", "HYPOTHESE", "METAPHER", "ANALOGIE", "UNRESOLVED")
INDEX_REL = "docs/intake/INDEX.md"
INTAKE_STATUS = "raw"
EXPORT_CHECKS = (
    "committed v10 baseline bytes",
    "reconstructed v17 and v18 state digests",
    "counter and claim-tag totals in payload, README and EXPORT",
    "CSV matrix regeneration",
    "manifest cardinality and per-file byte hashes",
    "linked intake row and both of its link targets",
)
V18_CHECKS = (
    "exact byte hash of the supplied materialized v18 index",
    "direct comparison of the reconstructed export against that index",
)
EXPORT_ONLY_LIMITS = (
    "private v18 original bytes were not supplied, so no direct index comparison ran",
    "frozen v17 original bytes are not part of this bundle in either scope",
)
V18_LIMITS = ("frozen v17 original bytes are not part of this bundle in either scope",)
DISCLAIMER = (
    "Structural and byte-integrity result only. No claim of scientific validity, "
    "complete reading of the originals, green repository CI or merge approval."
)
REMOVED_KEYS = {
    "file_id",
    "input_file_id",
    "run_id",
    "recorded_before_run",
    "writeback",
    "cursor",
    "cursor_used",
    "next_cursor",
    "page_2_cursor_used",
}
STAGES = ("v10", "v17", "v18")
FIELDS = (
    "entries",
    "READ_COMPLETE",
    "PARTIAL",
    "pending_candidates",
    "identities",
    "points",
    "relations",
    "conflicts",
    "outside_claim_vocabulary",
)
CSV_FIELDS = (
    "document_id",
    "source_id",
    "title",
    "source_version",
    "version_reliability",
    "observed_modified_at",
    "observed_size_bytes",
    "read_state_v17",
    "read_state",
    "read_ranges",
    "next_read",
    "source_family",
    "intake_status",
    "delta_kind",
    "implementation_state",
    "validation_state",
    "indexed_point_count_v17",
    "indexed_point_count",
    "priority",
    "candidates",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)


def digest_bytes(content):
    return hashlib.sha256(content).hexdigest()


def digest_value(value):
    return digest_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    )


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key not in REMOVED_KEYS}
    if isinstance(value, list):
        return [clean(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"\bfile_[0-9a-f]{24,}\b", "[interne Datei-ID ausgelassen]", value)
    return value


def document_id(source_id):
    return "doc-" + digest_bytes(source_id.encode())[:12]


def export_entry(entry):
    result = clean(entry)
    result["document_id"] = document_id(result["source_id"])
    return result


def indexed(items):
    result = {}
    for item in items:
        key = item["source_id"]
        require(key not in result, f"Duplicate source_id: {key}")
        result[key] = item
    return result


def snapshot(index):
    entries = [export_entry(entry) for entry in index["entries"]]
    ids = indexed(entries)
    pending = {}
    for observation in index.get("discovery", []):
        for item in observation.get("pending_candidates", []):
            if item["source_id"] not in ids:
                pending[item["source_id"]] = export_entry(item)
    return {
        "entries": entries,
        "pending_candidates": sorted(pending.values(), key=lambda item: item["source_id"]),
        "relations": clean(index["relations"]),
        "conflicts": clean(index["conflicts"]),
    }


def apply_delta(before, delta):
    result = copy.deepcopy(before)
    by_id = indexed(result["entries"])
    seen = set()
    for update in delta["updated_entries"]:
        item = update["entry"]
        key = item["source_id"]
        require(key in by_id and key not in seen, f"Invalid update: {key}")
        require(digest_value(by_id[key]) == update["previous_sha256"], f"Stale update base: {key}")
        seen.add(key)
        by_id[key] = copy.deepcopy(item)
    for item in delta["new_entries"]:
        key = item["source_id"]
        require(key not in by_id, f"New entry already exists: {key}")
        by_id[key] = copy.deepcopy(item)
    result["entries"] = list(by_id.values())
    result["pending_candidates"] = copy.deepcopy(delta["pending_candidates"])
    result["relations"].extend(copy.deepcopy(delta["added_relations"]))
    result["conflicts"].extend(copy.deepcopy(delta["added_conflicts"]))
    return result


def metrics(state):
    entries = indexed(state["entries"])
    pending = indexed(state["pending_candidates"])
    require(not entries.keys() & pending.keys(), "Entry/pending overlap")
    for item in [*entries.values(), *pending.values()]:
        require(item["document_id"] == document_id(item["source_id"]), "document_id drift")
    states = Counter(item["read_state"] for item in entries.values())
    require(set(states) <= {"READ_COMPLETE", "PARTIAL", "RETRY"}, "Unknown read state")
    for item in entries.values():
        if item["read_state"] == "PARTIAL":
            require(item.get("next_read") is not None, "PARTIAL without continuation")
    tags = Counter(point["tag"] for entry in entries.values() for point in entry.get("points", []))
    return {
        "entries": len(entries),
        "READ_COMPLETE": states["READ_COMPLETE"],
        "PARTIAL": states["PARTIAL"],
        "pending_candidates": len(pending),
        "identities": len(entries) + len(pending),
        "points": sum(tags.values()),
        "relations": len(state["relations"]),
        "conflicts": len(state["conflicts"]),
        "outside_claim_vocabulary": sum(n for tag, n in tags.items() if tag not in CLAIM_TAGS),
        "tag_distribution": dict(sorted(tags.items())),
    }


def counts_table(all_metrics):
    lines = ["| Metric | v10 | v17 | v18 |", "|---|---:|---:|---:|"]
    lines += [
        "| " + key + " | " + " | ".join(str(all_metrics[s][key]) for s in STAGES) + " |"
        for key in FIELDS
    ]
    return "\n".join(lines)


def tags_table(all_metrics):
    tags = sorted(set().union(*(all_metrics[s]["tag_distribution"] for s in STAGES)))
    lines = ["| Tag | v10 | v17 | v18 |", "|---|---:|---:|---:|"]
    lines += [
        "| "
        + tag
        + " | "
        + " | ".join(str(all_metrics[s]["tag_distribution"].get(tag, 0)) for s in STAGES)
        + " |"
        for tag in tags
    ]
    return "\n".join(lines)


def cell(value):
    if isinstance(value, (dict, list)):
        result = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    elif value is None:
        result = "null"
    else:
        result = str(value)
    return "'" + result if result.startswith(("=", "+", "-", "@", "\t", "\r")) else result


def matrix_text(v17, v18, assignments):
    old = indexed(v17["entries"] + v17["pending_candidates"])
    new = indexed(v18["entries"] + v18["pending_candidates"])
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    for key in sorted(new):
        item, earlier = new[key], old[key]
        row = {field: item.get(field, "NOT_RECORDED") for field in CSV_FIELDS}
        row.update(
            {
                "source_version": item.get("source_version") or "UNKNOWN",
                "read_state_v17": earlier.get("read_state", "DISCOVERED"),
                "read_state": item.get("read_state", "DISCOVERED"),
                "indexed_point_count_v17": len(earlier.get("points", [])),
                "indexed_point_count": len(item.get("points", [])),
                "priority": assignments[key]["priority"],
                "candidates": assignments[key]["candidates"],
            }
        )
        writer.writerow({field: cell(value) for field, value in row.items()})
    return output.getvalue()


def table_cells(line):
    stripped = line.strip()
    if "|" not in stripped:
        return None
    # Outer pipes are optional; omitting one must not hide a duplicate row.
    stripped = stripped.removeprefix("|").removesuffix("|")
    return [cell.strip() for cell in stripped.split("|")]


def markdown_link(text):
    match = re.fullmatch(r"\[([^\]\n]+)\]\(([^()\s]+)\)", text)
    return (match.group(1), match.group(2)) if match else None


def intake_rows(text, identifier):
    """Return data rows without silently dropping a malformed target row."""
    rows = [cells for cells in map(table_cells, text.splitlines()) if cells]
    headers = [cells for cells in rows if cells and cells[0] == "ID"]
    require(len(headers) == 1, f"Expected exactly one intake table header, found {len(headers)}")
    width = len(headers[0])
    ruler = re.compile(r"^:?-{2,}:?$")
    for cells in rows:
        if identifier in cells[0]:
            require(
                len(cells) == width,
                f"Intake row for {identifier} has {len(cells)} cells; expected {width}",
            )
    return [
        cells
        for cells in rows
        if len(cells) == width and cells[0] != "ID" and not all(ruler.match(c) for c in cells)
    ]


def check_intake_row(root, bundle, payload):
    """Match the intake row by its first table cell, never by raw substring count.

    The identifier also occurs inside the record link target, so counting
    occurrences in the file would report a linked row twice.
    """
    index_path = root / INDEX_REL
    index_dir = index_path.parent
    identifier = payload["intake"]["id"]
    matching = [
        cells
        for cells in intake_rows(index_path.read_text(encoding="utf-8"), identifier)
        if identifier in cells[0]
    ]
    require(
        len(matching) == 1,
        f"Expected exactly one intake row for {identifier}, found {len(matching)}",
    )
    cells = matching[0]
    record = Path(payload["intake"]["record"])
    expected = {
        "record": record.relative_to(index_dir.relative_to(root)).as_posix(),
        "overview": (bundle / "README.md").relative_to(index_dir).as_posix(),
    }
    identifier_link = markdown_link(cells[0])
    require(identifier_link is not None, f"Intake identifier cell is not a link: {cells[0]}")
    require(
        identifier_link[0] == identifier and identifier_link[1] == expected["record"],
        f"Intake identifier must link to {expected['record']}",
    )
    targets = {link[1] for link in map(markdown_link, cells) if link}
    require(
        expected["overview"] in targets,
        f"Intake row does not link to {expected['overview']}",
    )
    require(cells[4] == INTAKE_STATUS, f"Intake status must stay {INTAKE_STATUS}: {cells[4]}")
    for role, target in expected.items():
        resolved = (index_dir / target).resolve()
        require(
            resolved.is_relative_to(root.resolve()),
            f"Intake {role} link target escapes the repository: {target}",
        )
        require(resolved.is_file(), f"Intake {role} link target missing: {target}")


def safe_path(root, relative):
    path = root / relative
    require(
        not Path(relative).is_absolute() and ".." not in Path(relative).parts,
        f"Unsafe manifest path: {relative}",
    )
    require(path.resolve().is_relative_to(root.resolve()), "Manifest path escapes root")
    return path


def verify(bundle, root, input_v18=None):
    payload = load_json(bundle / "corpus-delta.json")
    require(payload["claim_vocabulary"] == list(CLAIM_TAGS), "Claim vocabulary drift")
    require(clean(payload) == payload, "Internal export keys leaked")
    base_path = safe_path(root, payload["baseline"]["path"])
    require(
        digest_bytes(base_path.read_bytes()) == payload["baseline"]["sha256"],
        "Baseline hash mismatch",
    )
    base = load_json(base_path)
    state10 = {
        key: base[key] for key in ("entries", "pending_candidates", "relations", "conflicts")
    }
    state17 = apply_delta(state10, payload["delta_v10_v17"])
    state18 = apply_delta(state17, payload["followup_v17_v18"])
    states = dict(zip(STAGES, (state10, state17, state18)))
    calculated = {stage: metrics(state) for stage, state in states.items()}
    require(calculated == payload["metrics"], "Payload counters or tag totals disagree")
    for stage in ("v17", "v18"):
        require(
            digest_value(states[stage]) == payload["state_sha256"][stage],
            f"Reconstructed {stage} differs",
        )
    require(len(payload["delta_v10_v17"]["new_entries"]) == 25, "Expected 25 v17 additions")
    require(len(payload["delta_v10_v17"]["added_relations"]) == 28, "Expected 28 relations")
    require(len(payload["delta_v10_v17"]["added_conflicts"]) == 9, "Expected 9 conflicts")
    require(len(payload["followup_v17_v18"]["new_entries"]) == 2, "Expected 2 partial readings")
    current_ids = set(indexed(state18["entries"] + state18["pending_candidates"]))
    require(set(payload["assignments"]) == current_ids, "Assignment coverage drift")
    for filename in ("README.md", "EXPORT.md"):
        text = (bundle / filename).read_text(encoding="utf-8")
        for label, expected in (
            ("COUNTS", counts_table(calculated)),
            ("TAGS", tags_table(calculated)),
        ):
            match = re.findall(rf"<!-- {label}:START -->\n(.*?)\n<!-- {label}:END -->", text, re.S)
            require(match == [expected], f"{filename}: {label} table mismatch")
        for stage in ("frozen_v17", "materialized_v18"):
            anchor = payload["provenance"][stage]
            require(anchor["sha256"] in text, f"{filename}: missing {stage} hash")
    require(
        (bundle / "corpus-matrix.csv").read_text(encoding="utf-8")
        == matrix_text(state17, state18, payload["assignments"]),
        "CSV matrix differs",
    )
    manifest = load_json(bundle / "MANIFEST.json")
    expected_paths = set(payload["manifest_files"])
    require(len(manifest["files"]) == len(expected_paths), "Manifest cardinality mismatch")
    require(
        {item["path"] for item in manifest["files"]} == expected_paths,
        "Manifest missing or extra paths",
    )
    for item in manifest["files"]:
        raw = safe_path(root, item["path"]).read_bytes()
        require(
            len(raw) == item["bytes"] and digest_bytes(raw) == item["sha256"],
            f"Manifest integrity failure: {item['path']}",
        )
    check_intake_row(root, bundle, payload)
    require((root / payload["intake"]["record"]).is_file(), "Missing intake record")
    if input_v18 is not None:
        require(
            input_v18.is_file(),
            f"Supplied v18 input is missing or not a file: {input_v18}",
        )
        raw = input_v18.read_bytes()
        require(
            digest_bytes(raw) == payload["provenance"]["materialized_v18"]["sha256"],
            "Materialized v18 byte hash mismatch",
        )
        blocks = re.findall(r"```json\s*\n(.*?)\n```", raw.decode(), re.S)
        require(len(blocks) == 1, "Expected exactly one index JSON block")
        direct = snapshot(json.loads(blocks[0], object_pairs_hook=no_duplicate_keys))
        require(direct == state18, "Export differs from the direct v18 index")
    return calculated


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bundle", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument(
        "--root", type=Path, help="Repository root; defaults to bundle's fifth parent"
    )
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument(
        "--export-only",
        action="store_true",
        help="Check the public export package and its committed baseline only",
    )
    scope.add_argument(
        "--input-v18",
        type=Path,
        metavar="PATH",
        help="Run the export checks and then compare against the private v18 index at PATH",
    )
    args = parser.parse_args()
    root = args.root or args.bundle.resolve().parents[4]
    try:
        result = verify(args.bundle.resolve(), root.resolve(), args.input_v18)
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    with_input = args.input_v18 is not None
    print(
        json.dumps(
            {
                "status": "PASS_WITH_V18_INPUT" if with_input else "PASS_EXPORT_ONLY",
                "input_v18_checked": with_input,
                "checked": list(EXPORT_CHECKS + (V18_CHECKS if with_input else ())),
                "not_checked": list(V18_LIMITS if with_input else EXPORT_ONLY_LIMITS),
                "disclaimer": DISCLAIMER,
                "metrics": result,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
