import json
import logging

# Пути к файлам
input_file = "basic_data.json"
output_file = "cleared_data.json"

# Загрузка данных из файла
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Фильтрация пользователей
filtered_data = [
    user for user in data
    if user.get("status") not in (None, "")  # Исключаем записи со статусом null или пустой строкой
]

# Подсчёт статистики
initial_count = len(data)
filtered_count = len(filtered_data)
removed_count = initial_count - filtered_count

# Сохранение очищенных данных в новый файл
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

