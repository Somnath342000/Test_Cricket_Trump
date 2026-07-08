import random
import json
import streamlit as st
from sheet import get_sheet

PLAYERS = [
    "Joy",
    "Krish",
    "Som"
]


# ==========================
# Snake Order
# ==========================
def snake(order):

    return [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]


# ==========================
# Save Toss
# ==========================
def save_toss(
        match_id,
        column,
        order
):

    ws = get_sheet("Match")

    rows = ws.get_all_values()

    for i, r in enumerate(
            rows[1:],
            start=2
    ):

        if r[0] == match_id:

            cols = {
                "BatDraft": "E",
                "BowlDraft": "F"
            }

            ws.update(
                f'{cols[column]}{i}',
                [[json.dumps(order)]]
            )

            return


# ==========================
# Read Toss
# ==========================
def get_toss(
        match_id,
        column
):

    ws = get_sheet("Match")

    rows = ws.get_all_records()

    for r in rows:

        if r["MatchID"] == match_id:

            value = r.get(column, "")

            if value:
                return json.loads(value)

    return None


# ==========================
# Generate Batting Toss
# ==========================
def batting_toss(
        match_id
):

    order = get_toss(
        match_id,
        "BatDraft"
    )

    if order is None:

        order = random.sample(
            PLAYERS,
            3
        )

        save_toss(
            match_id,
            "BatDraft",
            order
        )

    return order


# ==========================
# Generate Bowling Toss
# ==========================
def bowling_toss(
        match_id
):

    order = get_toss(
        match_id,
        "BowlDraft"
    )

    if order is None:

        order = random.sample(
            PLAYERS,
            3
        )

        save_toss(
            match_id,
            "BowlDraft",
            order
        )

    return order


# ==========================
# Display Toss
# ==========================
def show_toss(
        title,
        order
):

    st.subheader(title)

    st.write(
        f"🥇 1st : {order[0]}"
    )

    st.write(
        f"🥈 2nd : {order[1]}"
    )

    st.write(
        f"🥉 3rd : {order[2]}"
    )

    st.divider()

    seq = snake(order)

    st.write(
        "Snake Draft Order"
    )

    for i, p in enumerate(
            seq,
            start=1
    ):

        st.write(
            f"Pick {i} : {p}"
        )


# ==========================
# Current Turn
# ==========================
def current_turn(
        order,
        pick_no
):

    seq = snake(order)

    if pick_no < 1:
        return None

    if pick_no > 6:
        return None

    return seq[pick_no - 1]


# ==========================
# Can Pick?
# ==========================
def can_pick(
        player,
        order,
        pick_no
):

    turn = current_turn(
        order,
        pick_no
    )

    return player == turn
