import math


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Ошибка: деление на ноль!"
    return x / y


def power(x, y):
    return x ** y


def sin(x):
    return math.sin(math.radians(x))  # Преобразуем градусы в радианы


def cos(x):
    return math.cos(math.radians(x))  # Преобразуем градусы в радианы


def tan(x):
    return math.tan(math.radians(x))  # Преобразуем градусы в радианы


def calculator():
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Возведение в степень")
    print("6. Синус")
    print("7. Косинус")
    print("8. Тангенс")

    while True:
        choice = input("Введите номер операции (1/2/3/4/5/6/7/8): ")
        num1 = num2 = 0
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            if choice in ['1', '2', '3', '4', '5']:
                try:
                    num1 = float(input("Введите первое число: "))
                    num2 = float(input("Введите второе число: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            elif choice == '5':
                print(f"{num1} ^ {num2} = {power(num1, num2)}")
            elif choice in ['6', '7', '8']:
                try:
                    angle = float(input("Введите угол в градусах: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue

                if choice == '6':
                    print(f"sin({angle}) = {sin(angle)}")
                elif choice == '7':
                    print(f"cos({angle}) = {cos(angle)}")
                elif choice == '8':
                    print(f"tan({angle}) = {tan(angle)}")

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер операции от 1 до 8.")

        next_calculation = input("Хотите выполнить еще одно вычисление? (да/нет): ")
        if next_calculation.lower() != 'да':
            break


if __name__ == "__main__":
    calculator()
