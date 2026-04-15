import streamlit as st
import json

if not "user" in st.session_state:
    st.session_state.user = None

with open("userCoins.json", "r") as f:
    userCoins = json.load(f)

user = st.session_state.user

def bank():
    with st.form("BANK"):
        reciver = st.text_input("Reciver:")
        amount = st.number_input("Amount:")
        submit = st.form_submit_button("Send!")
        if submit:
         userCoins[user] -= amount
         userCoins[reciver] += amount

         with open("userCoins.json", "w") as f:
            json.dump(userCoins, f, indent=4)