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

def test_load_task_from_file_with_data():
    mock_data = json.dumps([
        {
            "title": "Loaded Task",
            "completed": False,
            "created_at": "2024-12-15T12:00:00",
            "due_date": None,
            "priority": "medium"
        }
    ])
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        manager = TaskManager()
        manager.load_from_file("mock_file.json")

    assert len(manager.tasks) == 1
    task = manager.tasks[0]
    assert task.title == "Loaded Task"
    assert not task.completed
    assert task.due_date is None
    assert task.priority == "medium"


