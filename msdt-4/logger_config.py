import logging

LOG_FILE = "application.log"

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

imageprocessor_logger = logging.getLogger("imageprocessor")
imageprocessor_logger.setLevel(logging.DEBUG)
imageprocessor_logger.addHandler(file_handler)

main_logger = logging.getLogger("main")
main_logger.setLevel(logging.DEBUG)
main_logger.addHandler(file_handler)
