import random
import time
from logging_config import logger
from sortings import bubble_sort, cocktail_sort, insertion_sort, \
    gnome_sort, selection_sort, comb_sort, quicksort

dict_sorting = {
    1: ["Сортировка пузырьком", bubble_sort],
    2: ["Сортировка перемешиванием", cocktail_sort],
    3: ["Сортировка вставками", insertion_sort],
    4: ["Гномья сортировка", gnome_sort],
    5: ["Сортировка выбором", selection_sort],
    6: ["Сортировка расческой", comb_sort],
    7: ["Быстрая сортировка ", quicksort]
}

dict_order = {
    1: ["По возрастанию", True],
    2: ["По убыванию", False]
}


def input_value_in_bounds(left, right, message):
    logger.debug('Произошел вызов функции "input_value_in_bounds"')
    is_selected = False
    temp = 0
    while not is_selected:
        print(message)
        temp = 0
        try:
            temp = int(input(f"Введите число от "
                             f"{left} до {right}: "))
            if temp < left or temp > right:
                logger.warning(f'Пользователь ввел "{temp}", '
                               f'ожидалось число от {left} до {right}')
                raise ValueError("Некорректный ввод.")
        except ValueError:
            if temp == 0:
                logger.warning('Пользователь ввел не число, '
                               f'ожидалось число от {left} до {right}')
            print("Некорректный ввод. Пожалуйста, попробуйте снова.\n")
            continue
        is_selected = True
    return temp


def build_input_message(dict_, predict_message):
    logger.debug('Произошел вызов функции "build_input_message"')
    message = predict_message + "\n\n"
    for i in dict_.keys():
        message += f'Чтобы выбрать "{dict_.get(i)[0]}" - нажмите {i}\n'
    return message


def select_type_sort():
    logger.debug('Произошел вызов функции "select_type_sort"')

    type_message = build_input_message(dict_sorting, "Выберите сортировку:")
    order_message = build_input_message(dict_order,
                                        "Выберите направление сортировки:")

    type_sort_digit = input_value_in_bounds(1, 7, type_message)
    logger.debug(f'Пользователь выбрал тип сортировки '
                 f'{dict_sorting.get(type_sort_digit)[0]}')
    order_digit = input_value_in_bounds(1, 2, order_message)
    logger.debug(f'Пользователь выбрал направление сортировки '
                 f'{dict_order.get(order_digit)[0]}')
    return dict_sorting.get(type_sort_digit), dict_order.get(order_digit)


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
    logger.info(f'Пользователь выбрал тип сортировки: {type_sort}, '
                f'направление сортировки: {order}')
    n = 10
    source_arr = [random.randint(0, 100) for _ in range(n)]

    print(f'Тип: "{type_sort[0]}". Направление: "{order[0]}"')
    start_time = time.time()
    result_arr = type_sort[1](source_arr, order[1])
    end_time = time.time()

    print("Исходный массив:")
    display_array(source_arr)

    print("Результат:")
    display_array(result_arr)

    time_sort = end_time - start_time
    print(f"Время выполнения: {time_sort:.8f} секунд")
    logger.info(f'При выборе сортировки "{type_sort[0]}" '
                f'с направлением "{order[0]}", '
                f'сортировка {n} элементов заняла {time_sort:.8f} секунд')


if __name__ == "__main__":
    logger.info('Начало выполнения программы')
    print("Сортировки. Захарова Милана")
    main()
    logger.info('Программа завершена')
