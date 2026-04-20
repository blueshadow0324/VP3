import streamlit as st
import json
from supabase import create_client
import random

if not "user" in st.session_state:
    st.session_state.user = None

url = "https://obcxepcywkmrcptxpwbq.supabase.co"
key = "sb_publishable__9MoOR67yL294bkkMM--Zg_wc3JK9cf"
db = create_client(url, key)


def gamble(user=None):
    res = db.table("users").select("*").execute()
    userCoins = {row["username"]: row["coins"] for row in res.data}
    coins = userCoins[user]
    st.title("Gamble")
    st.text(f"Coins: {coins}")
    st.button("Gamble 5!", on_click=randomGamble, args=(user, coins))

def randomGamble(user=None, coins=None):
    int = random.randint(1, 5)
    if int == 5:
        coins += 25
        db.table("users") \
            .update({"coins": coins}) \
            .eq("username", user) \
            .execute()
        st.warning("You won 25!")
    else:
        db.table("users") \
           .update({"coins": coins-5}) .eq("username", user) .execute()
        st.warning("You lost 5!")