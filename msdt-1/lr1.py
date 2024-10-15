import random
import os.path

from collections import defaultdict


# Информация о 2 лр
def info_lr2():
    print('Лабораторная работа №2')
    print('Вариант №8, выполнила студентка группы 6104-020302D, Добина Алина')
    print('Задание:')
    print('1. В списке целочисленных элементов найти максимальный нечётный элемент')
    print('2. С использованием цикла while найти в списке индекс первого '
          'двузначного элемента, кратного заданному числу')
    print('3. Отсортировать список (без использования стандартных функций '
          'сортировки) по убыванию старших цифр элементов списка '
          '(быстрая сортировка)')


# Информация о 3 лр
def info_lr3():
    print('Лабораторная работа №3')
    print('Вариант №8, выполнила студентка группы 6104-020302D, Добина Алина')
    print()
    print('Задание:')
    print(
        'В исходном текстовом файле записаны строки, содержащие произвольные '
        'алфавитно-цифровые символы.\n'
        'Требуется написать программу, которая для каждой строки исходного '
        'файла будет составлять и выводить в результирующий файл слово из тех '
        'букв английского алфавита, которые встречаются во входных данных '
        'либо как строчные, либо как прописные,\n'
        'причем буквы должны идти в алфавитном порядке. Каждая буква должна '
        'быть распечатана один раз.\n'
        'Буквы построенного слова должны быть прописными. Если во входных '
        'данных встречаются все буквы английского алфавита, то следует вывести '
        'строчными буквами слово "no".'
    )
    print()


# Информация о 4 лр
def info_lr4():
    print('Лабораторная работа №4')
    print('Вариант №8, выполнила студентка группы 6104-020302D, Добина Алина')
    print()
    print('Задание:')
    print(
        'Алгоритм вычисления функции F(n), где n – натуральное число, задан '
        'следующими соотношениями:\n'
        'F(n) = 1, при n < 2,\n'
        'F(n) = F(n // 2) + 1, когда n >= 2 и четное,\n'
        'F(n) = F(n – 3) + 3, когда n >= 2 и нечётное.\n'
        'Напишите программу, которая вычисляет:\n'
        '1. Минимальное значение n, для которого F(n) равно 31\n'
        '2. Количество кратных 3 четных цифр результата вычисления F(x), '
        'где x – число, заданное пользователем.'
        )
    print()


# Информация о дополнительной лр
def menu():
    print(
        "1. Реализуйте наивный алгоритм и алгоритм Кнута-Морриса-Пратта для поиска подстроки в строке. "
        "Сравните эффективность алгоритмов на различных входных данных.\n"
        "2. Реализуйте алгоритм, который находит все палиндромные подстроки в данной строке.\n"
        "3. Реализуйте алгоритм кодирования Хаффмана для сжатия текстовых данных. (отдельно)\n"
        "4. Реализуйте алгоритм для определения циклов в графе."
    )


# Ввод элементов списка
def input_list():
    elements = list(map(int, input("Введите элементы списка через пробел: ").split()))
    return elements


# Формирование списка случайных элементов
def random_list(random_numbers, count, lower_bound, upper_bound):
    for _ in range(count):
        random_numbers.append(random.randint(lower_bound, upper_bound))
    return random_numbers


# Поиск максимального нечетного элемента
def find_max(odd_numbers):
    max_odd = -10 ** 10
    for index in range(len(odd_numbers)):
        if (odd_numbers[index] % 2 != 0) and (odd_numbers[index] > max_odd):
            max_odd = odd_numbers[index]
    return max_odd


# Поиск индекса первого двузначного элемента, кратного заданному числу
def find_first_element(numbers, divisor):
    index = 0
    while index < len(numbers) and (numbers[index] % divisor != 0 or numbers[index] <= 9 or numbers[index] >= 100):
        index += 1
    return index


# Поиск первой цифры числа
def find_leading_digit(number):
    number = abs(number)
    while number > 9:
        number //= 10
    return number


# Быстрая сортировка по убыванию
def quick_sort(array, left, right):
    ind_left = left
    ind_right = right
    ind_middle = (left + right) // 2
    middle = array[ind_middle]
    while ind_left <= ind_right:
        while oldnum(m[ind_left]) > oldnum(middle):
            ind_left += 1
        while oldnum(array[ind_right]) < oldnum(middle):
            ind_right -= 1
        if ind_left <= ind_right:
            array[ind_left], array[ind_right] = array[ind_right], array[ind_left]
            ind_left += 1
            ind_right -= 1
    if ind_left < right:
        quick_sort(array, ind_left, right)
    if ind_right > left:
        quick_sort(array, left, ind_right)
    return array


# Функция считает кол-во использования букв
def count_used_letters(string):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_counts = [0] * 26
    string_result = ''
    for char in range(len(string)):
        for index in range(26):
            if string[char] == alphabet[index]:
                letter_counts[index] += 1
    for index in range(26):
        if letter_counts[index] != 0:
            string_result += alphabet[index]
    if string == '\n':
        return ''
    if string_result != '':
        return string_result
    else:
        return "В данной строке нет букв"


# Функция возвращает строку для результирующего файла
def get_word(string):
    letter_counts = count_used_letters(string)
    if letter_counts != "В данной строке нет букв":
        if len(letter_counts) == 26:
            return 'no'
        else:
            return letter_counts
    else:
        return letter_counts


# Функция работает с файлами
def file_to_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile.readlines():
            line = line.upper()
            outfile.write(get_word(line) + '\n')


# Функция F(n)
def f(n):
    if n < 2:
        return 1
    if n % 2 == 0:
        return f(n // 2) + 1
    else:
        return f(n - 3) + 3


# Задание 1 лр4
def min_n_31(n):
    while f(n) != 31:
        n += 1
    return n


# Задание 2 лр4
def count_multiples_of_3_even_digits(num):
    if num == 0:
        return 0
    elif num % 10 == 6 or num % 10 == 0:
        return count_multiples_of_3_even_digits(num // 10) + 1
    else:
        return count_multiples_of_3_even_digits(num // 10)


class HuffmanNode:
    def __init__(self, character, frequency, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.character}, {self.frequency})"


class HuffmanCoding:
    def get_code(self, input_data):
        frequency_map = self.build_frequency_map(input_data)
        node_queue = self.sort_by_frequency(frequency_map)
        self.root = self.build_tree(node_queue)
        code_map = self.create_huffman_code(self.root)
        return code_map

    def build_frequency_map(self, input_data):
        frequency_map = {}
        for character in input_data:
            frequency_map[character] = frequency_map.get(character, 0) + 1
        return frequency_map

    def sort_by_frequency(self, frequency_map):
        queue = [HuffmanNode(char, freq) for char, freq in frequency_map.items()]
        queue.sort(key=lambda node: node.frequency)
        return queue

    def build_tree(self, node_queue):
        while len(node_queue) > 1:
            node1 = node_queue.pop(0)
            node2 = node_queue.pop(0)
            combined_node = HuffmanNode('', node1.frequency + node2.frequency, node1, node2)
            node_queue.append(combined_node)
            node_queue.sort(key=lambda node: node.frequency)  # Maintain order after adding new node
        return node_queue.pop(0)

    def create_huffman_code(self, node):
        code_map = {}
        self.create_code_rec(node, code_map, "")
        return code_map

    def create_code_rec(self, node, code_map, current_code):
        if node.left is None and node.right is None:
            code_map[node.character] = current_code
            return
        self.create_code_rec(node.left, code_map, current_code + '0')
        self.create_code_rec(node.right, code_map, current_code + '1')

    def encode(self, code_map, input_data):
        return ''.join(code_map[char] for char in input_data)

    def decode(self, coded):
        decoded_string = ""
        current_node = self.root
        for bit in coded:
            current_node = current_node.right if bit == '1' else current_node.left
            if current_node.left is None and current_node.right is None:
                decoded_string += current_node.character
                current_node = self.root
        return decoded_string


# Наивный алгоритм поиска строки
def naive_search(text, pattern):
    text_length = len(text)
    pattern_length = len(pattern)

    for start_index in range(text_length - pattern_length + 1):
        match_index = 0
        while match_index < pattern_length and text[start_index + match_index] == pattern[match_index]:
            match_index += 1
        if match_index == pattern_length:
            return start_index  # Возвращает индекс начала совпадения
    return -1


# Алгоритм поиска подстроки Кнутта–Морриса–Пратта
def kmp_search(text, pattern):
    # Построение массива префиксов
    prefix_array = [0] * len(pattern)
    pattern_index = 0
    text_index = 1

    while text_index < len(pattern):
        if pattern[pattern_index] == pattern[text_index]:
            prefix_array[text_index] = pattern_index + 1
            text_index += 1
            pattern_index += 1
        else:
            if pattern_index == 0:
                prefix_array[text_index] = 0
                text_index += 1
            else:
                pattern_index = prefix_array[pattern_index - 1]

    # Поиск подстроки в тексте
    pattern_length = len(pattern)
    text_length = len(text)
    text_index = 0
    pattern_index = 0

    while text_index < text_length:
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1
            if pattern_index == pattern_length:
                print("Подстрока найдена! (КМП)")
                break
        else:
            if pattern_index > 0:
                pattern_index = prefix_array[pattern_index - 1]
            else:
                text_index += 1

    if text_index == text_length and pattern_index != pattern_length:
        print("Подстрока не найдена (КМП)")


# Поиск подстроки, которая является палиндромом
def expand_from_center(string, left_index, right_index):
    while left_index >= 0 and right_index < len(string) and string[left_index] == string[right_index]:
        left_index -= 1
        right_index += 1
    return string[left_index + 1:right_index]


# Поиск всех паллиндромов в подстроке
def find_palindromes(input_string):
    found_palindromes = []
    for index in range(len(input_string)):
        odd_palindrome = expand_from_center(input_string, index, index)
        if odd_palindrome and len(odd_palindrome) != 1:
            found_palindromes.append(odd_palindrome)
        even_palindrome = expand_from_center(input_string, index, index + 1)
        if even_palindrome and len(even_palindrome) != 1:
            found_palindromes.append(even_palindrome)
    return found_palindromes


# Проверка графа на содержание циклов
def has_cycle(graph):
    visited_nodes = set()
    recursion_stack = set()

    def dfs(current_node):
        if current_node in recursion_stack:
            return True
        if current_node in visited_nodes:
            return False

        visited_nodes.add(current_node)
        recursion_stack.add(current_node)

        for neighbor in graph[current_node]:
            if dfs(neighbor):
                return True

        recursion_stack.remove(current_node)
        return False

    for node in graph:
        if dfs(node):
            return True
    return False


# Создание направленного графа
def create_graph():
    graph = {}
    print("Введите вершины графа через пробел (например, A B C):")
    vertices = input().split()

    for vertex in vertices:
        graph[vertex] = []

    print("Введите ребра графа в формате 'вершина1 вершина2' (например, A B).\n"
          "Для завершения ввода введите '0'.")

    while True:
        edge_input = input().split()
        if edge_input[0] == '0':
            break

        if len(edge_input) != 2:
            print("Неверный формат ввода! Попробуйте снова.")
            continue

        vertex1, vertex2 = edge_input
        if vertex1 not in graph or vertex2 not in graph:
            print("Такой вершины нет в графе! Попробуйте снова.")
            continue

        graph[vertex1].append(vertex2)

    return graph






info_lr2()
print("Введите способ заполнения списка:")
print("1 - ввод элементов списка в одну строку через пробел:")
print("любое число - автоматическая генерация списка из n случайных элементов "
      "в заданном пользователем диапазоне:")
v = int(input())
print("")
m = []
if v == 1:
    print('Введите в строку элементы списка:')
    m = input_list()
else:
    n = int(input('Введите количество элементов списка:'))
    a, b = map(int, input('Введите диапазон элементов:').split())
    m = random_list(m, n, a, b)
    print(m)
    print('')
# Задача №1
c = find_max(m)
if c != -10 ** 10:
    print('Максимальный нечётный элемент', c)
else:
    print('В списке отсутствуют нечётные элементы')
print('')
# Задача №2
kr = int(input('Введите число, кратность которому нужно проверить:'))
ans = find_first_element(m, kr)
if ans > len(m) - 1:
    print('В списке отсутствуют двузначные элементы, кратные', kr)
else:
    print('Индекс первого двузначного элемента, кратного', kr, '-', ans)
print('')
# Задача №3
print('Исходный список:')
print(m)
print('Список после быстрой сортировки:')
print(quick_sort(m, 0, len(m) - 1))


info_lr3()

source_filename = input('Введите имя исходного файла: ')
if os.path.exists(source_filename):
    result_filename = input("Введите имя результирующего файла: ")
    file_to_file(source_filename, result_filename)
    print('Задание выполнено')
else:
    print('Такого файла не существует')





info_lr4()
print('Минимальное значение n, для которого F(n) равно 31 = ', min_n_31(1))
x = int(input('Введите значение x: '))
result = f(x)
print('Количество кратных 3 четных цифр результата вычисления "\
      F(x) = ', result, ':', count_multiples_of_3_even_digits(s))












flag = True

while flag:
    menu()
    print("Выберите номер задания:")
    choice = int(input())

    if choice == 1:
        print("Введите строку: ")
        main_string = input()
        print("Введите подстроку для поиска: ")
        substring = input()

        result_naive = naive_search(main_string, substring)
        cmp(main_string, substring)

        if result_naive != -1:
            print("Подстрока найдена (наивно)")
        else:
            print("Такая подстрока не найдена (наивно)")
        print()

    elif choice == 2:
        print("Введите строку: ")
        input_string = input()
        palindromes = find_palindromes(input_string)
        print(palindromes)

    elif choice == 3:
        print()
        # Реализация для задания 3

    elif choice == 4:
        graph = create_graph()
        if has_cycle(graph):
            print("Граф содержит циклы")
        else:
            print("Граф не содержит циклов")
