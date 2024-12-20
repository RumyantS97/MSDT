import pytest
from calculator import Calculator
from unittest.mock import patch


@pytest.fixture
def calc():
    return Calculator()

# Тест проверки сложения
def test_add(calc):
    assert calc.add(2, 3) == 5          
    assert calc.add(-1, 1) == 0       
    assert calc.add(0, 0) == 0       


# Тест проверки вычитания
def test_subtract(calc):
    assert calc.subtract(5, 3) == 2     
    assert calc.subtract(-1, 1) == -2  
    assert calc.subtract(0, 0) == 0  


# Тест проверки умножения
def test_multiply(calc):
    assert calc.multiply(2, 3) == 6    
    assert calc.multiply(-1, 5) == -5  
    assert calc.multiply(0, 5) == 0    


# Тест проверки деления
def test_divide(calc):
    assert calc.divide(6, 3) == 2.0     
    assert calc.divide(-10, 2) == -5.0
    with pytest.raises(ZeroDivisionError):
        calc.divide(5, 0)  # Ожидаем ошибку деления на 0


# Тест проверки деления дробных чисел
def test_divide_fractional(calc):
    assert calc.divide(7, 2) == 3.5   
    assert calc.divide(-9, 4) == -2.25 


# Тест проверки квадратного корня
def test_sqrt(calc):
    assert calc.sqrt(4) == 2.0
    assert calc.sqrt(0) == 0.0
    with pytest.raises(ValueError):
        calc.sqrt(-1)  # Ожидаем ошибку для отрицательных чисел
    with pytest.raises(TypeError):
        calc.sqrt('string')  # Ожидаем ошибку для некорректных типов данных


# Тест с моком функции sqrt из math
def test_sqrt_mocking(calc):
    with patch('math.sqrt', return_value=5):
        result = calc.sqrt(25)
        assert result == 5 


# Тест проверки типа входных данных
def test_invalid_input_type(calc):
    with pytest.raises(TypeError):
        calc.add('a', 3)  # Ожидаем ошибку для строкового значения вместо числа
    with pytest.raises(TypeError):
        calc.subtract(3, 'b')
    with pytest.raises(TypeError):
        calc.multiply(3, 'c')
    with pytest.raises(TypeError):
        calc.divide(4, 'd')
    with pytest.raises(TypeError):
        calc.sqrt([])  # Ожидаем ошибку для неподдерживаемого типа данных


# Параметризованный тест для проверки различных значений sqrt
def test_parametrized_sqrt(calc):
    test_cases = [
        (4, 2.0),
        (9, 3.0),
        (16, 4.0),
        (0, 0.0),
    ]
    for input_value, expected in test_cases:
        assert calc.sqrt(input_value) == expected


def test_mock_division_error(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0) 

    with pytest.raises(ValueError):
        calc.sqrt(-10)  # Ожидаем ошибку для отрицательных чисел

def test_sqrt_complex_numbers(calc):
    with pytest.raises(ValueError, match="Cannot calculate the square root of a negative number"):
        calc.sqrt(-10)  # Ожидаем ошибку для отрицательных чисел
    
    with pytest.raises(TypeError, match="Input must be int or float"):
        calc.sqrt([1, 2, 3])  # Ожидаем ошибку для неподдерживаемого типа данных
