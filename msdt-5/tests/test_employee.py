import math

import pytest
from src.employee import Employee, Account

# Тесты для класса Employee
@pytest.fixture
def employee():
    return Employee("John", "Doe", 3000)

def test_complet_name(employee):
    assert employee.complet_name() == "John Doe"

def test_month_salary(employee):
    assert employee.month_salary() == 3000

def test_annual_salary(employee):
    assert employee.annual_salary() == 3000 * 12

def test_increase_salary(employee):
    new_salary = employee.increase_salary(10)

    assert math.isclose(new_salary, 3000 * 1.1)
    assert math.isclose(employee.salary, 3000 * 1.1)

# Тесты для класса Account
@pytest.fixture
def account():
    return Account("RO49AAAA1B31007593840000", "Jane Doe", 1000)

def test_balance_display(mocker, account):
    mock_print = mocker.patch("builtins.print")
    account.balance_display()
    mock_print.assert_called_with(
        f"Owner {account.owner} has in account with iban:{account.iban}"
        f" the amount of {account.balance} RON."
    )

def test_debiting(account):
    new_balance = account.debiting(500)
    assert new_balance == 500

def test_deposit(account):
    new_balance = account.deposit(200)
    assert new_balance == 1200
