from collections import Counter
from collections import deque

#1. Алгоритм, который принимает строку и возвращает ее в обратном порядке.
def reverse_algoritmth(str):

    def reverse_str(str):
        res=''
        for i in range(len(str) - 1, - 1, - 1):
            res += str[i]
        return res

    print("Исходная строка " + str)
    print("Строка в обратном порядке "+reverse_str(str))

#2. Реализуйте алгоритм поиска всех анаграмм заданного слова в тексте.
def anagram_search_algorithm(word, text):

    def find_anagrams(word, text):
        word = word.lower()
        word_count = Counter(word)
        word_length = len(word)
        anagrams = []
        for i in range(len(text) - word_length + 1):
            if Counter(text[i:i+word_length].lower()) == word_count:
                anagrams.append(text[i:i+word_length])
        return anagrams

    anagrams = find_anagrams(word, text)
    print(f"Анаграммы слова '{word}' в тексте: {anagrams}")

#3. алгоритм сжатия строк с использованием счетчиков повторяющихся символов 
#и алгоритм для обратного преобразования.
def string_compression_decompression_algorithms(str):

    def compress_str(str):
        dictionary={}
        for i in str:
            if i in dictionary.keys():
                dictionary[i]=dictionary[i]+1
            else:
                dictionary[i]=1
        str=""
        for key, value in dictionary.items():
            str+=key
            str+=f"{value}"
        return str

    def decompress_str(str):
        res=""
        i=0
        while i<len(str):
            char=str[i]
            i += 1
            count = ""
            while i < len(str) and str[i].isdigit():
                count += str[i]
                i += 1
            res += char * int(count)
        return res
        
    print("Исходная строка " + str)
    print("Результат сжатия строки:")
    str=compress_str(str)
    print(str)
    print("Результат обратного преобразования:")
    print(decompress_str(str))

#4. Алгоритм для обхода графа в ширину (BFS)
def bfs_algorithm(graph, start):
 
    if not graph or not start:
        print("Граф пуст, его обход невозможен!") 
        return 
    def bfs():
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            print(node, end=' ')

            for child in graph[node]:
                if child not in visited:
                    queue.append(child)
                    visited.add(child)

    print("Граф:\n")
    print(graph)
    print("\nРезультат обхода графа в ширину (BFS):")
    bfs()

#5. Алгоритм рюкзака без повторений
def knapsack_without_repetition_algorithm(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                dp[i][j] = max(values[i - 1] + dp[i - 1][j - weights[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]
    selected_items = []
    j = capacity
    for i in range(n, 0, - 1):
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(i - 1)
            j -= weights[i - 1]
    selected_items.reverse()
    return dp[n][capacity], selected_items

#Проверка работосапособности алгоритмов:
line="Акнаб"
reverse_algoritmth(line)

word = "listen"
text = "enlists google inlets banana"
anagram_search_algorithm(word, text)

line="aaabbss"
string_compression_decompression_algorithms(line)

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
start_node = 'A'
bfs_algorithm(graph, start_node)

weights =[66,210,149,142,131,357,190,223,86,333]
values = [18,25,27,41,77,15,41,30,43,15]
capacity = 500
arr=["Томат","Баклажан","Перец сладкий","морковь","картофель","огурец","лук репчатый","Арбуз","Свекла сахарная" ,"Дыня" ]
max_value, selected_items = knapsack_without_repetition_algorithm(weights, values, capacity)
print("\nОбщая каллорийность:", max_value)
print("Выбранные продукты для выращивания:\t")
for i in range(len(selected_items)):
    print(arr[selected_items[i]])