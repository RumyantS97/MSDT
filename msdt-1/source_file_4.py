import math

flag = True
while flag:
    print("\nПривет! Выбери пункт(введи цифру) из меню для продолжения работы:")
    print("\t1 - Задание №1. Таблица значений функции.")
    print("\t2 - Задание №2. Серия выстрелов по мишени.")
    print("\t3 - Задание №3. Сумма ряда.")
    print("\t0 - Завершение работы программы.")
    symbol = input("\nВаш выбор: ")

    if symbol == "1":
        print("\nПрограмма для вычисления значений функции f(x), где x от -7 до 3, " +
              "на интервале от x_min дo x_max с шагом dx.")
        print("Привет! Введите значения минимального X, максимального X и шага dx:\n")

        x_min = float(input("x_min = "))
        x_max = float(input("x_max = "))
        dx = float(input("dx = "))
        print()

        if x_min > x_max:
            print("Ошибка границ интервала, введите корректные x_min и x_max!")
        else:
            print("Значение переменной X\tЗначение функции f(X)")
            i = x_min
            while i <= x_max:
                if i < -7.0 or i > 3.0:
                    print(f"{i:10.3f}\t{'НЕ определено':>25}")
                else:
                    if i <= -6.0:
                        fx = 2
                    elif i <= -2.0:
                        fx = i / 4 + 0.5
                    elif i <= 0.0:
                        fx = 2 - math.sqrt(4 - math.pow(i + 2, 2))
                    elif i <= 2.0:
                        fx = math.sqrt(4 - math.pow(i, 2))
                    else:
                        fx = -i + 2
                    print(f"{i:10.3f}\t{fx:20.3f}")
                i += dx
        print()

    elif symbol == "2":
        print("\nПрограмма для определения попадания в мишень выстрела с координатами X и Y")
        print("Привет! Введи координаты точек 10-ти выстрелов:\n")

        target = [[0.0, 0.0] for _ in range(10)]

        for i in range(10):
            print()
            target[i][0] = float(input(f"x{i} = "))
            target[i][1] = float(input(f"y{i} = "))

        print("\tКоординаты точки\t\tРезультат выстрела")
        for i in range(10):
            x, y = target[i]
            if y >= math.pow((x - 2), 2) - 3 and (y <= -x or (y <= x and y >= 0)):
                print(f"\t({x:8.2f}; {y:8.2f}) {'Попадание!':>25}")
            else:
                print(f"\t({x:8.2f}; {y:8.2f}) {'Промах!':>22}")
        print()

    elif symbol == "3":
        print("\nПрограмма для вычисления суммы ряда от X с заданной точностью E "
              + "и подсчётом количества членов в ряду.")
        print("Привет! Введи переменную X и заданную точность ряда E:\n")

        x = float(input("x = "))
        e = float(input("e = "))
        sum = math.pi / 2
        presum = sum
        quan = -1

        if x > 1:
            while abs(sum - presum) > e:
                presum = sum
                print(f"\nПресумма: {presum}")
                quan += 1
                print(f"n = {quan}")
                sum += math.pow(-1, quan + 1) / ((2 * quan + 1) * math.pow(x, 2 * quan + 1))
                print(f"Сумма: {sum}\n")

            print(f"\nСумма ряда с заданной точностью e = {e} равна: {sum:0.6f}\n"
                  + f"Количество членов в ряду равно: {quan + 1}")
        else:
            print("\nОшибка! Переменная x должна быть больше 1!")
        print()

    elif symbol == "0":
        print("\nЗавершение работы меню выбора!")
        flag = False

    else:
        print(f"\nВы ввели строку символов \"{symbol}\", возможно, это было случайно, попробуйте снова!")

print("\nПрограмма завершена!")
