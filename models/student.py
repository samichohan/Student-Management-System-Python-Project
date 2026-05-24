"""
models/student.py
-----------------
Student data model with validation logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


VALID_GRADES = ["A", "B", "C", "D", "F"]
PERFORMANCE_MAP = {
    "A": "Excellent",
    "B": "Good",
    "C": "Average",
    "D": "Below Average",
    "F": "Failing",
}


@dataclass
class Student:
    name: str
    age: int
    grade: str
    subject: str
    marks: float
    email: str
    student_id: Optional[str] = field(default=None)
    created_at: Optional[str] = field(default=None)

    def __post_init__(self):
        if self.student_id is None:
            self.student_id = self._generate_id()
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.grade = self.grade.upper()

    def _generate_id(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"STU-{timestamp[-8:]}"

    @property
    def performance(self) -> str:
        return PERFORMANCE_MAP.get(self.grade, "Unknown")

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "subject": self.subject,
            "marks": self.marks,
            "email": self.email,
            "performance": self.performance,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            student_id=data.get("student_id"),
            name=data["name"],
            age=int(data["age"]),
            grade=data["grade"],
            subject=data["subject"],
            marks=float(data["marks"]),
            email=data["email"],
            created_at=data.get("created_at"),
        )

    @staticmethod
    def validate(name: str, age: int, grade: str, subject: str,
                 marks: float, email: str) -> list[str]:
        errors = []

        if not name or len(name.strip()) < 2:
            errors.append("Name must be at least 2 characters long.")
        if not name.replace(" ", "").isalpha():
            errors.append("Name must contain only alphabets.")

        if not (5 <= age <= 100):
            errors.append("Age must be between 5 and 100.")

        if grade.upper() not in VALID_GRADES:
            errors.append(f"Grade must be one of: {', '.join(VALID_GRADES)}.")

        if not subject or len(subject.strip()) < 2:
            errors.append("Subject must be at least 2 characters long.")

        if not (0 <= marks <= 100):
            errors.append("Marks must be between 0 and 100.")

        if "@" not in email or "." not in email.split("@")[-1]:
            errors.append("Please enter a valid email address.")

        return errors
