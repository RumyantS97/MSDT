import pytest
from collections import deque
from lab5 import reverse_string, find_anagrams, compress, decompress, bfs # Замените your_module на имя вашего файла

# Тесты для reverse_string
def test_reverse_string_empty():
    assert reverse_string("") == ""

def test_reverse_string_single_char():
    assert reverse_string("a") == "a"

def test_reverse_string_palindrome():
    assert reverse_string("madam") == "madam"

def test_reverse_string_normal():
    assert reverse_string("hello") == "olleh"


# Параметризованные тесты для find_anagrams
@pytest.mark.parametrize("text, word, expected", [
    ("listen", "silent", ['listen']),
    ("abcba", "abc", ['abc', 'cba']), # Нет анаграмм
    ("elbow", "below", ['elbow']),
    ("rail safety", "fairy tales", ['rail safety']),
    ("conversation", "conservation", ['conversation'])
])
def test_find_anagrams(text, word, expected):
    assert find_anagrams(text, word) == expected

@pytest.mark.parametrize("input_str, expected", [
    ("hello", "olleh"),
    ("", ""),
    ("a", "a"),
    ("abcd", "dcba"),
])
def test_reverse_string(input_str, expected):
    assert reverse_string(input_str) == expected


@pytest.mark.parametrize("text, word, expected", [
    ("listen silent", "listen", ['listen', 'silent']),
    ("abc cba", "abc", ["abc", "cba"]),
    ("hello world", "world", ["world"]),
    ("aabbcc", "abc", []),  # Не все анаграммы будут найдены
])
def test_find_anagrams(text, word, expected):
    assert find_anagrams(text, word) == expected

# Тесты для compress
def test_compress_single_char():
    assert compress("a") == "a1"

def test_compress_repeated_chars():
    assert compress("aaabbccc") == "a3b2c3"

def test_compress_mixed_chars():
    assert compress("abbccaaa") == "a1b2c2a3"


# Тесты для decompress (Обратный тест для compress)
def test_decompress_empty():
    assert decompress("") == ""

def test_decompress_single_char():
    assert decompress("a1") == "a"

def test_decompress_repeated_chars():
    assert decompress("a3b2c3") == "aaabbccc"

def test_decompress_mixed_chars():
    assert decompress("a1b2c2a3") == "abbccaaa"


# Параметризованные тесты для bfs
@pytest.mark.parametrize("graph, start, expected", [
    ({'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': [], 'F': []}, 'A', {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2}),
    ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', {'A': 0, 'B': 1, 'C': 2, 'D': 3}),
    ({'A': [],}, 'A', {'A': 0}) # Граф с одной вершиной
])
def test_bfs(graph, start, expected):
    assert bfs(graph, start) == expected

@pytest.mark.parametrize("compressed_str, expected", [
    ("a3b2c1", "aaabbc"),
    ("a1b1c1d1", "abcd"),
    ("", ""),
    ("a3", "aaa"),
])
def test_decompress(compressed_str, expected):
    assert decompress(compressed_str) == expected


@pytest.mark.parametrize("graph, start, expected", [
    ({"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": ["G"], "E": ["F"], "F": [], "G": []}, 'A',
     {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 3}),
])
def test_bfs(graph, start, expected):
    assert bfs(graph, start) == expected
