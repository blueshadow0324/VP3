import streamlit as st
import json

from streamlit.runtime.state import session_state
from supabase import create_client
import random

if not "user" in st.session_state:
    st.session_state.user = None

url = "https://obcxepcywkmrcptxpwbq.supabase.co"
key = "sb_publishable__9MoOR67yL294bkkMM--Zg_wc3JK9cf"
db = create_client(url, key)

res = db.table("users").select("*").execute()
userCoins = {row["username"]: row["coins"] for row in res.data}
rest = db.table("Casino").select("*").execute()
pot = {row["pot"] for row in rest.data}

def pageUpdater(page):
    st.session_state.page = page

def gamble(user=None):
    res = db.table("users").select("*").execute()
    userCoins = {row["username"]: row["coins"] for row in res.data}
    coins = userCoins[user]
    st.title("Gamble")
    st.text(f"Coins: {coins}")
    st.button("Gamble 5!", on_click=randomGamble, args=(user, coins))
    st.divider()
    st.button("Custom gambling!", on_click=pageUpdater, args=("custom",))
    st.button("Jackpot!", on_click=pageUpdater, args=("jackpot", ))

def randomGamble(user=None, coins=None):
    if coins > 5:
        inte = random.randint(1, 5)
        if inte == 5:
            coins += 25
            db.table("users") \
                .update({"coins": coins}) \
                .eq("username", user) \
                .execute()
            st.warning("You won 25!")
        else:
            db.table("users") \
                .update({"coins": coins - 5}).eq("username", user).execute()
            st.warning("You lost 5!")
    else:
        st.warning("You dont have enough coins!")


def custom(user=None, coins=None):
    res = db.table("users").select("*").execute()
    userCoins = {row["username"]: row["coins"] for row in res.data}
    levelShare = {row["username"]: row["xpShare"] for row in res.data}
    share = levelShare[user]
    coins = userCoins[user]
    st.title("Custom gambling")
    st.text(f"Coins: {coins}")
    amount2 = st.number_input("Enter amount to gamble:", min_value=1, step=1)
    odds = st.number_input(
        "Enter odds:",
        min_value=1,
        step=1
    )
    st.button("Custom gamble!", on_click=customGamble, args=(user, coins, amount2, odds, share))

def customGamble(user, coins, amount, odds, share):
    if coins > amount:
        if odds != 1:
            if amount <= 10000:
                integ = random.randint(1, odds)
                if integ == 1:
                    coins += amount * odds
                    share += amount*(odds*odds)/10000
                    st.warning(f"You won {amount * odds} and {amount*(odds*odds)/10000} XP!")  # fixed message

                else:
                    coins -= amount
                    st.warning(f"You lost {amount}")

                db.table("users") \
                    .update({"coins": coins, "xpShare": share}) \
                    .eq("username", user) \
                    .execute()
            else:
                st.warning(f"You can't gamble more than {10000}")
        else:
            st.warning("You can't have 1 in odds!")
    else:
        st.warning("You don't have enough coins!")

def jackpotGUI(user, coins):
    reste = db.table("Casino").select("*").execute()
    print(reste.data)
    pot = reste.data[0]["pot"]
    st.title("Jackpot")
    st.text(f"Welcome {user}")
    st.text(f"Coins: {coins}")
    st.text(f"Pot: {pot}")
    st.text(f"Odds: 1/1000, Bet: 50KVP")
    st.button("Bet", on_click=jackpot, args=(user, coins, pot, ))
def jackpot(user, coins, pot):
    levelShare = {row["username"]: row["xpShare"] for row in res.data}
    share = levelShare[user]
    if coins >= 50000:
        randomINT = random.randint(1, 1000)
        if randomINT == 1000:
            st.warning(f"YOU WON THE JACPOT! {pot}")
            coins += pot
            share += 1000
            pot = 0
            db.table("users") \
                .update({"coins": coins, "xpShare": share}).eq("username", user).execute()
            db.table("Casino") \
                .update({"pot": pot}).eq("id", 1).execute()
        else:
            st.warning(f"You was {1000 - randomINT} from the jackpot!")
            pot = 50000 + pot
            coins -= 50000
            print(pot)
            db.table("Casino") \
                .update({"pot": pot}).eq("id", 1).execute()
            db.table("users") \
                .update({"coins": coins}).eq("username", user).execute()
    else:
        st.warning("You dont have enough for a ticket!")