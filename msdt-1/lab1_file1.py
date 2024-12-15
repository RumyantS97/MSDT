import random
import heapq
from collections import Counter

# Константы для сортировок
START_INDEX = 0
END_INDEX = -1
FIRST_ELEMENT = 0
SECOND_ELEMENT = 1
THIRD_ELEMENT = 2

# Общая функция для сортировки
def sort_array(array, algorithm):
    return algorithm(array)

# Функции сортировки
def sort_by_bubble(array_to_sort):
    array_length = len(array_to_sort)
    for i in range(array_length):
        for j in range(START_INDEX, array_length - i - 1):
            if array_to_sort[j] > array_to_sort[j + 1]:
                array_to_sort[j], array_to_sort[j + 1] = array_to_sort[j + 1], array_to_sort[j]
    return array_to_sort

def sort_by_cocktail_shaker(array_to_sort):
    array_length = len(array_to_sort)
    start = START_INDEX
    end = array_length - 1
    while start <= end:
        swapped = False
        for i in range(start, end):
            if array_to_sort[i] > array_to_sort[i + 1]:
                array_to_sort[i], array_to_sort[i + 1] = array_to_sort[i + 1], array_to_sort[i]
                swapped = True
        end -= 1
        for i in range(end, start, -1):
            if array_to_sort[i] < array_to_sort[i - 1]:
                array_to_sort[i], array_to_sort[i - 1] = array_to_sort[i - 1], array_to_sort[i]
                swapped = True
        start += 1
        if not swapped:
            break
    return array_to_sort

def sort_by_insertion(array_to_sort):
    for i in range(1, len(array_to_sort)):
        key = array_to_sort[i]
        j = i - 1
        while j >= START_INDEX and key < array_to_sort[j]:
            array_to_sort[j + 1] = array_to_sort[j]
            j -= 1
        array_to_sort[j + 1] = key
    return array_to_sort

def sort_by_quick(array_to_sort):
    if len(array_to_sort) <= 1:
        return array_to_sort
    pivot = array_to_sort[len(array_to_sort) // 2]
    left = [x for x in array_to_sort if x < pivot]
    middle = [x for x in array_to_sort if x == pivot]
    right = [x for x in array_to_sort if x > pivot]
    return sort_by_quick(left) + middle + sort_by_quick(right)

def sort_by_heap(array_to_sort):
    def adjust_heap(array_to_sort, array_length, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < array_length and array_to_sort[left] > array_to_sort[largest]:
            largest = left
        if right < array_length and array_to_sort[right] > array_to_sort[largest]:
            largest = right
        if largest != i:
            array_to_sort[i], array_to_sort[largest] = array_to_sort[largest], array_to_sort[i]
            adjust_heap(array_to_sort, array_length, largest)

    array_length = len(array_to_sort)
    for i in range(array_length // 2 - 1, START_INDEX - 1, -1):
        adjust_heap(array_to_sort, array_length, i)
    for i in range(array_length - 1, 0, -1):
        array_to_sort[i], array_to_sort[0] = array_to_sort[0], array_to_sort[i]
        adjust_heap(array_to_sort, i, 0)
    return array_to_sort

def sort_by_buckets(array_to_sort):
    if len(array_to_sort) == 0:
        return array_to_sort
    bucket_count = len(array_to_sort)
    max_val = max(array_to_sort)
    min_val = min(array_to_sort)
    bucket_size = (max_val - min_val) / bucket_count
    buckets = [[] for _ in range(bucket_count)]

    for num in array_to_sort:
        index = int((num - min_val) / bucket_size)
        if index == bucket_count:
            index -= 1
        buckets[index].append(num)

    for bucket in buckets:
        sort_by_insertion(bucket)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    return sorted_arr

# Функция выбора сортировки через словарь
def choose_sort_algorithm(choice):
    sorting_algorithms = {
        '1': sort_by_bubble,
        '2': sort_by_cocktail_shaker,
        '3': sort_by_insertion,
        '4': sort_by_quick,
        '5': sort_by_heap,
        '6': sort_by_buckets
    }
    return sorting_algorithms.get(choice, None)

# Главная функция
def main():
    size = int(input("Введите размер массива: "))
    array = [random.randint(0, 100) for _ in range(size)]
    print("Сгенерированный массив:", array)
    print("\nВыберите алгоритм сортировки:")
    print("1. Пузырьковая сортировка")
    print("2. Сортировка перемешиванием")
    print("3. Сортировка вставками")
    print("4. Быстрая сортировка")
    print("5. Пирамидальная сортировка")
    print("6. Блочная сортировка")
    choice = input("Ваш выбор: ")

    sort_algorithm = choose_sort_algorithm(choice)
    if sort_algorithm:
        print(f"\nСортируем выбранным алгоритмом ({choice})...")
        sorted_array = sort_array(array, sort_algorithm)
        print("Отсортированный массив:", sorted_array)
    else:
        print("Неверный выбор! Программа завершена.")

if __name__ == "__main__":
    main()
