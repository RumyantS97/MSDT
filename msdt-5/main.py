def kmh_to_mps(speed_kmh):
    # Перевод из км/ч в м/с
    return speed_kmh * (1000 / 3600)


def main():
    while True:
        print("\nМеню:")
        print("1. Ввести число и перевести его в м/с")
        print("2. Завершить работу")

        choice = input("Выберите опцию (1 или 2): ")

        if choice == '1':
            try:
                # Запрос ввода скорости в км/ч
                speed_kmh = float(input("Введите скорость в км/ч (положительное число): "))

                # Проверка, что число положительное
                if speed_kmh <= 0:
                    print("Ошибка: Скорость должна быть положительным числом.")
                    continue

                # Перевод в м/с
                speed_mps = kmh_to_mps(speed_kmh)
                print(f"{speed_kmh} км/ч = {speed_mps:.2f} м/с")

            except ValueError:
                # Обработка ошибки, если ввод не является числом
                print("Ошибка: Введите корректное числовое значение.")

        elif choice == '2':
            print("Завершение работы программы.")
            break

        else:
            print("Ошибка: Введите 1 или 2 для выбора опции.")


if __name__ == "__main__":
    main()