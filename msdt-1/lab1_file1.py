import random

# Пузырьковая сортировка
def sort_by_bubble(array_to_sort):
    array_length = len(array_to_sort)
    for i in range(array_length):
        for j in range(0, array_length - i - 1):
            if array_to_sort[j] > array_to_sort[j + 1]:
                array_to_sort[j], array_to_sort[j + 1] = array_to_sort[j + 1], array_to_sort[j]
    return array_to_sort

# Сортировка перемешиванием
def sort_by_cocktail_shaker(array_to_sort):
    array_length = len(array_to_sort)
    start = 0
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

# Сортировка вставками
def sort_by_insertion(array_to_sort):
    for i in range(1, len(array_to_sort)):
        key = array_to_sort[i]
        j = i - 1
        while j >= 0 and key < array_to_sort[j]:
            array_to_sort[j + 1] = array_to_sort[j]
            j -= 1
        array_to_sort[j + 1] = key
    return array_to_sort

# Быстрая сортировка
def sort_by_quick(array_to_sort):
    if len(array_to_sort) <= 1:
        return array_to_sort
    pivot = array_to_sort[len(array_to_sort) // 2]
    left = [x for x in array_to_sort if x < pivot]
    middle = [x for x in array_to_sort if x == pivot]
    right = [x for x in array_to_sort if x > pivot]
    return sort_by_quick(left) + middle + sort_by_quick(right)

# Пирамидальная сортировка (Heap Sort)
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

def sort_by_heap(array_to_sort):
    array_length = len(array_to_sort)
    for i in range(array_length // 2 - 1, -1, -1):
        adjust_heap(array_to_sort, array_length, i)
    for i in range(array_length - 1, 0, -1):
        array_to_sort[i], array_to_sort[0] = array_to_sort[0], array_to_sort[i]
        adjust_heap(array_to_sort, i, 0)
    return array_to_sort

# Блочная сортировка (Bucket Sort)
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

    if choice == '1':
        print("\nСортируем пузырьковой сортировкой...")
        sorted_array = sort_by_bubble(array)
    elif choice == '2':
        print("\nСортируем сортировкой перемешиванием...")
        sorted_array = sort_by_cocktail_shaker(array)
    elif choice == '3':
        print("\nСортируем сортировкой вставками...")
        sorted_array = sort_by_insertion(array)
    elif choice == '4':
        print("\nСортируем быстрой сортировкой...")
        sorted_array = sort_by_quick(array)
    elif choice == '5':
        print("\nСортируем пирамидальной сортировкой...")
        sorted_array = sort_by_heap(array)
    elif choice == '6':
        print("\nСортируем блочной сортировкой...")
        sorted_array = sort_by_buckets(array)
    else:
        print("Неверный выбор! Программа завершена.")
        return
    print("Отсортированный массив:", sorted_array)

if __name__ == "__main__":
    main()