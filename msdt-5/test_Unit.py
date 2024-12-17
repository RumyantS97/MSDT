import pytest
from math import isclose
from lab5 import (
    AdvancedMath
)
from unittest.mock import Mock

# ----------- Тесты для работы с векторами -----------

def test_vector_dot_product():
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    result = AdvancedMath.vector_dot_product(v1, v2)
    assert result == 32

def test_vector_magnitude():
    v = [3, 4]
    result = AdvancedMath.vector_magnitude(v)
    assert isclose(result, 5.0, rel_tol=1e-6)

def test_vector_normalize():
    v = [3, 4]
    result = AdvancedMath.vector_normalize(v)
    assert isclose(result[0], 0.6, rel_tol=1e-6)
    assert isclose(result[1], 0.8, rel_tol=1e-6)

def test_vector_normalize_zero_vector():
    v = [0, 0, 0]
    with pytest.raises(ValueError):
        AdvancedMath.vector_normalize(v)

# ----------- Тесты для работы с матрицами -----------

def test_matrix_addition():
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    result = AdvancedMath.matrix_addition(m1, m2)
    assert result == [[6, 8], [10, 12]]

def test_matrix_multiplication():
    m1 = [[1, 2], [3, 4]]
    m2 = [[2, 0], [1, 2]]
    result = AdvancedMath.matrix_multiplication(m1, m2)
    assert result == [[4, 4], [10, 8]]

@pytest.mark.parametrize("matrix, transpose", [
    ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
    ([[1]], [[1]]),
    ([[1, 2, 3]], [[1], [2], [3]])
])
def test_matrix_transpose(matrix, transpose):
    result = AdvancedMath.matrix_transpose(matrix)
    assert result == transpose

# ----------- Численные методы -----------

def test_newton_raphson():
    # Пример x^2 - 2 = 0, решение x = sqrt(2)
    f = lambda x: x**2 - 2
    df = lambda x: 2 * x
    root = AdvancedMath.newton_raphson(f, df, x0=1)
    assert isclose(root, 2**0.5, rel_tol=1e-6)

def test_newton_raphson_no_solution():
    # Функция с нулевой производной
    f = lambda x: x**3
    df = lambda x: 3 * x**2
    with pytest.raises(ValueError):
        AdvancedMath.newton_raphson(f, df, x0=0)

# ----------- Тест с моками (для integrate_trapezoidal) -----------

def test_integrate_trapezoidal_mock():
    # Создаем мок для функции f(x)
    mock_function = Mock(return_value=2)
    result = AdvancedMath.integrate_trapezoidal(mock_function, 0, 10, n=10)
    assert result == 20  # Площадь прямоугольника высотой 2 и шириной 10
    mock_function.assert_called()  # Проверка вызова функции

@pytest.mark.parametrize("f, a, b, n, expected", [
    (lambda x: x, 0, 1, 1000, 0.5),  # Интеграл x от 0 до 1 -> 0.5
    (lambda x: x**2, 0, 3, 1000, 9),  # Интеграл x^2 от 0 до 3 -> 9
])
def test_integrate_trapezoidal_parametrize(f, a, b, n, expected):
    result = AdvancedMath.integrate_trapezoidal(f, a, b, n)
    assert isclose(result, expected, rel_tol=1e-4)
