from sqlalchemy import func, desc, and_, distinct, select

from models import Student, Teacher, Group, Subject, Grade
from db_connect import session


def set_subj():
    subject = input("Please, enter a subject id from the list\nPhysics: 1\nMaths: 2\nArt: 3\n"
                    "PE: 4\nPhilosophy:5\nIT: 6\n>>>")
    return subject


def select_1():
    """--- Find the 5 students with the highest grade point average in all subjects ---"""
    statement = (select(Student.fullname, Group.name, func.round(func.avg(Grade.grade), 2).label("average_grade"))
                 .join(Group)
                 .join(Grade)
                 .group_by(Student.id)
                 .group_by(Group.name)
                 .order_by(desc("average_grade"))
                 .limit(5)
                 )

    result = session.execute(statement)
    print(select_1.__doc__)

    for student, group, grade in result.all():
        print(student, group, grade)


def select_2():
    """--- Find the student with the highest grade point average in a particular subject ---"""
    print(select_2.__doc__)
    statement = (select(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade'))
                 .join(Grade, Subject.id == Grade.subject_id)
                 .join(Student, Student.id == Grade.student_id)
                 .where(Subject.id == set_subj())
                 .group_by(Student.id, Subject.name)
                 .order_by(desc("average_grade"))
                 .limit(1)
                 )

    result = session.execute(statement)

    for subj, student, avg_grade in result.all():
        print(subj, student, avg_grade)

