import streamlit as st

BAT_GROUP = ["A","B","C","D","E","F"]
BOWL_GROUP = ["K","L","M","N","O","P"]


def batting_group(player):

    st.subheader("Batting Group")

    g = st.selectbox(
        f"{player} Select Group",
        BAT_GROUP,
        key=f"bat_{player}"
    )

    if st.button("Confirm Batting",key=f"cb{player}"):

        st.success(f"{player} selected Group {g}")

        return g


def bowling_group(player):

    st.subheader("Bowling Group")

    g = st.selectbox(
        f"{player} Select Group",
        BOWL_GROUP,
        key=f"bowl_{player}"
    )

    if st.button("Confirm Bowling",key=f"cw{player}"):

        st.success(f"{player} selected Group {g}")

        return g
