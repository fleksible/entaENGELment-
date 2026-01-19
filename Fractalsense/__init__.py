"""
FractalSense EntaENGELment - Beispielmodul für Fraktalvisualisierung

Dieses Modul implementiert die Fraktalvisualisierung für die FractalSense EntaENGELment App.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import time

# Optional numba import for performance optimization
try:
    from numba import jit
except ImportError:
    # Fallback no-op decorator when numba is not installed
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
from typing import Dict, List, Any, Tuple, Optional

# Importiere das Modul-Interface
from modular_app_structure import ModuleInterface

class FractalVisualizationModule(ModuleInterface):
    """Modul für die Visualisierung von Fraktalen."""
    
    def __init__(self):
        self._name = "fractal_visualization"
        self._version = "1.0.0"
        self._description = "Modul für die Visualisierung von Fraktalen"
        self._dependencies = []
        
        # Fraktalparameter
        self._center = complex(-0.75, 0)
        self._zoom = 1.0
        self._resolution = 400
        self._max_iter = 50
        self._colormap = 'viridis'
        
        # Matplotlib-Figur
        self._fig = None
        self._ax = None
        self._img = None
        
        # Event-System
        self._event_system = None
        
        # Konfigurationsmanager
        self._config_manager = None
    
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        """Initialisiert das Modul mit dem App-Kontext.
        
        Args:
            app_context: Dictionary mit dem App-Kontext
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False
        """
        try:
            # Event-System aus dem App-Kontext holen
            self._event_system = app_context.get("event_system")
            if self._event_system is None:
                print("Fehler: Event-System nicht im App-Kontext gefunden.")
                return False
            
            # Konfigurationsmanager aus dem App-Kontext holen
            self._config_manager = app_context.get("config_manager")
            if self._config_manager is None:
                print("Fehler: Konfigurationsmanager nicht im App-Kontext gefunden.")
                return False
            
            # Konfiguration laden
            self._load_config()
            
            # Event-Handler registrieren
            self._event_system.register_handler("sensor_data_updated", self._on_sensor_data_updated)
            self._event_system.register_handler("ui_zoom_in", self._on_zoom_in)
            self._event_system.register_handler("ui_zoom_out", self._on_zoom_out)
            self._event_system.register_handler("ui_move", self._on_move)
            
            # Matplotlib-Figur initialisieren
            self._fig, self._ax = plt.subplots(figsize=(8, 8))
            self._ax.axis('off')
            
            # Initiales Fraktal rendern
            self._render_fractal()
            
            print(f"Modul '{self._name}' erfolgreich initialisiert.")
            return True
        except Exception as e:
            print(f"Fehler bei der Initialisierung des Moduls '{self._name}': {str(e)}")
            return False
    
    def _load_config(self) -> None:
        """Lädt die Konfiguration des Moduls."""
        if self._config_manager:
            config = self._config_manager.get_module_config(self._name)
            
            if "center_real" in config and "center_imag" in config:
                self._center = complex(config.get("center_real", -0.75), 
                                      config.get("center_imag", 0))
            
            self._zoom = config.get("zoom", 1.0)
            self._resolution = config.get("resolution", 400)
            self._max_iter = config.get("max_iter", 50)
            self._colormap = config.get("colormap", 'viridis')
    
    def _save_config(self) -> None:
        """Speichert die Konfiguration des Moduls."""
        if self._config_manager:
            config = {
                "center_real": self._center.real,
                "center_imag": self._center.imag,
                "zoom": self._zoom,
                "resolution": self._resolution,
                "max_iter": self._max_iter,
                "colormap": self._colormap
            }
            
            self._config_manager.set_module_config(self._name, config)
    
    @jit(nopython=True)
    def _mandelbrot(self, h: int, w: int, max_iter: int, center: complex, zoom: float) -> np.ndarray:
        """Berechnet das Mandelbrot-Set.
        
        Args:
            h: Höhe des Bildes
            w: Breite des Bildes
            max_iter: Maximale Anzahl an Iterationen
            center: Zentrum des Ausschnitts
            zoom: Zoom-Faktor
            
        Returns:
            np.ndarray: Berechnetes Mandelbrot-Set
        """
        y, x = np.ogrid[1.4/zoom:-1.4/zoom:h*1j, -2/zoom:0.8/zoom:w*1j]
        c = x + y*1j + center
        z = c.copy()
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def _render_fractal(self) -> None:
        """Rendert das Fraktal."""
        try:
            # Fraktal berechnen
            data = self._mandelbrot(self._resolution, self._resolution, 
                                   self._max_iter, self._center, self._zoom)
            
            # Bild aktualisieren oder neu erstellen
            if self._img is None:
                self._img = self._ax.imshow(data, cmap=self._colormap, 
                                          extent=self._get_extent())
                self._ax.set_title(f"Mandelbrot-Set - Zoom: {self._zoom:.2e}")
            else:
                self._img.set_data(data)
                self._img.set_extent(self._get_extent())
                self._ax.set_title(f"Mandelbrot-Set - Zoom: {self._zoom:.2e}")
            
            # Figur aktualisieren
            self._fig.canvas.draw_idle()
            
            # Event senden, dass das Fraktal aktualisiert wurde
            if self._event_system:
                self._event_system.emit_event("fractal_updated", {
                    "center": self._center,
                    "zoom": self._zoom,
                    "timestamp": time.time()
                })
        except Exception as e:
            print(f"Fehler beim Rendern des Fraktals: {str(e)}")
    
    def _get_extent(self) -> Tuple[float, float, float, float]:
        """Gibt den Darstellungsbereich für imshow zurück.
        
        Returns:
            Tuple[float, float, float, float]: Darstellungsbereich (links, rechts, unten, oben)
        """
        return (-2/self._zoom + self._center.real, 
                0.8/self._zoom + self._center.real, 
                -1.4/self._zoom + self._center.imag, 
                1.4/self._zoom + self._center.imag)
    
    def _on_sensor_data_updated(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Event-Handler für aktualisierte Sensordaten.
        
        Args:
            event_type: Typ des Events
            event_data: Event-Daten
        """
        # Sensordaten extrahieren
        accel_x = event_data.get("accel_x", 0)
        accel_y = event_data.get("accel_y", 0)
        accel_z = event_data.get("accel_z", 0)
        gyro_x = event_data.get("gyro_x", 0)
        gyro_y = event_data.get("gyro_y", 0)
        
        # Fraktalparameter basierend auf Sensordaten aktualisieren
        # Zentrum basierend auf Gyroskop verschieben
        self._center += complex(gyro_x * 0.01, gyro_y * 0.01)
        
        # Zoom basierend auf Beschleunigung anpassen
        self._zoom *= (1 + accel_z * 0.05)
        self._zoom = max(0.5, min(100, self._zoom))
        
        # Fraktal neu rendern
        self._render_fractal()
    
    def _on_zoom_in(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Event-Handler für Zoom-In.
        
        Args:
            event_type: Typ des Events
            event_data: Event-Daten
        """
        # Zoom-Faktor verdoppeln
        self._zoom *= 2
        
        # Fraktal neu rendern
        self._render_fractal()
    
    def _on_zoom_out(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Event-Handler für Zoom-Out.
        
        Args:
            event_type: Typ des Events
            event_data: Event-Daten
        """
        # Zoom-Faktor halbieren
        self._zoom /= 2
        
        # Fraktal neu rendern
        self._render_fractal()
    
    def _on_move(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Event-Handler für Bewegung.
        
        Args:
            event_type: Typ des Events
            event_data: Event-Daten
        """
        # Bewegungsrichtung extrahieren
        dx = event_data.get("dx", 0)
        dy = event_data.get("dy", 0)
        
        # Zentrum verschieben
        self._center += complex(dx / self._zoom, dy / self._zoom)
        
        # Fraktal neu rendern
        self._render_fractal()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Eingabedaten und gibt Ergebnisse zurück.
        
        Args:
            input_data: Eingabedaten für die Verarbeitung
            
        Returns:
            Dict[str, Any]: Ergebnisse der Verarbeitung
        """
        # Verarbeite Eingabedaten
        if "center" in input_data:
            self._center = input_data["center"]
        
        if "zoom" in input_data:
            self._zoom = input_data["zoom"]
        
        if "resolution" in input_data:
            self._resolution = input_data["resolution"]
        
        if "max_iter" in input_data:
            self._max_iter = input_data["max_iter"]
        
        if "colormap" in input_data:
            self._colormap = input_data["colormap"]
        
        # Fraktal neu rendern
        self._render_fractal()
        
        # Ergebnisse zurückgeben
        return {
            "center": self._center,
            "zoom": self._zoom,
            "resolution": self._resolution,
            "max_iter": self._max_iter,
            "colormap": self._colormap,
            "extent": self._get_extent()
        }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """Gibt UI-Komponenten des Moduls zurück.
        
        Returns:
            Dict[str, Any]: UI-Komponenten des Moduls
        """
        # In einer realen Anwendung würden hier UI-Komponenten zurückgegeben werden
        # Für dieses Beispiel geben wir nur die Figur zurück
        return {
            "figure": self._fig,
            "controls": {
                "zoom_in": {
                    "type": "button",
                    "label": "Zoom In",
                    "event": "ui_zoom_in"
                },
                "zoom_out": {
                    "type": "button",
                    "label": "Zoom Out",
                    "event": "ui_zoom_out"
                },
                "colormap": {
                    "type": "dropdown",
                    "label": "Farbschema",
                    "options": ["viridis", "plasma", "inferno", "magma", "cividis"],
                    "value": self._colormap,
                    "event": "ui_change_colormap"
                }
            }
        }
    
    def cleanup(self) -> None:
        """Bereinigt Ressourcen des Moduls."""
        # Konfiguration speichern
        self._save_config()
        
        # Event-Handler entfernen
        if self._event_system:
            self._event_system.unregister_handler("sensor_data_updated", self._on_sensor_data_updated)
            self._event_system.unregister_handler("ui_zoom_in", self._on_zoom_in)
            self._event_system.unregister_handler("ui_zoom_out", self._on_zoom_out)
            self._event_system.unregister_handler("ui_move", self._on_move)
        
        # Matplotlib-Figur schließen
        if self._fig:
            plt.close(self._fig)
    
    @property
    def name(self) -> str:
        """Gibt den Namen des Moduls zurück."""
        return self._name
    
    @property
    def version(self) -> str:
        """Gibt die Version des Moduls zurück."""
        return self._version
    
    @property
    def description(self) -> str:
        """Gibt die Beschreibung des Moduls zurück."""
        return self._description
    
    @property
    def dependencies(self) -> List[str]:
        """Gibt die Abhängigkeiten des Moduls zurück."""
        return self._dependencies
