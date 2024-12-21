from loguru import logger
from .bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self, account_id, owner):
        logger.info(f'Initialize saving account {account_id}')
        super().__init__(account_id, owner, currency="USD")
