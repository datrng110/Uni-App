import os
from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
import re
from utils.constants import PASSWORD_REGEX

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_cli():
    while True:
        clear()
        print("Welcome to the University System")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")
        print()
        choice = input("Enter your choice: ").strip().lower()
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
        clear()
        print("Welcome to the Student System")
        print("(l) login")
        print("(r) register")
        print("(x) exit")
        print()
        choice = input("Enter your choice: ").strip().lower()
        if choice == 'l':
            student_login(controller)
        elif choice == 'r':
            student_register(controller)
        elif choice == 'x':
            break
        else:
            input("Invalid option. Press Enter to continue.")

def student_register(controller):
    print("\nStudent Registration")
    name = input("Enter full name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    success, message = controller.register(name, email, password)
    print()
    if success:
        from models.student import Student
        student = next((s for s in controller.students if s.email == email), None)
        print("Registration successful!")
        if student:
            print(f"Your student ID is: {student.id}")
    else:
        if "email" in message:
            print("Invalid email. Must be firstname.lastname@university.com")
        elif "password" in message:
            print("Invalid password. Must start with uppercase, have 5+ letters and 3+ digits.")
        else:
            print(message)
    input("Press Enter to continue.")

def change_password(student, controller):
    print("\033[93mUpdating Password\033[0m")  # Yellow

    while True:
        new_pass = input("New Password: ").strip()
        confirm_pass = input("Confirm Password: ").strip()

        # Validate format
        if not re.match(PASSWORD_REGEX, new_pass):
            print("\033[91mInvalid password format\033[0m")  # Red
            continue

        if new_pass != confirm_pass:
            print("\033[91mPassword does not match - try again\033[0m")  # Red
            continue

        # Passed all checks
        student.change_password(new_pass)
        controller.update_student(student)
        break


def student_login(controller):
    print("\nStudent Login")
    email = input("Enter email: ")
    password = input("Enter password: ")
    student = controller.login(email, password)
    if student:
        print(f"\nLogin successful. Welcome, {student.name}!")
        input("Press Enter to continue.")
        subject_enrolment_menu(student, controller)
    else:
        print("\nLogin failed. Please check your credentials.")
        input("Press Enter to continue.")

def subject_enrolment_menu(student, controller):
    while True:
        clear()
        print("Subject Enrolment System")
        print("(e) Enrol a subject")
        print("(r) Remove a subject")
        print("(s) Show enrolled subjects")
        print("(c) Change password")
        print("(x) Exit")
        print()
        choice = input("Enter your choice: ").strip().lower()
        if choice == 'e':
            ok, msg = student.enrol_subject()
            print(msg)
        elif choice == 'r':
            sid = input("Remove Subject by ID: ").strip()
            before = len(student.subjects)
            removed = student.remove_subject(sid)
            after = len(student.subjects)
            if removed:
               print(f"Droping Subject:{sid}")
               print(f"You are now enrolled in {after} out of 4 subjects")
            else:
               print(f"Subject-{sid} not found")
        elif choice == 's':
            subjects = student.subjects
            print(f"\033[93mShowing {len(subjects)} subjects\033[0m")  # Yellow text
            for s in subjects:
                print(f"[ Subject::{s.id} - mark = {s.mark} - grade = {s.grade:>4} ]")
        elif choice == 'c':
            change_password(student, controller)
        elif choice == 'x':
            break
        else:
            print("Invalid choice.")
        controller.update_student(student)
        input("Press Enter to continue.")

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
