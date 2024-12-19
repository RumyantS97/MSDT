import logging

logging.basicConfig(
    filename='Log.log',
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] => %(message)s',
    encoding='utf-8',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()
