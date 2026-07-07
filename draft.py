import random
import streamlit as st

players = ["Joy", "Krish", "Som"]

def batting_toss():

    order = random.sample(players, 3)

    draft = [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]

    st.success("🏏 Batting Toss")

    st.write("🥇 1st :", order[0])
    st.write("🥈 2nd :", order[1])
    st.write("🥉 3rd :", order[2])

    st.subheader("Batting Group Selection Order")

    for i, p in enumerate(draft):
        st.write(f"Pick {i+1} : {p}")

    return order, draft


def bowling_toss():

    order = random.sample(players, 3)

    draft = [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]

    st.success("🎯 Bowling Toss")

    st.write("🥇 1st :", order[0])
    st.write("🥈 2nd :", order[1])
    st.write("🥉 3rd :", order[2])

    st.subheader("Bowling Group Selection Order")

    for i, p in enumerate(draft):
        st.write(f"Pick {i+1} : {p}")

    return order, draft
