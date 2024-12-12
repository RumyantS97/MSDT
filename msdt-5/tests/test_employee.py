import pytest
import math
from src.employee import Employee, Account


# Тесты для класса Employee
@pytest.fixture
def employee():
    return Employee("John", "Doe", 3000)


# Тесты для метода describe_employee
def test_describe_employee(employee, capsys):
    employee.describe_employee()
    captured = capsys.readouterr()
    expected_output = "I am John Doe and my salary is 3000 euro.\n"
    assert captured.out == expected_output


# Тесты для метода complet_name
def test_complet_name(employee):
    assert employee.complet_name() == "John Doe"


# Тесты для метода month_salary
def test_month_salary(employee):
    assert employee.month_salary() == 3000


# Тесты для метода annual_salary
def test_annual_salary(employee):
    assert employee.annual_salary() == 36000


# Тесты для метода increase_salary
def test_increase_salary(employee):
    new_salary = employee.increase_salary(10)
    assert math.isclose(new_salary, 3300)  # Увеличение на 10%: 3000 * 1.10 = 3300
    assert employee.salary == 3300


# Тесты для метода increase_salary с другими значениями
def test_increase_salary_20_percent(employee):
    new_salary = employee.increase_salary(20)
    assert math.isclose(new_salary, 3600)  # Увеличение на 20%: 3000 * 1.20 = 3600


# Тесты для метода increase_salary с отрицательным процентом
def test_increase_salary_negative(employee):
    new_salary = employee.increase_salary(-10)
    assert math.isclose(new_salary, 2700)  # Уменьшение на 10%: 3000 * 0.90 = 2700


# Тесты для создания Employee с различными значениями
def test_employee_with_zero_salary():
    employee = Employee("Alice", "Smith", 0)
    assert employee.salary == 0
    assert employee.annual_salary() == 0


def test_employee_with_high_salary():
    employee = Employee("Big", "Boss", 1000000)
    assert employee.salary == 1000000
    assert employee.annual_salary() == 12000000


# Тесты для класса Account
@pytest.fixture
def account():
    return Account("RO123456789", "John Doe", 5000)


# Тесты для метода balance_display
def test_balance_display(account, capsys):
    account.balance_display()
    captured = capsys.readouterr()
    expected_output = "Owner John Doe has in account with iban:RO123456789 the amount of 5000 RON.\n"
    assert captured.out == expected_output


# Тесты для метода debiting
def test_debiting(account):
    new_balance = account.debiting(1000)
    assert math.isclose(new_balance, 4000)
    assert account.balance == 4000


def test_debiting_more_than_balance(account):
    new_balance = account.debiting(6000)
    assert math.isclose(new_balance, -1000)
    assert account.balance == -1000


# Тесты для метода deposit
def test_deposit(account):
    new_balance = account.deposit(1500)
    assert math.isclose(new_balance, 6500)
    assert account.balance == 6500


def test_deposit_negative_amount(account):
    new_balance = account.deposit(-500)
    assert math.isclose(new_balance, 4500)
    assert account.balance == 4500


# Тесты для Account с нулевым балансом
def test_account_with_zero_balance():
    account = Account("RO987654321", "Alice", 0)
    assert account.balance == 0
    account.deposit(500)
    assert account.balance == 500
    account.debiting(100)
    assert account.balance == 400


# Тесты для Account с отрицательным балансом
def test_account_with_negative_balance():
    account = Account("RO987654321", "Bob", -100)
    assert account.balance == -100
    account.deposit(200)
    assert account.balance == 100
    account.debiting(150)
    assert account.balance == -50
