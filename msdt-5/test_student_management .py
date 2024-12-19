import pytest
from unittest.mock import Mock
from student_management import Student, StudentManager


def test_create_student():
    manager = StudentManager()
    student = manager.add_student("Alice")
    assert student.student_id == 1
    assert student.name == "Alice"
    assert student.grades == {}


def test_add_grade():
    student = Student(1, "Alice")
    student.add_grade("Math", 90)
    assert student.grades == {"Math": 90}


def test_add_invalid_grade():
    student = Student(1, "Alice")
    with pytest.raises(ValueError):
        student.add_grade("Math", 101)


def test_get_average_grade():
    student = Student(1, "Alice")
    student.add_grade("Math", 90)
    student.add_grade("Science", 85)
    assert student.get_average_grade() == 87.5


def test_get_average_grade_no_grades():
    student = Student(1, "Alice")
    assert student.get_average_grade() == 0


def test_add_grade_to_student():
    manager = StudentManager()
    student = manager.add_student("Alice")
    manager.add_grade_to_student(student.student_id, "Math", 90)
    assert manager.get_student(student.student_id).grades == {"Math": 90}


# Моки
def test_mock_student_interaction():
    mock_student = Mock(spec=Student)
    mock_student.student_id = 1
    mock_student.name = "Alice"

    mock_student.get_average_grade.return_value = 85.0

    # Проверяем, что метод get_average_grade был вызван
    assert mock_student.get_average_grade() == 85.0
    mock_student.get_average_grade.assert_called_once()


def test_stub_student_manager():
    stub_manager = Mock(spec=StudentManager)

    stub_manager.get_student.return_value = Student(1, "Alice")

    student = stub_manager.get_student(1)
    assert student.name == "Alice"
    stub_manager.get_student.assert_called_with(1)


@pytest.mark.parametrize(
    "grades, expected_average",
    [
        ({"Math": 90, "Science": 85}, 87.5),
        ({"Math": 100, "Science": 70}, 85.0),
        ({"Math": 80}, 80.0),
        ({}, 0),
    ],
)
def test_average_grade_with_parameters(grades, expected_average):
    student = Student(1, "Alice")
    for subject, grade in grades.items():
        student.add_grade(subject, grade)
    assert student.get_average_grade() == expected_average
