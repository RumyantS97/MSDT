import heapq
from collections import defaultdict


# Поиск подстрок
# Сложность O(n*m)
def naive(text, pattern):
    result = []
    text_len = len(text)
    pattern_len = len(pattern)
    for i in range(text_len - pattern_len + 1):
        j = 0
        while j < pattern_len and text[i + j] == pattern[j]:
            j += 1
            if j == pattern_len:
                result.append(i)
    return result


# Поиск подстрок
# Сложность O(n+m)
def lps(pattern):
    pattern_len = len(pattern)
    lps = [0] * pattern_len
    j = 0
    i = 1

    while i < pattern_len:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp(text, pattern):
    result = []
    text_len = len(text)
    pattern_len = len(pattern)
    lpsres = lps(pattern)
    i = 0
    j = 0

    while i < text_len:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == pattern_len:
            result.append(i-j)
            j = lpsres[j-1]
        elif i < text_len and pattern[j] != text[i]:
            if j != 0:
                j = lpsres[j-1]
            else:
                i += 1
    return result


# Поиск палиндромов
# Сложность O(n^2)
def find_palindrom(text):
    def expand(low, high):
        while low >= 0 and high < len(text) and text[low] == text[high]:
            palindroms.append(text[low:high+1])
            low -= 1
            high += 1
    palindroms = []
    for i in range(len(text)):
        expand(i, i)
        expand(i, i+1)
    return palindroms


# Алгоритм Хаффмана
def huffman(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heapq.heappush(heap, [lo[0]+hi[0]]+lo[1:]+hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda x: (len(x[-1]), x))


# Поиск цикла в графе
def has_cycle(graph, v, visited, parent):
    visited[v] = True
    for i in graph[v]:
        if not visited[i]:
            if has_cycle(graph, i, visited, v):
                return True
        elif parent != i:
            return True
    return False


def find_cycle(graph):
    n = len(graph)
    visited = [False] * n
    for i in range(n):
        if not visited[i]:
            if has_cycle(graph, i, visited, -1):
                return True
    return False
