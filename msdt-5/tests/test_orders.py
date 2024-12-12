import pytest
import math
from unittest.mock import patch
from src.orders import calculate_total, Item, Order, DynamicallyPricedItem


# Тесты для функции calculate_total
def test_calculate_total_valid_values():
    result = calculate_total(100, 10, 5, 0.2)
    assert math.isclose(result, 126.0)

def test_calculate_total_negative_subtotal():
    with pytest.raises(ValueError, match="subtotal cannot be negative"):
        calculate_total(-100, 10, 5, 0.2)

def test_calculate_total_negative_shipping():
    with pytest.raises(ValueError, match="shipping cannot be negative"):
        calculate_total(100, -10, 5, 0.2)

def test_calculate_total_negative_discount():
    with pytest.raises(ValueError, match="discount cannot be negative"):
        calculate_total(100, 10, -5, 0.2)

def test_calculate_total_negative_tax_percent():
    with pytest.raises(ValueError, match="tax_percent cannot be negative"):
        calculate_total(100, 10, 5, -0.2)

def test_calculate_total_amount_less_than_zero():
    result = calculate_total(100, 10, 120, 0.2)
    assert math.isclose(result, 0.0)


# Тесты для класса Item
@pytest.fixture
def item():
    return Item("Laptop", 1000, 2)

def test_item_calculate_item_total(item):
    assert math.isclose(item.calculate_item_total(), 2000.00)


# Тесты для класса Order
@pytest.fixture
def order():
    return Order(shipping=10, discount=50, tax_percent=0.2)

def test_add_item_to_order(order, item):
    order.add_item(item)
    assert len(order.items) == 1
    assert order.items[0] == item

def test_calculate_subtotal(order, item):
    order.add_item(item)
    assert math.isclose(order.calculate_subtotal(), 2000.00)

def test_calculate_order_total(order, item):
    order.add_item(item)
    total = order.calculate_order_total()
    expected_total = (2000.00 + 10 - 50) * (1 + 0.2)
    assert math.isclose(total, expected_total)

def test_get_reward_points(order, item):
    order.add_item(item)
    assert order.get_reward_points() == 2362


# Тесты для класса DynamicallyPricedItem
@pytest.fixture
def dynamic_item():
    return DynamicallyPricedItem(id=12345, quantity=2)

@patch('requests.get')
def test_get_latest_price(mock_get, dynamic_item):
    mock_get.return_value.json.return_value = {'price': 200}
    price = dynamic_item.get_latest_price()
    assert math.isclose(price, 200)

@patch('requests.get')
def test_calculate_item_total_with_dynamic_price(mock_get, dynamic_item):
    mock_get.return_value.json.return_value = {'price': 200}
    total = dynamic_item.calculate_item_total()
    assert math.isclose(total, 400.00)
