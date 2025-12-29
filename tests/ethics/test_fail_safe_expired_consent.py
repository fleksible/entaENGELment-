"""Ethics-Tests: Fail-Safe bei abgelaufenem Consent.

Testet, dass das System sicher reagiert, wenn der Consent abgelaufen ist
oder andere ethische Constraints verletzt werden.
"""

from tools.mzm.gate_toggle import Context, load_policy, gate_open


def test_gate_closes_when_consent_expired():
    """Test: Gate schließt wenn Consent abgelaufen ist.

    Simuliert abgelaufenen Consent durch rcc_ec=False.
    Dies ist ein kritischer Fail-Safe: Das System muss bei fehlendem
    Consent IMMER blockieren, unabhängig von anderen Metriken.
    """
    policy = load_policy()

    # Alle anderen Werte sind perfekt, aber Consent ist abgelaufen
    ctx = Context(
        phi=0.95,           # Sehr hoher Phi-Wert
        rcc_ec=False,       # ABER: Consent abgelaufen!
        non_overlap=True,
        m_norm_l2=1.0,
        psi_lock=True
    )

    # Gate MUSS geschlossen bleiben
    assert gate_open(ctx, policy) is False


def test_gate_closes_without_lock():
    """Test: Gate schließt ohne Psi-Lock.

    Der Psi-Lock ist ein zusätzlicher Sicherheitsmechanismus.
    Ohne Lock darf das Gate nicht öffnen.
    """
    policy = load_policy()

    ctx = Context(
        phi=0.95,
        rcc_ec=True,
        non_overlap=True,
        m_norm_l2=1.0,
        psi_lock=False      # Kein Lock
    )

    assert gate_open(ctx, policy) is False


def test_gate_closes_on_overlap():
    """Test: Gate schließt bei Overlap-Verletzung.

    Non-Overlap (¬PO) ist eine Datenschutz-Invariante:
    Rohdaten dürfen nicht überlappen/geteilt werden.
    """
    policy = load_policy()

    ctx = Context(
        phi=0.95,
        rcc_ec=True,
        non_overlap=False,  # Overlap-Verletzung!
        m_norm_l2=1.0,
        psi_lock=True
    )

    assert gate_open(ctx, policy) is False


def test_multiple_violations_still_block():
    """Test: Mehrfache Verletzungen blockieren definitiv.

    Wenn mehrere ethische Constraints verletzt sind,
    muss das System absolut blockieren.
    """
    policy = load_policy()

    ctx = Context(
        phi=0.95,
        rcc_ec=False,       # Consent fehlt
        non_overlap=False,  # Overlap-Verletzung
        m_norm_l2=1.0,
        psi_lock=False      # Kein Lock
    )

    assert gate_open(ctx, policy) is False
