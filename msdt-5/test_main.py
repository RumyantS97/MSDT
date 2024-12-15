import pytest
import numpy as np
from unittest.mock import MagicMock, patch

from main import (
    polynomial, numericalIntegration, differentialEquationSolver,
    optimizer, matrixOperations, statistics, square_of_sine, ode_function
)


@pytest.mark.parametrize(
    "coefficients, x, expected",
    [
        ([1, -3, 2], 0, 2),  
        ([1, -3, 2], 1, 0), 
        ([1, 1], 2, 3)      
    ]
)
def test_polynomial_evaluate(coefficients, x, expected):
    poly = polynomial(coefficients)
    assert poly.evaluate(x) == pytest.approx(expected)


@pytest.mark.parametrize(
    "coeff1, coeff2, expected_sum",
    [
        ([1, -3, 2], [1, 1], [1, -2, 3]),
        ([0, 0, 1], [1, -1], [0, 1, 0])
    ]
)
def test_polynomial_add(coeff1, coeff2, expected_sum):
    poly1 = polynomial(coeff1)
    poly2 = polynomial(coeff2)
    result = poly1 + poly2
    assert np.array_equal(result.coefficients, expected_sum)


def test_polynomial_roots():
    poly = polynomial([1, -3, 2])
    roots = poly.roots()
    assert np.allclose(roots, [2, 1])


def test_numerical_integration():
    result = numericalIntegration.integrate(square_of_sine, 0, np.pi)
    expected = np.pi / 2
    assert result == pytest.approx(expected)


def test_optimizer_minimize():
    def func_to_minimize(x):
        return (x - 3) ** 2 + 1

    result = optimizer.minimize_function(func_to_minimize, [0])
    assert result.success
    assert result.x[0] == pytest.approx(3, rel=1e-3)
    assert result.fun == pytest.approx(1, rel=1e-3)


def test_matrix_operations():
    matrix_a = [[4, 2], [3, 1]]
    matrix_op = matrixOperations(matrix_a)

    assert np.array_equal(matrix_op.transpose(), np.array([[4, 3], [2, 1]]))

    assert matrix_op.determinant() == pytest.approx(-2)

    inverse = matrix_op.inverse()
    expected_inverse = np.array([[-0.5, 1], [1.5, -2]])
    assert np.allclose(inverse, expected_inverse)


@pytest.mark.parametrize(
    "data, expected_mean",
    [
        ([1, 2, 3, 4, 5], 3),
        ([10, 20, 30, 40, 50], 30)
    ]
)
def test_statistics_mean(data, expected_mean):
    assert statistics.mean(data) == pytest.approx(expected_mean)


@pytest.mark.parametrize(
    "data, expected_variance",
    [
        ([1, 2, 3, 4, 5], 2.0),
        ([10, 20, 30, 40, 50], 200.0)
    ]
)
def test_statistics_variance(data, expected_variance):
    assert statistics.variance(data) == pytest.approx(expected_variance)


@patch("main.quad")
def test_numerical_integration_mock(mock_quad):
    mock_quad.return_value = (1.57, None) 
    result = numericalIntegration.integrate(square_of_sine, 0, np.pi)
    mock_quad.assert_called_once_with(square_of_sine, 0, np.pi)
    assert result == pytest.approx(1.57)


@patch("main.solve_ivp")
def test_differential_solver_mock(mock_solve_ivp):
    mock_solution = MagicMock()
    mock_solution.t = [0, 1, 2]
    mock_solution.y = [[0, 0.5, 1.0]]
    mock_solve_ivp.return_value = mock_solution

    result = differentialEquationSolver.solve_ode(ode_function, [0], (0, 5), [0, 1, 2])
    mock_solve_ivp.assert_called_once_with(ode_function, (0, 5), [0], t_eval=[0, 1, 2])
    assert result.t == [0, 1, 2]
    assert result.y == [[0, 0.5, 1.0]]


@patch("main.minimize")
def test_optimizer_minimize_mock(mock_minimize):
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.x = [3]
    mock_result.fun = 1
    mock_minimize.return_value = mock_result

    def func_to_minimize(x):
        return (x - 3) ** 2 + 1

    result = optimizer.minimize_function(func_to_minimize, [0])
    mock_minimize.assert_called_once_with(func_to_minimize, [0])
    assert result.success is True
    assert result.x[0] == pytest.approx(3)
    assert result.fun == pytest.approx(1)
