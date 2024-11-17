import csv
import logging
from collections import defaultdict


# Настройка логирования
logging.basicConfig(
    filename='data_processor.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def load_csv(file_path):
    # Загрузка данных из CSV-файла
    logging.info(f"Загрузка CSV из {file_path}")
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        logging.debug(f"Загружено {len(data)} строк из {file_path}")
        return data
    except Exception as e:
        logging.error(f"Ошибка загрузки CSV: {e}")
        raise


def load_multiple_csv(file_paths):
    # Загрузка и объединение данных из нескольких csv файлов
    logging.info(f"Загрузка и объединение данных из файлов: {file_paths}")
    combined_data = []
    for file_path in file_paths:
        try:
            data = load_csv(file_path)
            combined_data.extend(data)
            logging.debug(f"Добавлено {len(data)} строк из файла {file_path}")
        except Exception as e:
            logging.warning(f"Ошибка при обработке файла: {file_path}: {e}")
    logging.debug(f"Общий объем данных после объединения: {len(combined_data)} строк")
    return combined_data


def group_by_column(data, column):
    # Группировка данных по указанной колонке
    logging.info(f"Группировка данных по колонке '{column}'")
    grouped_data = defaultdict(list)
    try:
        for row in data:
            grouped_data[row[column]].append(row)
        logging.debug(f"Создано {len(grouped_data)} групп")
        return grouped_data
    except Exception:
        logging.error(f"Указанной колонки '{column}' нет в данных")
        raise


def filter_groups(grouped_data, min_size):
    # Фильтрация групп по минимальному размеру
    logging.info(f"Фильтрация групп с размером меньше {min_size}")
    filtered = {key: value for key,
                value in grouped_data.items() if len(value) >= min_size}
    logging.debug(f"Осталось {len(filtered)} групп после фильтрации")
    return filtered


def sort_groups_by_size(grouped_data):
    # Сортировка групп по количеству записей в каждой
    logging.info(f"Сортировка групп по размеру")
    sorted_data = sorted(grouped_data.items(),
                         key=lambda x: len(x[1]),
                         reverse=True)
    logging.debug(f"Группы отсортированы. Первая группа содержит {len(sorted_data[0][1])} записей")
    return sorted_data


def save_to_csv(data, output_path):
    # Сохранение данных в csv файл
    logging.info(f"Сохранение данных в файл {output_path}")
    try:
        # Разворачиваем данные обратно в список словарей
        flattened_data = [item for _, group in data for item in group]
        keys = flattened_data[0].keys()
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(flattened_data)
        logging.debug(f"Успешно сохранено {len(flattened_data)} строк в {output_path}")
    except Exception as e:
        logging.error(f"Ошибка сохранения данных: {e}")
        raise


def main():
    # Ввод данных
    logging.info(f"Запуск программы обработки CSV")
    input_files = input("Введите пути к входным CSV-файлам: ").strip()
    output_file = input("Введите путь к выходному CSV-файлу: ").strip()
    group_by = input("Введите колонку для группировки: ").strip()
    filter_size = input("Введите мин. размер группы для фильтрации: ").strip()

    file_list = input_files.split(",")
    # Преобразуем введенное значение в число
    filter_size = int(filter_size) if filter_size else None

    try:
        if len(file_list) > 1:
            data = load_multiple_csv(file_list)
        else:
            data = load_csv(input_files)
        grouped = group_by_column(data, group_by)
        if filter_size:
            grouped = filter_groups(grouped, filter_size)
        sorted_groups = sort_groups_by_size(grouped)
        save_to_csv(sorted_groups, output_file)

        logging.info("Программа успешно завершена")
    except Exception as e:
        logging.error(f"Ошибка выполнения программы: {e}")
        exit(1)


if __name__ == "__main__":
    main()
