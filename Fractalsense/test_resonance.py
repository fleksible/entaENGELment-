"""
FractalSense EntaENGELment - Test-Skript für das ResonanceEnhancer-Modul

Dieses Skript testet die Funktionalität des ResonanceEnhancer-Moduls.
"""

import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import threading
import pygame

# Füge das Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importiere das modulare Framework
from modular_app_structure import ModuleInterface, EventSystem, ConfigManager

# Importiere die Module
from modules.resonance_enhancer import ResonanceEnhancerModule
from modules.resonance_enhancer.sound_generator import SoundGenerator
from modules.resonance_enhancer.color_generator import ColorGenerator

class TestApp:
    """Test-Anwendung für das ResonanceEnhancer-Modul."""
    
    def __init__(self):
        """Initialisiert die Test-Anwendung."""
        # Event-System erstellen
        self.event_system = EventSystem()
        
        # Konfigurationsmanager erstellen
        self.config_manager = ConfigManager("test_config.json")
        
        # App-Kontext erstellen
        self.app_context = {
            "event_system": self.event_system,
            "config_manager": self.config_manager
        }
        
        # ResonanceEnhancer-Modul erstellen
        self.resonance_enhancer = ResonanceEnhancerModule()
        
        # Sound-Generator erstellen
        self.sound_generator = SoundGenerator()
        
        # Color-Generator erstellen
        self.color_generator = ColorGenerator()
        
        # Tkinter-Fenster erstellen
        self.root = tk.Tk()
        self.root.title("ResonanceEnhancer Test")
        self.root.geometry("1000x800")
        
        # Hauptframe erstellen
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Linke Seite für Steuerelemente
        self.left_frame = ttk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Rechte Seite für Visualisierung
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Steuerelemente-Frame
        self.controls_frame = ttk.LabelFrame(self.left_frame, text="Steuerelemente")
        self.controls_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Statusleiste
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="Bereit")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Visualisierungsbereich
        self.canvas_frame = ttk.Frame(self.right_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Matplotlib-Figur erstellen
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Event-Handler registrieren
        self.event_system.register_handler("colormap_updated", self.on_colormap_updated)
        self.event_system.register_handler("generate_fractal_sound", self.on_generate_fractal_sound)
        self.event_system.register_handler("update_resonance_parameters", self.on_update_resonance_parameters)
        
        # Steuerelemente erstellen
        self.create_controls()
        
        # Beim Schließen des Fensters aufräumen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_controls(self):
        """Erstellt die Steuerelemente."""
        # Sound-Steuerelemente
        sound_frame = ttk.LabelFrame(self.controls_frame, text="Sound")
        sound_frame.pack(fill=tk.X, pady=5)
        
        # Audio aktivieren/deaktivieren
        audio_frame = ttk.Frame(sound_frame)
        audio_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(audio_frame, text="Audio:").pack(side=tk.LEFT)
        
        self.audio_var = tk.StringVar(value="Ein")
        audio_combo = ttk.Combobox(audio_frame, textvariable=self.audio_var, values=["Ein", "Aus"])
        audio_combo.pack(side=tk.RIGHT)
        audio_combo.bind("<<ComboboxSelected>>", self.on_audio_changed)
        
        # Lautstärke
        volume_frame = ttk.Frame(sound_frame)
        volume_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(volume_frame, text="Lautstärke:").pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=0.5)
        volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, variable=self.volume_var, orient=tk.HORIZONTAL)
        volume_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        volume_scale.bind("<ButtonRelease-1>", self.on_volume_changed)
        
        # Testton-Button
        test_sound_button = ttk.Button(sound_frame, text="Testton abspielen", command=self.on_test_sound)
        test_sound_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Farb-Steuerelemente
        color_frame = ttk.LabelFrame(self.controls_frame, text="Farbe")
        color_frame.pack(fill=tk.X, pady=5)
        
        # Farbmodus
        color_mode_frame = ttk.Frame(color_frame)
        color_mode_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(color_mode_frame, text="Farbmodus:").pack(side=tk.LEFT)
        
        self.color_mode_var = tk.StringVar(value="resonant")
        color_mode_combo = ttk.Combobox(color_mode_frame, textvariable=self.color_mode_var, 
                                       values=["resonant", "harmonic", "spectral", "fractal", "mereotopological"])
        color_mode_combo.pack(side=tk.RIGHT)
        color_mode_combo.bind("<<ComboboxSelected>>", self.on_color_mode_changed)
        
        # Farbkarte anzeigen Button
        show_colormap_button = ttk.Button(color_frame, text="Farbkarte anzeigen", command=self.on_show_colormap)
        show_colormap_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Sensor-Simulation-Steuerelemente
        sensor_frame = ttk.LabelFrame(self.controls_frame, text="Sensor-Simulation")
        sensor_frame.pack(fill=tk.X, pady=5)
        
        # Beschleunigung X
        accel_x_frame = ttk.Frame(sensor_frame)
        accel_x_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(accel_x_frame, text="Beschl. X:").pack(side=tk.LEFT)
        
        self.accel_x_var = tk.DoubleVar(value=0.0)
        accel_x_scale = ttk.Scale(accel_x_frame, from_=-2.0, to=2.0, variable=self.accel_x_var, orient=tk.HORIZONTAL)
        accel_x_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        accel_x_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Beschleunigung Y
        accel_y_frame = ttk.Frame(sensor_frame)
        accel_y_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(accel_y_frame, text="Beschl. Y:").pack(side=tk.LEFT)
        
        self.accel_y_var = tk.DoubleVar(value=0.0)
        accel_y_scale = ttk.Scale(accel_y_frame, from_=-2.0, to=2.0, variable=self.accel_y_var, orient=tk.HORIZONTAL)
        accel_y_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        accel_y_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Beschleunigung Z
        accel_z_frame = ttk.Frame(sensor_frame)
        accel_z_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(accel_z_frame, text="Beschl. Z:").pack(side=tk.LEFT)
        
        self.accel_z_var = tk.DoubleVar(value=0.0)
        accel_z_scale = ttk.Scale(accel_z_frame, from_=-2.0, to=2.0, variable=self.accel_z_var, orient=tk.HORIZONTAL)
        accel_z_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        accel_z_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Gyroskop X
        gyro_x_frame = ttk.Frame(sensor_frame)
        gyro_x_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(gyro_x_frame, text="Gyro X:").pack(side=tk.LEFT)
        
        self.gyro_x_var = tk.DoubleVar(value=0.0)
        gyro_x_scale = ttk.Scale(gyro_x_frame, from_=-2.0, to=2.0, variable=self.gyro_x_var, orient=tk.HORIZONTAL)
        gyro_x_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        gyro_x_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Gyroskop Y
        gyro_y_frame = ttk.Frame(sensor_frame)
        gyro_y_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(gyro_y_frame, text="Gyro Y:").pack(side=tk.LEFT)
        
        self.gyro_y_var = tk.DoubleVar(value=0.0)
        gyro_y_scale = ttk.Scale(gyro_y_frame, from_=-2.0, to=2.0, variable=self.gyro_y_var, orient=tk.HORIZONTAL)
        gyro_y_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        gyro_y_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Gyroskop Z
        gyro_z_frame = ttk.Frame(sensor_frame)
        gyro_z_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(gyro_z_frame, text="Gyro Z:").pack(side=tk.LEFT)
        
        self.gyro_z_var = tk.DoubleVar(value=0.0)
        gyro_z_scale = ttk.Scale(gyro_z_frame, from_=-2.0, to=2.0, variable=self.gyro_z_var, orient=tk.HORIZONTAL)
        gyro_z_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        gyro_z_scale.bind("<ButtonRelease-1>", self.on_sensor_changed)
        
        # Sensordaten senden Button
        send_sensor_button = ttk.Button(sensor_frame, text="Sensordaten senden", command=self.on_send_sensor_data)
        send_sensor_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Fraktal-Simulation-Steuerelemente
        fractal_frame = ttk.LabelFrame(self.controls_frame, text="Fraktal-Simulation")
        fractal_frame.pack(fill=tk.X, pady=5)
        
        # Zoom
        zoom_frame = ttk.Frame(fractal_frame)
        zoom_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)
        
        self.zoom_var = tk.DoubleVar(value=1.0)
        zoom_scale = ttk.Scale(zoom_frame, from_=0.5, to=10.0, variable=self.zoom_var, orient=tk.HORIZONTAL)
        zoom_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        zoom_scale.bind("<ButtonRelease-1>", self.on_fractal_changed)
        
        # Center Real
        center_real_frame = ttk.Frame(fractal_frame)
        center_real_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(center_real_frame, text="Center Real:").pack(side=tk.LEFT)
        
        self.center_real_var = tk.DoubleVar(value=-0.75)
        center_real_scale = ttk.Scale(center_real_frame, from_=-2.0, to=0.5, variable=self.center_real_var, orient=tk.HORIZONTAL)
        center_real_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        center_real_scale.bind("<ButtonRelease-1>", self.on_fractal_changed)
        
        # Center Imag
        center_imag_frame = ttk.Frame(fractal_frame)
        center_imag_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(center_imag_frame, text="Center Imag:").pack(side=tk.LEFT)
        
        self.center_imag_var = tk.DoubleVar(value=0.0)
        center_imag_scale = ttk.Scale(center_imag_frame, from_=-1.0, to=1.0, variable=self.center_imag_var, orient=tk.HORIZONTAL)
        center_imag_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        center_imag_scale.bind("<ButtonRelease-1>", self.on_fractal_changed)
        
        # Fraktaldaten senden Button
        send_fractal_button = ttk.Button(fractal_frame, text="Fraktaldaten senden", command=self.on_send_fractal_data)
        send_fractal_button.pack(fill=tk.X, padx=5, pady=5)
    
    def on_audio_changed(self, event):
        """Event-Handler für Änderungen am Audio-Status."""
        audio_enabled = self.audio_var.get() == "Ein"
        self.event_system.emit_event("ui_update_resonance_enhancer_audio_enabled", {
            "audio_enabled": audio_enabled
        })
        self.status_label.config(text=f"Audio {'aktiviert' if audio_enabled else 'deaktiviert'}")
    
    def on_volume_changed(self, event):
        """Event-Handler für Änderungen an der Lautstärke."""
        volume = self.volume_var.get()
        self.event_system.emit_event("ui_update_resonance_enhancer_volume", {
            "volume": volume
        })
        self.status_label.config(text=f"Lautstärke auf {volume:.2f} gesetzt")
    
    def on_test_sound(self):
        """Event-Handler für den Testton-Button."""
        # Erzeuge einen Testton mit dem SoundGenerator
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=1024)
        
        # Erzeuge verschiedene Testtöne je nach ausgewähltem Modus
        if hasattr(self, 'test_sound_mode'):
            self.test_sound_mode = (self.test_sound_mode + 1) % 5
        else:
            self.test_sound_mode = 0
        
        volume = self.volume_var.get()
        
        if self.test_sound_mode == 0:
            # Einfacher Sinuston
            wave = self.sound_generator.generate_sine_wave(440.0, 1.0, volume)
            sound_type = "Sinuston"
        elif self.test_sound_mode == 1:
            # Harmonischer Klang
            wave = self.sound_generator.generate_harmonic_wave(440.0, 1.0, amplitude=volume)
            sound_type = "Harmonischer Klang"
        elif self.test_sound_mode == 2:
            # FM-Synthese
            wave = self.sound_generator.generate_fm_wave(440.0, 110.0, 2.0, 1.0, volume)
            sound_type = "FM-Synthese"
        elif self.test_sound_mode == 3:
            # Resonanter Klang
            wave = self.sound_generator.generate_resonant_wave(440.0, 0.8, 1.0, volume)
            sound_type = "Resonanter Klang"
        else:
            # Fraktaler Klang
            wave = self.sound_generator.generate_fractal_wave(440.0, 1.5, 5, 1.0, volume)
            sound_type = "Fraktaler Klang"
        
        # Hüllkurve anwenden
        wave = self.sound_generator.apply_envelope(wave, 0.1, 0.2, 0.7, 0.3)
        
        # Abspielen
        self.sound_generator.play_sound_async(wave)
        
        self.status_label.config(text=f"Testton ({sound_type}) abgespielt")
    
    def on_color_mode_changed(self, event):
        """Event-Handler für Änderungen am Farbmodus."""
        color_mode = self.color_mode_var.get()
        self.event_system.emit_event("ui_update_resonance_enhancer_color_mode", {
            "color_mode": color_mode
        })
        self.status_label.config(text=f"Farbmodus auf '{color_mode}' gesetzt")
        
        # Farbkarte sofort anzeigen
        self.on_show_colormap()
    
    def on_show_colormap(self):
        """Event-Handler für den Farbkarte-anzeigen-Button."""
        color_mode = self.color_mode_var.get()
        
        # Achse leeren
        self.ax.clear()
        
        # Farbkarte abrufen
        cmap = self.color_generator.get_colormap(color_mode)
        if cmap is None:
            cmap = plt.get_cmap(color_mode)
        
        # Farbkarte anzeigen
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        
        self.ax.imshow(gradient, aspect='auto', cmap=cmap)
        self.ax.set_title(f"Farbkarte: {color_mode}")
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        
        # Canvas aktualisieren
        self.canvas.draw()
        
        self.status_label.config(text=f"Farbkarte '{color_mode}' angezeigt")
    
    def on_sensor_changed(self, event):
        """Event-Handler für Änderungen an den Sensordaten."""
        # Sensordaten werden erst beim Klicken auf den Button gesendet
        pass
    
    def on_send_sensor_data(self):
        """Event-Handler für den Sensordaten-senden-Button."""
        # TODO: Implement sensor data sending
        pass