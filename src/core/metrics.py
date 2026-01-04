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
    """Mutual Information - Misst Informationsdichte/Komplexität.

    Args:
        x: Erste Datenreihe
        y: Zweite Datenreihe

    Returns:
        float: MI-Wert (Dummy-Implementierung)
    """
    # TODO: Vollständige Implementierung in v1.1
    return 0.5


def fd(series: list[Union[int, float]]) -> float:
    """Fractal Dimension - Misst Selbstähnlichkeit/Organisation.

    Args:
        series: Datenreihe zur Analyse

    Returns:
        float: FD-Wert (Dummy-Implementierung)
    """
    # TODO: Vollständige Implementierung in v1.1
    return 1.5


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
