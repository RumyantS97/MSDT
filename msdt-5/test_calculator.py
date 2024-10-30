import pytest
from calculator import Calculator
from unittest.mock import Mock

@pytest.fixture
def calculator():
    return Calculator()

# 1. Тест на сложение
def test_add(calculator):
    assert calculator.add(3, 5) == 8
    assert calculator.add(-3, 3) == 0

# 2. Тест на вычитание
def test_subtract(calculator):
    assert calculator.subtract(10, 4) == 6
    assert calculator.subtract(5, 10) == -5

# 3. Тест на умножение
def test_multiply(calculator):
    assert calculator.multiply(3, 5) == 15
    assert calculator.multiply(-3, 5) == -15

# 4. Тест на деление
def test_divide(calculator):
    assert calculator.divide(10, 2) == 5
    assert calculator.divide(5, 2) == 2.5

# 5. Тест на деление на ноль
def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(5, 0)

# 6. Тест на некорректные типы входных данных
@pytest.mark.parametrize("a, b", [("3", 5), (3, "5"), (None, 5), (3, None)])
def test_invalid_input(calculator, a, b):
    with pytest.raises(TypeError):
        calculator.add(a, b)

# 7. Тест на параметризованное деление
@pytest.mark.parametrize("a, b, result", [(10, 2, 5), (9, 3, 3), (5, 0.5, 10)])
def test_divide_parametrized(calculator, a, b, result):
    assert calculator.divide(a, b) == result

# 8. Тест с моком для проверки вызова метода _validate_input
def test_validate_input_call():
    mock_calculator = Calculator()
    mock_calculator._validate_input = Mock()
    mock_calculator.add(2, 3)
    mock_calculator._validate_input.assert_called_once_with(2, 3)

# Тесты для sqrt
# 9. Тест на нахождение квадратного корня положительного числа
def test_sqrt_positive(calculator):
    assert calculator.sqrt(9) == 3
    assert calculator.sqrt(16) == 4
    assert calculator.sqrt(0) == 0

# 10. Тест на отрицательное число
def test_sqrt_negative(calculator):
    with pytest.raises(ValueError):
        calculator.sqrt(-4)

# 11. Тест на некорректный тип входного значения
def test_sqrt_invalid_type(calculator):
    with pytest.raises(TypeError):
        calculator.sqrt("9")

# 12. Параметризованный тест для sqrt с разными входными значениями
@pytest.mark.parametrize("input_value, expected_output", [
    (25, 5),
    (0.25, 0.5),
    (1, 1),
    (100, 10)
])
def test_sqrt_parametrized(calculator, input_value, expected_output):
    assert calculator.sqrt(input_value) == expected_output