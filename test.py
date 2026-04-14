import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation function
def go_to(page_name):
    st.session_state.page = page_name

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.button("Home", on_click=go_to, args=("home",))
st.sidebar.button("About", on_click=go_to, args=("about",))
st.sidebar.button("Dashboard", on_click=go_to, args=("dashboard",))

# Page content
def home():
    st.title("Home Page")
    st.write("Welcome!")

def about():
    st.title("About Page")
    st.write("This is a custom multipage app.")

def dashboard():
    st.title("Dashboard")
    st.write("Data goes here 📊")

# Router
if st.session_state.page == "home":
    home()
elif st.session_state.page == "about":
    about()
elif st.session_state.page == "dashboard":
    dashboard()