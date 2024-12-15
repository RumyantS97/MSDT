import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("horizontal_data_cleaning.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Путь к исходному файлу
input_file = "users.json"

# Путь к файлу с очищенными данными
output_file = "basic_data.json"

# Функция для преобразования даты рождения в формат "YYYY-MM-DD"
def parse_bdate(bdate):
    try:
        if len(bdate.split('.')) == 3:
            return datetime.strptime(bdate, "%d.%m.%Y").strftime("%Y-%m-%d")
        elif len(bdate.split('.')) == 2:
            # Если год отсутствует, пропускаем
            return None
    except (ValueError, AttributeError) as e:
        return None

# Загрузка данных из файла
logging.info(f"Загрузка данных из файла {input_file}")
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Формирование списка с очищенными данными
cleaned_data = []

for user in data:
    # Извлекаем нужные атрибуты
    user_id = user.get("_id")  # Идентификатор пользователя
    sex = user.get("sex")
    status = user.get("status", None)  # Могут быть пустыми
    bdate = parse_bdate(user.get("bdate", None))  # Преобразуем дату
    faculty_name = None

    # Проверяем наличие факультета
    if "universities" in user and user["universities"]:
        faculty_name = user["universities"][0].get("faculty_name", None)

    # Добавляем в список результат
    cleaned_data.append({
        "id": user_id,
        "sex": sex,
        "status": status,
        "bdate": bdate,
        "faculty_name": faculty_name
    })

logging.info(f"Обработано записей: {len(cleaned_data)}")
logging.info(f"Сохранение данных в файл {output_file}")
# Сохранение очищенных данных в новый файл
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

logging.info("Данные успешно сохранены.")
