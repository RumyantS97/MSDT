import sys

def seconds_to_dhms(seconds):
    # Проверка, что входное значение - целое число и неотрицательное
    if not isinstance(seconds, int):
        raise ValueError("Ввод должен быть положительным целым числом.")
    if seconds < 0:
        raise ValueError("Ввод должен быть положительным целым числом.")

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"

def handle_custom_separator(input_str, separator):
    try:
        seconds_values = input_str.split(separator)
        results = [seconds_to_dhms(int(seconds.strip())) for seconds in seconds_values]
        return "; ".join(results)
    except ValueError:
        return "Ошибка: введите положительное целое число секунд"

def main():
    # Проверяем, был ли указан аргумент командной строки
    if len(sys.argv) < 2:
        print("Использование: python seconds_to_time.py [количество_секунд]")
        return

    # Проверяем, есть ли кастомный разделитель (например ";")
    input_value = sys.argv[1]
    if ";" in input_value:
        result = handle_custom_separator(input_value, ";")
        print(f"Результат: {result}")
        return

    # Пытаемся преобразовать аргумент в целое число
    try:
        seconds = int(input_value)
        if seconds < 0:
            raise ValueError("Ввод должен быть положительным целым числом.")
    except ValueError as e:
        print(f"Ошибка: введите положительное целое число секунд")
        return

    # Выполняем конвертацию секунд в формат dd:hh:mm:ss
    result = seconds_to_dhms(seconds)
    print(f"Результат: {result}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")

# cd C:\Users\User\PycharmProjects\secondsToTime
# python seconds_to_time.py 67890
