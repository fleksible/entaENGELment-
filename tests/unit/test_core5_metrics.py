"""Unit-Tests für Core-5 Metriken.

Testet die grundlegende Funktionalität der fünf Kern-Metriken:
ECI, PLV, MI, FD, PF — sowohl auf Wertebereich/Typ als auch (wo analytisch
bekannt) auf numerische Korrektheit gegen Referenzfälle.
"""

import math

from src.core.metrics import eci, fd, mi, pf, plv


def test_metrics_exist_and_return_numbers():
    assert 0.0 <= eci([0.4, 0.6]) <= 1.0
    assert 0.0 <= plv([0.0, 0.1, 0.2]) <= 1.0
    assert isinstance(mi([1], [2]), float)
    assert isinstance(fd([1, 2, 3]), float)
    assert isinstance(pf([1, -1, 1]), float)


def test_eci_valid_range():
    """Test: ECI gibt Werte im gültigen Bereich [0, 1] zurück."""
    result = eci([0.4, 0.6])
    assert 0.0 <= result <= 1.0


def test_eci_empty_signal():
    """Test: ECI mit leerem Signal gibt 0.0 zurück."""
    result = eci([])
    assert result == 0.0


def test_eci_is_clamped_mean():
    """[FACT] ECI-Proxy == geklemmter Mittelwert des Signals."""
    assert eci([0.4, 0.6]) == 0.5
    assert eci([2.0, 2.0]) == 1.0  # oberhalb 1 → geklemmt
    assert eci([-1.0, -1.0]) == 0.0  # unterhalb 0 → geklemmt


def test_plv_valid_range():
    """Test: PLV gibt Werte im gültigen Bereich [0, 1] zurück."""
    result = plv([0.0, 0.1, 0.2])
    assert 0.0 <= result <= 1.0


def test_plv_empty_phases():
    """Test: PLV mit leerer Phasenliste gibt 0.0 zurück."""
    result = plv([])
    assert result == 0.0


def test_plv_identical_phases_is_one():
    """[FACT] Identische Phasen → perfektes Phase-Locking (PLV == 1)."""
    assert plv([0.5, 0.5, 0.5, 0.5, 0.5]) == 1.0


def test_plv_antiphase_is_near_zero():
    """[FACT] Gegenphasige Phasen (0, π, 0, π) → PLV ≈ 0."""
    assert plv([0.0, math.pi, 0.0, math.pi]) < 1e-9


def test_plv_uniform_spread_is_near_zero():
    """[FACT] Gleichverteilte Phasen auf dem Einheitskreis → PLV ≈ 0."""
    assert plv([0.0, math.pi / 2, math.pi, 3 * math.pi / 2]) < 1e-9


def test_mi_returns_float():
    """Test: MI gibt float zurück."""
    result = mi([1], [2])
    assert isinstance(result, float)


def test_mi_identical_series_is_positive():
    """[FACT] MI zweier identischer Reihen ist strikt positiv (geteilte Info)."""
    series = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert mi(series, series) > 0.0


def test_mi_constant_partner_is_zero():
    """[FACT] MI ist 0, wenn eine Reihe konstant ist (kein gemeinsamer Info-Gehalt)."""
    series = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert mi(series, [5] * 9) == 0.0


def test_fd_returns_float():
    """Test: FD gibt float zurück."""
    result = fd([1, 2, 3])
    assert isinstance(result, float)


def test_fd_linear_series_is_near_one():
    """[FACT] Higuchi-FD einer Geraden ≈ 1.0 (maximal glatt)."""
    result = fd(list(range(1, 17)))
    assert 1.0 <= result <= 1.2


def test_fd_is_clamped_to_valid_interval():
    """[FACT] FD-Ergebnis liegt stets im Intervall [1.0, 2.0]."""
    for series in ([1, 2, 3, 4, 5, 6, 7, 8], [3, 1, 4, 1, 5, 9, 2, 6]):
        assert 1.0 <= fd(series) <= 2.0


def test_pf_returns_float():
    """Test: PF gibt float zurück."""
    result = pf([1, -1, 1])
    assert isinstance(result, float)


def test_pf_empty_series():
    """Test: PF mit leerer Serie gibt 0.0 zurück."""
    result = pf([])
    assert result == 0.0


def test_pf_calculation():
    """Test: PF berechnet korrekt den Durchschnitt der Absolutwerte."""
    result = pf([1, -2, 3])
    expected = (1 + 2 + 3) / 3
    assert abs(result - expected) < 1e-9
