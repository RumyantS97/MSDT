from loguru import logger
from models.checking_account import CheckingAccount
from models.saving_account import SavingsAccount
from exceptions.account_not_found_error import AccountNotFoundError

class Bank:
    def __init__(self):
        self.accounts = {}
        logger.info("Bank initialized.")

    def create_account(self, account_id, owner, account_type="checking"):
        if account_id in self.accounts:
            logger.info(f"Attempt to create an account with existing ID: {account_id}.")
            raise ValueError("An account with this ID already exists.")

        if account_type == "checking":
            account = CheckingAccount(account_id, owner)
        elif account_type == "savings":
            account = SavingsAccount(account_id, owner)
        else:
            logger.info(f"Invalid account type: {account_type}.")
            raise ValueError("Invalid account type. Available types: checking, savings.")

        self.accounts[account_id] = account
        logger.info(f"Account {account_id} successfully created.")

    def get_account(self, account_id):
        if account_id not in self.accounts:
            logger.info(f"Account with ID {account_id} not found.")
            raise AccountNotFoundError(f"Account with ID {account_id} not found.")

        logger.info(f"Request for account with ID {account_id} successfully completed.")
        return self.accounts[account_id]

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        from_account.withdraw(amount)
        to_account.deposit(amount)
        logger.info(f"Successfully transferred {amount} from account {from_account_id} to account {to_account_id}.")