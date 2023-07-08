import argparse

from models import Group, Student, Teacher, Subject, Grade
from db_connect import session


def get_args():
    parser = argparse.ArgumentParser("CLI CRUD for SQLAlchemy")
    parser.add_argument("-a", "--action", help="Please select the desired action from the following list: create, read, update, delete.")
    parser.add_argument("-m", "--model", help="Please select the model: Group, Student, Teacher, Subject or Grade")

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


def create(model):


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

        func(model)  # calling one of CRUDs function and pass "arguments" to it


if __name__ == '__main__':
    main()
