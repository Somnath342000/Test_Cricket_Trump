import streamlit as st
from sheet import connect_sheet

BAT = ["A","B","C","D","E","F"]
BOWL = ["K","L","M","N","O","P"]


def available_groups(match_id, typ):

    ws = connect_sheet().worksheet("Groups")

    rows = ws.get_all_values()

    used = []

    for r in rows[1:]:
        if r[0] == match_id and r[3] == typ:
            used.append(r[4])

    return [g for g in (BAT if typ=="BAT" else BOWL) if g not in used]


def pick_group(match_id, player, typ, pick):

    ws = connect_sheet().worksheet("Groups")

    rows = ws.get_all_values()

    # একই Player আগে Pick করেছে কিনা
    for r in rows[1:]:
        if (
            r[0] == match_id and
            r[1] == str(pick) and
            r[2] == player and
            r[3] == typ
        ):
            st.success(f"{player} already selected {r[4]}")
            return

    groups = available_groups(match_id, typ)

    if not groups:
        st.warning("No Group Available")
        return

    g = st.selectbox(
        f"{typ} Group",
        groups,
        key=f"{player}_{typ}_{pick}"
    )

    if st.button(f"Confirm {typ} {pick}", key=f"btn_{player}_{typ}_{pick}"):

        ws.append_row([
            match_id,
            pick,
            player,
            typ,
            g
        ])

        st.success(f"{player} selected Group {g}")
