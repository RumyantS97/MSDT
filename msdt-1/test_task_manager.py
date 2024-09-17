import pytest
from unittest.mock import MagicMock
from task_manager import TaskManager
from task import Task
@pytest.fixture
def task_manager():
    manager = TaskManager()
    manager.storage = MagicMock()
    manager.load_tasks = MagicMock()# Подмена сохранения и загрузки
    manager.save_tasks = MagicMock()
    return manager

def test_add_task(task_manager):# Тест для добавления задачи
    task_manager.add_task("Task 1", "Description 1")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Task 1"

def test_edit_task(task_manager):# Тест для редактора задачи
    task = Task("Task 1", "Description 1")
    task_manager.tasks.append(task)
    task_manager.edit_task(task.id, "Updated Task", "Updated Description")
    assert task_manager.tasks[0].title == "Updated Task"
    assert task_manager.tasks[0].description == "Updated Description"

def test_delete_task(task_manager):# Тест для удаления задачи
    task = Task("Task 1", "Description 1")
    task_manager.tasks.append(task)
    task_manager.delete_task(task.id)
    assert len(task_manager.tasks) == 0

def test_mark_task_completed(task_manager):# Тест для маркировки задачи
    task = Task("Task 1", "Description 1")
    task_manager.tasks.append(task)
    task_manager.mark_task_completed(task.id)
    assert task_manager.tasks[0].completed is True