from unittest.mock import patch

import pytest
from lab5 import *


@pytest.mark.parametrize("array, target, expected", [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 5, (1, 1)),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 7, (2, 0)),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 10, None),
    ([[1]], 1, (0, 0)),
    ([], 1, None),
])
def test_find_in_2d_array_simple(array, target, expected):
    assert find_in_2d_array(array, target) == expected


@patch('builtins.enumerate')
def test_find_in_2d_array_with_mock(mock_enumerate):
    # Мокаем стандартное поведение enumerate
    def mocked_enumerate(iterable, start=0):
        return zip(range(start, start + len(iterable)), iterable)
    mock_enumerate.side_effect = mocked_enumerate
    array = [['a', 'b', 'c'], ['d', 'e', 'f']]
    target = 'e'
    expected = (1, 1)
    assert find_in_2d_array(array, target) == expected
    mock_enumerate.assert_called()


@pytest.mark.parametrize("array, target, expected", [
    ([[1, 1, 1, 1], [1, 1, 2, 1], [1, 1, 1, 1]], 2, (1, 2)),
    ([[5] * 1000 for _ in range(1000)], 5, (0, 0)),
])
def test_find_in_2d_array_complex(array, target, expected):
    assert find_in_2d_array(array, target) == expected


def test_find_in_2d_array_negative():
    array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    target = -1
    assert find_in_2d_array(array, target) is None


def test_find_in_2d_array_edge_case():
    array = [[1, "two", 3], [4, 5, "six"], [7, 8, 9]]
    target = "six"
    assert find_in_2d_array(array, target) == (1, 2)


def test_find_in_2d_array_first_occurrence():
    array = [
        [1, 2, 3],
        [4, 5, 3],
        [7, 8, 3]
    ]
    target = 3
    expected = (0, 2)
    assert find_in_2d_array(array, target) == expected


@pytest.mark.parametrize("array, target, expected", [
    ([[None, None, None], [None, None, None]], None, (0, 0)),
    ([[True, False], [False, True]], True, (0, 0)),
])
def test_find_in_2d_array_special(array, target, expected):
    assert find_in_2d_array(array, target) == expected