import random
import math

class Node:
    def __init__ (self, data):
        self.data=data
        self.next=None

class LinkedList:
        def __init__(self):
            self.head=None
            
        def add_at_position(self, pos, data): 
                if pos<0:
                    print("Invalid position!")
                    return
                new_node=node(data)
                if pos==0:
                    new_node.next=self.head
                    self.head=new_node
                    return
                current=self.head
                count=0
                while current is not None and count<pos-1:
                    current=current.next
                    count+=1
                if current is None:
                    print("Position out of bounds")
                else:
                    new_node.next=current.next
                    current.next=new_node
        
        def delete_at_position(self,pos):    
                if pos<0:
                    print ("Invalid position!")
                    return
                current=self.head
                if pos==0:
                    self.head=current.next
                    return
                count=0
                prev=None
                while current is not None and count<pos:
                    prev=current
                    current=current.next
                    count+=1
                if current is None:
                    print("Position out of bounds")
                else:
                    prev.next=current.next

        def add_to_beginning(self, data):
            new_node=node(data)
            new_node.next=self.head
            self.head=new_node

        def add_to_end(self, data):
            new_node=node(data)
            if self.head is None:
                self.head=new_node
                return
            current=self.head
            while current.next:
                current=current.next
            current.next=new_node
        
        def delete_first(self):
            if self.head is None:
                print("List is empty")
                return
            self.head=self.head.next

        def delete_last(self):
            if self.head is None:
                print("List is empty")
                return
            if self.head.next is None:
                self.head=None
                return
            current=self.head
            while current.next.next:
                current=current.next
            current.next=None

        def generate_random_list(self, size, min_val, max_val):
            for _ in range(size):
                rand_num=random.randint(min_val, max_val)
                self.add_to_end(rand_num)
        
        def display_list(self):
            if self.head==None:
                print("List is empty")
                return
            current=self.head
            while current:
                print(current.data,end=' ')
                current=current.next
            print()

        def sort_list(self): 
                if self.head==None:
                    return
                current=self.head
                while current:
                    index=current.next
                    while index:
                        if current.data>index.data:
                            temp=current.data
                            current.data=index.data
                            index.data=temp
                        index=index.next
                    current=current.next

        def find_max(self):
            if self.head is None:
                return None
            max_value=self.head.data
            current=self.head
            while current:
                if current.data > max_value:
                    max_value=current.data
                current=current.next
            return max_value
        
        def find_min(self):
            if self.head is None:
                return None
            min_value=self.head.data
            current=self.head
            while current:
                if current.data < min_value:
                    min_value=current.data
                current=current.next
            return min_value

        def get_length(self):
            current=self.head
            length=0
            while current:
                length+=1
                current=current.next
            return length

        def vector_norm(self):
            if self.head is None:
                return 0
            sum_of_squares = 0
            current=self.head
            while current:
                sum_of_squares+=current.data**2
                current=current.next
            return math.sqrt(sum_of_squares)

        # Новая функция: Переворот списка (реверс)
        def reverse_list(self):
            prev = None
            current = self.head
            while current:
                next_node = current.next
                current.next = prev
                prev = current
                current = next_node
            self.head = prev

        # Новая функция: Проверка на пустоту
        def is_empty(self):
            return self.head is None
        
        # Новая функция: Удаление всех элементов списка
        def clear_list(self):
            self.head = None

        # Новая функция: Поиск среднего значения элементов списка
        def average_value(self):
            if self.head is None:
                return None
            total = 0
            count = 0
            current=self.head
            while current:
                total += current.data
                count += 1
                current=current.next
            return total / count if count > 0 else 0

        # Новая функция: Проверка, является ли список палиндромом
        def is_palindrome(self):
            values = []
            current=self.head
            while current:
                values.append(current.data)
                current=current.next
            return values == values[::-1]

        # Новая функция: Объединение двух списков
        def merge(self, other_list):
            if self.head is None:
                self.head = other_list.head
                return
            current=self.head
            while current.next:
                current=current.next
            current.next = other_list.head

        # Новая функция: Поиск общего элемента в двух списках
        def find_common_element(self, other_list):
            elements = set()
            current=self.head
            while current:
                elements.add(current.data)
                current=current.next
            current=other_list.head
            while current:
                if current.data in elements:
                    return current.data
                current=current.next
            return None
        
        # Новая функция: Подсчет вхождений элемента
        def count_occurrences(self, value):
            current=self.head
            count=0
            while current:
                if current.data == value:
                    count+=1
                current=current.next
            return count

        # Новая функция: Удаление всех вхождений элемента
        def delete_all_occurrences(self, value):
            current=self.head
            prev=None
            while current:
                if current.data == value:
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                else:
                    prev = current
                current = current.next

        # Новая функция: Дублирование каждого элемента списка
        def duplicate_elements(self):
            current=self.head
            while current:
                new_node=node(current.data)
                new_node.next=current.next
                current.next=new_node
                current=new_node.next

# Пример использования новых функций
l1=linkedlist()
l2=linkedlist()

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
occurrences = l.count_occurrences(value)
print(f"Value {value} occurs {occurrences} times.")

# Удаление всех вхождений элемента
l.delete_all_occurrences(5)
print("After deleting all occurrences of 5:")
l.display_list()

# Дублирование всех элементов списка
l.duplicate_elements()
print("After duplicating all elements:")
l.display_list()
