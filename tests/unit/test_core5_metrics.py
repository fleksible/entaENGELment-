"""Unit-Tests für Core-5 Metriken.

Testet die grundlegende Funktionalität der fünf Kern-Metriken:
ECI, PLV, MI, FD, PF
"""

from src.core.metrics import eci, plv, mi, fd, pf


def test_eci_valid_range():
    """Test: ECI gibt Werte im gültigen Bereich [0, 1] zurück."""
    result = eci([0.4, 0.6])
    assert 0.0 <= result <= 1.0


def test_eci_empty_signal():
    """Test: ECI mit leerem Signal gibt 0.0 zurück."""
    result = eci([])
    assert result == 0.0


def test_plv_valid_range():
    """Test: PLV gibt Werte im gültigen Bereich [0, 1] zurück."""
    result = plv([0.0, 0.1, 0.2])
    assert 0.0 <= result <= 1.0


def test_plv_empty_phases():
    """Test: PLV mit leerer Phasenliste gibt 0.0 zurück."""
    result = plv([])
    assert result == 0.0


def test_mi_returns_float():
    """Test: MI gibt float zurück."""
    result = mi([1], [2])
    assert isinstance(result, float)


def test_fd_returns_float():
    """Test: FD gibt float zurück."""
    result = fd([1, 2, 3])
    assert isinstance(result, float)


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
