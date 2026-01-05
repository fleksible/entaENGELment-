"""Bio Spiral Viewer application package.

This package exposes helper APIs to load the EntaENGELment seed
information, evaluate the live resonance metrics, and produce an
operator-facing textual view of the spiral state.  The code aims to stay
close to the governance principles documented in the framework, so that
visualisations always reflect Gate/ETHICS/CRI decisions.
"""

from .cli import run

__all__ = ["run"]
