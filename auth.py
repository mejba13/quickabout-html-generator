# auth.py
import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")

# Session timeout in minutes
SESSION_DURATION = 30

def login_form():
    st.title("🔐 QuickAbout Login")
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["login_time"] = datetime.now()
            st.rerun()
        else:
            st.error("Invalid username or password")

def is_authenticated():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        login_time = st.session_state.get("login_time")
        if login_time and datetime.now() - login_time < timedelta(minutes=SESSION_DURATION):
            return True
        else:
            st.warning("Session expired. Please log in again.")
            st.session_state.clear()
            return False
    return False

def logout_button():
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
