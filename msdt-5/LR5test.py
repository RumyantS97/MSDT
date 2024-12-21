import pytest
from unittest.mock import patch
import math

# Импортируем функции из вашего кода
from LR5 import basic_operations, factorial, square_root, solve_quadratic

def test_basic_operations():
    result = basic_operations(10, 5)
    assert result["Сложение"] == 15
    assert result["Вычитание"] == 5
    assert result["Умножение"] == 50
    assert result["Деление"] == 2

def test_division_by_zero():
    result = basic_operations(10, 0)
    assert result["Деление"] == "Деление на ноль невозможно"

def test_factorial_positive():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_negative():
    assert factorial(-5) == "Факториал отрицательного числа не определен"

def test_square_root_positive():
    assert square_root(16) == 4

def test_square_root_negative():
    assert square_root(-16) == "Квадратный корень отрицательного числа не определен"

@pytest.mark.parametrize("a, b, c, expected", [
    (1, -3, 2, (2.0, 1.0)),  # Два действительных корня
    (1, 2, 1, (-1.0,)),      # Один действительный корень
    (1, 0, 1, "Нет действительных корней"),  # Нет действительных корней
    (0, 2, 1, "Это не квадратное уравнение")  # Не квадратное уравнение
])
def test_solve_quadratic(a, b, c, expected):
    assert solve_quadratic(a, b, c) == expected

@patch('math.sqrt', return_value=5)
def test_mock_square_root(mock_sqrt):
    result = square_root(25)
    mock_sqrt.assert_called_once_with(25)
    assert result == 5

