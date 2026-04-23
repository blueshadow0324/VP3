import streamlit as st
from supabase import create_client

url = "https://obcxepcywkmrcptxpwbq.supabase.co"
key = "sb_publishable__9MoOR67yL294bkkMM--Zg_wc3JK9cf"
db = create_client(url, key)

def job(user):
    st.title("Job")
    st.text(f"Welcome user {user}")
    st.button("Click", on_click=gain, args=(user,))

def gain(user):
    res = db.table("users").select("*").execute()
    userCoins = {row["username"]: row["coins"] for row in res.data}
    coins = userCoins[user]
    coins += 100
    db.table("users") \
        .update({"coins": coins}) \
        .eq("username", user) \
        .execute()