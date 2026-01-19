"""
FractalSense EntaENGELment - Dokumentation

Diese Datei enthält die Dokumentation für die modulare App-Struktur und die implementierten Module.
"""

# FractalSense EntaENGELment - Modulare App-Struktur

## Übersicht

Die FractalSense EntaENGELment App ist eine modulare Anwendung, die Smartphone-Sensordaten (Phyphox) nutzt, 
um fraktale Strukturen, Hypergraphen und Dimensionsübergänge zu visualisieren. Die App ist in einem 
modularen Framework implementiert, das eine einfache Integration neuer Module ermöglicht.

## Architektur

Die App basiert auf einer modularen Architektur mit folgenden Hauptkomponenten:

1. **Modulares Framework**: Implementiert in `modular_app_structure.py`
   - ModuleInterface: Basis-Interface für alle Module
   - ModuleRegistry: Verwaltet die Registrierung und Verwaltung von Modulen
   - EventSystem: Implementiert ein Event-System für die Kommunikation zwischen Modulen
   - ConfigManager: Verwaltet die Konfiguration der App und der Module
   - FractalSenseApp: Hauptklasse der App

2. **Module**: Implementiert in separaten Verzeichnissen unter `modules/`
   - Fractal Visualization: Visualisiert Fraktale (Mandelbrot-Set)
   - Sensor Integration: Integriert Phyphox-Sensordaten
   - Hypergraph Visualization: Visualisiert Hypergraphen basierend auf Sensordaten

3. **Hauptanwendung**: Implementiert in `main.py`
   - FractalSenseGUI: Grafische Benutzeroberfläche für die App

## Modulares Framework

### ModuleInterface

Das `ModuleInterface` definiert die Schnittstelle, die alle Module implementieren müssen:

```python
class ModuleInterface(ABC):
    @abstractmethod
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        """Initialisiert das Modul mit dem App-Kontext."""
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Eingabedaten und gibt Ergebnisse zurück."""
        pass
    
    @abstractmethod
    def get_ui_components(self) -> Dict[str, Any]:
        """Gibt UI-Komponenten des Moduls zurück."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Bereinigt Ressourcen des Moduls."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Gibt den Namen des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Gibt die Version des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Gibt die Beschreibung des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """Gibt die Abhängigkeiten des Moduls zurück."""
        pass
```

### ModuleRegistry

Der `ModuleRegistry` verwaltet die Registrierung und Verwaltung von Modulen:

- Registriert Modulklassen
- Entdeckt Module in einem Verzeichnis
- Initialisiert Module in der richtigen Reihenfolge basierend auf Abhängigkeiten
- Gibt Zugriff auf initialisierte Module

### EventSystem

Das `EventSystem` implementiert ein Event-System für die Kommunikation zwischen Modulen:

- Registriert Event-Handler
- Entfernt Event-Handler
- Sendet Events an alle registrierten Handler

### ConfigManager

Der `ConfigManager` verwaltet die Konfiguration der App und der Module:

- Lädt die Konfiguration aus einer Datei
- Speichert die Konfiguration in einer Datei
- Gibt Zugriff auf die Konfiguration
- Verwaltet die Konfiguration der Module

### FractalSenseApp

Die `FractalSenseApp` ist die Hauptklasse der App:

- Initialisiert die App
- Startet die App
- Stoppt die App
- Gibt Zugriff auf Module

## Module

### Fractal Visualization

Das Modul `fractal_visualization` visualisiert Fraktale (Mandelbrot-Set):

- Rendert das Mandelbrot-Set mit einstellbarer Auflösung und Iterationszahl
- Unterstützt Zoom und Navigation
- Reagiert auf Sensordaten zur dynamischen Anpassung des Fraktals
- Bietet UI-Komponenten zur Steuerung

Hauptfunktionen:
- `_render_fractal()`: Rendert das Fraktal
- `_mandelbrot()`: Berechnet das Mandelbrot-Set (mit Numba-Optimierung)
- Event-Handler für Sensordaten und UI-Interaktionen

### Sensor Integration

Das Modul `sensor_integration` integriert Phyphox-Sensordaten:

- Verbindet sich mit der Phyphox-App über die REST-API
- Ruft kontinuierlich Sensordaten ab (Beschleunigung, Gyroskop)
- Filtert und verarbeitet Sensordaten
- Sendet Events mit verarbeiteten Sensordaten

Hauptfunktionen:
- `_start_polling()`: Startet die kontinuierliche Abfrage von Sensordaten
- `_stop_polling()`: Stoppt die Abfrage von Sensordaten
- `_get_sensor_data()`: Ruft Sensordaten von Phyphox ab
- `_process_sensor_data()`: Verarbeitet und filtert Sensordaten

### Hypergraph Visualization

Das Modul `hypergraph_visualization` visualisiert Hypergraphen basierend auf Sensordaten:

- Erstellt Hypergraphen aus Sensordaten
- Visualisiert Hypergraphen mit hypernetx (falls verfügbar)
- Bietet eine alternative Visualisierung ohne hypernetx
- Reagiert auf Sensordaten und Fraktal-Updates

Hauptfunktionen:
- `_update_hypergraph()`: Aktualisiert den Hypergraphen basierend auf Sensordaten
- `_create_hypergraph_from_sensor_data()`: Erstellt einen Hypergraphen aus Sensordaten
- `_visualize_hypergraph()`: Visualisiert den Hypergraphen

## Hauptanwendung

Die Hauptanwendung `main.py` implementiert die grafische Benutzeroberfläche für die App:

- Erstellt und initialisiert die App
- Erstellt die GUI mit Tkinter
- Zeigt UI-Komponenten der Module an
- Verarbeitet Benutzerinteraktionen

## Verwendung

### Installation

1. Installiere die erforderlichen Pakete:
   ```
   pip install numpy matplotlib numba requests hypernetx
   ```

2. Klone das Repository oder kopiere die Dateien in ein Verzeichnis.

### Ausführung

1. Starte die App:
   ```
   python main.py
   ```

2. Optional: Gib einen alternativen Pfad zur Konfigurationsdatei an:
   ```
   python main.py --config=meine_config.json
   ```

3. Optional: Gib ein alternatives Modulverzeichnis an:
   ```
   python main.py --modules-dir=meine_module
   ```

4. Optional: Setze das Log-Level:
   ```
   python main.py --log-level=DEBUG
   ```

### Konfiguration

Die Konfiguration der App erfolgt über eine JSON-Datei (standardmäßig `config.json`):

```json
{
  "app": {
    "name": "FractalSense EntaENGELment",
    "version": "1.0.0",
    "modules_dir": "modules"
  },
  "modules": {
    "fractal_visualization": {
      "center_real": -0.75,
      "center_imag": 0,
      "zoom": 1.0,
      "resolution": 400,
      "max_iter": 50,
      "colormap": "viridis"
    },
    "sensor_integration": {
      "ip_address": "192.168.1.100",
      "port": 8080,
      "polling_interval": 0.1,
      "filter_buffer_size": 10
    },
    "hypergraph_visualization": {
      "threshold": 0.5,
      "history_buffer_size": 50
    }
  }
}
```

## Erweiterung

### Neue Module erstellen

Um ein neues Modul zu erstellen:

1. Erstelle ein neues Verzeichnis unter `modules/` mit dem Namen des Moduls.
2. Erstelle eine `__init__.py`-Datei im Modulverzeichnis.
3. Implementiere eine Klasse, die `ModuleInterface` implementiert.
4. Stelle sicher, dass die Klasse alle erforderlichen Methoden implementiert.

Beispiel für ein minimales Modul:

```python
from modular_app_structure import ModuleInterface
from typing import Dict, List, Any

class MyModule(ModuleInterface):
    def __init__(self):
        self._name = "my_module"
        self._version = "1.0.0"
        self._description = "Mein eigenes Modul"
        self._dependencies = []
    
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        # Initialisiere das Modul
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Verarbeite Eingabedaten
        return {}
    
    def get_ui_components(self) -> Dict[str, Any]:
        # Gib UI-Komponenten zurück
        return {}
    
    def cleanup(self) -> None:
        # Bereinige Ressourcen
        pass
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def dependencies(self) -> List[str]:
        return self._dependencies
```

### Event-System verwenden

Um das Event-System zu verwenden:

1. Hole das Event-System aus dem App-Kontext:
   ```python
   self._event_system = app_context.get("event_system")
   ```

2. Registriere Event-Handler:
   ```python
   self._event_system.register_handler("event_type", self._handler)
   ```

3. Implementiere Event-Handler:
   ```python
   def _handler(self, event_type: str, event_data: Dict[str, Any]) -> None:
       # Verarbeite Event
       pass
   ```

4. Sende Events:
   ```python
   self._event_system.emit_event("event_type", {"key": "value"})
   ```

### Konfiguration verwenden

Um die Konfiguration zu verwenden:

1. Hole den Konfigurationsmanager aus dem App-Kontext:
   ```python
   self._config_manager = app_context.get("config_manager")
   ```

2. Lade die Konfiguration des Moduls:
   ```python
   config = self._config_manager.get_module_config(self._name)
   ```

3. Speichere die Konfiguration des Moduls:
   ```python
   self._config_manager.set_module_config(self._name, {"key": "value"})
   ```

## Beispiele

### Beispiel: Sensordaten verarbeiten

```python
def _on_sensor_data_updated(self, event_type: str, event_data: Dict[str, Any]) -> None:
    # Sensordaten extrahieren
    accel_x = event_data.get("accel_x", 0)
    accel_y = event_data.get("accel_y", 0)
    accel_z = event_data.get("accel_z", 0)
    
    # Sensordaten verarbeiten
    # ...
    
    # Event senden
    self._event_system.emit_event("processed_data", {"result": result})
```

### Beispiel: UI-Komponenten erstellen

```python
def get_ui_components(self) -> Dict[str, Any]:
    return {
        "controls": {
            "parameter": {
                "type": "number",
                "label": "Parameter",
                "value": self._parameter,
                "min": 0,
                "max": 100
            },
            "action": {
                "type": "button",
                "label": "Aktion ausführen",
                "event": "ui_action"
            }
        }
    }
```

## Fehlerbehebung

### Modul wird nicht geladen

- Stelle sicher, dass das Modul in einem Verzeichnis unter `modules/` liegt.
- Stelle sicher, dass das Verzeichnis eine `__init__.py`-Datei enthält.
- Stelle sicher, dass die Modulklasse `ModuleInterface` implementiert.
- Überprüfe die Logs auf Fehlermeldungen.

### Event-Handler wird nicht aufgerufen

- Stelle sicher, dass der Event-Handler korrekt registriert wurde.
- Stelle sicher, dass der Event-Typ korrekt ist.
- Überprüfe die Logs auf Fehlermeldungen.

### Konfiguration wird nicht geladen

- Stelle sicher, dass die Konfigurationsdatei existiert und gültig ist.
- Stelle sicher, dass der Modulname korrekt ist.
- Überprüfe die Logs auf Fehlermeldungen.

## Bekannte Probleme

- Die Hypergraph-Visualisierung erfordert das Paket `hypernetx`, das möglicherweise nicht auf allen Systemen verfügbar ist.
- Die Phyphox-Integration erfordert eine laufende Phyphox-App mit aktivierter Remote-Schnittstelle.
- Die GUI ist derzeit auf Tkinter beschränkt und könnte in Zukunft auf andere Frameworks erweitert werden.

## Zukünftige Erweiterungen

- Unterstützung für weitere Fraktaltypen (Julia-Set, Newton-Fraktal, etc.)
- Erweiterte Hypergraph-Visualisierung mit mehr Analysemöglichkeiten
- Integration weiterer Sensoren (Magnetometer, Barometer, etc.)
- Unterstützung für andere GUI-Frameworks (Qt, Web-basiert, etc.)
- Speichern und Laden von Fraktal-Zuständen
- Export von Visualisierungen als Bilder oder Videos
