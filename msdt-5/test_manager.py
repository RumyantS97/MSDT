from todo_manager import TaskManager, Task
import pytest
import json
from datetime import datetime
from unittest.mock import mock_open, patch

def test_add_task():
    manager = TaskManager()
    manager.add_task("Test Task")
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Test Task"
    assert not manager.tasks[0].completed

def test_remove_task():
    manager = TaskManager()
    manager.add_task("Test Task")
    manager.remove_task("Test Task")
    assert len(manager.tasks) == 0

def test_mark_task_completed():
    manager = TaskManager()
    manager.add_task("Test Task")
    manager.mark_task_completed("Test Task")
    assert manager.tasks[0].completed

def test_filter_tasks_by_completion():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.mark_task_completed("Task 1")
    completed_tasks = manager.filter_tasks(completed=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Task 1"


def test_filter_tasks_by_priority():
    manager = TaskManager()
    manager.add_task("Task 1", priority="high")
    manager.add_task("Task 2", priority="low")
    high_priority_tasks = manager.filter_tasks(priority="high")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0].priority == "high"



@pytest.mark.parametrize("title, due_date, priority", [
    ("Task 1", None, "medium"),
    ("Task 2", "2024-12-31", "high"),
    ("Task 3", None, "low")
])
def test_add_task_parametrized(title, due_date, priority):
    manager = TaskManager()
    manager.add_task(title, due_date, priority)
    task = manager.tasks[-1]
    assert task.title == title
    assert task.priority == priority
    assert (task.due_date is not None) == (due_date is not None)


@pytest.mark.parametrize(
    "title, due_date, priority, expected_title, expected_due_date, expected_priority",
    [
        ("Task 1", datetime(2024, 12, 6), "high", "Task 1", "2024-12-06T00:00:00", "high"),
        ("Task 2", datetime(2024, 12, 7), "medium", "Task 2", "2024-12-07T00:00:00", "medium"),
        ("Task 3", None, "low", "Task 3", "null", "low"),
    ]
)
def test_save_and_load_tasks_with_mock_parametrized(title, due_date, priority, expected_title, expected_due_date, expected_priority):
    # Создаем TaskManager и добавляем задачу
    manager = TaskManager()
    manager.add_task(title, due_date=due_date, priority=priority)
    
    # Мокаем open() и проверяем сохранение задач в файл
    with patch("builtins.open", mock_open()) as mocked_file:
        # Сохраняем задачи в файл
        manager.save_to_file("mocked_file.json")
        
        # Проверяем, что файл был открыт в режиме записи
        mocked_file.assert_called_once_with("mocked_file.json", "w")
        
        # Получаем записанные данные
        written_data = mocked_file().write.call_args[0][0]
        
        # Проверяем, что данные содержат ожидаемые значения
        assert f'"title": "{expected_title}"' in written_data
        assert f'"priority": "{expected_priority}"' in written_data
        assert f'"due_date": "{expected_due_date}"' in written_data
