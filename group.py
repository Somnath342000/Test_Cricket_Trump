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
        #---------
import streamlit as st
from sheet import connect_sheet

BAT = ["A","B","C","D","E","F"]
BOWL = ["K","L","M","N","O","P"]


def available_groups(match_id, typ):

    ws = connect_sheet().worksheet("Draft")

    rows = ws.get_all_values()

    used = []

    for r in rows[1:]:
        if r[0] == match_id and r[3] == typ:
            used.append(r[4])

    return [g for g in (BAT if typ=="BAT" else BOWL) if g not in used]


def pick_group(match_id, player, typ, pick):

    groups = available_groups(match_id, typ)

    if len(groups)==0:
        st.success("All Groups Selected")
        return

    g = st.selectbox(
        f"{typ} Group",
        groups,
        key=f"{typ}{pick}"
    )

    if st.button(f"Confirm {typ} {pick}"):

        ws = connect_sheet().worksheet("Draft")

        ws.append_row([
            match_id,
            pick,
            player,
            typ,
            g
        ])

        st.success(f"{player} selected {g}")
