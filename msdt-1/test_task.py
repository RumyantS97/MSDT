from task import Task


def test_task_creation():
    # Тест для создаиня задачи
    task = Task("Test Task", "This is a test task.")
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
    assert task.completed is False


def test_edit_task():
    # Тест для редактирования задачи
    task = Task("Test Task", "This is a test task.")
    task.edit("Updated Task", "Updated description.")
    assert task.title == "Updated Task"
    assert task.description == "Updated description."


def test_mark_task_completed():
    # Тест для маркировки задачи
    task = Task("Test Task", "This is a test task.")
    task.mark_completed()
    assert task.completed is True
