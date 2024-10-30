import pytest
from unittest.mock import patch
from collections import deque

from LR02 import check_brackets, MinStack, max_in_window, find_duplicates, zero_matrix


# Задание 1
@pytest.mark.parametrize("input_str,expected", [
    ("((()))", True),
    ("({)}", False),
    ("[]", True),
    ("[({})]", True),
    ("[({})", False),
])
def test_check_brackets(input_str, expected):
    assert check_brackets(input_str) == expected

# Задание 2
def test_min_stack():
    stack = MinStack()
    stack.push(3)
    stack.push(5)
    stack.push(2)
    stack.push(1)

    assert stack.min() == 1

    stack.pop()
    assert stack.min() == 2

    stack.pop()
    stack.pop()
    assert stack.min() == 3

# Задание 3
@pytest.mark.parametrize("arr,k,expected", [
    ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
    ([4, 3, 5, 1, -1, 0, 2], 4, [5, 5, 5, 2]),
    ([2, 2, 2, 2, 2], 2, [2, 2, 2, 2])
])
def test_max_in_window(arr, k, expected):
    assert max_in_window(arr, k) == expected

# Использование mock для функции max_in_window
def test_max_in_window_mock():
    with patch('deque', return_value=deque([1, 3, 5])) as mock_deque:
        arr = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        max_in_window(arr, k)
        mock_deque.assert_called()  # Проверяем, что deque был вызван

# Задание 4
@pytest.mark.parametrize("nums,expected", [
    ([1, 3, 4, 2, 2], 2),
    ([3, 1, 3, 4, 2], 3),
    ([1, 1], 1),
])
def test_find_duplicates(nums, expected):
    assert find_duplicates(nums) == expected

# Задание 5
@pytest.mark.parametrize("matrix,expected", [
    (
        [
            [1, 2, 3],
            [4, 0, 6],
            [7, 8, 9]
        ],
        [
            [1, 0, 3],
            [0, 0, 0],
            [7, 0, 9]
        ]
    ),
    (
        [
            [0, 2, 3],
            [4, 1, 3],
            [3, 8, 0]
        ],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    )
])
def test_zero_matrix(matrix, expected):
    assert zero_matrix(matrix) == expected

# Дополнительный тест для zero_matrix с проверкой на неизменные строки/столбцы
def test_zero_matrix_stab():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    assert zero_matrix(matrix) == matrix  # Ожидаем, что если нет 0, матрица не меняется
