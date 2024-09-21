from random import randint

def hello():
    print('''Лабораторнная работа №2
    Вариант №8. Выполнил студент группы 6103-020302D Красюк А. М.
    Задание:
    1. В списке целочисленных элементов найти максимальный нечётный элемент
    2. С использованием цикла while найти в списке индекс первого двузначного элемента,
       кратного заданному числу
    3. Отсортировать список (без использования стандартных функций сортировки)
       по убыванию старших цифр элементов списка (быстрая сортировка)''')
    print()
    print('''Введите способ заполнения списка:
    1 - ввод элементов списка в одну строку через пробел:
    любое число - автоматическое формирование списка из n элементов:''')

def get_1_den(a):
    a = abs(a)
    while a >= 10:
          a = a // 10
    return a

def makelist():
    choise = int(input())
    if choise == 1:
        user_list = list(map(int, input('Введите в строку элементы списка:\n').split()))
        return user_list
    else:
        length = int(input('Введите количество элементов списка: '))
        bottom, top = map(int, input('Введите диапазон элементов:\n').split())
        user_list = []
        for i in range(length):
            user_list.append(randint(bottom, top))
        print(user_list)
        return user_list

def parameter_search(user_list):
    maximum = -10**10
    for element in range(len(user_list)):
        if user_list[element] > maximum and user_list[element] % 2 != 0:
            maximum = user_list[element]
    return maximum

def index_search(user_list, number):
    i = 0
    while (i < len(user_list)) and ((abs(user_list[i])//10 < 1) or (abs(user_list[i])//10 >= 10) or (user_list[i] % number != 0)):
          i += 1
    if i<len(user_list):
          return i
    else:
          return None

def quicksort(user_list, fst, lst):
    if fst>=lst:
        return
    i, j = fst, lst
    pivot = user_list[randint(fst, lst)]
    pivot = get_1_den(pivot)
    while i <= j:
        while get_1_den(user_list[i]) > pivot:
            i += 1
        while get_1_den(user_list[j]) < pivot:
            j -= 1
        if i <= j:
            user_list[i], user_list[j] = user_list[j], user_list[i]
            i, j = i + 1, j - 1
    quicksort(user_list, fst, j)
    quicksort(user_list, i, lst)

hello()
numbers = makelist()
print()
print('Максимальный нечётный элемент: ' + str(parameter_search(numbers)))
print()
multiplicity = int(input('Введите число, кратность которому нужно проверить: '))
index = index_search(numbers, multiplicity)
if not index == None:
    print('Индекс первого двузначного элемента, кратного заданному числу: ' + str(index))
else:
    print('В списке отсутствуют двузначные элементы, кратные заданному числу')
print()
print('Исходный список\n', numbers)
print()
quicksort(numbers, 0, len(numbers)-1)
print('Список после быстрой сортировки:\n', numbers)