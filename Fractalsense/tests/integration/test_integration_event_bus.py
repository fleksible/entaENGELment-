"""
Integrationstests für den geteilten Event-Bus (ADR-0004).

Der Bus gehört der Anwendung und wird über `app_context["event_system"]` injiziert.
Diese Tests prüfen, dass die Weiterleitungen genau auf dieser Instanz landen — also
dass ein Abonnent auf dem geteilten Bus die abgeleiteten Events tatsächlich empfängt.

Sie schlagen mit der früheren Implementierung fehl, die in jedem Handler ein neues
`EventSystem()` konstruiert hat: dessen Emits liefen in eine weggeworfene Registry,
der Kreis UI -> integration -> UI schloss sich nie.

Abgedeckte Ketten:
- colormap_updated     -> update_fractal_colormap
- fractal_updated      -> generate_fractal_sound
- sensor_data_updated  -> update_resonance_parameters
- hypergraph_updated   -> generate_hypergraph_sound
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import integration
from modular_app_structure import EventSystem

# Quell-Event -> abgeleitetes Ziel-Event
FORWARDING_CHAINS = [
    ("colormap_updated", "update_fractal_colormap"),
    ("fractal_updated", "generate_fractal_sound"),
    ("sensor_data_updated", "update_resonance_parameters"),
    ("hypergraph_updated", "generate_hypergraph_sound"),
]


@pytest.fixture
def bus():
    """Ein frischer, anwendungseigener Event-Bus."""
    return EventSystem()


@pytest.fixture
def integrated_bus(bus):
    """Ein Bus, auf dem der ResonanceEnhancer integriert wurde."""
    assert integration.integrate_resonance_enhancer({"event_system": bus}) is True
    return bus


def collect(bus, event_type):
    """Registriert einen Sammler für event_type und gibt dessen Liste zurück."""
    received = []
    bus.register_handler(event_type, lambda event_type, data: received.append(data))
    return received


class TestForwardingOnSharedBus:
    """Die abgeleiteten Events müssen auf dem injizierten Bus ankommen."""

    @pytest.mark.parametrize("source_event,target_event", FORWARDING_CHAINS)
    def test_chain_reaches_subscriber_on_shared_bus(
        self, integrated_bus, source_event, target_event
    ):
        """Ein Abonnent auf dem geteilten Bus erhält das weitergeleitete Event."""
        received = collect(integrated_bus, target_event)

        integrated_bus.emit_event(source_event, {})

        assert (
            len(received) == 1
        ), f"{source_event} -> {target_event} kam nicht auf dem geteilten Bus an"

    def test_all_chains_share_one_bus_instance(self, integrated_bus):
        """Alle vier Ketten laufen über dieselbe Instanz — kein zweiter Bus im Spiel."""
        collectors = {target: collect(integrated_bus, target) for _, target in FORWARDING_CHAINS}

        for source, _ in FORWARDING_CHAINS:
            integrated_bus.emit_event(source, {})

        assert {target: len(items) for target, items in collectors.items()} == {
            target: 1 for _, target in FORWARDING_CHAINS
        }


class TestPayloadShapes:
    """Die Payloads bleiben unverändert (keine Vertragsänderung)."""

    def test_colormap_payload(self, integrated_bus):
        """colormap_updated reicht den Farbkartennamen durch."""
        received = collect(integrated_bus, "update_fractal_colormap")

        integrated_bus.emit_event("colormap_updated", {"colormap": "spectral"})

        assert received == [{"colormap": "spectral"}]

    def test_colormap_payload_default(self, integrated_bus):
        """Ohne Farbkarte im Payload greift der Default."""
        received = collect(integrated_bus, "update_fractal_colormap")

        integrated_bus.emit_event("colormap_updated", {})

        assert received == [{"colormap": "viridis"}]

    def test_fractal_sound_payload(self, integrated_bus):
        """fractal_updated leitet Klangparameter aus Zentrum und Zoom ab."""
        received = collect(integrated_bus, "generate_fractal_sound")
        center = complex(-0.75, 0.1)

        integrated_bus.emit_event("fractal_updated", {"center": center, "zoom": 4.0})

        assert received == [
            {
                "base_frequency": 220.0 * 1.4,
                "modulation_index": 0.75 * 5.0,
                "center": center,
                "zoom": 4.0,
            }
        ]

    def test_resonance_payload(self, integrated_bus):
        """sensor_data_updated ergänzt die Magnituden und reicht die Achsen durch."""
        received = collect(integrated_bus, "update_resonance_parameters")

        integrated_bus.emit_event(
            "sensor_data_updated",
            {
                "accel_x": 1.0,
                "accel_y": 2.0,
                "accel_z": 2.0,
                "gyro_x": 0.0,
                "gyro_y": 3.0,
                "gyro_z": 4.0,
            },
        )

        assert received == [
            {
                "accel_magnitude": 3.0,
                "gyro_magnitude": 5.0,
                "accel_x": 1.0,
                "accel_y": 2.0,
                "accel_z": 2.0,
                "gyro_x": 0.0,
                "gyro_y": 3.0,
                "gyro_z": 4.0,
            }
        ]

    def test_hypergraph_payload(self, integrated_bus):
        """hypergraph_updated leitet die Akkordkomplexität aus der Kantenzahl ab."""
        received = collect(integrated_bus, "generate_hypergraph_sound")

        integrated_bus.emit_event("hypergraph_updated", {"nodes_count": 6, "edges_count": 7})

        assert received == [{"nodes_count": 6, "edges_count": 7, "chord_complexity": 3}]


class TestIdempotency:
    """Wiederholte Integration darf keine doppelten Handler registrieren."""

    def test_second_integration_is_a_noop(self, bus):
        """Zweimal integrieren -> jedes Event wird trotzdem nur einmal weitergeleitet."""
        assert integration.integrate_resonance_enhancer({"event_system": bus}) is True
        assert integration.integrate_resonance_enhancer({"event_system": bus}) is True

        collectors = {target: collect(bus, target) for _, target in FORWARDING_CHAINS}

        for source, _ in FORWARDING_CHAINS:
            bus.emit_event(source, {})

        for target, items in collectors.items():
            assert len(items) == 1, f"{target} wurde {len(items)}x weitergeleitet"

    def test_repeated_integration_reports_success(self, bus):
        """Auch der wiederholte Aufruf meldet Erfolg, nicht Fehler."""
        integration.integrate_resonance_enhancer({"event_system": bus})

        assert integration.integrate_resonance_enhancer({"event_system": bus}) is True


class TestNoGlobalState:
    """EventSystem bleibt unabhängig instanziierbar — kein Singleton."""

    def test_instances_have_separate_registries(self):
        """Zwei Busse teilen keine Handler."""
        bus_a, bus_b = EventSystem(), EventSystem()
        received_a = collect(bus_a, "ping")

        bus_b.emit_event("ping", {})

        assert received_a == []

    def test_integrating_one_bus_does_not_wire_another(self, bus):
        """Ein nicht integrierter Bus leitet nichts weiter."""
        integration.integrate_resonance_enhancer({"event_system": bus})

        other_bus = EventSystem()
        received = collect(other_bus, "update_fractal_colormap")

        other_bus.emit_event("colormap_updated", {"colormap": "spectral"})

        assert received == []

    def test_integration_flag_is_per_instance(self, bus):
        """Der Idempotenz-Marker hängt am Bus, nicht an der Klasse."""
        integration.integrate_resonance_enhancer({"event_system": bus})

        fresh = EventSystem()
        assert getattr(fresh, integration._CONNECTED_FLAG, False) is False

    def test_forwarding_targets_the_injected_bus_only(self, bus):
        """Weitergeleitet wird ausschließlich auf den injizierten Bus."""
        integration.integrate_resonance_enhancer({"event_system": bus})

        listener = EventSystem()
        received_elsewhere = collect(listener, "update_resonance_parameters")
        received_here = collect(bus, "update_resonance_parameters")

        bus.emit_event("sensor_data_updated", {"accel_x": 1.0})

        assert len(received_here) == 1
        assert received_elsewhere == []


class TestIntegrationEntryPoint:
    """Verhalten von integrate_resonance_enhancer selbst."""

    def test_returns_false_without_event_system(self):
        """Fehlt der Bus im App-Kontext, schlägt die Integration fehl."""
        assert integration.integrate_resonance_enhancer({}) is False

    def test_returns_false_when_event_system_is_none(self):
        """Ein explizites None ist ebenfalls ein Fehlerfall."""
        assert integration.integrate_resonance_enhancer({"event_system": None}) is False


class TestMappersArePure:
    """Die _on_*-Funktionen bilden nur ab und emittieren nicht selbst."""

    def test_mappers_return_target_and_payload(self):
        """Jeder Mapper liefert (Ziel-Event, Payload)."""
        mappers = {
            integration._on_colormap_updated: "update_fractal_colormap",
            integration._on_fractal_updated_for_sound: "generate_fractal_sound",
            integration._on_sensor_data_updated_for_resonance: "update_resonance_parameters",
            integration._on_hypergraph_updated: "generate_hypergraph_sound",
        }

        for mapper, expected_target in mappers.items():
            target, payload = mapper("source_event", {})
            assert target == expected_target
            assert isinstance(payload, dict)
