from task import Task
from storage import Storage

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.storage = Storage()
        self.load_tasks()

    def load_tasks(self):
        # загрузка задач из файла
        self.tasks = self.storage.load()

    def save_tasks(self):
        # сохранение задач в файла
        self.storage.save(self.tasks)

    def add_task(self, title, description):
        # добавить новую задачу
        new_task = Task(title, description)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Задача '{title}' добавлена.")

    def view_tasks(self):
        # все задачи вывести
        if not self.tasks:
            print("Список задач пуст.")
        else:
            for task in self.tasks:
                print(task)

    def edit_task(self, task_id, title, description):
        # редактор
        task = self.by_id(task_id)
        if task:
            task.edit(title, description)
            self.save_tasks()
            print(f"Задача '{task_id}' отредактирована.")
        else:
            print(f"Задача с ID '{task_id}' не найдена.")

    def delete_task(self, task_id):
        # удаление
        task = self.by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Задача '{task_id}' удалена.")
        else:
            print(f"Задача с ID '{task_id}' не найдена.")

    # маркировка
    def mark_task_completed(self, task_id):
        task = self.by_id(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            print(f"Задача '{task_id}' отмечена как выполненная.")
        else:
            print(f"Задача с ID '{task_id}' не найдена.")

    def by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None