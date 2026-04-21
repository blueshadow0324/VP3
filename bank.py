import streamlit as st
import json
from supabase import create_client

if not "user" in st.session_state:
    st.session_state.user = None

with open("userCoins.json", "r") as f:
    userCoins = json.load(f)

user = st.session_state.user
url = "https://obcxepcywkmrcptxpwbq.supabase.co"
key = "sb_publishable__9MoOR67yL294bkkMM--Zg_wc3JK9cf"
db = create_client(url, key)

def bank(user="None"):
    res = db.table("users").select("*").execute()
    userCoins = {row["username"]: row["coins"] for row in res.data}
    userData = {row["username"]: row["password"] for row in res.data}
    userBank = {row["username"]: row["bank"] for row in res.data}
    # Full row data for internal use if needed
    fullUserData = {row["username"]: row for row in res.data}

    coins = userCoins[user]

    st.title("Bank")
    st.text(f"Hello, {user}!")
    st.text(f"Coins: {coins}")
    with st.form("BANK"):
        reciver = st.text_input("Reciver:")
        amount = st.number_input("Amount:")
        submit = st.form_submit_button("Send!")
        if submit:
            if amount > 0:
                if userCoins[user] > amount:
                    userCoins[user] -= amount
                    userCoins[reciver] += amount
                    db.table("users") \
                        .update({"coins": userCoins[user]}) \
                        .eq("username", user) \
                        .execute()
                    db.table("users") \
                        .update({"coins": userCoins[reciver]}) .eq("username", reciver) .execute()
            else:
                st.warning("You dont have enough coins!")
    st.divider()
    bank = userBank[user]
    st.text(f"Bank: {bank} coins")

    with st.form("ACC"):
        coinsAmount = st.number_input("Coins:")
        deposit = st.form_submit_button("Deposit")
        withdraw = st.form_submit_button("Withdraw")
        if deposit:
            if coins > coinsAmount:
                coins -= coinsAmount
                bank += coinsAmount
                st.warning(f"You have deposited: {coinsAmount}")
        if withdraw:
            if bank > coinsAmount:
                coins += coinsAmount
                bank -= coinsAmount
                st.warning(f"You have withdrew: {coinsAmount}")
