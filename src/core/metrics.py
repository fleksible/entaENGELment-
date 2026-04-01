"""Core-5 Metriken für entaENGELment Framework.

Dieses Modul implementiert die fünf Kern-Metriken des entaENGELment-Frameworks:
- ECI (Ethical Consent Index)
- PLV (Phase Locking Value)
- MI (Mutual Information)
- FD (Fractal Dimension)
- PF (Power Flux)

Version: 1.0 (Minimal-Stubs für Testbarkeit; vollständige Implementierung folgt in v1.1)
"""

import math
from typing import Union


def eci(signal: list[Union[int, float]]) -> float:
    """Ethical Consent Index - Misst aktiven, bewussten Consent.

    Args:
        signal: Liste von Signal-Werten zur Analyse

    Returns:
        float: ECI-Wert zwischen 0.0 und 1.0
    """
    if not signal:
        return 0.0
    return float(min(max(sum(signal) / len(signal), 0.0), 1.0))


def plv(phases: list[Union[int, float]]) -> float:
    """Phase Locking Value (PLV) – Standarddefinition.

    Erwartet Phasen (idealerweise Phasendifferenzen) in RADIANS.
    Robust gegen Drift, weil die Auswertung auf dem Einheitskreis passiert.

    Args:
        phases: Liste von Phasen-Werten (Radians)

    Returns:
        float: PLV-Wert zwischen 0.0 und 1.0
    """
    if not phases:
        return 0.0

    sum_cos = 0.0
    sum_sin = 0.0
    two_pi = 2.0 * math.pi

    for p in phases:
        x = float(p)
        # normalize to [-pi, pi] for numerical stability
        x = ((x + math.pi) % two_pi) - math.pi
        sum_cos += math.cos(x)
        sum_sin += math.sin(x)

    n = float(len(phases))
    mean_cos = sum_cos / n
    mean_sin = sum_sin / n

    r = math.sqrt(mean_cos * mean_cos + mean_sin * mean_sin)
    return float(min(max(r, 0.0), 1.0))


def mi(x: list[Union[int, float]], y: list[Union[int, float]]) -> float:
    """Mutual Information - Misst geteilte Information zwischen zwei Signalen.

    Verwendet histogram-basierte Schätzung mit sqrt(n) Bins.

    Args:
        x: Erste Datenreihe
        y: Zweite Datenreihe (wird auf len(x) gekürzt)

    Returns:
        float: MI-Wert >= 0.0 (0.0 = keine gemeinsame Information)
    """
    n = min(len(x), len(y))
    if n < 2:
        return 0.0

    xs = list(x[:n])
    ys = list(y[:n])

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if x_min == x_max or y_min == y_max:
        return 0.0

    bins = max(2, int(math.sqrt(n)))

    def _bin(val: float, vmin: float, vmax: float) -> int:
        idx = int((val - vmin) / (vmax - vmin) * bins)
        return min(idx, bins - 1)

    joint: dict[tuple[int, int], int] = {}
    x_counts: dict[int, int] = {}
    y_counts: dict[int, int] = {}

    for xi, yi in zip(xs, ys):
        bx = _bin(float(xi), x_min, x_max)
        by = _bin(float(yi), y_min, y_max)
        joint[(bx, by)] = joint.get((bx, by), 0) + 1
        x_counts[bx] = x_counts.get(bx, 0) + 1
        y_counts[by] = y_counts.get(by, 0) + 1

    result = 0.0
    for (bx, by), cnt in joint.items():
        pxy = cnt / n
        px = x_counts[bx] / n
        py = y_counts[by] / n
        if pxy > 0 and px > 0 and py > 0:
            result += pxy * math.log(pxy / (px * py))

    return float(max(0.0, result))


def fd(series: list[Union[int, float]]) -> float:
    """Fractal Dimension - Misst Selbstähnlichkeit/Organisation (Higuchi-Methode).

    Schätzt die fraktale Dimension einer Zeitreihe via Higuchi-Algorithmus.
    Ergebnis liegt typischerweise in [1.0, 2.0] (1.0 = glatt, 2.0 = komplex).

    Args:
        series: Datenreihe zur Analyse (mindestens 4 Punkte empfohlen)

    Returns:
        float: FD-Wert (clamped auf [1.0, 2.0])
    """
    n = len(series)
    if n < 4:
        return 1.0

    k_max = min(4, n // 2)
    log_k: list[float] = []
    log_l: list[float] = []

    for k in range(1, k_max + 1):
        lengths: list[float] = []
        for m in range(1, k + 1):
            idxs = list(range(m - 1, n, k))
            if len(idxs) < 2:
                continue
            total = sum(abs(series[idxs[i]] - series[idxs[i - 1]]) for i in range(1, len(idxs)))
            length = total * (n - 1) / (k * (len(idxs) - 1))
            lengths.append(length)
        if not lengths:
            continue
        avg = sum(lengths) / len(lengths)
        if avg > 0:
            log_k.append(math.log(1.0 / k))
            log_l.append(math.log(avg))

    if len(log_k) < 2:
        return 1.5

    # Linear regression slope = Higuchi FD estimate
    n_pts = len(log_k)
    sx = sum(log_k)
    sy = sum(log_l)
    sxx = sum(v * v for v in log_k)
    sxy = sum(log_k[i] * log_l[i] for i in range(n_pts))
    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-10:
        return 1.5
    slope = (n_pts * sxy - sx * sy) / denom

    return float(min(max(slope, 1.0), 2.0))


def pf(series: list[Union[int, float]]) -> float:
    """Power Flux - Misst Energiefluss/Aktivität.

    Args:
        series: Datenreihe zur Analyse

    Returns:
        float: PF-Wert basierend auf Absolutwerten
    """
    if not series:
        return 0.0
    return float(sum(abs(v) for v in series) / len(series))
