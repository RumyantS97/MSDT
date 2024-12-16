from collections import deque

# Лабораторная работа №2

# ЗАДАНИЕ 1

# Метод для задания 1
def round_brackets(string):
    stack = []
    for char in string:  # Сложность O(N)
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
    # Если stack пустой, то строка корректна
    return len(stack) == 0


# Метод для задания 1
def check_brackets(string):
    stack = []
    # dictionary = {key = value}
    # Keys - закрывающие скобки
    # Values - открывающие скобки
    bracket_dict = {')': '(', ']': '[', '}': '{', '>': '<'}

    for char in string:  # Сложность O(N)

        # Открывающиеся скобки заносим в stack
        if char in bracket_dict.values():
            stack.append(char)

        # Если встретилась закрывающаяся скобка:
        elif char in bracket_dict.keys():
            # Если stack пустой или value для скобки (лежит в stack) != текущему символу
            if not stack or bracket_dict[char] != stack.pop():
                # Возвращаем false
                return False

    # Если stack пустой, то строка корректна
    return len(stack) == 0


# Выполнение задания 1
print("ЗАДАНИЕ 1")
input_string = input("Введите строку: ")
print("\nПроверка круглых скобок: " + str(round_brackets(input_string)))
print("Проверка всех скобок: " + str(check_brackets(input_string)))


# ЗАДАНИЕ 2
class Stack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def get_min(self):
        if self.min_stack:  # У всех текущих условных операторов сложность константная
            # Последний элемент стека - минимальный
            return self.min_stack[-1]

    def push(self, value):
        self.stack.append(value)
        # Если min_stack пустой или элемент <= минимального
        if not self.min_stack or value <= self.min_stack[-1]:
            # Заносим его в min_stack
            self.min_stack.append(value)

    def pop(self):
        if self.stack:
            popped_value = self.stack.pop()
            # Если удаляемый элемент - минимальный
            if popped_value == self.min_stack[-1]:
                # Удаляем из min_stack последний
                self.min_stack.pop()
            return popped_value


print("ЗАДАНИЕ 2")
stack_instance = Stack()
num_elements = int(input("Укажите, сколько элементов добавить в stack: "))
for i in range(num_elements):
    value = int(input(f"Укажите значение элемента №{i}: "))
    stack_instance.push(value)
print("Stack: ", stack_instance.stack)
print("Минимальный элемент:", stack_instance.get_min())
num_remove = int(input("Укажите, сколько элементов удалить: "))
for i in range(num_remove):
    stack_instance.pop()
print("Stack:", stack_instance.stack)
print("Минимальный элемент:", stack_instance.get_min())


# ЗАДАНИЕ 3
# Метод для задания 3
def window_max(arr, k):  # Сложность - O(N), от k не зависит
    n = len(arr)

    # Создаю двухстороннюю очередь deque
    window = deque()

    # Очередь - элементы по убыванию, где максимальный - первый.

    # Работа с очередью
    def window_add(i):

        # Если очередь не пустая, и если текущий элемент >=
        # последнего элемента в очереди, то есть самого минимального
        while window and arr[i] >= arr[window[-1]]:
            window.pop()  # Удаляем последний элемент из очереди

        # Добавляем текущий элемент в конец очереди
        window.append(i)

    # Удаление элемента, выходящего за пределы окна
    def window_delete(i):
        # Если в начале очереди хранится индекс удаляемого элемента
        if window and window[0] == i:
            # Удаление из начала очереди (слева)
            window.popleft()

    # Инициализация окна
    for i in range(k):  # Обход элементов первого окна
        window_add(i)  # Заносим их в окно

    # Обход остальных элементов
    for i in range(k, n):
        # Вывод максимального из окна
        print(arr[window[0]])

        # Сдвигаем окно вправо
        # Удаление элемента, выходящего за пределы
        window_delete(i - k)
        # Добавление нового элемента
        window_add(i)

    # Вывод финального максимума
    print(arr[window[0]])


# Выполнение задания 3
print("\nЗАДАНИЕ 3")
arr3 = []
arr_size = int(input("Укажите размер массива (n): "))
for i in range(arr_size):
    arr3.append(int(input(f"Укажите значение элемента массива №{i}:")))

k_value = int(input("Укажите значение k: "))
while k_value > arr_size or k_value < 1:
    print("[!] Некорректный ввод")
    k_value = int(input("Повторите ввод: "))

print("Массив: ", arr3)
print("Размер окна: ", k_value)
print("Максимумы: ")
window_max(arr3, k_value)


# ЗАДАНИЕ 4
# Метод для задания 4
def find_duplicates(arr):
    if not arr:
        print("[!] Входной массив пустой.")
        return set()

    # Множество для повторяющихся элементов
    duplicates = set()

    try:
        # Проходим по элементам массива
        for number in arr:  # Сложность O(N)
            # Получаем модуль числа
            number_abs = abs(number)

            # number_abs считается дубликатом, если значение элемента по индексу
            # number_abs отрицательное
            if arr[number_abs] < 0:
                # Добавляем число в множество дубликатов
                duplicates.add(number_abs)

            # Делаем число отрицательным (метка)
            else:
                arr[number_abs] = -arr[number_abs]
    except IndexError:
        print("[!] Ошибка: значение элемента массива выходит за пределы индекса.")
    return duplicates


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
print("Повторяющиеся элементы:", find_duplicates(arr4))


# ЗАДАНИЕ 5
# Метод для задания 5
def reset_to_zero(matrix, rows, cols):
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
num_rows = int(input("Укажите количество строк: "))
num_cols = int(input("Укажите количество столбцов: "))

matrix = []
rows = set()
cols = set()
print("Заполнение матрицы:")

for i in range(num_rows):
    row = []
    for j in range(num_cols):
        value = int(input(f"Введите значение для элемента ({i}, {j}): "))
        row.append(value)
        if value == 0:
            rows.add(i)
            cols.add(j)
    matrix.append(row)

print("Исходная матрица:")
for row in matrix:
    print(row)

reset_to_zero(matrix, rows, cols)

print("Результирующая матрица:")
for row in matrix:
    print(row)


# ЗАДАНИЕ 6
# Метод для задания 6
def is_anagram(s1, s2):
    if not s1 or not s2:
        return False

    # Проверка длины строк
    if len(s1) != len(s2):
        return False

    # Считаем количество каждого символа в первой строке
    char_count = {}
    for char in s1:  # Сложность O(N)
        char_count[char] = char_count.get(char, 0) + 1

    # Проверяем, совпадают ли символы во второй строке
    for char in s2:  # Сложность O(N)
        if char not in char_count or char_count[char] == 0:
            return False
        char_count[char] -= 1

    return True


# Выполнение задания 6
print("\nЗАДАНИЕ 6")
string1 = input("Введите первую строку: ")
string2 = input("Введите вторую строку: ")
if is_anagram(string1.strip(), string2.strip()):
    print("Строки являются анаграммами.")
else:
    print("Строки не являются анаграммами.")


# ЗАДАНИЕ 7
# Метод для задания 7
def majority_element(arr):
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
arr_size = int(input("Введите размер массива: "))
arr7 = []
for i in range(arr_size):
    arr7.append(int(input(f"Введите значение элемента массива №{i}: ")))

result = majority_element(arr7)
if result is not None:
    print(f"Элемент {result} встречается более чем в половине случаев.")
else:
    print("Нет элемента, который встречается более чем в половине случаев.")
