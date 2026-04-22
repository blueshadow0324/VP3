import streamlit as st
import random
import time

items = ["Apple","Banana","Orange","Win","Lose"]

if st.button("Spin"):
    placeholder = st.empty()

    for i in range(30):
        pick = random.choice(items)
        placeholder.write(f"🎡 {pick}")
        time.sleep(0.1)

    st.success(f"Result: {pick}")