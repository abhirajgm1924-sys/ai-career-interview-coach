import streamlit as st

st.title("AI Career Interview Coach")

role = st.selectbox(
    "Select Role",
    [
        "Data Analyst",
        "Data Engineer",
        "Data Scientist",
        "Business Analyst",
        "Analytics Engineer",
        "ML Engineer"
    ]
)

st.write(f"Selected Role: {role}")