import pytest

from main import TaskList


@pytest.fixture
def task_list() -> TaskList:
    """
        функция для создания экземпляра TaskList
        :return: TaskList
    """
    return TaskList()


def test_add_task() -> None:
    """
        Тест добавления задачи в список задач.
    """
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2)
    assert len(task_list.tasks) == 1


def test_remove_task() -> None:
    """
       Тест удаления задачи из списка задач.
    """
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2)
    task_list.remove_task(0)
    assert len(task_list.tasks) == 0


def test_complete_task() -> None:
    """
        Тест завершения задачи в списке задач.
    """
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2)
    task_list.complete_task(0)
    assert task_list.tasks[0].completed is True


def test_save_and_load_from_file(tmp_path) -> None:
    """
        Тест сохранения и загрузки списка задач из файла.
        :param tmp_path: Путь к файлу
    """
    file_path = tmp_path / "tasks.txt"
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2)
    task_list.save_to_file(file_path)
    new_task_list = TaskList()
    new_task_list.load_from_file(file_path)
    assert len(new_task_list.tasks) == 1
    assert new_task_list.tasks[0].description == "Buy groceries"


@pytest.mark.parametrize("completed, overdue, expected_count", [
    (True, False, 1),
    (False, True, 0),
    (False, False, 1)
])
def test_filter_tasks(completed, overdue, expected_count) -> None:
    """
        Тест для фильтрации задач на основе статуса завершения и просрочки.
        :param completed: выполненные задачи
        :param overdue: просроченные задачи
        :param expected_count: ожидаемое значение

    """
    task_list = TaskList()
    task_list.add_task("Test task 1", priority=2)
    task_list.add_task("Test task 2")
    task_list.complete_task(0)

    filtered_tasks = task_list.filter_tasks(completed=completed, overdue=overdue)
    assert len(filtered_tasks) == expected_count


@pytest.mark.parametrize("tag, expected_count", [
    ("work", 2),
    ("personal", 2),
    ("shopping", 0)
])
def test_filter_by_tag(tag, expected_count) -> None:
    """
        Тест на фильтрацию задач по определенному тегу.
        :param tag: тэг
        :param expected_count: ожидаемое значение
    """
    task_list = TaskList()
    task_list.add_task("Test task 1", priority=2, tags=["work"])
    task_list.add_task("Test task 2", tags=["personal"])
    task_list.add_task("Test task 3", tags=["work", "personal"])

    filtered_tasks = task_list.filter_by_tag(tag)
    assert len(filtered_tasks) == expected_count


def test_save_and_load_from_json(tmp_path) -> None:
    """
        Тест сохранения и загрузки списка задач в формате JSON.
    """
    file_path = tmp_path / "tasks.json"
    task_list = TaskList()
    task_list.add_task("Buy groceries", priority=2, tags=["shopping"])
    task_list.save_to_json(file_path)
    new_task_list = TaskList()
    new_task_list.load_from_json(file_path)
    assert len(new_task_list.tasks) == 1
    assert new_task_list.tasks[0].description == "Buy groceries"
    assert "shopping" in new_task_list.tasks[0].tags


# Run tests
if __name__ == "__main__":
    pytest.main(["-v", "–color=yes"])
