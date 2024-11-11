import pytest
from unittest import mock
from code_lr5 import (
    naive_algorithm, kmp, find_palindromes, count_palindromes_in_string,
    build_huffman_tree, get_huffman_codes,
    compress_data, decompress_data, has_cycle
)

# Tests for substring search algorythms
@pytest.mark.parametrize("s, p, expected", [
    ("hello world", "world", 6),
    ("abcde", "cde", 2),
    ("aaaaa", "aaa", 0),
    ("abcdef", "gh", -1),
    ("test", "", 0),  # Empty substring
])
def test_naive_algorithm(s, p, expected):
    assert naive_algorithm(s, p) == expected

@pytest.mark.parametrize("s, p, expected", [
    ("hello world", "world", 6),
    ("abcde", "cde", 2),
    ("aaaaa", "aaa", 0),
    ("abcdef", "gh", -1),
    ("test", "", 0),  # Empty substring
])
def test_kmp(s, p, expected):
    assert kmp(s, p) == expected


# Tests for finding palindromes
@pytest.mark.parametrize("input_str, expected", [
    ("abba", ["abba", "bb"]),
    ("racecar", ["racecar", "aceca", "cec"]),
    ("noon", ["noon", "oo"]),
    ("abc", []),
    ("", [])
])
def test_find_palindromes_param(input_str, expected):
    assert find_palindromes(input_str) == expected


@mock.patch('code_lr5.find_palindromes')
def test_count_palindromes_in_string(mock_find_palindromes):
    # Setting the mock
    mock_find_palindromes.return_value = ["abba", "racecar"]

    # Calling the testing function
    result = count_palindromes_in_string("abba racecar no lemon no melon")

    assert result == 2  # Expecting 2 palindromes to be found

    # Checking that the mock was called with the expected argument
    mock_find_palindromes.assert_called_with("abba racecar no lemon no melon")


# Tests for Huffman coding
@pytest.fixture
def symbols_freq():
    return {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}

@pytest.fixture
def huffman_tree(symbols_freq):
    return build_huffman_tree(symbols_freq)

@pytest.mark.parametrize("text, expected_length", [
    ("abc", 5),
    ("", 0),  # Empty string
    ("a" * 100, 100)  # Long text
])
def test_compress_data(symbols_freq, text, expected_length):
    tree = build_huffman_tree(symbols_freq)
    codes = get_huffman_codes(tree)
    compressed = compress_data(text, codes)
    assert len(compressed) >= expected_length

@pytest.mark.parametrize("text", [
    "abc",
    "aaaa",
    "abcdef",
    ""
])
def test_compress_and_decompress(symbols_freq, text):
    tree = build_huffman_tree(symbols_freq)
    codes = get_huffman_codes(tree)
    compressed = compress_data(text, codes)
    assert decompress_data(compressed, codes) == text


# Tests for the algorithm for determining cycles in a graph
@pytest.fixture
def cyclic_graph():
    return {0: [1], 1: [2], 2: [0]}

@pytest.fixture
def acyclic_graph():
    return {0: [1], 1: [2], 2: []}

def test_has_cycle(cyclic_graph):
    assert has_cycle(cyclic_graph) is True

def test_no_cycle(acyclic_graph):
    assert has_cycle(acyclic_graph) is False

@mock.patch('code_lr5.dfs', return_value=True)
def test_dfs_cycle_detection(mock_dfs, cyclic_graph):
    assert has_cycle(cyclic_graph) is True
    assert mock_dfs.called  # Checking the dfs function was called

def test_invalid_graph_structure():
    invalid_graph = {0: [1], 1: "not a list"}
    with pytest.raises(TypeError):
        has_cycle(invalid_graph)
