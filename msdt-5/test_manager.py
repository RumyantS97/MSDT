from todo_manager import TaskManager, Task
import pytest
import json
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


def test_save_and_load_tasks_with_mock():
    manager = TaskManager()
    manager.add_task("Task 1", due_date=datetime(2024, 12, 6), priority="high")
    
    with patch("builtins.open", mock_open()) as mocked_file:
        manager.save_to_file("mocked_file.json")
        
       
        mocked_file.assert_called_once_with("mocked_file.json", "w")
        

        written_data = mocked_file().write.call_args[0][0]
        
        assert '"title": "Task 1"' in written_data
        assert '"priority": "high"' in written_data
        assert '"due_date": "2024-12-06T00:00:00"' in written_data
