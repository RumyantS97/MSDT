from operations_enum import OperationsEnum


def calculator():

    while True:
        print(OperationsEnum.get_message_for_input())
        choice = input("Введите номер операции: ")
        num1 = num2 = 0
        if choice in OperationsEnum.get_codes():
            if choice in ['1', '2', '3', '4', '5']:
                try:
                    num1 = float(input("Введите первое число: "))
                    num2 = float(input("Введите второе число: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue

            if choice == '1':
                print(f"{num1} + {num2} = {OperationsEnum.ADD.func(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {OperationsEnum.SUB.func(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {OperationsEnum.MUL.func(num1, num2)}")
            elif choice == '4':
                result = OperationsEnum.DIV.func(num1, num2)
                print(f"{num1} / {num2} = {result}")
            elif choice == '5':
                print(f"{num1} ^ {num2} = {OperationsEnum.POW.func(num1, num2)}")
            elif choice in ['6', '7', '8']:
                try:
                    angle = float(input("Введите угол в градусах: "))
                except ValueError:
                    print("Ошибка: введите числовое значение.")
                    continue

                if choice == '6':
                    print(f"sin({angle}) = {OperationsEnum.SIN.func(angle)}")
                elif choice == '7':
                    print(f"cos({angle}) = {OperationsEnum.COS.func(angle)}")
                elif choice == '8':
                    print(f"tan({angle}) = {OperationsEnum.TAN.func(angle)}")

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер операции от 1 до 8.")

        next_calculation = input("Хотите выполнить еще одно вычисление? (да/нет): ")
        if next_calculation.lower() != 'да':
            break


if __name__ == "__main__":
    calculator()
