import streamlit as st
import pandas as pd

from sheet import (
    get_player_groups,
    save_selection,
    get_selection,
    used_cards
)


# =====================================
# Load Excel
# =====================================
@st.cache_data
def load_players():
    return pd.read_excel("Players.xlsx")


# =====================================
# Load Single Group
# =====================================
def load_group(group):

    df = load_players()

    return (
        df[df["Group"] == group]
        .sort_values("Player Name")
        .reset_index(drop=True)
    )


# =====================================
# Load Multiple Groups
# =====================================
def load_groups(groups):

    df = load_players()

    return (
        df[df["Group"].isin(groups)]
        .sort_values("Player Name")
        .reset_index(drop=True)
    )


# =====================================
# Selection Page
# =====================================
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

    # already locked?
    old = get_selection(
        match_id,
        post,
        player
    )

    if old:

        st.success("Cards Locked 🔒")

        st.write(f"Card 1 : {old[0]}")
        st.write(f"Card 2 : {old[1]}")
        st.write(f"Card 3 : {old[2]}")

        return

    # players already used in previous posts
    already_used = used_cards(
        match_id,
        player
    )

    # player's own groups
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

    st.subheader(
        f"Post {post} Card Selection"
    )

    # =====================================
    # Card 1 (Batting)
    # =====================================
    bat_df = load_groups(
        bat_groups
    )

    bat_df = bat_df[
        ~bat_df["Player Name"].isin(
            already_used
        )
    ]

    if bat_df.empty:
        st.error(
            "No batting players left."
        )
        return

    card1 = st.selectbox(
        "Card 1 (Batsman)",
        bat_df["Player Name"].tolist(),
        key=f"{player}_card1"
    )

    # =====================================
    # Card 2 (Bowling)
    # =====================================
    bowl_df = load_groups(
        bowl_groups
    )

    bowl_df = bowl_df[
        ~bowl_df["Player Name"].isin(
            already_used
        )
    ]

    bowl_df = bowl_df[
        ~bowl_df["Player Name"].isin(
            [card1]
        )
    ]

    if bowl_df.empty:
        st.error(
            "No bowling players left."
        )
        return

    card2 = st.selectbox(
        "Card 2 (Bowler)",
        bowl_df["Player Name"].tolist(),
        key=f"{player}_card2"
    )

    # =====================================
    # Card 3 (Wild Card)
    # =====================================
    all_df = load_groups(
        all_groups
    )

    all_df = all_df[
        ~all_df["Player Name"].isin(
            already_used
        )
    ]

    all_df = all_df[
        ~all_df["Player Name"].isin(
            [card1, card2]
        )
    ]

    if all_df.empty:
        st.error(
            "No players left."
        )
        return

    card3 = st.selectbox(
        "Card 3 (Wild Card)",
        all_df["Player Name"].tolist(),
        key=f"{player}_card3"
    )

    st.divider()

    # final safety check
    if len({
        card1,
        card2,
        card3
    }) != 3:

        st.error(
            "Same player cannot be selected twice."
        )
        return

    # =====================================
    # Save
    # =====================================
    if st.button(
            "🔒 Lock Cards",
            key=f"lock_{player}_{post}"
    ):

        save_selection(
            match_id,
            post,
            player,
            card1,
            card2,
            card3
        )

        st.success(
            "Cards Locked Successfully ✅"
        )

        st.rerun()
