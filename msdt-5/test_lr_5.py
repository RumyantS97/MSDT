import pytest
from unittest.mock import patch
from lr_5 import naive, kmp, find_palindrom, huffman, find_cycle


# Тест для наивного алгоритма поиска строк
@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        ("hello world", "world", [6]),
        ("aaaaa", "aa", [0, 1, 2, 3]),
        ("abcdef", "gh", []),
    ],
)
def test_naive(text, pattern, expected):
    assert naive(text, pattern) == expected


# Тест для алгоритма Кнута-Морриса-Пратта поиска строк
@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        ("abracadabra", "abra", [0, 7]),
        ("mississippi", "iss", [1, 4]),
        ("test", "no", []),
    ],
)
def test_kmp(text, pattern, expected):
    assert kmp(text, pattern) == expected


# Тест для поиска палиндромов
@pytest.mark.parametrize(
    "text, expected",
    [
        ("abba", ["a", "b", "b", "a", "bb", "abba"]),
        ("racecar", ["r", "a", "c", "e", "c", "a", "r", "cec", "aceca", "racecar"]),
        ("abc", ["a", "b", "c"]),
    ],
)
def test_find_palindrom(text, expected):
    result = find_palindrom(text)
    assert sorted(result) == sorted(expected)


# Тест для алгоритма Хаффмана
def test_huffman():
    text = "aaabbc"
    result = huffman(text)
    assert result == [["a", "0"], ["b", "11"], ["c", "10"]]


# Тест для цикла в графе
def test_find_cycle():
    graph_with_cycle = [[1], [2], [0]]
    graph_without_cycle = [[1], [2], []]

    assert find_cycle(graph_with_cycle) is True
    assert find_cycle(graph_without_cycle) is False


# Мок для алгоритма Хаффмана
@patch("lr_5.huffman")
def test_huffman_with_mock_patch(mock_huffman):
    mock_huffman.return_value = {"a": 5, "b": 3, "c": 2}
    text = "aaabbc"
    result = huffman(text)
    expected_result = [["a", "0"], ["b", "11"], ["c", "10"]]
    assert result == expected_result


#  Комбинация KMP и naive
@pytest.mark.parametrize("algorithm", [naive, kmp])
def test_large_text(algorithm):
    text = "a" * 1000 + "b"
    pattern = "a" * 100 + "b"
    result = algorithm(text, pattern)
    assert result == [900]
