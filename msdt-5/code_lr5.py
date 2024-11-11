import heapq


# TASK 1
# Naive algorithm
def naive_algorithm(s, p):
    for i in range(len(s) - len(p) + 1):
        for j in range(len(p)):
            if s[i + j] != p[j]:
                break
        else:
            return i
    return -1


# The Knuth-Morris-Pratt algorithm
def prefix_function(p):
    array = [0] * len(p)
    j = 0
    i = 1
    while i < len(p):
        if p[j] == p[i]:
            array[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                array[i] = 0
                i += 1
            else:
                j = array[j - 1]
    return array


def kmp(s, p):
    if not p:
        return 0   # The substring is empty
    if not s:
        return -1  # The string is empty
    prefix_array = prefix_function(p)
    i = 0
    j = 0
    while i < len(s):
        if s[i] == p[j]:
            i += 1
            j += 1
            if j == len(p):
                return i - j
        else:
            if j > 0:
                j = prefix_array[j - 1]
            else:
                i += 1
    if i == len(s):
        return -1


# TASK 2
# An algorithm that finds all palindromic substrings in a given string
def find_palindromes(s):
    if not s:
        return []

    palindromes = []

    # Looking for odd-length palindromes
    for center in range(len(s)):
        radius = 0
        while center - radius >= 0 and center + radius < len(s) and s[center - radius] == s[center + radius]:
            if 2 * radius + 1 > 1:  # Adding only palindromes longer than one character
                palindromes.append(s[center - radius:center + radius + 1])
            radius += 1

    # Ищем палиндромы четной длины
    for center in range(len(s) - 1):
        radius = 0
        while center - radius >= 0 and center + radius + 1 < len(s) and s[center - radius] == s[center + radius + 1]:
            if 2 * (radius + 1) > 1:  # Adding only palindromes longer than one character
                palindromes.append(s[center - radius:center + radius + 2])
            radius += 1

    return sorted(palindromes, key=lambda x: (-len(x), s.index(x)))

def count_palindromes_in_string(s):
    palindromes = find_palindromes(s)
    return len(palindromes)

#  TASK 3
# Huffman encoding algorithm for text data compression
def build_huffman_tree(symbols_freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in symbols_freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        el1 = heapq.heappop(heap)
        el2 = heapq.heappop(heap)

        for pair in el1[1:]:
            pair[1] = '0' + pair[1]

        for pair in el2[1:]:
            pair[1] = '1' + pair[1]

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


# TASK 4
# Algorithm for determining cycles in a graph
def dfs(node, visited, stack, graph):
    visited[node] = True
    stack[node] = True

    for neighbor in graph[node]:
        if not visited[neighbor]:
            if dfs(neighbor, visited, stack, graph):
                return True
        elif stack[neighbor]:
            return True

    stack[node] = False
    return False

def has_cycle(graph):
    num_nodes = len(graph)
    visited = [False] * num_nodes
    stack = [False] * num_nodes

    for node in range(num_nodes):
        if not visited[node]:
            if dfs(node, visited, stack, graph):
                return True

    return False
