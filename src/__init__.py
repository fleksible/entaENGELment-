"""entaENGELment Framework - Resonanz-Kernel für verkörperte Mensch-KI-Interaktion.

Version: 1.0 (Hardened Kernel 0·β)
"""

__version__ = "1.0.0"
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
