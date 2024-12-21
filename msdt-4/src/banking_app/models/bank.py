from models.checking_account import CheckingAccount
from models.saving_account import SavingsAccount

from exceptions.account_not_found_error import AccountNotFoundError


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id, owner, account_type="checking"):
        if account_id in self.accounts:
            raise ValueError("Аккаунт с таким ID уже существует.")
        
        if account_type == "checking":
            account = CheckingAccount(account_id, owner)
        elif account_type == "savings":
            account = SavingsAccount(account_id, owner)
        else:
            raise ValueError("Неверный тип аккаунта. Доступные типы: checking, savings.")
        
        self.accounts[account_id] = account
        print(f"Аккаунт {account_id} успешно создан.")

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Аккаунт с ID {account_id} не найден.")
        return self.accounts[account_id]

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        from_account.withdraw(amount)
        to_account.deposit(amount)
        print(f"Успешный перевод {amount} {from_account.currency} от {from_account_id} к {to_account_id}.")
