"""
Tests für die Event-Handler der ResonanceEnhancer-Testanwendung (TestApp).

Deckt ab:
- on_send_sensor_data / on_send_fractal_data emittieren ihre Events
- Payload-Keys passen zu den Consumern in integration.py
- on_colormap_updated / on_generate_fractal_sound / on_update_resonance_parameters
- on_fractal_changed (sendet bewusst nicht), on_close (Aufräumen)
- Hilfsmethoden _ensure_audio_ready (Audio-Fallback) und _render_colormap
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
    # backend_tkagg ist ein Tk-Backend — ohne tkinter nicht importierbar, auch wenn
    # matplotlib selbst vorhanden ist.
    "tkinter": ("tkinter", "tkinter.ttk", "matplotlib.backends.backend_tkagg"),
    "matplotlib": (
        "matplotlib",
        "matplotlib.pyplot",
        "matplotlib.figure",
        "matplotlib.backends",
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
    """Minimaler Ersatz für tk.DoubleVar / tk.StringVar."""

    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class _FakeLabel:
    """Minimaler Ersatz für ttk.Label — merkt sich den zuletzt gesetzten Text."""

    def __init__(self):
        self.text = None

    def config(self, text=None, **kwargs):
        self.text = text


class _StubApp:
    """Trägt nur die Attribute, die die getesteten Handler tatsächlich anfassen.

    Widgets (ax/canvas/fig/root) und die Generatoren sind MagicMocks — die Handler
    sollen auf Event-Payload und Statusmeldung geprüft werden, nicht auf Rendering.
    """

    def __init__(self, event_system, **values):
        self.event_system = event_system
        self.status_label = _FakeLabel()
        self.ax = MagicMock()
        self.canvas = MagicMock()
        self.fig = MagicMock()
        self.root = MagicMock()
        self.color_generator = MagicMock()
        self.sound_generator = MagicMock()
        for name, value in values.items():
            setattr(self, f"{name}_var", _FakeVar(value))

    def _ensure_audio_ready(self):
        return True

    def _render_colormap(self, cmap, title):
        self.rendered = (cmap, title)


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


@pytest.fixture
def fractal_app():
    """Stub-App mit Fraktal-Parametern und Farb-/Audio-Auswahl."""
    return _StubApp(
        EventSystem(),
        zoom=4.0,
        center_real=-0.75,
        center_imag=0.1,
        color_mode="resonant",
        audio="Ein",
        volume=0.5,
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


class TestSendFractalData:
    """Tests für TestApp.on_send_fractal_data."""

    def test_emits_fractal_updated(self, fractal_app, test_resonance):
        """Should emit 'fractal_updated' with center as complex and zoom."""
        received = []
        fractal_app.event_system.register_handler(
            "fractal_updated", lambda event_type, data: received.append(data)
        )

        test_resonance.TestApp.on_send_fractal_data(fractal_app)

        assert len(received) == 1
        assert received[0]["center"] == complex(-0.75, 0.1)
        assert received[0]["zoom"] == 4.0

    def test_payload_matches_integration_contract(self, fractal_app, test_resonance):
        """The consumer in integration.py should accept the payload."""
        received = []
        fractal_app.event_system.register_handler(
            "fractal_updated", lambda event_type, data: received.append(data)
        )

        test_resonance.TestApp.on_send_fractal_data(fractal_app)

        import integration

        integration._on_fractal_updated_for_sound("fractal_updated", received[0])

    def test_updates_status_label(self, fractal_app, test_resonance):
        """Should report center and zoom in the status bar."""
        test_resonance.TestApp.on_send_fractal_data(fractal_app)

        assert "-0.75+0.10i" in fractal_app.status_label.text
        assert "4.00" in fractal_app.status_label.text


class TestFractalChanged:
    """Tests für TestApp.on_fractal_changed."""

    def test_does_not_emit(self, fractal_app, test_resonance):
        """Slider moves should not emit — data is sent via the button."""
        received = []
        fractal_app.event_system.register_handler(
            "fractal_updated", lambda event_type, data: received.append(data)
        )

        test_resonance.TestApp.on_fractal_changed(fractal_app, None)

        assert received == []


class TestColormapUpdated:
    """Tests für TestApp.on_colormap_updated."""

    def test_applies_colormap_from_event(self, fractal_app, test_resonance):
        """Should adopt the colormap from the event and refresh the display."""
        shown = []
        fractal_app.on_show_colormap = lambda: shown.append(fractal_app.color_mode_var.get())

        test_resonance.TestApp.on_colormap_updated(
            fractal_app, "colormap_updated", {"colormap": "spectral"}
        )

        assert fractal_app.color_mode_var.get() == "spectral"
        assert shown == ["spectral"]
        assert "spectral" in fractal_app.status_label.text

    def test_falls_back_to_current_selection(self, fractal_app, test_resonance):
        """Without a colormap in the payload the current selection is kept."""
        fractal_app.on_show_colormap = lambda: None

        test_resonance.TestApp.on_colormap_updated(fractal_app, "colormap_updated", {})

        assert fractal_app.color_mode_var.get() == "resonant"


class TestGenerateFractalSound:
    """Tests für TestApp.on_generate_fractal_sound."""

    def test_plays_fm_wave_from_event_parameters(self, fractal_app, test_resonance):
        """Should build an FM wave from base_frequency/modulation_index and play it."""
        test_resonance.TestApp.on_generate_fractal_sound(
            fractal_app,
            "generate_fractal_sound",
            {"base_frequency": 440.0, "modulation_index": 2.0},
        )

        gen = fractal_app.sound_generator
        gen.generate_fm_wave.assert_called_once_with(440.0, 110.0, 2.0, 1.0, 0.5)
        gen.apply_envelope.assert_called_once()
        gen.play_sound_async.assert_called_once()
        assert "440.0 Hz" in fractal_app.status_label.text

    def test_skips_when_audio_disabled(self, fractal_app, test_resonance):
        """Should not touch the sound generator when audio is switched off."""
        fractal_app.audio_var.set("Aus")

        test_resonance.TestApp.on_generate_fractal_sound(
            fractal_app, "generate_fractal_sound", {"base_frequency": 440.0}
        )

        fractal_app.sound_generator.play_sound_async.assert_not_called()
        assert "Audio aus" in fractal_app.status_label.text

    def test_skips_when_no_audio_device(self, fractal_app, test_resonance):
        """Should degrade gracefully when the mixer cannot be initialized."""
        fractal_app._ensure_audio_ready = lambda: False

        test_resonance.TestApp.on_generate_fractal_sound(
            fractal_app, "generate_fractal_sound", {"base_frequency": 440.0}
        )

        fractal_app.sound_generator.play_sound_async.assert_not_called()
        assert "nicht verfügbar" in fractal_app.status_label.text


class TestUpdateResonanceParameters:
    """Tests für TestApp.on_update_resonance_parameters."""

    def test_renders_sensor_based_colormap(self, fractal_app, test_resonance):
        """Should build a sensor-based colormap from the event payload."""
        payload = {
            "accel_magnitude": 3.0,
            "gyro_magnitude": 5.0,
            "accel_x": 1.0,
            "accel_y": 2.0,
            "accel_z": 2.0,
            "gyro_x": 0.0,
            "gyro_y": 3.0,
            "gyro_z": 4.0,
        }

        test_resonance.TestApp.on_update_resonance_parameters(
            fractal_app, "update_resonance_parameters", payload
        )

        sensor_data, zoom = fractal_app.color_generator.create_sensor_based_colormap.call_args[0]
        assert sensor_data == {
            "accel_x": 1.0,
            "accel_y": 2.0,
            "accel_z": 2.0,
            "gyro_x": 0.0,
            "gyro_y": 3.0,
            "gyro_z": 4.0,
        }
        assert zoom == 4.0
        assert fractal_app.rendered[1] == "Farbkarte: sensorbasiert"
        assert "3.00" in fractal_app.status_label.text
        assert "5.00" in fractal_app.status_label.text

    def test_tolerates_missing_keys(self, fractal_app, test_resonance):
        """Missing sensor axes should default to 0.0 rather than raise."""
        test_resonance.TestApp.on_update_resonance_parameters(
            fractal_app, "update_resonance_parameters", {}
        )

        sensor_data, _ = fractal_app.color_generator.create_sensor_based_colormap.call_args[0]
        assert set(sensor_data.values()) == {0.0}


class TestClose:
    """Tests für TestApp.on_close."""

    def test_stops_audio_and_destroys_window(self, fractal_app, test_resonance, monkeypatch):
        """Should stop playback, close the figure and destroy the window."""
        fake_pygame = MagicMock()
        fake_pygame.mixer.get_init.return_value = (44100, -16, 1)
        monkeypatch.setattr(test_resonance, "pygame", fake_pygame)
        fake_plt = MagicMock()
        monkeypatch.setattr(test_resonance, "plt", fake_plt)

        test_resonance.TestApp.on_close(fractal_app)

        fractal_app.sound_generator.stop_sound.assert_called_once()
        fake_pygame.mixer.quit.assert_called_once()
        fake_plt.close.assert_called_once_with(fractal_app.fig)
        fractal_app.root.destroy.assert_called_once()

    def test_skips_mixer_quit_when_not_initialized(self, fractal_app, test_resonance, monkeypatch):
        """Should not quit a mixer that was never initialized."""
        fake_pygame = MagicMock()
        fake_pygame.mixer.get_init.return_value = None
        monkeypatch.setattr(test_resonance, "pygame", fake_pygame)
        monkeypatch.setattr(test_resonance, "plt", MagicMock())

        test_resonance.TestApp.on_close(fractal_app)

        fake_pygame.mixer.quit.assert_not_called()
        fractal_app.root.destroy.assert_called_once()


class TestEnsureAudioReady:
    """Tests für TestApp._ensure_audio_ready."""

    def test_returns_true_when_already_initialized(self, fractal_app, test_resonance, monkeypatch):
        """Should not re-initialize an already running mixer."""
        fake_pygame = MagicMock()
        fake_pygame.mixer.get_init.return_value = (44100, -16, 1)
        monkeypatch.setattr(test_resonance, "pygame", fake_pygame)

        assert test_resonance.TestApp._ensure_audio_ready(fractal_app) is True
        fake_pygame.mixer.init.assert_not_called()

    def test_initializes_when_needed(self, fractal_app, test_resonance, monkeypatch):
        """Should initialize the mixer on first use."""
        fake_pygame = MagicMock()
        fake_pygame.mixer.get_init.return_value = None
        monkeypatch.setattr(test_resonance, "pygame", fake_pygame)

        assert test_resonance.TestApp._ensure_audio_ready(fractal_app) is True
        fake_pygame.mixer.init.assert_called_once()

    def test_returns_false_without_audio_device(self, fractal_app, test_resonance, monkeypatch):
        """Should report failure instead of raising when there is no audio device."""
        fake_pygame = MagicMock()
        fake_pygame.error = RuntimeError
        fake_pygame.mixer.get_init.return_value = None
        fake_pygame.mixer.init.side_effect = RuntimeError("no device")
        monkeypatch.setattr(test_resonance, "pygame", fake_pygame)

        assert test_resonance.TestApp._ensure_audio_ready(fractal_app) is False


class TestRenderColormap:
    """Tests für TestApp._render_colormap."""

    def test_draws_gradient_and_clears_ticks(self, fractal_app, test_resonance):
        """Should clear the axis, draw the gradient and refresh the canvas."""
        cmap = object()

        test_resonance.TestApp._render_colormap(fractal_app, cmap, "Farbkarte: test")

        fractal_app.ax.clear.assert_called_once()
        assert fractal_app.ax.imshow.call_args.kwargs["cmap"] is cmap
        fractal_app.ax.set_title.assert_called_once_with("Farbkarte: test")
        fractal_app.ax.set_xticks.assert_called_once_with([])
        fractal_app.ax.set_yticks.assert_called_once_with([])
        fractal_app.canvas.draw.assert_called_once()
