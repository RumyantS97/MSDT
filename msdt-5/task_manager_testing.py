import pytest
from datetime import datetime
from unittest.mock import patch
from task_manager import Task, TaskManager

@pytest.fixture
def task_manager():
    return TaskManager()

def test_task_creation():
    task = Task("Test Task", "Test Description", 3)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == 3
    assert not task.completed
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None

def test_task_invalid_priority():
    with pytest.raises(ValueError):
        Task("Test Task", "Test Description", 6)
    with pytest.raises(ValueError):
        Task("Test Task", "Test Description", 0)

def test_empty_title():
    with pytest.raises(ValueError):
        Task("", "Test Description", 3)

@pytest.mark.parametrize("title,description,priority", [
    ("Task 1", "Description 1", 1),
    ("Task 2", "Description 2", 3),
    ("Task 3", "Description 3", 5)
])
def test_add_multiple_tasks(task_manager, title, description, priority):
    task_id = task_manager.add_task(title, description, priority)
    task = task_manager.get_task(task_id)
    assert task.title == title
    assert task.description == description
    assert task.priority == priority

def test_complete_task(task_manager):
    task_id = task_manager.add_task("Test Task", "Test Description")
    
    with patch('task_manager.datetime') as mock_datetime:
        mock_now = datetime(2023, 1, 1, 12, 0)
        mock_datetime.now.return_value = mock_now
        
        task_manager.complete_task(task_id)
        task = task_manager.get_task(task_id)
        
        assert task.completed
        assert task.completed_at == mock_now

def test_delete_task(task_manager):
    task_id = task_manager.add_task("Test Task", "Test Description")
    assert task_manager.delete_task(task_id)
    assert task_manager.get_task(task_id) is None

def test_update_task(task_manager):
    task_id = task_manager.add_task("Test Task", "Test Description", 1)
    task_manager.update_task(task_id, title="Updated Task", priority=4)
    task = task_manager.get_task(task_id)
    assert task.title == "Updated Task"
    assert task.priority == 4
    assert task.description == "Test Description"

def test_get_filtered_tasks(task_manager):
    task1_id = task_manager.add_task("Task 1", "Description 1")
    task2_id = task_manager.add_task("Task 2", "Description 2")
    task3_id = task_manager.add_task("Task 3", "Description 3")
    
    task_manager.complete_task(task1_id)
    task_manager.complete_task(task2_id)
    
    completed = task_manager.get_completed_tasks()
    pending = task_manager.get_pending_tasks()
    
    assert len(completed) == 2
    assert len(pending) == 1
    assert pending[0][0] == task3_id