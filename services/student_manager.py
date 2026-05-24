"""
services/student_manager.py
----------------------------
Manager class: handles all CRUD operations and JSON storage.
"""

import json
import os
from typing import Optional
from models.student import Student


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "students.json")


class StudentManager:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = os.path.abspath(filepath)
        self._students: dict[str, Student] = {}
        self._load()

    # ── Private helpers ────────────────────────────────────────────────────────

    def _load(self):
        """Load students from JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._students = {
                    sid: Student.from_dict(data)
                    for sid, data in raw.items()
                }
            except (json.JSONDecodeError, KeyError):
                self._students = {}
        else:
            self._students = {}

    def _save(self):
        """Persist all students to JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(
                {sid: s.to_dict() for sid, s in self._students.items()},
                f,
                indent=2,
                ensure_ascii=False,
            )

    # ── CRUD ───────────────────────────────────────────────────────────────────

    def add_student(self, student: Student) -> Student:
        """Add a new student and persist."""
        self._students[student.student_id] = student
        self._save()
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a single student by ID."""
        return self._students.get(student_id)

    def update_student(self, student_id: str, **kwargs) -> Optional[Student]:
        """Update fields of an existing student."""
        student = self._students.get(student_id)
        if not student:
            return None

        # Update only provided fields
        updatable = ["name", "age", "grade", "subject", "marks", "email"]
        for key, value in kwargs.items():
            if key in updatable:
                setattr(student, key, value)

        # Normalize grade
        student.grade = student.grade.upper()
        self._save()
        return student

    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID."""
        if student_id in self._students:
            del self._students[student_id]
            self._save()
            return True
        return False

    def list_students(self) -> list[Student]:
        """Return all students sorted by name."""
        return sorted(self._students.values(), key=lambda s: s.name.lower())

    # ── Search & Filter ────────────────────────────────────────────────────────

    def search(self, query: str) -> list[Student]:
        """Full-text search across name, email, subject, and student_id."""
        q = query.lower().strip()
        return [
            s for s in self._students.values()
            if q in s.name.lower()
            or q in s.email.lower()
            or q in s.subject.lower()
            or q in s.student_id.lower()
        ]

    def filter_students(
        self,
        grade: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        min_marks: Optional[float] = None,
        max_marks: Optional[float] = None,
        performance: Optional[str] = None,
    ) -> list[Student]:
        """Filter students by multiple criteria."""
        results = list(self._students.values())

        if grade and grade != "All":
            results = [s for s in results if s.grade == grade.upper()]
        if min_age is not None:
            results = [s for s in results if s.age >= min_age]
        if max_age is not None:
            results = [s for s in results if s.age <= max_age]
        if min_marks is not None:
            results = [s for s in results if s.marks >= min_marks]
        if max_marks is not None:
            results = [s for s in results if s.marks <= max_marks]
        if performance and performance != "All":
            results = [s for s in results if s.performance == performance]

        return sorted(results, key=lambda s: s.name.lower())

    # ── Stats ──────────────────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        """Return aggregate statistics about all students."""
        students = list(self._students.values())
        if not students:
            return {}

        marks_list = [s.marks for s in students]
        grade_dist = {}
        for s in students:
            grade_dist[s.grade] = grade_dist.get(s.grade, 0) + 1

        return {
            "total": len(students),
            "avg_marks": round(sum(marks_list) / len(marks_list), 2),
            "highest_marks": max(marks_list),
            "lowest_marks": min(marks_list),
            "avg_age": round(sum(s.age for s in students) / len(students), 1),
            "grade_distribution": grade_dist,
            "top_student": max(students, key=lambda s: s.marks).name,
        }
