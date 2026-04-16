import streamlit as st
import json
from dashboard import dashboard
from bank import bank

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"

def pageUpdate(page):
    st.session_state.page = page

st.sidebar.title("Nav")
st.sidebar.button("Bank", on_click=pageUpdate, args=("bank", ))
st.sidebar.button("Home", on_click=pageUpdate, args=("home", ))

with open("userData.json", "r") as f:
    userData = json.load(f)
def login():
    with st.form("FORM"):
        username = st.text_input("Username:")
        password = st.text_input("Password:")

        submit = st.form_submit_button("Login")
        if submit:
            if username in userData:
              if password == userData[username]:
                  st.session_state.user = username
                  st.session_state.unlocked = True
    st.button("Register", on_click=pageUpdate, args=("register", ))
def register():
    with open("userCoins.json", "r") as f:
        coinsData = json.load(f)
    with st.form("REGI"):
        usernameINP = st.text_input("Username")
        passwordINP = st.text_input("Password")
        submit = st.form_submit_button("Register")
        print("D")
        if submit:
            print("subed")
            userData[usernameINP] = passwordINP
            coinsData[usernameINP] = 100
            with open("userData.json", "w") as f:
                json.dump(userData, f, indent=4)
            with open("userCoins.json", "w") as f:
                json.dump(coinsData, f, indent=4)

            print(userData)
            st.session_state.page = "login"

def home():
    st.text(f"Hi, {st.session_state.user}!")

if st.session_state.unlocked:
    if st.session_state.page == "home":
        dashboard(user=st.session_state.user)
    if st.session_state.page == "bank":
        bank(user=st.session_state.user)
if st.session_state.page == "register":
    register()

if not st.session_state.unlocked:
    if not st.session_state.page == "register":
      login()