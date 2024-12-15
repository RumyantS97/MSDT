from Vectors import Vectors

def main():
    vect1 = None
    vect2 = None
    flag = True

    while flag:
        try:
            size = int(input("Введите размерность первого вектора: "))
            vect1 = Vectors(size)
            print("Введите элементы вектора:")
            for i in range(vect1.length()):
                vect1.set_elements(i, float(input(f"a[{i}] = ")))

            size = int(input("Введите размерность второго вектора: "))
            vect2 = Vectors(size)
            print("Введите элементы вектора:")
            for i in range(vect2.length()):
                vect2.set_elements(i, float(input(f"a[{i}] = ")))

            flag = False
        except ValueError as ex:
            print("Ошибка: ", ex)

    while True:
        print("\n\t0 - Закончить работу")
        print("\t1 - Вывод информации о векторах")
        print("\t2 - Получение длины векторов")
        print("\t3 - Поиск минимального значения из элементов первого вектора")
        print("\t4 - Поиск максимального значения из элементов первого вектора")
        print("\t5 - Сортировка по возрастанию первого вектора")
        print("\t6 - Сортировка по убыванию первого вектора")
        print("\t7 - Нахождение Евклидовой длины первого вектора")
        print("\t8 - Умножение первого вектора на число")
        print("\t9 - Сложение первого и второго векторов")
        print("\t10 - Скалярное произведение первого и второго векторов")

        choice = input("Ваш выбор: ")

        if choice == "0":
            print("Завершение работы!")
            break

        elif choice == "1":
            print("Первый вектор: ", vect1)
            print("Второй вектор: ", vect2)

        elif choice == "2":
            print("Длина первого вектора: ", vect1.length())
            print("Длина второго вектора: ", vect2.length())

        elif choice == "3":
            print("Минимальный элемент: ", vect1.search_min())

        elif choice == "4":
            print("Максимальный элемент: ", vect1.search_max())

        elif choice == "5":
            print("Производится сортировка по возрастанию...")
            vect1.ascending_sort()
            print("Результат: ", vect1)

        elif choice == "6":
            print("Производится сортировка по убыванию...")
            vect1.descending_sort()
            print("Результат: ", vect1)

        elif choice == "7":
            print("Евклидова длина первого вектора: ", vect1.norm_vector())

        elif choice == "8":
            try:
                num = float(input("Введите число для умножения: "))
                print("Результат: ", vect1.multi_number(num))
            except ValueError as ex:
                print("Ошибка: ", ex)

        elif choice == "9":
            try:
                print("Производится сложение первого и второго векторов...")
                print("Результат: ", Vectors.adding_vectors(vect1, vect2))
            except ValueError as ex:
                print("Ошибка: ", ex)

        elif choice == "10":
            try:
                print("Производится скалярное произведение первого и второго векторов...")
                print("Результат: ", Vectors.scalar_vectors(vect1, vect2))
            except ValueError as ex:
                print("Ошибка: ", ex)

        else:
            print("Некорректный выбор! Такого пункта нет в меню!")


main()