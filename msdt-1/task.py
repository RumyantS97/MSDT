import uuid


class Task:
    def __init__(self, title, description):
        # Уникальный идентификатор для каждой задачи
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.completed = False

    def edit(self, title, description):
        # Редактор задач
        self.title = title
        self.description = description

    def mark_completed(self):
        # Отметить задачу выполненной
        self.completed=True

    def __str__(self):
        if self.completed:
            status = "Выполнено"
        else:
            status = "Не выполнено"
        return f"[{self.id}] {self.title}: {self.description} ({status})"