import streamlit as st
import json

with open("userData.json", "r") as f:
    userData = json.load(f)
with open("userCoins.json", "r") as f:
    userCoins = json.load(f)

def dashboard(user="None"):
    coins = userCoins[user]
    st.title("Dashboard")
    st.text(f"Welcome user, {user}!")
    st.text(f"Coins: {coins}")
