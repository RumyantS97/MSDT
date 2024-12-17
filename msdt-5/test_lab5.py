import unittest
from unittest.mock import patch

from lab5 import CharacterFinder
from parameterized import parameterized

class TestCharacterFinder(unittest.TestCase):

    # Примитивные тесты
    def test_find_character_in_middle(self):
        input_str = "window"
        target = 'n'
        expected_index = 2
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_find_character_at_beginning(self):
        input_str = "apple"
        target = 'a'
        expected_index = 0
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_find_character_at_end(self):
        input_str = "helloo"
        target = 'o'
        expected_index = 4
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_character_not_found(self):
        input_str = "android"
        target = 'z'
        expected_index = -1
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_empty_string(self):
        input_str = ""
        target = 'a'
        expected_index = -1
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_case_sensitivity(self):
        input_str = "Hello"
        target = 'h'
        expected_index = -1
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_string_with_spaces(self):
        input_str = "h e l l o"
        target = 'e'
        expected_index = 2
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_long_string(self):
        input_str = "a" * 999 + "b"
        target = 'b'
        expected_index = 999
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    def test_utf8_character(self):
        input_str = "fire 🔥"
        target = "🔥"
        expected_index = input_str.index(target)
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    @parameterized.expand([
        ("test_find_character_in_middle", "window", 'n', 2),
        ("test_find_character_at_beginning", "apple", 'a', 0),
        ("test_find_character_at_end", "helloo", 'o', 4),
        ("test_character_not_found", "android", 'z', -1),
        ("test_empty_string", "", 'a', -1),
    ])
    def test_find_character(self, name, input_str, target, expected_index):
        self.assertEqual(expected_index, CharacterFinder.find_character(input_str, target))

    @patch.object(CharacterFinder, 'fetch_data_from_server', return_value="mocked response")
    def test_find_character_from_url_with_mock(self, mock_fetch):
        url = "http://example.com"
        target = 'r'
        expected_index = 7

        result = CharacterFinder.find_character_from_url(url, target)
        self.assertEqual(result, expected_index)