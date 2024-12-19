class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    def add_grade(self, subject, grade):
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100.")
        self.grades[subject] = grade

    def get_average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def __str__(self):
        return f"Student(ID={self.student_id}, Name='{self.name}', Grades={self.grades})"


class StudentManager:
    def __init__(self):
        self.students = {}
        self.next_id = 1

    def add_student(self, name):
        student = Student(self.next_id, name)
        self.students[self.next_id] = student
        self.next_id += 1
        return student

    def find_student_by_name(self, name):
        return [student for student in self.students.values() if student.name.lower() == name.lower()]

    def get_student(self, student_id):
        return self.students.get(student_id)

    def add_grade_to_student(self, student_id, subject, grade):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        student.add_grade(subject, grade)
        return student

    def get_average_grade_for_student(self, student_id):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        return student.get_average_grade()

    def __str__(self):
        students_info = "\n".join(str(student) for student in self.students.values())
        return f"Student Manager:\n{students_info}"