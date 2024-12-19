import numpy as np
import pytest
from unittest.mock import patch
from features import (find_nearest, find_all_minima, find_all_maxima,
                      maxima_in_range, minima_in_range,
                      find_local_maxima, find_local_minima)


@pytest.mark.parametrize("array, value, expected_index, expected_value", [
    ([0, 1, 2, 3, 4], 3.2, 3, 3),
    ([10, 20, 30, 40, 50], 25, 1, 20),
    ([0.1, 0.5, 0.9, 1.5], 0.75, 2, 0.9),  
])
def test_find_nearest(array, value, expected_index, expected_value):
    idx, val = find_nearest(array, value)
    assert idx == expected_index
    assert val == expected_value


def test_find_all_minima():
    arr = [3, 2, 1, 2, 3]
    expected = [2]
    result = find_all_minima(arr)
    assert result.tolist() == expected


def test_find_all_maxima():
    arr = [1, 3, 2, 3, 1, 5, 4]
    expected = [1, 3, 5]
    result = find_all_maxima(arr)
    assert result.tolist() == expected


@pytest.mark.parametrize("r, g_r, r_min, r_max, expected", [
    (np.array([1, 2, 3, 4]), np.array([10, 15, 5, 20]), 2, 4, (4, 20)),
])
def test_maxima_in_range(r, g_r, r_min, r_max, expected):
    result = maxima_in_range(r, g_r, r_min, r_max)
    assert result == expected


@pytest.mark.parametrize("r, g_r, r_min, r_max, expected", [
    (np.array([1, 2, 3, 4]), np.array([10, 15, 5, 20]), 2, 4, (3, 5)),
])
def test_minima_in_range(r, g_r, r_min, r_max, expected):
    result = minima_in_range(r, g_r, r_min, r_max)
    assert result == expected


def test_find_local_maxima():
    r = np.array([1, 2, 3, 4, 5])
    g_r = np.array([10, 15, 5, 20, 10])
    r_guess = 2
    result = find_local_maxima(r, g_r, r_guess)
    assert result == (2, 15)


def test_find_local_minima_with_mock():
    r = np.array([1, 2, 3, 4, 5])
    g_r = np.array([10, 5, 15, 0, 20])
    r_guess = 2
    with patch("features.find_all_minima", return_value=[1, 3]):
        result = find_local_minima(r, g_r, r_guess)
        assert result == (2, 5)  
