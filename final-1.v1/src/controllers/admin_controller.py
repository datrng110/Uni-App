from models.database import Database

class AdminController:
    def __init__(self):
        self.db = Database()
        self.students = self.db.load_students()

    def show_all(self):
        return [
            f"{s.id} - {s.name} - {s.email} - Subjects: {len(s.subjects)} - Avg: {s.get_average():.2f}"
            for s in self.students
        ]

    def group_by_grade(self):
        grade_groups = {}
        for s in self.students:
            for sub in s.subjects:
                grade_groups.setdefault(sub.grade, []).append(s.name)
        return grade_groups

    def partition_pass_fail(self):
        passed = [s.name for s in self.students if s.is_pass()]
        failed = [s.name for s in self.students if not s.is_pass()]
        return passed, failed

    def remove_by_id(self, student_id):
        before = len(self.students)
        self.students = [s for s in self.students if s.id != student_id]
        self.db.save_students(self.students)
        return len(self.students) < before

    def clear_all(self):
        self.students = []
        self.db.clear()
        return True

# Ensures this module is treated as a package
__all__ = ['AdminController']
