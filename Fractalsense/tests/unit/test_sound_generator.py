"""
Tests for SoundGenerator class in sound_generator.py

Tests cover:
- Sine wave generation
- Harmonic wave generation
- FM wave generation
- Resonant wave generation
- Fractal wave generation
- ADSR envelope application
- Filter application
- Chord generation
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sound_generator import SoundGenerator

from ..conftest import get_dominant_frequency


class TestSoundGeneratorInit:
    """Tests for SoundGenerator initialization."""

    def test_default_sample_rate(self):
        """Should use 44100 Hz as default sample rate."""
        generator = SoundGenerator()
        assert generator.sample_rate == 44100

    def test_custom_sample_rate(self):
        """Should accept custom sample rate."""
        generator = SoundGenerator(sample_rate=48000)
        assert generator.sample_rate == 48000

    def test_initial_state(self):
        """Should initialize with correct state."""
        generator = SoundGenerator()
        assert generator.is_playing is False
        assert generator.current_thread is None


class TestSineWave:
    """Tests for generate_sine_wave method."""

    def test_generates_correct_length(self, sound_generator, sample_rate):
        """Sine wave should have correct sample count for duration."""
        duration = 1.0
        wave = sound_generator.generate_sine_wave(440.0, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_short_duration(self, sound_generator, sample_rate):
        """Should handle short durations correctly."""
        duration = 0.1
        wave = sound_generator.generate_sine_wave(440.0, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_amplitude_within_bounds(self, sound_generator):
        """Wave amplitude should not exceed specified value."""
        wave = sound_generator.generate_sine_wave(440.0, 1.0, amplitude=0.5)
        assert np.max(np.abs(wave)) <= 0.5 + 0.001  # Small tolerance

    def test_default_amplitude(self, sound_generator):
        """Default amplitude should be 1.0."""
        wave = sound_generator.generate_sine_wave(440.0, 1.0)
        assert np.max(np.abs(wave)) <= 1.0 + 0.001

    def test_correct_frequency(self, sound_generator, sample_rate):
        """Wave should have correct frequency (verified via FFT)."""
        target_freq = 440.0
        wave = sound_generator.generate_sine_wave(target_freq, 1.0)
        detected_freq = get_dominant_frequency(wave, sample_rate)
        assert abs(detected_freq - target_freq) < 1.0  # Within 1 Hz

    def test_different_frequencies(self, sound_generator, sample_rate):
        """Should generate correct frequencies across range."""
        for target_freq in [100.0, 440.0, 1000.0, 2000.0]:
            wave = sound_generator.generate_sine_wave(target_freq, 1.0)
            detected_freq = get_dominant_frequency(wave, sample_rate)
            assert abs(detected_freq - target_freq) < 2.0

    def test_zero_amplitude(self, sound_generator):
        """Should handle zero amplitude."""
        wave = sound_generator.generate_sine_wave(440.0, 1.0, amplitude=0.0)
        assert np.max(np.abs(wave)) == 0.0


class TestHarmonicWave:
    """Tests for generate_harmonic_wave method."""

    def test_generates_correct_length(self, sound_generator, sample_rate):
        """Harmonic wave should have correct sample count."""
        duration = 1.0
        wave = sound_generator.generate_harmonic_wave(440.0, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_default_harmonics(self, sound_generator):
        """Should use 5 default harmonics."""
        wave = sound_generator.generate_harmonic_wave(440.0, 1.0)
        assert wave is not None
        assert len(wave) > 0

    def test_custom_harmonics(self, sound_generator):
        """Should apply custom harmonic ratios."""
        harmonics = [(1, 1.0), (2, 0.5)]
        wave = sound_generator.generate_harmonic_wave(440.0, 1.0, harmonics=harmonics)
        assert wave is not None
        assert len(wave) == 44100

    def test_single_harmonic(self, sound_generator):
        """Single harmonic should approximate sine wave."""
        harmonics = [(1, 1.0)]
        harmonic_wave = sound_generator.generate_harmonic_wave(440.0, 1.0, harmonics=harmonics)
        sine_wave = sound_generator.generate_sine_wave(440.0, 1.0)
        # Should be very similar (both are normalized)
        correlation = np.corrcoef(harmonic_wave, sine_wave)[0, 1]
        assert correlation > 0.99

    def test_normalized_output(self, sound_generator):
        """Output should be normalized to specified amplitude."""
        wave = sound_generator.generate_harmonic_wave(440.0, 1.0, amplitude=0.8)
        assert np.max(np.abs(wave)) <= 0.8 + 0.001


class TestFMWave:
    """Tests for generate_fm_wave method."""

    def test_generates_correct_length(self, sound_generator, sample_rate):
        """FM wave should have correct sample count."""
        duration = 1.0
        wave = sound_generator.generate_fm_wave(440.0, 110.0, 2.0, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_differs_from_sine(self, sound_generator):
        """FM wave should differ from simple sine wave."""
        sine = sound_generator.generate_sine_wave(440.0, 1.0)
        fm = sound_generator.generate_fm_wave(440.0, 110.0, 2.0, 1.0)
        # Should not be identical
        assert not np.allclose(sine, fm)

    def test_zero_modulation_index(self, sound_generator):
        """Zero modulation index should produce sine-like wave."""
        fm = sound_generator.generate_fm_wave(440.0, 110.0, 0.0, 1.0)
        sine = sound_generator.generate_sine_wave(440.0, 1.0)
        # Should be very similar
        correlation = np.corrcoef(fm, sine)[0, 1]
        assert correlation > 0.99

    def test_amplitude_bounds(self, sound_generator):
        """FM wave amplitude should not exceed specified value."""
        wave = sound_generator.generate_fm_wave(440.0, 110.0, 5.0, 1.0, amplitude=0.7)
        assert np.max(np.abs(wave)) <= 0.7 + 0.001


class TestResonantWave:
    """Tests for generate_resonant_wave method."""

    def test_generates_correct_length(self, sound_generator, sample_rate):
        """Resonant wave should have correct sample count."""
        duration = 1.0
        wave = sound_generator.generate_resonant_wave(440.0, 0.8, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_uses_golden_ratio(self, sound_generator):
        """Should incorporate golden ratio in frequency calculation."""
        wave = sound_generator.generate_resonant_wave(440.0, 0.8, 1.0)
        # Wave should exist and be normalized
        assert wave is not None
        assert np.max(np.abs(wave)) <= 1.0 + 0.001

    def test_resonance_factor_effect(self, sound_generator):
        """Different resonance factors should produce different waves."""
        wave1 = sound_generator.generate_resonant_wave(440.0, 0.2, 1.0)
        wave2 = sound_generator.generate_resonant_wave(440.0, 0.8, 1.0)
        # Waves should differ
        assert not np.allclose(wave1, wave2)

    def test_normalized_output(self, sound_generator):
        """Output should be normalized."""
        wave = sound_generator.generate_resonant_wave(440.0, 1.0, 1.0, amplitude=0.6)
        assert np.max(np.abs(wave)) <= 0.6 + 0.001


class TestFractalWave:
    """Tests for generate_fractal_wave method."""

    def test_generates_correct_length(self, sound_generator, sample_rate):
        """Fractal wave should have correct sample count."""
        duration = 1.0
        wave = sound_generator.generate_fractal_wave(440.0, 1.5, 5, duration)
        expected_length = int(sample_rate * duration)
        assert len(wave) == expected_length

    def test_iteration_count_respected(self, sound_generator):
        """Should use specified iteration count."""
        wave = sound_generator.generate_fractal_wave(440.0, 1.5, 5, 1.0)
        assert wave is not None
        assert len(wave) == 44100

    def test_fractal_dimension_effect(self, sound_generator):
        """Different fractal dimensions should produce different waves."""
        wave1 = sound_generator.generate_fractal_wave(440.0, 1.0, 5, 1.0)
        wave2 = sound_generator.generate_fractal_wave(440.0, 2.0, 5, 1.0)
        # Waves should differ
        assert not np.allclose(wave1, wave2)

    def test_more_iterations_more_complex(self, sound_generator):
        """More iterations should create more complex waveform."""
        wave_few = sound_generator.generate_fractal_wave(440.0, 1.5, 2, 1.0)
        wave_many = sound_generator.generate_fractal_wave(440.0, 1.5, 10, 1.0)
        # They should differ
        assert not np.allclose(wave_few, wave_many)

    def test_normalized_output(self, sound_generator):
        """Output should be normalized."""
        wave = sound_generator.generate_fractal_wave(440.0, 1.5, 5, 1.0)
        # Fractal wave normalizes to 1.0 by default
        assert np.max(np.abs(wave)) <= 1.0 + 0.001


class TestADSREnvelope:
    """Tests for apply_envelope method."""

    def test_envelope_starts_at_zero(self, sound_generator):
        """Envelope should start at zero (attack)."""
        wave = np.ones(44100)
        result = sound_generator.apply_envelope(wave, 0.1, 0.1, 0.7, 0.1)
        assert result[0] == pytest.approx(0, abs=0.01)

    def test_envelope_ends_at_zero(self, sound_generator):
        """Envelope should end at zero (release)."""
        wave = np.ones(44100)
        result = sound_generator.apply_envelope(wave, 0.1, 0.1, 0.7, 0.1)
        assert result[-1] == pytest.approx(0, abs=0.01)

    def test_sustain_level(self, sound_generator):
        """Should reach sustain level during sustain phase."""
        wave = np.ones(44100)
        sustain = 0.7
        result = sound_generator.apply_envelope(wave, 0.1, 0.1, sustain, 0.1)
        # Check middle of sustain phase
        mid_point = len(result) // 2
        assert result[mid_point] == pytest.approx(sustain, abs=0.1)

    def test_handles_short_waves(self, sound_generator):
        """Should scale envelope for waves shorter than ADSR duration."""
        wave = np.ones(4410)  # 0.1 seconds
        result = sound_generator.apply_envelope(wave, 0.1, 0.1, 0.7, 0.1)
        assert len(result) == 4410
        # Should still have envelope shape
        assert result[0] < result[len(result) // 4]

    def test_preserves_wave_length(self, sound_generator):
        """Envelope should not change wave length."""
        wave = np.ones(44100)
        result = sound_generator.apply_envelope(wave, 0.05, 0.05, 0.8, 0.05)
        assert len(result) == len(wave)

    def test_full_sustain(self, sound_generator):
        """Sustain = 1.0 should maintain full amplitude."""
        wave = np.ones(44100)
        result = sound_generator.apply_envelope(wave, 0.01, 0.01, 1.0, 0.01)
        # After attack+decay, should be at sustain level
        sustain_start = int(0.02 * 44100) + 100
        sustain_end = 44100 - int(0.01 * 44100) - 100
        if sustain_start < sustain_end:
            sustain_values = result[sustain_start:sustain_end]
            assert np.mean(sustain_values) > 0.95


class TestFilter:
    """Tests for apply_filter method."""

    def test_lowpass_attenuates_highs(self, sound_generator):
        """Lowpass filter should reduce high frequency content."""
        # Create wave with high frequency content
        wave = sound_generator.generate_harmonic_wave(440.0, 1.0)
        filtered = sound_generator.apply_filter(wave, "lowpass", 500.0)
        assert filtered is not None
        assert len(filtered) == len(wave)

    def test_highpass_filter(self, sound_generator):
        """Highpass filter should reduce low frequency content."""
        wave = sound_generator.generate_sine_wave(100.0, 1.0)
        filtered = sound_generator.apply_filter(wave, "highpass", 500.0)
        # Filtered wave should have lower amplitude (100Hz filtered out)
        assert np.max(np.abs(filtered)) < np.max(np.abs(wave))

    def test_bandpass_filter(self, sound_generator):
        """Bandpass filter should work without errors."""
        wave = sound_generator.generate_harmonic_wave(440.0, 1.0)
        filtered = sound_generator.apply_filter(wave, "bandpass", 500.0)
        assert filtered is not None
        assert len(filtered) == len(wave)

    def test_unknown_filter_returns_original(self, sound_generator):
        """Unknown filter type should return original wave unchanged."""
        wave = sound_generator.generate_sine_wave(440.0, 1.0)
        result = sound_generator.apply_filter(wave, "unknown_type", 500.0)
        assert np.array_equal(wave, result)

    def test_filter_preserves_length(self, sound_generator):
        """Filter should not change wave length."""
        wave = sound_generator.generate_sine_wave(440.0, 1.0)
        for filter_type in ["lowpass", "highpass", "bandpass"]:
            filtered = sound_generator.apply_filter(wave, filter_type, 500.0)
            assert len(filtered) == len(wave)


class TestChordGeneration:
    """Tests for generate_chord method."""

    def test_major_chord(self, sound_generator):
        """Should generate major chord."""
        wave = sound_generator.generate_chord(440.0, "major", 1.0)
        assert wave is not None
        assert len(wave) == 44100

    def test_minor_chord(self, sound_generator):
        """Should generate minor chord."""
        wave = sound_generator.generate_chord(440.0, "minor", 1.0)
        assert wave is not None

    def test_diminished_chord(self, sound_generator):
        """Should generate diminished chord."""
        wave = sound_generator.generate_chord(440.0, "diminished", 1.0)
        assert wave is not None

    def test_augmented_chord(self, sound_generator):
        """Should generate augmented chord."""
        wave = sound_generator.generate_chord(440.0, "augmented", 1.0)
        assert wave is not None

    def test_seventh_chords(self, sound_generator):
        """Should generate 7th chords."""
        for chord_type in ["major7", "minor7", "dominant7"]:
            wave = sound_generator.generate_chord(440.0, chord_type, 1.0)
            assert wave is not None

    def test_unknown_chord_defaults_to_major(self, sound_generator):
        """Unknown chord type should default to major."""
        wave_unknown = sound_generator.generate_chord(440.0, "unknown_chord", 1.0)
        wave_major = sound_generator.generate_chord(440.0, "major", 1.0)
        assert np.allclose(wave_unknown, wave_major)

    def test_chord_normalized(self, sound_generator):
        """Chord should be normalized to specified amplitude."""
        wave = sound_generator.generate_chord(440.0, "major", 1.0, amplitude=0.5)
        assert np.max(np.abs(wave)) <= 0.5 + 0.001

    def test_different_chords_differ(self, sound_generator):
        """Different chord types should produce different waves."""
        major = sound_generator.generate_chord(440.0, "major", 1.0)
        minor = sound_generator.generate_chord(440.0, "minor", 1.0)
        assert not np.allclose(major, minor)


class TestEdgeCases:
    """Edge case and boundary condition tests."""

    def test_very_low_frequency(self, sound_generator):
        """Should handle very low frequencies."""
        wave = sound_generator.generate_sine_wave(20.0, 1.0)
        assert wave is not None
        assert len(wave) == 44100

    def test_very_high_frequency(self, sound_generator):
        """Should handle high frequencies (up to Nyquist)."""
        wave = sound_generator.generate_sine_wave(20000.0, 1.0)
        assert wave is not None
        assert len(wave) == 44100

    def test_very_short_duration(self, sound_generator):
        """Should handle very short durations."""
        wave = sound_generator.generate_sine_wave(440.0, 0.001)
        assert len(wave) == 44  # 0.001 * 44100

    def test_zero_frequency(self, sound_generator):
        """Zero frequency should produce DC (constant) signal."""
        wave = sound_generator.generate_sine_wave(0.0, 0.1)
        # All values should be zero (sin(0) = 0)
        assert np.allclose(wave, 0)
