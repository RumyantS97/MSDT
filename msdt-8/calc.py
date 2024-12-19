from operations_enum import OperationsEnum


def calculator():

    while True:
        print(OperationsEnum.get_message_for_input())
        choice = input("Введите номер операции: ")
        if choice in OperationsEnum.get_codes():
            operation = OperationsEnum.get_item_by_code(choice)
            if operation.operand_count == 2:
                try:
                    num1 = float(input("Введите первое число: "))
                    num2 = float(input("Введите второе число: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue
                print(f'{operation.description} для чисел {num1} и {num2} = {operation.func(num1, num2)}')
            elif operation.operand_count == 1:
                try:
                    num = float(input("Введите число: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue
                print(f'{operation.description} числа {num} = {operation.func(num)}')
        else:
            print("Некорректный ввод. Пожалуйста, выбирайте номер операции из списка.")

        next_calculation = input("Хотите выполнить еще одно вычисление? (да/any key): ")
        if next_calculation.lower() != 'да':
            break


if __name__ == "__main__":
    calculator()
