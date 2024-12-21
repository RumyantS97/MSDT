import sys

from loguru import logger
# Use datetime today() for log file naming
from datetime import date


# Add info+ logs in file
logger.add(
    # log directory
    f'logs/info/log_{date.today()}.log',
    # log format
    format='{time} | {level} | {message}',
    # new file creating
    rotation='7:00',
    # file live
    retention='1 week',
    # format of compression
    compression='zip',
    # logging level
    level='INFO'
)

# Add error messages in the error files
logger.add(
    # log directory
    f'logs/error/log_{date.today()}.log',
    # log format
    format='{time} | {level} | {message}',
    # new file creating
    rotation='7:00',
    # format of compression
    compression='zip',
    # logging level
    level='ERROR'
)

# Add debug info in stderr
logger.add(sys.stderr, level='DEBUG')

