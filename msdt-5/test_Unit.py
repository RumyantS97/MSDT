import pytest
from collections import Counter
from unittest.mock import Mock
from LR_05 import (
    Node, find_loop_start, copy_list, remove_duplicates,
    reverse_string, find_anagrams, compress_string, decompress_string, bfs
)

# Тест для функции find_loop_start без цикла
def test_find_loop_start_no_loop():
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    assert find_loop_start(node1) is None  # Ожидаем отсутствие цикла

# Тест для функции find_loop_start с циклом
def test_find_loop_start_with_loop():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node1.next = node2
    node2.next = node3
    node3.next = node1  # Создаем цикл
    assert find_loop_start(node1) == node1  # Ожидаем, что цикл начинается с node1


# Тест для функции copy_list с указателями random
def test_copy_list_with_random():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node1.next = node2
    node2.next = node3
    node1.random = node3
    node2.random = node1
    node3.random = node2

    copied_list = copy_list(node1)  # Копируем список
    assert copied_list.value == node1.value
    assert copied_list.random.value == node1.random.value
    assert copied_list.next.random.value == node2.random.value  # Проверка корректности указателей random


# Тест для функции remove_duplicates
def test_remove_duplicates():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(1)
    node4 = Node(3)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    remove_duplicates(node1)  # Удаляем дубликаты
    assert node1.next.value == 2
    assert node1.next.next.value == 3  # Проверяем, что остались только уникальные значения


# Параметризованный тест для функции reverse_string
@pytest.mark.parametrize("input_string,expected_output", [
    ("hello", "olleh"),
    ("abcd", "dcba"),
    ("", ""),
])
def test_reverse_string(input_string, expected_output):
    assert reverse_string(input_string) == expected_output  # Проверка переворота строки


# Параметризованный тест для функции find_anagrams
@pytest.mark.parametrize("word,text,expected_output", [
    ("abc", "cbabcacab", ["cba", "abc", "bca"]),
    ("abc", "abcdcba", ["cba"]),
    ("aab", "aabaab", ["aab", "aba", "aab"]),
])
def test_find_anagrams(word, text, expected_output):
    assert find_anagrams(word, text) == expected_output  # Проверка нахождения анаграмм в тексте


# Тест для функций compress_string и decompress_string
def test_compress_and_decompress_string():
    s = "aaabbcccc"
    compressed = compress_string(s)
    assert compressed == "a3b2c4"  # Проверка на сжатие строки

    decompressed = decompress_string(compressed)
    assert decompressed == s  # Проверка на восстановление исходной строки


# Тест для функции bfs с использованием mock-объекта
def test_bfs_with_mock():
    graph_mock = Mock()
    graph_mock.__getitem__.side_effect = lambda x: {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }[x]
    start_node = 'A'
    assert bfs(graph_mock, start_node) == ['A', 'B', 'C', 'D', 'E', 'F']  # Проверка на корректность обхода графа
