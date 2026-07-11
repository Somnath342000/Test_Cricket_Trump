import streamlit as st
import gspread
import time
import random
from functools import wraps
from google.oauth2.service_account import Credentials

# ======================================================
# SETTINGS
# ======================================================

SPREADSHEET_ID = "1xFyZezkjGk665bGw5VnX3OwaWT2_gj_fglYg1MUrJ8U"

MAX_RETRY = 5

RETRY_DELAY = 1.5

PLAYERS = [
    "Som",
    "Joy",
    "Krish"
]

# ======================================================
# RETRY DECORATOR
# ======================================================

def retry(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        last_error = None

        for attempt in range(MAX_RETRY):

            try:

                return func(*args, **kwargs)

            except Exception as e:

                last_error = e

                wait = RETRY_DELAY * (attempt + 1)

                time.sleep(wait)

        raise last_error

    return wrapper


# ======================================================
# GOOGLE CONNECTION
# ======================================================

@st.cache_resource(show_spinner=False)
@retry
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
        SPREADSHEET_ID
    )


# ======================================================
# SHEET GETTER
# ======================================================

@retry
def get_sheet(name):

    return connect_sheet().worksheet(name)


# ======================================================
# SAFE READ
# ======================================================

@retry
def read_records(sheet_name):

    ws = get_sheet(sheet_name)

    return ws.get_all_records()


@retry
def read_values(sheet_name):

    ws = get_sheet(sheet_name)

    return ws.get_all_values()


# ======================================================
# SAFE UPDATE
# ======================================================

@retry
def update_cell(
    sheet_name,
    cell,
    value
):

    ws = get_sheet(sheet_name)

    ws.update(
        cell,
        [[value]]
    )


@retry
def update_range(
    sheet_name,
    cell_range,
    values
):

    ws = get_sheet(sheet_name)

    ws.update(
        cell_range,
        values
    )


@retry
def append_row(
    sheet_name,
    row
):

    ws = get_sheet(sheet_name)

    ws.append_row(
        row,
        value_input_option="USER_ENTERED"
    )


# ======================================================
# FIND ROW
# ======================================================

def find_match_row(
    sheet_name,
    match_id
):

    rows = read_values(sheet_name)

    for i, r in enumerate(
        rows[1:],
        start=2
    ):

        if len(r) == 0:
            continue

        if str(r[0]) == str(match_id):

            return i

    return None


def find_player_row(
    sheet_name,
    match_id,
    player
):

    rows = read_values(sheet_name)

    for i, r in enumerate(
        rows[1:],
        start=2
    ):

        if len(r) < 2:
            continue

        if (
            str(r[0]) == str(match_id)
            and
            str(r[1]) == str(player)
        ):

            return i

    return None


# ======================================================
# RANDOM MATCH ID
# ======================================================

def generate_match_id():

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ123456789"

    while True:

        code = "".join(
            random.choice(chars)
            for _ in range(6)
        )

        if not match_exists(code):

            return code


# ======================================================
# BASIC MATCH CHECK
# ======================================================

def match_exists(match_id):

    rows = read_records("Match")

    for r in rows:

        if str(r["MatchID"]) == str(match_id):

            return True

    return False


def get_match(match_id):

    rows = read_records("Match")

    for r in rows:

        if str(r["MatchID"]) == str(match_id):

            return r

    return None
#-------------Part2--------#
# ======================================================
# CREATE MATCH
# ======================================================

def create_match(
    match_id,
    creator
):

    if match_exists(match_id):
        return False

    append_row(
        "Match",
        [
            match_id,
            "Waiting",
            1,
            1,
            "",
            "",
            creator
        ]
    )

    return True


# ======================================================
# GET CREATOR
# ======================================================

def get_creator(match_id):

    match = get_match(match_id)

    if match is None:
        return None

    return match.get("Creator", "")


# ======================================================
# IS CREATOR
# ======================================================

def is_creator(
    match_id,
    player
):

    creator = get_creator(match_id)

    return creator == player


# ======================================================
# PLAYER LIST
# ======================================================

def joined_players(match_id):

    rows = read_records("Groups")

    players = []

    for r in rows:

        if str(r["MatchID"]) == str(match_id):

            if r["Player"] not in players:

                players.append(
                    r["Player"]
                )

    return players


# ======================================================
# AVAILABLE PLAYER NAMES
# ======================================================

def available_names(match_id):

    names = PLAYERS.copy()

    used = joined_players(match_id)

    return [
        p for p in names
        if p not in used
    ]


# ======================================================
# PLAYER ALREADY JOINED?
# ======================================================

def player_joined(
    match_id,
    player
):

    return (
        player
        in
        joined_players(match_id)
    )


# ======================================================
# JOIN MATCH
# ======================================================

def join_match(
    match_id,
    player
):

    if not match_exists(match_id):
        return False, "Match not found."

    if player_joined(
            match_id,
            player
    ):
        return False, "Player name already taken."

    append_row(
        "Groups",
        [
            match_id,
            player,
            "",
            "",
            "",
            ""
        ]
    )

    players = joined_players(
        match_id
    )

    if len(players) == 3:

        update_match_status(
            match_id,
            "Ready"
        )

    return True, "Joined Successfully."


# ======================================================
# UPDATE MATCH STATUS
# ======================================================

def update_match_status(
        match_id,
        status
):

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return

    update_cell(
        "Match",
        f"B{row}",
        status
    )


# ======================================================
# UPDATE POST
# ======================================================

def update_post(
        match_id,
        post
):

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return

    update_cell(
        "Match",
        f"C{row}",
        post
    )


# ======================================================
# UPDATE CALL
# ======================================================

def update_call(
        match_id,
        call
):

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return

    update_cell(
        "Match",
        f"D{row}",
        call
    )


# ======================================================
# LIVE MATCH READY?
# ======================================================

def match_ready(match_id):

    players = joined_players(
        match_id
    )

    return len(players) == 3


# ======================================================
# MATCH STATUS
# ======================================================

def match_status(match_id):

    match = get_match(match_id)

    if match is None:
        return "Unknown"

    return match.get(
        "Status",
        "Waiting"
    )


# ======================================================
# LIVE PLAYER PANEL
# ======================================================

def live_players(match_id):

    data = []

    for p in PLAYERS:

        if player_joined(
                match_id,
                p
        ):
            data.append(
                {
                    "Player": p,
                    "Status": "🟢 Joined"
                }
            )

        else:

            data.append(
                {
                    "Player": p,
                    "Status": "🔴 Waiting"
                }
            )

    return data
#-----------Part3----------#
# ======================================================
# TOSS ENGINE
# ======================================================

def save_toss(
    match_id,
    bat_order=None,
    bowl_order=None
):
    """
    Save batting / bowling toss order.
    Existing value will not be overwritten.
    """

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return False

    match = get_match(match_id)

    if match is None:
        return False

    ws = get_sheet("Match")

    # -----------------------------
    # Save Batting Toss
    # -----------------------------
    if bat_order is not None:

        old = str(
            match.get(
                "BatDraft",
                ""
            )
        ).strip()

        if old == "":

            ws.update(
                f"F{row}",
                [[",".join(bat_order)]]
            )

            ws.update(
                f"H{row}",
                [[1]]
            )

    # -----------------------------
    # Save Bowling Toss
    # -----------------------------
    if bowl_order is not None:

        old = str(
            match.get(
                "BowlDraft",
                ""
            )
        ).strip()

        if old == "":

            ws.update(
                f"G{row}",
                [[",".join(bowl_order)]]
            )

            ws.update(
                f"I{row}",
                [[1]]
            )

    return True


# ======================================================
# GET TOSS
# ======================================================

def get_toss(match_id):

    match = get_match(match_id)

    if match is None:
        return None

    bat = []
    bowl = []

    if match.get("BatDraft"):

        bat = [
            x.strip()
            for x in
            match["BatDraft"].split(",")
        ]

    if match.get("BowlDraft"):

        bowl = [
            x.strip()
            for x in
            match["BowlDraft"].split(",")
        ]

    return {
        "BatDraft": bat,
        "BowlDraft": bowl
    }


# ======================================================
# BATTING TOSS DONE?
# ======================================================

def batting_toss_done(
    match_id
):

    toss = get_toss(match_id)

    if toss is None:
        return False

    return len(
        toss["BatDraft"]
    ) == 3


# ======================================================
# BOWLING TOSS DONE?
# ======================================================

def bowling_toss_done(
    match_id
):

    toss = get_toss(match_id)

    if toss is None:
        return False

    return len(
        toss["BowlDraft"]
    ) == 3


# ======================================================
# BOTH TOSS COMPLETE?
# ======================================================

def toss_completed(
    match_id
):

    return (
        batting_toss_done(
            match_id
        )
        and
        bowling_toss_done(
            match_id
        )
    )


# ======================================================
# BAT PICK
# ======================================================

def get_bat_pick(
    match_id
):

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(
            match.get(
                "BatPick",
                1
            )
        )
    except:
        return 1


def next_bat_pick(
    match_id
):

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return

    pick = get_bat_pick(
        match_id
    )

    if pick < 6:

        update_cell(
            "Match",
            f"H{row}",
            pick + 1
        )


# ======================================================
# BOWL PICK
# ======================================================

def get_bowl_pick(
    match_id
):

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(
            match.get(
                "BowlPick",
                1
            )
        )
    except:
        return 1


def next_bowl_pick(
    match_id
):

    row = find_match_row(
        "Match",
        match_id
    )

    if row is None:
        return

    pick = get_bowl_pick(
        match_id
    )

    if pick < 6:

        update_cell(
            "Match",
            f"I{row}",
            pick + 1
        )


# ======================================================
# CURRENT DRAFT PLAYER
# ======================================================

def current_draft_player(
    order,
    pick
):

    snake = [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]

    if pick < 1:
        return None

    if pick > 6:
        return None

    return snake[pick - 1]


# ======================================================
# CAN PICK ?
# ======================================================

def can_pick_group(
    match_id,
    player,
    draft_type="bat"
):

    toss = get_toss(
        match_id
    )

    if toss is None:
        return False

    if draft_type == "bat":

        order = toss["BatDraft"]

        pick = get_bat_pick(
            match_id
        )

    else:

        order = toss["BowlDraft"]

        pick = get_bowl_pick(
            match_id
        )

    if len(order) != 3:
        return False

    turn = current_draft_player(
        order,
        pick
    )

    return turn == player
#----------- part 4 -------#
