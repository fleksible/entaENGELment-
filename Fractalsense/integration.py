"""
FractalSense EntaENGELment - Integration des ResonanceEnhancer-Moduls

Dieses Modul integriert den ResonanceEnhancer mit den bestehenden Modulen.

Architektur: Der Event-Bus gehört der Anwendung und wird explizit injiziert
(ADR-0004). `integrate_resonance_enhancer()` erhält ihn über
`app_context["event_system"]`; jeder Forwarding-Handler emittiert auf genau dieser
Instanz. Kein Singleton, kein Modulzustand — die Weiterleitung entsteht als Closure
über den übergebenen Bus.

Die `_on_*`-Funktionen sind reine Abbildungen: sie berechnen aus einem Quell-Event
`(Ziel-Event, Payload)` und emittieren selbst nicht. Den Transport übernimmt
`_make_forwarder()`. Dadurch bleibt die Abbildungslogik ohne Bus testbar.
"""

from typing import Any, Callable

# Importiere das modulare Framework
from modular_app_structure import EventSystem

# Marker auf der Bus-Instanz: verhindert doppelte Registrierung bei wiederholter
# Integration. Bewusst pro Instanz (setattr auf dem übergebenen Bus), nicht global —
# zwei EventSystem-Instanzen bleiben vollständig unabhängig.
_CONNECTED_FLAG = "_resonance_enhancer_connected"

# Typalias für die reinen Abbildungsfunktionen: (event_type, event_data) -> (ziel, payload)
EventMapper = Callable[[str, dict[str, Any]], "tuple[str, dict[str, Any]]"]


def integrate_resonance_enhancer(app_context: dict[str, Any]) -> bool:
    """Integriert das ResonanceEnhancer-Modul mit den bestehenden Modulen.

    Die Registrierung ist idempotent: ein zweiter Aufruf mit demselben Bus
    registriert die Forwarding-Handler nicht erneut und gibt True zurück.

    Args:
        app_context: Dictionary mit dem App-Kontext; muss unter "event_system"
            den Event-Bus der Anwendung enthalten

    Returns:
        bool: True, wenn die Integration erfolgreich war (oder bereits bestand),
        sonst False
    """
    try:
        # Event-System aus dem App-Kontext holen — dieser Bus trägt den gesamten Kreis
        event_system = app_context.get("event_system")
        if event_system is None:
            print("Fehler: Event-System nicht im App-Kontext gefunden.")
            return False

        if getattr(event_system, _CONNECTED_FLAG, False):
            print("ResonanceEnhancer ist mit diesem Event-Bus bereits verbunden.")
            return True

        # Verbindung zwischen Fractal Visualization und ResonanceEnhancer herstellen
        _connect_fractal_to_resonance(event_system)

        # Verbindung zwischen Sensor Integration und ResonanceEnhancer herstellen
        _connect_sensor_to_resonance(event_system)

        # Verbindung zwischen Hypergraph Visualization und ResonanceEnhancer herstellen
        _connect_hypergraph_to_resonance(event_system)

        setattr(event_system, _CONNECTED_FLAG, True)

        print("ResonanceEnhancer erfolgreich mit bestehenden Modulen integriert.")
        return True
    except Exception as e:
        print(f"Fehler bei der Integration des ResonanceEnhancer-Moduls: {str(e)}")
        return False


def _make_forwarder(event_system: EventSystem, mapper: EventMapper) -> Callable[..., None]:
    """Baut einen Forwarding-Handler, der auf dem übergebenen Bus emittiert.

    Args:
        event_system: Der Bus, auf dem das Ziel-Event emittiert wird
        mapper: Reine Abbildung (event_type, event_data) -> (ziel_event, payload)

    Returns:
        Callable: Handler mit der vom EventSystem erwarteten Signatur
        (event_type, event_data)
    """

    def _forward(event_type: str, event_data: dict[str, Any]) -> None:
        target_event, payload = mapper(event_type, event_data)
        event_system.emit_event(target_event, payload)

    return _forward


def _connect_fractal_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Fractal Visualization Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Farbkarten-Updates registrieren
    event_system.register_handler(
        "colormap_updated", _make_forwarder(event_system, _on_colormap_updated)
    )

    # Event-Handler für Fraktal-Updates registrieren
    event_system.register_handler(
        "fractal_updated", _make_forwarder(event_system, _on_fractal_updated_for_sound)
    )


def _connect_sensor_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Sensor Integration Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Sensordaten-Updates registrieren
    event_system.register_handler(
        "sensor_data_updated",
        _make_forwarder(event_system, _on_sensor_data_updated_for_resonance),
    )


def _connect_hypergraph_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Hypergraph Visualization Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Hypergraph-Updates registrieren
    event_system.register_handler(
        "hypergraph_updated", _make_forwarder(event_system, _on_hypergraph_updated)
    )


def _on_colormap_updated(
    event_type: str, event_data: dict[str, Any]
) -> "tuple[str, dict[str, Any]]":
    """Bildet ein Farbkarten-Update auf das Fractal-Visualization-Event ab.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten

    Returns:
        tuple: (Ziel-Event, Payload) — emittiert wird in _make_forwarder
    """
    # Extrahiere Farbkarte
    colormap = event_data.get("colormap", "viridis")

    # Ziel: Fractal Visualization Modul
    return "update_fractal_colormap", {"colormap": colormap}


def _on_fractal_updated_for_sound(
    event_type: str, event_data: dict[str, Any]
) -> "tuple[str, dict[str, Any]]":
    """Bildet ein Fraktal-Update auf die Klangparameter ab.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten

    Returns:
        tuple: (Ziel-Event, Payload) — emittiert wird in _make_forwarder
    """
    # Extrahiere Fraktal-Parameter
    center = event_data.get("center", complex(-0.75, 0))
    zoom = event_data.get("zoom", 1.0)

    # Berechne Klangparameter basierend auf Fraktal-Parametern
    base_frequency = 220.0 * (1.0 + zoom / 10.0)  # Höhere Frequenz bei höherem Zoom
    # Modulationsindex basierend auf Realteil des Zentrums
    modulation_index = abs(center.real) * 5.0

    # Ziel: ResonanceEnhancer
    return "generate_fractal_sound", {
        "base_frequency": base_frequency,
        "modulation_index": modulation_index,
        "center": center,
        "zoom": zoom,
    }


def _on_sensor_data_updated_for_resonance(
    event_type: str, event_data: dict[str, Any]
) -> "tuple[str, dict[str, Any]]":
    """Bildet Sensordaten auf die Resonanz-Parameter ab.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten

    Returns:
        tuple: (Ziel-Event, Payload) — emittiert wird in _make_forwarder
    """
    # Extrahiere Sensordaten
    accel_x = event_data.get("accel_x", 0)
    accel_y = event_data.get("accel_y", 0)
    accel_z = event_data.get("accel_z", 0)
    gyro_x = event_data.get("gyro_x", 0)
    gyro_y = event_data.get("gyro_y", 0)
    gyro_z = event_data.get("gyro_z", 0)

    # Berechne Magnitudes
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2) ** 0.5
    gyro_magnitude = (gyro_x**2 + gyro_y**2 + gyro_z**2) ** 0.5

    # Ziel: ResonanceEnhancer
    return "update_resonance_parameters", {
        "accel_magnitude": accel_magnitude,
        "gyro_magnitude": gyro_magnitude,
        "accel_x": accel_x,
        "accel_y": accel_y,
        "accel_z": accel_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z,
    }


def _on_hypergraph_updated(
    event_type: str, event_data: dict[str, Any]
) -> "tuple[str, dict[str, Any]]":
    """Bildet ein Hypergraph-Update auf die Klangparameter ab.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten

    Returns:
        tuple: (Ziel-Event, Payload) — emittiert wird in _make_forwarder
    """
    # Extrahiere Hypergraph-Parameter
    nodes_count = event_data.get("nodes_count", 0)
    edges_count = event_data.get("edges_count", 0)

    # Berechne Klangparameter basierend auf Hypergraph-Struktur
    chord_complexity = min(5, max(1, edges_count // 2))  # 1-5 basierend auf Kantenanzahl

    # Ziel: ResonanceEnhancer
    return "generate_hypergraph_sound", {
        "nodes_count": nodes_count,
        "edges_count": edges_count,
        "chord_complexity": chord_complexity,
    }
