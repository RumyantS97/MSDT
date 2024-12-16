class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}

    def add_grade(self, subject, grade):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(grade)

    def calculate_average(self):
        total_grades = 0
        count = 0
        for grades in self.grades.values():
            total_grades += sum(grades)
            count += len(grades)
        return total_grades / count if count > 0 else 0

    def __str__(self):
        return f"Студент: {self.name}, Средняя оценка: {self.calculate_average():.2f}"


class School:
    def __init__(self):
        self.students = {}
        self.subjects = []

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = Student(name)
            print(f"Студент '{name}' добавлен.")
        else:
            print(f"Студент '{name}' уже существует.")

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)
            print(f"Предмет '{subject}' добавлен.")
        else:
            print(f"Предмет '{subject}' уже существует.")

    def add_grade(self, student_name, subject, grade):
        if student_name in self.students and subject in self.subjects:
            self.students[student_name].add_grade(subject, grade)
            print(f"Оценка {grade} добавлена для студента {student_name} по предмету {subject}.")
        else:
            print("Некорректное имя студента или предмета.")

    def generate_report(self):
        print("\nОтчет по школе:")
        for student in self.students.values():
            print(student)
            for subject, grades in student.grades.items():
                print(f"  {subject}: {grades}")
            print()


def main():
    school = School()

    while True:
        print("\nМеню управления школой:")
        print("1. Добавить студента")
        print("2. Добавить предмет")
        print("3. Добавить оценку")
        print("4. Сгенерировать отчет")
        print("5. Выход")

        choice = input("Выберите опцию (1-5): ")

        if choice == '1':
            name = input("Введите имя студента: ")
            school.add_student(name)

        elif choice == '2':
            subject = input("Введите название предмета: ")
            school.add_subject(subject)

        elif choice == '3':
            student_name = input("Введите имя студента: ")
            subject = input("Введите название предмета: ")
            grade = float(input("Введите оценку: "))
            school.add_grade(student_name, subject, grade)

        elif choice == '4':
            school.generate_report()

        elif choice == '5':
            print("Выход из системы управления школой.")
            break

        else:
            print("Некорректный вариант. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
