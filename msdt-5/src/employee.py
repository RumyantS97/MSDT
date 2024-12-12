import math

class Employee:
    def __init__(self, first_name, second_name, salary):
        self.first_name = first_name
        self.second_name = second_name
        self.salary = salary

    def describe_employee(self):
        print(f"I am {self.first_name} {self.second_name} and my salary is {self.salary} euro.")

    def complet_name(self) -> str:
        return self.first_name + " " + self.second_name

    def month_salary(self) -> int:
        return self.salary

    def annual_salary(self) -> int:
        return self.salary * 12

    def increase_salary(self, procent: int) -> float:
        self.salary += ((self.salary * procent) / 100)
        return self.salary


class Account:
    def __init__(self, iban, owner, sold):
        self.iban = iban
        self.owner = owner
        self.balance = sold

    def balance_display(self):
        print(f"Owner {self.owner} has in account with iban:{self.iban} the amount of {self.balance} RON.")

    def debiting(self, taken_amount):
        self.balance -= taken_amount
        return self.balance

    def deposit(self, entered_amount):
        self.balance += entered_amount
        return self.balance