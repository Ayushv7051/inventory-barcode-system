import streamlit as st
import runpy

# --- Dummy Users (replace with DB later if needed) ---
USERS = {
    "staff": {"password": "1234", "role": "reader"},
    "normal staff": {"password": "admin123", "role": "straam"},
    "admin": {"password": "admin123", "role": "straam"}
}

st.set_page_config(page_title="Login", layout="centered")

# --- Initialize session state ---
if "loggedin" not in st.session_state:
    st.session_state.loggedin = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- Login Page ---
def login_page():
    st.title("Staff Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.loggedin = True
            st.session_state.role = USERS[username]["role"]
            st.session_state.username = username
            st.rerun()  # redirect immediately
        else:
            st.error("Invalid credentials")

# --- Logout Button ---
def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.loggedin = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

# --- Role-based Redirect ---
if not st.session_state.loggedin:
    login_page()
else:
    st.sidebar.success(f"Welcome {st.session_state.username} ({st.session_state.role})")
    logout_button()
    
    if st.session_state.role == "reader":
        runpy.run_path("reader.py")
    elif st.session_state.role == "straam":
        runpy.run_path("straam.py")
