import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ==========================
# Connection
# ==========================
@st.cache_resource
def connect_sheet():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    return client.open_by_key(
        "1cmH0UZbWBvkmjbPq2dP5HCKsKEY2FFaB"
    )


def get_sheet(name):
    return connect_sheet().worksheet(name)


# ==========================
# Match Sheet
# ==========================
def create_match(match_id):

    ws = get_sheet("Match")

    ws.append_row([
        match_id,
        "Waiting",
        1,
        1
    ])


def match_exists(match_id):

    ws = get_sheet("Match")

    rows = ws.get_all_values()

    for r in rows[1:]:
        if r[0] == match_id:
            return True

    return False


def get_match(match_id):

    ws = get_sheet("Match")

    rows = ws.get_all_records()

    for r in rows:
        if r["MatchID"] == match_id:
            return r

    return None


def update_match_status(match_id, status):

    ws = get_sheet("Match")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0] == match_id:
            ws.update(f"B{i}", [[status]])
            return


def update_post(match_id, post):

    ws = get_sheet("Match")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0] == match_id:
            ws.update(f"C{i}", [[post]])
            return


def update_call(match_id, call):

    ws = get_sheet("Match")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0] == match_id:
            ws.update(f"D{i}", [[call]])
            return


# ==========================
# Groups Sheet
# ==========================
def save_groups(
        match_id,
        player,
        bat1,
        bat2,
        bowl1,
        bowl2
):

    ws = get_sheet("Groups")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
                r[0] == match_id and
                r[1] == player
        ):

            ws.update(
                f"C{i}:F{i}",
                [[bat1, bat2, bowl1, bowl2]]
            )
            return

    ws.append_row([
        match_id,
        player,
        bat1,
        bat2,
        bowl1,
        bowl2
    ])


def get_player_groups(match_id, player):

    ws = get_sheet("Groups")

    rows = ws.get_all_records()

    for r in rows:

        if (
                r["MatchID"] == match_id and
                r["Player"] == player
        ):

            return {
                "Bat1": r["Bat1"],
                "Bat2": r["Bat2"],
                "Bowl1": r["Bowl1"],
                "Bowl2": r["Bowl2"]
            }

    return None


# ==========================
# Selection Sheet
# ==========================
def save_selection(
        match_id,
        post,
        player,
        card1,
        card2,
        card3
):

    ws = get_sheet("Selections")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
                r[0] == match_id and
                str(r[1]) == str(post) and
                r[2] == player
        ):

            ws.update(
                f"D{i}:F{i}",
                [[card1, card2, card3]]
            )
            return

    ws.append_row([
        match_id,
        post,
        player,
        card1,
        card2,
        card3
    ])


def get_selection(
        match_id,
        post,
        player
):

    ws = get_sheet("Selections")

    rows = ws.get_all_records()

    for r in rows:

        if (
                r["MatchID"] == match_id and
                str(r["Post"]) == str(post) and
                r["Player"] == player
        ):

            return [
                r["Card1"],
                r["Card2"],
                r["Card3"]
            ]

    return None


# ==========================
# Scores Sheet
# ==========================
def save_call(
        match_id,
        post,
        call,
        category,
        som,
        joy,
        krish
):

    ws = get_sheet("Scores")

    ws.append_row([
        match_id,
        post,
        call,
        category,
        som,
        joy,
        krish
    ])


def get_scores(match_id, post):

    ws = get_sheet("Scores")

    rows = ws.get_all_records()

    data = []

    for r in rows:

        if (
                r["MatchID"] == match_id and
                str(r["Post"]) == str(post)
        ):
            data.append(r)

    return data
