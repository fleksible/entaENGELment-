from tools.mzm.gate_toggle import Context, load_policy, gate_open

def test_gate_opens_with_valid_ctx():
    policy = load_policy()
    ctx = Context(phi=0.9, rcc_ec=True, non_overlap=True, m_norm_l2=1.0, psi_lock=True)
    assert gate_open(ctx, policy) is True

def test_gate_closes_on_phi_below_threshold():
    policy = load_policy()
    ctx = Context(phi=0.5, rcc_ec=True, non_overlap=True, m_norm_l2=1.0, psi_lock=True)
    assert gate_open(ctx, policy) is False
