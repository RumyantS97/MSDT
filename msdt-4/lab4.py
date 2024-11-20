import logging

# Настройка логгирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class Node1:
    """Класс для задачи 1 (поиск петли в списке)."""
    def __init__(self, value):
        self.value = value
        self.next = None


class Node2:
    """Класс для задачи 2 (копирование списка с указателем random)."""
    def __init__(self, value):
        self.value = value
        self.next = None
        self.random = None


class Node:
    """Класс для задачи 3 (удаление дубликатов в списке)."""
    def __init__(self, value):
        self.value = value
        self.next = None


def print_linked_list(head):
    """Выводит связный список."""
    current = head
    logging.debug("Печать связного списка.")
    while current:
        print(current.value, end=" -> ")
        current = current.next
    print("None")


def find_loop_start(head):
    """Находит начальный узел петли в связном списке."""
    logging.info("Начало поиска петли в списке.")
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            logging.info("Петля обнаружена.")
            break

    if slow != fast:
        logging.warning("Петля не найдена.")
        return None

    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    logging.info("Начальный узел петли найден: %s", slow.value)
    return slow


def copy_list(head):
    """Копирует связный список с указателями random."""
    if not head:
        logging.warning("Список пуст, копирование невозможно.")
        return None

    logging.info("Начало копирования связного списка.")
    current = head

    # Шаг 1: Создание копий узлов
    while current:
        new_node = Node2(current.value)
        new_node.next = current.next
        current.next = new_node
        current = new_node.next
    logging.debug("Создание копий узлов завершено.")

    # Шаг 2: Установка указателей random
    current = head
    while current:
        current.next.random = current.random.next if current.random else None
        current = current.next.next
    logging.debug("Указатели random установлены.")

    # Шаг 3: Разделение списков
    new_head = head.next
    current = head
    new_current = new_head
    while current:
        current.next = new_current.next
        current = current.next
        new_current.next = current.next if current else None
        new_current = new_current.next
    logging.info("Копирование завершено.")

    return new_head


def remove_duplicates(head):
    """Удаляет дубликаты в несортированном связном списке."""
    logging.info("Начало удаления дубликатов из связного списка.")
    current = head
    while current:
        runner = current
        while runner.next:
            if runner.next.value == current.value:
                logging.debug("Удален дубликат значения: %s", current.value)
                runner.next = runner.next.next
            else:
                runner = runner.next
        current = current.next
    logging.info("Удаление дубликатов завершено.")


# Задание 1
print("Задание 1")
node1 = Node1(1)
node2 = Node1(2)
node3 = Node1(3)
node4 = Node1(4)
node5 = Node1(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node3  # Создание петли

loop_start = find_loop_start(node1)
if loop_start:
    print("Начальный узел петли:", loop_start.value)
else:
    print("Петли не найдено")
    print_linked_list(node1)


# Задание 2
print("\nЗадание 2")
node1 = Node2(1)
node2 = Node2(2)
node3 = Node2(3)

node1.next = node2
node2.next = node3

node1.random = node3
node2.random = node1
node3.random = node2

new_head = copy_list(node1)

# Вывод значений нового списка и соответствующих указателей random
current = new_head
while current:
    print("Value:", current.value)
    print("Random value:", current.random.value if current.random else None)
    print()
    current = current.next


# Задание 3
print("\nЗадание 3")
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(2)
node5 = Node(1)
node6 = Node(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6

# Вывод исходного списка для проверки
print_linked_list(node1)

# Удаление дубликатов
remove_duplicates(node1)

# Вывод списка после удаления дубликатов
print_linked_list(node1)
