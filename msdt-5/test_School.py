import pytest
from unittest.mock import patch, MagicMock
from LR5 import Student, School


# Тесты для класса Student
#Проверяет правильность инициализации студента.
def test_student_initialization():
    student = Student("Иван")
    assert student.name == "Иван"
    assert student.grades == {}

#Проверяет добавление оценки для нового предмета.
def test_add_grade_new_subject():
    student = Student("Петр")
    student.add_grade("Математика", 5)
    assert student.grades == {"Математика": [5]}

#Проверяет добавление оценки для существующего предмета.
def test_add_grade_existing_subject():
    student = Student("Сергей")
    student.add_grade("История", 4)
    student.add_grade("История", 5)
    assert student.grades == {"История": [4, 5]}

#Проверяет среднюю оценку студента без оценок.
def test_calculate_average_no_grades():
    student = Student("Анна")
    assert student.calculate_average() == 0

#Проверяет среднюю оценку студента с несколькими оценками.
def test_calculate_average_with_grades():
    student = Student("Мария")
    student.add_grade("Физика", 3)
    student.add_grade("Физика", 5)
    student.add_grade("Химия", 4)
    assert student.calculate_average() == (3 + 5 + 4) / 3


# Тесты для класса School
#Проверяет добавление нового студента в школу.
def test_add_student():
    school = School()
    school.add_student("Алексей")
    assert "Алексей" in school.students

#Проверяет добавление нового предмета в школу.
def test_add_subject():
    school = School()
    school.add_subject("Литература")
    assert "Литература" in school.subjects

#Проверяет добавление оценки для существующего студента и предмета
def test_add_grade_valid():
    school = School()
    school.add_student("Дмитрий")
    school.add_subject("География")
    school.add_grade("Дмитрий", "География", 4)

    assert "География" in school.students["Дмитрий"].grades
    assert school.students["Дмитрий"].grades["География"] == [4]

#Проверяет попытку добавления оценки для несуществующего студента
def test_add_grade_invalid_student():
    school = School()
    school.add_subject("Искусство")

    # Проверка на некорректное имя студента
    result = school.add_grade("Неизвестный", "Искусство", 5)

    # Ожидаем, что ничего не добавится
    assert "Неизвестный" not in school.students

#Параметризованный тест для проверки добавления оценок с различными входными данными
@pytest.mark.parametrize("student_name, subject, first_grade, second_grade, expected_grades", [
    ("Кирилл", "Музыка", 5, 3, [5, 3]),
])
def test_add_grades_parametrized(student_name, subject, first_grade, second_grade, expected_grades):
    # Создаем новый экземпляр школы для каждого теста
    school = School()

    # Добавляем студента и предмет
    school.add_student(student_name)
    school.add_subject(subject)

    # Добавляем первую и вторую оценки
    school.add_grade(student_name, subject, first_grade)
    school.add_grade(student_name, subject, second_grade)

    # Проверяем оценки
    assert school.students[student_name].grades[subject] == expected_grades


#Проверяем, что отчет содержит ожидаемую информацию о студенте и его оценках
def test_report_generation(capsys):
    school = School()

    # Добавляем студентов и предметы
    school.add_student("Ольга")
    school.add_subject("Химия")

    # Добавляем оценки
    school.add_grade("Ольга", "Химия", 5)

    # Генерируем отчет
    school.generate_report()

    # Проверяем вывод в консоль
    captured = capsys.readouterr()

    assert "Отчет по школе:" in captured.out
    assert "Студент: Ольга" in captured.out
    assert "Химия: [5]" in captured.out


# Тесты с использованием моков и стабов
#Здесь мы используем unittest.mock.patch для замены класса Student
#на мок-объект. Мы настраиваем поведение метода calculate_average,
#чтобы он возвращал фиксированное значение (4.5).
#Затем мы проверяем, что метод был вызван и вернул ожидаемое значение
@patch('LR5.Student')
def test_student_mock(mock_student):
    mock_student_instance = mock_student.return_value
    mock_student_instance.calculate_average.return_value = 4.5

    # Проверяем вызов метода calculate_average
    average = mock_student_instance.calculate_average()

    assert average == 4.5
    mock_student_instance.calculate_average.assert_called_once()

#В этом тесте мы заменяем класс School на мок-объект и настраиваем его так,
#чтобы он содержал студента с именем "Алексей". Мы также настраиваем метод
#calculate_average для этого студента. Затем мы проверяем, что метод
#возвращает ожидаемое значение (4.0).
@patch('LR5.School')
def test_school_mock(mock_school):
    mock_school_instance = mock_school.return_value
    mock_school_instance.students = {"Алексей": MagicMock()}

    # Настройка мока для студента
    mock_school_instance.students["Алексей"].calculate_average.return_value = 4.0

    # Проверяем вызов метода calculate_average у студента
    average = mock_school_instance.students["Алексей"].calculate_average()

    assert average == 4.0
