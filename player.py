import streamlit as st
import pandas as pd
from sheet import connect_sheet

# Players.xlsx GitHub root folder-এ থাকবে
df = pd.read_excel("Players.xlsx")


def load_group(group):

    data = df[df["Group"] == group]

    return data


def select_player(match_id, player, group, ptype):

    ws = connect_sheet().worksheet("Selection")

    rows = ws.get_all_values()

    # Player already submitted?
    for r in rows[1:]:
        if (
            r[0] == match_id and
            r[1] == player and
            r[2] == ptype
        ):
            st.success(f"{ptype} already selected : {r[3]}")
            return

    data = load_group(group)

    name = st.selectbox(
        f"Select {ptype}",
        data["Player Name"],
        key=f"{player}_{ptype}_{group}"
    )

    link = data.loc[
        data["Player Name"] == name,
        "Hyperlink"
    ].values[0]

    st.caption(link)

    if st.button(
        f"Confirm {ptype}",
        key=f"btn_{player}_{ptype}"
    ):

        ws.append_row([
            match_id,
            player,
            ptype,
            name,
            group,
            link
        ])

        st.success(f"{name} Selected")
