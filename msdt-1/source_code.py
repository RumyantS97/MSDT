def less_than(a, b):
    return a < b

def greater_than(a, b):
    return a > b

def equal_to(a, b):
    return a == b

def not_equal_to(a, b):
    return a != b

def less_than_or_equal_to(a, b):
    return a <= b

def greater_than_or_equal_to(a, b):
    return a >= b

operator_lt = less_than
operator_gt = greater_than
operator_eq = equal_to
operator_ne = not_equal_to
operator_le = less_than_or_equal_to
operator_ge = greater_than_or_equal_to

def bubble_sort(arr, order):
    operatorRighter = operator_gt if order else operator_le
    n = len(arr)
    # Проходим по всем элементам массива
    for i in range(n):
        # Флаг для проверки, были ли произведены обмены
        swapped = False
        # Последние i элементов уже отсортированы
        for j in range(0, n - i - 1):
            # Сравниваем соседние элементы
            if operatorRighter(arr[j],arr[j+1]):
                # Меняем местами, если они в неправильном порядке
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Если не было обменов, массив уже отсортирован
        if not swapped:
            break

def cocktail_sort(arr, order):
    operatorLefter = operator_lt if order else operator_ge
    operatorRighter = operator_gt if order else operator_le

    n = len(arr)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        # Сбрасываем флаг swapped для текущего прохода
        swapped = False

        # Проход слева направо
        for i in range(start, end):
            if operatorRighter(arr[i],arr[i+1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        # Если ничего не было обменяно, массив уже отсортирован
        if not swapped:
            break

        # Уменьшаем конец, так как последний элемент уже на своем месте
        end -= 1

        # Сбрасываем флаг swapped для следующего прохода
        swapped = False

        # Проход справа налево
        for i in range(end, start, -1):
            if operatorLefter(arr[i],arr[i-1]):
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True

        # Увеличиваем начало, так как первый элемент уже на своем месте
        start += 1


def insertion_sort(arr, order):
    operatorRighter = operator_gt if order else operator_le
    # Проходим по всем элементам массива, начиная со второго
    for i in range(1, len(arr)):
        key = arr[i]  # Текущий элемент для вставки
        j = i - 1

        # Сдвигаем элементы, которые больше ключа, на одну позицию вправо
        while j >= 0 and operatorRighter(arr[j],key):
            arr[j + 1] = arr[j]
            j -= 1

        # Вставляем ключ на его правильное место
        arr[j + 1] = key

def gnome_sort(arr, order):
    operatorLefter = operator_lt if order else operator_ge
    index = 0
    n = len(arr)

    while index < n:
        # Если текущий элемент больше следующего, меняем их местами
        if index == 0 or operatorLefter(arr[index-1],arr[index]):
            index += 1
        else:
            # Меняем местами элементы
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1

def selection_sort(arr, order):
    operatorLefter = operator_lt if order else operator_ge
    n = len(arr)
    # Проходим по всем элементам массива
    for i in range(n):
        # Предполагаем, что текущий элемент является минимальным
        min_index = i
        # Сравниваем с остальными элементами
        for j in range(i + 1, n):
            if operatorLefter(arr[j],arr[min_index]):
                min_index = j
        # Меняем местами найденный минимальный элемент
        # с первым элементом неотсортированной части
        arr[i], arr[min_index] = arr[min_index], arr[i]


def comb_sort(arr, order):
    operatorRighter = operator_gt if order else operator_le
    n = len(arr)
    gap = n  # Начальное расстояние
    shrink_factor = 1.3  # Фактор уменьшения расстояния
    sorted = False  # Флаг для отслеживания, отсортирован ли массив

    while not sorted:
        # Уменьшаем расстояние
        gap = int(gap / shrink_factor)
        if gap < 1:
            gap = 1

        sorted = True  # Предполагаем, что массив отсортирован

        # Сравниваем элементы с текущим расстоянием
        for i in range(n - gap):
            if operatorRighter(arr[i],arr[i+gap]):
                # Меняем местами, если они в неправильном порядке
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                # Если произошла замена, массив не отсортирован
                sorted = False

def quicksort(arr, order):
    operatorLefter = operator_lt if order else operator_gt
    operatorRighter = operator_gt if order else operator_lt
    if len(arr) <= 1:
        return arr
    else:
        # Выбираем опорный элемент (пивот)
        pivot = arr[len(arr) // 2]
        # Элементы меньше пивота
        left = [x for x in arr if operatorLefter(x,pivot)]
        # Элементы равные пивоту
        middle = [x for x in arr if x == pivot]
        # Элементы больше пивота
        right = [x for x in arr if operatorRighter(x,pivot)]
        # Рекурсивно сортируем и объединяем
        return quicksort(left, order) + middle + quicksort(right, order)


def selectTypeSort():
    typeSort = order = 1
    while True:
        # Запрашиваем ввод числа от 1 до 7
        print("Чтобы выбрать сортировку пузырьком - нажмите 1\n"
              "Чтобы выбрать сортировку перемешиванием - нажмите 2\n"
              "Чтобы выбрать сортировку вставками - нажмите 3\n"
              "Чтобы выбрать гномью сортировку - нажмите 4\n"
              "Чтобы выбрать сортировку выбором - нажмите 5\n"
              "Чтобы выбрать сортировку расческой - нажмите 6\n"
              "Чтобы выбрать быструю сортировку - нажмите 7\n")
        left = 1; right = 7
        try:
            typeSort = int(input(f"Введите число от {left} до {right}: "))
            if typeSort < left or typeSort > right:
                raise BaseException("Число вне диапазона.")
        except BaseException:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
            continue

        # Запрашиваем ввод числа 1 или 2
        print("Чтобы сортировать по возрастанию - нажмите 1\n"
              "Чтобы сортировать по убыванию нажмите - 2")
        left = 1; right = 2
        try:
            order = int(input(f"Введите число от {left} до {right}: "))
            if order < left or order > right:
                raise BaseException("Число вне диапазона.")
        except BaseException:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
            continue

        # Выход из цикла после успешного выполнения
        break

    return typeSort, order

def display_array(arr):
    """Выводит массив в зависимости от его длины."""
    if len(arr) < 40:
        # Если длина массива меньше 40, выводим весь массив
        print(arr)
    else:
        # Если длина больше 40, выводим первые 20 и последние 20 элементов
        print(arr[:20] + ['...'] + arr[-20:])

import random
import time

if __name__ == "__main__":
    print("Сортировки. Захарова Милана")
    typeSort, order = selectTypeSort()
    n = 1000
    arr = [random.randint(0, 100) for _ in range(n)]
    result = arr.copy()
    start_time = end_time = 0

    if typeSort == 1:
        print("Сортировка пузырьком")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            bubble_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            bubble_sort(result, False)
            end_time = time.time()

    elif typeSort == 2:
        print("Сортировка перемешиванием")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            cocktail_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            cocktail_sort(result, False)
            end_time = time.time()

    elif typeSort == 3:
        print("Сортировка вставками")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            insertion_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            insertion_sort(result, False)
            end_time = time.time()

    elif typeSort == 4:
        print("Гномья сортировка")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            gnome_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            gnome_sort(result, False)
            end_time = time.time()

    elif typeSort == 5:
        print("Сортировка выбором")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            selection_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            selection_sort(result, False)
            end_time = time.time()

    elif typeSort == 6:
        print("Сортировка расческой")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            comb_sort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            comb_sort(result, False)
            end_time = time.time()

    elif typeSort == 7:
        print("Быстрая сортировка")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = quicksort(result, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = quicksort(result, False)
            end_time = time.time()


    print("Исходный массив:")
    display_array(arr)
    print("Результат:")
    display_array(result)
    print(f"Время выполнения: {(end_time-start_time):.8f} секунд")
