#!/usr/bin/env python3
"""VOID-011: deterministischer Metrik-Export auf Toy-Daten (SIMULATION_PROXY).

Erzeugt ``data/metrics/void011_resonance_metrics.csv`` plus ``.meta.json``.
Die Werte stammen aus synthetischen Signalen
(``src/tools/toy_resonance_dataset.py``) und den Core-Metriken
(``src/core/metrics.py``). Sie sind KEINE Messwerte: jede Zeile trägt den
Claim-Tag ``SIMULATION_PROXY`` (policies/claim_tags_v0_2.yaml).

Deterministisch: feste Seeds, kein Zeitstempel, Werte auf feste Nachkommastellen
gerundet. ``--check`` vergleicht den Commit-Stand mit einer Neuberechnung
(exit 1 bei Drift).

Usage:
    python tools/void011_metrics_export.py          # schreiben
    python tools/void011_metrics_export.py --check  # nur prüfen
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import random
from pathlib import Path

try:
    from src.core.metrics import mi
    from src.tools.toy_resonance_dataset import compute_demo_metrics, generate_mycel_signals
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.core.metrics import mi
    from src.tools.toy_resonance_dataset import compute_demo_metrics, generate_mycel_signals

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = Path("data/metrics/void011_resonance_metrics.csv")
META_PATH = Path("data/metrics/void011_resonance_metrics.meta.json")

CLAIM_TAG = "SIMULATION_PROXY"
SEEDS = (7, 42)
COUPLINGS = (0.1, 0.35, 0.8)
N_SAMPLES = 256
DECIMALS = 10
UNITS = {
    "ECI": "ratio",
    "PLV": "ratio",
    "MI": "nats",
    "FD": "dimensionless",
    "PF": "signal_units",
    "MI_BASELINE": "nats",
    "MI_EXCESS": "nats",
}
# Der Histogramm-Schätzer mi() hat einen Positiv-Bias (hier ~0,5 nats bei
# unabhängigen Signalen; das √n-Binning lässt ihn mit n nicht verschwinden).
# MI_BASELINE = Mittel von mi()
# über zufällig gemischte b-Reihen; MI_EXCESS = MI - MI_BASELINE ist die
# ehrlichere Kennzahl für geteilte Information.
SHUFFLES = 8
COLUMNS = (
    "run_id",
    "seed",
    "coupling",
    "n",
    "metric_name",
    "metric_value",
    "unit",
    "claim_tag",
    "generator",
)
CLAIM_BOUNDARY = (
    "Synthetische Toy-Signale (Kuramoto-artig gekoppelte Oszillatoren mit Rauschen). "
    "Kein Messwert und keine empirische Aussage über reale Systeme; die Werte "
    "informieren nur Modelle und Tests (SIMULATION_PROXY)."
)


def mi_shuffle_baseline(a: list[float], b: list[float], seed: int) -> float:
    """Mittlere MI gegen permutiertes b: Schätzer-Boden ohne echte Kopplung."""
    total = 0.0
    for k in range(SHUFFLES):
        shuffled = list(b)
        random.Random(seed * 1000 + k).shuffle(shuffled)
        total += mi(a, shuffled)
    return total / SHUFFLES


def build_rows() -> list[dict[str, str]]:
    """Berechnet alle Seed×Kopplung-Läufe als CSV-Zeilen (deterministisch)."""
    rows: list[dict[str, str]] = []
    for seed in SEEDS:
        for coupling in COUPLINGS:
            ds = generate_mycel_signals(n=N_SAMPLES, seed=seed, coupling=coupling)
            metrics = compute_demo_metrics(ds)
            metrics["MI_BASELINE"] = mi_shuffle_baseline(ds.a, ds.b, seed)
            metrics["MI_EXCESS"] = metrics["MI"] - metrics["MI_BASELINE"]
            for name in UNITS:
                rows.append(
                    {
                        "run_id": f"S{seed}-C{coupling}",
                        "seed": str(seed),
                        "coupling": str(coupling),
                        "n": str(N_SAMPLES),
                        "metric_name": name,
                        "metric_value": f"{round(metrics[name], DECIMALS):.{DECIMALS}f}",
                        "unit": UNITS[name],
                        "claim_tag": CLAIM_TAG,
                        "generator": "tools/void011_metrics_export.py",
                    }
                )
    return rows


def render_csv(rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def monotone_in_coupling(rows: list[dict[str, str]], metric: str) -> bool:
    """Metrik steigt je Seed mit der Kopplung (Plausibilitätsgrenze des Proxys)."""
    value = {
        (r["seed"], r["coupling"]): float(r["metric_value"])
        for r in rows
        if r["metric_name"] == metric
    }
    for seed in SEEDS:
        series = [value[(str(seed), str(coupling))] for coupling in COUPLINGS]
        if any(b <= a for a, b in zip(series, series[1:], strict=False)):
            return False
    return True


SOURCES = (
    "src/core/metrics.py",
    "src/tools/toy_resonance_dataset.py",
    "tools/void011_metrics_export.py",
)


def source_digests() -> dict[str, str]:
    """sha256 je erzeugender Quelle (Zeilenenden normalisiert, plattformstabil).

    Bindet den Export an die Implementierung: Jede Änderung an diesen Dateien
    verlangt einen neu erzeugten Export (Drift-Check schlägt sonst an).
    """
    return {
        path: hashlib.sha256((ROOT / path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for path in SOURCES
    }


def render_meta(csv_text: str, rows: list[dict[str, str]]) -> str:
    meta = {
        "artifact_path": CSV_PATH.as_posix(),
        "void_id": "VOID-011",
        "claim_tag": CLAIM_TAG,
        "claim_boundary": CLAIM_BOUNDARY,
        "generator": "tools/void011_metrics_export.py",
        "dataset": "src/tools/toy_resonance_dataset.py:generate_mycel_signals",
        "metrics_impl": "src/core/metrics.py",
        "seeds": list(SEEDS),
        "couplings": list(COUPLINGS),
        "n": N_SAMPLES,
        "precision_decimals": DECIMALS,
        "rows": len(rows),
        "checks": {
            "plv_monotone_in_coupling": monotone_in_coupling(rows, "PLV"),
            "mi_excess_monotone_in_coupling": monotone_in_coupling(rows, "MI_EXCESS"),
        },
        "mi_baseline": {
            "method": "Mittel von mi(a, b permutiert) über feste Permutationen",
            "shuffles": SHUFFLES,
            "reason": "Histogramm-MI hat Positiv-Bias (~0,5 nats bei Unabhängigkeit, n=256)",
        },
        "csv_sha256": hashlib.sha256(csv_text.encode("utf-8")).hexdigest(),
        "source_sha256": source_digests(),
        "provenance_note": (
            "Deterministisch aus festen Seeds erzeugt, ohne Zeitstempel. "
            "Reproduzieren: python tools/void011_metrics_export.py --check"
        ),
    }
    return json.dumps(meta, indent=2, ensure_ascii=False) + "\n"


def render() -> tuple[str, str]:
    rows = build_rows()
    csv_text = render_csv(rows)
    return csv_text, render_meta(csv_text, rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="nur auf Drift prüfen")
    args = parser.parse_args()

    csv_text, meta_text = render()
    csv_file, meta_file = ROOT / CSV_PATH, ROOT / META_PATH

    if args.check:
        drift = [
            str(path.relative_to(ROOT))
            for path, expected in ((csv_file, csv_text), (meta_file, meta_text))
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        if drift:
            print(
                f"[DRIFT] {', '.join(drift)}; neu erzeugen: python tools/void011_metrics_export.py"
            )
            return 1
        print(f"[CHECK] Up to date: {CSV_PATH} ({CLAIM_TAG})")
        return 0

    csv_file.parent.mkdir(parents=True, exist_ok=True)
    csv_file.write_text(csv_text, encoding="utf-8")
    meta_file.write_text(meta_text, encoding="utf-8")
    print(f"[WRITE] {CSV_PATH} + {META_PATH.name} ({CLAIM_TAG})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
