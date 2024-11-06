import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import HIDDEN, NORMAL
from tkcalendar import Calendar  # Импорт для календаря


class Task:
 def __init__(self, title, description, due_date):
  self.title = title
  self.description = description
  self.due_date = due_date
  self.completed = False
  self.priority = "Нормальный"
  self.on_hold = False
  self.comments = []

 def set_priority(self, priority):
  """Устанавливает приоритет задачи."""
  if priority in ["Высокий","Нормальный","Низкий"]:
   self.priority=priority
  else:
   raise ValueError("Недопустимый приоритет")

 def mark_as_completed(self):
  """Отмечает задачу как завершённую."""
  self.completed=True

 def __str__(self):
  """Возвращает строковое представление задачи."""
  status = "Завершено" if self.completed else "В процессе"
  hold_status = "На паузе" if self.on_hold else "Активно"
  comments = "\n  Комментарии: " + ";".join(self.comments) if self.comments else ""
  return f"{self.title} - {self.description} (Срок: {self.due_date}, Статус: {status}, Приоритет: {self.priority}, Состояние: {hold_status}){comments}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def hold_task(self, title):
        """Приостанавливает задачу по названию."""
        for task in self.tasks:
            if task.title == title:
                task.on_hold = True
                return f"Задача '{title}' приостановлена."
        return f"Задача '{title}' не найдена."

    def resume_task(self, title):
        """Возобновляет задачу по названию."""
        for task in self.tasks:
            if task.title == title:
                task.on_hold = False
                return f"Задача '{title}' возобновлена."
        return f"Задача '{title}' не найдена."

    def sort_tasks_by_priority(self):
        """Сортирует задачи по приоритету."""
        self.tasks.sort(key=lambda task: {"Высокий": 1, "Нормальный": 2, "Низкий": 3}[task.priority])
        return "Задачи отсортированы по приоритету."

    def sort_tasks_by_due_date(self):
        """Сортирует задачи по дате завершения."""
        self.tasks.sort(key=lambda task: task.due_date)
        return "Задачи отсортированы по дате завершения."

    def add_comment_to_task(self, title, comment):
        """Добавляет комментарий к задаче."""
        for task in self.tasks:
            if task.title == title:
                task.comments.append(comment)
                return f"Комментарий добавлен к задаче '{title}'."
        return f"Задача '{title}' не найдена."

    def add_task(self, title, description, due_date, priority):
        """Добавляет новую задачу."""
        task = Task(title, description, due_date)
        task.set_priority(priority)
        self.tasks.append(task)
        return f"Задача '{title}' добавлена с приоритетом '{priority}'."

    def list_tasks(self):
        """Возвращает список задач."""
        if not self.tasks:
            return "Список задач пуст."
        return "\n".join([f"- {task}" for task in self.tasks])

    def mark_task_as_completed(self, title):
        """Отмечает задачу как завершённую по названию."""
        for task in self.tasks:
            if task.title == title:
                task.mark_as_completed()
                return f"Задача '{title}' отмечена как завершённая."
        return f"Задача '{title}' не найдена."

    def delete_task(self, title):
        """Удаляет задачу по названию."""
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return f"Задача '{title}' удалена."
        return f"Задача '{title}' не найдена."

    def search_task(self, keyword):
        """Ищет задачу по ключевому слову."""
        results = [task for task in self.tasks if keyword.lower() in task.title.lower()]
        if not results:
            return f"Задачи с ключевым словом '{keyword}' не найдены."
        return "\n".join([f"- {task}" for task in results])


class TaskManagerApp(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("Менеджер задач с Котиком")
        self.configure(bg="#f4f4f9")
        self.geometry("1000x800")  # Увеличенный размер окна
        self.priority_var = tk.StringVar(value="Нормальный")  # Переменная для приоритета
        self.create_widgets()
        self.create_pet()

    def create_widgets(self):
        """Создаёт виджеты приложения."""
        self.title_label = tk.Label(self, text="Менеджер задач", font=("Arial", 20, "bold"), bg="#f4f4f9", fg="#333")
        self.title_label.pack(pady=10)

        self.task_list = tk.Text(self, height=10, width=80, wrap="word", font=("Arial", 10))
        self.task_list.pack(pady=10)
        self.task_list.config(state=tk.DISABLED)

        self.show_tasks()

        button_frame = tk.Frame(self, bg="#f4f4f9")
        button_frame.pack(pady=10)

        self.add_task_button = tk.Button(button_frame, text="Добавить задачу", command=self.open_add_task_window, bg="#4CAF50", fg="white", width=25)
        self.add_task_button.grid(row=0, column=0, padx=5, pady=5)

        self.show_tasks_button = tk.Button(button_frame, text="Показать все задачи", command=self.show_tasks, bg="#2196F3", fg="white", width=25)
        self.show_tasks_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_task_button = tk.Button(button_frame, text="Удалить задачу", command=self.delete_task, bg="#F44336", fg="white", width=25)
        self.delete_task_button.grid(row=1, column=0, padx=5, pady=5)

        self.complete_task_button = tk.Button(button_frame, text="Завершить задачу", command=self.complete_task, bg="#9C27B0", fg="white", width=25)
        self.complete_task_button.grid(row=1, column=1, padx=5, pady=5)

        self.search_task_button = tk.Button(button_frame, text="Поиск задачи", command=self.search_task, bg="#FF9800", fg="white", width=25)
        self.search_task_button.grid(row=2, column=0, padx=5, pady=5)

        self.hold_task_button = tk.Button(button_frame, text="Приостановить задачу", command=self.hold_task,
                                          bg="#FF6347", fg="white", width=25)
        self.hold_task_button.grid(row=2, column=1, padx=5, pady=5)

        self.resume_task_button = tk.Button(button_frame, text="Возобновить задачу", command=self.resume_task,
                                            bg="#32CD32", fg="white", width=25)
        self.resume_task_button.grid(row=3, column=0, padx=5, pady=5)

        self.sort_priority_button = tk.Button(button_frame, text="Сортировать по приоритету",
                                              command=self.sort_by_priority, bg="#8B0000", fg="white", width=25)
        self.sort_priority_button.grid(row=3, column=1, padx=5, pady=5)

        self.sort_due_date_button = tk.Button(button_frame, text="Сортировать по дате", command=self.sort_by_due_date,
                                              bg="#1E90FF", fg="white", width=25)
        self.sort_due_date_button.grid(row=4, column=0, padx=5, pady=5)

        self.add_comment_button = tk.Button(button_frame, text="Добавить комментарий", command=self.add_comment,
                                            bg="#FFD700", fg="black", width=25)
        self.add_comment_button.grid(row=4, column=1, padx=5, pady=5)

    def create_pet(self):
        self.canvas = tk.Canvas(self, width=200, height=100, bg="lightgreen",
                                highlightthickness=0)  # Размеры холста остаются уменьшенными
        self.canvas.pack(anchor="n", padx=10, pady=10)  # Изменён якорь на "n" (север) и добавлен отступ

        self.canvas.body_color = "magenta"

        # Параметры питомца остаются без изменений
        self.body = self.canvas.create_oval(10, 5, 190, 95, outline=self.canvas.body_color, fill=self.canvas.body_color)
        self.ear_left = self.canvas.create_polygon(30, 0, 30, 15, 15, 5, outline=self.canvas.body_color,
                                                   fill=self.canvas.body_color)
        self.ear_right = self.canvas.create_polygon(170, 0, 170, 15, 185, 5, outline=self.canvas.body_color,
                                                    fill=self.canvas.body_color)
        self.eye_left = self.canvas.create_oval(40, 35, 55, 50, outline="black", fill="white")
        self.pupil_left = self.canvas.create_oval(45, 40, 50, 45, outline="black", fill="black")
        self.eye_right = self.canvas.create_oval(145, 35, 160, 50, outline="black", fill="white")
        self.pupil_right = self.canvas.create_oval(150, 40, 155, 45, outline="black", fill="black")
        self.mouth_normal = self.canvas.create_line(60, 75, 100, 85, 140, 75, smooth=1, width=2)
        self.mouth_happy = self.canvas.create_line(60, 75, 100, 95, 140, 75, smooth=1, width=2, state=HIDDEN)
        self.cheek_left = self.canvas.create_oval(35, 65, 45, 75, outline="pink", fill="pink", state=HIDDEN)
        self.cheek_right = self.canvas.create_oval(155, 65, 165, 75, outline="pink", fill="pink", state=HIDDEN)

        self.toggle_eyes()
        self.canvas.bind('<Motion>', self.show_happy)
        self.canvas.bind('<Leave>', self.hide_happy)

    def sort_by_priority(self):
        result = self.task_manager.sort_tasks_by_priority()
        messagebox.showinfo("Результат", result)
        self.show_tasks()

    def sort_by_due_date(self):
        result = self.task_manager.sort_tasks_by_due_date()
        messagebox.showinfo("Результат", result)
        self.show_tasks()

    def add_comment(self):
        title = simpledialog.askstring("Добавить комментарий", "Введите название задачи:")
        if title:
            comment = simpledialog.askstring("Комментарий", "Введите комментарий:")
            if comment:
                result = self.task_manager.add_comment_to_task(title, comment)
                messagebox.showinfo("Результат", result)
                self.show_tasks()

    def toggle_eyes(self):
        current_color = self.canvas.itemcget(self.eye_left, 'fill')
        new_color = self.canvas.body_color if current_color == "white" else "white"
        current_state = self.canvas.itemcget(self.pupil_left, 'state')
        new_state = NORMAL if current_state == HIDDEN else HIDDEN

        self.canvas.itemconfigure(self.pupil_left, state=new_state)
        self.canvas.itemconfigure(self.pupil_right, state=new_state)
        self.canvas.itemconfigure(self.eye_left, fill=new_color)
        self.canvas.itemconfigure(self.eye_right, fill=new_color)
        self.after(500, self.toggle_eyes)

    def show_happy(self, event):
        if 35 < event.x < 265 and 20 < event.y < 250:
            self.canvas.itemconfigure(self.cheek_left, state=NORMAL)
            self.canvas.itemconfigure(self.cheek_right, state=NORMAL)
            self.canvas.itemconfigure(self.mouth_happy, state=NORMAL)
            self.canvas.itemconfigure(self.mouth_normal, state=HIDDEN)

    def hide_happy(self, event):
        self.canvas.itemconfigure(self.cheek_left, state=HIDDEN)
        self.canvas.itemconfigure(self.cheek_right, state=HIDDEN)
        self.canvas.itemconfigure(self.mouth_happy, state=HIDDEN)
        self.canvas.itemconfigure(self.mouth_normal, state=NORMAL)

    def open_add_task_window(self):
        add_task_window = tk.Toplevel(self)
        add_task_window.title("Добавить задачу")
        add_task_window.geometry("500x500")  # Увеличенный размер окна для ввода задачи

        tk.Label(add_task_window, text="Название задачи:").pack(pady=5)
        title_entry = tk.Entry(add_task_window, width=50)
        title_entry.pack(pady=5)

        tk.Label(add_task_window, text="Описание задачи:").pack(pady=5)
        description_entry = tk.Entry(add_task_window, width=50)
        description_entry.pack(pady=5)

        tk.Label(add_task_window, text="Дата завершения:").pack(pady=5)
        calendar = Calendar(add_task_window, selectmode="day")
        calendar.pack(pady=5)

        tk.Label(add_task_window, text="Приоритет:").pack(pady=5)
        priority_frame = tk.Frame(add_task_window)
        priority_frame.pack(pady=5)
        tk.Radiobutton(priority_frame, text="Высокий", variable=self.priority_var, value="Высокий").pack(side=tk.LEFT)
        tk.Radiobutton(priority_frame, text="Нормальный", variable=self.priority_var, value="Нормальный").pack(side=tk.LEFT)
        tk.Radiobutton(priority_frame, text="Низкий", variable=self.priority_var, value="Низкий").pack(side=tk.LEFT)

        tk.Button(add_task_window, text="Добавить", command=lambda: self.add_task(title_entry, description_entry, calendar)).pack(pady=10)

    def add_task(self, title_entry, description_entry, calendar):
        title = title_entry.get()
        description = description_entry.get()
        due_date = calendar.get_date()  # Получаем дату в формате MM/DD/YY
        due_date = datetime.datetime.strptime(due_date, "%m/%d/%y").strftime("%Y-%m-%d")

        priority = self.priority_var.get()

        try:
            # Преобразуем дату из строки в объект date с использованием формата "YYYY-MM-DD"
            due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            result = self.task_manager.add_task(title, description, due_date, priority)
            messagebox.showinfo("Успех", result)
            self.show_tasks()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты.")

    def show_tasks(self):
        self.task_list.config(state=tk.NORMAL)
        self.task_list.delete(1.0, tk.END)
        self.task_list.insert(tk.END, self.task_manager.list_tasks())
        self.task_list.config(state=tk.DISABLED)

    def delete_task(self):
        title = simpledialog.askstring("Удалить задачу", "Введите название задачи:")
        if title:
            result = self.task_manager.delete_task(title)
            messagebox.showinfo("Результат", result)
            self.show_tasks()

    def complete_task(self):
        title = simpledialog.askstring("Завершить задачу", "Введите название задачи:")
        if title:
            result = self.task_manager.mark_task_as_completed(title)
            messagebox.showinfo("Результат", result)
            self.show_tasks()

    def search_task(self):
        keyword = simpledialog.askstring("Поиск задачи", "Введите ключевое слово для поиска:")
        if keyword:
            result = self.task_manager.search_task(keyword)
            messagebox.showinfo("Результат поиска", result)

    def hold_task(self):
        title = simpledialog.askstring("Приостановить задачу", "Введите название задачи:")
        if title:
            result = self.task_manager.hold_task(title)
            messagebox.showinfo("Результат", result)
            self.show_tasks()

    def resume_task(self):
        title = simpledialog.askstring("Возобновить задачу", "Введите название задачи:")
        if title:
            result = self.task_manager.resume_task(title)
            messagebox.showinfo("Результат", result)
            self.show_tasks()


if __name__ == "__main__":
    task_manager = TaskManager()
    app = TaskManagerApp(task_manager)
    app.mainloop()
