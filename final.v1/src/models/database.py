import os
import json
from models.student import Student
from utils.constants import STUDENT_FILE

class Database:
    def __init__(self):
        self.file_path = STUDENT_FILE

    def load_students(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as f:
            try:
                data = json.load(f)
                return [Student.from_dict(s) for s in data]
            except json.JSONDecodeError:
                return []

    def save_students(self, students):
        with open(self.file_path, 'w') as f:
            json.dump([s.to_dict() for s in students], f, indent=2)

    def clear(self):
        open(self.file_path, 'w').close()
