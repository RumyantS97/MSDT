import logging
import heapq
from collections import Counter

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler()
    ]
)


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def create_huffman_tree(frequencies):
    logging.info("Создание дерева Хаффмана.")
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    logging.debug(f"Изначальная куча: {[(node.char, node.freq) for node in heap]}")

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        logging.debug(f"Извлечены узлы: {left.char}:{left.freq}, {right.char}:{right.freq}")
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
        logging.debug(f"Добавлен объединённый узел с частотой: {merged.freq}")

    logging.info("Дерево Хаффмана создано.")
    return heap[0]


def generate_huffman_codes(tree, current_code="", codes=None):
    if codes is None:
        codes = {}

    if tree.char is not None:
        codes[tree.char] = current_code
        logging.debug(f"Символ: {tree.char}, Код: {current_code}")
        return codes

    if tree.left:
        generate_huffman_codes(tree.left, current_code + "0", codes)
    if tree.right:
        generate_huffman_codes(tree.right, current_code + "1", codes)
    return codes


def encode_using_huffman(text, huffman_codes):
    logging.info("Кодирование текста с использованием кодов Хаффмана.")
    encoded = ''.join(huffman_codes[char] for char in text)
    logging.debug(f"Закодированный текст: {encoded}")
    return encoded


def decode_using_huffman(encoded_text, tree):
    logging.info("Декодирование текста с использованием дерева Хаффмана.")
    decoded_text = []
    current = tree

    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded_text.append(current.char)
            current = tree

    result = ''.join(decoded_text)
    logging.debug(f"Декодированный текст: {result}")
    return result


def analyze_frequency(text):
    logging.info("Анализ частоты символов в тексте.")
    frequencies = Counter(text)
    logging.debug(f"Частоты символов: {frequencies}")
    return frequencies


def search_naively(text, pattern):
    logging.info("Поиск подстроки наивным методом.")
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            logging.debug(f"Подстрока найдена на позиции: {i}")
            return i
    logging.debug("Подстрока не найдена.")
    return -1


def search_using_kmp(text, pattern):
    logging.info("Поиск подстроки методом Кнута-Морриса-Пратта.")

    def build_prefix_table(pattern):
        m = len(pattern)
        lps = [0] * m
        j = 0
        for i in range(1, m):
            if pattern[i] == pattern[j]:
                j += 1
                lps[i] = j
            else:
                if j != 0:
                    j = lps[j - 1]
                    i -= 1
                else:
                    lps[i] = 0
        return lps

    lps = build_prefix_table(pattern)
    logging.debug(f"Префикс-функция: {lps}")

    i, j = 0, 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            logging.debug(f"Подстрока найдена на позиции: {i - j}")
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    logging.debug("Подстрока не найдена.")
    return -1


def find_all_palindromes(text):
    logging.info("Поиск всех палиндромных подстрок.")
    palindromes = []
    n = len(text)

    def expand_palindrome_center(left, right):
        while left >= 0 and right < n and text[left] == text[right]:
            palindromes.append(text[left:right + 1])
            left -= 1
            right += 1

    for i in range(n):
        expand_palindrome_center(i, i)  # Odd-length palindromes
        expand_palindrome_center(i, i + 1)  # Even-length palindromes
    logging.debug(f"Найденные палиндромы: {palindromes}")
    return palindromes


def main():
    logging.info("Запуск приложения.")
    print("7. Наивный алгоритм и алгоритм Кнута-Морриса-Пратта для поиска подстроки")
    print("8. Алгоритм поиска всех палиндромных подстрок")
    print("9. Алгоритмы для частотного анализа и кодирования Хаффмана")
    choice = input("Ваш выбор: ")

    if choice == '1':
        text = input("Введите текст: ")
        pattern = input("Введите подстроку для поиска: ")
        logging.info("Выбрана операция поиска подстроки.")
        print("\nНаивный алгоритм:")
        naive_result = search_naively(text, pattern)
        print("Результат:", naive_result)
        print("\nАлгоритм Кнута-Морриса-Пратта:")
        kmp_result = search_using_kmp(text, pattern)
        print("Результат:", kmp_result)
    elif choice == '8':
        text = input("Введите текст: ")
        logging.info("Выбрана операция поиска палиндромов.")
        palindromes = find_all_palindromes(text)
        print("\nНайденные палиндромные подстроки:", palindromes)
    elif choice == '9':
        text = input("Введите текст для анализа частоты символов: ")
        logging.info("Выбрана операция кодирования Хаффмана.")
        frequencies = analyze_frequency(text)
        print("\nЧастоты символов:", frequencies)
        huffman_tree = create_huffman_tree(frequencies)
        huffman_codes = generate_huffman_codes(huffman_tree)
        print("\nКоды Хаффмана:", huffman_codes)
        encoded_text = encode_using_huffman(text, huffman_codes)
        print("\nЗакодированный текст:", encoded_text)
        decoded_text = decode_using_huffman(encoded_text, huffman_tree)
        print("\nДекодированный текст:", decoded_text)
    else:
        logging.warning("Неверный выбор пользователя.")
        print("Неверный выбор! Программа завершена.")
        return


if __name__ == "__main__":
    main()
