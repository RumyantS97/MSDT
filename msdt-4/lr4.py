import csv
import random
import statistics
from typing import List, Dict
import logging


logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s [%(levelname)s] %(message)s",  
    handlers=[logging.StreamHandler()]  
)
logger = logging.getLogger("data_processing")


def read_csv(file_path: str) -> List[Dict[str, str]]:
    logger.info(f"Reading CSV file: {file_path}")
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    logger.info(f"Read {len(data)} rows from CSV file.")
    return data


def clean_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    logger.debug("Cleaning data...")
    cleaned_data = [row for row in data if all(row.values())]
    logger.info(f"Cleaned data: {len(cleaned_data)} rows remain after cleaning.")
    return cleaned_data


def filter_data(data: List[Dict[str, str]], column_name: str, min_value: int) -> List[Dict[str, str]]:
    logger.debug(f"Filtering data where column '{column_name}' >= {min_value}...")
    filtered_data = [row for row in data if row[column_name].isdigit() and int(row[column_name]) >= min_value]
    logger.info(f"Filtered data: {len(filtered_data)} rows match the condition.")
    return filtered_data


def generate_random_column(data: List[Dict[str, str]], column_name: str) -> None:
    logger.debug(f"Generating random values for column '{column_name}'...")
    for row in data:
        row[column_name] = random.randint(0, 100)
    logger.info(f"Generated random values for {len(data)} rows.")


def calculate_statistics(data: List[Dict[str, str]], column_name: str) -> Dict[str, float]:
    logger.info(f"Calculating statistics for column '{column_name}'...")
    values = [int(row[column_name]) for row in data if row[column_name].isdigit()]
    stats = {
        'mean': sum(values) / len(values) if values else 0,
        'max': max(values) if values else 0,
        'min': min(values) if values else 0,
        'median': statistics.median(values) if values else 0
    }
    logger.info(f"Statistics: {stats}")
    return stats


def group_by_column(data: List[Dict[str, str]], column_name: str) -> Dict[str, List[Dict[str, str]]]:
    logger.debug(f"Grouping data by column '{column_name}'...")
    grouped_data = {}
    for row in data:
        key = row[column_name]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(row)
    logger.info(f"Grouped data by column '{column_name}': {len(grouped_data)} groups created.")
    return grouped_data


def save_csv(data: List[Dict[str, str]], file_path: str) -> None:
    logger.info(f"Saving data to CSV file: {file_path}")
    if not data:
        logger.warning("No data to save.")
        return
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"Data saved to CSV file '{file_path}' successfully.")


def display_group_info(groups: Dict[str, List[Dict[str, str]]]):
    logger.debug("Displaying group information...")
    for group, items in groups.items():
        logger.info(f"Group '{group}': {len(items)} items")


def main(input_file: str, output_file: str, random_column: str):
    logger.info("Starting the data processing pipeline...")
    try:
        data = read_csv(input_file)
        data = clean_data(data)
        generate_random_column(data, random_column)
        
        stats = calculate_statistics(data, random_column)
        logger.info("Summary of statistics:")
        for stat_name, value in stats.items():
            logger.info(f"  {stat_name}: {value}")

        filtered_data = filter_data(data, random_column, 50)
        groups = group_by_column(filtered_data, random_column)
        display_group_info(groups)

        save_csv(filtered_data, output_file)
        logger.info("Data processing pipeline completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = "input.csv"
    output_file = "output.csv"
    random_column = "RandomValue"
    main(input_file, output_file, random_column)
