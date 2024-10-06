import random
import math


class Node:
    """Класс, представляющий узел связанного списка."""

    def __init__(self, data):
        """
        Инициализация узла.

        :param data: Значение, которое будет храниться в узле.
        """
        self.data = data
        self.next = None


class LinkedList:
    """Класс, представляющий связанный список."""

    def __init__(self):
        """Инициализация пустого связанного списка."""
        self.head = None
            
    def add_at_position(self, pos, data): 
        """
        Добавляет узел с данными в указанную позицию.

        :param pos: Позиция, куда будет добавлен узел.
        :param data: Данные для добавляемого узла.
        """
        if pos < 0:
            print("Invalid position!")
            return
        new_node = Node(data)
        if pos == 0:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        count = 0
        while current is not None and count < pos - 1:
            current = current.next
            count += 1
        if current is None:
            print("Position out of bounds")
        else:
            new_node.next = current.next
            current.next = new_node
        
    def delete_at_position(self, pos):    
        """
        Удаляет узел в указанной позиции.

        :param pos: Позиция узла для удаления.
        """
        if pos < 0:
            print("Invalid position!")
            return
        current = self.head
        if pos == 0:
            self.head = current.next
            return
        count = 0
        prev = None
        while current is not None and count < pos:
            prev = current
            current = current.next
            count += 1
        if current is None:
            print("Position out of bounds")
        else:
            prev.next = current.next

    def add_to_beginning(self, data):
        """
        Добавляет узел с данными в начало списка.

        :param data: Данные для добавляемого узла.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add_to_end(self, data):
        """
        Добавляет узел с данными в конец списка.

        :param data: Данные для добавляемого узла.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        
    def delete_first(self):
        """Удаляет первый узел списка."""
        if self.head is None:
            print("List is empty")
            return
        self.head = self.head.next

    def delete_last(self):
        """Удаляет последний узел списка."""
        if self.head is None:
            print("List is empty")
            return
        if self.head.next is None:
            self.head = None
            return
        current = self.head
        while current.next.next:
            current = current.next
        current.next = None

    def generate_random_list(self, size, min_val, max_val):
        """
        Генерирует список случайных чисел заданного размера.

        :param size: Количество случайных чисел.
        :param min_val: Минимальное значение случайных чисел.
        :param max_val: Максимальное значение случайных чисел.
        """
        for _ in range(size):
            rand_num = random.randint(min_val, max_val)
            self.add_to_end(rand_num)
        
    def display_list(self):
        """Выводит содержимое списка в консоль."""
        if self.head == None:
            print("List is empty")
            return
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()

    def sort_list(self): 
        """Сортирует список по возрастанию."""
        if self.head == None:
            return
        current = self.head
        while current:
            index = current.next
            while index:
                if current.data > index.data:
                    temp = current.data
                    current.data = index.data
                    index.data = temp
                index = index.next
            current = current.next

    def find_max(self):
        """
        Находит максимальное значение в списке.

        :return: Максимальное значение, если список не пуст; None в противном случае.
        """
        if self.head is None:
            return None
        max_value = self.head.data
        current = self.head
        while current:
            if current.data > max_value:
                max_value = current.data
            current = current.next
        return max_value
        
    def find_min(self):
        """
        Находит минимальное значение в списке.

        :return: Минимальное значение, если список не пуст; None в противном случае.
        """
        if self.head is None:
            return None
        min_value = self.head.data
        current = self.head
        while current:
            if current.data < min_value:
                min_value = current.data
            current = current.next
        return min_value

    def get_length(self):
        """
        Возвращает длину списка.

        :return: Длина списка.
        """
        current = self.head
        length = 0
        while current:
            length += 1
            current = current.next
        return length

    def vector_norm(self):
        """
        Вычисляет норму вектора, представленного элементами списка.

        :return: Норма вектора.
        """
        if self.head is None:
            return 0
        sum_of_squares = 0
        current = self.head
        while current:
            sum_of_squares += current.data ** 2
            current = current.next
        return math.sqrt(sum_of_squares)

    def reverse_list(self):
        """Переворачивает список."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def is_empty(self):
        """
        Проверяет, пуст ли список.

        :return: True, если список пуст; False в противном случае.
        """
        return self.head is None
        
    def clear_list(self):
        """Удаляет все элементы из списка."""
        self.head = None

    def average_value(self):
        """
        Вычисляет среднее значение элементов списка.

        :return: Среднее значение, если список не пуст; None в противном случае.
        """
        if self.head is None:
            return None
        total = 0
        count = 0
        current = self.head
        while current:
            total += current.data
            count += 1
            current = current.next
        return total / count if count > 0 else 0

    def is_palindrome(self):
        """
        Проверяет, является ли список палиндромом.

        :return: True, если список является палиндромом; False в противном случае.
        """
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        return values == values[::-1]

    def merge(self, other_list):
        """
        Объединяет текущий список с другим списком.

        :param other_list: Другой связанный список для объединения.
        """
        if self.head is None:
            self.head = other_list.head
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = other_list.head

    def find_common_element(self, other_list):
        """
        Находит первый общий элемент между текущим списком и другим списком.

        :param other_list: Другой связанный список для поиска общего элемента.
        :return: Первый общий элемент, если найден; None в противном случае.
        """
        elements = set()
        current = self.head
        while current:
            elements.add(current.data)
            current = current.next
        current = other_list.head
        while current:
            if current.data in elements:
                return current.data
            current = current.next
        return None
        
    def count_occurrences(self, value):
        """
        Подсчитывает количество вхождений указанного значения в списке.

        :param value: Значение для поиска.
        :return: Количество вхождений значения в списке.
        """
        current = self.head
        count = 0
        while current:
            if current.data == value:
                count += 1
            current = current.next
        return count

    def delete_all_occurrences(self, value):
        """
        Удаляет все вхождения указанного значения из списка.

        :param value: Значение для удаления.
        """
        current = self.head
        prev = None
        while current:
            if current.data == value:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
            else:
                prev = current
            current = current.next

    def duplicate_elements(self):
        """Дублирует каждый элемент списка."""
        current = self.head
        while current:
            new_node = Node(current.data)
            new_node.next = current.next
            current.next = new_node
            current = new_node.next


# Пример использования новых функций
l1 = LinkedList()
l2 = LinkedList()

# Генерация случайных списков
l1.generate_random_list(5, 1, 50)
l2.generate_random_list(5, 20, 70)

print("First list:")
l1.display_list()

print("Second list:")
l2.display_list()

# Объединение двух списков
l1.merge(l2)
print("After merging two lists:")
l1.display_list()

# Поиск общего элемента
common_element = l1.find_common_element(l2)
if common_element:
    print("Common element found:", common_element)
else:
    print("No common element found")

# Проверка на палиндром
print("Is the list a palindrome?", l1.is_palindrome())

# Поиск среднего значения
print("Average value of the list:", l1.average_value())

# Переворот списка
l1.reverse_list()
print("List after reversing:")
l1.display_list()

# Удаление всех элементов
l1.clear_list()
print("After clearing the list:")
l1.display_list()

# Подсчет вхождений элемента
value = 5
occurrences = l1.count_occurrences(value)  
print(f"Value {value} occurs {occurrences} times.")

# Удаление всех вхождений элемента
l1.delete_all_occurrences(5)  
print("After deleting all occurrences of 5:")
l1.display_list()

# Дублирование всех элементов списка
l1.duplicate_elements()  
print("After duplicating all elements:")
l1.display_list()
