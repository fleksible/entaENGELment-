"""
CPT Test Harness (unit/integration style).
This is a minimal harness demonstrating C/P/T transforms and distance checks.
Dependencies: numpy, scipy (for cosine), scikit-learn (optional tf-idf)
"""

import numpy as np
import json
import os
from typing import List
from scipy.spatial.distance import cosine

# simple text->vector using bag-of-words (very small dependency-free impl)
def text_vector(tokens: List[str]) -> np.ndarray:
    # token list -> normalized counts
    if not tokens:
        return np.zeros(1)
    uniq = sorted(set(tokens))
    vec = np.array([tokens.count(u) for u in uniq], dtype=float)
    if vec.sum() > 0:
        vec = vec / vec.sum()
    return vec

def tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split() if t.strip()]

def c_transform_affect(features: dict) -> dict:
    # invert sentiment-like numeric fields if present (heuristic)
    out = dict(features)
    if 'sentiment' in out:
        out['sentiment'] = -out['sentiment']
    return out

def p_transform_parity(seq_features: List[float]) -> List[float]:
    # mirror sequence
    return list(reversed(seq_features))

def t_transform_time(seq_features: List[float]) -> List[float]:
    # time reversal = same as parity for sequences here
    return list(reversed(seq_features))

def vector_from_features(features: dict) -> np.ndarray:
    # derive a small numeric fingerprint vector
    keys = sorted(features.keys())
    vals = []
    for k in keys:
        v = features[k]
        if isinstance(v, (int, float)):
            vals.append(float(v))
        else:
            vals.append(len(str(v)))
    arr = np.array(vals, dtype=float)
    if arr.size == 0:
        return np.zeros(1)
    return arr / (np.linalg.norm(arr) + 1e-12)

def run_cpt_harness(sessions: List[dict], out_path: str = "reports/cpt_test_report.json"):
    """
    sessions: list of dict with minimal fields:
      - id: str
      - text: str
      - features: dict (numeric features e.g. sentiment, hrv)
      - seq: list of floats (prosody or time-series)
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    report = {"n_sessions": len(sessions), "results": []}
    for s in sessions:
        base_vec = vector_from_features(s.get("features", {}))
        # C transform
        c_feats = c_transform_affect(s.get("features", {}))
        c_vec = vector_from_features(c_feats)
        # P transform (mirror seq)
        seq = s.get("seq", [])
        p_seq = p_transform_parity(seq)
        t_seq = t_transform_time(seq)

        # distances
        d_c = float(cosine(base_vec, c_vec)) if base_vec.size == c_vec.size else None
        # for sequences, use L2 normalized distance
        def seq_dist(a,b):
            a = np.array(a); b = np.array(b)
            if a.size == 0 and b.size == 0:
                return 0.0
            if a.size != b.size:
                # pad shorter with zeros
                n = max(a.size,b.size)
                a2 = np.zeros(n); b2 = np.zeros(n)
                a2[:a.size] = a; b2[:b.size] = b
                a = a2; b = b2
            return float(np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b) + 1e-12))

        d_p = seq_dist(seq, p_seq)
        d_t = seq_dist(seq, t_seq)

        report["results"].append({
            "id": s.get("id"),
            "d_c": d_c,
            "d_p": d_p,
            "d_t": d_t
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report

# quick smoke run (used by pytest)
def test_cpt_harness_smoke(tmp_path):
    sessions = [
        {"id":"s1","text":"hello world", "features":{"sentiment":0.5,"hrv":42}, "seq":[0.1,0.2,0.3]},
        {"id":"s2","text":"goodbye now", "features":{"sentiment":-0.2,"hrv":30}, "seq":[0.4,0.1]}
    ]
    out = run_cpt_harness(sessions, out_path=str(tmp_path/"cpt_report.json"))
    assert out["n_sessions"] == 2
    for r in out["results"]:
        assert "d_c" in r and "d_p" in r and "d_t" in r
