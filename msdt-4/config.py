import logging


def logging_config():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename='msdt-4/logs.txt',
        encoding='utf-8'
    )
