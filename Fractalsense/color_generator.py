"""
FractalSense EntaENGELment - Erweitertes Farbmodul für ResonanceEnhancer

Dieses Modul erweitert die Farbfunktionalität des ResonanceEnhancer-Moduls mit komplexeren Farbstrukturen.
"""

import colorsys
from typing import Dict, List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def _register_colormap(name: str, cmap) -> None:
    """Register a colormap with matplotlib (compatible with old and new API)."""
    try:
        # New API (matplotlib >= 3.9)
        mpl.colormaps.register(cmap, name=name, force=True)
    except AttributeError:
        # Old API (matplotlib < 3.9)
        plt.register_cmap(name=name, cmap=cmap)


class ColorGenerator:
    """Klasse zur Erzeugung komplexer Farbstrukturen für das ResonanceEnhancer-Modul."""

    def __init__(self):
        """Initialisiert den ColorGenerator."""
        self.custom_colormaps = {}
        self.create_default_colormaps()

    def create_default_colormaps(self) -> None:
        """Erstellt die Standard-Farbkarten."""
        # Resonante Farbkarte (violett zu gold)
        self.create_resonant_colormap()

        # Harmonische Farbkarte (basierend auf Fibonacci-Sequenz)
        self.create_harmonic_colormap()

        # Spektrale Farbkarte (basierend auf Spektralfarben)
        self.create_spectral_colormap()

        # Fraktale Farbkarte (basierend auf Mandelbrot-Iteration)
        self.create_fractal_colormap()

        # Mereotopologische Farbkarte (für Hypergraphen)
        self.create_mereotopological_colormap()

        # Registriere die benutzerdefinierten Farbkarten bei Matplotlib
        for name, cmap in self.custom_colormaps.items():
            _register_colormap(name, cmap)

    def create_resonant_colormap(self) -> None:
        """Erstellt eine resonante Farbkarte (violett zu gold)."""
        resonant_colors = []
        for i in range(256):
            # HSV-Farbverlauf von Violett (270°) zu Gold (45°)
            h = (270 - (i / 255) * 225) / 360  # Normalisiert auf [0, 1]
            s = 0.8
            v = 0.9
            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            resonant_colors.append((r, g, b))

        self.custom_colormaps["resonant"] = LinearSegmentedColormap.from_list(
            "resonant", resonant_colors
        )

    def create_harmonic_colormap(self) -> None:
        """Erstellt eine harmonische Farbkarte (basierend auf Fibonacci-Sequenz)."""
        harmonic_colors = []
        phi = (1 + np.sqrt(5)) / 2  # Goldener Schnitt
        for i in range(256):
            # Verwende den goldenen Schnitt für harmonische Farbverschiebung
            h = (i * phi) % 1.0
            s = 0.7 + 0.3 * np.sin(i * phi * np.pi)
            v = 0.8 + 0.2 * np.cos(i * phi * np.pi)
            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            harmonic_colors.append((r, g, b))

        self.custom_colormaps["harmonic"] = LinearSegmentedColormap.from_list(
            "harmonic", harmonic_colors
        )

    def create_spectral_colormap(self) -> None:
        """Erstellt eine spektrale Farbkarte (basierend auf Spektralfarben)."""
        spectral_colors = []
        for i in range(256):
            # Wellenlänge von 380nm (violett) bis 750nm (rot)
            wavelength = 380 + (750 - 380) * (i / 255)

            # Vereinfachte Umwandlung von Wellenlänge zu RGB
            if 380 <= wavelength < 440:
                r = -(wavelength - 440) / (440 - 380)
                g = 0.0
                b = 1.0
            elif 440 <= wavelength < 490:
                r = 0.0
                g = (wavelength - 440) / (490 - 440)
                b = 1.0
            elif 490 <= wavelength < 510:
                r = 0.0
                g = 1.0
                b = -(wavelength - 510) / (510 - 490)
            elif 510 <= wavelength < 580:
                r = (wavelength - 510) / (580 - 510)
                g = 1.0
                b = 0.0
            elif 580 <= wavelength < 645:
                r = 1.0
                g = -(wavelength - 645) / (645 - 580)
                b = 0.0
            elif 645 <= wavelength <= 750:
                r = 1.0
                g = 0.0
                b = 0.0
            else:
                r, g, b = 0, 0, 0

            # Intensitätsanpassung an den Rändern des sichtbaren Spektrums
            if 380 <= wavelength < 420:
                factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
            elif 420 <= wavelength < 700:
                factor = 1.0
            elif 700 <= wavelength <= 750:
                factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 700)
            else:
                factor = 0.0

            r *= factor
            g *= factor
            b *= factor

            spectral_colors.append((r, g, b))

        self.custom_colormaps["spectral"] = LinearSegmentedColormap.from_list(
            "spectral", spectral_colors
        )

    def create_fractal_colormap(self) -> None:
        """Erstellt eine fraktale Farbkarte (basierend auf Mandelbrot-Iteration)."""
        fractal_colors = []

        # Verwende eine nicht-lineare Verteilung für interessantere Farbübergänge
        for i in range(256):
            # Nicht-lineare Verteilung basierend auf Quadratwurzel
            t = np.sqrt(i / 255)

            # Farbton basierend auf Mandelbrot-ähnlicher Iteration
            h = (0.5 + 0.5 * np.sin(t * 20 * np.pi)) % 1.0

            # Sättigung und Hellwert mit fraktalen Mustern
            s = 0.6 + 0.4 * np.sin(t * 10 * np.pi)
            v = 0.7 + 0.3 * np.cos(t * 15 * np.pi)

            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            fractal_colors.append((r, g, b))

        self.custom_colormaps["fractal"] = LinearSegmentedColormap.from_list(
            "fractal", fractal_colors
        )

    def create_mereotopological_colormap(self) -> None:
        """Erstellt eine mereotopologische Farbkarte (für Hypergraphen)."""
        # Farbkarte für Hypergraphen mit klaren Unterschieden zwischen Knoten und Kanten
        mereotopological_colors = []

        # Erste Hälfte für Knoten (blau bis grün)
        for i in range(128):
            t = i / 127
            h = 0.5 + 0.2 * t  # Blau (0.5) bis Grün (0.7)
            s = 0.7 + 0.3 * t
            v = 0.8
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            mereotopological_colors.append((r, g, b))

        # Zweite Hälfte für Kanten (rot bis violett)
        for i in range(128):
            t = i / 127
            h = 0.95 + 0.15 * t  # Rot (0.95) bis Violett (1.1 % 1 = 0.1)
            s = 0.8 - 0.2 * t
            v = 0.9
            r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
            mereotopological_colors.append((r, g, b))

        self.custom_colormaps["mereotopological"] = LinearSegmentedColormap.from_list(
            "mereotopological", mereotopological_colors
        )

    def create_dynamic_colormap(
        self, base_hsv: Tuple[float, float, float], shift_factor: float, name: str = "dynamic"
    ) -> LinearSegmentedColormap:
        """Erstellt eine dynamische Farbkarte basierend auf HSV-Werten.

        Args:
            base_hsv: Basis-HSV-Werte (Farbton, Sättigung, Hellwert)
            shift_factor: Faktor für die Farbverschiebung
            name: Name der Farbkarte

        Returns:
            LinearSegmentedColormap: Erstellte Farbkarte
        """
        h, s, v = base_hsv

        colors = []
        for i in range(256):
            # Variiere den Farbton leicht über die Farbkarte
            h_i = (h + i * shift_factor / 256) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h_i, s, v)
            colors.append((r, g, b))

        dynamic_cmap = LinearSegmentedColormap.from_list(name, colors)

        # Registriere die Farbkarte bei Matplotlib
        _register_colormap(name, dynamic_cmap)

        return dynamic_cmap

    def create_sensor_based_colormap(
        self, sensor_data: Dict[str, float], fractal_zoom: float, name: str = "sensor_based"
    ) -> LinearSegmentedColormap:
        """Erstellt eine Farbkarte basierend auf Sensordaten und Fraktal-Zoom.

        Args:
            sensor_data: Dictionary mit Sensordaten
            fractal_zoom: Zoom-Faktor des Fraktals
            name: Name der Farbkarte

        Returns:
            LinearSegmentedColormap: Erstellte Farbkarte
        """
        # Extrahiere relevante Sensordaten
        accel_x = sensor_data.get("accel_x", 0)
        accel_y = sensor_data.get("accel_y", 0)
        accel_z = sensor_data.get("accel_z", 0)
        gyro_x = sensor_data.get("gyro_x", 0)
        gyro_y = sensor_data.get("gyro_y", 0)
        gyro_z = sensor_data.get("gyro_z", 0)

        # Berechne Magnitudes
        accel_magnitude = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
        gyro_magnitude = np.sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)

        # Basis-HSV-Werte basierend auf Sensordaten
        h_base = (0.7 + gyro_x * 0.1 + gyro_y * 0.1) % 1.0  # Farbton basierend auf Gyroskop
        s_base = max(
            0.4, min(0.9, 0.6 + accel_magnitude * 0.05)
        )  # Sättigung basierend auf Beschleunigung
        v_base = max(
            0.6, min(0.95, 0.8 + np.log10(max(1.0, fractal_zoom)) * 0.05)
        )  # Hellwert basierend auf Zoom

        colors = []
        for i in range(256):
            # Variiere den Farbton basierend auf Position und Sensordaten
            t = i / 255

            # Farbton mit nicht-linearer Variation
            h = (h_base + t * gyro_magnitude * 0.2) % 1.0

            # Sättigung mit Wellenform basierend auf Beschleunigung
            s = s_base + 0.1 * np.sin(t * 2 * np.pi * (1 + accel_z))
            s = max(0.4, min(1.0, s))

            # Hellwert mit Variation basierend auf Zoom
            v = v_base + 0.1 * np.cos(t * 3 * np.pi * np.log10(max(1.0, fractal_zoom)))
            v = max(0.5, min(1.0, v))

            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            colors.append((r, g, b))

        sensor_cmap = LinearSegmentedColormap.from_list(name, colors)

        # Registriere die Farbkarte bei Matplotlib
        _register_colormap(name, sensor_cmap)

        return sensor_cmap

    def create_resonant_gradient(
        self, base_frequency: float, harmonic_ratio: float, n_colors: int = 256
    ) -> List[Tuple[float, float, float]]:
        """Erstellt einen resonanten Farbverlauf basierend auf Frequenzverhältnissen.

        Args:
            base_frequency: Basisfrequenz
            harmonic_ratio: Harmonisches Verhältnis
            n_colors: Anzahl der Farben

        Returns:
            List[Tuple[float, float, float]]: Liste von RGB-Farben
        """
        colors = []

        for i in range(n_colors):
            t = i / (n_colors - 1)

            # Frequenzverhältnisse für verschiedene Farbkanäle
            freq_r = base_frequency
            freq_g = base_frequency * harmonic_ratio
            freq_b = base_frequency * harmonic_ratio**2

            # Phasenverschiebung für interessantere Muster
            phase_r = 0
            phase_g = np.pi / 3
            phase_b = 2 * np.pi / 3

            # RGB-Werte basierend auf Sinuswellen
            r = 0.5 + 0.5 * np.sin(2 * np.pi * freq_r * t + phase_r)
            g = 0.5 + 0.5 * np.sin(2 * np.pi * freq_g * t + phase_g)
            b = 0.5 + 0.5 * np.sin(2 * np.pi * freq_b * t + phase_b)

            colors.append((r, g, b))

        return colors

    def create_golden_ratio_colormap(
        self, base_hue: float = 0.0, name: str = "golden_ratio"
    ) -> LinearSegmentedColormap:
        """Erstellt eine Farbkarte basierend auf dem goldenen Schnitt.

        Args:
            base_hue: Basis-Farbton (0.0 bis 1.0)
            name: Name der Farbkarte

        Returns:
            LinearSegmentedColormap: Erstellte Farbkarte
        """
        phi = (1 + np.sqrt(5)) / 2  # Goldener Schnitt

        colors = []
        for i in range(256):
            t = i / 255

            # Farbton basierend auf goldenem Schnitt
            h = (base_hue + t * phi) % 1.0

            # Sättigung und Hellwert mit Fibonacci-Verhältnissen
            s = 0.5 + 0.5 * np.sin(t * phi * 2 * np.pi)
            v = 0.5 + 0.5 * np.cos(t * phi * 2 * np.pi)

            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            colors.append((r, g, b))

        golden_cmap = LinearSegmentedColormap.from_list(name, colors)

        # Registriere die Farbkarte bei Matplotlib
        _register_colormap(name, golden_cmap)

        return golden_cmap

    def create_quantum_colormap(
        self, energy_levels: int = 7, name: str = "quantum"
    ) -> LinearSegmentedColormap:
        """Erstellt eine Farbkarte basierend auf Quantenenergie-Niveaus.

        Args:
            energy_levels: Anzahl der Energieniveaus
            name: Name der Farbkarte

        Returns:
            LinearSegmentedColormap: Erstellte Farbkarte
        """
        # Farben für jedes Energieniveau
        level_colors = []

        for level in range(energy_levels):
            # Normalisierter Level
            e = level / (energy_levels - 1)

            # Farbton basierend auf Energieniveau (von Rot bis Violett)
            h = e * 0.8  # 0.0 (rot) bis 0.8 (violett)

            # Sättigung und Hellwert
            s = 0.8
            v = 0.9

            # Umwandlung in RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            level_colors.append((r, g, b))

        # Erstelle Farbkarte mit diskreten Übergängen zwischen Energieniveaus
        colors = []

        for i in range(256):
            # Bestimme das Energieniveau und den Übergang
            t = i / 255 * (energy_levels - 1)
            level = int(t)
            frac = t - level

            # Interpoliere zwischen benachbarten Energieniveaus
            if level < energy_levels - 1:
                r = level_colors[level][0] * (1 - frac) + level_colors[level + 1][0] * frac
                g = level_colors[level][1] * (1 - frac) + level_colors[level + 1][1] * frac
                b = level_colors[level][2] * (1 - frac) + level_colors[level + 1][2] * frac
            else:
                r, g, b = level_colors[-1]

            colors.append((r, g, b))

        quantum_cmap = LinearSegmentedColormap.from_list(name, colors)

        # Registriere die Farbkarte bei Matplotlib
        _register_colormap(name, quantum_cmap)

        return quantum_cmap
