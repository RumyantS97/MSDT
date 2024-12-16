import pytest
from MathSolver import MathSolver  # Предполагается, что ваш класс в файле math_solver.py
import math

@pytest.fixture
def solver():
    return MathSolver()

# Тесты для квадратного уравнения
def test_solve_quadratic_real_roots(solver):
    assert solver.solve_quadratic(1, -3, 2) == (2.0, 1.0)

def test_solve_quadratic_one_root(solver):
    assert solver.solve_quadratic(1, -2, 1) == (1.0,)

def test_solve_quadratic_no_real_roots(solver):
    assert solver.solve_quadratic(1, 0, 1) == "Нет действительных корней"

# Тесты для факториала
def test_factorial_positive(solver):
    assert solver.factorial(5) == 120

def test_factorial_zero(solver):
    assert solver.factorial(0) == 1

def test_factorial_negative(solver):
    assert solver.factorial(-5) == "Факториал отрицательного числа не определен"

# Тесты для кубического уравнения
def test_solve_cubic_one_root(solver):
    assert solver.solve_cubic(1, -6, 11, -6) == (3.0,)

def test_solve_cubic_three_real_roots(solver):
    roots = solver.solve_cubic(1, -3, 3, -1)
    assert len(roots) == 3
    assert all(isinstance(root, complex) for root in roots[1:])

# Параметризованный тест для модуля
@pytest.mark.parametrize("input_value, expected_output", [
    (10, 10),
    (-10, 10),
    (0, 0),
])
def test_modulus(solver, input_value, expected_output):
    assert solver.modulus(input_value) == expected_output

# Параметризованный тест для квадратного корня
@pytest.mark.parametrize("input_value, expected_output", [
    (16, 4),
    (0, 0),
    (-4, "Квадратный корень из отрицательного числа не определен"),
])
def test_square_root(solver, input_value, expected_output):
    assert solver.square_root(input_value) == expected_output

# Мок для проверки котангенса
from unittest.mock import patch

@patch('math.tan')
def test_cotangent_mocked(mock_tan, solver):
    mock_tan.return_value = 1  # tan(pi/4) = 1
    assert solver.cotangent(math.pi / 4) == 1.0

@patch('math.tan')
def test_cotangent_undefined(mock_tan, solver):
    mock_tan.return_value = 0  # tan(angle) = 0 (например, angle = 0)
    assert solver.cotangent(0) == "Котангенс не определен"

# Тест для тангенса
def test_tangent(solver):
    assert solver.tangent(math.pi / 4) == 1.0