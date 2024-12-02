class DivisionResult:
    def __init__(self, q, r):
        self.q = q
        self.r = r


# Проверка корректности введённого пункта меню
def read_menu(input_str):
    input_str = input_str.strip()
    if (input_str != "1" and input_str != "2"):
        raise ValueError("Ошибка: Введён неверный пункт меню.")
    return input_str


# Проверка корректности введённого целого числа
def parse_integer(input_str):
    input_str = input_str.strip()
    if not input_str or not input_str.lstrip("-").isdigit():
        raise ValueError(
            "Ошибка: Введённая строка не является целым числом."
        )
    return int(input_str)


# Деление
def divide(x, y):

    if (x == 0):
        q = 0
        r = 0

    elif (x > 0 and y > 0):
        q = x // y
        r = x % y

    elif (x > 0 and y < 0):
        q = -(x // abs(y))
        r = x % abs(y)

    elif x < 0 and y > 0:
        q = -(abs(x) // abs(y)) - 1
        r = x - y * q

    else:  # x < 0 and y < 0
        q = (abs(x) // abs(y)) + 1
        r = x - y * q

    return DivisionResult(q, r)

def main():
    menu_string = (
        "Выберите пункт меню:\n"
        "1 – ввести числа и посчитать остаток от деления;\n"
        "2 – завершить работу;\n"
        "Введите пункт меню: "
    )

    while True:

        while True:
            print(menu_string, end='')
            try:
                menu_option = read_menu(input())
                break
            except ValueError as e:
                print(e)

        if menu_option == "2":
            print("Завершение работы...")
            break

        elif menu_option == "1":

            while True:
                try:
                    x = parse_integer(
                        input("Введите целое значение делимого x: ")
                    )
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    y = parse_integer(
                        input("Введите целое значение делителя y: ")
                    )
                    if y == 0:
                        raise ZeroDivisionError(
                            "Делитель не может быть равен 0!"
                        )
                    break
                except (ValueError, ZeroDivisionError) as e:
                    print(str(e))

            result = divide(x, y)
            print(f"Значение x = {x}")
            print(f"Значение y = {y}")
            print(f"Частное от деления q = {result.q}")
            print(f"Остаток от деления r = {result.r}")

if __name__ == "__main__":
    main()