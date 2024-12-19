import sys

from loguru import logger


def loguru_config():
    logger.remove()  # Удаляем стандартный вывод
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                                  "<level>{level: <8}</level> | "
                                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                                  "<white>{message}</white>",
               level="DEBUG")
