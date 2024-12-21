import pytest
from models.checking_account import CheckingAccount
from models.saving_account import SavingsAccount
from exceptions.account_not_found_error import AccountNotFoundError
from bank import Bank  # Предполагается, что класс Bank находится в файле bank.py

@pytest.fixture
def bank():
    """Создает экземпляр банка для тестов."""
    return Bank()

@pytest.mark.parametrize("account_id, owner, account_type", [
    ("123", "Alice", "checking"),
    ("456", "Bob", "savings"),
])
def test_create_account(bank, account_id, owner, account_type):
    """Тестирует создание аккаунтов."""
    bank.create_account(account_id, owner, account_type)
    account = bank.get_account(account_id)
    assert account.owner == owner
    assert account.account_id == account_id
    assert type(account) == (CheckingAccount if account_type == "checking" else SavingsAccount)

def test_create_account_with_existing_id(bank):
    """Тестирует попытку создания аккаунта с существующим ID."""
    bank.create_account("123", "Alice", "checking")
    with pytest.raises(ValueError, match="An account with this ID already exists."):
        bank.create_account("123", "Bob", "savings")

@pytest.mark.parametrize("account_id", ["123", "456"])
def test_get_account(bank, account_id):
    """Тестирует получение аккаунтов."""
    bank.create_account(account_id, "Owner", "checking")
    account = bank.get_account(account_id)
    assert account.account_id == account_id

def test_get_nonexistent_account(bank):
    """Тестирует получение несуществующего аккаунта."""
    with pytest.raises(AccountNotFoundError, match="Account with ID nonexistent not found."):
        bank.get_account("nonexistent")

@pytest.mark.parametrize("from_account_id, to_account_id, amount", [
    ("123", "456", 50),
    ("456", "123", 30),
])
def test_transfer(bank, from_account_id, to_account_id, amount):
    """Тестирует перевод средств между аккаунтами."""
    bank.create_account(from_account_id, "Alice", "checking")
    bank.create_account(to_account_id, "Bob", "savings")
    
    # Начальные депозиты
    bank.accounts[from_account_id].deposit(100)
    
    # Перевод средств
    bank.transfer(from_account_id, to_account_id, amount)
    
    assert bank.accounts[from_account_id].balance == 100 - amount
    assert bank.accounts[to_account_id].balance == amount

def test_transfer_nonexistent_account(bank):
    """Тестирует перевод средств с несуществующего аккаунта."""
    bank.create_account("123", "Alice", "checking")
    
    with pytest.raises(AccountNotFoundError, match="Account with ID nonexistent not found."):
        bank.transfer("123", "nonexistent", 50)