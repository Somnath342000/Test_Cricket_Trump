import streamlit as st
from sheet import (
    get_sheet,
    get_player_groups
)

BAT_GROUPS = ["A", "B", "C", "D", "E", "F"]
BOWL_GROUPS = ["K", "L", "M", "N", "O", "P"]


# ==========================
# All Used Groups
# ==========================
def used_groups(match_id):
    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    used_bat = []
    used_bowl = []

    for r in rows:
        if str(r.get("MatchID", "")) != str(match_id):
            continue

        if r.get("Bat1"):
            used_bat.append(r["Bat1"])

        if r.get("Bat2"):
            used_bat.append(r["Bat2"])

        if r.get("Bowl1"):
            used_bowl.append(r["Bowl1"])

        if r.get("Bowl2"):
            used_bowl.append(r["Bowl2"])

    return used_bat, used_bowl


# ==========================
# Available Groups
# ==========================
def available_batting(match_id):
    used_bat, _ = used_groups(match_id)

    return [
        g for g in BAT_GROUPS
        if g not in used_bat
    ]


def available_bowling(match_id):
    _, used_bowl = used_groups(match_id)

    return [
        g for g in BOWL_GROUPS
        if g not in used_bowl
    ]


# ==========================
# Save One Pick
# ==========================
def save_group_pick(
        match_id,
        player,
        field,
        value
):
    # Duplicate protection
    if field.startswith("Bat"):
        if value not in available_batting(match_id):
            st.error(
    f"{value} group already selected."
)
return
    if field.startswith("Bowl"):
        if value not in available_bowling(match_id):
            st.error(
    f"{value} group already selected."
)
return

    ws = get_sheet("Groups")
    rows = ws.get_all_values()

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
                range_name=f"{col}{i}",
                values=[[value]]
            )

            return

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

    row[fields[field]] = value

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
        data.get("Bat1", "") != "" and
        data.get("Bat2", "") != "" and
        data.get("Bowl1", "") != "" and
        data.get("Bowl2", "") != ""
    )


# ==========================
# Draft Screen
# ==========================
def draft_screen(
        match_id,
        player
):
    st.subheader(
        "🏏 Group Selection"
    )

    # Auto refresh every 3 seconds
    st.empty()

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
        groups = available_batting(match_id)

        if groups:
            g = st.selectbox(
                "Batting Group 1",
                groups,
                key="bat1"
            )

            if st.button(
                    "Save Bat1"
            ):
                try:
                    save_group_pick(
                        match_id,
                        player,
                        "Bat1",
                        g
                    )
                    st.rerun()

                except Exception as e:
                    st.error(str(e))
        else:
            st.warning(
                "No batting groups left."
            )
    else:
        st.success(
            f'Bat1 : {data["Bat1"]}'
        )

    # ------------------
    # Bat2
    # ------------------
    if data["Bat2"] == "":
        groups = available_batting(match_id)

        if groups:
            g = st.selectbox(
                "Batting Group 2",
                groups,
                key="bat2"
            )

            if st.button(
                    "Save Bat2"
            ):
                try:
                    save_group_pick(
                        match_id,
                        player,
                        "Bat2",
                        g
                    )
                    st.rerun()

                except Exception as e:
                    st.error(str(e))
    else:
        st.success(
            f'Bat2 : {data["Bat2"]}'
        )

    # ------------------
    # Bowl1
    # ------------------
    if data["Bowl1"] == "":
        groups = available_bowling(match_id)

        if groups:
            g = st.selectbox(
                "Bowling Group 1",
                groups,
                key="bowl1"
            )

            if st.button(
                    "Save Bowl1"
            ):
                try:
                    save_group_pick(
                        match_id,
                        player,
                        "Bowl1",
                        g
                    )
                    st.rerun()

                except Exception as e:
                    st.error(str(e))
        else:
            st.warning(
                "No bowling groups left."
            )
    else:
        st.success(
            f'Bowl1 : {data["Bowl1"]}'
        )

    # ------------------
    # Bowl2
    # ------------------
    if data["Bowl2"] == "":
        groups = available_bowling(match_id)

        if groups:
            g = st.selectbox(
                "Bowling Group 2",
                groups,
                key="bowl2"
            )

            if st.button(
                    "Save Bowl2"
            ):
                try:
                    save_group_pick(
                        match_id,
                        player,
                        "Bowl2",
                        g
                    )
                    st.rerun()

                except Exception as e:
                    st.error(str(e))
        else:
            st.warning(
                "No bowling groups left."
            )
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
