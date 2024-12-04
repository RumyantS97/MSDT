import pytest
from pytest import approx

from main import (
    add_matrices, subtract_matrices, transpose_matrix,
    multiply_matrices, is_square_matrix, scalar_multiply_matrix,
    trace_matrix, determinant_matrix, inverse_matrix, identity_matrix
)


def test_inverse_matrix():
    matrix = [[2, 0], [0, 2]]
    expected = [[0.5, 0.0], [0.0, 0.5]]
    assert inverse_matrix(matrix) == expected


@pytest.mark.parametrize("matrix1, matrix2, expected", [
    ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[6, 8], [10, 2]]),
    ([[0, 0], [0, 0]], [[1, 1], [1, 1]], [[1, 1], [1, 1]]),
])
def test_add_matrices(matrix1, matrix2, expected):
    assert add_matrices(matrix1, matrix2) == expected


@pytest.mark.parametrize("matrix1, matrix2, expected", [
    ([[1, 2], [3, 4]], [[1, 0], [0, 1]], [[1, 2], [3, 4]]),
    ([[2, 0], [1, 3]], [[1, 2], [0, 1]], [[2, 4], [1, 5]]),
])
def test_multiply_matrices(matrix1, matrix2, expected):
    assert multiply_matrices(matrix1, matrix2) == expected


@pytest.mark.parametrize("matrix1, matrix2, expected", [
    ([[5, 6], [7, 8]], [[1, 2], [3, 4]], [[4, 4], [4, 4]]),
    ([[1, 1], [1, 1]], [[0, 0], [0, 0]], [[1, 1], [1, 1]]),
])
def test_subtract_matrices(matrix1, matrix2, expected):
    assert subtract_matrices(matrix1, matrix2) == expected


def test_subtract_matrices_invalid():
    with pytest.raises(ValueError):
        subtract_matrices([[1, 2]], [[1]])


@pytest.mark.parametrize("matrix, expected", [
    ([[1, 2], [3, 4]], 5),
    ([[5, 0], [0, 3]], 8),
])
def test_trace_matrix(matrix, expected):
    assert trace_matrix(matrix) == expected


def test_trace_matrix_invalid():
    with pytest.raises(ValueError):
        trace_matrix([[1, 2, 3], [4, 5, 6]])


def test_is_square_matrix():
    assert is_square_matrix([[1, 2], [3, 4]]) is True
    assert is_square_matrix([[1, 2, 3], [4, 5, 6]]) is False


@pytest.mark.parametrize("matrix, scalar, expected", [
    ([[1, 2], [3, 4]], 2, [[2, 4], [6, 8]]),
    ([[0, 0], [0, 0]], 10, [[0, 0], [0, 0]]),
])
def test_scalar_multiply_matrix(matrix, scalar, expected):
    assert scalar_multiply_matrix(matrix, scalar) == expected


def test_determinant_matrix():
    matrix = [[1, 2], [3, 4]]
    assert determinant_matrix(matrix) == -2

    with pytest.raises(ValueError):
        determinant_matrix([[1, 2, 3], [4, 5, 6]])


def test_identity_matrix():
    assert identity_matrix(2) == [[1, 0], [0, 1]]
    assert identity_matrix(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def test_inverse_matrix_real():
    matrix = [[4, 7], [2, 6]]
    expected = [[0.6, -0.7], [-0.2, 0.4]]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            assert inverse_matrix(matrix)[i][j] == approx(
                expected[i][j], rel=1e-9)


@pytest.mark.parametrize("matrix, expected", [
    ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
    ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
])
def test_transpose_matrix(matrix, expected):
    assert transpose_matrix(matrix) == expected
