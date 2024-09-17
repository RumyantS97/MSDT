from task_manager import TaskManager
from utils import display_main_menu

def main():

    task_manager = TaskManager()

    while True:
        display_main_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            task_manager.add_task(title, description)
        elif choice == '2':
            task_manager.view_tasks()
        elif choice == '3':
            task_id = input("Введите ID задачи для редактирования: ")
            title = input("Введите новое название задачи: ")
            description = input("Введите новое описание задачи: ")
            task_manager.edit_task(task_id, title, description)
        elif choice == '4':
            task_id = input("Введите ID задачи для удаления: ")
            task_manager.delete_task(task_id)
        elif choice == '5':
            task_id = input("Введите ID задачи для отметки выполнения: ")
            task_manager.mark_task_completed(task_id)
        elif choice == '6':
            print("Выход")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()