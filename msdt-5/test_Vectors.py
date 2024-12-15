from unittest.mock import MagicMock

import pytest

from Vectors import Vectors


@pytest.mark.parametrize("size, expected_length", [
    (5, 5),
    (10, 10),
    (-1, 5),  # При некорректной размерности, устанавливается значение по умолчанию (5)
])
def test_vectors_initialization(size, expected_length):
    vector = Vectors(size)
    assert vector.length() == expected_length
    assert all(elem == 0.0 for elem in vector.vector)


def test_get_and_set_elements():
    vector = Vectors(3)
    vector.set_elements(0, 1.5)
    vector.set_elements(1, -2.3)
    vector.set_elements(2, 3.8)

    assert vector.get_elements(0) == 1.5
    assert vector.get_elements(1) == -2.3
    assert vector.get_elements(2) == 3.8

    with pytest.raises(ValueError):
        vector.get_elements(3)  # Некорректный индекс
    with pytest.raises(ValueError):
        vector.set_elements(3, 10)


def test_norm_vector():
    vector = Vectors(3)
    vector.set_elements(0, 3)
    vector.set_elements(1, 4)
    vector.set_elements(2, 0)
    # Евклидова длина вектора (3, 4, 0) равна 5
    assert pytest.approx(vector.norm_vector(), 0.01) == 5.0


def test_search_min_max():
    vector = Vectors(4)
    vector.set_elements(0, -10)
    vector.set_elements(1, 0)
    vector.set_elements(2, 7)
    vector.set_elements(3, -3)

    assert vector.search_min() == -10
    assert vector.search_max() == 7


def test_sorting():
    vector = Vectors(5)
    vector.set_elements(0, 3)
    vector.set_elements(1, -1)
    vector.set_elements(2, 2)
    vector.set_elements(3, -5)
    vector.set_elements(4, 0)

    vector.ascending_sort()
    assert vector.vector == [-5, -1, 0, 2, 3]

    vector.descending_sort()
    assert vector.vector == [3, 2, 0, -1, -5]


@pytest.mark.parametrize("vec1, vec2, expected", [
    ([1, 2, 3], [4, 5, 6], [5, 7, 9]),
    ([0, 0, 0], [1, -1, 1], [1, -1, 1]),
    ([-1, -2, -3], [-4, -5, -6], [-5, -7, -9]),
])
def test_adding_vectors(vec1, vec2, expected):
    v1 = Vectors(len(vec1))
    v2 = Vectors(len(vec2))

    for i, value in enumerate(vec1):
        v1.set_elements(i, value)
    for i, value in enumerate(vec2):
        v2.set_elements(i, value)

    result = Vectors.adding_vectors(v1, v2)
    assert result.vector == expected


def test_scalar_vectors_mock():
    v1 = MagicMock()
    v2 = MagicMock()
    v1.length.return_value = 3
    v2.length.return_value = 3

    v1.get_elements.side_effect = [1, 2, 3]
    v2.get_elements.side_effect = [4, 5, 6]

    result = Vectors.scalar_vectors(v1, v2)

    # Скалярное произведение (1*4 + 2*5 + 3*6 = 32)
    assert result == 32
    # Проверка, что вызван метод для последнего индекса
    v1.get_elements.assert_called_with(2)

