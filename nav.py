import streamlit as st

def pageUpdate(page):
    st.session_state.page = page
def nav():
    st.sidebar.title("Nav")
    st.sidebar.button("Bank", on_click=pageUpdate, args=("bank",))
    st.sidebar.button( "Home", on_click=pageUpdate, args=("home",))