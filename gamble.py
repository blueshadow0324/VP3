import streamlit as st
import json
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
    coins = userCoins[user]
    st.title("Custom gambling")
    st.text(f"Coins: {coins}")
    amount2 = st.number_input("Enter amount to gamble:", min_value=1, step=1)
    odds = st.number_input(
        "Enter odds:",
        min_value=1,
        step=1
    )
    st.button("Custom gamble!", on_click=customGamble, args=(user, coins, amount2, odds))

def customGamble(user, coins, amount, odds):
    if coins > amount:
        if odds != 1:
            if amount <= 10000:
                integ = random.randint(1, odds)
                if integ == 1:
                    coins += amount * odds
                    st.warning(f"You won {amount * odds}!")  # fixed message

                else:
                    coins -= amount
                    st.warning(f"You lost {amount}")

                db.table("users") \
                    .update({"coins": coins}) \
                    .eq("username", user) \
                    .execute()
            else:
                st.warning(f"You can't gamble more than {10000}")
        else:
            st.warning("You can't have 1 in odds!")
    else:
        st.warning("You don't have enough coins!")

def jackpotGUI(user, coins):
    st.title("Jackpot")
    st.text(f"Welcome {user}")
    st.button("Bet", on_click=jackpot)
def jackpot(user, coins):
    pot = st.session_state.pot
    randomINT = random.randint(1, 200)
    if randomINT == 200:
        st.warning(f"YOU WON THE JACPOT! {pot}")
    else:
        st.warning(f"You was {200-randomINT} from wining")
        pot += 1000
        coins -= 1000