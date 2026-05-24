"""
ui/components.py
-----------------
Reusable UI helper functions for Streamlit pages.
"""

import pandas as pd
import streamlit as st
from models.student import Student, VALID_GRADES


# ── Table display ──────────────────────────────────────────────────────────────

def display_students_table(students: list[Student], title: str = "Students"):
    if not students:
        st.info("📭 No students found.")
        return

    st.markdown(f"**{title}** — {len(students)} record(s)")
    rows = [s.to_dict() for s in students]
    df = pd.DataFrame(rows)

    # Rename for presentation
    df = df.rename(columns={
        "student_id": "ID",
        "name": "Name",
        "age": "Age",
        "grade": "Grade",
        "subject": "Subject",
        "marks": "Marks",
        "email": "Email",
        "performance": "Performance",
        "created_at": "Added On",
    })

    # Color-code performance column
    def color_performance(val):
        colors = {
            "Excellent": "background-color: #d4edda; color: #155724;",
            "Good": "background-color: #cce5ff; color: #004085;",
            "Average": "background-color: #fff3cd; color: #856404;",
            "Below Average": "background-color: #ffe5d0; color: #7d3c00;",
            "Failing": "background-color: #f8d7da; color: #721c24;",
        }
        return colors.get(val, "")

    styled = df.style.map(color_performance, subset=["Performance"])
    st.dataframe(styled, use_container_width=True, hide_index=True)


# ── Student form ───────────────────────────────────────────────────────────────

def student_form(key: str, defaults: dict = None) -> dict | None:
    """
    Renders an add/edit form. Returns form data dict on submit, else None.
    """
    d = defaults or {}
    with st.form(key=key, clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", value=d.get("name", ""))
            age = st.number_input("Age *", min_value=5, max_value=100,
                                  value=int(d.get("age", 18)))
            grade = st.selectbox("Grade *", VALID_GRADES,
                                 index=VALID_GRADES.index(d.get("grade", "A"))
                                 if d.get("grade") in VALID_GRADES else 0)
        with col2:
            subject = st.text_input("Subject *", value=d.get("subject", ""))
            marks = st.number_input("Marks (0–100) *", min_value=0.0,
                                    max_value=100.0, step=0.5,
                                    value=float(d.get("marks", 0.0)))
            email = st.text_input("Email *", value=d.get("email", ""))

        submitted = st.form_submit_button("💾 Save Student",
                                          use_container_width=True)
        if submitted:
            return {
                "name": name.strip(),
                "age": age,
                "grade": grade,
                "subject": subject.strip(),
                "marks": marks,
                "email": email.strip(),
            }
    return None


# ── Metric cards ───────────────────────────────────────────────────────────────

def show_stats_cards(stats: dict):
    if not stats:
        st.info("No data to display statistics.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Students", stats.get("total", 0))
    c2.metric("📊 Avg Marks", stats.get("avg_marks", 0))
    c3.metric("🏆 Highest Marks", stats.get("highest_marks", 0))
    c4.metric("📉 Lowest Marks", stats.get("lowest_marks", 0))

    c5, c6, c7 = st.columns(3)
    c5.metric("🎂 Avg Age", stats.get("avg_age", 0))
    c6.metric("🥇 Top Student", stats.get("top_student", "—"))

    grade_dist = stats.get("grade_distribution", {})
    if grade_dist:
        c7.metric("📋 Grade Spread",
                  " | ".join(f"{g}:{n}" for g, n in sorted(grade_dist.items())))
