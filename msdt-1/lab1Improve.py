# Задание 1
print("Задание 1")


def check_brackets(input_string):
    stack = []
    for char in input_string:
        if char == '(':
            stack.append('(')
        elif char == ')':
            if not stack or stack.pop() != '(':
                return False
    return len(stack) == 0


input_string = "((()))"
print(input_string, "\t: ", check_brackets(input_string))  # Вернет True

input_string = "(()))"
print(input_string, "\t: ", check_brackets(input_string), "\n")  # Вернет False


def check_brackets(input_string):
    bracket_pairs = {
        '(': ')',
        '[': ']',
        '{': '}'
    }
    stack = []
    for char in input_string:
        # print(char, stack)
        if char in bracket_pairs.keys():
            stack.append(char)
        elif char in bracket_pairs.values():
            if not stack or bracket_pairs[stack.pop()] != char:
                return False
    return len(stack) == 0


input_string = "{[()()]}"
print(input_string, ": ", check_brackets(input_string))  # Вернет True

input_string = "({)}"
print(input_string, "\t : ", check_brackets(input_string))  # Вернет False

# Задание 2
print("\nЗадание 2")


class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self):
        if self.stack:
            if self.stack[-1] == self.min_stack[-1]:
                self.min_stack.pop()
            return self.stack.pop()

    def min(self):
        if self.min_stack:
            return self.min_stack[-1]

    def print_stack(self):
        for i in self.stack:
            print(i, end=" ")
        print()


# Пример использования
min_stack = MinStack()
min_stack.push(3)
min_stack.push(5)
min_stack.push(2)
min_stack.print_stack()
print("min: ", min_stack.min())  # Вернет 2
min_stack.pop()
min_stack.print_stack()
print("min: ", min_stack.min())  # Вернет 3
min_stack.pop()
min_stack.print_stack()

# Задание 3
print("\nЗадание 3")
from collections import deque


def max_in_window(arr, k):
    n = len(arr)
    if n == 0:
        return

    max_in_window = []
    d = deque()

    for i in range(n):
        while d and d[0] < i - k + 1:
            d.popleft()

        while d and arr[i] >= arr[d[-1]]:
            d.pop()

        d.append(i)

        if i >= k - 1:
            max_in_window.append(arr[d[0]])

    return max_in_window


# Пример использования
arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = max_in_window(arr, k)
print(arr)
print("\t", result)

# Задание 4
print("\nЗадание 4")
def find_duplicate(nums):
    tortoise = nums[0]
    hare = nums[0]

    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break

    tortoise = nums[0]
    while tortoise != hare:
        tortoise = nums[tortoise]
        hare = nums[hare]

    return tortoise

# Пример использования
nums = [1, 3, 4, 2, 2]
print(nums)
print(find_duplicate(nums))  # Вывод: 2


# Задание 5
print("\nЗадание 5")
def zero_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    row_zero = [False] * rows
    col_zero = [False] * cols

    # Поиск нулевых элементов
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                row_zero[i] = True
                col_zero[j] = True

    # Обнуление строк
    for i in range(rows):
        if row_zero[i]:
            matrix[i] = [0] * cols

    # Обнуление столбцов
    for j in range(cols):
        if col_zero[j]:
            for i in range(rows):
                matrix[i][j] = 0

    return matrix

# Пример использования
matrix = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 8, 9]
]

result = zero_matrix(matrix)
for row in result:
    print(row)


import random
import string


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_substring(string, min_length, max_length):
    start = random.randint(0, len(string) - max_length)
    end = random.randint(min_length, max_length)
    return string[start:start + end]


import time


def compare_algorithms(text_length, pattern_length, num_tests):
    text = generate_random_string(text_length)
    pattern = generate_random_substring(text, 1, pattern_length)

    naive_times = []
    kmp_times = []

    for _ in range(num_tests):
        start_time = time.time()
        naive_search(text, pattern)
        naive_times.append(time.time() - start_time)

        start_time = time.time()
        kmp_search(text, pattern)
        kmp_times.append(time.time() - start_time)

    avg_naive_time = sum(naive_times) / num_tests
    avg_kmp_time = sum(kmp_times) / num_tests

    return avg_naive_time, avg_kmp_time


# Задание 1
print("Задание 1")


def naive_search(text, pattern):  # O(m * (n - m)), худший сл(m/2): O(n^2), лучший: O(n)
    n = len(text)
    m = len(pattern)
    result = []

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            result.append(i)

    return result


def compute_lps_array(pattern):
    m = len(pattern)
    lps = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j

    return lps


def kmp_search(text, pattern):  # O(n)
    n = len(text)
    m = len(pattern)
    lps = compute_lps_array(pattern)
    result = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            result.append(i - m + 1)
            j = lps[j - 1]

    return result


avg_naive_time, avg_kmp_time = compare_algorithms(1000, 3, 100)
print(f"Avg Time наивного алгоритма:\t {avg_naive_time * 1000:.5f} ms")
print(f"Avg Time Кнута-Морриса-Пратта:\t {avg_kmp_time * 1000:.5f} ms")

#задание 2
print("\nЗадание 2")


def find_palindromes(s):
    def is_palindrome(substring):
        return substring == substring[::-1]

    palindromes = []
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            if is_palindrome(s[i:j]):
                palindromes.append(s[i:j])

    return palindromes

    # O(n^2)


def palindromic_substrings(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            palindromes.append(s[left:right + 1])
            left -= 1
            right += 1

    palindromes = []
    for i in range(len(s)):
        expand(i, i)  # Палиндромы с центром в символе
        expand(i, i + 1)  # Палиндромы с центром между символами

    return palindromes


# Пример использования
input_string = "abcbabad"
# print(input_string[4:len(input_string)+4])
palindrome_substrings = find_palindromes(input_string)
print("Палиндромные подстроки в строке:")
print(palindrome_substrings)

palindrome_substrings = palindromic_substrings(input_string)
print("Палиндромные подстроки в строке:")
print(palindrome_substrings)

print("\nЗадание 3") # O(Nlog(N))
# Задание 3
import heapq
from collections import defaultdict

class node:
    def __init__(self, char, freq):
        self.char = char # Символ
        self.freq = freq # Частота повоторений
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq_dict = defaultdict(int) # Создаем словарь и заносим к ключу количество совпадений
    for char in text:
        freq_dict[char] += 1

    min_heap = []
    for char, freq in freq_dict.items(): # Создаем кучу и заносим по возр для каждого символа узел с символом и частотой
        heapq.heappush(min_heap, node(char, freq))

    while len(min_heap) > 1: # Проходим пока не останется один узел _ Log(n)
        left = heapq.heappop(min_heap)
        right = heapq.heappop(min_heap)
        combined_freq = left.freq + right.freq
        parent = node(None, combined_freq) # Создаем новый узел из двух наименее повторяющихся
        parent.left = left
        parent.right = right
        heapq.heappush(min_heap, parent) # Заносим новый узел к остальным

    return min_heap[0]

def build_huffman_codes(node, current_code, huffman_codes): # Для каждого узла сохраняется его двоичный код из дерева
    if node:
        if node.char:
            huffman_codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + '0', huffman_codes)
        build_huffman_codes(node.right, current_code + '1', huffman_codes)

def huffman_encoding(text):
    root = build_huffman_tree(text) # Построение дерева
    huffman_codes = {} # Заведение словаря для символов(их довичный код)
    build_huffman_codes(root, '', huffman_codes)

    encoded_text = ''.join(huffman_codes[char] for char in text) # Преобразовываем текст проходя посимвольно
    return encoded_text, huffman_codes # Возвращаем закодированный текст и словарь с кодом

def huffman_decoding(encoded_text, huffman_codes):
    decoded_text = ''
    current_code = '' # Накопление битов для тек символа
    for bit in encoded_text:
        current_code += bit
        for char, code in huffman_codes.items():
            if code == current_code:
                decoded_text += char
                current_code = ''
                break

    return decoded_text

# Пример использования
text = "hello world"
encoded_text, huffman_codes = huffman_encoding(text)
print("Encoded text:", encoded_text)
decoded_text = huffman_decoding(encoded_text, huffman_codes)
print("Decoded text:", decoded_text)


# Задание 4
print("\nЗадание 4")
from collections import defaultdict

def has_cycle(graph): # O(n + m)
    def dfs(node, visited, rec_stack):
        visited[node] = True
        rec_stack[node] = True

        for neighbor in graph[node]: # Проходка по соседям вершины
            if not visited[neighbor]: # Если не посещали соседа, вызываем рекурсивно функцию
                if dfs(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]: # Если обнаруживается сосед как записаный, то есть цикл
                return True

        rec_stack[node] = False
        return False

    visited = defaultdict(bool) # Словарь для отслеживания посещенных вершин
    rec_stack = defaultdict(bool) # Словарь для отслеживания вершин в текущем стеке вызовов

    for node in graph:
        if not visited[node]:
            if dfs(node, visited, rec_stack):
                return True

    return False

# Пример использования
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [3]
}

if has_cycle(graph):
    print("Граф содержит цикл.")
else:
    print("Граф не содержит циклов.")
