"""
scripts/triad_compare.py

Simple triad compare tool:
- Reads three triad templates (markdown) or free text files
- Tokenizes, computes TF-like normalized counts and cosine similarities
- Produces a small JSON with pairwise similarities and top common tokens

Usage:
  python scripts/triad_compare.py claude.md gpt.md fleks.md out.json
"""

import json
import math
import re
import sys
from collections import Counter


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    # simple tokenization: words, lowercased, remove short tokens
    toks = re.findall(r"[A-Za-z0-9_]+", text.lower())
    return [t for t in toks if len(t) > 2]


def tf_vector(tokens):
    c = Counter(tokens)
    total = sum(c.values())
    if total == 0:
        return {}, set()
    vec = {k: v / total for k, v in c.items()}
    return vec, set(c.keys())


def dot_product(a, b):
    s = 0.0
    for k, v in a.items():
        if k in b:
            s += v * b[k]
    return s


def cosine_sim(a, b):
    if not a or not b:
        return 0.0
    num = dot_product(a, b)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return num / (na * nb)


def top_common_tokens(a_set, b_set, top_n=10):
    return sorted(a_set & b_set)[:top_n]


def main(a_path, b_path, c_path, out_path="reports/triad_similarity.json"):
    a_text = read_text(a_path)
    b_text = read_text(b_path)
    c_text = read_text(c_path)

    a_toks = tokenize(a_text)
    b_toks = tokenize(b_text)
    c_toks = tokenize(c_text)

    a_vec, a_set = tf_vector(a_toks)
    b_vec, b_set = tf_vector(b_toks)
    c_vec, c_set = tf_vector(c_toks)

    ab = cosine_sim(a_vec, b_vec)
    ac = cosine_sim(a_vec, c_vec)
    bc = cosine_sim(b_vec, c_vec)

    center = ab + ac + bc

    payload = {
        "pairwise": {"A_B": ab, "A_C": ac, "B_C": bc},
        "center_sum": center,
        "common": {
            "A_B_common": top_common_tokens(a_set, b_set),
            "A_C_common": top_common_tokens(a_set, c_set),
            "B_C_common": top_common_tokens(b_set, c_set),
            "A_B_C_common": sorted(a_set & b_set & c_set)[:20],
        },
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Triad similarity written to {out_path}")
    return payload


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python scripts/triad_compare.py claude.md gpt.md fleks.md [out.json]")
        sys.exit(1)
    a, b, c = sys.argv[1:4]
    out = sys.argv[4] if len(sys.argv) > 4 else "reports/triad_similarity.json"
    main(a, b, c, out)
