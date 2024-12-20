from datetime import datetime
from typing import List, Optional, Dict

class Task:
    def __init__(self, title: str, description: str, priority: int = 1):
        if not title:
            raise ValueError("Title cannot be empty")
        if priority < 1 or priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None

    def complete(self):
        self.completed = True
        self.completed_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[int] = None):
        if title is not None:
            if not title:
                raise ValueError("Title cannot be empty")
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            if priority < 1 or priority > 5:
                raise ValueError("Priority must be between 1 and 5")
            self.priority = priority

class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, title: str, description: str, priority: int = 1) -> int:
        task = Task(title, description, priority)
        task_id = self._next_id
        self.tasks[task_id] = task
        self._next_id += 1
        return task_id

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, 
                    description: Optional[str] = None, priority: Optional[int] = None) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.update(title, description, priority)
        return True

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.complete()
        return True

    def delete_task(self, task_id: int) -> bool:
        if task_id not in self.tasks:
            return False
        del self.tasks[task_id]
        return True

    def get_all_tasks(self) -> List[tuple[int, Task]]:
        return [(task_id, task) for task_id, task in self.tasks.items()]

    def get_completed_tasks(self) -> List[tuple[int, Task]]:
        return [(task_id, task) for task_id, task in self.tasks.items() if task.completed]

    def get_pending_tasks(self) -> List[tuple[int, Task]]:
        return [(task_id, task) for task_id, task in self.tasks.items() if not task.completed]