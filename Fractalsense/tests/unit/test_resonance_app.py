"""
Tests für die Sensordaten-Weitergabe der ResonanceEnhancer-Testanwendung.

Deckt ab:
- TestApp.on_send_sensor_data emittiert 'sensor_data_updated'
- Payload-Keys passen zu integration._on_sensor_data_updated_for_resonance
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modular_app_structure import EventSystem

# test_resonance ist ein GUI-Skript und importiert tkinter/matplotlib/pygame auf
# Modulebene. Der hier getestete Handler berührt nichts davon — fehlt eine dieser
# Abhängigkeiten (headless CI), wird nur ihre Import-Oberfläche gestubbt, damit die
# Logik trotzdem geprüft wird.
_GUI_STUBS = {
    "tkinter": ("tkinter", "tkinter.ttk"),
    "matplotlib": (
        "matplotlib",
        "matplotlib.pyplot",
        "matplotlib.figure",
        "matplotlib.backends",
        "matplotlib.backends.backend_tkagg",
    ),
    "pygame": ("pygame",),
}


@pytest.fixture
def test_resonance(monkeypatch):
    """Importiert test_resonance, ggf. mit gestubbten GUI-Abhängigkeiten."""
    stubbed = False
    for package, module_names in _GUI_STUBS.items():
        if importlib.util.find_spec(package) is not None:
            continue
        for name in module_names:
            monkeypatch.setitem(sys.modules, name, MagicMock())
        stubbed = True

    if stubbed:
        # Frischer Import, damit die Stubs greifen (und danach zurückgerollt werden).
        monkeypatch.delitem(sys.modules, "test_resonance", raising=False)

    return importlib.import_module("test_resonance")


class _FakeVar:
    """Minimaler Ersatz für tk.DoubleVar."""

    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


class _FakeLabel:
    """Minimaler Ersatz für ttk.Label — merkt sich den zuletzt gesetzten Text."""

    def __init__(self):
        self.text = None

    def config(self, text=None, **kwargs):
        self.text = text


class _StubApp:
    """Trägt nur die Attribute, die on_send_sensor_data tatsächlich liest."""

    def __init__(self, event_system, **values):
        self.event_system = event_system
        self.status_label = _FakeLabel()
        for name, value in values.items():
            setattr(self, f"{name}_var", _FakeVar(value))


@pytest.fixture
def sensor_app():
    """Stub-App mit bekannten Sensorwerten und echtem EventSystem."""
    return _StubApp(
        EventSystem(),
        accel_x=1.0,
        accel_y=2.0,
        accel_z=2.0,
        gyro_x=0.0,
        gyro_y=3.0,
        gyro_z=4.0,
    )


class TestSendSensorData:
    """Tests für TestApp.on_send_sensor_data."""

    def test_emits_sensor_data_updated(self, sensor_app, test_resonance):
        """Should emit 'sensor_data_updated' with the current slider values."""
        received = []
        sensor_app.event_system.register_handler(
            "sensor_data_updated", lambda event_type, data: received.append(data)
        )

        test_resonance.TestApp.on_send_sensor_data(sensor_app)

        assert len(received) == 1
        assert received[0] == {
            "accel_x": 1.0,
            "accel_y": 2.0,
            "accel_z": 2.0,
            "gyro_x": 0.0,
            "gyro_y": 3.0,
            "gyro_z": 4.0,
        }

    def test_payload_matches_integration_contract(self, sensor_app, test_resonance):
        """Should use exactly the keys integration.py reads for the resonance mapping."""
        received = []
        sensor_app.event_system.register_handler(
            "sensor_data_updated", lambda event_type, data: received.append(data)
        )

        test_resonance.TestApp.on_send_sensor_data(sensor_app)

        import integration

        # Keys, die integration erwartet, sind alle im Payload vorhanden
        for key in ("accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"):
            assert key in received[0]

        # Der Consumer verarbeitet das Payload ohne Fehler
        integration._on_sensor_data_updated_for_resonance("sensor_data_updated", received[0])

    def test_updates_status_label(self, sensor_app, test_resonance):
        """Should report the accel/gyro magnitudes in the status bar."""
        test_resonance.TestApp.on_send_sensor_data(sensor_app)

        # |a| = sqrt(1+4+4) = 3.0, |w| = sqrt(0+9+16) = 5.0
        assert "3.00" in sensor_app.status_label.text
        assert "5.00" in sensor_app.status_label.text
