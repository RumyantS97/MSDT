ADD = '1'
SUBTRACT = '2'
MULTIPLY = '3'
DIVIDE = '4'
POWER = '5'
MODULUS = '6'

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    if b == 0:
        return "Ошибка: деление на ноль невозможно."
    return a / b

def raise_to_power(a, b):
    return a ** b

def calculate_modulus(a, b):
    if b == 0:
        return "Ошибка: деление на ноль невозможно."
    return a % b

def run_calculator_program():
    print("Добро пожаловать в ручной калькулятор!")
    print("Выберите операцию:")
    print("1: Сложение (+)")
    print("2: Вычитание (-)")
    print("3: Умножение (*)")
    print("4: Деление (/)")
    print("5: Возведение в степень (**)")
    print("6: Остаток от деления (%)")
    print("Введите 'exit', чтобы выйти.")

    while True:
        choice = input("\nВыберите операцию: ")
        if choice.lower() == 'exit':
            print("Выход из программы. До свидания!")
            break

        if choice not in [ADD, SUBTRACT, MULTIPLY, DIVIDE, POWER, MODULUS]:
            print("Ошибка: некорректный ввод. Попробуйте снова.")
            continue

        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))

            if choice == ADD:
                print(f"Результат: {num1} + {num2} = {add_numbers(num1, num2)}")
            elif choice == SUBTRACT:
                print(f"Результат: {num1} - {num2} = {subtract_numbers(num1, num2)}")
            elif choice == MULTIPLY:
                print(f"Результат: {num1} * {num2} = {multiply_numbers(num1, num2)}")
            elif choice == DIVIDE:
                print(f"Результат: {num1} / {num2} = {divide_numbers(num1, num2)}")
            elif choice == POWER:
                print(f"Результат: {num1} ** {num2} = {raise_to_power(num1, num2)}")
            elif choice == MODULUS:
                print(f"Результат: {num1} % {num2} = {calculate_modulus(num1, num2)}")
        except ValueError:
            print("Ошибка: введите числовые значения.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

# Запуск программы
run_calculator_program()