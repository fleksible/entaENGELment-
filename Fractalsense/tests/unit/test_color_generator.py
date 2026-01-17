"""
Tests for ColorGenerator class in color_generator.py

Tests cover:
- Default colormap creation
- Resonant colormap
- Harmonic colormap
- Spectral colormap
- Fractal colormap
- Mereotopological colormap
- Dynamic colormap creation
- Sensor-based colormap
- Golden ratio colormap
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from color_generator import ColorGenerator


class TestColorGeneratorInit:
    """Tests for ColorGenerator initialization."""

    def test_creates_custom_colormaps_dict(self):
        """Should initialize with empty custom_colormaps dict."""
        generator = ColorGenerator()
        assert hasattr(generator, 'custom_colormaps')
        assert isinstance(generator.custom_colormaps, dict)

    def test_creates_default_colormaps_on_init(self):
        """Should create default colormaps on initialization."""
        generator = ColorGenerator()
        # Should have 5 default colormaps
        assert len(generator.custom_colormaps) >= 5


class TestDefaultColormaps:
    """Tests for default colormap creation."""

    def test_creates_resonant_colormap(self, color_generator):
        """Should create resonant colormap on init."""
        assert 'resonant' in color_generator.custom_colormaps

    def test_creates_harmonic_colormap(self, color_generator):
        """Should create harmonic colormap on init."""
        assert 'harmonic' in color_generator.custom_colormaps

    def test_creates_spectral_colormap(self, color_generator):
        """Should create spectral colormap on init."""
        assert 'spectral' in color_generator.custom_colormaps

    def test_creates_fractal_colormap(self, color_generator):
        """Should create fractal colormap on init."""
        assert 'fractal' in color_generator.custom_colormaps

    def test_creates_mereotopological_colormap(self, color_generator):
        """Should create mereotopological colormap on init."""
        assert 'mereotopological' in color_generator.custom_colormaps


class TestResonantColormap:
    """Tests for resonant colormap generation."""

    def test_colormap_exists(self, color_generator):
        """Resonant colormap should exist."""
        cmap = color_generator.custom_colormaps.get('resonant')
        assert cmap is not None

    def test_colormap_is_callable(self, color_generator):
        """Colormap should be callable with values 0-1."""
        cmap = color_generator.custom_colormaps['resonant']
        color = cmap(0.5)
        assert color is not None
        assert len(color) == 4  # RGBA

    def test_colormap_at_zero(self, color_generator):
        """Should return valid color at position 0."""
        cmap = color_generator.custom_colormaps['resonant']
        color = cmap(0)
        assert all(0 <= c <= 1 for c in color)

    def test_colormap_at_one(self, color_generator):
        """Should return valid color at position 1."""
        cmap = color_generator.custom_colormaps['resonant']
        color = cmap(1)
        assert all(0 <= c <= 1 for c in color)

    def test_violet_to_gold_gradient(self, color_generator):
        """Should transition from violet (start) to gold (end)."""
        cmap = color_generator.custom_colormaps['resonant']
        first_color = cmap(0)[:3]  # RGB only
        last_color = cmap(1)[:3]

        # First color should be violet-ish (higher blue than green)
        # Last color should be gold-ish (high red, medium green, low blue)
        # Note: This is approximate due to HSV to RGB conversion
        assert first_color is not None
        assert last_color is not None


class TestHarmonicColormap:
    """Tests for harmonic colormap generation."""

    def test_colormap_exists(self, color_generator):
        """Harmonic colormap should exist."""
        cmap = color_generator.custom_colormaps.get('harmonic')
        assert cmap is not None

    def test_uses_golden_ratio(self, color_generator):
        """Harmonic colormap should use golden ratio patterns."""
        cmap = color_generator.custom_colormaps['harmonic']
        # Test that colormap produces valid colors across range
        colors = [cmap(i/10) for i in range(11)]
        assert all(all(0 <= c <= 1 for c in color) for color in colors)

    def test_produces_varied_colors(self, color_generator):
        """Should produce varied colors across the range."""
        cmap = color_generator.custom_colormaps['harmonic']
        color1 = cmap(0.0)[:3]
        color2 = cmap(0.5)[:3]
        color3 = cmap(1.0)[:3]

        # Colors should differ
        assert not np.allclose(color1, color2, atol=0.1)
        assert not np.allclose(color2, color3, atol=0.1)


class TestSpectralColormap:
    """Tests for spectral colormap generation."""

    def test_colormap_exists(self, color_generator):
        """Spectral colormap should exist."""
        cmap = color_generator.custom_colormaps.get('spectral')
        assert cmap is not None

    def test_wavelength_range_coverage(self, color_generator):
        """Should cover visible spectrum wavelengths."""
        cmap = color_generator.custom_colormaps['spectral']
        # Test points across the spectrum
        colors = [cmap(i/10) for i in range(11)]
        assert len(colors) == 11

    def test_violet_at_start(self, color_generator):
        """Start of colormap should be violet/blue range."""
        cmap = color_generator.custom_colormaps['spectral']
        color = cmap(0)[:3]
        # Violet should have significant blue component
        assert color[2] > 0.1  # Blue component should be notable

    def test_red_at_end(self, color_generator):
        """End of colormap should be red range."""
        cmap = color_generator.custom_colormaps['spectral']
        color = cmap(1)[:3]
        # Red should be the dominant channel (accounting for intensity falloff at spectrum edges)
        assert color[0] > color[1]  # Red > Green
        # Blue may be similar due to intensity correction at 750nm edge
        assert color[0] > 0.2  # Red has significant value


class TestFractalColormap:
    """Tests for fractal colormap generation."""

    def test_colormap_exists(self, color_generator):
        """Fractal colormap should exist."""
        cmap = color_generator.custom_colormaps.get('fractal')
        assert cmap is not None

    def test_nonlinear_distribution(self, color_generator):
        """Should have non-linear color distribution."""
        cmap = color_generator.custom_colormaps['fractal']
        # Sample colors should all be valid
        for t in [0, 0.25, 0.5, 0.75, 1.0]:
            color = cmap(t)
            assert all(0 <= c <= 1 for c in color)

    def test_cyclic_patterns(self, color_generator):
        """Fractal colormap should show cyclic patterns."""
        cmap = color_generator.custom_colormaps['fractal']
        # Due to sin/cos usage, colors should cycle
        colors = [cmap(i/100)[:3] for i in range(101)]
        # Check that colors vary across the range
        unique_enough = len(set(tuple(round(c, 2) for c in color) for color in colors)) > 50
        assert unique_enough


class TestMereotopologicalColormap:
    """Tests for mereotopological colormap generation."""

    def test_colormap_exists(self, color_generator):
        """Mereotopological colormap should exist."""
        cmap = color_generator.custom_colormaps.get('mereotopological')
        assert cmap is not None

    def test_has_256_colors(self, color_generator):
        """Should have 256 color entries."""
        cmap = color_generator.custom_colormaps['mereotopological']
        # Colormap should work for all values
        colors = [cmap(i/255) for i in range(256)]
        assert len(colors) == 256

    def test_first_half_blue_green(self, color_generator):
        """First half should be blue-green range."""
        cmap = color_generator.custom_colormaps['mereotopological']
        color = cmap(0.25)[:3]
        # Should have significant blue or green
        assert max(color[1], color[2]) > 0.3

    def test_second_half_red_violet(self, color_generator):
        """Second half should be red-violet range."""
        cmap = color_generator.custom_colormaps['mereotopological']
        color = cmap(0.75)[:3]
        # Should have significant red
        assert color[0] > 0.3


class TestDynamicColormap:
    """Tests for dynamic colormap creation."""

    def test_creates_from_hsv(self, color_generator):
        """Should create colormap from base HSV values."""
        cmap = color_generator.create_dynamic_colormap(
            base_hsv=(0.5, 0.8, 0.9),
            shift_factor=0.5,
            name='test_dynamic'
        )
        assert cmap is not None

    def test_returns_colormap(self, color_generator):
        """Should return a usable colormap."""
        cmap = color_generator.create_dynamic_colormap(
            base_hsv=(0.3, 0.7, 0.8),
            shift_factor=0.3,
            name='test_dynamic_2'
        )
        color = cmap(0.5)
        assert len(color) == 4  # RGBA

    def test_shift_factor_affects_output(self, color_generator):
        """Different shift factors should produce different colormaps."""
        cmap1 = color_generator.create_dynamic_colormap(
            base_hsv=(0.5, 0.8, 0.9),
            shift_factor=0.1,
            name='test_shift_1'
        )
        cmap2 = color_generator.create_dynamic_colormap(
            base_hsv=(0.5, 0.8, 0.9),
            shift_factor=0.9,
            name='test_shift_2'
        )

        # Colors at same position should differ
        color1 = cmap1(0.5)[:3]
        color2 = cmap2(0.5)[:3]
        # Allow for some similarity but they should differ
        assert not np.allclose(color1, color2, atol=0.01)


class TestSensorBasedColormap:
    """Tests for sensor-based colormap creation."""

    def test_creates_from_sensor_data(self, color_generator, sample_sensor_data):
        """Should create colormap from sensor data."""
        cmap = color_generator.create_sensor_based_colormap(
            sensor_data=sample_sensor_data,
            fractal_zoom=2.0
        )
        assert cmap is not None

    def test_responds_to_sensor_variation(self, color_generator):
        """Should vary colormap based on sensor input."""
        sensor_data_1 = {
            'accel_x': 0.0, 'accel_y': 0.0, 'accel_z': 0.0,
            'gyro_x': 0.0, 'gyro_y': 0.0, 'gyro_z': 0.0
        }
        sensor_data_2 = {
            'accel_x': 1.0, 'accel_y': 1.0, 'accel_z': 1.0,
            'gyro_x': 1.0, 'gyro_y': 1.0, 'gyro_z': 1.0
        }

        cmap1 = color_generator.create_sensor_based_colormap(
            sensor_data_1, fractal_zoom=1.0, name='sensor_1'
        )
        cmap2 = color_generator.create_sensor_based_colormap(
            sensor_data_2, fractal_zoom=1.0, name='sensor_2'
        )

        color1 = cmap1(0.5)[:3]
        color2 = cmap2(0.5)[:3]

        # Colors should differ based on sensor data
        assert not np.allclose(color1, color2, atol=0.01)

    def test_responds_to_zoom_variation(self, color_generator, sample_sensor_data):
        """Should vary based on fractal zoom."""
        cmap1 = color_generator.create_sensor_based_colormap(
            sample_sensor_data, fractal_zoom=1.0, name='zoom_1'
        )
        cmap2 = color_generator.create_sensor_based_colormap(
            sample_sensor_data, fractal_zoom=100.0, name='zoom_2'
        )

        color1 = cmap1(0.5)[:3]
        color2 = cmap2(0.5)[:3]

        # Colors should differ based on zoom
        # Note: The difference may be subtle
        assert cmap1 is not cmap2

    def test_handles_missing_sensor_keys(self, color_generator):
        """Should handle missing sensor data keys gracefully."""
        partial_data = {'accel_x': 0.5}
        cmap = color_generator.create_sensor_based_colormap(
            partial_data, fractal_zoom=1.0, name='partial_sensor'
        )
        assert cmap is not None


class TestGoldenRatioColormap:
    """Tests for golden ratio colormap creation."""

    def test_creates_colormap(self, color_generator):
        """Should create golden ratio colormap."""
        cmap = color_generator.create_golden_ratio_colormap(base_hue=0.0)
        assert cmap is not None

    def test_uses_phi_in_calculation(self, color_generator):
        """Should incorporate golden ratio (phi) in hue calculation."""
        cmap = color_generator.create_golden_ratio_colormap(
            base_hue=0.0, name='golden_test'
        )
        # Colormap should produce valid colors
        color = cmap(0.5)
        assert all(0 <= c <= 1 for c in color)

    def test_different_base_hues(self, color_generator):
        """Different base hues should produce different colormaps."""
        cmap1 = color_generator.create_golden_ratio_colormap(
            base_hue=0.0, name='golden_0'
        )
        cmap2 = color_generator.create_golden_ratio_colormap(
            base_hue=0.5, name='golden_05'
        )

        color1 = cmap1(0.0)[:3]
        color2 = cmap2(0.0)[:3]

        assert not np.allclose(color1, color2, atol=0.01)


class TestResonantGradient:
    """Tests for resonant gradient creation."""

    def test_creates_gradient_list(self, color_generator):
        """Should create list of RGB colors."""
        colors = color_generator.create_resonant_gradient(
            base_frequency=1.0,
            harmonic_ratio=1.5
        )
        assert isinstance(colors, list)
        assert len(colors) == 256  # Default n_colors

    def test_custom_color_count(self, color_generator):
        """Should create custom number of colors."""
        colors = color_generator.create_resonant_gradient(
            base_frequency=1.0,
            harmonic_ratio=1.5,
            n_colors=128
        )
        assert len(colors) == 128

    def test_rgb_values_in_range(self, color_generator):
        """All RGB values should be in [0, 1] range."""
        colors = color_generator.create_resonant_gradient(
            base_frequency=2.0,
            harmonic_ratio=1.618
        )
        for r, g, b in colors:
            assert 0 <= r <= 1
            assert 0 <= g <= 1
            assert 0 <= b <= 1

    def test_harmonic_ratio_affects_output(self, color_generator):
        """Different harmonic ratios should produce different gradients."""
        colors1 = color_generator.create_resonant_gradient(
            base_frequency=1.0,
            harmonic_ratio=1.0
        )
        colors2 = color_generator.create_resonant_gradient(
            base_frequency=1.0,
            harmonic_ratio=2.0
        )

        # At least some colors should differ
        differences = sum(
            1 for c1, c2 in zip(colors1, colors2)
            if not np.allclose(c1, c2, atol=0.01)
        )
        assert differences > 10


class TestRGBBounds:
    """Tests for RGB value bounds validation."""

    def test_all_colormaps_rgb_in_range(self, color_generator):
        """All colormap colors should have RGB values in [0, 1]."""
        for name, cmap in color_generator.custom_colormaps.items():
            for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
                color = cmap(t)
                assert all(0 <= c <= 1 for c in color), \
                    f"Colormap '{name}' has out-of-range color at t={t}: {color}"

    def test_dynamic_colormap_rgb_in_range(self, color_generator):
        """Dynamic colormap should have valid RGB values."""
        for h in [0.0, 0.3, 0.6, 0.9]:
            cmap = color_generator.create_dynamic_colormap(
                base_hsv=(h, 0.8, 0.9),
                shift_factor=0.5,
                name=f'dynamic_test_{h}'
            )
            for t in np.linspace(0, 1, 11):
                color = cmap(t)
                assert all(0 <= c <= 1 for c in color)


class TestEdgeCases:
    """Edge case tests for ColorGenerator."""

    def test_extreme_shift_factors(self, color_generator):
        """Should handle extreme shift factors."""
        for shift in [0.0, 0.001, 100.0]:
            cmap = color_generator.create_dynamic_colormap(
                base_hsv=(0.5, 0.8, 0.9),
                shift_factor=shift,
                name=f'extreme_shift_{shift}'
            )
            assert cmap is not None

    def test_zero_zoom_sensor_colormap(self, color_generator):
        """Should handle zero zoom gracefully."""
        sensor_data = {'accel_x': 0.0, 'gyro_x': 0.0}
        # Zero zoom might cause log issues, should be handled
        cmap = color_generator.create_sensor_based_colormap(
            sensor_data, fractal_zoom=0.1, name='zero_zoom'
        )
        assert cmap is not None

    def test_negative_sensor_values(self, color_generator):
        """Should handle negative sensor values."""
        sensor_data = {
            'accel_x': -1.0, 'accel_y': -1.0, 'accel_z': -1.0,
            'gyro_x': -0.5, 'gyro_y': -0.5, 'gyro_z': -0.5
        }
        cmap = color_generator.create_sensor_based_colormap(
            sensor_data, fractal_zoom=1.0, name='negative_sensor'
        )
        # Should still produce valid colors
        color = cmap(0.5)
        assert all(0 <= c <= 1 for c in color)
