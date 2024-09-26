# Задание 3
# Алгоритм кодирования Хаффмана для сжатия текстовых данных
import heapq
from collections import defaultdict

def build_huffman_tree(symbols_freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in symbols_freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        el1 = heapq.heappop(heap)
        el2 = heapq.heappop(heap)
        for pair in el1[1:]: pair[1] = '0' + pair[1]
        for pair in el2[1:]: pair[1] = '1' + pair[1]
        heapq.heappush(heap, [el1[0] + el2[0]] + el1[1:] + el2[1:])

    return heap[0]


def get_huffman_codes(tree):
    huff_codes = {}
    for pair in tree[1:]:
        symbol, code = pair
        huff_codes[symbol] = code
    return huff_codes


def compress_data(text, huff_codes):
    result = ""
    for char in text:
        result += huff_codes[char]
    return result


def decompress_data(compressed_data, huff_codes):
    huff_codes_reversed = {code: symbol for symbol, code in huff_codes.items()}
    decoded_data = ""
    temp_code = ""

    for bit in compressed_data:
        temp_code += bit
        if temp_code in huff_codes_reversed:
            decoded_data += huff_codes_reversed[temp_code]
            temp_code = ""

    return decoded_data


text = "абракадабра"

# Подсчет частоты символов в тексте
symbols_freq = defaultdict(int)
for symbol in text:
    symbols_freq[symbol] += 1
print(symbols_freq)

# Построение дерева Хаффмана и генерация кодов
huffman_tree = build_huffman_tree(symbols_freq)
huffman_codes = get_huffman_codes(huffman_tree)
print(huffman_tree)
print(huffman_codes)

# Сжатие и распаковка данных
compressed_data = compress_data(text, huffman_codes)
decompressed_data = decompress_data(compressed_data, huffman_codes)

print(f"Исходный текст: {text}")
print(f"Сжатые данные: {compressed_data}")
print(f"Восстановленный текст: {decompressed_data}")