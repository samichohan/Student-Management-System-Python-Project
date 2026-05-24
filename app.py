"""
app.py
------
Main entry point for the Student Management System.
Run with: streamlit run app.py
"""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from services.student_manager import StudentManager
from ui.pages import (
    page_dashboard,
    page_add_student,
    page_update_student,
    page_delete_student,
    page_search,
    page_filter,
)

# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 12px;
        border-left: 4px solid #0f3460;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Form styling */
    .stForm {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
    }

    /* Title */
    h1 {
        color: #0f3460;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────

@st.cache_resource
def get_manager():
    return StudentManager()

manager = get_manager()

# ── Sidebar navigation ─────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎓 SMS")
    st.markdown("**Student Management System**")
    st.markdown("---")

    total = len(manager.list_students())
    st.markdown(f"📊 **Total Students:** `{total}`")
    st.markdown("---")

    nav = st.radio(
        "Navigation",
        options=[
            "🏠  Dashboard",
            "➕  Add Student",
            "✏️  Update Student",
            "🗑️  Delete Student",
            "🔍  Search",
            "🎛️  Filter",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<small style='opacity:0.5'>Built with Python OOP + Streamlit</small>",
        unsafe_allow_html=True,
    )

# ── Route to page ──────────────────────────────────────────────────────────────

page_map = {
    "🏠  Dashboard": page_dashboard,
    "➕  Add Student": page_add_student,
    "✏️  Update Student": page_update_student,
    "🗑️  Delete Student": page_delete_student,
    "🔍  Search": page_search,
    "🎛️  Filter": page_filter,
}

page_map[nav](manager)
