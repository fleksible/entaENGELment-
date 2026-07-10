"""entaENGELment Framework - Resonanz-Kernel für verkörperte Mensch-KI-Interaktion.

Version: 0.1.0 (Alpha)
"""

__version__ = "0.1.0"
__author__ = "fleksible"

# Expose wichtige Komponenten auf Package-Ebene
from src.core.metrics import eci, fd, mi, pf, plv

__all__ = [
    "eci",
    "plv",
    "mi",
    "fd",
    "pf",
]
