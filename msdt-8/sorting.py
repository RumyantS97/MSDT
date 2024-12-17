import random
import time
from logging_config import logger
from sortings import bubble_sort, cocktail_sort, insertion_sort, \
    gnome_sort, selection_sort, comb_sort, quicksort


def select_type_sort():
    logger.debug('Произошел вызов функции "select_type_sort"')
    type_sort_ = order_ = 0
    type_selected = order_selected = False
    while True:
        if not type_selected:
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
            type_sort_temp = 0
            try:
                type_sort_temp = int(input(f"Введите число от "
                                           f"{left} до {right}: "))
                if type_sort_temp < left or type_sort_temp > right:
                    logger.warning(f'Пользователь ввел "{type_sort_temp}", '
                                   f'ожидалось число от {left} до {right}')
                    raise ValueError("Число вне диапазона.")
            except ValueError:
                if type_sort_temp == 0:
                    logger.warning('Пользователь ввел не число, '
                                   f'ожидалось число от {left} до {right}')
                print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
                continue
            type_selected = True
            type_sort_ = type_sort_temp
            logger.debug(f'Пользователь выбрал тип сортировки {type_sort_}')

        if not order_selected:
            # Запрашиваем ввод числа 1 или 2
            print("Чтобы сортировать по возрастанию - нажмите 1\n"
                  "Чтобы сортировать по убыванию нажмите - 2")
            left = 1
            right = 2
            order_temp = 0
            try:
                order_temp = int(input(f"Введите число от "
                                       f"{left} до {right}: "))
                if order_temp < left or order_temp > right:
                    logger.warning(f'Пользователь ввел "{order_temp}", '
                                   f'ожидалось число от {left} до {right}')
                    raise ValueError("Число вне диапазона.")
            except ValueError:
                if order_temp == 0:
                    logger.warning('Пользователь ввел не число, '
                                   f'ожидалось число от {left} до {right}')
                print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
                continue
            order_ = order_temp
            logger.debug(f'Пользователь выбрал направление {order_}')

        # Выход из цикла после успешного выполнения
        break

    return type_sort_, order_


def display_array(arr_):
    logger.debug('Произошел вызов функции "display_array"')
    """Выводит массив в зависимости от его длины."""
    if len(arr_) < 40:
        # Если длина массива меньше 40, выводим весь массив
        print(arr_)
    else:
        # Если длина больше 40, выводим первые 20 и последние 20 элементов
        print(arr_[:20] + ['...'] + arr_[-20:])


def main():
    logger.debug('Произошел вызов функции "main"')
    type_sort, order = select_type_sort()
    n = 10
    source_arr = [random.randint(0, 100) for _ in range(n)]
    logger.info(f'Пользователь выбрал тип сортировки: {type_sort}, '
                f'направление сортировки: {order}')
    start_time = end_time = 0

    if type_sort == 1:
        print("Сортировка пузырьком")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = bubble_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = bubble_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 2:
        print("Сортировка перемешиванием")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = cocktail_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = cocktail_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 3:
        print("Сортировка вставками")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = insertion_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = insertion_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 4:
        print("Гномья сортировка")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = gnome_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = gnome_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 5:
        print("Сортировка выбором")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = selection_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = selection_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 6:
        print("Сортировка расческой")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = comb_sort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = comb_sort(source_arr, False)
            end_time = time.time()

    elif type_sort == 7:
        print("Быстрая сортировка")
        if order == 1:
            print("Тип сортировки: по возрастанию")
            start_time = time.time()
            result = quicksort(source_arr, True)
            end_time = time.time()
        else:
            print("Тип сортировки: по убыванию")
            start_time = time.time()
            result = quicksort(source_arr, False)
            end_time = time.time()

    print("Исходный массив:")
    display_array(source_arr)
    print("Результат:")
    display_array(result)
    time_sort = end_time - start_time
    print(f"Время выполнения: {time_sort:.8f} секунд")
    logger.info(f'При выборе сортировки {type_sort} с направлением {order}, '
                f'сортировка {n} элементов заняла {time_sort:.8f} секунд')


if __name__ == "__main__":
    logger.info('Начало выполнения программы')
    print("Сортировки. Захарова Милана")
    main()
    try:
        # Поломка для демонстрации логирования исключений
        t = 10/0
    except ZeroDivisionError:
        logger.exception('Ошибка деления на 0!!!')
    logger.info('Программа завершена')
