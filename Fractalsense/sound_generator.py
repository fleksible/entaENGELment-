"""
FractalSense EntaENGELment - Erweitertes Soundmodul für ResonanceEnhancer

Dieses Modul erweitert die Soundfunktionalität des ResonanceEnhancer-Moduls mit komplexeren Klangstrukturen.
"""

import numpy as np
import pygame
import threading
import time
from typing import Dict, List, Any, Tuple, Optional

class SoundGenerator:
    """Klasse zur Erzeugung komplexer Klänge für das ResonanceEnhancer-Modul."""
    
    def __init__(self, sample_rate: int = 44100):
        """Initialisiert den SoundGenerator.
        
        Args:
            sample_rate: Abtastrate in Hz
        """
        self.sample_rate = sample_rate
        self.is_playing = False
        self.current_thread = None
    
    def generate_sine_wave(self, frequency: float, duration: float, amplitude: float = 1.0) -> np.ndarray:
        """Generiert eine Sinuswelle.
        
        Args:
            frequency: Frequenz in Hz
            duration: Dauer in Sekunden
            amplitude: Amplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        return wave
    
    def generate_harmonic_wave(self, base_frequency: float, duration: float, 
                              harmonics: List[Tuple[int, float]] = None, 
                              amplitude: float = 1.0) -> np.ndarray:
        """Generiert eine Welle mit Obertönen.
        
        Args:
            base_frequency: Grundfrequenz in Hz
            duration: Dauer in Sekunden
            harmonics: Liste von Tupeln (Multiplikator, relative Amplitude) für Obertöne
            amplitude: Gesamtamplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        if harmonics is None:
            # Standardmäßig erste 5 Obertöne mit abnehmender Amplitude
            harmonics = [(1, 1.0), (2, 0.5), (3, 0.33), (4, 0.25), (5, 0.2)]
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave = np.zeros_like(t)
        
        # Grundton und Obertöne addieren
        for harmonic, rel_amp in harmonics:
            wave += rel_amp * np.sin(2 * np.pi * base_frequency * harmonic * t)
        
        # Normalisieren und Amplitude anwenden
        wave = wave / np.max(np.abs(wave)) * amplitude
        
        return wave
    
    def generate_fm_wave(self, carrier_freq: float, modulator_freq: float, 
                        modulation_index: float, duration: float, 
                        amplitude: float = 1.0) -> np.ndarray:
        """Generiert eine frequenzmodulierte Welle.
        
        Args:
            carrier_freq: Trägerfrequenz in Hz
            modulator_freq: Modulatorfrequenz in Hz
            modulation_index: Modulationsindex (Stärke der Modulation)
            duration: Dauer in Sekunden
            amplitude: Amplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        # Frequenzmodulation: carrier + sin(modulator * t) * modulation_index
        wave = amplitude * np.sin(2 * np.pi * carrier_freq * t + 
                                 modulation_index * np.sin(2 * np.pi * modulator_freq * t))
        return wave
    
    def generate_resonant_wave(self, base_frequency: float, resonance_factor: float, 
                              duration: float, amplitude: float = 1.0) -> np.ndarray:
        """Generiert eine resonante Wellenform basierend auf dem goldenen Schnitt.
        
        Args:
            base_frequency: Grundfrequenz in Hz
            resonance_factor: Resonanzfaktor (0.0 bis 1.0)
            duration: Dauer in Sekunden
            amplitude: Amplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        phi = (1 + np.sqrt(5)) / 2  # Goldener Schnitt
        
        # Frequenzen basierend auf dem goldenen Schnitt
        frequencies = [
            base_frequency,
            base_frequency * phi,
            base_frequency * phi**2 % (base_frequency * 2),  # Moduliert, um im hörbaren Bereich zu bleiben
            base_frequency / phi
        ]
        
        # Relative Amplituden
        amplitudes = [
            1.0,
            0.618 * resonance_factor,  # phi - 1
            0.382 * resonance_factor,  # 1 - (phi - 1)
            0.5 * resonance_factor
        ]
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave = np.zeros_like(t)
        
        # Frequenzen mischen
        for freq, amp in zip(frequencies, amplitudes):
            wave += amp * np.sin(2 * np.pi * freq * t)
        
        # Normalisieren und Amplitude anwenden
        wave = wave / np.max(np.abs(wave)) * amplitude
        
        return wave
    
    def generate_fractal_wave(self, base_frequency: float, fractal_dimension: float, 
                             iterations: int, duration: float, 
                             amplitude: float = 1.0) -> np.ndarray:
        """Generiert eine fraktale Wellenform.
        
        Args:
            base_frequency: Grundfrequenz in Hz
            fractal_dimension: Fraktale Dimension (1.0 bis 2.0)
            iterations: Anzahl der Iterationen
            duration: Dauer in Sekunden
            amplitude: Amplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave = np.zeros_like(t)
        
        # Fraktale Wellenform durch rekursive Addition von Sinuswellen
        for i in range(1, iterations + 1):
            # Frequenz und Amplitude basierend auf fraktaler Dimension
            freq = base_frequency * i
            amp = amplitude * (1.0 / i**fractal_dimension)
            
            wave += amp * np.sin(2 * np.pi * freq * t)
        
        # Normalisieren
        wave = wave / np.max(np.abs(wave))
        
        return wave
    
    def apply_envelope(self, wave: np.ndarray, attack: float, decay: float, 
                      sustain: float, release: float) -> np.ndarray:
        """Wendet eine ADSR-Hüllkurve auf eine Wellenform an.
        
        Args:
            wave: Wellenform
            attack: Anstiegszeit in Sekunden
            decay: Abfallzeit in Sekunden
            sustain: Haltepegel (0.0 bis 1.0)
            release: Ausklingzeit in Sekunden
            
        Returns:
            np.ndarray: Wellenform mit angewendeter Hüllkurve
        """
        samples = len(wave)
        envelope = np.ones(samples)
        
        # Umrechnung von Sekunden in Samples
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        # Gesamtdauer der Hüllkurve berechnen
        total_env_samples = attack_samples + decay_samples + release_samples
        
        # Sicherstellen, dass die Hüllkurve nicht länger als die Wellenform ist
        if total_env_samples > samples:
            scale = samples / total_env_samples
            attack_samples = int(attack_samples * scale)
            decay_samples = int(decay_samples * scale)
            release_samples = int(release_samples * scale)
        
        # Sustain-Samples berechnen
        sustain_samples = samples - attack_samples - decay_samples - release_samples
        
        # Hüllkurve erstellen
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        if decay_samples > 0:
            envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain, decay_samples)
        
        if sustain_samples > 0:
            envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain
        
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
        
        # Hüllkurve anwenden
        return wave * envelope
    
    def apply_filter(self, wave: np.ndarray, filter_type: str, cutoff_freq: float, 
                    resonance: float = 1.0) -> np.ndarray:
        """Wendet einen einfachen Filter auf eine Wellenform an.
        
        Args:
            wave: Wellenform
            filter_type: Filtertyp ('lowpass', 'highpass', 'bandpass')
            cutoff_freq: Grenzfrequenz in Hz
            resonance: Resonanz (Q-Faktor)
            
        Returns:
            np.ndarray: Gefilterte Wellenform
        """
        # Einfache Implementierung eines IIR-Filters
        # In einer vollständigen Implementierung würde hier ein komplexerer Filter verwendet werden
        
        # Normalisierte Grenzfrequenz
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        
        # Filterkoeffizienten
        alpha = np.sin(omega) / (2 * resonance)
        
        if filter_type == 'lowpass':
            b0 = (1 - np.cos(omega)) / 2
            b1 = 1 - np.cos(omega)
            b2 = (1 - np.cos(omega)) / 2
            a0 = 1 + alpha
            a1 = -2 * np.cos(omega)
            a2 = 1 - alpha
        elif filter_type == 'highpass':
            b0 = (1 + np.cos(omega)) / 2
            b1 = -(1 + np.cos(omega))
            b2 = (1 + np.cos(omega)) / 2
            a0 = 1 + alpha
            a1 = -2 * np.cos(omega)
            a2 = 1 - alpha
        elif filter_type == 'bandpass':
            b0 = alpha
            b1 = 0
            b2 = -alpha
            a0 = 1 + alpha
            a1 = -2 * np.cos(omega)
            a2 = 1 - alpha
        else:
            # Bei unbekanntem Filtertyp Wellenform unverändert zurückgeben
            return wave
        
        # Normalisieren
        b0 /= a0
        b1 /= a0
        b2 /= a0
        a1 /= a0
        a2 /= a0
        
        # Filter anwenden
        filtered_wave = np.zeros_like(wave)
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        for i in range(len(wave)):
            x0 = wave[i]
            y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            
            filtered_wave[i] = y0
            
            # Verzögerungselemente aktualisieren
            x2, x1 = x1, x0
            y2, y1 = y1, y0
        
        return filtered_wave
    
    def generate_chord(self, base_frequency: float, chord_type: str, 
                      duration: float, amplitude: float = 1.0) -> np.ndarray:
        """Generiert einen Akkord.
        
        Args:
            base_frequency: Grundfrequenz in Hz
            chord_type: Akkordtyp ('major', 'minor', 'diminished', 'augmented', 'sus4', etc.)
            duration: Dauer in Sekunden
            amplitude: Amplitude (0.0 bis 1.0)
            
        Returns:
            np.ndarray: Generierte Wellenform
        """
        # Intervalle für verschiedene Akkordtypen
        intervals = {
            'major': [1, 1.25, 1.5],  # 1, 3, 5
            'minor': [1, 1.2, 1.5],   # 1, b3, 5
            'diminished': [1, 1.2, 1.4],  # 1, b3, b5
            'augmented': [1, 1.25, 1.6],  # 1, 3, #5
            'sus4': [1, 1.33, 1.5],   # 1, 4, 5
            'sus2': [1, 1.125, 1.5],  # 1, 2, 5
            'major7': [1, 1.25, 1.5, 1.875],  # 1, 3, 5, 7
            'minor7': [1, 1.2, 1.5, 1.8],     # 1, b3, 5, b7
            'dominant7': [1, 1.25, 1.5, 1.8]  # 1, 3, 5, b7
        }
        
        # Standardmäßig Dur-Akkord verwenden
        if chord_type not in intervals:
            chord_type = 'major'
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        wave = np.zeros_like(t)
        
        # Töne des Akkords addieren
        for interval in intervals[chord_type]:
            freq = base_frequency * interval
            wave += np.sin(2 * np.pi * freq * t)
        
        # Normalisieren und Amplitude anwenden
        wave = wave / np.max(np.abs(wave)) * amplitude
        
        return wave
    
    def play_sound(self, wave: np.ndarray) -> None:
        """Spielt eine Wellenform ab.
        
        Args:
            wave: Abzuspielende Wellenform
        """
        if self.is_playing:
            return
        
        self.is_playing = True
        
        # In 16-bit PCM konvertieren
        wave_int16 = (wave * 32767).astype(np.int16)
        
        # Sound erstellen und abspielen
        try:
            sound = pygame.mixer.Sound(buffer=wave_int16)
            sound.play()
            
            # Warten, bis der Sound abgespielt ist
            duration = len(wave) / self.sample_rate
            time.sleep(duration + 0.1)
            
        except Exception as e:
            print(f"Fehler beim Abspielen des Sounds: {str(e)}")
        
        self.is_playing = False
    
    def play_sound_async(self, wave: np.ndarray) -> None:
        """Spielt eine Wellenform asynchron ab.
        
        Args:
            wave: Abzuspielende Wellenform
        """
        if self.is_playing:
            return
        
        # Sound in separatem Thread abspielen
        self.current_thread = threading.Thread(target=self.play_sound, args=(wave,))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def stop_sound(self) -> None:
        """Stoppt den aktuell abgespielten Sound."""
        pygame.mixer.stop()
        self.is_playing = False
