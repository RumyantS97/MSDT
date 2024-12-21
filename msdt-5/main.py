import os

def find_largest_number_less_or_equal(array, n):
    """
    Находит наибольшее целое число в массиве, которое меньше или равно n.
    :param array: Список целых чисел.
    :param n: Целое число для сравнения.
    :return: Наибольшее целое число <= n или None, если такого числа нет.
    """
    filtered_numbers = [x for x in array if x <= n]
    return max(filtered_numbers, default=None)

def read_input_from_file(file_path):
    """
    Читает массив и n из файла.
    :param file_path: Путь к входному файлу.
    :return: Кортеж, содержащий массив и n.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            array = list(map(int, lines[0].strip().split()))
            n = int(lines[1].strip())
            return array, n
    except (IndexError, ValueError):
        raise ValueError("Неверный формат файла. Убедитесь, что первая строка содержит целые числа, а вторая строка - целое число.")

def write_output_to_file(file_path, result):
    """
    Записывает результат в файл.
    :param file_path: Путь к выходному файлу.
    :param result: Результат для записи.
    """
    with open(file_path, 'w') as file:
        file.write(f"Наибольшее число <= n: {result}" if result is not None else "Подходящее число не найдено.")

def main():
    print("Добро пожаловать в программу поиска наибольшего числа!")

    while True:
        try:
            choice = input("Выберите способ ввода данных: (1) С клавиатуры (2) Из файла: ").strip()

            if choice == '1':
                array = list(map(int, input("Введите массив (целые числа через пробел): ").strip().split()))
                n = int(input("Введите значение n: ").strip())
            elif choice == '2':
                file_path = input("Введите путь к входному файлу: ").strip()
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Указанный файл не существует.")
                array, n = read_input_from_file(file_path)
            else:
                print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
                continue

            if len(array) > 100000:
                raise ValueError("Размер массива превышает допустимый предел в 100 000 элементов.")

            result = find_largest_number_less_or_equal(array, n)
            if result is not None:
                print(f"Наибольшее число <= {n}: {result}")
            else:
                print("Подходящее число не найдено.")

            output_choice = input("Хотите сохранить результат в файл? (Y/N): ").strip().lower()
            if output_choice == 'y':
                output_path = input("Введите путь к выходному файлу: ").strip()
                write_output_to_file(output_path, result)
                print(f"Результат сохранен в файл: {output_path}.")

        except ValueError as ve:
            print(f"Ошибка: {ve}")
        except FileNotFoundError as fnfe:
            print(f"Ошибка: {fnfe}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

        continue_choice = input("Хотите продолжить? (Y/N): ").strip().lower()
        if continue_choice != 'y':
            print("Выход из программы. До свидания!")
            break

if __name__ == "__main__":
    main()
