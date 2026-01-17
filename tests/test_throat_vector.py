from src.tools.throat_vector import throat_vector


def test_throat():
    v = throat_vector(1, 1, 1)
    assert v > 0
