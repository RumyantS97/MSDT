"""The `BankAccount` class in Python represents a bank account with
functionalities for depositing, withdrawing, checking balance, and viewing
transaction history.
"""
from models.transaction import Transaction
from exceptions.insufficient_funds_error import InsufficientFundsError


class BankAccount:
    """This class represents a bank account in Python."""  # noqa: D404

    def __init__(self, account_id, owner, currency="USD"):
        """The function initializes a class instance with account details including
        account ID, owner, balance, currency, and transactions list.

        :param account_id: The `account_id` parameter in the `__init__` method is
        used to initialize the account ID for a new account object. It is a unique
        identifier for the account within the system
        :param owner: The `owner` parameter in the `__init__` method of a class
        typically represents the owner or holder of the account. It could be a
        person, organization, or entity that owns the account. This parameter is
        used to initialize the `owner` attribute of the class instance with the
        value passed

        :param currency: The `currency` parameter in the `__init__` method of a
        class represents the currency in which the account is denominated. By
        default, it is set to "USD" (United States Dollar), but you can provide a
        different currency when creating an instance of the class. This parameter
        allows, defaults to USD (optional).

        """
        self.account_id = account_id
        self.owner = owner
        self.balance = 0.0
        self.currency = currency
        self.transactions = []

    def deposit(self, amount):
        """The `deposit` function adds a specified amount to an account balance and
        creates a transaction record.

        :param amount: The `amount` parameter in the `deposit` method represents
        the sum of money that is being deposited into an account. It is used to
        increase the balance of the account by that specific amount
        """
        if amount <= 0:
            raise ValueError("Сумма для пополнения должна быть положительной.")
        self.balance += amount
        transaction = Transaction("Пополнение", amount, self.balance)
        self.transactions.append(transaction)
        print(
            f"Успешно пополнен счет на {amount} {self.currency}.\n"
            f"Текущий баланс: {self.balance} {self.currency}")

    def withdraw(self, amount):
        """This function is likely a method within a class that handles withdrawing a
        specified amount of money.

        :param amount: The `withdraw` method is used to deduct a specific `amount`
        from an account balance. The `amount` parameter represents the value that
        will be withdrawn from the account balance

        """  # noqa: D404
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной.")
        if amount > self.balance:
            raise InsufficientFundsError("Недостаточно средств на счете.")
        self.balance -= amount
        transaction = Transaction("Снятие", amount, self.balance)
        self.transactions.append(transaction)
        print(f"Успешно снято {amount} {self.currency}.\n"
              f"Текущий баланс: {self.balance} {self.currency}")

    def get_balance(self):
        """This function is likely a method within a class that retrieves the current
        balance.
        """  # noqa: D404
        return self.balance

    def get_transaction_history(self):
        """This function retrieves the transaction history."""  # noqa: D404
        return [str(transaction) for transaction in self.transactions]
