from app.utils.helpers import adder


def test_adder():
    assert adder(1, 2, 3) == 6
    assert adder(-1, 1) == 0
    assert adder(0, 0, 0) == 0
    assert adder(5) == 5
