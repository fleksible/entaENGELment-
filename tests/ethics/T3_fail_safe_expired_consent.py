from tools.mzm.gate_toggle import Context, gate_open, load_policy


def test_gate_closes_when_consent_expired():
    policy = load_policy()
    # Simuliere abgelaufenen Consent: rcc_ec=False
    ctx = Context(phi=0.95, rcc_ec=False, non_overlap=True, m_norm_l2=1.0, psi_lock=True)
    assert gate_open(ctx, policy) is False
