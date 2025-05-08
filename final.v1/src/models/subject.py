import random

class Subject:
    def __init__(self, subject_id=None, mark=None):
        self.id = subject_id or f"{random.randint(1, 999):03d}"
        self.mark = mark or random.randint(25, 100)
        self.grade = self.get_grade()

    def get_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'F'

    def to_dict(self):
        return {"id": self.id, "mark": self.mark, "grade": self.grade}

    @staticmethod
    def from_dict(data):
        return Subject(subject_id=data['id'], mark=data['mark'])
