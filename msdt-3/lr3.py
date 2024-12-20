import pandas as pd
import re
from checksum import calculate_checksum
import json

def validation_string_values(array_params):

    array_params = array_params.tolist()[0].split(";")
    clean_params = [s.replace('"', '') for s in array_params]
    telephone = re.compile(r"""
        ^
        \+
        7
        -
        \(\d{3}\)
        -
        \d{3}
        -
        \d{2}
        -
        \d{2}
        $                                                                     
    """, re.VERBOSE)
    inn = re.compile(r"""
        ^
        \d{12}             
        $ 
                                 
    """, re.VERBOSE)
    identifier = re.compile (r"""
        ^
        \d{2}
        -
        \d{2}
        / 
        \d{2}                                                                                  
        $                     
    """, re.VERBOSE)
    latitude = re.compile(r"""
        ^
        [-]?
        (
            [0-9]|
            [1-8][0-9]|
            90                 
        )
        \.
        (
            [0-9]      
        ){,6}
        $
    """, re.VERBOSE)
    blood = re.compile(r"""
        ^
        ([ABO]|AB)
        [\−\+]
        $
    """, re.VERBOSE)
    uuid = re.compile(r"""
        ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
    """, re.VERBOSE)
    date = re.compile(r"""
        ^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$
    """, re.VERBOSE)
    # Проверка http_status_message
    http = re.compile(r"""
        ^
        [\d]{3}                  # Код стутуса
        \s+                      # Пробел после кода
        [a-zA-Z|\s]+             # Описание статуса
        $
    """, re.VERBOSE)
# Проверка ip_v4
    ip = re.compile(r"""
        ^
        (
            [0-1][0-9]{2}|
            2[0-4][0-9]|         
            25[0-5]|
            [0-9][0-9]|
            [0-9]
        )
        (
            \.(
                [0-1][0-9]{2}|
                2[0-4][0-9]|     
                25[0-5]|
                [0-9][0-9]|
                [0-9]
            )
        ){3}
        $
    """, re.VERBOSE)
    isbn = re.compile(r"""
        ^
        (\d{3}-)?
        \d
        -
        \d{5}
        -
        \d{3}
        -
        \d
        $
    """, re.VERBOSE)

    if not date.match(clean_params[9]):
        #print (clean_params[9])
        return False
    if not uuid.match(clean_params[8]):
        #print (clean_params[8])
        return False
    if not blood.match(clean_params[6]):
        #print (clean_params[6])
        return False
    if not latitude.match(clean_params[5]):
        #print (clean_params[5])
        return False
    if not identifier.match(clean_params[3]):
        #print(clean_params[3])
        return False
    if not telephone.match(clean_params[0]):
       #print(clean_params[0])
       return False
    if not inn.match(clean_params[2]):
        #print(clean_params[2])
        return False
    if not http.match(clean_params[1]):
        #print(clean_params[1])
        return False
    if not ip.match(clean_params[4]):
        #print(clean_params[4])
        return False
    if not isbn.match(clean_params[7]):
        #print(clean_params[7])
        return False
    return True

def serialize_result(variant: int, checksum: str) -> None:
    result = {
        'variant': variant,
        'checksum': checksum
    }
    with open ( 'result.json', 'w', encoding='utf-8' ) as json_file:
        json.dump( result, json_file, ensure_ascii = False, indent = 4 )

# Читаем CSV файл
df = pd.read_csv('54.csv', encoding = 'utf-16', delimiter='\t')

# Задаём массив ошибочных строк
error_strings = []

# Проходимся по строкам файла
for i in range (10000):
    if not validation_string_values(df.iloc[i]):
        error_strings.append(i)
        
print(error_strings)
print(len(error_strings))

#Получаем контрольную сумму и перезаписываем JSON файл
checksum = calculate_checksum(error_strings)
serialize_result(54, checksum)
