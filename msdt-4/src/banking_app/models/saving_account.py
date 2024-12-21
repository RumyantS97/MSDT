from models.bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self, account_id, owner):
        super().__init__(account_id, owner, currency="USD")
