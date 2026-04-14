import streamlit as st
import json

with open("userData.json", "r") as f:
    userData = json.load(f)

def dashboard():
    st.text(f"dashboard")
