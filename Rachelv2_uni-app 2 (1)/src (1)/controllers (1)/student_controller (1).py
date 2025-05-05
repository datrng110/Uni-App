import re
from models.student import Student
from models.database import Database
from utils.constants import EMAIL_REGEX, PASSWORD_REGEX

class StudentController:
    def __init__(self):
        self.db = Database()
        self.students = self.db.load_students()

    def register(self, name, email, password):
        if not re.match(EMAIL_REGEX, email):
            return False, "Invalid email format."
        if not re.match(PASSWORD_REGEX, password):
            return False, "Invalid password format."
        if any(s.email == email for s in self.students):
            return False, "Email already registered."
        student = Student(name, email, password)
        self.students.append(student)
        self.db.save_students(self.students)
        return True, "Registration successful."

    def login(self, email, password):
        for student in self.students:
            if student.email == email and student.password == password:
                return student
        return None

    def update_student(self, student):
        for i, s in enumerate(self.students):
            if s.id == student.id:
                self.students[i] = student
                self.db.save_students(self.students)
                break
