from collections import deque


def reverse_string(string):
    if not string:
        return ""

    reversed_string = ""

    for i in range(len(string) - 1, -1, -1):
        reversed_string += string[i]

    return reversed_string


def find_anagrams(text, word):
    # Создаем словарь из букв заданного слова и их количества.
    word_dict = {}
    for char in word:
        word_dict[char] = word_dict.get(char, 0) + 1

    anagrams = []

    # Итерируем по тексту.
    for i in range(len(text) - len(word) + 1):
        # Создаем словарь из букв слова из текста и их количества.
        text_dict = {}
        for j in range(i, i + len(word)):
            text_dict[text[j]] = text_dict.get(text[j], 0) + 1

        # Проверяем, совпадают ли словари букв.
        if text_dict == word_dict:
            anagrams.append(text[i:i + len(word)])

    return anagrams


def compress(string):
    compressed_string = []
    current_char = string[0]
    count = 1

    for char in string[1:]:
        if char == current_char:
            count += 1
        else:
            compressed_string.append(current_char + str(count))
            current_char = char
            count = 1

    compressed_string.append(current_char + str(count))

    return ''.join(compressed_string)


def decompress(compressed_string):
    decompressed_string = []
    i = 0
    while i < len(compressed_string):
        char = compressed_string[i]
        i += 1
        count = ""
        while i < len(compressed_string) and compressed_string[i].isdigit():
            count += compressed_string[i]
            i += 1

        if count:
            count = int(count)

        decompressed_string.append(char * count)

    return ''.join(decompressed_string)


def bfs(graph, start):
    result = {start: 0}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in result:
                result[neighbor] = result[vertex] + 1
                # Когда мы видим новую вершину, мы добавляем ее в правую часть очереди.
                queue.append(neighbor)
    return result


# Функция для интерактивного меню выбора заданий
def task_menu(user_input):
    task = user_input
    menu = """Меню: 
1. Перевернуть строку 
2. Найти анаграммы 
3. Сжатие строки 
4. Обход графа 
0. Завершить программу 

Выберите номер задания (1, 2, 3, 4, 5) или 0 для выхода: """

    while True:
        task = input(menu)

        if task == '1':
            s = input("Введите строку: ")
            print(reverse_string(s))
        elif task == '2':
            s = input("Введите строку: ")
            w = input("Введите слово: ")
            print(find_anagrams(s, w))
        elif task == '3':
            s = input("Введите строку: ")
            print("Сжатая: " + compress(s))
            print("Разжатая: " + decompress(compress(s)))
        elif task == "4":
            # Создаем тестовый граф. 
            graph = {
                'A': ['B', 'C'],
                'B': ['D', 'E'],
                'C': ['F'],
                'D': ['G'],
                'E': ['F'],
                'F': [],
                'G': []
            }

            # Выполняем обход графа в ширину, начиная с вершины 'A'. 
            visited_vertices = bfs(graph, 'A')

            # Выводим список посещенных вершин. 
            print("Посещенные вершины:", visited_vertices)


        elif task == '0':
            print("Программа завершена.")
            break
        else:
            print("Неверный номер задания. Пожалуйста, выберите 1, 2, 3 или 0 для выхода.")

        # Запуск программы
