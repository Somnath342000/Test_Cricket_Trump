import streamlit as st
import pandas as pd

df = pd.read_excel("players.xlsx")


def select_player(group, key):

    data = df[df["Group"] == group]

    p = st.selectbox(
        "Select Player",
        data["Player Name"],
        key=key
    )

    row = data[data["Player Name"] == p].iloc[0]

    st.write("ID :", row["ID"])
    st.write("Group :", row["Group"])

    return p
