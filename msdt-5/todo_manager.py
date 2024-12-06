import json
from datetime import datetime

class Task:
    
    
    def __init__(self, title, due_date=None, priority='medium'):
        self.title = title
        self.completed = False
        self.created_at = datetime.now()
        self.due_date = due_date
        self.priority = priority

    def mark_completed(self):
      
        self.completed = True

    def to_dict(self):
       
        return {
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority
        }

    @classmethod
    def from_dict(cls, data):
        
        return cls(
            title=data['title'],
            due_date=datetime.fromisoformat(data['due_date']) if data['due_date'] else None,
            priority=data['priority']
        )

class TaskManager:
    
    
    def __init__(self):
        self.tasks = []

    def add_task(self, title, due_date=None, priority='medium'):
        
        task = Task(title, due_date, priority)
        self.tasks.append(task)

    def remove_task(self, title):
      
        self.tasks = [task for task in self.tasks if task.title != title]

    def mark_task_completed(self, title):
       
        for task in self.tasks:
            if task.title == title:
                task.mark_completed()
                return True
        return False

    def filter_tasks(self, completed=None, priority=None):
        
        result = self.tasks
        if completed is not None:
            result = [task for task in result if task.completed == completed]
        if priority:
            result = [task for task in result if task.priority == priority]
        return result

    def save_to_file(self, file_path):
     
        with open(file_path, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_from_file(self, file_path):
      
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []

