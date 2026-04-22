import streamlit as st
from gamble import gamble
from supabase import create_client
from dashboard import dashboard
from bank import bank
from gamble import custom
import streamlit.components.v1 as components

components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4881378862565200"
crossorigin="anonymous"></script>
""", height=0)

# Supabase Setup
url = "https://obcxepcywkmrcptxpwbq.supabase.co"
key = "sb_publishable__9MoOR67yL294bkkMM--Zg_wc3JK9cf"
db = create_client(url, key)

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"
if "odds" not in st.session_state:
    st.session_state.odds = None
if "amount" not in st.session_state:
    st.session_state.amount = None

def pageUpdate(page):
    st.session_state.page = page

st.sidebar.title("Nav")
st.sidebar.button("Bank", on_click=pageUpdate, args=("bank",))
st.sidebar.button("Home", on_click=pageUpdate, args=("home",))
st.sidebar.button("Gamble", on_click=pageUpdate, args=("gamble", ))
# Pull data from Supabase into dictionaries
res = db.table("users").select("*").execute()
userCoins = {row["username"]: row["coins"] for row in res.data}
userData = {row["username"]: row["password"] for row in res.data}
# Full row data for internal use if needed
fullUserData = {row["username"]: row for row in res.data}


def login():
    with st.form("FORM"):
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        submit = st.form_submit_button("Login")
        if submit:
            if username in userData:
                if password == userData[username]:
                    st.session_state.user = username
                    st.session_state.unlocked = True
                    st.rerun()
    st.button("Register", on_click=pageUpdate, args=("register",))


def register():
    with st.form("REGI"):
        usernameINP = st.text_input("Username")
        passwordINP = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            # Insert into Supabase instead of writing to JSON
            db.table("users").insert({
                "username": usernameINP,
                "password": passwordINP,
                "coins": 100,  # Default starting coins
                "bank": 0
            }).execute()

            st.success("Registered!")
            st.session_state.page = "login"
            st.rerun()


def home():
    st.text(f"Hi, {st.session_state.user}!")


if st.session_state.unlocked:
    if st.session_state.page == "home":
        dashboard(user=st.session_state.user)
    if st.session_state.page == "bank":
        bank(user=st.session_state.user)
    if st.session_state.page == "gamble":
        gamble(user=st.session_state.user)
    if st.session_state.page == "custom":
        custom(user=st.session_state.user, coins=userCoins[st.session_state.user])

if st.session_state.page == "register":
    register()

if not st.session_state.unlocked:
    if not st.session_state.page == "register":
        login()