import asyncio
import random
from datetime import datetime, timedelta

class Task:
    """
    Represents a task, assigned worker, ID, and optional deadline.
    
    """
    
    def __init__(self, title: str, worker: str, task_id: int, deadline: datetime = None):
        self.title = title
        self.worker = worker
        self.task_id = task_id
        self.deadline = deadline
        self.created_at = datetime.now()
        self.status = "pending"

    def __str__(self) -> str:
        """Returns a string representation of the task.

        :return: string representation of the task.
        """
        deadline_str = self.deadline.strftime("%Y-%m-%d %H:%M") if self.deadline else "No deadline"
        return (f"[{self.worker}] Task ID: {self.task_id}, {self.title} "
                f"({self.status}, Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}, "
                f"Deadline: {deadline_str})" )


class TaskManager:
    """
    Manages a list of tasks, providing methods to add, remove, list, and update tasks.

    """
    def __init__(self):
        self.tasks = {}  
        self.next_task_id = 1

    async def add_task(self, title: str, worker: str, deadline: datetime = None) -> int:
        """
        Adds a new task to the task list.

        :param title: title of the task.
        :param worker: worker assigned to the task.
        :param deadline: deadline for the task.
        :return: ID of the newly added task.
        """
        # Simulate an asynchronous operation
        await asyncio.sleep(random.uniform(0, 1))
        task_id = self.next_task_id
        self.next_task_id += 1
        task = Task(title, worker, task_id, deadline)
        self.tasks[task_id] = task
        print(f"Task added: {task}")
        return task_id

    async def remove_task(self, task_id: int) -> None:
        """
        Removes a task from the task list by its ID.

        :param task_id: ID of the task to remove.
        """
        await asyncio.sleep(random.uniform(0, 1))
        if task_id in self.tasks:
            removed_task = self.tasks.pop(task_id)
            print(f"Task removed: {removed_task}")
        else:
            print(f"Task with ID {task_id} not found")

    async def list_tasks(self, worker: str = None) -> None:
        """
        Lists all tasks, optionally filtered by worker.

        """
        await asyncio.sleep(random.uniform(0, 1))
        print("Listing tasks:")
        for task in self.tasks.values():
            if worker is None or task.worker == worker:
                print(task)

    async def set_deadline(self, task_id: int, deadline: datetime) -> None:
        """
        Sets or updates the deadline for a task.

        :param task_id: ID of the task to update.
        :param deadline: new deadline for the task.
        """
        await asyncio.sleep(random.uniform(0, 1)) 
        if task_id in self.tasks:
            self.tasks[task_id].deadline = deadline
            print(f"Deadline updated for task: {self.tasks[task_id]}")
        else:
            print(f"Task with ID {task_id} not found")

    async def update_task_status(self, task_id: int, status: str):
        """
        Sets or updates the status for a task.

        :param task_id: ID of the task to update.
        :param status: new status for the task.
        """
        await asyncio.sleep(random.uniform(0, 1))
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            print(f"Task {task_id} status updated to: {status}")
        else:
            print(f"Task with ID {task_id} not found")



async def worker_interaction(task_manager: TaskManager, worker: str) -> None:
    """
    Represents a worker interacting with the task manager.

    :param task_manager: task manager instance.
    :param worker: name of the worker.
    """
    print(f"Worker {worker} starts interaction")
    task_id = await task_manager.add_task(f"Worker {worker} started a task", worker)
    await task_manager.add_task("Complete project", worker, datetime.now() + timedelta(days=2))
    await task_manager.list_tasks(worker)
    await task_manager.set_deadline(task_id, datetime.now() + timedelta(hours=5))
    await asyncio.sleep(1) 
    await task_manager.update_task_status(task_id, "in progress")
    await asyncio.sleep(2)
    await task_manager.update_task_status(task_id, "completed")
    await task_manager.remove_task(task_id)
    await task_manager.list_tasks(worker)


async def main():
    """
    Main function to run the task manager.
    
    """
    task_manager = TaskManager()
    workers = ["NameA", "NameB", "NameC"]
    await asyncio.gather(*(worker_interaction(task_manager, worker) for worker in workers))


asyncio.run(main())
