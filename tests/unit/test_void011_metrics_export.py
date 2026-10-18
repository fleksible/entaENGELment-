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
