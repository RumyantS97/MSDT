from models.bank import Bank
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.insufficient_funds_error import InsufficientFundsError

def main():
    bank = Bank()

    while True:
        print("\nВыберите действие:")
        print("1. Создать аккаунт")
        print("2. Пополнить счет")
        print("3. Снять средства")
        print("4. Проверить баланс")


        print("5. Перевести средства")
        print("6. Показать историю транзакций")
        print("7. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            account_id = input("Введите ID аккаунта: ")
            owner = input("Введите имя владельца: ")
            account_type = input("Введите тип аккаунта (checking/savings): ")
            try:
                bank.create_account(account_id, owner, account_type)
            except ValueError as e:
                print(e)

        elif choice == '2':
            account_id = input("Введите ID аккаунта: ")
            amount = float(input("Введите сумму для пополнения: "))
            try:
                account = bank.get_account(account_id)
                account.deposit(amount)
            except (ValueError, AccountNotFoundError) as e:
                print(e)

        elif choice == '3':
            account_id = input("Введите ID аккаунта: ")
            amount = float(input("Введите сумму для снятия: "))
            try:
                account = bank.get_account(account_id)
                account.withdraw(amount)
            except (InsufficientFundsError, ValueError, AccountNotFoundError) as e:
                print(e)

        elif choice == '4':
            account_id = input("Введите ID аккаунта: ")
            try:
                account = bank.get_account(account_id)
                print(
                    f"Баланс аккаунта {account_id}: {account.get_balance()} "
                    f"{account.currency}")
            except AccountNotFoundError as e:
                print(e)

        elif choice == '5':
            from_account_id = input("Введите ID отправителя: ")
            to_account_id = input("Введите ID получателя: ")
            amount = float(input("Введите сумму для перевода: "))
            try:
                bank.transfer(from_account_id, to_account_id, amount)
            except (InsufficientFundsError, AccountNotFoundError) as e:
                print(e)

        elif choice == '6':
            account_id = input("Введите ID аккаунта: ")
            try:
                account = bank.get_account(account_id)
                history = account.get_transaction_history()
                print(f"История транзакций для аккаунта {account_id}:")
                for transaction in history:
                    print(transaction)
            except AccountNotFoundError as e:
                print(e)

        elif choice == '7':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
