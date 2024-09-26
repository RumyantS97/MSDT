import random
import time


def shaker_sort(array):
    swapped = True  # Был ли обмен элементами
    start_index = 0
    end_index = len(array) - 1

    while swapped:
        swapped = False
        for i in range(start_index, end_index):  # Проход слева направо
            if array[i] > array[i + 1]:  # Меняем элементы, если следующий меньше
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True

        if not swapped:
            break  # Если не было обменов, прерываем цикл, массив отсортирован

        swapped = False
        end_index -= 1  # Последний элемент уже на месте
        for i in range(end_index - 1, start_index - 1, -1):  # Проход справа налево
            if array[i] > array[i + 1]:  # Меняем элементы, если следующий меньше
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        start_index += 1


def quicksort(array, left, right):
    if left < right:
        x = partition(array, left, right)
        quicksort(array, left, x - 1)
        quicksort(array, x + 1, right)


def partition(array, left, right):
    random_index = random.randint(left, right)
    random_element = array[random_index]  # Запоминаем выбранный опорный элемент

    array[random_index], array[right] = array[right], array[random_index]  # Помещаем его в конец массива

    j = left  # Элемент для разделения массива

    for i in range(left, right):
        if array[i] < random_element:
            array[i], array[j] = array[j], array[i]
            j += 1

    array[j], array[right] = array[right], array[j]

    return j


def main():
    print("\nПрактическая работа №1. Алгоритмы сортировки.\nВыполнила: Купцова Таисия, группа 6203-020302D\nВариант "
          "3. Шейкер-сортировка и быстрая сортировка (quicksort).")

    s_times = []
    q_times = []

    for size in range(6):
        N = random.randint(1000, 19600)
        array = [random.randint(-10, 10) for _ in range(N)]

        print("\nРазмер " + str(size + 1) + "-го массива N = " + str(N))

        arr1 = array.copy()
        print("\n... Выполнение шейкер-сортировки ...")
        start_time = time.time()
        shaker_sort(arr1)

        end_time = time.time()
        time_s = end_time - start_time
        print("Время шейкер-сортировки:", time_s, "сек")
        s_times.append(time_s)

        arr2 = array.copy()
        print("\n... Выполнение быстрой сортировки ...")
        start_time = time.time()
        quicksort(arr2, 0, len(arr2) - 1)
        end_time = time.time()
        time_q = end_time - start_time
        print("Время быстрой сортировки:", time_q, "сек")
        q_times.append(time_q)

    average_q_time = sum(q_times) / 6
    average_s_time = sum(s_times) / 6

    print("\n")
    print("|{:<20}|{:<20}|{:<20}".format("Сортировка", "Среднее время (сек)", "Время (сек)"))
    print("|{:<20}|{:<20}|{:<20}|".format("Шейкер-сортировка", average_s_time, ', '.join(map(str, s_times))))
    print("|{:<20}|{:<20}|{:<20}|".format("Быстрая сортировка", average_q_time, ', '.join(map(str, q_times))))
    print("\n")


main()