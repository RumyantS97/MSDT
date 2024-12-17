import logging


def my_log() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='msdt-4/code_log.txt',
        encoding='utf-8'
    )
