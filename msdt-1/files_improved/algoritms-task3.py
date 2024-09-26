from collections import deque

class MyStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self):
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        return self.stack.pop()

    def min(self):
        return self.min_stack[-1]


def check_brackets(s):
    stack = []
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0


def find_max_in_window(arr, k):
    if len(arr) == 0 or k <= 0:
        return

    window = deque()  # Создаем пустую двустороннюю очередь для хранения индексов элементов

    for i in range(len(arr)):
        # Удаляем из очереди индексы элементов, которые выходят за пределы текущего окна
        while window and window[0] <= i - k:
            window.popleft()

        # Удаляем из очереди индексы элементов, которые < текущего (уже не могут быть максимумом в текущем окне)
        while window and arr[i] >= arr[window[-1]]:
            window.pop()

        # Добавляем индекс текущего элемента в очередь
        window.append(i)

        # Если текущий индекс больше или равен размеру окна - 1, значит можем вывести максимум
        if i >= k - 1:
            print(arr[window[0]], end=" ")


def find_duplicates(arr):
    print("\nПовторяющиеся числа: ")
    for num in arr:
        if arr[abs(num)] > 0:
            arr[abs(num)] *= -1
        else:
            print(abs(num), end=" ")


def set_zeros(matrix):
    row = [False] * len(matrix)
    column = [False] * len(matrix[0])

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                row[i] = True
                column[j] = True

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if row[i] or column[j]:
                matrix[i][j] = 0


# 1. Дана строка со скобками. Проверьте правильность расстановки скобок за время О(n).
# а) в строке содержатся только круглые скобки;
# б) скобки могут быть любые.
# 2. Реализуйте «вручную» стек со стандартными функциями push/pop и дополнительной
# функцией min, возвращающей минимальный элемент стека. Все эти функции должны
# работать за O(1). Память должна быть оптимальна.
# 3. Задача «Поддержания max в окне». Дан массив размером n и счетчик k, определяющий
# размер окна в массиве. Окно двигается от начала до конца массива. Необходимо найти
# максимум в окне и напечатать все их значения. Время работы алгоритма должно быть
# О(n) и не зависеть от k.
# 4. Дан массив размера n+1. Элементы массива числа из множества {1, 2, 3 ... n}. Найдите
# повторяющееся число за время О(n), не используя дополнительной памяти.
# Повторяющихся элементов может быть несколько.
# 5. Обнулите столбец N и строку M матрицы, если элемент в ячейке (N, M) нулевой. Затраты
# памяти и времени работы должны быть минимизированы.


print("1 - проверка строки со скобками")
print("2 - проверка стека")
print("3 - max в окне")
print("4 - поиск дубликатов в массиве")
print("5 - обнулить столбец N и строку M матрицы, если элемент в ячейке (N, M) нулевой")
print("Выберите задание: ")

choice = int(input())
if choice == 1:
    print("Введите строку для проверки скобок: ")
    string_with_brackets = input()
    print(check_brackets(string_with_brackets))

elif choice == 2:
    stack = MyStack()
    stack.push(3)
    stack.push(5)
    stack.push(2)
    print(stack.min())  # 2
    stack.pop()
    print(stack.min())  # 3


elif choice == 3:
    print("Введите массив: ")
    arr = list(map(int, input().split(" ")))
    print("Введите k: ")
    k = int(input())
    find_max_in_window(arr, k)

elif choice == 4:
    print("Введите массив: ")
    arr = list(map(int, input().split(" ")))
    find_duplicates(arr)

elif choice == 5:
    matrix = [[1, 2, 3],
              [4, 0, 6],
              [7, 8, 9]]
    set_zeros(matrix)
    for row in matrix:
        print(row)

else:
    print("Ошибка")
