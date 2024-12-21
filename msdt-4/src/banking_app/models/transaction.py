class Transaction:
    def __init__(self, transaction_type, amount, balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}, Остаток: {self.balance_after}"
