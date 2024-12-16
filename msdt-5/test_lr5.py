import pytest
from collections import Counter
from unittest.mock import patch
from lr5 import (
    count_characters,
    count_words,
    count_sentences,
    count_unique_words,
    word_frequencies,
    most_common_words,
    average_word_length,
    average_sentence_length,
    count_paragraphs,
    analyze_text
)

@pytest.mark.parametrize("text, expected", [
    ("Hello world", 11),
    ("", 0),
    (" \n\t", 3)
])
def test_count_characters(text, expected):
    assert count_characters(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello world", 2),
    ("", 0),
    ("Hello, wonderful world!", 3)
])
def test_count_words(text, expected):
    assert count_words(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello. World.", 2),
    ("", 0),
    ("This is a test. Is it working?", 2)
])
def test_count_sentences(text, expected):
    assert count_sentences(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello hello world", 2),
    ("", 0),
    ("A, a, b, c, c, c!", 3)
])
def test_count_unique_words(text, expected):
    assert count_unique_words(text) == expected

def test_word_frequencies():
    text = "Hello world! Hello again, world."
    expected = {"hello": 2, "world": 2, "again": 1}
    assert word_frequencies(text) == expected

@pytest.mark.parametrize("text, n, expected", [
    ("apple apple banana orange orange orange", 2, [("orange", 3), ("apple", 2)]),
    ("", 3, []),
    ("one two three", 1, [("one", 1)])
])
def test_most_common_words(text, n, expected):
    assert most_common_words(text, n) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello world", 5.0),
    ("", 0),
    ("A long sentence", 4.333333333333333)
])
def test_average_word_length(text, expected):
    assert average_word_length(text) == pytest.approx(expected)

@pytest.mark.parametrize("text, expected", [
    ("Hello world. Hi again.", 2.0),
    ("", 0),
    ("One sentence", 2.0)
])
def test_average_sentence_length(text, expected):
    assert average_sentence_length(text) == pytest.approx(expected)

@pytest.mark.parametrize("text, expected", [
    ("Hello\nWorld", 2),
    ("", 0),
    ("Paragraph one.\n\nParagraph two.", 2)
])
def test_count_paragraphs(text, expected):
    assert count_paragraphs(text) == expected

def test_analyze_text():
    text = "Hello world. Hello again."
    analysis = analyze_text(text)
    assert analysis["character_count"] == 25
    assert analysis["word_count"] == 4
    assert analysis["unique_word_count"] == 3
    assert analysis["sentence_count"] == 2
    assert analysis["paragraph_count"] == 1
    assert analysis["average_word_length"] == pytest.approx(5.0)
    assert analysis["average_sentence_length"] == pytest.approx(2.0)
    assert analysis["most_common_words"] == [("hello", 2), ("world", 1), ("again", 1)]

@patch("lr5.word_frequencies")
def test_most_common_words_mock(mock_word_frequencies):
    mock_word_frequencies.return_value = Counter({"test": 10, "mock": 5})
    assert most_common_words("irrelevant", 1) == [("test", 10)]
    mock_word_frequencies.assert_called_once()

@patch("lr5.count_characters", return_value=42)
def test_analyze_text_with_mock(mock_count_characters):
    text = "Dummy text"
    analysis = analyze_text(text)
    assert analysis["character_count"] == 42
    mock_count_characters.assert_called_once_with(text)
