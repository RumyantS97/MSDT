# ЗАДАНИЕ 1
# Наивный алгоритм
def naive_algorithm(s, p):
    for i in range(len(s) - len(p) + 1):
        for j in range(len(p)):
            if s[i + j]!=p[j]:
                break
        else:
            return i
    return -1

# Алгоритм Кнута-Морриса-Пратта
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
                j = prefix_array[j-1]
            else:
                i += 1
    if i == len(s):
        return -1


# ЗАДАНИЕ 2
# Алгоритм, который находит все палиндромные подстроки в данной строке
def find_palindromes(s):
    modified_string = '#' + '#'.join(s) + '#'
    n = len(modified_string)

    palindrome_lengths = [0] * n   # Массив для хранения длин палиндромов
    center = right = 0  # Центр и граница самого правого палиндрома

    for i in range(n):
        if i < right:
            palindrome_lengths[i] = min(right - i, palindrome_lengths[2 * center - i])

        # Расшириряем палиндром в обе стороны
        while (i - palindrome_lengths[i] - 1 >= 0 and
               i + palindrome_lengths[i] + 1 < n and
               modified_string[i - palindrome_lengths[i] - 1] == modified_string[i + palindrome_lengths[i] + 1]):
            palindrome_lengths[i] += 1

        if i + palindrome_lengths[i] > right:    # Обновляем центр и границу самого правого палиндрома
            center, right = i, i + palindrome_lengths[i]

    palindromes = []
    for i in range(n):
        if palindrome_lengths[i] > 0:
            # Удаляем символы и добавляем в результат
            palindromes.append(modified_string[i - palindrome_lengths[i]:i + palindrome_lengths[i] + 1].replace('#', ''))

    return palindromes


# ЗАДАНИЕ 4
# Алгоритм для определения циклов в графе
def has_cycle(graph):
    num_nodes = len(graph)
    visited = [False] * num_nodes
    stack = [False] * num_nodes
    def dfs(node, visited, stack):
        visited[node] = True
        stack[node] = True

        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, visited, stack):
                    return True
            elif stack[neighbor]:
                return True

        stack[node] = False
        return False

    for node in range(num_nodes):
        if not visited[node]:
            if dfs(node, visited, stack):
                return True

    return False


print(naive_algorithm("abcaaaffff", "aaa"))
print(kmp("abcaaaffff", "aaa"))
print(find_palindromes("abcbafaea"))

# Пример использования
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [3]
}
print(has_cycle(graph))