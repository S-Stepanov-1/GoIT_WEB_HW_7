from datetime import datetime, date, timedelta
from random import randint, choice
from faker import Faker
from sqlalchemy import select

from db_connect import session
from models import Student, Teacher, Group, Subject, Grade


NUMBER_OF_STUDENTS = 50
NUMBER_OF_TEACHERS = 4
GROUPS = ["PRO-20", "UK-20s", "MIT-20", "MTU-20"]
SUBJECTS = ["Physics", "Maths", "Art", "PE", "Philosophy", "IT"]

START_DATE = datetime.strptime("2022-09-01", "%Y-%m-%d")
FINISH_DATE = datetime.strptime("2023-05-31", "%Y-%m-%d")


fake = Faker()


def get_list_date(start, finish) -> list[date]:
    """The function returns a list with workdays between two dates: start and finish"""
    result = []
    current_day = start
    while current_day <= finish:
        if current_day.isoweekday() < 6:
            result.append(current_day)
        current_day += timedelta(1)

    return result


def seed_groups():
    for group in GROUPS:
        session.add(Group(name=group))


def seed_teachers():
    for _ in range(NUMBER_OF_TEACHERS):
        teacher = Teacher(name=fake.first_name(), surname=fake.last_name())
        session.add(teacher)


def seed_students():
    groups_ids = session.scalars(select(Group.id)).all()

    for _ in range(NUMBER_OF_STUDENTS):
        student = Student(name=fake.first_name(), surname=fake.last_name(), group_id=choice(groups_ids))
        session.add(student)


def seed_subjects():
    teachers_ids = session.scalars(select(Teacher.id)).all()

    for subject in SUBJECTS:
        session.add(Subject(name=subject, teacher_id=choice(teachers_ids)))


def seed_grades():
    date_list = get_list_date(START_DATE, FINISH_DATE)

    for day in date_list:

        random_students = [randint(1, NUMBER_OF_STUDENTS) for _ in range(6)]
        random_subject = randint(1, len(SUBJECTS))
        random_grade = randint(1, 5)

        for student in random_students:
            grade = Grade(grade=random_grade, date_of=day, student_id=student, subject_id=random_subject)
            session.add(grade)


def main():
    seed_groups()
    seed_teachers()
    seed_students()
    seed_subjects()
    seed_grades()

    session.commit()


if __name__ == '__main__':
    main()
