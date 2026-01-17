"""
Pytest Configuration and Shared Fixtures for FractalSense EntaENGELment Tests
"""

import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# Sound Generator Fixtures
# ============================================================================

@pytest.fixture
def sample_rate():
    """Default sample rate for audio tests."""
    return 44100


@pytest.fixture
def sound_generator():
    """Create a SoundGenerator instance for testing."""
    from sound_generator import SoundGenerator
    return SoundGenerator(sample_rate=44100)


@pytest.fixture
def mock_pygame():
    """Mock pygame.mixer for tests that don't need actual audio output."""
    with patch('pygame.mixer') as mock:
        mock.get_init.return_value = True
        mock.Sound.return_value = MagicMock()
        yield mock


# ============================================================================
# Color Generator Fixtures
# ============================================================================

@pytest.fixture
def color_generator():
    """Create a ColorGenerator instance for testing."""
    from color_generator import ColorGenerator
    return ColorGenerator()


# ============================================================================
# Module System Fixtures
# ============================================================================

@pytest.fixture
def event_system():
    """Create an EventSystem instance for testing."""
    from modular_app_structure import EventSystem
    return EventSystem()


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file for testing."""
    import json
    config_data = {
        'app': {
            'name': 'Test App',
            'version': '1.0.0'
        },
        'modules': {
            'TestModule': {
                'enabled': True,
                'setting1': 'value1'
            }
        }
    }
    config_file = tmp_path / 'test_config.json'
    config_file.write_text(json.dumps(config_data, indent=2))
    return str(config_file)


# ============================================================================
# Sensor Data Fixtures
# ============================================================================

@pytest.fixture
def sample_sensor_data():
    """Sample sensor data for testing sensor integration."""
    return {
        'accel_x': 0.5,
        'accel_y': -0.3,
        'accel_z': 0.8,
        'gyro_x': 0.1,
        'gyro_y': -0.2,
        'gyro_z': 0.05
    }


@pytest.fixture
def sample_fractal_params():
    """Sample fractal parameters for testing."""
    return {
        'center': complex(-0.75, 0),
        'zoom': 2.0,
        'maxIterations': 100,
        'fractalType': 'mandelbrot'
    }


# ============================================================================
# Wave Data Fixtures
# ============================================================================

@pytest.fixture
def sine_wave_440hz(sound_generator):
    """Generate a 440Hz sine wave for testing."""
    return sound_generator.generate_sine_wave(440.0, 1.0)


@pytest.fixture
def short_wave(sound_generator):
    """Generate a short wave for envelope testing."""
    return sound_generator.generate_sine_wave(440.0, 0.1)


# ============================================================================
# Helper Functions
# ============================================================================

def assert_wave_valid(wave, expected_length=None, max_amplitude=1.0):
    """Assert that a wave array is valid.

    Args:
        wave: The wave array to validate
        expected_length: Expected length (optional)
        max_amplitude: Maximum allowed amplitude
    """
    assert wave is not None, "Wave should not be None"
    assert isinstance(wave, np.ndarray), "Wave should be a numpy array"
    assert len(wave) > 0, "Wave should have length > 0"

    if expected_length is not None:
        assert len(wave) == expected_length, f"Expected length {expected_length}, got {len(wave)}"

    assert np.max(np.abs(wave)) <= max_amplitude + 0.01, \
        f"Wave amplitude {np.max(np.abs(wave))} exceeds max {max_amplitude}"


def get_dominant_frequency(wave, sample_rate):
    """Get the dominant frequency of a wave using FFT.

    Args:
        wave: The wave array
        sample_rate: Sample rate in Hz

    Returns:
        float: Dominant frequency in Hz
    """
    fft = np.fft.fft(wave)
    freqs = np.fft.fftfreq(len(wave), 1/sample_rate)

    # Only look at positive frequencies
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft[:len(fft)//2])

    # Find the peak
    peak_idx = np.argmax(positive_fft)
    return abs(positive_freqs[peak_idx])
