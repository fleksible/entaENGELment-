"""
FractalSense EntaENGELment - README

Diese Datei enthält eine Übersicht über die FractalSense EntaENGELment App und Anweisungen zur Installation und Verwendung.
"""

# FractalSense EntaENGELment

Eine modulare Anwendung zur Visualisierung von Fraktalen, Hypergraphen und Dimensionsübergängen basierend auf Smartphone-Sensordaten (Phyphox).

## Übersicht

FractalSense EntaENGELment ist ein resonantes, interaktives System, das Smartphone-Sensordaten (Phyphox) nutzt, um fraktale Strukturen, Hypergraphen und Dimensionsübergänge zu visualisieren. Es ist in einem modularen Framework implementiert, das eine einfache Integration neuer Module ermöglicht.

Die Anwendung verbindet technische Elemente mit philosophischen Konzepten:
- **Resonanz als Einheit**: Sensordaten und Fraktale verschmelzen in einer fundamentalen Frequenz
- **Autopoiesis**: Das System entwickelt sich selbst durch die Interaktion mit dem Benutzer
- **Mereotopologie**: Hypergraphen und Fraktale bilden ein navigierbares Wissensnetz
- **Supraleitung**: Datenfluss als plasmaartiger Zustand, stabilisiert durch Resonanz

## Funktionen

- **Modulares Framework**: Einfache Integration neuer Module
- **Fraktalvisualisierung**: Interaktive Visualisierung des Mandelbrot-Sets
- **Sensordatenintegration**: Verbindung mit Phyphox für Echtzeit-Sensordaten
- **Hypergraph-Visualisierung**: Darstellung von Sensordaten als Hypergraphen
- **Event-basierte Kommunikation**: Lose Kopplung zwischen Modulen
- **Konfigurationsmanagement**: Speichern und Laden von Einstellungen

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Pip (Python-Paketmanager)

### Abhängigkeiten installieren

```bash
pip install numpy matplotlib numba requests hypernetx
```

### Phyphox-App

Für die Sensordatenintegration wird die Phyphox-App benötigt:
- [Phyphox für Android](https://play.google.com/store/apps/details?id=de.rwth_aachen.phyphox)
- [Phyphox für iOS](https://apps.apple.com/app/phyphox/id1127319693)

## Verwendung

### Starten der Anwendung

```bash
python main.py
```

### Kommandozeilenoptionen

- `--config`: Pfad zur Konfigurationsdatei (Standard: `config.json`)
- `--modules-dir`: Verzeichnis mit Modulen (Standard: `modules`)
- `--log-level`: Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Beispiel:
```bash
python main.py --config=meine_config.json --modules-dir=meine_module --log-level=DEBUG
```

### Phyphox-Verbindung einrichten

1. Öffne die Phyphox-App auf deinem Smartphone
2. Aktiviere die Remote-Schnittstelle in den Einstellungen
3. Verbinde dein Smartphone und deinen Computer mit demselben WLAN-Netzwerk
4. Notiere die IP-Adresse, die in der Phyphox-App angezeigt wird
5. Gib diese IP-Adresse in der FractalSense-App ein

## Modulare Architektur

Die Anwendung basiert auf einer modularen Architektur:

- **Modulares Framework**: `modular_app_structure.py`
- **Module**:
  - `fractal_visualization`: Visualisierung von Fraktalen
  - `sensor_integration`: Integration von Phyphox-Sensordaten
  - `hypergraph_visualization`: Visualisierung von Hypergraphen

Weitere Details zur Architektur und zur Erstellung eigener Module findest du in der [Dokumentation](documentation.md).

## Dateien

- `main.py`: Hauptanwendung mit GUI
- `modular_app_structure.py`: Modulares Framework
- `modules/`: Verzeichnis mit Modulen
  - `fractal_visualization/`: Modul für Fraktalvisualisierung
  - `sensor_integration/`: Modul für Sensordatenintegration
  - `hypergraph_visualization/`: Modul für Hypergraph-Visualisierung
- `documentation.md`: Ausführliche Dokumentation
- `README.md`: Diese Datei

## Erweiterung

Die Anwendung kann durch neue Module erweitert werden. Eine Anleitung zur Erstellung eigener Module findest du in der [Dokumentation](documentation.md).

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht.
