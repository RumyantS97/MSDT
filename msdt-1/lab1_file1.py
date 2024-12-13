import random

# Пузырьковая сортировка
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Сортировка перемешиванием
def cocktail_shaker_sort(arr):
    n=len(arr)
    start = 0
    end = n - 1
    while start <= end:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        end -= 1
        for i in range(end, start, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True
        start += 1
        if not swapped:
            break
    return arr

# Сортировка вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Быстрая сортировка
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Пирамидальная сортировка (Heap Sort)
def heapify(arr,n,i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

# Блочная сортировка (Bucket Sort)
def bucket_sort(arr):
    if len(arr) == 0:
        return arr
    bucket_count = len(arr)
    max_val = max(arr)
    min_val = min(arr)
    bucket_size = (max_val - min_val) / bucket_count
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = int((num - min_val) / bucket_size)
        if index == bucket_count:
            index -= 1
        buckets[index].append(num)

    for bucket in buckets:
        insertion_sort(bucket)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    return sorted_arr

def main():
    size = int(input("Введите размер массива: "))
    array = [ random.randint(0, 100) for _ in range(size)]
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
        sorted_array = bubble_sort(array)
    elif choice == '2':
        print("\nСортируем сортировкой перемешиванием...")
        sorted_array = cocktail_shaker_sort(array)
    elif choice == '3':
        print("\nСортируем сортировкой вставками...")
        sorted_array = insertion_sort(array)
    elif choice == '4':
        print("\nСортируем быстрой сортировкой...")
        sorted_array = quick_sort(array)
    elif choice == '5':
        print("\nСортируем пирамидальной сортировкой...")
        sorted_array = heap_sort(array)
    elif choice == '6':
        print("\nСортируем блочной сортировкой...")
        sorted_array = bucket_sort(array)
    else:
        print("Неверный выбор! Программа завершена.")
        return
    print("Отсортированный массив:", sorted_array)

if __name__ == "__main__":
    main()