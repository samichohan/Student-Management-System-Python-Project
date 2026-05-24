<<<<<<< HEAD
# 🎓 Student Management System

A complete Student Management System built with **Python OOP** and **Streamlit**.

Live App: https://student-management-system-python-project.streamlit.app/

## 📁 Project Structure

```
student_mgmt/
├── app.py                  # Main entry point
├── requirements.txt
├── data/
│   └── students.json       # JSON storage (auto-created)
├── models/
│   ├── __init__.py
│   └── student.py          # Student dataclass + validation
├── services/
│   ├── __init__.py
│   └── student_manager.py  # CRUD + search + filter logic
└── ui/
    ├── __init__.py
    ├── components.py        # Reusable UI widgets
    └── pages.py             # One function per page
```

## ⚙️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## ✨ Features

- **Dashboard** — stats cards + grade distribution chart
- **Add Student** — validated form, auto ID generation
- **Update Student** — select & edit any student
- **Delete Student** — confirmation before delete
- **Search** — search by name, email, subject, or ID
- **Filter** — filter by grade, age range, marks range, performance

## 🗄️ Storage

All data is saved in `data/students.json` automatically. 8 sample students are included.

## ✅ Validation Rules

| Field   | Rule |
|---------|------|
| Name    | Min 2 chars, alphabets only |
| Age     | 5 – 100 |
| Grade   | A, B, C, D, or F |
| Marks   | 0 – 100 |
| Email   | Must contain @ and domain |
=======
# Student-Management-System-Project
>>>>>>> 307895e72e9d0f7e5cec30462b903a41611c500d
