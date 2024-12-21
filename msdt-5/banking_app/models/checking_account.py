from loguru import logger
from .bank_account import BankAccount

class CheckingAccount(BankAccount):
    def __init__(self, account_id, owner):
        logger.info(f'Initialize checking account {account_id}')
        super().__init__(account_id, owner, currency="USD")
