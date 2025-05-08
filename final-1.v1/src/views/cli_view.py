import os
from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
import re
from utils.constants import EMAIL_REGEX,PASSWORD_REGEX

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_cli():
    while True:
        choice = input("\033[94mUniversity System: (A)dmin, (S)tudent, or X:\033[0m").strip().lower()
        if choice == 'a':
            admin_menu()
        elif choice == 's':
            student_menu()
        elif choice == 'x':
            break
        else:
            input("Invalid option. Press Enter to continue.")

def student_menu():
    controller = StudentController()
    while True:
        choice = input("\t\033[94mStudent System (l/r/x):\033[0m").strip().lower()
        if choice == 'l':
            student_login(controller)
        elif choice == 'r':
            student_register(controller)
        elif choice == 'x':
            break
        else:
            input("Invalid option. Press Enter to continue.")

def student_register(controller):
    print("\t\033[92mStudent Sign Up\033[0m")  # Green
    while True:
        email = input("\tEnter email: ")
        password = input("\tEnter password: ")
        name_part = email.split('@')[0]
        name = ' '.join([part.capitalize() for part in name_part.split('.')])
        success, message = controller.register(name, email, password)
        if success:
            from models.student import Student
            student = next((s for s in controller.students if s.email == email), None)
            print("\t\033[93memail and password formats acceptable\033[0m")  #Yellow
            if student:
                print(f"\tName: {student.name}")
                print(f"\t\033[93mEnrolling Student {student.name}\033[0m") # Yellow
            break
        else:
            if "already registered" in message:
                print(f"\t\033[93memail and password formats acceptable\033[0m")  #Yellow
                print(f"\t\033[91mStudent {name} already exists\033[0m")  # Red
            elif "password" in message.lower() or "email" in message.lower():
                print(f"\t\033[91mIncorrect email or password format\033[0m")  # Red
            else:
                print(message)

def change_password(student, controller):
    print("\t\033[93mUpdating Password\033[0m")  # Yellow

    while True:
        new_pass = input("\tNew Password: ").strip()

        # Validate format
        if not re.match(PASSWORD_REGEX, new_pass):
            print("\t\033[91mIncorrect password format\033[0m")  # Red
            continue

        while True:
            confirm_pass = input("\tConfirm Password: ").strip()
            if new_pass != confirm_pass:
                print("\t\033[91mPassword does not match – try again\033[0m")  # Red
                continue
            break
        # Passed all checks
        student.change_password(new_pass)
        controller.update_student(student)
        break


def student_login(controller):
    print("\t\033[92mStudent Sign In\033[0m")  # Green
    while True: 
        email = input("\tEnter email: ")
        password = input("\tEnter password: ")
    #Check format
        if not re.match(EMAIL_REGEX, email) or not re.match(PASSWORD_REGEX, password):
            print("\t\033[91mIncorrect email or password format\033[0m")  # Red
            continue
        print("\t\033[93memail and password formats acceptable\033[0m")  # Yellow
        #Check login
        student = controller.login(email, password)
        if student:
            subject_enrolment_menu(student, controller)
        else:
            print("\t\033[91mStudent does not exist\033[0m")  # Red
        break 

def subject_enrolment_menu(student, controller):
    while True:
        choice = input("\t\033[94mStudent Course Menu (c/e/r/s/x):\033[0m").strip().lower()
        if choice == 'e':
            if len(student.subjects) >= 4:
                print("\t\033[91mStudents are allowed to enrol in 4 subjects only\033[0m")
                continue
            ok, msg = student.enrol_subject()
            print(f"\t{msg}")
        elif choice == 'r':
            sid = input("\tRemove Subject by ID: ").strip()
            before = len(student.subjects)
            removed = student.remove_subject(sid)
            after = len(student.subjects)
            if removed:
               print(f"\t\033[93mDropping Subject-{sid}\033[0m")
               print(f"\t\033[93mYou are now enrolled in {after} out of 4 subjects\033[0m")
            else:
               print(f"\tSubject::{sid} not found")
        elif choice == 's':
            subjects = student.subjects
            print(f"\t\033[93mShowing {len(subjects)} subjects\033[0m")  # Yellow text
            for s in subjects:
                print(f"\t[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade:>4} ]")
        elif choice == 'c':
            change_password(student, controller)
        elif choice == 'x':
            break
        else:
            print("Invalid choice.")
        controller.update_student(student)

def admin_menu():
    controller = AdminController()
    while True:
        clear()
        print("Welcome to the Admin System")
        print("(c) Clear all student data")
        print("(g) Group students by grade")
        print("(p) Partition students by PASS/FAIL")
        print("(r) Remove a student by ID")
        print("(s) Show all students")
        print("(x) Exit")
        print()
        choice = input("Enter your choice: ").strip().lower()
        if choice == 's':
            print("\nAll Students:")
            print("\n".join(controller.show_all()) or "No students found.")
        elif choice == 'g':
            grade_groups = controller.group_by_grade()
            for grade, names in grade_groups.items():
                print(f"Grade {grade}: {', '.join(set(names))}")
        elif choice == 'p':
            passed, failed = controller.partition_pass_fail()
            print("PASS:", ", ".join(passed))
            print("FAIL:", ", ".join(failed))
        elif choice == 'r':
            sid = input("Enter student ID to remove: ")
            removed = controller.remove_by_id(sid)
            print("Student removed." if removed else "Student ID not found.")
        elif choice == 'c':
            controller.clear_all()
            print("All student data cleared.")
        elif choice == 'x':
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue.")
