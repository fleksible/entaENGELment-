"""VOID-011: der committete SIMULATION_PROXY-Metrik-Export ist reproduzierbar."""

import csv
import hashlib
import io
import json
from pathlib import Path

import yaml

from tools import void011_metrics_export as export

ROOT = Path(__file__).resolve().parents[2]


def test_committed_export_matches_regeneration():
    csv_text, meta_text = export.render()
    assert (ROOT / export.CSV_PATH).read_text(encoding="utf-8") == csv_text
    assert (ROOT / export.META_PATH).read_text(encoding="utf-8") == meta_text


def test_render_is_deterministic():
    assert export.render() == export.render()


def test_every_row_is_tagged_simulation_proxy():
    rows = list(csv.DictReader(io.StringIO(export.render()[0])))
    assert len(rows) == len(export.SEEDS) * len(export.COUPLINGS) * len(export.UNITS)
    assert {r["claim_tag"] for r in rows} == {"SIMULATION_PROXY"}
    assert {r["metric_name"] for r in rows} == set(export.UNITS)


def test_claim_tag_is_defined_in_policy():
    policy = yaml.safe_load((ROOT / "policies" / "claim_tags_v0_2.yaml").read_text())
    assert export.CLAIM_TAG in policy["tags"]


def test_meta_hash_and_plausibility_check():
    csv_text, meta_text = export.render()
    meta = json.loads(meta_text)
    assert meta["csv_sha256"] == hashlib.sha256(csv_text.encode("utf-8")).hexdigest()
    assert meta["claim_tag"] == "SIMULATION_PROXY"
    assert meta["checks"]["plv_monotone_in_coupling"] is True
    assert meta["checks"]["mi_excess_monotone_in_coupling"] is True


def test_mi_excess_is_mi_minus_shuffle_baseline():
    """MI_EXCESS zieht den Schätzer-Bias ab; bei Unabhängigkeit liegt die Baseline > 0."""
    values = {
        (r["run_id"], r["metric_name"]): float(r["metric_value"])
        for r in csv.DictReader(io.StringIO(export.render()[0]))
    }
    for run_id in {run for run, _ in values}:
        mi, base, excess = (values[(run_id, m)] for m in ("MI", "MI_BASELINE", "MI_EXCESS"))
        assert base > 0.1, run_id
        assert abs(mi - base - excess) < 1e-9, run_id


def test_meta_binds_generating_sources():
    meta = json.loads(export.render()[1])
    assert set(meta["source_sha256"]) == set(export.SOURCES)
    for path, digest in meta["source_sha256"].items():
        content = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        assert digest == hashlib.sha256(content).hexdigest(), path
