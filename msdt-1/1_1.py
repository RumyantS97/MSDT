import json
import os

from datetime import datetime, timedelta


class Expense:
    """Класс, представляющий расход."""

    def __init__(self, amount, category, date, note="", repeat=None):
        self.amount = amount
        self.category = category
        self.date = date
        self.note= note
        self.repeat = repeat  # Еженедельно или ежемесячно

    def __repr__(self):
        repeat_str = f", Повторение: {self.repeat}" if self.repeat else ""
        return f"{self.amount} руб. - {self.category} (Дата: {self.date}{repeat_str}) Заметка: {self.note}"


class Income:
    def __init__(self, amount, date, note=""):
        self.amount = amount
        self.date = date
        self.note = note

    def __repr__(self):
        return f"{self.amount} руб. (Дата: {self.date}) Заметка: {self.note}"


class FinanceTracker:
    """Класс для отслеживания финансов."""

    def __init__(self, filename="expenses_and_incomes.json"):
        self.filename = filename
        self.expenses = []
        self.incomes = []
        self.budgets = {}
        self.load_data()

    def add_expense(self, amount, category, date, note="", repeat=None):
        expense =Expense(amount, category, date, note, repeat)
        self.expenses.append(expense)
        print(f"Добавлен расход: {amount} руб., Категория: {category}, "
              f"Повторение: {repeat}")
        self.check_budget(category)

    def add_income(self, amount, date, note=""):
        income =Income(amount, date, note)
        self.incomes.append(income)
        print(f"Добавлен доход: {amount} руб.")

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            print(f"Удален расход: {removed}")
        else:
            print(f"Расход с индексом {index} не найден!")

    def remove_income(self, index):
        if 0 <= index < len(self.incomes):
            removed = self.incomes.pop(index)
            print(f"Удалён доход: {removed}")
        else:
            print(f"Доход с индексом {index} не найден!")

    def edit_expense(self, index):
        if 0 <= index < len(self.expenses):
            expense = self.expenses[index]
            print(f"Редактирование расхода: {expense}")

            new_amount = input("Введите новую сумму (или оставьте пустым для пропуска): ")
            if new_amount:
                expense.amount = float(new_amount)

            new_category = input("Введите новую категорию (или оставьте пустым для пропуска): ")

            if new_category != None:
                expense.category = new_category

            new_date = input("Введите новую дату (Формат: ГГГГ-ММ-ДД) (или оставьте пустым для пропуска): ")
            if new_date:
                expense.date = new_date

            new_note = input("Введите новую заметку (или оставьте пустым для пропуска): ")
            if new_note:
                expense.note = new_note

            repeat_option = input("Введите новый интервал повторения (weekly/monthly) или оставьте пустым для пропуска: ")
            if repeat_option in ['weekly', 'monthly']:
                expense.repeat = repeat_option

            print(f"Расход обновлен: {expense}")
        else:
            print(f"Расход с индексом {index} не найден!")

    def edit_income(self, index):
        if 0 <= index < len(self.incomes):
            income = self.incomes[index]
            print(f"Редактирование дохода: {income}")

            new_amount = input("Введите новую сумму (или оставьте пустым для пропуска): ")
            if new_amount:
                income.amount = float(new_amount)

            new_date = input("Введите новую дату (Формат: ГГГГ-ММ-ДД) (или оставьте пустым для пропуска): ")
            if new_date:
                income.date = new_date

            new_note = input("Введите новую заметку (или оставьте пустым для пропуска): ")
            if new_note:
                income.note = new_note

            print(f"Доход обновлен: {income}")
        else:
            print(f"Доход с индексом {index} не найден!")

    def view_expenses(self):
        if not self.expenses:
            print("Список расходов пуст!")
            return

        for idx, expense in enumerate(self.expenses, 1):
            print(f"{idx}. {expense}")

    def view_incomes(self):
        if not self.incomes:
            print("Список доходов пуст!")
            return

        for idx, income in enumerate(self.incomes, 1):
            print(f"{idx}. {income}")

    def apply_recurring_expenses(self):
        today = datetime.now().strftime("%Y-%m-%d")
        new_expenses = []
        for expense in self.expenses:
            if expense.repeat == "weekly":
                new_date = datetime.strptime(expense.date, "%Y-%m-%d") + timedelta(weeks=1)
                if new_date.strftime("%Y-%m-%d") <= today:
                    new_expenses.append(Expense(expense.amount, expense.category, new_date.strftime("%Y-%m-%d"), expense.note, expense.repeat))
            elif expense.repeat == "monthly":
                new_date = datetime.strptime(expense.date, "%Y-%m-%d") + timedelta(weeks=4)
                if new_date.strftime("%Y-%m-%d") <= today:
                    new_expenses.append(Expense(expense.amount, expense.category, new_date.strftime("%Y-%m-%d"), expense.note, expense.repeat))
        
        self.expenses.extend(new_expenses)

    def total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        print(f"Общая сумма расходов: {total} руб.")
        return total

    def total_incomes(self):
        total = sum(income.amount for income in self.incomes)
        print(f"Общая сумма доходов: {total} руб.")
        return total

    def calculate_balance(self):
        total_income = self.total_incomes()
        total_expense = self.total_expenses()
        balance = total_income - total_expense
        print(f"Ваш баланс: {balance} руб.")
        return balance

    def set_budget(self, category, amount):
        self.budgets[category] = amount
        print(f"Установлен бюджет для категории {category}: {amount} руб.")

    def check_budget(self, category):
        if category in self.budgets:
            spent = sum(expense.amount for expense in self.expenses if expense.category == category)
            if spent > self.budgets[category]:
                print(f"Внимание! Превышен бюджет для категории {category}. "
                      f"Потрачено: {spent} руб., Бюджет: {self.budgets[category]} руб.")

    def filter_expenses(self, category=None, min_amount=None, max_amount=None, start_date=None, end_date=None):
        filtered = self.expenses

        if category:
            filtered = [expense for expense in filtered if expense.category == category]

        if min_amount is not None:
            filtered = [expense for expense in filtered if expense.amount >= min_amount]

        if max_amount is not None:
            filtered = [expense for expense in filtered if expense.amount <= max_amount]

        if start_date:
            filtered = [expense for expense in filtered if expense.date >= start_date]

        if end_date:
            filtered = [expense for expense in filtered if expense.date <= end_date]

        if not filtered:
            print("Нет расходов, соответствующих заданным критериям.")
        else:
            for idx, expense in enumerate(filtered, 1):
                print(f"{idx}. {expense}")

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump({
                "expenses": [expense.__dict__ for expense in self.expenses],
                "incomes": [income.__dict__ for income in self.incomes],
                "budgets": self.budgets
            }, f, indent=4)
        print("Данные сохранены!")

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.expenses = [Expense(**item) for item in data["expenses"]]
                self.incomes = [Income(**item) for item in data["incomes"]]
                self.budgets = data.get("budgets", {})
            print("Данные загружены!")
        else:
            print("Файл данных не найден. Начинаем с чистого листа.")

    def clear_data(self):
        self.expenses = []
        self.incomes = []
        self.budgets = {}
        print("Все данные очищены!")


def display_menu():
    """Отображение меню действий."""
    print("\nМеню:")
    print("1. Добавить расход")
    print("2. Добавить доход")
    print("3. Удалить расход")
    print("4. Удалить доход")
    print("5. Редактировать расход")
    print("6. Редактировать доход")
    print("7. Показать все расходы")
    print("8. Показать все доходы")
    print("9. Общая сумма расходов")
    print("10. Общая сумма доходов")
    print("11. Баланс")
    print("12. Установить бюджет")
    print("13. Применить повторяющиеся расходы")
    print("14. Фильтровать расходы")
    print("15. Сохранить данные")
    print("16. Загрузить данные")
    print("17. Очистить все данные")
    print("18. Выход")


def main():
    """Главная функция программы, управляющая логикой приложения."""
    tracker = FinanceTracker()

    while True:
        display_menu()
        choice = input("Выберите действие (1-17): ")

        if choice == "1":
            amount = input("Введите сумму расхода: ")
            category = input("Введите категорию: ")
            date = input("Введите дату (Формат: ГГГГ-ММ-ДД): ")
            note = input("Введите заметку (опционально): ")
            repeat = input("Введите интервал повторения (weekly/monthly) или оставьте пустым: ")
            tracker.add_expense(float(amount), category, date, note, repeat)

        elif choice == "2":
            amount = input("Введите сумму дохода: ")
            date = input("Введите дату (Формат: ГГГГ-ММ-ДД): ")
            note = input("Введите заметку (опционально): ")
            tracker.add_income(float(amount), date, note)

        elif choice == "3":
            index = int(input("Введите номер расхода для удаления: ")) - 1
            tracker.remove_expense(index)

        elif choice == "4":
            index = int(input("Введите номер дохода для удаления: ")) - 1
            tracker.remove_income(index)

        elif choice == "5":
            index = int(input("Введите номер расхода для редактирования: ")) - 1
            tracker.edit_expense(index)

        elif choice == "6":
            index = int(input("Введите номер дохода для редактирования: ")) - 1
            tracker.edit_income(index)

        elif choice == "7":
            tracker.view_expenses()

        elif choice == "8":
            tracker.view_incomes()

        elif choice == "9":
            tracker.total_expenses()

        elif choice == "10":
            tracker.total_incomes()



        elif choice == "11":
            tracker.calculate_balance()

        elif choice == "12":
            category = input("Введите категорию: ")
            amount = input(f"Введите бюджет для категории {category}: ")
            tracker.set_budget(category, float(amount))

        elif choice == "13":
            category = input("Введите категорию для фильтрации (или оставьте пустым): ")
            min_amount = input("Введите минимальную сумму для фильтрации (или оставьте пустым): ")
            max_amount = input("Введите максимальную сумму для фильтрации (или оставьте пустым): ")
            start_date = input("Введите начальную дату для фильтрации (ГГГГ-ММ-ДД) (или оставьте пустым): ")
            end_date = input("Введите конечную дату для фильтрации (ГГГГ-ММ-ДД) (или оставьте пустым): ")
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None
            tracker.filter_expenses(category, min_amount, max_amount, start_date, end_date)

        elif choice == "14":
            tracker.save_data()

        elif choice == "15":
            tracker.load_data()

        elif choice == "16":
            tracker.clear_data()

        elif choice == "17":
            print("Выход...")
            break

        else:
            print("Неверный ввод! Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()