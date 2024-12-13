import json


def write_to_json_file(path: str, data: dict) -> None:
    """
    Writes a dict to json file
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
    