import streamlit as st
import json

def dashboard(user="None"):
    st.title("Dashboard")
    st.text(f"Welcome user, {user}!"),
