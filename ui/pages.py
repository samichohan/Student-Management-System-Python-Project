"""
ui/pages.py
------------
Individual page renderers for each section of the app.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.student import Student, VALID_GRADES, PERFORMANCE_MAP
from services.student_manager import StudentManager
from ui.components import display_students_table, student_form, show_stats_cards


# ── Dashboard ──────────────────────────────────────────────────────────────────

def page_dashboard(manager: StudentManager):
    st.title("🎓 Student Management System")
    st.markdown("---")

    stats = manager.get_statistics()
    show_stats_cards(stats)

    st.markdown("---")

    students = manager.list_students()
    if students:
        st.subheader("📋 All Students")
        display_students_table(students)

        # Grade distribution chart
        if stats.get("grade_distribution"):
            st.subheader("📊 Grade Distribution")
            grade_dist = stats["grade_distribution"]
            fig, ax = plt.subplots(figsize=(5, 3))
            colors = {
                "A": "#28a745", "B": "#17a2b8",
                "C": "#ffc107", "D": "#fd7e14", "F": "#dc3545"
            }
            bar_colors = [colors.get(g, "#6c757d") for g in grade_dist.keys()]
            ax.bar(grade_dist.keys(), grade_dist.values(), color=bar_colors,
                   edgecolor="white", linewidth=1.5)
            ax.set_xlabel("Grade")
            ax.set_ylabel("Number of Students")
            ax.set_title("Students by Grade")
            ax.spines[["top", "right"]].set_visible(False)
            st.pyplot(fig)
    else:
        st.info("👋 Welcome! No students yet. Go to **Add Student** to begin.")


# ── Add Student ────────────────────────────────────────────────────────────────

def page_add_student(manager: StudentManager):
    st.title("➕ Add New Student")
    st.markdown("All fields marked with * are required.")

    data = student_form(key="add_form")

    if data:
        errors = Student.validate(**data)
        if errors:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            student = Student(**data)
            manager.add_student(student)
            st.success(f"✅ Student **{student.name}** added successfully! "
                       f"(ID: `{student.student_id}`)")
            


# ── Update Student ─────────────────────────────────────────────────────────────

def page_update_student(manager: StudentManager):
    st.title("✏️ Update Student")

    students = manager.list_students()
    if not students:
        st.warning("No students available to update.")
        return

    options = {f"{s.name}  [{s.student_id}]": s.student_id for s in students}
    choice = st.selectbox("Select Student to Update", list(options.keys()))
    selected_id = options[choice]
    student = manager.get_student(selected_id)

    if not student:
        st.error("Student not found.")
        return

    st.markdown(f"**Editing:** {student.name} | **ID:** `{student.student_id}`")
    st.markdown("---")

    data = student_form(key="update_form", defaults=student.to_dict())

    if data:
        errors = Student.validate(**data)
        if errors:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            manager.update_student(selected_id, **data)
            st.success(f"✅ Student **{data['name']}** updated successfully!")


# ── Delete Student ─────────────────────────────────────────────────────────────

def page_delete_student(manager: StudentManager):
    st.title("🗑️ Delete Student")

    students = manager.list_students()
    if not students:
        st.warning("No students available to delete.")
        return

    options = {f"{s.name}  [{s.student_id}]": s.student_id for s in students}
    choice = st.selectbox("Select Student to Delete", list(options.keys()))
    selected_id = options[choice]
    student = manager.get_student(selected_id)

    if student:
        st.markdown("### Student Details")
        df = pd.DataFrame([student.to_dict()])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.warning(f"⚠️ Are you sure you want to delete **{student.name}**? "
                   "This action cannot be undone.")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Delete", type="primary", use_container_width=True):
                name = student.name
                manager.delete_student(selected_id)
                st.success(f"✅ Student **{name}** deleted successfully.")
                st.rerun()


# ── Search ─────────────────────────────────────────────────────────────────────

def page_search(manager: StudentManager):
    st.title("🔍 Search Students")

    query = st.text_input("Search by name, email, subject, or ID",
                          placeholder="Type to search...")

    if query:
        results = manager.search(query)
        display_students_table(results, title=f"Results for '{query}'")
    else:
        st.info("Enter a search term above to find students.")


# ── Filter ─────────────────────────────────────────────────────────────────────

def page_filter(manager: StudentManager):
    st.title("🎛️ Filter Students")

    with st.expander("🔧 Filter Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            grade = st.selectbox("Grade", ["All"] + VALID_GRADES)
            performance = st.selectbox(
                "Performance",
                ["All"] + list(PERFORMANCE_MAP.values())
            )
        with col2:
            min_age = st.number_input("Min Age", 5, 100, 5)
            max_age = st.number_input("Max Age", 5, 100, 100)
        with col3:
            min_marks = st.number_input("Min Marks", 0.0, 100.0, 0.0)
            max_marks = st.number_input("Max Marks", 0.0, 100.0, 100.0)

    results = manager.filter_students(
        grade=grade,
        min_age=min_age,
        max_age=max_age,
        min_marks=min_marks,
        max_marks=max_marks,
        performance=performance,
    )
    display_students_table(results, title="Filtered Results")
