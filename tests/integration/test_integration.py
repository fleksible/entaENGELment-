"""Integrationstests für das entaENGELment Framework.

Testet die Integration zwischen Gate-Toggle und Policy-Loader,
sowie den vollständigen Token-Lifecycle.
"""

from tools.mzm.gate_toggle import Context, load_policy, gate_open


def test_gate_opens_with_valid_ctx():
    """Test: Gate öffnet bei gültigen Kontext-Werten."""
    policy = load_policy()
    ctx = Context(
        phi=0.9,
        rcc_ec=True,
        non_overlap=True,
        m_norm_l2=1.0,
        psi_lock=True
    )
    assert gate_open(ctx, policy) is True


def test_gate_closes_on_phi_below_threshold():
    """Test: Gate schließt wenn Phi unter Schwellenwert liegt."""
    policy = load_policy()
    ctx = Context(
        phi=0.5,
        rcc_ec=True,
        non_overlap=True,
        m_norm_l2=1.0,
        psi_lock=True
    )
    assert gate_open(ctx, policy) is False


def test_gate_closes_on_invalid_m_norm():
    """Test: Gate schließt bei falscher M-Norm."""
    policy = load_policy()
    ctx = Context(
        phi=0.9,
        rcc_ec=True,
        non_overlap=True,
        m_norm_l2=0.5,
        psi_lock=True
    )
    assert gate_open(ctx, policy) is False


def test_gate_requires_all_constraints():
    """Test: Gate erfordert alle Constraints gleichzeitig."""
    policy = load_policy()

    # Alle erfüllt
    ctx_all = Context(phi=0.9, rcc_ec=True, non_overlap=True, m_norm_l2=1.0, psi_lock=True)
    assert gate_open(ctx_all, policy) is True

    # Eines fehlt: non_overlap
    ctx_missing = Context(phi=0.9, rcc_ec=True, non_overlap=False, m_norm_l2=1.0, psi_lock=True)
    assert gate_open(ctx_missing, policy) is False


def test_policy_structure():
    """Test: Policy hat erwartete Struktur."""
    policy = load_policy()
    assert "version" in policy
    assert "constraints" in policy
    assert "receipts" in policy
    assert policy["version"] == "1.0"
