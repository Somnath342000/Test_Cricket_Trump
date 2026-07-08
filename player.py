import streamlit as st
import pandas as pd
from sheet import (
    get_player_groups,
    save_selection,
    get_selection
)


@st.cache_data
def load_players():
    return pd.read_excel("Players.xlsx")


def load_group(group):
    df = load_players()
    return (
        df[df["Group"] == group]
        .sort_values("Player Name")
        .reset_index(drop=True)
    )


def load_groups(groups):

    df = load_players()

    return (
        df[df["Group"].isin(groups)]
        .sort_values("Player Name")
        .reset_index(drop=True)
    )


def selection_page(
        match_id,
        post,
        player
):

    groups = get_player_groups(
        match_id,
        player
    )

    if groups is None:
        st.warning(
            "Please complete Group Draft first."
        )
        return

    old = get_selection(
        match_id,
        post,
        player
    )

    if old:

        st.success("Cards Locked")

        st.write(f"Card 1 : {old[0]}")
        st.write(f"Card 2 : {old[1]}")
        st.write(f"Card 3 : {old[2]}")

        return

    bat_groups = [
        groups["Bat1"],
        groups["Bat2"]
    ]

    bowl_groups = [
        groups["Bowl1"],
        groups["Bowl2"]
    ]

    all_groups = (
        bat_groups +
        bowl_groups
    )

    # ------------------
    # Card 1
    # Batting only
    # ------------------
    bat_df = load_groups(
        bat_groups
    )

    card1 = st.selectbox(
        "Card 1 (Batsman)",
        bat_df["Player Name"],
        key=f"{player}_card1"
    )

    # ------------------
    # Card 2
    # Bowling only
    # ------------------
    bowl_df = load_groups(
        bowl_groups
    )

    card2 = st.selectbox(
        "Card 2 (Bowler)",
        bowl_df["Player Name"],
        key=f"{player}_card2"
    )

    # ------------------
    # Card 3
    # Wild Card
    # ------------------
    all_df = load_groups(
        all_groups
    )

    card3 = st.selectbox(
        "Card 3 (Wild Card)",
        all_df["Player Name"],
        key=f"{player}_card3"
    )

    st.divider()
if len({
        card1,
        card2,
        card3
}) != 3:

    st.error(
        "Same player cannot be selected twice."
    )
    return


    if st.button("🔒 Lock Cards"):

        save_selection(
            match_id,
            post,
            player,
            card1,
            card2,
            card3
        )

        st.success(
            "Cards Locked Successfully"
        )

        st.rerun()
