import csv
import random
from statistics import mean


class CheckNames:

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def __delete__(self, instance):
        raise AttributeError(f'Свойство "{self.param_name}" нельзя удалять')

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Значение {value} должно быть текстом')
        if not value.isalpha():
            raise TypeError(f'Значение {value} должно содержать только буквы')
        if not value.istitle():
            raise TypeError(f'Значение {value} должно начинаться с заглавной буквы')


class Student:
    name = CheckNames()
    surname = CheckNames()
    patronymic = CheckNames()

    def __init__(self, name, surname, patronymic):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        with open('subjects.csv', 'r', newline='', encoding='utf-8') as csv_file:
            for i in csv.reader(csv_file):
                self._sub_data = i
        self._grades = {}
        self._middle_grades = {}

    @property
    def grades(self):
        return self._grades

    def grades_fill(self):
        MIN_GRADE = 2
        MAX_GRADE = 5
        MIN_TEST_GRADE = 0
        MAX_TEST_GRADE = 100
        grades_list = []
        grades_test_list = []
        for i in self._sub_data:
            current_grade = random.randint(MIN_GRADE, MAX_GRADE)
            current_test_grade = random.randint(MIN_TEST_GRADE, MAX_TEST_GRADE)
            self._grades[i] = {"grade": current_grade, "test_grade": current_test_grade}
            grades_list.append(current_grade)
            grades_test_list.append(current_test_grade)
        self._middle_grades = {"middle_grade": mean(grades_list), "middle_tests_grade": mean(grades_test_list)}

    def __str__(self):
        result = f'Студент: {self.name} {self.surname} {self.patronymic}\n\n'
        for key, value in self._grades.items():
            result += f'Предмет: {key}\nОценка: {value.get("grade")}\nОценка теста: {value.get("test_grade")}\n\n'
        result += f'Средняя оценка предметов: {self._middle_grades.get("middle_grade")}\n' \
                  f'Средняя оценка тестов: {self._middle_grades.get("middle_tests_grade")}'
        return result


if __name__ == '__main__':
    student1 = Student("Кириллов", "Кирилл", "Сергеевич")
    student1.grades_fill()
    print(student1)
