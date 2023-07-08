import argparse

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
    if model == "Student":
        if args.name and args.surname and args.group_id:
            model = globals()[model]
            student = model(name=args.name, surname=args.surname, group_id=args.group_id)
            session.add(student)
        else:
            print("\nPlease try again, enter name, surname and group_id\n")
    # ------------------------------------------------------------------------------------
    elif model == "Teacher":
        if args.name and args.surname:
            model = globals()[model]
            teacher = model(name=args.name, surname=args.surname)
            session.add(teacher)
        else:
            print("\nPlease try again, enter name and surname\n")
    # --------------------------------------------------------------------------------------
    elif model == "Subject":
        if args.name and args.teacher_id:
            model = globals()[model]
            subject = model(name=args.name, teacher_id=args.teacher_id)
            session.add(subject)
        else:
            print("\nPlease try again, enter name, surname and group_id\n")
    # ---------------------------------------------------------------------------------------
    elif model in ["Group", "Grade"]:
        if args.name:
            model = globals()[model]
            item = model(name=args.name)
            session.add(item)
        else:
            print("\nPlease try again and enter the name\n")


def read(model):
    ...


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
