import argparse
from datetime import datetime


from models import Group, Student, Teacher, Subject, Grade
from db_connect import session


def get_args():
    parser = argparse.ArgumentParser("CLI CRUD for SQLAlchemy")
    parser.add_argument("-a", "--action", help="Please select the desired action from the following list: create, read, update, delete.")
    parser.add_argument("-m", "--model", help="Please select the model: Group, Student, Teacher, Subject or Grade")
    parser.add_argument("-n", "--name", help="Name of group or name of subject | OR first student's or teacher's name")
    parser.add_argument("-s", "--surname", help="Last student's or teacher's name")
    parser.add_argument("-i", "--id", help="ID of model")
    parser.add_argument("-g", "--group_id", help="This argument is used only for students and shows the group of student")
    parser.add_argument("-t", "--teacher_id", help="This argument is used only for subjects and shows who is the teacher of this subject")
    parser.add_argument("--grade", help="Grade (1, 2, 3, 4 or 5) for a student in a particular subject")
    parser.add_argument("--student_id", help="This argument is only used for grades and shows the id of the student receiving the grade.")
    parser.add_argument("--subject_id", help="This argument is only used for grades and shows the id of the course being graded.")

    args = parser.parse_args()
    return args


def arg_handler(arguments):
    if arguments.action in ["create", "read", "update", "delete"]:  # checking action

        if arguments.model in ["Group", "Student", "Teacher", "Subject", "Grade"]:  # checking model
            return True
        else:
            print("\nWrong model. Please try again\n")
            exit(1)

    else:
        print("\nSomething went wrong... Try again\n")
        exit(2)


def create(model, args):
    match model:
        case "Student":
            if args.name and args.surname and args.group_id:
                student = Student(name=args.name, surname=args.surname, group_id=args.group_id)
                session.add(student)
            else:
                print("\nPlease try again, enter name, surname and group_id\n")
    # ------------------------------------------------------------------------------------
        case "Teacher":
            if args.name and args.surname:
                teacher = Teacher(name=args.name, surname=args.surname)
                session.add(teacher)
            else:
                print("\nPlease try again, enter name and surname\n")
    # --------------------------------------------------------------------------------------
        case "Subject":
            if args.name and args.teacher_id:
                subject = Subject(name=args.name, teacher_id=args.teacher_id)
                session.add(subject)
            else:
                print("\nPlease try again, enter name, surname and group_id\n")
    # ---------------------------------------------------------------------------------------
        case "Grade":
            if args.grade and args.student_id and args.subject_id:
                today = datetime.today().strftime("%Y-%m-%d")
                grade = Grade(grade=args.grade, date_of=today, student_id=args.student_id, subject_id=args.subject_id)
                session.add(grade)
            else:
                print("\nPlease try again. Enter grade, student_id and subject_id\n")
    # --------------------------------------------------------------------------------------
        case "Group":
            if args.name:
                item = Group(name=args.name)
                session.add(item)
            else:
                print("\nPlease try again and enter the name\n")


def read(model):



def update(model):
    ...


def delete(model):
    ...


def main():
    arguments = get_args()

    if arg_handler(arguments):
        func = eval(arguments.action)  # converting a String to a Function
        model = arguments.model

        func(model, arguments)  # calling one of CRUDs function and pass "arguments" to it

        session.commit()


if __name__ == '__main__':
    main()