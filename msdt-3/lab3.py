import pandas as pd
import re

def validation_string_values(array_params):

    # Готовим значения под RE
    # Делаем их списком и удаляем лишние кавычки
    array_params = array_params.tolist()[0].split(";")
    clean_params = [s.replace('"', '') for s in array_params]
    #print(clean_params[0])
    
    # RE
    # Проверка email
    email_pattern = re.compile(r"""
        ^
        [a-zA-Z0-9.%+-]+         # Имя пользователя
        @                        # Символ 'собака'
        [a-zA-Z0-9-]+            # Основное имя домена
        (?:\.[a-zA-Z0-9-]+)?     # Возможный поддомен
        [\.com|\.org]            # Код почты
        $
    """, re.VERBOSE)

    # Проверка http_status_message
    http_pattern = re.compile(r"""
        ^
        [\d]{3}                  # Код стутуса
        \s+                      # Пробел после кода
        [a-zA-Z|\s]+             # Описание статуса
        $
    """, re.VERBOSE)

    # Проверка snils
    snils_pattern = re.compile(r"""
        ^
        [\d]{11}                 # Код снилса
        $
    """, re.VERBOSE)

    # Проверка passport
    '''
        В данном датасете есть ошибка: первые 2 цифры паспорта - код региона
        значения которого входят в [01, 89].
        Если код выглядит как "9\d" это также является ошибкой
    '''
    
    passport_pattern = re.compile(r"""
        ^
        (?!00)\d{2}              # Код региона
        \s+                      # Пробелы внутри серии
        [0-9]{2}                 # Год выдачи
        \s+                      # Пробелы после серии
        (?!000000)\d{6}          # Номер выдачи паспорта
        $
    """, re.VERBOSE)

    # Проверка ip_v4
    ip_pattern = re.compile(r"""
        ^
        (
            [0-1][0-9]{2}|
            2[0-4][0-9]|         # Бит адреса
            25[0-5]|
            [0-9][0-9]|
            [0-9]
        )
        (
            \.(
                [0-1][0-9]{2}|
                2[0-4][0-9]|     # Бит адреса
                25[0-5]|
                [0-9][0-9]|
                [0-9]
            )
        ){3}
        $
    """, re.VERBOSE)

    # Проверка longitude
    longitude_pattern = re.compile(r"""
        ^
        [-]?
        (
            [0-9]|
            [1-9][0-9]|
            1[0-7][0-9]|         # Целы градусы
            180
        )
        \.
        (
            [0-9]                # Доли градуса
        ){,6}
        $
    """, re.VERBOSE)

    # Проверка hex_color
    color_pattern = re.compile(r"""^#[0-9a-fA-F]{6}$""")

    # Проверка isbn
    '''
        Формат кода книги тоже задаётся иным образом
    '''
    isbn_pattern = re.compile(r"""
        ^
        (\d{3}-)?\d-\d{5}-\d{3}-\d
        $
    """, re.VERBOSE)

    # Проверка local_code
    code_pattern = re.compile(r"""
        ^
        [a-zA-Z]{1,8}            # Код языка
        (
            -                    # Код страны
            [a-zA-Z0-9]{1,8}
        )*
        $
    """, re.VERBOSE)

    # Проверка time
    time_pattern = re.compile(r"""
        ^
        (
            [0-1][0-9]|2[0-3]    # Часы в 24 часовом формате
        )
        :                        # Разделение часов и минут
        (
            [0-5][0-9]           # Минуты в часах
        )
        :                        # Разделение минут и секунд
        (
            [0-5][0-9]           # Секунды в минутах
        )
        \.                       # Разделение секунд и доли секунд
        [0-9]{6}                 # Доли секунд
        $
    """, re.VERBOSE)

    # Проверка полей
    if not email_pattern.match(clean_params[0]):
        #print(clean_params[0])
        return False
    
    if not http_pattern.match(clean_params[1]):
        #print(clean_params[1])
        return False
    
    if not snils_pattern.match(clean_params[2]):
        #print(clean_params[2])
        return False
    
    if not passport_pattern.match(clean_params[3]):
        #print(clean_params[3])
        return False

    if not ip_pattern.match(clean_params[4]):
        #print(clean_params[4])
        return False

    if not longitude_pattern.match(clean_params[5]):
        #print(clean_params[5])
        return False

    if not color_pattern.match(clean_params[6]):
        #print(clean_params[6])
        return False
    
    if not isbn_pattern.match(clean_params[7]):
        #print(clean_params[7])
        return False
    
    if not code_pattern.match(clean_params[8]):
        #print(clean_params[8])
        return False
    
    if not time_pattern.match(clean_params[9]):
        #print(clean_params[9])
        return False
    
    # Если всё верно
    return True
        
 
# Читаем CSV файл
df = pd.read_csv('57.csv', encoding = 'utf-16', delimiter='\t')

# Задаём массив ошибочных строк
error_strings = []

# Проходимся по строкам файла
for i in range (10000):
    if not validation_string_values(df.iloc[i]):
        error_strings.append(i)
        
print(error_strings)
print(len(error_strings))
