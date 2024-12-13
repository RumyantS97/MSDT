import csv
import random
import statistics
from typing import List, Dict

def log(message: str):
    print(f"[LOG]: {message}")

def read_csv(file_path: str) -> List[Dict[str, str]]:
    log("Reading CSV file...")
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    log("CSV file read successfully.")
    return data

def clean_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    log("Cleaning data...")
    cleaned_data = []
    for row in data:
        if all(row.values()):  # Удаление строк с пустыми значениями
            cleaned_data.append(row)
    log("Data cleaned successfully.")
    return cleaned_data

def filter_data(data: List[Dict[str, str]], column_name: str, min_value: int) -> List[Dict[str, str]]:
    log(f"Filtering data where column '{column_name}' >= {min_value}...")
    filtered_data = [row for row in data if row[column_name].isdigit() and int(row[column_name]) >= min_value]
    log(f"Data filtered successfully. Remaining rows: {len(filtered_data)}.")
    return filtered_data

def generate_random_column(data: List[Dict[str, str]], column_name: str) -> None:
    log(f"Generating random values for column '{column_name}'...")
    for row in data:
        row[column_name] = random.randint(0, 100)
    log(f"Random values for column '{column_name}' generated.")

def calculate_statistics(data: List[Dict[str, str]], column_name: str) -> Dict[str, float]:
    log(f"Calculating statistics for column '{column_name}'...")
    values = [int(row[column_name]) for row in data if row[column_name].isdigit()]
    stats = {
        'mean': sum(values) / len(values) if values else 0,
        'max': max(values) if values else 0,
        'min': min(values) if values else 0,
        'median': statistics.median(values) if values else 0
    }
    log(f"Statistics for column '{column_name}' calculated.")
    return stats

def group_by_column(data: List[Dict[str, str]], column_name: str) -> Dict[str, List[Dict[str, str]]]:
    log(f"Grouping data by column '{column_name}'...")
    grouped_data = {}
    for row in data:
        key = row[column_name]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(row)
    log(f"Data grouped by column '{column_name}'. Groups: {len(grouped_data)}.")
    return grouped_data

def save_csv(data: List[Dict[str, str]], file_path: str) -> None:
    log(f"Saving data to CSV file '{file_path}'...")
    if not data:
        log("No data to save.")
        return
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    log(f"Data saved to CSV file '{file_path}' successfully.")

def display_group_info(groups: Dict[str, List[Dict[str, str]]]):
    log("Displaying group information...")
    for group, items in groups.items():
        log(f"Group: {group}, Items: {len(items)}")

def main(input_file: str, output_file: str, random_column: str):
    log("Starting the process...")
    data = read_csv(input_file)
    data = clean_data(data)
    generate_random_column(data, random_column)

    stats = calculate_statistics(data, random_column)
    log("Summary of statistics:")
    for stat_name, value in stats.items():
        log(f"  {stat_name}: {value}")

    filtered_data = filter_data(data, random_column, 50)
    groups = group_by_column(filtered_data, random_column)
    display_group_info(groups)

    save_csv(filtered_data, output_file)
    log("Process completed.")

if __name__ == "__main__":
    input_file = "input.csv"
    output_file = "output.csv"
    random_column = "RandomValue"
    main(input_file, output_file, random_column)
