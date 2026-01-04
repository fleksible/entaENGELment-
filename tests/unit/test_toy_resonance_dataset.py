from src.tools.toy_resonance_dataset import compute_demo_metrics, generate_mycel_signals


def test_generate_mycel_signals_shapes_and_ranges():
    ds = generate_mycel_signals(n=64, seed=1, coupling=0.5)

    assert len(ds.t) == 64
    assert len(ds.a) == 64
    assert len(ds.b) == 64
    assert len(ds.phases) == 64
    assert len(ds.consent_signal) == 64

    assert all(0.0 <= v <= 1.0 for v in ds.consent_signal)


def test_compute_demo_metrics_returns_all_keys_and_numbers():
    ds = generate_mycel_signals(n=64, seed=2, coupling=0.4)
    m = compute_demo_metrics(ds)

    assert set(m.keys()) == {"ECI", "PLV", "MI", "FD", "PF"}
    for v in m.values():
        assert isinstance(v, float)


def test_plv_increases_with_coupling():
    """PLV should increase with higher coupling (monotonicity check)."""
    low = compute_demo_metrics(generate_mycel_signals(n=256, seed=7, coupling=0.1))["PLV"]
    high = compute_demo_metrics(generate_mycel_signals(n=256, seed=7, coupling=0.8))["PLV"]

    # robust monotonicity check (deterministic seed)
    assert high > low + 0.1
