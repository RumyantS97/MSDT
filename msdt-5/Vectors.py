class Vectors:
    def __init__(self, size):
        if size <= 0:
            print("Размерность должна быть больше нуля!")
            size = 5
        self.vector = [0.0] * size

    def get_elements(self, index):
        if 0 <= index < self.length():
            return self.vector[index]
        else:
            raise ValueError("Некорректный индекс!")

    def set_elements(self, index, elem):
        if 0 <= index < self.length():
            self.vector[index] = elem
        else:
            raise ValueError("Некорректный индекс!")

    def length(self):
        return len(self.vector)

    def search_min(self):
        min_value = self.vector[0]
        for i in range(self.length()):
            if min_value > self.vector[i]:
                min_value = self.vector[i]
        return min_value

    def search_max(self):
        max_value = self.vector[0]
        for i in range(self.length()):
            if max_value < self.vector[i]:
                max_value = self.vector[i]
        return max_value

    def __str__(self):
        return " ".join(map(str, self.vector))

    def ascending_sort(self):
        for i in range(1, self.length()):
            key = self.vector[i]
            j = i - 1
            while j >= 0 and self.vector[j] > key:
                self.vector[j + 1] = self.vector[j]
                j -= 1
            self.vector[j + 1] = key

    def descending_sort(self):
        for i in range(1, self.length()):
            key = self.vector[i]
            j = i - 1
            while j >= 0 and self.vector[j] < key:
                self.vector[j + 1] = self.vector[j]
                j -= 1
            self.vector[j + 1] = key

    def norm_vector(self):
        sum = 0
        for x in self.vector:
            sum += x ** 2
        return sum ** 0.5

    def multi_number(self, num):
        new_vect = Vectors(self.length())
        for i in range(self.length()):
            new_vect.set_elements(i, self.vector[i] * num)
        return new_vect

    @staticmethod
    def adding_vectors(v1, v2):
        if v1.length() != v2.length():
            raise ValueError("Размерности векторов не равны!")
        new_vect = Vectors(v1.length())
        for i in range(v1.length()):
            new_vect.set_elements(i, v1.get_elements(i) + v2.get_elements(i))
        return new_vect

    @staticmethod
    def scalar_vectors(v1, v2):
        if v1.length() != v2.length():
            raise ValueError("Размерности векторов не равны!")
        scal = 0
        for i in range(v1.length()):
            scal += v1.get_elements(i) * v2.get_elements(i)
        return scal
