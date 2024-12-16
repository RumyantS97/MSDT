import string
from collections import Counter


def count_characters(text):
    """Counts the number of characters in the text."""
    return len(text)


def count_words(text):
    """Counts the number of words in the text."""
    words = text.split()
    return len(words)


def count_sentences(text):
    """Counts the number of sentences in the text."""
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])


def count_unique_words(text):
    """Counts the number of unique words in the text."""
    words = [word.strip(string.punctuation).lower() for word in text.split()]
    return len(set(words))


def word_frequencies(text):
    """Returns a frequency dictionary of words in the text."""
    words = [word.strip(string.punctuation).lower() for word in text.split()]
    return Counter(words)


def most_common_words(text, n=5):
    """Returns the n most common words in the text."""
    frequencies = word_frequencies(text)
    return frequencies.most_common(n)


def average_word_length(text):
    """Calculates the average word length in the text."""
    words = [word.strip(string.punctuation) for word in text.split()]
    if not words:
        return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)


def average_sentence_length(text):
    """Calculates the average sentence length in words."""
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    total_words = sum(len(sentence.split()) for sentence in sentences)
    return total_words / len(sentences)


def count_paragraphs(text):
    """Counts the number of paragraphs in the text."""
    paragraphs = text.split('\n')
    return len([p for p in paragraphs if p.strip()])


def analyze_text(text):
    """Analyzes the text and returns a summary of its metrics."""
    analysis = {
        "character_count": count_characters(text),
        "word_count": count_words(text),
        "unique_word_count": count_unique_words(text),
        "sentence_count": count_sentences(text),
        "paragraph_count": count_paragraphs(text),
        "average_word_length": average_word_length(text),
        "average_sentence_length": average_sentence_length(text),
        "most_common_words": most_common_words(text)
    }
    return analysis


def display_analysis(analysis):
    """Displays the results of text analysis."""
    print("Text Analysis Results:")
    print(f"Total Characters: {analysis['character_count']}")
    print(f"Total Words: {analysis['word_count']}")
    print(f"Unique Words: {analysis['unique_word_count']}")
    print(f"Total Sentences: {analysis['sentence_count']}")
    print(f"Total Paragraphs: {analysis['paragraph_count']}")
    print(f"Average Word Length: {analysis['average_word_length']:.2f}")
    print(f"Average Sentence Length: {analysis['average_sentence_length']:.2f} words")
    print("Most Common Words:")
    for word, count in analysis['most_common_words']:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    sample_text = (
        "Hello world"
    )

    analysis = analyze_text(sample_text)
    display_analysis(analysis)

    # Additional metrics for testing
    print("\nAdditional Testing Metrics:")
    print(f"Word Frequencies: {word_frequencies(sample_text)}")
    print(f"Most Common Words (Top 3): {most_common_words(sample_text, 3)}")
