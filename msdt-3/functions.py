import json
import csv
import re


def read_csv(path):
    try:
        data = []
        with open(path, mode = "r", encoding="utf-16") as file:
            file_reader = csv.reader(file, delimiter = ';')
            next(file_reader, None)
            for row in file_reader:
                data.append(row)
            return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f'"The file {path} does not exist') \
            from e
    except Exception as e:
        raise e
        
        
def read_json(path):
    try:
        with open(path, mode = "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {path} does not exist") \
            from e
    except Exception as e:
        raise e
        

def write_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {path} does not exist") \
            from e
    except Exception as e:
        raise e
    
    
def check_validation(data, patterns):
    for key, value in zip(patterns.keys(), data):
        if not re.match(patterns[key], value):
            return False
    return True


def get_list(data, patterns):
    list = []
    for i, row in enumerate(data):
        if not check_validation(row, patterns):
            list.append(i)
    return list