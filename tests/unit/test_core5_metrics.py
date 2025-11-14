from src.core.metrics import eci, plv, mi, fd, pf

def test_metrics_exist_and_return_numbers():
    assert 0.0 <= eci([0.4, 0.6]) <= 1.0
    assert 0.0 <= plv([0.0, 0.1, 0.2]) <= 1.0
    assert isinstance(mi([1],[2]), float)
    assert isinstance(fd([1,2,3]), float)
    assert isinstance(pf([1,-1,1]), float)
