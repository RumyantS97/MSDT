import math

import pytest
import operations


@pytest.mark.parametrize("x,y", [(1, 1), (-2, -2), (2.5, 3.45)])
def test_binary_operations(x, y):
    assert operations.add(x, y) == x + y
    assert operations.subtract(x, y) == x - y
    assert operations.multiply(x, y) == x * y
    assert operations.divide(x, y) == x / y
    assert operations.power(x, y) == x ** y


@pytest.mark.parametrize("x", [0, 30, 180])
def test_unary_operations(x):
    assert operations.sin(x) == math.sin(math.radians(x))
    assert operations.cos(x) == math.cos(math.radians(x))
    assert operations.tan(x) == math.tan(math.radians(x))
    assert operations.sqrt(x) == x ** 0.5


def test_negative_sqrt():
    with pytest.raises(ValueError):
        operations.sqrt(-2)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        operations.divide(1, 0)

