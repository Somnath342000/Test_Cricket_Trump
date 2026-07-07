import random
import streamlit as st

players = ["Joy", "Krish", "Som"]


def snake(order):
    return [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]


def batting_toss():

    if "bat_order" not in st.session_state:
        st.session_state.bat_order = random.sample(players, 3)

    order = st.session_state.bat_order
    draft = snake(order)

    st.subheader("🏏 Batting Toss")

    st.write(f"🥇 1st : {order[0]}")
    st.write(f"🥈 2nd : {order[1]}")
    st.write(f"🥉 3rd : {order[2]}")

    st.write("### Batting Group Selection")

    for i, p in enumerate(draft):
        st.write(f"Pick {i+1} : {p}")

    return order, draft


def bowling_toss():

    if "bowl_order" not in st.session_state:
        st.session_state.bowl_order = random.sample(players, 3)

    order = st.session_state.bowl_order
    draft = snake(order)

    st.subheader("🎯 Bowling Toss")

    st.write(f"🥇 1st : {order[0]}")
    st.write(f"🥈 2nd : {order[1]}")
    st.write(f"🥉 3rd : {order[2]}")

    st.write("### Bowling Group Selection")

    for i, p in enumerate(draft):
        st.write(f"Pick {i+1} : {p}")

    return order, draft
