import random
import os.path
from collections import defaultdict

def info():
    print('Лабораторная работа №2')
    print('Вариант №8, выполнила студентка группы 6104-020302D, Добина Алина')
    print('Задание:')
    print('1. В списке целочисленных элементов найти максимальный нечётный элемент')
    print('2. С использованием цикла while найти в списке индекс первого '
          'двузначного элемента, кратного заданному числу')
    print('3. Отсортировать список (без использования стандартных функций '
          'сортировки) по убыванию старших цифр элементов списка '
          '(быстрая сортировка)')


# Ввод элементов списка
def inputList(m):
    m = list(map(int, input().split()))
    return (m)


# Формирование списка случайных элементов
def randomList(m, n, a, b):
    for i in range(n):
        m.append(random.randint(a, b))
    return (m)


# Поиск максимального нечетного элемента
def findMax(m):
    maxim = -10 ** 10
    for i in range(len(m)):
        if (m[i] % 2 != 0) and (m[i] > maxim):
            maxim = m[i]
    return maxim


# Поиск индекса первого двузначного элемента, кратного заданному числу
def firstelement(m, kr):
    ind = 0
    while ind < len(m) and (m[ind] % kr != 0 or m[ind] <= 9 or m[ind] >= 100):
        ind += 1
    return ind


# Поиск старшей цифры
def oldnum(n):
    n = abs(n)
    while n > 9:
        n //= 10
    return n


# Быстрая сортировка по убыванию

def QuickSort(m, left, right):
    ind_left = left
    ind_right = right
    ind_middle = (left + right) // 2
    middle = m[ind_middle]
    while ind_left <= ind_right:
        while oldnum(m[ind_left]) > oldnum(middle):
            ind_left += 1
        while oldnum(m[ind_right]) < oldnum(middle):
            ind_right -= 1
        if ind_left <= ind_right:
            m[ind_left], m[ind_right] = m[ind_right], m[ind_left]
            ind_left += 1
            ind_right -= 1
    if ind_left < right:
        QuickSort(m, ind_left, right)
    if ind_right > left:
        QuickSort(m, left, ind_right)
    return m


info()
print("Введите способ заполнения списка:")
print("1 - ввод элементов списка в одну строку через пробел:")
print("любое число - автоматическая генерация списка из n случайных элементов "
      "в заданном пользователем диапазоне:")
v = int(input())
print("")
m = []
if v == 1:
    print('Введите в строку элементы списка:')
    m = inputList(m)
else:
    n = int(input('Введите количество элементов списка:'))
    a, b = map(int, input('Введите диапазон элементов:').split())
    m = randomList(m, n, a, b)
    print(m)
    print('')
# Задача №1
c = findMax(m)
if c != -10 ** 10:
    print('Максимальный нечётный элемент', c)
else:
    print('В списке отсутствуют нечётные элементы')
print('')
# Задача №2
kr = int(input('Введите число, кратность которому нужно проверить:'))
ans = firstelement(m, kr)
if ans > len(m) - 1:
    print('В списке отсутствуют двузначные элементы, кратные', kr)
else:
    print('Индекс первого двузначного элемента, кратного', kr, '-', ans)
print('')
# Задача №3
print('Исходный список:')
print(m)
print('Список после быстрой сортировки:')
print(QuickSort(m, 0, len(m) - 1))




def info():
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


# Функция считает кол-во использования букв
def CounterOfUsingLetters(s):
    m = [0] * 26
    ans = ''
    for i in range(len(s)):
        for j in range(26):
            if s[i] == alf[j]:
                m[j] += 1
    for k in range(26):
        if m[k] != 0:
            ans += alf[k]
    if s == '\n':
        return ''
    if ans != '':
        return ans
    else:
        return "В данной строке нет букв"


# Функция возвращает строку для результирующего файла
def GetWord(s):
    if CounterOfUsingLetters(s) != "В данной строке нет букв":
        if len(CounterOfUsingLetters(s)) == 26:
            return 'no'
        else:
            return CounterOfUsingLetters(s)
    else:
        return CounterOfUsingLetters(s)


# Функция работает с файлами
def FileToFile(file1, file2):
    with open(fname1, 'r') as file1, open(fname2, 'w') as file2:
        for line in file1.readlines():
            line = line.upper()
            file2.write(GetWord(line) + '\n')


info()
alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
fname1 = input('Введите имя исходного файла: ')
if os.path.exists(fname1):
    fname2 = input("Введите имя результирующего файла: ")
    FileToFile(fname1, fname2)
    print('Задание выполнено')
else:
    print('Такого файла не существует')

def info():
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


    # Функция F(n)
    def f(n):
        if n < 2:
            return 1
        if n % 2 == 0:
            return f(n // 2) + 1
        else:
            return f(n - 3) + 3


    # Задание 1
    def MinN31(n):
        while f(n) != 31:
            n += 1
        return n


    # Задание 2
    def Task2(s):
        if s == 0:
            return 0
        elif s % 10 == 6 or s % 10 == 0:
            return Task2(s // 10) + 1
        else:
            return Task2(s // 10)


    info()
    print('Минимальное значение n, для которого F(n) равно 31 = ', MinN31(1))
    x = int(input('Введите значение x: '))
    s = f(x)
    print('Количество кратных 3 четных цифр результата вычисления F(x) = ', s, ':', Task2(s))


class HuffmanNode:
    def __init__(self, ch, frequency, left, right):
        self.ch = ch
        self.frequency = frequency
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + str(self.ch) + ", " + str(self.frequency) + ")"


class HuffmanCoding:
    def getCode(self, input):
        freqMap = self.buildFrequencyMap(input)
        nodeQueue = self.sortByFrequence(freqMap)
        self.root = self.buildTree(nodeQueue)
        codeMap = self.createHuffmanCode(self.root)
        return codeMap

    def buildFrequencyMap(self, input):
        map = {}
        for c in input:
            map[c] = map.get(c, 0) + 1
        return map

    def sortByFrequence(self, map):
        queue = []
        for k, v in map.items():
            queue.append(HuffmanNode(k, v, None, None))
        queue.sort(key=lambda x: x.frequency)
        return queue

    def buildTree(self, nodeQueue):
        while len(nodeQueue) > 1:
            node1 = nodeQueue.pop(0)
            node2 = nodeQueue.pop(0)
            node = HuffmanNode('', node1.frequency + node2.frequency, node1, node2)
            nodeQueue.append(node)
        return nodeQueue.pop(0)

    def createHuffmanCode(self, node):
        map = {}
        self.createCodeRec(node, map, "")
        return map

    def createCodeRec(self, node, map, s):
        if node.left == None and node.right == None:
            map[node.ch] = s
            return
        self.createCodeRec(node.left, map, s + '0')
        self.createCodeRec(node.right, map, s + '1')

    def encode(self, codeMap, input):
        s = ""
        for i in range(0, len(input)):
            s += codeMap.get(input[i])
        return s

    def decode(self, coded):
        s = ""
        curr = self.root
        for i in range(0, len(coded)):
            curr = curr.right if coded[i] == '1' else curr.left
            if curr.left == None and curr.right == None:
                s += curr.ch
                curr = self.root
        return s





def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1


def cmp(text, pattern):
    t = pattern
    p = [0] * len(t)
    j = 0
    i = 1
    while i < len(t):
        if t[j] == t[i]:
            p[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                p[i] = 0
                i += 1
            else:
                j = p[j - 1]
    a = text
    m = len(t)
    n = len(a)
    i = 0
    j = 0
    while i < n:
        if a[i] == t[j]:
            i += 1
            j += 1
            if j == m:
                print("Подстрока найдена! (кмп)")
                break
        else:
            if j > 0:
                j = p[j - 1]
            else:
                i += 1
    if i == n and j != m:
        print("Подстрока не найдена (кмп)")


def expand_from_center(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return s[left + 1:right]


def find_palindromes(s):
    palindromes = []
    for i in range(len(s)):
        pal1 = expand_from_center(s, i, i)
        if pal1 and len(pal1) != 1:
            palindromes.append(pal1)
        pal2 = expand_from_center(s, i, i + 1)
        if (pal2 and len(pal2) != 1):
            palindromes.append(pal2)
    return palindromes


def has_cycle(graph):
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            return True
    return False


def create_graph():
    graph = {}
    print("Введите вершины графа через пробел (например, A B C):")
    vertices = input().split()
    for vertex in vertices:
        graph[vertex] = []
    print("Введите ребра графа в формате 'вершина1 вершина2' (например, A B).\n"
          "Для завершения ввода введите '0'.")
    while True:
        edge = input().split()
        if edge[0] == '0':
            break
        if len(edge) != 2:
            print("Неверный формат ввода! Попробуйте снова.")
            continue
        if edge[0] not in graph or edge[1] not in graph:
            print("Такой вершины нет в графе! Попробуйте снова.")
            continue
        graph[edge[0]].append(edge[1])
    return graph


def menu():
    print(
        "1. Реализуйте наивный алгоритм и алгоритм Кнута-Морриса-Пратта для поиска подстроки в строке. "
        "Сравните эффективность алгоритмов на различных входных данных.\n"
        "2. Реализуйте алгоритм, который находит все палиндромные подстроки в данной строке.\n"
        "3. Реализуйте алгоритм кодирования Хаффмана для сжатия текстовых данных. (отдельно)\n"
        "4. Реализуйте алгоритм для определения циклов в графе."
    )



flag = True
while flag:
    menu()
    print("Выберите номер задания:")
    choose = int(input())
    if (choose == 1):
        print("Введите строку: ")
        main_s = str(input())
        print("Введите подстроку для поиска: ")
        subs = str(input())
        res1 = naive_search(main_s, subs)
        cmp(main_s, subs)
        if (res1 != -1):
            print("Подстрока найдена (наивно)")
        else:
            print("Такая подстрока не найдена (наивно)")
        print()
    elif (choose == 2):
        print("Введите строку: ")
        s = str(input())
        ans = find_palindromes(s)
        print(ans)
    elif (choose == 3):
        print()
    elif (choose == 4):
        graph = create_graph()
        if has_cycle(graph):
            print("Граф содержит циклы")
        else:
            print("Граф не содержит циклов")
