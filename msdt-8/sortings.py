from logging_config import logger, DEBUG_EX
from custom_operators import operator_gt, operator_le, operator_lt, \
    operator_ge


def bubble_sort(arr_, order_):
    logger.debug('Произошел вызов функции "bubble_sort"')
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
    logger.debug('Произошел вызов функции "cocktail_sort"')
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
    logger.debug('Произошел вызов функции "insertion_sort"')
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
    logger.debug('Произошел вызов функции "gnome_sort"')
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
    logger.debug('Произошел вызов функции "selection_sort"')
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
    logger.debug('Произошел вызов функции "comb_sort"')
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


# Функция вызова quick_sort. Используется чтобы debug log не учитывал рекурсию
def quicksort_exec(arr_, order_):
    logger.debug('Произошел вызов функции "quicksort_exec"')
    return quicksort(arr_, order_)


def quicksort(arr_, order_):
    logger.log(DEBUG_EX, 'Произошел вызов функции "quicksort"')
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

