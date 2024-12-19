import pytest
from operations_enum import OperationsEnum


def test_get_codes():
    assert OperationsEnum.get_codes() \
           == ['1', '2', '3', '4', '5', '6', '7', '8', '9']


# Проверяем что вернется строка и не будет никаких исключений
def test_get_message_from_input():
    assert OperationsEnum.get_message_for_input().__class__ == 'asd'.__class__


@pytest.mark.parametrize("x", ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
def test_get_exist_item(x):
    assert OperationsEnum.get_item_by_code(x) is not None


@pytest.mark.parametrize("x", ['0', 2, 'asd', ''])
def test_get_non_exist_item(x):
    assert OperationsEnum.get_item_by_code(x) is None
