import random

def generate_random_text(word_count=50):
    """Генерирует случайный текст, состоящий из указанного числа слов."""
    words = [
        "apple", "banana", "orange", "grape", "peach", "pear", "watermelon", "pineapple",
        "cherry", "mango", "strawberry", "blueberry", "kiwi", "plum", "apricot", "papaya",
        "lemon", "melon", "fig", "coconut", "berry", "fruit", "vegetable", "tomato", "carrot",
        "potato", "cucumber", "lettuce", "spinach", "onion", "garlic", "broccoli", "asparagus",
        "artichoke", "zucchini", "cabbage", "peas", "corn", "celery", "squash", "pumpkin",
        "beetroot", "radish", "garlic", "parsnip", "chili", "ginger", "turmeric", "oregano",
        "thyme", "rosemary", "basil", "cilantro", "mint", "sage"
    ]
    
    # Генерация случайного текста
    text = ' '.join(random.choices(words, k=word_count))
    return text

def generate_random_paragraphs(paragraph_count=3, word_count_per_paragraph=50):
    """Генерирует несколько случайных абзацев текста."""
    return '\n\n'.join(generate_random_text(word_count_per_paragraph) for _ in range(paragraph_count))
from collections import Counter

def word_count(text):
    """Возвращает словарь с количеством каждого уникального слова в тексте."""
    words = text.lower().split()
    return dict(Counter(words))

def unique_words(text):
    """Возвращает множество уникальных слов из текста."""
    return set(text.lower().split())

def filter_words_by_length(words, min_length):
    """Фильтрует список слов, возвращая только те, длина которых >= min_length."""
    if not isinstance(min_length, int) or min_length < 1:
        raise ValueError("min_length должен быть положительным целым числом")
    return [word for word in words if len(word) >= min_length]

def most_common_words(text, n=3):
    """Возвращает n самых частых слов в тексте."""
    words = text.lower().split()
    word_freq = Counter(words)
    return word_freq.most_common(n)

def generate_summary(text, max_length):
    """
    Генерирует краткое содержание текста, ограничивая его max_length символами.
    Если текст меньше max_length, возвращает исходный текст.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."
