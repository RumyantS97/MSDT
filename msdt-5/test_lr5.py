
import pytest
from unittest.mock import patch
from lr5 import word_count, unique_words, filter_words_by_length, most_common_words, generate_summary

# Тест с параметром
@pytest.mark.parametrize('text, result',
                         [("a b c d e e b g", 6), 
                          ("a b b", 2), 
                          ("apple strawberry cherry orange potato", 5)])
def test_unique_wordss(text, result):
    # Используем функцию `unique_words` для получения количества уникальных слов
    assert len(unique_words(text)) == result

def test_word_count():
    text = "apple orange apple banana banana banana"
    result = word_count(text)
    assert result == {"apple": 2, "orange": 1, "banana": 3}

def test_unique_words():
    text = "hello world hello"
    result = unique_words(text)
    assert result == {"hello", "world"}

def test_filter_words_by_length():
    words = ["hello", "world", "a", "test"]
    result = filter_words_by_length(words, 4)
    assert result == ["hello", "world", "test"]

    with pytest.raises(ValueError):
        filter_words_by_length(words, -1)

def test_most_common_words():
    text = "apple orange apple banana banana banana"
    result = most_common_words(text, 2)
    assert result == [("banana", 3), ("apple", 2)]

    result = most_common_words(text, 1)
    assert result == [("banana", 3)]

def test_generate_summary():
    text = "This is a test text for generating a summary."
    result = generate_summary(text, 20)
    assert result == "This is a test text..."

    result = generate_summary(text, 50)
    assert result == text

def test_combined_analysis():
    """Сложный тест: анализ текста с использованием нескольких функций."""
    text = "apple orange apple banana banana banana"
    unique = unique_words(text)
    most_common = most_common_words(text, 2)
    filtered = filter_words_by_length(list(unique), 6)  # Фильтруем слова, длина которых >= 6

    assert "banana" in unique
    assert most_common == [("banana", 3), ("apple", 2)]
    
    # Сортируем оба списка перед сравнением, чтобы не учитывать порядок
    assert sorted(filtered) == sorted(["banana", "orange"])

def test_edge_cases():
    """Сложный тест: проверка граничных случаев."""
    empty_text = ""
    assert word_count(empty_text) == {}
    assert unique_words(empty_text) == set()
    assert most_common_words(empty_text) == []
    
    with pytest.raises(ValueError):
        filter_words_by_length(["a", "b"], 0)


def test_most_common_words_with_mock():
    """Тест с использованием мока для функции most_common_words"""
    mock_unique_words = ["apple", "orange", "banana"]

    with patch("lr5.unique_words", return_value=mock_unique_words):  # Путь к функции через строку
        text = "apple orange apple banana banana banana"
        result = most_common_words(text, 2)
        
        # Проверяем, что функция использует мокированные данные
        assert ("banana", 3) in result
        assert ("apple", 2) in result
        assert len(result) == 2