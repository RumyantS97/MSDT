import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def connect_to_db():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="Yanepidor228!", database="atms")
        logging.info("Успешное подключение к базе данных.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Ошибка подключения к базе данных: {err}")
        raise


def clear_entries(entries):
    logging.info("Начало очистки полей ввода.")
    for entry in entries:
        entry.delete(0, tk.END)
    logging.info("Все поля ввода успешно очищены.")


def load_data(tree, query):
    logging.info(f"Попытка загрузки данных с запросом: {query}")
    try:
        for row in tree.get_children():
            tree.delete(row)

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        logging.info(f"Успешная загрузка данных: {len(rows)} записей.")
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")


def manage_banks(tab):
    def add_bank():
        bank_id = entry_bank_id.get()
        bank_name = entry_bank_name.get()
        legal_address = entry_legal_address.get()

        if not bank_name or not legal_address:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            logging.warning("Не удалось добавить банк: поля не заполнены.")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Banks (bank_id, bank_name, legal_address) VALUES (%s, %s, %s)",
                (bank_id, bank_name, legal_address)
            )
            conn.commit()
            conn.close()
            logging.info(f"Банк добавлен: ID={bank_id}, Название={bank_name}.")
            messagebox.showinfo("Успех", "Банк добавлен!")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка при добавлении банка: {err}")
            messagebox.showerror("Ошибка", f"Не удалось добавить банк: {err}")

        clear_entries([entry_bank_id, entry_bank_name, entry_legal_address])
        load_data(tree_banks, "SELECT * FROM Banks")


    tk.Label(tab, text="ID банка:").pack(pady=5)
    entry_bank_id = tk.Entry(tab)
    entry_bank_id.pack(pady=5)

    tk.Label(tab, text="Название банка:").pack(pady=5)
    entry_bank_name = tk.Entry(tab)
    entry_bank_name.pack(pady=5)

    tk.Label(tab, text="Юридический адрес:").pack(pady=5)
    entry_legal_address = tk.Entry(tab)
    entry_legal_address.pack(pady=5)

    tk.Button(tab, text="Добавить банк", command=add_bank).pack(pady=10)
    tk.Button(tab, text="Очистить поля", command=lambda: clear_entries([entry_bank_id, entry_bank_name, entry_legal_address])).pack(pady=10)

    tree_banks = ttk.Treeview(tab, columns=("ID", "Название банка", "Юридический адрес"), show="headings")
    tree_banks.heading("ID", text="ID")
    tree_banks.heading("Название банка", text="Название банка")
    tree_banks.heading("Юридический адрес", text="Юридический адрес")
    tree_banks.pack(pady=20)

    load_data(tree_banks, "SELECT * FROM Banks")



def manage_atms(tab):
    def add_atm():
        logging.info("Пользователь нажал на кнопку добавления банкомата.")
        atm_id = entry_atm_id.get()
        atm_address = entry_atm_address.get()
        bank_id = entry_bank_id_atm.get()

        if not atm_address or not bank_id:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            logging.warning("Не удалось добавить банкомат: не все поля заполнены.")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            logging.info(f"Попытка добавить банкомат с данными: ID={atm_id}, Адрес={atm_address}, ID банка={bank_id}.")
            cursor.execute(
                "INSERT INTO ATMs (atm_id, atm_address, bank_id) VALUES (%s, %s, %s)",
                (atm_id, atm_address, bank_id)
            )
            conn.commit()
            logging.info(f"Банкомат добавлен успешно: ID={atm_id}, Адрес={atm_address}, ID банка={bank_id}.")
            messagebox.showinfo("Успех", "Банкомат добавлен!")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка добавления банкомата: {err}")
            messagebox.showerror("Ошибка", f"Не удалось добавить банкомат: {err}")
        finally:
            conn.close()
            logging.info("Соединение с базой данных закрыто после попытки добавить банкомат.")

        clear_entries([entry_atm_id, entry_atm_address, entry_bank_id_atm])
        load_data(tree_atms, "SELECT * FROM ATMs")
        logging.info("Обновлён список банкоматов после добавления нового.")

    tk.Label(tab, text="ID банкомата:").pack(pady=5)
    entry_atm_id = tk.Entry(tab)
    entry_atm_id.pack(pady=5)

    tk.Label(tab, text="Адрес банкомата:").pack(pady=5)
    entry_atm_address = tk.Entry(tab)
    entry_atm_address.pack(pady=5)

    tk.Label(tab, text="ID банка:").pack(pady=5)
    entry_bank_id_atm = tk.Entry(tab)
    entry_bank_id_atm.pack(pady=5)

    tk.Button(tab, text="Добавить банкомат", command=add_atm).pack(pady=10)
    tk.Button(tab, text="Очистить поля", command=lambda: clear_entries([entry_atm_id, entry_atm_address, entry_bank_id_atm])).pack(pady=10)

    tree_atms = ttk.Treeview(tab, columns=("ID банкомата", "Адрес банкомата", "ID банка"), show="headings")
    tree_atms.heading("ID банкомата", text="ID банкомата")
    tree_atms.heading("Адрес банкомата", text="Адрес банкомата")
    tree_atms.heading("ID банка", text="ID банка")
    tree_atms.pack(pady=20)

    logging.info("Интерфейс вкладки 'Банкоматы' создан.")
    load_data(tree_atms, "SELECT * FROM ATMs")
    logging.info("Список банкоматов загружен.")


def manage_clients(tab_clients):
    def load_clients():
        logging.info("Загрузка списка клиентов.")
        for row in tree_clients.get_children():
            tree_clients.delete(row)

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clients")
            rows = cursor.fetchall()
            logging.info(f"Загружено {len(rows)} записей из таблицы клиентов.")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка при загрузке клиентов: {err}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить список клиентов: {err}")
        finally:
            conn.close()
            logging.info("Соединение с базой данных закрыто после загрузки клиентов.")

        for row in rows:
            tree_clients.insert("", "end", values=row)

    def add_client():
        logging.info("Пользователь нажал на кнопку добавления клиента.")
        card_number = entry_card_number.get()
        client_name = entry_client_name.get()
        client_address = entry_client_address.get()
        bank_id = entry_bank_id.get()

        if not card_number or not client_name or not client_address or not bank_id:
            logging.warning("Не удалось добавить клиента: не все поля заполнены.")
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            logging.info(f"Попытка добавить клиента: Номер карты={card_number}, Имя={client_name}, Адрес={client_address}, ID банка={bank_id}.")
            cursor.execute(
                "INSERT INTO Clients (card_number, client_name, client_address, bank_id) VALUES (%s, %s, %s, %s)",
                (card_number, client_name, client_address, bank_id)
            )
            conn.commit()
            logging.info(f"Клиент успешно добавлен: Номер карты={card_number}.")
            messagebox.showinfo("Успех", "Клиент добавлен!")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка добавления клиента: {err}")
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {err}")
        finally:
            conn.close()
            logging.info("Соединение с базой данных закрыто после добавления клиента.")

        clear_entries([entry_card_number, entry_client_name, entry_client_address, entry_bank_id])
        load_clients()

    def delete_client():
        logging.info("Пользователь нажал на кнопку удаления клиента.")
        selected_item = tree_clients.selection()
        if not selected_item:
            logging.warning("Попытка удаления клиента без выбора записи.")
            messagebox.showerror("Ошибка", "Выберите запись для удаления.")
            return

        card_number = tree_clients.item(selected_item, "values")[0]
        logging.info(f"Попытка удалить клиента с номером карты {card_number}.")

        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить клиента с номером карты {card_number}?")
        if confirm:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Clients WHERE card_number = %s", (card_number,))
                conn.commit()
                logging.info(f"Клиент с номером карты {card_number} успешно удалён.")
                messagebox.showinfo("Успех", "Запись удалена!")
            except mysql.connector.Error as err:
                logging.error(f"Ошибка удаления клиента с номером карты {card_number}: {err}")
                messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {err}")
            finally:
                conn.close()
                logging.info("Соединение с базой данных закрыто после удаления клиента.")

            load_clients()

    label_card_number = tk.Label(tab_clients, text="Номер карты:")
    label_card_number.pack(pady=5)
    entry_card_number = tk.Entry(tab_clients)
    entry_card_number.pack(pady=5)

    label_client_name = tk.Label(tab_clients, text="Имя клиента:")
    label_client_name.pack(pady=5)
    entry_client_name = tk.Entry(tab_clients)
    entry_client_name.pack(pady=5)

    label_client_address = tk.Label(tab_clients, text="Адрес клиента:")
    label_client_address.pack(pady=5)
    entry_client_address = tk.Entry(tab_clients)
    entry_client_address.pack(pady=5)

    label_bank_id = tk.Label(tab_clients, text="ID банка:")
    label_bank_id.pack(pady=5)
    entry_bank_id = tk.Entry(tab_clients)
    entry_bank_id.pack(pady=5)

    button_add_client = tk.Button(tab_clients, text="Добавить клиента", command=add_client)
    button_add_client.pack(pady=10)

    button_delete_client = tk.Button(tab_clients, text="Удалить клиента", command=delete_client)
    button_delete_client.pack(pady=10)

    tree_clients = ttk.Treeview(tab_clients, columns=("Номер карты", "Имя клиента", "Адрес клиента", "ID банка"), show="headings")
    tree_clients.heading("Номер карты", text="Номер карты")
    tree_clients.heading("Имя клиента", text="Имя клиента")
    tree_clients.heading("Адрес клиента", text="Адрес клиента")
    tree_clients.heading("ID банка", text="ID банка")
    tree_clients.pack(pady=20)

    logging.info("Интерфейс вкладки 'Клиенты' создан.")
    load_clients()
    logging.info("Список клиентов загружен.")


def manage_operations(tab_operations):
    def load_operations():
        logging.info("Загрузка списка операций.")
        for row in tree_operations.get_children():
            tree_operations.delete(row)

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations")
            rows = cursor.fetchall()
            logging.info(f"Загружено {len(rows)} записей из таблицы операций.")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка при загрузке операций: {err}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить список операций: {err}")
        finally:
            conn.close()
            logging.info("Соединение с базой данных закрыто после загрузки операций.")

        for row in rows:
            tree_operations.insert("", "end", values=row)

    def add_operation():
        logging.info("Пользователь нажал на кнопку добавления операции.")
        operation_id = entry_operation_id.get()
        card_number = entry_card_number.get()
        atm_id = entry_atm_id.get()
        operation_date = entry_operation_date.get()
        operation_time = entry_operation_time.get()
        is_commission = entry_is_commission.get()
        amount = entry_amount.get()

        if not all([operation_id, card_number, atm_id, operation_date, operation_time, is_commission, amount]):
            logging.warning("Не удалось добавить операцию: не все поля заполнены.")
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            logging.info(f"Попытка добавить операцию: ID={operation_id}, Карта={card_number}, Банкомат={atm_id}, "
                         f"Дата={operation_date}, Время={operation_time}, Комиссия={is_commission}, Сумма={amount}.")
            cursor.execute(
                "INSERT INTO Operations (operation_id, card_number, atm_id, operation_date, operation_time, is_commission, amount) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (operation_id, card_number, atm_id, operation_date, operation_time, is_commission, amount)
            )
            conn.commit()
            logging.info(f"Операция успешно добавлена: ID={operation_id}.")
            messagebox.showinfo("Успех", "Операция добавлена!")
        except mysql.connector.Error as err:
            logging.error(f"Ошибка добавления операции: {err}")
            messagebox.showerror("Ошибка", f"Не удалось добавить операцию: {err}")
        finally:
            conn.close()
            logging.info("Соединение с базой данных закрыто после добавления операции.")

        clear_entries([entry_operation_id, entry_card_number, entry_atm_id, entry_operation_date, entry_operation_time, entry_is_commission, entry_amount])
        load_operations()

    def delete_operation():
        logging.info("Пользователь нажал на кнопку удаления операции.")
        selected_item = tree_operations.selection()
        if not selected_item:
            logging.warning("Попытка удаления операции без выбора записи.")
            messagebox.showerror("Ошибка", "Выберите запись для удаления.")
            return

        operation_id = tree_operations.item(selected_item, "values")[0]
        logging.info(f"Попытка удалить операцию с ID {operation_id}.")

        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить операцию с ID {operation_id}?")
        if confirm:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Operations WHERE operation_id = %s", (operation_id,))
                conn.commit()
                logging.info(f"Операция с ID {operation_id} успешно удалена.")
                messagebox.showinfo("Успех", "Запись удалена!")
            except mysql.connector.Error as err:
                logging.error(f"Ошибка удаления операции с ID {operation_id}: {err}")
                messagebox.showerror("Ошибка", f"Не удалось удалить операцию: {err}")
            finally:
                conn.close()
                logging.info("Соединение с базой данных закрыто после удаления операции.")

            load_operations()

    label_operation_id = tk.Label(tab_operations, text="ID операции:")
    label_operation_id.pack(pady=5)
    entry_operation_id = tk.Entry(tab_operations)
    entry_operation_id.pack(pady=5)

    label_card_number = tk.Label(tab_operations, text="Номер карты:")
    label_card_number.pack(pady=5)
    entry_card_number = tk.Entry(tab_operations)
    entry_card_number.pack(pady=5)

    label_atm_id = tk.Label(tab_operations, text="ID банкомата:")
    label_atm_id.pack(pady=5)
    entry_atm_id = tk.Entry(tab_operations)
    entry_atm_id.pack(pady=5)

    label_operation_date = tk.Label(tab_operations, text="Дата операции:")
    label_operation_date.pack(pady=5)
    entry_operation_date = tk.Entry(tab_operations)
    entry_operation_date.pack(pady=5)

    label_operation_time = tk.Label(tab_operations, text="Время операции:")
    label_operation_time.pack(pady=5)
    entry_operation_time = tk.Entry(tab_operations)
    entry_operation_time.pack(pady=5)

    label_is_commission = tk.Label(tab_operations, text="Комиссия (1/0):")
    label_is_commission.pack(pady=5)
    entry_is_commission = tk.Entry(tab_operations)
    entry_is_commission.pack(pady=5)

    label_amount = tk.Label(tab_operations, text="Сумма:")
    label_amount.pack(pady=5)
    entry_amount = tk.Entry(tab_operations)
    entry_amount.pack(pady=5)

    button_add_operation = tk.Button(tab_operations, text="Добавить операцию", command=add_operation)
    button_add_operation.pack(pady=10)

    button_delete_operation = tk.Button(tab_operations, text="Удалить операцию", command=delete_operation)
    button_delete_operation.pack(pady=10)

    tree_operations = ttk.Treeview(tab_operations, columns=("ID операции", "Номер карты", "ID банкомата", "Дата операции", "Время операции", "Комиссия", "Сумма"), show="headings")
    tree_operations.heading("ID операции", text="ID операции")
    tree_operations.heading("Номер карты", text="Номер карты")
    tree_operations.heading("ID банкомата", text="ID банкомата")
    tree_operations.heading("Дата операции", text="Дата операции")
    tree_operations.heading("Время операции", text="Время операции")
    tree_operations.heading("Комиссия", text="Комиссия")
    tree_operations.heading("Сумма", text="Сумма")
    tree_operations.pack(pady=20)

    logging.info("Интерфейс вкладки 'Операции' создан.")
    load_operations()
    logging.info("Список операций загружен.")


def main_window():
    root = tk.Tk()
    root.title("Управление данными")
    logging.info("Приложение запущено.")

    notebook = ttk.Notebook(root)


    tab_banks = ttk.Frame(notebook)
    tab_atms = ttk.Frame(notebook)
    tab_clients = ttk.Frame(notebook)
    tab_operations = ttk.Frame(notebook)

    notebook.add(tab_banks, text="Банки")
    notebook.add(tab_atms, text="Банкоматы")
    notebook.add(tab_clients, text="Клиенты")
    notebook.add(tab_operations, text="Операции")

    notebook.pack(expand=True, fill="both")


    manage_banks(tab_banks)
    manage_atms(tab_atms)
    manage_clients(tab_clients)
    manage_operations(tab_operations)


    root.mainloop()
    logging.info("Приложение завершено.")


if __name__ == "__main__":
    main_window()
