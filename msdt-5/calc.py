from operations_enum import OperationsEnum
from log_settings import logger


def calculator():
    logger.debug(f'Вызвана функция calculator')
    logger.info(f'Основной программный модуль запущен')
    count = success_count = 0
    while True:
        count += 1
        print(OperationsEnum.get_message_for_input())
        choice = input("Введите номер операции: ")
        if choice in OperationsEnum.get_codes():
            operation = OperationsEnum.get_item_by_code(choice)
            logger.info(f'Пользователь выбрал выполнять операцию '
                        f'{operation.description}')
            if operation.operand_count == 2:
                try:
                    num1 = float(input("Введите первое число: "))
                    num2 = float(input("Введите второе число: "))
                except ValueError:
                    logger.warning(f'Пользователь вводит не число')
                    print("Ошибка: введите числовое значение.")
                    continue
                success_count += 1
                logger.debug(f'Пользователь ввел числа {num1} и {num2}')
                print(f'{operation.description} для чисел '
                      f'{num1} и {num2} = {operation.func(num1, num2)}')
            elif operation.operand_count == 1:
                try:
                    num = float(input("Введите число: "))
                except ValueError:
                    logger.warning(f'Пользователь вводит не число')
                    print("Ошибка: введите числовое значение.")
                    continue
                success_count += 1
                logger.debug(f'Пользователь ввел число {num}')
                print(f'{operation.description} числа '
                      f'{num} = {operation.func(num)}')
        else:
            logger.warning(f'Пользователь ввел неизвестный код операции')
            print("Некорректный ввод. Выбирайте номер операции из списка.")

        next_calculation = \
            input("Хотите выполнить еще одно вычисление? (да/any key): ")
        if next_calculation.lower() != 'да':
            logger.debug(f'Пользователь отказался калькулировать(')
            break
        logger.debug(f'Пользователь согласился калькулировать дальше)')

    logger.info(f'Пользователь выполнил {count} попыток выполнить операцию')
    logger.info(f'Попыток когда произошел валидный ввод: {success_count}')


if __name__ == "__main__":
    logger.info("Программа запущена")
    calculator()
    logger.info("Программа успешно завершена")
