"""
FractalSense EntaENGELment - Integration des ResonanceEnhancer-Moduls

Dieses Modul integriert den ResonanceEnhancer mit den bestehenden Modulen.
"""

import os
import sys
import importlib
from typing import Any

# Importiere das modulare Framework
from modular_app_structure import ModuleInterface, EventSystem

def integrate_resonance_enhancer(app_context: dict[str, Any]) -> bool:
    """Integriert das ResonanceEnhancer-Modul mit den bestehenden Modulen.

    Args:
        app_context: Dictionary mit dem App-Kontext

    Returns:
        bool: True, wenn die Integration erfolgreich war, sonst False
    """
    try:
        # Event-System aus dem App-Kontext holen
        event_system = app_context.get("event_system")
        if event_system is None:
            print("Fehler: Event-System nicht im App-Kontext gefunden.")
            return False

        # Verbindung zwischen Fractal Visualization und ResonanceEnhancer herstellen
        _connect_fractal_to_resonance(event_system)

        # Verbindung zwischen Sensor Integration und ResonanceEnhancer herstellen
        _connect_sensor_to_resonance(event_system)

        # Verbindung zwischen Hypergraph Visualization und ResonanceEnhancer herstellen
        _connect_hypergraph_to_resonance(event_system)

        print("ResonanceEnhancer erfolgreich mit bestehenden Modulen integriert.")
        return True
    except Exception as e:
        print(f"Fehler bei der Integration des ResonanceEnhancer-Moduls: {str(e)}")
        return False

def _connect_fractal_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Fractal Visualization Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Farbkarten-Updates registrieren
    event_system.register_handler("colormap_updated", _on_colormap_updated)

    # Event-Handler für Fraktal-Updates registrieren
    event_system.register_handler("fractal_updated", _on_fractal_updated_for_sound)

def _connect_sensor_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Sensor Integration Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Sensordaten-Updates registrieren
    event_system.register_handler("sensor_data_updated", _on_sensor_data_updated_for_resonance)

def _connect_hypergraph_to_resonance(event_system: EventSystem) -> None:
    """Verbindet das Hypergraph Visualization Modul mit dem ResonanceEnhancer.

    Args:
        event_system: Event-System für die Kommunikation zwischen Modulen
    """
    # Event-Handler für Hypergraph-Updates registrieren
    event_system.register_handler("hypergraph_updated", _on_hypergraph_updated)

def _on_colormap_updated(event_type: str, event_data: dict[str, Any]) -> None:
    """Event-Handler für aktualisierte Farbkarten.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten
    """
    # Extrahiere Farbkarte
    colormap = event_data.get("colormap", "viridis")

    # Sende Event an Fractal Visualization Modul
    from modular_app_structure import EventSystem
    event_system = EventSystem()
    event_system.emit_event("update_fractal_colormap", {"colormap": colormap})

def _on_fractal_updated_for_sound(event_type: str, event_data: dict[str, Any]) -> None:
    """Event-Handler für aktualisiertes Fraktal (für Klangerzeugung).

    Args:
        event_type: Typ des Events
        event_data: Event-Daten
    """
    # Extrahiere Fraktal-Parameter
    center = event_data.get("center", complex(-0.75, 0))
    zoom = event_data.get("zoom", 1.0)

    # Berechne Klangparameter basierend auf Fraktal-Parametern
    base_frequency = 220.0 * (1.0 + zoom / 10.0)  # Höhere Frequenz bei höherem Zoom
    modulation_index = abs(center.real) * 5.0  # Modulationsindex basierend auf Realteil des Zentrums

    # Sende Event an ResonanceEnhancer
    from modular_app_structure import EventSystem
    event_system = EventSystem()
    event_system.emit_event("generate_fractal_sound", {
        "base_frequency": base_frequency,
        "modulation_index": modulation_index,
        "center": center,
        "zoom": zoom
    })

def _on_sensor_data_updated_for_resonance(event_type: str, event_data: dict[str, Any]) -> None:
    """Event-Handler für aktualisierte Sensordaten (für ResonanceEnhancer).

    Args:
        event_type: Typ des Events
        event_data: Event-Daten
    """
    # Extrahiere Sensordaten
    accel_x = event_data.get("accel_x", 0)
    accel_y = event_data.get("accel_y", 0)
    accel_z = event_data.get("accel_z", 0)
    gyro_x = event_data.get("gyro_x", 0)
    gyro_y = event_data.get("gyro_y", 0)
    gyro_z = event_data.get("gyro_z", 0)

    # Berechne Magnitudes
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2)**0.5
    gyro_magnitude = (gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5

    # Sende Event an ResonanceEnhancer
    from modular_app_structure import EventSystem
    event_system = EventSystem()
    event_system.emit_event("update_resonance_parameters", {
        "accel_magnitude": accel_magnitude,
        "gyro_magnitude": gyro_magnitude,
        "accel_x": accel_x,
        "accel_y": accel_y,
        "accel_z": accel_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z
    })

def _on_hypergraph_updated(event_type: str, event_data: dict[str, Any]) -> None:
    """Event-Handler für aktualisierten Hypergraphen.

    Args:
        event_type: Typ des Events
        event_data: Event-Daten
    """
    # Extrahiere Hypergraph-Parameter
    nodes_count = event_data.get("nodes_count", 0)
    edges_count = event_data.get("edges_count", 0)

    # Berechne Klangparameter basierend auf Hypergraph-Struktur
    chord_complexity = min(5, max(1, edges_count // 2))  # 1-5 basierend auf Kantenanzahl

    # Sende Event an ResonanceEnhancer
    from modular_app_structure import EventSystem
    event_system = EventSystem()
    event_system.emit_event("generate_hypergraph_sound", {
        "nodes_count": nodes_count,
        "edges_count": edges_count,
        "chord_complexity": chord_complexity
    })
