import streamlit as st
from sheet import (
    get_sheet,
    get_player_groups
)

BAT_GROUPS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
]

BOWL_GROUPS = [
    "K",
    "L",
    "M",
    "N",
    "O",
    "P"
]


# ==========================
# All Used Groups
# ==========================
def used_groups(match_id):

    ws = get_sheet("Groups")

    rows = ws.get_all_records()

    used_bat = []
    used_bowl = []

    for r in rows:

        if r["MatchID"] != match_id:
            continue

        if r["Bat1"]:
            used_bat.append(r["Bat1"])

        if r["Bat2"]:
            used_bat.append(r["Bat2"])

        if r["Bowl1"]:
            used_bowl.append(r["Bowl1"])

        if r["Bowl2"]:
            used_bowl.append(r["Bowl2"])

    return used_bat, used_bowl


# ==========================
# Available Batting Groups
# ==========================
def available_batting(match_id):

    used_bat, _ = used_groups(
        match_id
    )

    return [
        g
        for g in BAT_GROUPS
        if g not in used_bat
    ]


# ==========================
# Available Bowling Groups
# ==========================
def available_bowling(match_id):

    _, used_bowl = used_groups(
        match_id
    )

    return [
        g
        for g in BOWL_GROUPS
        if g not in used_bowl
    ]


# ==========================
# Save One Group Pick
# ==========================
def save_group_pick(
        match_id,
        player,
        field,
        value
):

    ws = get_sheet("Groups")

    rows = ws.get_all_values()

    # player row exists?
    for i, r in enumerate(
            rows[1:],
            start=2
    ):

        if (
                len(r) >= 2 and
                r[0] == match_id and
                r[1] == player
        ):

            columns = {
                "Bat1": "C",
                "Bat2": "D",
                "Bowl1": "E",
                "Bowl2": "F"
            }

            col = columns[field]

            ws.update(
                f"{col}{i}",
                [[value]]
            )

            return

    # first insert
    row = [
        match_id,
        player,
        "",
        "",
        "",
        ""
    ]

    fields = {
        "Bat1": 2,
        "Bat2": 3,
        "Bowl1": 4,
        "Bowl2": 5
    }

    row[
        fields[field]
    ] = value

    ws.append_row(row)


# ==========================
# Player Completed?
# ==========================
def group_completed(
        match_id,
        player
):

    data = get_player_groups(
        match_id,
        player
    )

    if data is None:
        return False

    return (
        data["Bat1"] != "" and
        data["Bat2"] != "" and
        data["Bowl1"] != "" and
        data["Bowl2"] != ""
    )


# ==========================
# Draft Screen
# ==========================
def draft_screen(
        match_id,
        player
):

    st.subheader(
        "Group Selection"
    )

    data = get_player_groups(
        match_id,
        player
    )

    if data is None:
        data = {
            "Bat1": "",
            "Bat2": "",
            "Bowl1": "",
            "Bowl2": ""
        }

    # ------------------
    # Bat1
    # ------------------
    if data["Bat1"] == "":

        groups = available_batting(
            match_id
        )

        if groups:

            g = st.selectbox(
                "Batting Group 1",
                groups,
                key="bat1"
            )

            if st.button(
                    "Save Bat1"
            ):

                save_group_pick(
                    match_id,
                    player,
                    "Bat1",
                    g
                )

                st.rerun()

    else:
        st.success(
            f'Bat1 : {data["Bat1"]}'
        )

    # ------------------
    # Bat2
    # ------------------
    if data["Bat2"] == "":

        groups = available_batting(
            match_id
        )

        if groups:

            g = st.selectbox(
                "Batting Group 2",
                groups,
                key="bat2"
            )

            if st.button(
                    "Save Bat2"
            ):

                save_group_pick(
                    match_id,
                    player,
                    "Bat2",
                    g
                )

                st.rerun()

    else:
        st.success(
            f'Bat2 : {data["Bat2"]}'
        )

    # ------------------
    # Bowl1
    # ------------------
    if data["Bowl1"] == "":

        groups = available_bowling(
            match_id
        )

        if groups:

            g = st.selectbox(
                "Bowling Group 1",
                groups,
                key="bowl1"
            )

            if st.button(
                    "Save Bowl1"
            ):

                save_group_pick(
                    match_id,
                    player,
                    "Bowl1",
                    g
                )

                st.rerun()

    else:
        st.success(
            f'Bowl1 : {data["Bowl1"]}'
        )

    # ------------------
    # Bowl2
    # ------------------
    if data["Bowl2"] == "":

        groups = available_bowling(
            match_id
        )

        if groups:

            g = st.selectbox(
                "Bowling Group 2",
                groups,
                key="bowl2"
            )

            if st.button(
                    "Save Bowl2"
            ):

                save_group_pick(
                    match_id,
                    player,
                    "Bowl2",
                    g
                )

                st.rerun()

    else:
        st.success(
            f'Bowl2 : {data["Bowl2"]}'
        )

    if group_completed(
            match_id,
            player
    ):
        st.success(
            "All Groups Locked ✅"
        )
