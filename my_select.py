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


def select_3():
    """--- Find the average score of groups in a particular subject ---"""
    print(select_3.__doc__)

    statement = (select(Group.name, Subject.name, func.round(func.avg(Grade.grade), 2))
                 .join(Student, Student.group_id == Group.id)
                 .join(Grade, Grade.student_id == Student.id)
                 .join(Subject, Subject.id == Grade.subject_id)
                 .group_by(Group.name)
                 .group_by(Subject.name)
                 .order_by(Group.name)
                 )

    result = session.execute(statement)
    for subj, group, avg_grade in result.all():
        print(subj, group, avg_grade)


def select_4():
    """--- Find the average score on the stream (across the entire grade table) ---"""
    print(select_4.__doc__)

    statement = (select(func.round(func.avg(Grade.grade), 2))
                 )

    result = session.execute(statement)
    print(result.scalar())


def select_5():
    """--- Find what courses a particular teacher is reading ---"""
    print(select_5.__doc__)

    statement = (select(Teacher.fullname, Subject.name)
                 .join(Subject, Subject.teacher_id == Teacher.id)
                 .order_by(Teacher.fullname)
                 )
    result = session.execute(statement)
    for teacher, subj in result.all():
        print(teacher, "\t", subj)


def select_6():
    """--- Find a list of students in a particular group ---"""
    print(select_6.__doc__)

    statement = (select(Group.name, Student.fullname)
                 .join(Student, Student.group_id == Group.id)
                 .where(Group.id == 1)
                 .group_by(Student.id)
                 .group_by(Group.name))

    result = session.execute(statement)
    for group, student in result.all():
        print(group, " | ", student)


def select_7():
    """---- Find the grades of students in an individual group in a particular subject ---"""
    print(select_7.__doc__)

    statement = (select(Subject.name, Group.name, Student.fullname, Grade.grade)
                 .join(Grade, Grade.subject_id == Subject.id)
                 .join(Student, Student.id == Grade.student_id)
                 .join(Group, Group.id == Student.group_id)
                 .where(Group.id == 1)  # you can change the values for "g.id"...
                 .where(Subject.id == 1)  # ...and for "subj.id" to get grades for different groups in different subjects
                 )
    result = session.execute(statement)
    for line in result.all():
        print(line)


def select_8():
    """--- Find the average score that a particular teacher gives in his or her subjects ---"""
    print(select_8.__doc__)

    statement = (select(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2))
                 .join(Subject, Subject.teacher_id == Teacher.id)
                 .join(Grade, Grade.subject_id == Subject.id)
                 .group_by(Teacher.id)
                 .group_by(Subject.name)
                 .order_by(Teacher.id)
                 )
    result = session.execute(statement)
    for teacher, subject, avg_grade in result.all():
        print(teacher, subject, avg_grade)
