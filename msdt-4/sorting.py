import random
import time


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


def bubble_sort(arr_, order_):
    operator_righter = operator_gt if order_ else operator_le
    n_ = len(arr_)
    # Проходим по всем элементам массива
    for i in range(n_):
        # Флаг для проверки, были ли произведены обмены
        swapped = False
        # Последние i элементов уже отсортированы
        for j in range(0, n_ - i - 1):
            # Сравниваем соседние элементы
            if operator_righter(arr_[j], arr_[j + 1]):
                # Меняем местами, если они в неправильном порядке
                arr_[j], arr_[j + 1] = arr_[j + 1], arr_[j]
                swapped = True
        # Если не было обменов, массив уже отсортирован
        if not swapped:
            break


def cocktail_sort(arr_, order_):
    operator_lefter = operator_lt if order_ else operator_ge
    operator_righter = operator_gt if order_ else operator_le

    n_ = len(arr_)
    swapped = True
    start = 0
    end = n_ - 1

    while swapped:
        # Сбрасываем флаг swapped для текущего прохода
        swapped = False

        # Проход слева направо
        for i in range(start, end):
            if operator_righter(arr_[i], arr_[i + 1]):
                arr_[i], arr_[i + 1] = arr_[i + 1], arr_[i]
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
            if operator_lefter(arr_[i], arr_[i - 1]):
                arr_[i], arr_[i - 1] = arr_[i - 1], arr_[i]
                swapped = True

        # Увеличиваем начало, так как первый элемент уже на своем месте
        start += 1


def insertion_sort(arr_, order_):
    operator_righter = operator_gt if order_ else operator_le
    # Проходим по всем элементам массива, начиная со второго
    for i in range(1, len(arr_)):
        key = arr_[i]  # Текущий элемент для вставки
        j = i - 1

        # Сдвигаем элементы, которые больше ключа, на одну позицию вправо
        while j >= 0 and operator_righter(arr_[j], key):
            arr_[j + 1] = arr_[j]
            j -= 1

        # Вставляем ключ на его правильное место
        arr_[j + 1] = key


def gnome_sort(arr_, order_):
    operator_lefter = operator_lt if order_ else operator_ge
    index = 0
    n_ = len(arr_)

    while index < n_:
        # Если текущий элемент больше следующего, меняем их местами
        if index == 0 or operator_lefter(arr_[index - 1], arr_[index]):
            index += 1
        else:
            # Меняем местами элементы
            arr_[index], arr_[index - 1] = arr_[index - 1], arr_[index]
            index -= 1


def selection_sort(arr_, order_):
    operator_lefter = operator_lt if order_ else operator_ge
    n_ = len(arr_)
    # Проходим по всем элементам массива
    for i in range(n_):
        # Предполагаем, что текущий элемент является минимальным
        min_index = i
        # Сравниваем с остальными элементами
        for j in range(i + 1, n_):
            if operator_lefter(arr_[j], arr_[min_index]):
                min_index = j
        # Меняем местами найденный минимальный элемент
        # с первым элементом неотсортированной части
        arr_[i], arr_[min_index] = arr_[min_index], arr_[i]


def comb_sort(arr_, order_):
    operator_righter = operator_gt if order_ else operator_le
    n_ = len(arr_)
    gap = n_  # Начальное расстояние
    shrink_factor = 2  # Фактор уменьшения расстояния
    sorted_ = False  # Флаг для отслеживания, отсортирован ли массив

    while not sorted_:
        # Уменьшаем расстояние
        gap = int(gap / shrink_factor)
        if gap < 1:
            gap = 1

        sorted_ = True  # Предполагаем, что массив отсортирован

        # Сравниваем элементы с текущим расстоянием
        for i in range(n_ - gap):
            if operator_righter(arr_[i], arr_[i + gap]):
                # Меняем местами, если они в неправильном порядке
                arr_[i], arr_[i + gap] = arr_[i + gap], arr_[i]
                # Если произошла замена, массив не отсортирован
                sorted_ = False


def quicksort(arr_, order_):
    operator_lefter = operator_lt if order_ else operator_gt
    operator_righter = operator_gt if order_ else operator_lt
    if len(arr_) <= 1:
        return arr_
    else:
        # Выбираем опорный элемент (пивот)
        pivot = arr_[len(arr_) // 2]
        # Элементы меньше пивота
        left = [x for x in arr_ if operator_lefter(x, pivot)]
        # Элементы равные пивоту
        middle = [x for x in arr_ if x == pivot]
        # Элементы больше пивота
        right = [x for x in arr_ if operator_righter(x, pivot)]
        # Рекурсивно сортируем и объединяем
        return quicksort(left, order_) + middle + quicksort(right, order_)


def select_type_sort():
    type_sort_ = order_ = 1
    while True:
        # Запрашиваем ввод числа от 1 до 7
        print("Чтобы выбрать сортировку пузырьком - нажмите 1\n"
              "Чтобы выбрать сортировку перемешиванием - нажмите 2\n"
              "Чтобы выбрать сортировку вставками - нажмите 3\n"
              "Чтобы выбрать гномью сортировку - нажмите 4\n"
              "Чтобы выбрать сортировку выбором - нажмите 5\n"
              "Чтобы выбрать сортировку расческой - нажмите 6\n"
              "Чтобы выбрать быструю сортировку - нажмите 7\n")
        left = 1
        right = 7
        try:
            type_sort_ = int(input(f"Введите число от {left} до {right}: "))
            if type_sort_ < left or type_sort_ > right:
                raise ValueError("Число вне диапазона.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
            continue

        # Запрашиваем ввод числа 1 или 2
        print("Чтобы сортировать по возрастанию - нажмите 1\n"
              "Чтобы сортировать по убыванию нажмите - 2")
        left = 1
        right = 2
        try:
            order_ = int(input(f"Введите число от {left} до {right}: "))
            if order_ < left or order_ > right:
                raise ValueError("Число вне диапазона.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
            continue

        # Выход из цикла после успешного выполнения
        break

    return type_sort_, order_


def display_array(arr_):
    """Выводит массив в зависимости от его длины."""
    if len(arr_) < 40:
        # Если длина массива меньше 40, выводим весь массив
        print(arr_)
    else:
        # Если длина больше 40, выводим первые 20 и последние 20 элементов
        print(arr_[:20] + ['...'] + arr_[-20:])


if __name__ == "__main__":
    print("Сортировки. Захарова Милана")
    type_sort, order = select_type_sort()
    n = 1000
    arr = [random.randint(0, 100) for _ in range(n)]
    result = arr.copy()
    start_time = end_time = 0

    if type_sort == 1:
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

    elif type_sort == 2:
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

    elif type_sort == 3:
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

    elif type_sort == 4:
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

    elif type_sort == 5:
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

    elif type_sort == 6:
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

    elif type_sort == 7:
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
