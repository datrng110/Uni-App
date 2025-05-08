import random
from typing import List
from models.subject import Subject

class Student:
    def __init__(self, name, email, password, student_id=None, subjects=None):
        self.id = student_id or f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects: List[Subject] = subjects or []

    def enrol_subject(self):
        if len(self.subjects) >= 4:
            return False, "\t\033[91mStudents are allowed to enrol in 4 subjects only\033[0m"
        subject = Subject()
        self.subjects.append(subject)
        msg = (
            f"\033[93mEnrolling in Subject–{subject.id}\033[0m\n"
            f"\t\033[93mYou are now enrolled in {len(self.subjects)} out of 4 subjects\033[0m"
)
        return True, msg

    def remove_subject(self, subject_id):
        before = len(self.subjects)
        self.subjects = [s for s in self.subjects if s.id != subject_id]
        return len(self.subjects) < before

    def change_password(self, new_password):
        self.password = new_password

    def get_average(self):
        if not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def is_pass(self):
        return self.get_average() >= 50

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects]
        }

    @staticmethod
    def from_dict(data):
        subjects = [Subject.from_dict(s) for s in data.get("subjects", [])]
        return Student(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            student_id=data["id"],
            subjects=subjects
        )
