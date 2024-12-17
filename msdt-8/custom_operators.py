from logging_config import logger, DEBUG_EX


def less_than(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "less_than"')
    return a < b


def greater_than(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "greater_than"')
    return a > b


def equal_to(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "equal_to"')
    return a == b


def not_equal_to(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "not_equal_to"')
    return a != b


def less_than_or_equal_to(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "less_than_or_equal_to"')
    return a <= b


def greater_than_or_equal_to(a, b):
    logger.log(DEBUG_EX, 'Произошел вызов функции "greater_than_or_equal_to"')
    return a >= b


operator_lt = less_than
operator_gt = greater_than
operator_eq = equal_to
operator_ne = not_equal_to
operator_le = less_than_or_equal_to
operator_ge = greater_than_or_equal_to
