from enum import Enum
import operations


class OperationsEnum(Enum):
    ADD = (1, "Сложение", 2, operations.add)
    SUB = (2, "Вычитание", 2, operations.subtract)
    MUL = (3, "Умножение", 2, operations.multiply)
    DIV = (4, "Деление", 2, operations.divide)
    POW = (5, "Степень", 2, operations.power)
    SIN = (6, "Синус", 1, operations.sin)
    COS = (7, "Косинус", 1, operations.cos)
    TAN = (8, "Тангенс", 1, operations.tan)

    def __init__(self, code, description, operand_count, func):
        self.code = code
        self.description = description
        self.operand_count = operand_count
        self.func = func
