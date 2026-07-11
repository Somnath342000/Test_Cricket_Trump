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
# =====================================
# PLAYER JOIN / LIVE PLAYER
# =====================================

PLAYERS = [
    "Som",
    "Joy",
    "Krish"
]


def get_joined_players(match_id):
    """
    Return joined player names.
    """
    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    players = []

    for r in rows:
        if str(r["MatchID"]) == str(match_id):
            if r["Player"]:
                players.append(r["Player"])

    return list(set(players))


def available_player_names(match_id):
    """
    Return available player names.
    Example:
    Som joined
    -> Joy, Krish
    """
    joined = get_joined_players(match_id)

    return [
        p for p in PLAYERS
        if p not in joined
    ]


def player_exists(match_id, player):
    """
    Check player already joined?
    """
    joined = get_joined_players(match_id)

    return player in joined


def join_player(match_id, player):
    """
    Join player only once.
    """

    if player_exists(match_id, player):
        return False

    ws = get_sheet("Groups")

    ws.append_row([
        match_id,
        player,
        "",
        "",
        "",
        ""
    ])

    return True


def total_joined_players(match_id):
    """
    Number of joined players.
    """
    return len(
        get_joined_players(match_id)
    )


def all_players_joined(match_id):
    """
    Match starts only when
    all 3 players joined.
    """
    return total_joined_players(match_id) == 3


def waiting_players(match_id):
    """
    Remaining player names.
    """
    joined = get_joined_players(match_id)

    return [
        p for p in PLAYERS
        if p not in joined
    ]


def show_live_players(match_id):
    """
    Live player list.
    """
    joined = get_joined_players(match_id)

    return {
        "Joined": joined,
        "Waiting": waiting_players(match_id)
    }


def creator_only(match_id, player):
    """
    Only creator can control toss.
    """
    match = get_match(match_id)

    if match is None:
        return False

    creator = match.get("CreatedBy", "")

    return creator == player


def can_join(match_id, player):
    """
    Validation before join.
    """

    if not match_exists(match_id):
        return False, "Match not found."

    if player_exists(match_id, player):
        return False, "Player already joined."

    if total_joined_players(match_id) >= 3:
        return False, "Match is already full."

    return True, "OK"
#----------part 5----------#
# =====================================
# GROUP DRAFT ENGINE
# =====================================

BAT_GROUPS = ["A", "B", "C", "D", "E", "F"]
BOWL_GROUPS = ["K", "L", "M", "N", "O", "P"]


def get_group_record(match_id, player):
    """
    Get one player's group record.
    """
    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    for r in rows:
        if (
            str(r["MatchID"]) == str(match_id)
            and str(r["Player"]) == str(player)
        ):
            return r

    return None


def used_batting_groups(match_id):
    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    used = []

    for r in rows:

        if str(r["MatchID"]) != str(match_id):
            continue

        if r["Bat1"]:
            used.append(r["Bat1"])

        if r["Bat2"]:
            used.append(r["Bat2"])

    return used


def used_bowling_groups(match_id):
    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    used = []

    for r in rows:

        if str(r["MatchID"]) != str(match_id):
            continue

        if r["Bowl1"]:
            used.append(r["Bowl1"])

        if r["Bowl2"]:
            used.append(r["Bowl2"])

    return used


def available_batting_groups(match_id):
    used = used_batting_groups(match_id)

    return [
        g
        for g in BAT_GROUPS
        if g not in used
    ]


def available_bowling_groups(match_id):
    used = used_bowling_groups(match_id)

    return [
        g
        for g in BOWL_GROUPS
        if g not in used
    ]


def save_group(
        match_id,
        player,
        field,
        value
):
    """
    field =
    Bat1
    Bat2
    Bowl1
    Bowl2
    """

    ws = get_sheet("Groups")
    rows = ws.get_all_values()

    columns = {
        "Bat1": "C",
        "Bat2": "D",
        "Bowl1": "E",
        "Bowl2": "F"
    }

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(match_id)
            and str(r[1]) == str(player)
        ):

            ws.update(
                f"{columns[field]}{i}",
                [[value]]
            )

            return True

    return False


def player_group_locked(
        match_id,
        player
):
    """
    Player finished all groups?
    """

    data = get_group_record(
        match_id,
        player
    )

    if data is None:
        return False

    return (
        data["Bat1"] != ""
        and
        data["Bat2"] != ""
        and
        data["Bowl1"] != ""
        and
        data["Bowl2"] != ""
    )


def all_group_locked(match_id):
    """
    All three players completed?
    """

    joined = get_joined_players(match_id)

    if len(joined) != 3:
        return False

    for p in joined:

        if not player_group_locked(
                match_id,
                p
        ):
            return False

    return True


def player_groups(
        match_id,
        player
):
    """
    Return player's own groups.
    """

    data = get_group_record(
        match_id,
        player
    )

    if data is None:
        return []

    return [
        data["Bat1"],
        data["Bat2"],
        data["Bowl1"],
        data["Bowl2"]
    ]


def batting_group_available(
        match_id,
        group_name
):
    return (
        group_name
        in
        available_batting_groups(match_id)
    )


def bowling_group_available(
        match_id,
        group_name
):
    return (
        group_name
        in
        available_bowling_groups(match_id)
    )
#---------part6--------#
# =====================================
# SNAKE DRAFT TURN ENGINE
# =====================================

def snake_order(order):
    """
    Convert toss order into snake draft.
    Example:
    Joy, Krish, Som

    ->
    Joy
    Krish
    Som
    Som
    Krish
    Joy
    """

    if len(order) != 3:
        return []

    return [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]


def draft_pick_count(match_id, draft_type):
    """
    draft_type :
    BAT
    BOWL
    """

    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    count = 0

    for r in rows:

        if str(r["MatchID"]) != str(match_id):
            continue

        if draft_type == "BAT":

            if r["Bat1"]:
                count += 1

            if r["Bat2"]:
                count += 1

        else:

            if r["Bowl1"]:
                count += 1

            if r["Bowl2"]:
                count += 1

    return count


def current_draft_turn(match_id, draft_type):
    """
    Return current player's turn.
    """

    toss = get_toss(match_id)

    if toss is None:
        return None

    if draft_type == "BAT":
        order = toss["BatDraft"]
    else:
        order = toss["BowlDraft"]

    draft = snake_order(order)

    picked = draft_pick_count(
        match_id,
        draft_type
    )

    if picked >= 6:
        return None

    return draft[picked]


def can_pick_group(
        match_id,
        player,
        draft_type
):
    """
    Check whether player can pick now.
    """

    turn = current_draft_turn(
        match_id,
        draft_type
    )

    return player == turn


def next_group_field(
        match_id,
        player,
        draft_type
):
    """
    Which field should be filled?

    Bat1
    Bat2
    Bowl1
    Bowl2
    """

    data = get_group_record(
        match_id,
        player
    )

    if data is None:
        return None

    if draft_type == "BAT":

        if data["Bat1"] == "":
            return "Bat1"

        if data["Bat2"] == "":
            return "Bat2"

    else:

        if data["Bowl1"] == "":
            return "Bowl1"

        if data["Bowl2"] == "":
            return "Bowl2"

    return None


def draft_completed(match_id, draft_type):
    """
    Check BAT/BOWL draft completed.
    """

    return draft_pick_count(
        match_id,
        draft_type
    ) == 6


def next_turn_player(match_id, draft_type):
    """
    Next player's name.
    """

    return current_draft_turn(
        match_id,
        draft_type
    )
#--------part7----------#
# =====================================
# CARD SELECTION ENGINE
# =====================================

def get_player_selection(match_id, post, player):
    """
    Return player's locked cards.
    """

    ws = get_sheet("Selections")
    rows = ws.get_all_records()

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and str(r["Post"]) == str(post)
            and str(r["Player"]) == str(player)
        ):

            return r

    return None


def cards_locked(match_id, post, player):
    """
    Check player already locked cards.
    """

    return get_player_selection(
        match_id,
        post,
        player
    ) is not None


def save_player_cards(
        match_id,
        post,
        player,
        card1,
        card2,
        card3
):
    """
    Save three locked cards.
    """

    if cards_locked(
            match_id,
            post,
            player
    ):
        return False

    ws = get_sheet("Selections")

    ws.append_row([
        match_id,
        post,
        player,
        card1,
        card2,
        card3
    ])

    return True


def selected_cards(match_id, player):
    """
    All previously used cards.
    """

    ws = get_sheet("Selections")
    rows = ws.get_all_records()

    cards = []

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and str(r["Player"]) == str(player)
        ):

            cards.extend([
                r["Card1"],
                r["Card2"],
                r["Card3"]
            ])

    return cards


def available_cards(
        all_players,
        used_cards
):
    """
    Remove already used cards.
    """

    return [

        p

        for p in all_players

        if p not in used_cards

    ]


def all_players_locked(
        match_id,
        post
):
    """
    Three players locked?
    """

    ws = get_sheet("Selections")
    rows = ws.get_all_records()

    players = []

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and
            str(r["Post"]) == str(post)
        ):

            players.append(
                r["Player"]
            )

    return len(set(players)) == 3


def locked_players(
        match_id,
        post
):
    """
    Live locked player list.
    """

    ws = get_sheet("Selections")
    rows = ws.get_all_records()

    players = []

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and
            str(r["Post"]) == str(post)
        ):

            players.append(
                r["Player"]
            )

    return players


def waiting_card_players(
        match_id,
        post
):
    """
    Players still not locked.
    """

    joined = get_joined_players(
        match_id
    )

    locked = locked_players(
        match_id,
        post
    )

    return [

        p

        for p in joined

        if p not in locked

    ]


def player_cards(
        match_id,
        post,
        player
):
    """
    Return card list.
    """

    data = get_player_selection(
        match_id,
        post,
        player
    )

    if data is None:
        return []

    return [

        data["Card1"],
        data["Card2"],
        data["Card3"]

    ]
#---------part8--------#
# =====================================
# CALL & MATCH PROGRESS ENGINE
# =====================================

TOTAL_POSTS = 12
TOTAL_CALLS = 18


# =====================================
# Current Post
# =====================================
def current_post(match_id):

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(match.get("CurrentPost", 1))
    except:
        return 1


# =====================================
# Current Call
# =====================================
def current_call(match_id):

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(match.get("CurrentCall", 1))
    except:
        return 1


# =====================================
# Update Current Post
# =====================================
def set_current_post(match_id, post):

    ws = get_sheet("Match")
    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0] == match_id:

            ws.update(
                f"C{i}",
                [[post]]
            )

            return True

    return False


# =====================================
# Update Current Call
# =====================================
def set_current_call(match_id, call):

    ws = get_sheet("Match")
    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0] == match_id:

            ws.update(
                f"D{i}",
                [[call]]
            )

            return True

    return False


# =====================================
# Move To Next Call
# =====================================
def next_call(match_id):

    post = current_post(match_id)
    call = current_call(match_id)

    # Normal Call
    if call < TOTAL_CALLS:

        set_current_call(
            match_id,
            call + 1
        )

        return

    # Finished Call 18

    set_current_call(
        match_id,
        1
    )

    if post < TOTAL_POSTS:

        set_current_post(
            match_id,
            post + 1
        )

    else:

        # Match Finished
        set_current_post(
            match_id,
            TOTAL_POSTS + 1
        )


# =====================================
# Match Finished?
# =====================================
def match_finished(match_id):

    return current_post(
        match_id
    ) > TOTAL_POSTS


# =====================================
# Post Finished?
# =====================================
def post_finished(match_id):

    return (
        current_call(match_id) == 1
        and
        current_post(match_id) > 1
    )


# =====================================
# Remaining Calls
# =====================================
def remaining_calls(match_id):

    return max(
        0,
        TOTAL_CALLS -
        current_call(match_id) +
        1
    )


# =====================================
# Remaining Posts
# =====================================
def remaining_posts(match_id):

    return max(
        0,
        TOTAL_POSTS -
        current_post(match_id) +
        1
    )


# =====================================
# Reset Match
# =====================================
def reset_match_progress(match_id):

    set_current_post(
        match_id,
        1
    )

    set_current_call(
        match_id,
        1
    )


# =====================================
# Game Status
# =====================================
def game_status(match_id):

    if match_finished(match_id):

        return "🏆 MATCH FINISHED"

    return (
        f"Post : {current_post(match_id)} | "
        f"Call : {current_call(match_id)}"
    )


# =====================================
# Current Caller
# sequence = 18 Player Order
# =====================================
def current_caller(
        match_id,
        sequence
):

    if len(sequence) != 18:
        return None

    call = current_call(
        match_id
    )

    if call < 1 or call > 18:
        return None

    return sequence[
        call - 1
    ]


# =====================================
# Is Player's Turn?
# =====================================
def is_player_turn(
        match_id,
        player,
        sequence
):

    return (
        current_caller(
            match_id,
            sequence
        )
        == player
    )


# =====================================
# Next Caller
# =====================================
def next_caller(
        match_id,
        sequence
):

    call = current_call(
        match_id
    )

    if call >= TOTAL_CALLS:
        return None

    return sequence[
        call
    ]


# =====================================
# Current Progress %
# =====================================
def match_progress(match_id):

    post = current_post(match_id)
    call = current_call(match_id)

    if match_finished(match_id):
        return 100

    completed = (
        (post - 1) * TOTAL_CALLS
        +
        (call - 1)
    )

    total = (
        TOTAL_POSTS *
        TOTAL_CALLS
    )

    return round(
        completed * 100 / total,
        2
    )
#--------part9A--------#
# =====================================
# PART 9A : SCORE ENGINE
# Save / Read Score
# =====================================

PLAYERS = [
    "Som",
    "Joy",
    "Krish"
]


def save_score(
        match_id,
        post,
        call,
        category,
        som,
        joy,
        krish
):
    """
    Save one call score.
    Duplicate হলে Update করবে।
    """

    ws = get_sheet("Scores")
    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(match_id)
            and
            str(r[1]) == str(post)
            and
            str(r[2]) == str(call)
        ):

            ws.update(
                f"D{i}:G{i}",
                [[
                    category,
                    som,
                    joy,
                    krish
                ]]
            )

            return True

    ws.append_row([
        match_id,
        post,
        call,
        category,
        som,
        joy,
        krish
    ])

    return True


# =====================================
# Get One Call
# =====================================
def get_call_score(
        match_id,
        post,
        call
):

    ws = get_sheet("Scores")
    rows = ws.get_all_records()

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and
            str(r["Post"]) == str(post)
            and
            str(r["Call"]) == str(call)
        ):

            return r

    return None


# =====================================
# Get One Post
# =====================================
def get_post_scores(
        match_id,
        post
):

    ws = get_sheet("Scores")
    rows = ws.get_all_records()

    data = []

    for r in rows:

        if (
            str(r["MatchID"]) == str(match_id)
            and
            str(r["Post"]) == str(post)
        ):

            data.append(r)

    return data


# =====================================
# Has Call Saved?
# =====================================
def call_exists(
        match_id,
        post,
        call
):

    return (
        get_call_score(
            match_id,
            post,
            call
        )
        is not None
    )


# =====================================
# Number Of Calls Saved
# =====================================
def total_saved_calls(
        match_id,
        post
):

    return len(
        get_post_scores(
            match_id,
            post
        )
    )


# =====================================
# Post Completed?
# =====================================
def score_completed(
        match_id,
        post
):

    return (
        total_saved_calls(
            match_id,
            post
        ) == 18
    )


# =====================================
# Last Saved Call
# =====================================
def last_saved_call(
        match_id,
        post
):

    rows = get_post_scores(
        match_id,
        post
    )

    if len(rows) == 0:
        return 0

    return max(
        int(r["Call"])
        for r in rows
    )


# =====================================
# Delete One Call
# Admin Function
# =====================================
def delete_call(
        match_id,
        post,
        call
):

    ws = get_sheet("Scores")
    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if (
            str(r[0]) == str(match_id)
            and
            str(r[1]) == str(post)
            and
            str(r[2]) == str(call)
        ):

            ws.delete_rows(i)

            return True

    return False
#----------part9b--------#

# =====================================
# PART 9B : LIVE SCOREBOARD ENGINE
# =====================================

def total_post_score(match_id, post):
    """
    Total score of one post.
    """

    rows = get_post_scores(
        match_id,
        post
    )

    score = {
        "Som": 0,
        "Joy": 0,
        "Krish": 0
    }

    for r in rows:

        score["Som"] += float(
            r.get("Som", 0) or 0
        )

        score["Joy"] += float(
            r.get("Joy", 0) or 0
        )

        score["Krish"] += float(
            r.get("Krish", 0) or 0
        )

    return score


# =====================================
# One Player Score
# =====================================
def player_post_score(
        match_id,
        post,
        player
):

    score = total_post_score(
        match_id,
        post
    )

    return score.get(
        player,
        0
    )


# =====================================
# Live Scoreboard
# =====================================
def live_scoreboard(
        match_id,
        post
):

    score = total_post_score(
        match_id,
        post
    )

    return [
        {
            "Player": "Som",
            "Score": score["Som"]
        },
        {
            "Player": "Joy",
            "Score": score["Joy"]
        },
        {
            "Player": "Krish",
            "Score": score["Krish"]
        }
    ]


# =====================================
# Current Ranking
# =====================================
def current_ranking(
        match_id,
        post
):

    score = total_post_score(
        match_id,
        post
    )

    return sorted(

        score.items(),

        key=lambda x: x[1],

        reverse=True

    )


# =====================================
# Leading Player
# =====================================
def leading_player(
        match_id,
        post
):

    rank = current_ranking(
        match_id,
        post
    )

    if len(rank) == 0:
        return None

    return rank[0][0]


# =====================================
# Leading Score
# =====================================
def leading_score(
        match_id,
        post
):

    rank = current_ranking(
        match_id,
        post
    )

    if len(rank) == 0:
        return 0

    return rank[0][1]


# =====================================
# Is Post Completed?
# =====================================
def post_score_locked(
        match_id,
        post
):

    return score_completed(
        match_id,
        post
    )


# =====================================
# Remaining Calls
# =====================================
def calls_left(
        match_id,
        post
):

    return max(

        0,

        18 -

        total_saved_calls(
            match_id,
            post
        )

    )


# =====================================
# Score Summary
# =====================================
def score_summary(
        match_id,
        post
):

    score = total_post_score(
        match_id,
        post
    )

    return {

        "Som": score["Som"],

        "Joy": score["Joy"],

        "Krish": score["Krish"],

        "Leader": leading_player(
            match_id,
            post
        ),

        "LeaderScore": leading_score(
            match_id,
            post
        ),

        "CallsCompleted": total_saved_calls(
            match_id,
            post
        ),

        "CallsRemaining": calls_left(
            match_id,
            post
        )

    }
#-------part9c1--------#
# =====================================
# PART 9C-1 : MATCH SCORE ENGINE
# Overall Match Score
# =====================================

def overall_match_score(match_id):
    """
    Total score of all 12 posts.
    """

    score = {
        "Som": 0.0,
        "Joy": 0.0,
        "Krish": 0.0
    }

    for post in range(1, 13):

        post_score = total_post_score(
            match_id,
            post
        )

        score["Som"] += float(
            post_score["Som"]
        )

        score["Joy"] += float(
            post_score["Joy"]
        )

        score["Krish"] += float(
            post_score["Krish"]
        )

    return score


# =====================================
# Overall Player Score
# =====================================

def overall_player_score(
        match_id,
        player
):

    score = overall_match_score(
        match_id
    )

    return float(
        score.get(
            player,
            0
        )
    )


# =====================================
# Final Ranking
# =====================================

def final_ranking(
        match_id
):

    score = overall_match_score(
        match_id
    )

    ranking = sorted(

        score.items(),

        key=lambda x: x[1],

        reverse=True

    )

    return ranking


# =====================================
# Current Position
# =====================================

def player_position(
        match_id,
        player
):

    ranking = final_ranking(
        match_id
    )

    for pos, item in enumerate(
            ranking,
            start=1
    ):

        if item[0] == player:
            return pos

    return None


# =====================================
# Highest Score
# =====================================

def highest_match_score(
        match_id
):

    ranking = final_ranking(
        match_id
    )

    if len(ranking) == 0:
        return 0

    return float(
        ranking[0][1]
    )


# =====================================
# Lowest Score
# =====================================

def lowest_match_score(
        match_id
):

    ranking = final_ranking(
        match_id
    )

    if len(ranking) == 0:
        return 0

    return float(
        ranking[-1][1]
    )


# =====================================
# Score Difference
# =====================================

def score_gap(
        match_id
):

    ranking = final_ranking(
        match_id
    )

    if len(ranking) < 2:
        return 0

    return float(
        ranking[0][1]
    ) - float(
        ranking[1][1]
    )


# =====================================
# Current Leader
# =====================================

def current_match_leader(
        match_id
):

    ranking = final_ranking(
        match_id
    )

    if len(ranking) == 0:
        return None

    return ranking[0][0]


# =====================================
# Score Summary
# =====================================

def match_summary(
        match_id
):

    score = overall_match_score(
        match_id
    )

    return {

        "Som": score["Som"],

        "Joy": score["Joy"],

        "Krish": score["Krish"],

        "Leader": current_match_leader(
            match_id
        ),

        "Highest": highest_match_score(
            match_id
        ),

        "Lowest": lowest_match_score(
            match_id
        ),

        "Gap": score_gap(
            match_id
        )

    }
#-------9c2------#
# =====================================
# PART 9C-2 : WINNER ENGINE
# =====================================

def final_winner(match_id):
    """
    Returns:
    (PlayerName, Score)
    """

    ranking = final_ranking(match_id)

    if not ranking:
        return None

    return ranking[0]


# =====================================
# Runner Up
# =====================================

def runner_up(match_id):

    ranking = final_ranking(match_id)

    if len(ranking) < 2:
        return None

    return ranking[1]


# =====================================
# Third Position
# =====================================

def third_place(match_id):

    ranking = final_ranking(match_id)

    if len(ranking) < 3:
        return None

    return ranking[2]


# =====================================
# Is Draw Match?
# =====================================

def is_draw_match(match_id):

    ranking = final_ranking(match_id)

    if len(ranking) < 2:
        return False

    return ranking[0][1] == ranking[1][1]


# =====================================
# Winner Name
# =====================================

def winner_name(match_id):

    winner = final_winner(match_id)

    if winner is None:
        return ""

    return winner[0]


# =====================================
# Winner Score
# =====================================

def winner_score(match_id):

    winner = final_winner(match_id)

    if winner is None:
        return 0

    return float(winner[1])


# =====================================
# Crown Symbol
# =====================================

def winner_crown(match_id):

    if is_draw_match(match_id):
        return "🤝 DRAW"

    return "👑 " + winner_name(match_id)


# =====================================
# Final Result Dictionary
# =====================================

def final_result(match_id):

    ranking = final_ranking(match_id)

    return {

        "Winner": winner_name(match_id),

        "WinnerScore": winner_score(match_id),

        "RunnerUp": (
            ranking[1][0]
            if len(ranking) >= 2 else ""
        ),

        "Third": (
            ranking[2][0]
            if len(ranking) >= 3 else ""
        ),

        "Ranking": ranking,

        "Draw": is_draw_match(match_id),

        "Crown": winner_crown(match_id)

    }


# =====================================
# Match Finished?
# =====================================

def match_finished(match_id):

    match = get_match(match_id)

    if match is None:
        return False

    try:
        return int(match["CurrentPost"]) > 12
    except:
        return False
#----------part 9c3------#
# =====================================
# PART 9C-3 : MATCH COMPLETE ENGINE
# =====================================

def completed_posts(match_id):
    """
    Number of completed posts.
    """

    count = 0

    for post in range(1, 13):

        if score_completed(
            match_id,
            post
        ):
            count += 1

    return count


# =====================================
# Remaining Posts
# =====================================

def remaining_posts(match_id):

    return max(
        0,
        12 - completed_posts(match_id)
    )


# =====================================
# Is Entire Match Completed?
# =====================================

def is_match_completed(match_id):

    return completed_posts(
        match_id
    ) >= 12


# =====================================
# Champion
# =====================================

def champion(match_id):

    if not is_match_completed(
            match_id
    ):
        return None

    return winner_name(
        match_id
    )


# =====================================
# Champion Crown
# =====================================

def champion_badge(match_id):

    if not is_match_completed(
            match_id
    ):
        return ""

    if is_draw_match(
            match_id
    ):
        return "🤝 DRAW"

    return f"👑 {winner_name(match_id)}"


# =====================================
# Match Status Text
# =====================================

def match_status_text(match_id):

    if is_match_completed(
            match_id
    ):
        return "Completed"

    return "Running"


# =====================================
# Complete Match Summary
# =====================================

def complete_match_summary(match_id):

    return {

        "CompletedPosts":
            completed_posts(
                match_id
            ),

        "RemainingPosts":
            remaining_posts(
                match_id
            ),

        "Status":
            match_status_text(
                match_id
            ),

        "Winner":
            champion(
                match_id
            ),

        "Badge":
            champion_badge(
                match_id
            ),

        "Ranking":
            final_ranking(
                match_id
            ),

        "Scores":
            overall_match_score(
                match_id
            )
    }


# =====================================
# Is Champion?
# =====================================

def is_champion(
        match_id,
        player
):

    c = champion(
        match_id
    )

    if c is None:
        return False

    return c == player


# =====================================
# Winner Emoji
# =====================================

def winner_icon(
        match_id,
        player
):

    if is_champion(
            match_id,
            player
    ):
        return "👑"

    return ""


# =====================================
# Player Display Name
# =====================================

def player_display_name(
        match_id,
        player
):

    return (
        winner_icon(
            match_id,
            player
        )
        + " "
        + player
    )


# =====================================
# Final Leaderboard
# =====================================

def leaderboard(match_id):

    rank = final_ranking(
        match_id
    )

    data = []

    for pos, item in enumerate(
            rank,
            start=1
    ):

        data.append({

            "Rank": pos,

            "Player": player_display_name(
                match_id,
                item[0]
            ),

            "Score": item[1]

        })

    return data


# =====================================
# Update Match Completed
# =====================================

def finish_match(match_id):

    if not is_match_completed(
            match_id
    ):
        return False

    update_match_status(
        match_id,
        "Completed"
    )

    return True
#---------part 9d ---------#
# =====================================
# PART 9D : MATCH PROGRESS ENGINE
# =====================================

def current_post(match_id):
    """
    Returns current post number.
    """

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(match["CurrentPost"])
    except:
        return 1


# =====================================
# Current Call
# =====================================

def current_call(match_id):
    """
    Returns current call number.
    """

    match = get_match(match_id)

    if match is None:
        return 1

    try:
        return int(match["CurrentCall"])
    except:
        return 1


# =====================================
# Next Call
# =====================================

def next_call(match_id):

    call = current_call(match_id)

    if call < 18:

        update_call(
            match_id,
            call + 1
        )

    else:

        update_call(
            match_id,
            1
        )

        update_post(
            match_id,
            current_post(match_id) + 1
        )


# =====================================
# Previous Call
# =====================================

def previous_call(match_id):

    call = current_call(match_id)

    if call > 1:

        update_call(
            match_id,
            call - 1
        )


# =====================================
# Reset Current Post
# =====================================

def reset_post(match_id):

    update_post(
        match_id,
        1
    )

    update_call(
        match_id,
        1
    )


# =====================================
# Last Post?
# =====================================

def last_post(match_id):

    return current_post(match_id) >= 12


# =====================================
# Last Call?
# =====================================

def last_call(match_id):

    return current_call(match_id) >= 18


# =====================================
# Match Progress
# =====================================

def match_progress(match_id):

    post = current_post(match_id)

    call = current_call(match_id)

    percent = (
        ((post - 1) * 18) + call
    ) / 216 * 100

    return round(percent, 2)


# =====================================
# Progress Summary
# =====================================

def progress_summary(match_id):

    return {

        "CurrentPost": current_post(match_id),

        "CurrentCall": current_call(match_id),

        "Progress": match_progress(match_id),

        "LastPost": last_post(match_id),

        "LastCall": last_call(match_id)

    }


# =====================================
# Match Running?
# =====================================

def is_running(match_id):

    match = get_match(match_id)

    if match is None:
        return False

    return str(
        match["Status"]
    ).lower() != "completed"


# =====================================
# Match Finished?
# =====================================

def is_finished(match_id):

    return not is_running(match_id)
#--------part 9e-------#
# =====================================
# PART 9E : PLAYER ENGINE
# =====================================

PLAYERS = [
    "Som",
    "Joy",
    "Krish"
]


# =====================================
# Get Joined Players
# =====================================

def joined_players(match_id):

    ws = get_sheet("Groups")
    rows = ws.get_all_records()

    players = []

    for r in rows:

        if str(r["MatchID"]) == str(match_id):

            if r["Player"] not in players:
                players.append(r["Player"])

    return players


# =====================================
# Available Player Names
# =====================================

def available_players(match_id):

    joined = joined_players(match_id)

    return [

        p

        for p in PLAYERS

        if p not in joined

    ]


# =====================================
# Already Joined?
# =====================================

def player_joined(
        match_id,
        player
):

    return player in joined_players(
        match_id
    )


# =====================================
# Can Join Match?
# =====================================

def can_join_match(
        match_id,
        player
):

    if player not in PLAYERS:
        return False

    if player_joined(
            match_id,
            player
    ):
        return False

    return True


# =====================================
# Total Joined Players
# =====================================

def total_joined(match_id):

    return len(
        joined_players(
            match_id
        )
    )


# =====================================
# All Players Joined?
# =====================================

def all_players_joined(match_id):

    return total_joined(
        match_id
    ) == 3


# =====================================
# Match Creator
# =====================================

def match_creator(match_id):

    match = get_match(match_id)

    if match is None:
        return None

    return match.get(
        "CreatedBy",
        ""
    )


# =====================================
# Is Match Creator?
# =====================================

def is_creator(
        match_id,
        player
):

    creator = match_creator(
        match_id
    )

    return creator == player


# =====================================
# Can Toss?
# Only Creator
# =====================================

def can_do_toss(
        match_id,
        player
):

    return is_creator(
        match_id,
        player
    )


# =====================================
# Live Player Status
# =====================================

def player_status(match_id):

    data = []

    joined = joined_players(
        match_id
    )

    for p in PLAYERS:

        data.append({

            "Player": p,

            "Joined": p in joined,

            "Creator": is_creator(
                match_id,
                p
            )

        })

    return data


# =====================================
# Waiting Players
# =====================================

def waiting_players(match_id):

    joined = joined_players(
        match_id
    )

    return [

        p

        for p in PLAYERS

        if p not in joined

    ]
#---------part 9F-------#
# =====================================
# PART 9F : LIVE DRAFT STATUS ENGINE
# =====================================

# Group Draft Completed?
def player_group_completed(
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

        data["Bat1"] != ""
        and
        data["Bat2"] != ""
        and
        data["Bowl1"] != ""
        and
        data["Bowl2"] != ""

    )


# =====================================
# All Group Draft Finished?
# =====================================

def all_group_completed(match_id):

    for player in PLAYERS:

        if not player_group_completed(
                match_id,
                player
        ):
            return False

    return True


# =====================================
# Selection Locked?
# =====================================

def player_selection_completed(
        match_id,
        post,
        player
):

    cards = get_selection(
        match_id,
        post,
        player
    )

    return cards is not None


# =====================================
# All Players Locked?
# =====================================

def all_selection_completed(
        match_id,
        post
):

    for player in PLAYERS:

        if not player_selection_completed(
                match_id,
                post,
                player
        ):
            return False

    return True


# =====================================
# Match Ready?
# =====================================

def match_ready(match_id):

    if not all_players_joined(
            match_id
    ):
        return False

    if not all_group_completed(
            match_id
    ):
        return False

    return True


# =====================================
# Ready To Start Post?
# =====================================

def post_ready(
        match_id,
        post
):

    return all_selection_completed(
        match_id,
        post
    )


# =====================================
# Draft Status
# =====================================

def draft_status(match_id):

    status = {}

    for player in PLAYERS:

        status[player] = {

            "Joined":
                player_joined(
                    match_id,
                    player
                ),

            "Groups":
                player_group_completed(
                    match_id,
                    player
                )

        }

    return status


# =====================================
# Selection Status
# =====================================

def selection_status(
        match_id,
        post
):

    status = {}

    for player in PLAYERS:

        status[player] = player_selection_completed(
            match_id,
            post,
            player
        )

    return status


# =====================================
# Match Lobby Status
# =====================================

def lobby_status(match_id):

    return {

        "Joined":
            total_joined(
                match_id
            ),

        "Ready":
            match_ready(
                match_id
            ),

        "GroupsLocked":
            all_group_completed(
                match_id
            ),

        "Players":
            joined_players(
                match_id
            )

    }
#----------
