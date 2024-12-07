import pytest
from collections import deque


# Ваши функции
def reverse_string(string):
    if not string:
        return ""

    reversed_string = ""

    for i in range(len(string) - 1, -1, -1):
        reversed_string += string[i]

    return reversed_string


def find_anagrams(text, word):
    word_dict = {}
    for char in word:
        word_dict[char] = word_dict.get(char, 0) + 1

    anagrams = []

    for i in range(len(text) - len(word) + 1):
        text_dict = {}
        for j in range(i, i + len(word)):
            text_dict[text[j]] = text_dict.get(text[j], 0) + 1

        if text_dict == word_dict:
            anagrams.append(text[i:i + len(word)])

    return anagrams


def compress(string):
    compressed_string = []
    if not string:  # Добавлено для обработки пустой строки
        return ""

    current_char = string[0]
    count = 1

    for char in string[1:]:
        if char == current_char:
            count += 1
        else:
            compressed_string.append(current_char + str(count))
            current_char = char
            count = 1

    compressed_string.append(current_char + str(count))

    return ''.join(compressed_string)


def decompress(compressed_string):
    decompressed_string = []
    i = 0
    while i < len(compressed_string):
        char = compressed_string[i]
        i += 1
        count = ""
        while i < len(compressed_string) and compressed_string[i].isdigit():
            count += compressed_string[i]
            i += 1

        if count:
            count = int(count)

        decompressed_string.append(char * count)

    return ''.join(decompressed_string)


def bfs(graph, start):
    result = {start: 0}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in result:
                result[neighbor] = result[vertex] + 1
                queue.append(neighbor)
    return result


# Параметризованные тесты
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


@pytest.mark.parametrize("input_str, expected", [
    ("aaabbc", "a3b2c1"),
    ("abcd", "a1b1c1d1"),
    ("", ""),
    ("aaa", "a3"),
])
def test_compress(input_str, expected):
    assert compress(input_str) == expected


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