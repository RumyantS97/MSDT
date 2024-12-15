import pytest
from operations import Operations
from unittest.mock import Mock

@pytest.fixture
def operations():
    return Operations()

# 1. Тест на нахождение факториала
def test_factorial(operations):
    assert operations.factorial(5) == 120
    assert operations.factorial(0) == 1

# 2. Тест на факториал отрицательного числа
def test_factorial_negative(operations):
    with pytest.raises(ValueError):
        operations.factorial(-1)
    with pytest.raises(ValueError):
        operations.factorial(-10)

# 3. Параметризованный тест на возведение в степень
@pytest.mark.parametrize("a, b, c", [
    (2, 3, 8),
    (5, 0, 1),
    (3, -1, 1/3),
])
def test_power(operations, a, b, c):
    assert operations.power(a, b) == c

# 4. Тест на нахождение логарифма
def test_logarithm(operations):
    assert operations.logarithm(1) == 0  # Логарифм по основанию e
    assert operations.logarithm(10, 10) == 1
    assert operations.logarithm(16, 2) == 4

# 5. Тест на логарифм не положительного числа
def test_logarithm_non_positive(operations):
    with pytest.raises(ValueError):
        operations.logarithm(-10)

# 6. Тест на взятие квадратного корня
def test_square_root(operations):
    assert operations.square_root(9) == 3
    assert operations.square_root(0) == 0

# 7. Тест на корень из отрицательного числа
def test_square_root_negative(operations):
    with pytest.raises(ValueError):
        operations.square_root(-4)


# 8. Параметризованный тест на деление с остатком
@pytest.mark.parametrize("a, b, c", [ 
    (10, 3, 1),
    (5, 2, 1),
])
def test_division_by_modulus(operations, a, b, c):
    assert operations.division_by_modulus(a, b) == c

# 9. Тест с моком для проверки вызова метода
def test_factorial_call():
    mock_operations = Operations()
    mock_operations.factorial = Mock()
    mock_operations.factorial(5)
    mock_operations.factorial.assert_called_once_with(5)
