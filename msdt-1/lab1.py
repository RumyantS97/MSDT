import random


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.random = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_element(self, value):

        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def input_list(self):

        current = self.head
        while current:
            print(current.value, "->", end=" ")
            current = current.next
        print("null")

    def partition(self, partition_value):

        smaller_head = smaller_tail = None
        greater_or_equal_head = greater_or_equal_tail = None

        current = self.head

        while current:
            next_node = current.next
            current.next = None

            if current.value < partition_value:
                if not smaller_head:
                    smaller_head = current
                    smaller_tail = current
                else:
                    smaller_tail.next = current
                    smaller_tail = current
            else:
                if not greater_or_equal_head:
                    greater_or_equal_head = current
                    greater_or_equal_tail = current
                else:
                    greater_or_equal_tail.next = current
                    greater_or_equal_tail = current

            current = next_node

        if not smaller_head:
            self.head = greater_or_equal_head
        else:
            smaller_tail.next = greater_or_equal_head
            self.head = smaller_head

    @staticmethod
    def find_kth_from_end(head, k):

        if not head or k <= 0:
            raise ValueError("Недопустимые аргументы")

        fast_pointer = slow_pointer = head

        for _ in range(k):
            if not fast_pointer:
                raise ValueError(f"Список короче {k} элементов")
            fast_pointer = fast_pointer.next

        while fast_pointer:
            fast_pointer = fast_pointer.next
            slow_pointer = slow_pointer.next

        return slow_pointer.value

    @staticmethod
    def copy_random_list(head):

        if not head:
            return None

        current = head
        while current:
            new_node = Node(current.value)
            new_node.next = current.next
            current.next = new_node
            current = new_node.next

        current = head
        while current:
            if current.random:
                current.next.random = current.random.next
            current = current.next.next

        new_head = head.next
        current = head
        while current:
            new_node = current.next
            current.next = new_node.next
            if new_node.next:
                new_node.next = new_node.next.next
            current = current.next

        return new_head

    @staticmethod
    def print_list_with_random(head):

        while head:
            print("Значение:", head.value, end="")
            if head.random:
                print(", Случайный указатель на:", head.random.value)
            else:
                print(", Случайный указатель на: None")
            head = head.next

    def remove_duplicates(self):

        current = self.head
        seen = set()
        prev = None

        while current:
            if current.value in seen:
                prev.next = current.next
            else:
                seen.add(current.value)
                prev = current
            current = current.next

    def reverse(self):

        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    @staticmethod
    def merge_sorted_lists(head1, head2):

        dummy = Node(0)
        tail = dummy

        while head1 and head2:

            if head1.value < head2.value:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next

        if head1:
            tail.next = head1
        elif head2:
            tail.next = head2

        return dummy.next


if __name__ == "__main__":
    while True:

        print("Лабораторная работа 1. Списки. 2 вариант")
        print("1 - задание ")
        print("2 - задание ")
        print("3 - задание ")
        print("4 - завершить работу ")
        print("5 - удалить дубликаты ")
        print("6 - реверсировать список ")
        print("7 - объединить два отсортированных списка ")
        number = input("Введите номер задания: ")
        print("")

        if number == '1':

            linked_list = LinkedList()
            linked_list.add_element(3)
            linked_list.add_element(5)
            linked_list.add_element(8)
            linked_list.add_element(5)
            linked_list.add_element(10)
            linked_list.add_element(2)
            linked_list.add_element(1)

            print("Исходный список:")
            linked_list.input_list()

            partition_value = 5
            linked_list.partition(partition_value)
            print(f"Список после разбиения вокруг значения {partition_value}")
            linked_list.input_list()

        elif number == '2':

            linked_list = LinkedList()
            n = random.randint(4, 8)
            for _ in range(n):
                value = random.randint(0, 99)
                linked_list.add_element(value)

            print("Исходный список: ")
            linked_list.input_list()

            k = int(input("Введите значение k: "))
            head = linked_list.head
            try:
                result = LinkedList.find_kth_from_end(head, k)
                print(f"{k}-ый с конца элемент: {result}")
            except ValueError as e:
                print(e)

        elif number == '3':

            list1_head = Node(7)
            list1_head.next = Node(8)
            list1_head.next.next = Node(3)
            list1_head.next.next.next = Node(1)
            list1_head.next.next.next.next = Node(2)

            list1_head.random = list1_head.next.next
            list1_head.next.random = list1_head.next.next.next.next
            list1_head.next.next.random = list1_head
            list1_head.next.next.next.random = list1_head.next
            list1_head.next.next.next.next.random = None

            print("Исходный связный список: ")
            LinkedList.print_list_with_random(list1_head)

            new_head = LinkedList.copy_random_list(list1_head)
            print("Изменённый связный список: ")
            LinkedList.print_list_with_random(new_head)

        elif number == '4':

            break

        elif number == '5':

            linked_list = LinkedList()
            linked_list.add_element(1)
            linked_list.add_element(3)
            linked_list.add_element(3)
            linked_list.add_element(2)
            linked_list.add_element(1)
            linked_list.add_element(4)
            print("Исходный список с дубликатами:")
            linked_list.input_list()

            linked_list.remove_duplicates()
            print("Список после удаления дубликатов:")
            linked_list.input_list()

        elif number == '6':

            linked_list = LinkedList()
            linked_list.add_element(1)
            linked_list.add_element(2)
            linked_list.add_element(3)
            linked_list.add_element(4)
            print("Исходный список:")
            linked_list.input_list()

            linked_list.reverse()
            print("Список после реверсирования:")
            linked_list.input_list()

        elif number == '7':

            linked_list1 = LinkedList()
            linked_list1.add_element(1)
            linked_list1.add_element(3)
            linked_list1.add_element(5)

            linked_list2 = LinkedList()
            linked_list2.add_element(2)
            linked_list2.add_element(4)
            linked_list2.add_element(6)

            print("Первый отсортированный список:")
            linked_list1.input_list()

            print("Второй отсортированный список:")
            linked_list2.input_list()

            merged_head = LinkedList.merge_sorted_lists(linked_list1.head, linked_list2.head)
            print("Объединённый отсортированный список:")
            current = merged_head
            while current:
                print(current.value, "->", end=" ")
                current = current.next
            print("null")
