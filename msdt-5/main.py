import json

from datetime import datetime


class Task:
    def __init__(self, description, priority=1, due_date=None, tags=None, completed=False) -> None:
        """
        Инициализирует задачу с указанным описанием, приоритетом, датой выполнения, тегами и статусом выполнения.
        :param description: Описание задачи
        :param priority: Приоритет задачи (по умолчанию 1)
        :param due_date: Дата выполнения задачи (по умолчанию None)
        :param tags: Теги задачи (по умолчанию None)
        :param completed: Статус выполнения задачи (по умолчанию False)
        """
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.tags = tags
        self.completed = completed

    def complete(self) -> None:
        """
            Помечает задачу как выполненную.
        """
        self.completed = True

    def is_overdue(self) -> bool:
        """
            Проверяет, просрочена ли задача.
            :return: True, если задача просрочена, иначе False
        """
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False

    def add_tag(self, tag) -> None:
        """
            Добавляет тег к задаче.
            :param tag: Тег для добавления
        """
        self.tags.add(tag)

    def remove_tag(self, tag) -> None:
        """
           Удаляет тег из задачи.
           :param tag: Тег для удаления
        """
        self.tags.discard(tag)

    def __str__(self) -> str:
        """
            Возвращает строковое представление задачи.
            :return: Строковое представление задачи
        """
        status = '✓' if self.completed else ' '
        overdue = ' (overdue)' if self.is_overdue() else ''
        return f"{status} {self.description} (Priority: {self.priority}){overdue}"


class TaskList:
    def __init__(self) -> None:
        """
           Инициализирует список задач.
        """
        self.tasks = []

    def add_task(self, description, priority=1, tags=None) -> None:
        """
           Добавляет новую задачу в список.
           :param description: Описание задачи
           :param priority: Приоритет задачи (по умолчанию 1)
           :param tags: Теги задачи (по умолчанию None)
        """
        task = Task(description, priority)
        if tags:
            task.tags = tags
        self.tasks.append(task)

    def remove_task(self, task_index) -> None:
        """
           Удаляет задачу из списка по индексу.
           :param task_index: Индекс задачи для удаления
        """
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

    def complete_task(self, task_index) -> None:
        """
           Помечает задачу как выполненную по индексу.
           :param task_index: Индекс задачи для пометки как выполненной
        """
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True

    def display_tasks(self) -> None:
        """
          Выводит все задачи из списка.
        """
        if self.tasks:
            for i, task in enumerate(self.tasks):
                print(f"{i + 1}. {task}")
        else:
            print("No tasks in the list")

    def save_to_file(self, filename) -> None:
        """
           Сохраняет список задач в файл.
           :param filename: Имя файла для сохранения
        """
        with open(filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.priority},{task.completed}\n")

    def load_from_file(self, filename) -> None:
        """
          Загружает список задач из файла.
          :param filename: Имя файла для загрузки
        """
        with open(filename, 'r') as file:
            for line in file:
                description, priority, completed = line.strip().split(',')
                task = Task(description, int(priority))
                task.completed = bool(completed)
                self.tasks.append(task)

    def filter_tasks(self, completed=False, overdue=False) -> list:
        """
           Фильтрует список задач по статусу выполнения и просроченности.
           :param completed: Флаг фильтрации по выполненным задачам
           :param overdue: Флаг фильтрации по просроченным задачам
           :return: Отфильтрованный список задач
        """
        if completed:
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif overdue:
            filtered_tasks = [task for task in self.tasks if task.is_overdue()]
        else:
            filtered_tasks = [task for task in self.tasks if not task.completed and not task.is_overdue()]
        return filtered_tasks

    def filter_by_tag(self, tag) -> list:
        """
           Фильтрует список задач по указанному тегу.
           :param tag: Тег для фильтрации
           :return: Отфильтрованный список задач
        """
        return [task for task in self.tasks if task.tags is not None and tag in task.tags]

    def save_to_json(self, filename) -> None:
        """
           Сохраняет список задач в JSON файл.
           :param filename: Имя файла для сохранения
        """
        with open(filename, 'w') as file:
            data = {
                "tasks": [vars(task) for task in self.tasks]
            }
            json.dump(data, file, indent=4)

    def load_from_json(self, filename) -> None:
        """
           Загружает список задач из JSON файла.
           :param filename: Имя файла для загрузки
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            self.tasks = [Task(**task_data) for task_data in data["tasks"]]


def main():
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2)
    task_list.add_task("Read a book")
    task_list.add_task("Call mom", priority=3)
    task_list.display_tasks()
    task_list.complete_task(0)
    task_list.remove_task(1)
    print("\nAfter completing a task and removing one:")
    task_list.display_tasks()
    task_list.save_to_file("tasks.txt")
    new_task_list = TaskList()
    new_task_list.load_from_file("tasks.txt")
    print("\nLoaded from file:")
    new_task_list.display_tasks()


if __name__ == "__main__":
    main()