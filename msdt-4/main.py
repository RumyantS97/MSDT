import random as rand
import logging


logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    filename = "msdt-4\log.txt",
    filemode = "w"
)

class Node:
    def __init__(self, value = 0, next=None):
        self.value = value
        self.next = next
        self.random = None
        

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0
        self.list_node = []


    def add(self, value=0):
        logging.info(f"Добавление узла с значением: {value}")
        if not self.head:
            self.head = Node(value)
            self.length += 1
            self.list_node.append(self.head)
            self.head.random = self.head
            logging.debug(f"Создан узел-хед: {self.head.value} с указателем random на себя.")
        else:
            self.length += 1
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(value)
            self.list_node.append(current.next)
            current = self.head
            while current:
                current.random = self.list_node[rand.randint(0, self.length - 1)]
                logging.debug(f"Назначен случайный указатель random для узла {current.value}: {current.random.value}")
                current = current.next


    def __copy__(self):
        logging.info("Создание глубокой копии LinkedList.")
        if not self.head:
            return LinkedList()
        else:
            current = self.head
            while current:
                new_node = Node(current.value)
                new_node.next = current.next
                current.next = new_node
                current = new_node.next
            current = self.head
            while current:
                if current.random is not None:
                    current.next.random = current.random
                    logging.debug(f"Установлен random для копированного узла {current.next.value} на {current.next.random.value}")
                current = current.next.next
            new_node = self.head.next
            cur_old = self.head
            cur_new = new_node
            while cur_old:
                cur_old.next = cur_old.next.next
                cur_old = cur_old.next
                if cur_new.next:
                    cur_new.next = cur_new.next.next
                    cur_new = cur_new.next

            new_ll = LinkedList()
            new_ll.head = new_node
            logging.info("Глубокая копия LinkedList успешно создана.")
            return new_ll
        

    def __str__(self):
        if not self.head:
            return "[]"
        else:
            s = "["
            current = self.head
            s += f"{str(current.value)}({str(current.random.value)})"
            while current.next:
                current = current.next
                s += f"->{str(current.value)}({str(current.random.value)})"
            s += "]"
            return s


a = [10, 15, 21, 4, 2, 105, 11]
ll = LinkedList()
for i in range(len(a)):
    ll.add(a[i])
print(ll)
b = ll.__copy__()
print(b)

def zero_matrix(matrix):
    logging.info("Начало функции zero_matrix.")
    if not matrix:
        logging.warning("Пустая матрица передана.")
        return

    rows_with_zero = set()
    cols_with_zero = set()
    logging.debug(f"Исходная матрица: {matrix}")

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                rows_with_zero.add(i)
                cols_with_zero.add(j)
                logging.debug(f"Найден нулевой элемент на позиции ({i}, {j})")

    for i in rows_with_zero:
        for j in range(len(matrix[0])):
            matrix[i][j] = 0
            logging.debug(f"Устанавливаю строку {i} в нули")

    for j in cols_with_zero:
        for i in range(len(matrix)):
            matrix[i][j] = 0
            logging.debug(f"Устанавливаю столбец {j} в нули")

    logging.info("Завершена функция zero_matrix.")
    logging.debug(f"Результирующая матрица: {matrix}")


matrix = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 8, 9]
]

zero_matrix(matrix)

for row in matrix:
    print(row)

