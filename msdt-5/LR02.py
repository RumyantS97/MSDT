from collections import deque

print('Задание 1')


def check_brackets(s):
    stack = []
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            stack.pop()
    return len(stack) == 0


s = "((()))"
result = check_brackets(s)
print(result)


def check_brackets(s):
    stack = []
    brackets = {'(': ')', '[': ']', '{': '}'}
    for char in s:
        if char in brackets.keys():
            stack.append(char)
        elif char in brackets.values():
            if not stack or brackets[stack[-1]] != char:
                return False
            stack.pop()
    return len(stack) == 0


s = "({)}"
result = check_brackets(s)
print(result)

print('Задание 2')


class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self):
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        self.stack.pop()

    def min(self):
        return self.min_stack[-1]


stack = MinStack()
stack.push(3)
stack.push(5)
stack.push(2)
stack.push(1)

print(stack.min())

stack.pop()
stack.pop()

print(stack.min())

print('Задание 3')


def max_in_window(arr, k):
    n = len(arr)
    result = []
    window = deque()

    for i in range(k):
        while window and arr[i] >= arr[window[-1]]:
            window.pop()

        window.append(i)

    for i in range(k, n):
        result.append(arr[window[0]])

        if window and window[0] <= i - k:
            window.popleft()

        while window and arr[i] >= arr[window[-1]]:
            window.pop()

        window.append(i)

    result.append(arr[window[0]])

    return result


arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(max_in_window(arr, k))

print('Задание 4')


def find_duplicates(nums):
    slow = nums[0]
    fast = nums[0]

    slow = nums[slow]
    fast = nums[nums[fast]]

    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    slow = nums[0]
    while slow != fast:
        slow = nums[slow]

        fast = nums[fast]

    return slow


nums = [1, 2, 3, 4, 5, 3]
print(find_duplicates(nums))

print('Задание 5')


def zero_matrix(matrix):
    rows_with_zero = set()
    cols_with_zero = set()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                rows_with_zero.add(i)
                cols_with_zero.add(j)

    for row in rows_with_zero:
        for j in range(len(matrix[0])):
            matrix[row][j] = 0

    for col in cols_with_zero:
        for i in range(len(matrix)):
            matrix[i][col] = 0

    return matrix


matrix = [
    [0, 2, 3],
    [4, 1, 3],
    [3, 8, 9]
]

result = zero_matrix(matrix)
for row in result:
    print(row)
