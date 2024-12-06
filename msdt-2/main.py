import os
import re
import vobject
import quopri
from datetime import date
from dotenv import load_dotenv
from prettytable import PrettyTable

# Загружаем переменные окружения
load_dotenv()
v_card = os.getenv('VCF')

if not os.path.exists(v_card):
    raise FileNotFoundError(f"Файл '{v_card}' не найден.")

# Функция для очистки проблемных строк из файла .vcf
def clean_vcf_file(input_file, output_file):
    """
    Очищает проблемные строки из файла vCard и сохраняет его в новый файл.

    :param input_file: Путь к исходному файлу .vcf
    :param output_file: Путь к очищенному файлу .vcf
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Удаляем строки, которые содержат специфические параметры, вызывающие ошибки при разборе
            if re.search(r'TEL;.*\(CHARSET=UTF-8,ENCODING=QUOTED-PRINTABLE', line):
                # Пропускаем эти строки, чтобы избежать ошибок парсинга
                continue
            outfile.write(line)


# Очищаем исходный файл и сохраняем в новый
cleaned_v_card = 'contacts_cleaned.vcf'
clean_vcf_file(v_card, cleaned_v_card)

# Создаем таблицу для отображения контактов
vcf_table = PrettyTable()
vcf_table.field_names = ['full_name', 'birthday_and_years', 'address', 'number']
vcf_table.align = 'l'
vcf_table.sortby = 'full_name'
vcf_table.hrules = True


def get_zodiac_sign(birthday):
    """
    Определяет знак зодиака на основе даты рождения.

    :param birthday: Дата рождения (объект datetime.date)
    :return: Строка, содержащая название знака зодиака
    """
    zodiac_signs = {
        'Capricorn': (date(birthday.year, 12, 22), date(birthday.year + 1, 1, 19)),
        'Aquarius': (date(birthday.year, 1, 20), date(birthday.year, 2, 18)),
        'Pisces': (date(birthday.year, 2, 19), date(birthday.year, 3, 20)),
        'Aries': (date(birthday.year, 3, 21), date(birthday.year, 4, 19)),
        'Taurus': (date(birthday.year, 4, 20), date(birthday.year, 5, 20)),
        'Gemini': (date(birthday.year, 5, 21), date(birthday.year, 6, 20)),
        'Cancer': (date(birthday.year, 6, 21), date(birthday.year, 7, 22)),
        'Leo': (date(birthday.year, 7, 23), date(birthday.year, 8, 22)),
        'Virgo': (date(birthday.year, 8, 23), date(birthday.year, 9, 22)),
        'Libra': (date(birthday.year, 9, 23), date(birthday.year, 10, 22)),
        'Scorpio': (date(birthday.year, 10, 23), date(birthday.year, 11, 21)),
        'Sagittarius': (date(birthday.year, 11, 22), date(birthday.year, 12, 21))
    }

    for zodiac, (start_date, end_date) in zodiac_signs.items():
        if start_date <= birthday <= end_date:
            return zodiac
    return ''


try:
    # Открываем очищенный файл vCard с кодировкой utf-8
    with open(cleaned_v_card, encoding='utf-8') as phone_book:
        # Парсим контакты из файла vCard
        contacts = vobject.readComponents(phone_book, allowQP=True)
        for contact in contacts:
            try:
                # Обрабатываем поле full_name с декодированием, если оно закодировано
                if hasattr(contact, 'fn'):
                    full_name_raw = contact.fn.value
                    # Проверяем, есть ли QUOTED-PRINTABLE и декодируем при необходимости
                    if 'ENCODING=QUOTED-PRINTABLE' in full_name_raw:
                        full_name = quopri.decodestring(full_name_raw).decode('utf-8')
                    else:
                        full_name = full_name_raw
                else:
                    full_name = "Неизвестный контакт"

                # Обработка номера телефона, если существует
                number = []
                if hasattr(contact, 'tel_list'):
                    for phone_number in contact.tel_list:
                        number.append(phone_number.value)
                number = '\n'.join(number)

                # Обработка адреса
                address = []
                if hasattr(contact, 'adr_list'):
                    for adds in contact.adr_list:
                        street = adds.value.street
                        if isinstance(street, str):
                            address.append(street)
                        else:
                            address.append(''.join(street))
                address = '\n'.join(address)

                # Дата рождения и знаки зодиака (если существуют)
                try:
                    birthday = date.fromisoformat(contact.bday.value)
                    today = date.today()
                    years = (today - birthday).days // 365

                    sign = get_zodiac_sign(birthday)
                    birthday_and_years = f'Birthday: {birthday.strftime("%d.%m.%Y")}\nZodiac sign: {sign}\nAge: {years}'

                except AttributeError:
                    birthday_and_years = ''

                # Заполняем таблицу
                vcf_table.add_row([full_name, birthday_and_years, address, number])

            except Exception as e:
                # Игнорируем неправильные контакты
                print(f"Ошибка при обработке контакта: {e}")
                continue

except FileNotFoundError:
    raise FileNotFoundError(f"Файл '{v_card}' не найден. Проверьте путь в переменной окружения.")

# Заголовок таблицы с количеством строк
vcf_table.title = f'rowcount: {vcf_table.__getattr__("rowcount")}'

# Сохранение отчета с текущей датой
output_file_name = f'report_{os.path.splitext(os.path.basename(v_card))[0]}_{date.today().strftime("%Y-%m-%d")}.txt'
with open(output_file_name, 'w', encoding='utf-8') as report:
    report.write(vcf_table.get_string())



