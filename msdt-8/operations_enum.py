from enum import Enum
import operations


class OperationsEnum(Enum):
    ADD = ('1', "Сложение", 2, operations.add)
    SUB = ('2', "Вычитание", 2, operations.subtract)
    MUL = ('3', "Умножение", 2, operations.multiply)
    DIV = ('4', "Деление", 2, operations.divide)
    POW = ('5', "Степень", 2, operations.power)
    SIN = ('6', "Синус", 1, operations.sin)
    COS = ('7', "Косинус", 1, operations.cos)
    TAN = ('8', "Тангенс", 1, operations.tan)
    SQR = ('9', "Квадратный корень", 1, operations.sqrt)

    def __init__(self, code, description, operand_count, func):
        self.code = code
        self.description = description
        self.operand_count = operand_count
        self.func = func

    @staticmethod
    def get_codes():
        return [i.code for i in OperationsEnum]

    @staticmethod
    def get_message_for_input():
        message = "Выберите операцию:\n"
        for i in OperationsEnum:
            message += f'{i.description} - нажмите {i.code}\n'
        return message

    @staticmethod
    def get_item_by_code(code):
        for i in OperationsEnum:
            if i.code == code:
                return i
        return None

