class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.random = None


def find_loop_start(head):
    slow = head
    fast = head

    # Поиск точки встречи черепахи и зайца
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break

    # Проверка на отсутствие петли
    if slow != fast:
        return None

    # Нахождение начального узла петли
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow


def copy_list(head):
    if not head:
        return None

    # Создаем копии узлов и вставляем их после исходных узлов
    current = head
    while current:
        new_node = Node(current.value)
        new_node.next = current.next
        current.next = new_node
        current = new_node.next

    # Настройка указателей random в новых узлах
    current = head
    while current:
        current.next.random = current.random.next if current.random else None
        current = current.next.next

    # Разделение копий узлов от исходных узлов
    current = head
    new_head = head.next
    while current:
        temp = current.next
        current.next = temp.next if temp else None
        current = temp

    return new_head


def remove_duplicates(head):
    if not head:
        return

    unique_values = set()
    unique_values.add(head.value)
    current = head

    while current.next:
        if current.next.value in unique_values:
            current.next = current.next.next
        else:
            unique_values.add(current.next.value)
            current = current.next


# создание списка для 1 задания
def first():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)

    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Петля

    loop_start = find_loop_start(node1)
    if loop_start:
        return "Начальный узел цикла: " + str(loop_start.value)
    else:
        return "Нет цикла в связанном списке."


def second():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)

    node1.next = node2
    node2.next = node3
    node1.random = node3
    node2.random = node1
    node3.random = node2

    # Копирование списка
    new_head = copy_list(node1)

    # Вывод значений нового списка
    current = new_head
    result = ''
    while current:
        result += f"Значение: {current.value}, Случайные точки на: {current.random.value if current.random else None}\n"
        current = current.next
    return result


# Пример использования
def third():
    # Создание несортированного связанного списка с дубликатами
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(1)
    node4 = Node(3)
    node5 = Node(5)

    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5

    # Удаление дубликатов
    remove_duplicates(node1)

    # Вывод значений списка без дубликатов
    current = node1
    result = ''
    while current:
        result += str(current.value)
        current = current.next
    return result


print('Первое задание\n' + first())
print('\nВторое задание\n' + second())
print('\nТретье задание\n' + third())
