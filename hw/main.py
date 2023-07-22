import csv
import re

class NameValidator:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not value.isalpha() or not value.istitle():
            raise ValueError(f"Invalid {self.name}. Only alphabet characters with the first letter capitalized are allowed.")
        instance.__dict__[self.name] = value

class SubjectValidator:
    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self):
        self.subjects = set()

    def __set__(self, instance, value):
        if value not in self.subjects:
            raise ValueError(f"{value} is not a valid subject.")
        instance.__dict__[self.name] = value

class Student:
    first_name = NameValidator()
    last_name = NameValidator()
    patronymic = NameValidator()

    subjects = SubjectValidator()

    def __init__(self, first_name, last_name, patronymic, subjects_file):
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.subjects = self.load_subjects(subjects_file)
        self.scores = {subject: {'grades': [], 'test_results': []} for subject in self.subjects}

    @staticmethod
    def load_subjects(file_path):
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            subjects = next(reader)  # Assuming the first row contains subject names
        return subjects

    def add_score(self, subject, grade, test_result):
        if grade not in range(2, 6) or test_result not in range(0, 101):
            raise ValueError("Invalid grade or test result. Grades should be between 2 and 5, test results should be between 0 and 100.")
        if subject not in self.subjects:
            raise ValueError(f"{subject} is not a valid subject.")
        self.scores[subject]['grades'].append(grade)
        self.scores[subject]['test_results'].append(test_result)

    def average_grade(self, subject=None):
        if subject:
            if subject not in self.subjects:
                raise ValueError(f"{subject} is not a valid subject.")
            grades = self.scores[subject]['grades']
            if not grades:
                return 0
            return sum(grades) / len(grades)
        else:
            all_grades = [grade for subject_scores in self.scores.values() for grade in subject_scores['grades']]
            if not all_grades:
                return 0
            return sum(all_grades) / len(all_grades)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

# Пример использования класса Student
subjects_file = 'subjects.csv'
student = Student("John", "Doe", "Smith", subjects_file)

student.add_score("Math", 5, 90)
student.add_score("Physics", 4, 85)
student.add_score("History", 3, 78)

print(student)
print(student.average_grade("Math"))  # Вывод: 5.0
print(student.average_grade("Physics"))  # Вывод: 4.0
print(student.average_grade("History"))  # Вывод: 3.0
print(student.average_grade())  # Вывод: 4.0
