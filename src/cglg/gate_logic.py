"""[HYP] Minimaler Gate-Threshold-Proxy (Stub).

ACHTUNG: Dies ist ein bewusst minimaler Platzhalter (φ ≥ Schwelle). Die
tatsächliche, policy-getriebene Gate-Logik (Phi, RCC:EC, Non-Overlap,
||M||₂, Psi-Lock, Ledger-Integration, Strict-Mode) lebt in
``tools/mzm/gate_toggle.py`` (``gate_open``). Für echte Gate-Entscheidungen
diese Funktion NICHT verwenden.

Siehe VOID-011 / VOID-012 für den Ausbau der CGLG-Membran.
"""


def gate(phi: float, threshold: float = 0.6) -> bool:
    """[HYP] Öffnet, wenn ``phi >= threshold``. Proxy — siehe Modul-Docstring."""
    return phi >= threshold
