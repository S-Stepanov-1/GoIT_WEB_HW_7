from sqlalchemy import func, desc, select

from models import Student, Teacher, Group, Subject, Grade
from db_connect import session

from prettytable import PrettyTable


def handle_input():
    while True:
        try:
            q_num = int(input("Please enter the query number you want to perform: "))
            if 1 <= q_num <= 12:  # we have only 11 queries to DB in this task
                return q_num
            else:
                print("\nThe query number must be from 1 to 11. Try again.\n")
        except ValueError:
            print("\nPlease use integer number like 1, 2, 3...\n")


def set_subj():
    subject = input("Please, enter a subject id from the list\nPhysics: 1\nMaths: 2\nArt: 3\n"
                    "PE: 4\nPhilosophy:5\nIT: 6\n>>>")
    return subject


def select_1():
    """--- Find the 5 students with the highest grade point average in all subjects ---"""
    print(select_1.__doc__)
    statement = (select(Student.fullname, Group.name, func.round(func.avg(Grade.grade), 2).label("average_grade"))
                 .join(Group)
                 .join(Grade)
                 .group_by(Student.id)
                 .group_by(Group.name)
                 .order_by(desc("average_grade"))
                 .limit(5)
                 )

    result = session.execute(statement)
    return result.all()


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
    return result.all()


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
    return result.all()


def select_4():
    """--- Find the average score on the stream (across the entire grade table) ---"""
    print(select_4.__doc__)

    statement = (select(func.round(func.avg(Grade.grade), 2)))

    result = session.execute(statement)
    return result.all()


def select_5():
    """--- Find what courses a particular teacher is reading ---"""
    print(select_5.__doc__)

    statement = (select(Teacher.fullname, Subject.name)
                 .join(Subject, Subject.teacher_id == Teacher.id)
                 .order_by(Teacher.fullname)
                 )

    result = session.execute(statement)
    return result.all()


def select_6():
    """--- Find a list of students in a particular group ---"""
    print(select_6.__doc__)

    statement = (select(Group.name, Student.fullname)
                 .join(Student, Student.group_id == Group.id)
                 .where(Group.id == 1)
                 .group_by(Student.id)
                 .group_by(Group.name))

    result = session.execute(statement)
    return result.all()


def select_7():
    """---- Find the grades of students in an individual group in a particular subject ---"""
    print(select_7.__doc__)

    statement = (select(Subject.name, Group.name, Student.fullname, Grade.grade)
                 .join(Grade, Grade.subject_id == Subject.id)
                 .join(Student, Student.id == Grade.student_id)
                 .join(Group, Group.id == Student.group_id)
                 .where(Group.id == 1)  # you can change the values for "g.id"...
                 .where(Subject.id == 1)
                 # ...and for "subj.id" to get grades for different groups in different subjects
                 )
    result = session.execute(statement)
    return result.all()


def select_8():
    """--- Find the average score that a particular teacher gives in his or her subjects ---"""
    print(select_8.__doc__)

    statement = (select(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2))
                 .join(Subject, Teacher.id == Subject.teacher_id)
                 .join(Grade, Grade.subject_id == Subject.id)
                 .group_by(Teacher.id)
                 .group_by(Subject.name)
                 .order_by(Teacher.id)
                 )
    result = session.execute(statement)
    return result.all()


def select_9():
    """--- Find a list of the courses a particular student is taking ---"""
    print(select_9.__doc__)

    statement = (select(Student.fullname, Subject.name)
                 .join(Grade, Student.id == Grade.student_id)
                 .join(Subject, Subject.id == Grade.subject_id)
                 # .where(Student.id == 1)  # uncomment this line and change Student.id to get info about each particular student
                 .group_by(Student.id)
                 .group_by(Subject.id)
                 .order_by(Student.name)
                 )
    result = session.execute(statement)
    return result.all()


def select_10():
    """--- A list of courses that a particular student is taught by a particular teacher ---"""
    print(select_10.__doc__)

    statement = (select(Teacher.fullname, Student.fullname, Subject.name)
                 .join(Subject, Teacher.id == Subject.teacher_id)
                 .join(Grade, Subject.id == Grade.subject_id)
                 .join(Student, Student.id == Grade.student_id)
                 # uncomment 2 next lines and change Student.id and Teacher.id to get a list of subjects that a particular student is taught by a particular teacher
                 # .where(Student.id == 10)
                 # .where(Teacher.id == 2)
                 .group_by(Student.id).group_by(Teacher.id).group_by(Subject.id)
                 .order_by(Student.id)
                 )
    result = session.execute(statement)
    return result.all()


def select_11():
    """--- The average score that a particular teacher gives to a particular student in each course ---"""
    print(select_11.__doc__)

    statement = (select(Student.fullname, Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2))
                 .join(Grade, Student.id == Grade.student_id)
                 .join(Subject, Subject.id == Grade.subject_id)
                 .join(Teacher, Teacher.id == Subject.teacher_id)
                 # change Teacher.id & Student.id to find the average score
                 # that a particular teacher gives to a particular student in each course
                 .where(Teacher.id == 2)
                 .where(Student.id == 5)
                 .group_by(Teacher.id)
                 .group_by(Student.id)
                 .group_by(Subject.name)
                 )
    result = session.execute(statement)
    return result.all()


def select_12():
    """--- The grades of students in a particular group in a particular subject in the last class ---"""
    print(select_12.__doc__)

    group_id = input("Enter a group id: >>> ")
    subject_id = input("Enter a subject id: >>> ")

    # firstly we should find the last class for the given group and subject
    sub_query = (select(Grade.date_of)
                 .join(Student)
                 .join(Group, Group.id == group_id)
                 .where(Grade.subject_id == subject_id)
                 .order_by(desc(Grade.date_of))
                 .limit(1)).scalar_subquery()

    statement = (select(Group.name, Subject.name, Student.fullname, Grade.date_of, Grade.grade)
                 .join(Student, Student.group_id == Group.id)
                 .join(Grade, Grade.student_id == Student.id)
                 .join(Subject, Subject.id == Grade.subject_id)
                 .where(Grade.subject_id == subject_id)
                 .where(Group.id == group_id)
                 .where(Grade.date_of == sub_query)
                 .order_by(desc(Grade.date_of))
                 )

    result = session.execute(statement)
    return result.all()


def main():
    functions = {1: select_1, 2: select_2, 3: select_3, 4: select_4, 5: select_5, 6: select_6,
                 7: select_7, 8: select_8, 9: select_9, 10: select_10, 11: select_11, 12: select_12
                 }

    query_number = handle_input()
    list_result = functions[query_number]()  # calling the 'select_X' function according to query_number

    table = PrettyTable(header=False)
    for lst in list_result:
        table.add_row(lst)
    print(table)


if __name__ == '__main__':
    main()
