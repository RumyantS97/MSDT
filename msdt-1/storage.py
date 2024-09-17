import json
from task import Task

class Storage:
    def __init__(self,filename='tasks.json'):
        self.filename=filename

    def save(self,tasks):
        # сохранение задач в файла
        with open(self.filename, 'w', encoding='utf-8') as file:
            data = [{'id': task.id,'title': task.title,'description': task.description,'completed': task.completed} for task in tasks]
            json.dump(data,file,ensure_ascii=False,indent=4)
    def load(self):
        #загрузка задач из файла
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                tasks=[]
                for task_data in data:
                    task = Task(task_data['title'],task_data['description'])
                    task.id = task_data['id']
                    task.completed = task_data['completed']
                    tasks.append(task)
                return tasks
        except FileNotFoundError:
            return []