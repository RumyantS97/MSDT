from collections import deque

# Лабораторная работа №2

# ЗАДАНИЕ 1

# Метод для задания 1
def roundBrackets(string):
    stack = []
    for char in string:                                             # Сложность O(N)
        # Открывающиеся скобки заносим в stack
        if char == '(':
            stack.append(char)

        # Если встретилась закрывающаяся скобка и stack не пустой:
        elif char == ')' and len(stack) != 0:
            # Извлекаем крайний элемент
            stack.pop()
        # Если встретился любой другой символ кроме круглых скобок:
        else:
            # Возвращаем false
            return False
    # Если stack путой, то строка корректна
    return len(stack) == 0


# Метод для задания 1
def brackets(string):
    stack = []
    # Dictionary = {key = value}
    # Keys - закрыващиеся скобки
    # Values - открывающиеся скобки
    dictionary = {')': '(', ']': '[', '}': '{', '>': '<'}

    for char in string:                                       # Сложность O(N)

        # Открывающиеся скобки заносим в stack
        if char in dictionary.values():
            stack.append(char)

        # Если встретилась закрывающаяся скобка:
        elif char in dictionary.keys():
            # Если stack пустой или value для скобки (лежит в stack) != текущему символу
            if not stack or dictionary[char] != stack.pop():
                # Возвращаем false
                return False

    # Если stack путой, то строка корректна
    return len(stack) == 0


# Выполнение задания 1
print("ЗАДАНИЕ 1")
s1 = input("Введите строку: ")
print("\nПроверка круглых скобок: " + str(roundBrackets(s1)))
print("Проверка всех скобок: " + str(brackets(s1)))


# ЗАДАНИЕ 2
class Stack:
    def __init__(self):
        self.stack = []
        self.minstack = []

    def min(self):
        if self.minstack:                                # У всех текущих условных операторов сложность константная
            # Последний элемент стека - минимальный
            return self.minstack[-1]

    def push(self, x):
        self.stack.append(x)
        # Если minstack пустой или элемент <= минимального
        if not self.minstack or x <= self.minstack[-1]:
            # Заносим его в minstack
            self.minstack.append(x)

    def pop(self):
        if self.stack:
            bye = self.stack.pop()
            # Если удаляемый элемент - минимальный
            if bye == self.minstack[-1]:
                # Удаляем из minstack последний
                self.minstack.pop()
            return bye


print("ЗАДАНИЕ 2")
stack = Stack()
leng = int(input("Укажите, сколько элементов добавить в stack: "))
for i in range(leng):
    val = int(input(f"Укажите значение элемента №{i}: "))
    stack.push(val)
print("Stack: ", stack.stack)
print("Минимальный элемент:", stack.min())
k = int(input("Укажите, сколько элементов удалить: "))
for i in range(k):
    stack.pop()
print("Stack:", stack.stack)
print("Минимальный элемент:", stack.min())


# ЗАДАНИЕ 3
# Метод для задания 3
def windowMax(arr, k):                      # Сложность - O(N), от k не зависит
    n = len(arr)

    # Создаю двухстороннюю очередь deque
    window = deque()

    # Очередь - элементы по убыванию, где максимальный - первый.

    # Работа с очередью
    def windowAdd(i):

        # Если очередь не пустая, и если текущий элемент >= последнего элемента в очереди, то есть самого минимального
        while window and arr[i] >= arr[window[-1]]:
            window.pop()  # Удаляем последний элемент из очереди

        # Добавляем текущий элемент в конец очереди
        window.append(i)

    # Удаление элемента, выходящего за пределы окна
    def windowDelete(i):
        # Если в начале очереди хранится индекс удаляемого элемента
        if window and window[0] == i:
            # Удаление из начала очереди (слева)
            window.popleft()

    # Инициализация окна
    for i in range(k):    # Обход элементов первого окна
        windowAdd(i)  # Заносим их в окно

    # Обход остальных элементов
    for i in range(k, n):
        # Вывод максимального из окна
        print(arr[window[0]])

        # Сдвигаем окно вправо
        # Удаление элемента, выходящего за пределы
        windowDelete(i - k)
        # Добавление нового элемента
        windowAdd(i)

    # Вывод финального максимума
    print(arr[window[0]])


# Выполнение задания 3
print("\nЗАДАНИЕ 3")
arr3 = []
n = int(input("Укажите размер массива (n): "))
for i in range(n):
    arr3.append(int(input(f"Укажите значение элемента массива №{i}:")))

k = int(input("Укажите значение k: "))
while k > n or k < 1:
    print("[!] Некорректный ввод")
    k = int(input("Повторите ввод: "))

print("Массив: ", arr3)
print("Размер окна: ", k)
print("Максимумы: ")
windowMax(arr3, k)


# ЗАДАНИЕ 4
# Метод для задания 4
def duplicateFind(arr):
    if not arr:
        print("[!] Входной массив пустой.")
        return set()

    # Множество для повторяющихся элементов
    duplicate = set()

    try:
        # Проходим по элементам массива
        for number in arr:  # Сложность O(N)
            # Получаем модуль числа
            numberAbs = abs(number)

            # numberAbs считается дубликатом, если значение элемента по индексу numberAbs отрицательное
            if arr[numberAbs] < 0:
                # Добавляем число в множество дубликатов
                duplicate.add(numberAbs)

            # делаем число отрицательным (метка)
            else:
                arr[numberAbs] = -arr[numberAbs]
    except IndexError:
        print("[!] Ошибка: значение элемента массива выходит за пределы индекса.")
    return duplicate


# Выполнение задания 4
print("\nЗАДАНИЕ 4")
arr4 = []
n = int(input("Укажите n: "))
for i in range(n + 1):
    k = int(input(f"Укажите значение элемента массива {i}: "))
    while k <= 0 or k > n:
        print("[!] Некорректный ввод. Значение должно быть от 1 до n.")
        k = int(input("Повторите ввод: "))
    arr4.append(k)

print("Исходный массив:")
print(arr4)
print("Повторяющиеся элементы:", duplicateFind(arr4))


# ЗАДАНИЕ 5
# Метод для задания 5
def resetZero(matrix, rows, cols):
    if not matrix:
        print("[!] Матрица пуста.")
        return

    # Обнуление строк
    for i in rows:
        for j in range(len(matrix[0])):
            matrix[i][j] = 0

    # Обнуление столбцов
    for i in range(len(matrix)):
        for j in cols:
            matrix[i][j] = 0


print("\nЗАДАНИЕ 5")
x = int(input("Укажите количество строк: "))
y = int(input("Укажите количество столбцов: "))

matrix = []
rows = set()
cols = set()
print("Заполнение матрицы:")

for i in range(x):
    row = []
    for j in range(y):
        value = int(input(f"Введите значение для элемента ({i}, {j}): "))
        row.append(value)
        if value == 0:
            rows.add(i)
            cols.add(j)
    matrix.append(row)

print("Исходная матрица:")
for row in matrix:
    print(row)

resetZero(matrix, rows, cols)

print("Результирующая матрица:")
for row in matrix:
    print(row)


# ЗАДАНИЕ 6
# Метод для задания 6
def isAnagram(s1, s2):
    if not s1 or not s2:
        return False

    # Проверка длины строк
    if len(s1) != len(s2):
        return False

    # Считаем количество каждого символа в первой строке
    count = {}
    for char in s1:  # Сложность O(N)
        count[char] = count.get(char, 0) + 1

    # Проверяем, совпадают ли символы во второй строке
    for char in s2:  # Сложность O(N)
        if char not in count or count[char] == 0:
            return False
        count[char] -= 1

    return True


# Выполнение задания 6
print("\nЗАДАНИЕ 6")
s1 = input("Введите первую строку: ")
s2 = input("Введите вторую строку: ")
if isAnagram(s1.strip(), s2.strip()):
    print("Строки являются анаграммами.")
else:
    print("Строки не являются анаграммами.")


# ЗАДАНИЕ 7
# Метод для задания 7
def majorityElement(arr):
    if not arr:
        print("[!] Входной массив пустой.")
        return None

    # Алгоритм Boyer-Moore для нахождения кандидата
    candidate = None
    count = 0

    # Первый проход: определение кандидата
    for num in arr:  # Сложность O(N)
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)

    # Второй проход: проверка кандидата
    count = 0
    for num in arr:  # Сложность O(N)
        if num == candidate:
            count += 1

    # Возвращаем кандидат, если он встречается более n/2 раз
    return candidate if count > len(arr) // 2 else None


# Выполнение задания 7
print("\nЗАДАНИЕ 7")
n = int(input("Введите размер массива: "))
arr7 = []
for i in range(n):
    arr7.append(int(input(f"Введите значение элемента массива №{i}: ")))

result = majorityElement(arr7)
if result is not None:
    print(f"Элемент {result} встречается более чем в половине случаев.")
else:
    print("Нет элемента, который встречается более чем в половине случаев.")
