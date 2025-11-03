import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Physics Programming", page_icon="🧠")

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "projects")
projects = [f for f in os.listdir(PROJECTS_DIR) if f.endswith(".py")]

st.title("🧠 Physics Programming")
st.write("Select a project to run:")

selected = st.selectbox("Available projects:", projects)

if st.button("▶ Run project"):
    st.info(f"Running {selected}...")

    script_path = os.path.join(PROJECTS_DIR, selected)

    result = subprocess.run(
        ["python", script_path],
        capture_output=True,
        text=True
    )

    st.subheader("📜 Program output:")
    st.code(result.stdout or "(no output)", language="python")

    if result.stderr:
        st.error(result.stderr)
