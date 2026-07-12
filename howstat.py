import pandas as pd
import streamlit as st

# =====================================
# HOWSTAT ENGINE
# PART - 1
# =====================================

PLAYER_FILE = "Players.xlsx"


# =====================================
# LOAD DATABASE
# =====================================

@st.cache_data(show_spinner=False)
def load_database():
    """
    Load complete player database.

    Excel Columns Example

    Player Name
    Group
    Matches
    Innings
    Aggregate
    Highest Score
    Average
    50s
    100s
    200s
    300s
    Ducks
    4s
    6s
    Balls Faced
    Top Scored in Innings

    Balls
    Maidens
    Runs Conceded
    Wickets
    Bowling Average
    5 Wickets in Innings
    10 Wickets in Match
    Best - Innings
    Best - Match
    Economy Rate
    Strike Rate

    Catches
    Most Catches in Innings
    Most Catches in Match
    """

    df = pd.read_excel(
        PLAYER_FILE
    )

    df = df.fillna("")

    return df


# =====================================
# TOTAL PLAYERS
# =====================================

def total_players():

    return len(
        load_database()
    )


# =====================================
# ALL PLAYER NAMES
# =====================================

def player_names():

    df = load_database()

    return sorted(

        df["Player Name"]

        .tolist()

    )


# =====================================
# PLAYER EXISTS
# =====================================

def player_exists(player):

    return player in player_names()


# =====================================
# GET PLAYER ROW
# =====================================

def player_row(player):

    df = load_database()

    row = df[
        df["Player Name"] == player
    ]

    if row.empty:
        return None

    return row.iloc[0]


# =====================================
# PLAYER GROUP
# =====================================

def player_group(player):

    row = player_row(player)

    if row is None:
        return None

    return row["Group"]


# =====================================
# COMPLETE PLAYER DATA
# =====================================

def player_data(player):

    row = player_row(player)

    if row is None:
        return None

    return row.to_dict()


# =====================================
# PLAYER STAT
# =====================================

def get_player_stat(

        player,

        category

):

    data = player_data(player)

    if data is None:

        return None

    return data.get(
        category
    )


# =====================================
# AVAILABLE COLUMNS
# =====================================

def database_columns():

    return list(

        load_database()

        .columns

    )


# =====================================
# VALID CATEGORY
# =====================================

def category_exists(category):

    return (

        category

        in

        database_columns()

    )


# =====================================
# DATABASE SUMMARY
# =====================================

def database_summary():

    df = load_database()

    return {

        "Players":

            len(df),

        "Columns":

            len(df.columns),

        "Groups":

            sorted(

                df["Group"]

                .unique()

                .tolist()

            )

    }
#-------part2------#
# =====================================
# HOWSTAT ENGINE
# PART - 2
# Data Cleaning & Value Engine
# =====================================

import re

# =====================================
# Higher Value Categories
# =====================================

HIGHER_VALUE = [

    "Matches",
    "Innings",
    "Aggregate",
    "Highest Score",
    "Average",
    "50s",
    "100s",
    "200s",
    "300s",
    "4s",
    "6s",
    "Balls Faced",
    "Top Scored in Innings",

    "Balls",
    "Maidens",
    "Wickets",
    "5 Wickets in Innings",
    "10 Wickets in Match",

    "Catches",
    "Most Catches in Innings",
    "Most Catches in Match"

]

# =====================================
# Lower Value Categories
# =====================================

LOWER_VALUE = [

    "Ducks",
    "Bowling Average",
    "Economy Rate",
    "Strike Rate",
    "Runs Conceded"

]

# =====================================
# Bowling Figure Categories
# =====================================

FIGURE_VALUE = [

    "Best - Innings",
    "Best - Match"

]

# =====================================
# Is Higher Category
# =====================================

def is_higher(category):

    return category in HIGHER_VALUE


# =====================================
# Is Lower Category
# =====================================

def is_lower(category):

    return category in LOWER_VALUE


# =====================================
# Is Figure Category
# =====================================

def is_figure(category):

    return category in FIGURE_VALUE


# =====================================
# Empty Value
# =====================================

def empty_value(value):

    if value is None:
        return True

    if str(value).strip() == "":
        return True

    if str(value).lower() == "nan":
        return True

    return False


# =====================================
# Numeric Value
# =====================================

def numeric(value):

    if empty_value(value):
        return 0

    try:

        value = str(value)

        value = value.replace(",", "")

        return float(value)

    except:

        return 0


# =====================================
# Integer Value
# =====================================

def integer(value):

    return int(

        round(

            numeric(value)

        )

    )


# =====================================
# Clean Text
# =====================================

def clean_text(value):

    if empty_value(value):
        return ""

    return str(value).strip()


# =====================================
# Parse Bowling Figure
# Example:
# 9/56
# 10/240
# =====================================

def parse_figure(value):

    value = clean_text(value)

    if "/" not in value:

        return (

            0,

            9999

        )

    try:

        wickets, runs = value.split("/")

        wickets = int(wickets)

        runs = int(runs)

        return (

            wickets,

            runs

        )

    except:

        return (

            0,

            9999

        )


# =====================================
# Figure To Dictionary
# =====================================

def figure_dict(value):

    wickets, runs = parse_figure(value)

    return {

        "Wickets": wickets,

        "Runs": runs

    }


# =====================================
# Figure Text
# =====================================

def figure_text(value):

    wickets, runs = parse_figure(value)

    return f"{wickets}/{runs}"


# =====================================
# Compare Figures
# Return
# 1 = First Better
# 2 = Second Better
# 0 = Equal
# =====================================

def compare_figures(

        figure1,

        figure2

):

    w1, r1 = parse_figure(

        figure1

    )

    w2, r2 = parse_figure(

        figure2

    )

    # More wickets win

    if w1 > w2:

        return 1

    if w2 > w1:

        return 2

    # Same wickets
    # Less runs win

    if r1 < r2:

        return 1

    if r2 < r1:

        return 2

    return 0


# =====================================
# Valid Player
# =====================================

def valid_player(player):

    return player_exists(player)


# =====================================
# Valid Category
# =====================================

def valid_category(category):

    return category_exists(category)


# =====================================
# Read Stat
# =====================================

def stat(player, category):

    if not valid_player(player):

        return None

    if not valid_category(category):

        return None

    return get_player_stat(

        player,

        category

    )


# =====================================
# Numeric Stat
# =====================================

def numeric_stat(

        player,

        category

):

    return numeric(

        stat(

            player,

            category

        )

    )


# =====================================
# Figure Stat
# =====================================

def figure_stat(

        player,

        category

):

    return parse_figure(

        stat(

            player,

            category

        )

    )


# =====================================
# Player Summary
# =====================================

def player_summary(player):

    if not valid_player(player):

        return None

    return {

        "Player":

            player,

        "Group":

            player_group(player),

        "Matches":

            numeric_stat(

                player,

                "Matches"

            ),

        "Runs":

            numeric_stat(

                player,

                "Aggregate"

            ),

        "Wickets":

            numeric_stat(

                player,

                "Wickets"

            ),

        "Catches":

            numeric_stat(

                player,

                "Catches"

            )

    }
#---------part 3A-------->
# =====================================
# HOWSTAT ENGINE
# PART - 3A
# PLAYER INDEX ENGINE
# =====================================

from functools import lru_cache

# =====================================
# PLAYER INDEX
# =====================================

@st.cache_data(show_spinner=False)
def player_index():

    """
    Create player dictionary.

    Key:
        Player Name

    Value:
        Complete Player Record
    """

    df = load_database()

    index = {}

    for _, row in df.iterrows():

        record = row.to_dict()

        name = str(
            record["Player Name"]
        ).strip()

        index[name] = record

    return index


# =====================================
# GET RECORD
# =====================================

def player_record(player):

    return player_index().get(player)


# =====================================
# FAST PLAYER DATA
# =====================================

def fast_player_data(player):

    record = player_record(player)

    if record is None:

        return None

    return dict(record)


# =====================================
# FAST PLAYER STAT
# =====================================

def fast_stat(

        player,

        category

):

    record = player_record(player)

    if record is None:

        return None

    return record.get(category)


# =====================================
# PLAYER FOUND?
# =====================================

def player_found(player):

    return player in player_index()


# =====================================
# PLAYER COUNT
# =====================================

def player_count():

    return len(

        player_index()

    )


# =====================================
# ALL PLAYERS
# =====================================

def all_players():

    return sorted(

        player_index().keys()

    )


# =====================================
# SEARCH PLAYER
# =====================================

def search_player(keyword):

    keyword = str(

        keyword

    ).lower().strip()

    result = []

    for player in all_players():

        if keyword in player.lower():

            result.append(player)

    return result


# =====================================
# PLAYER POSITION
# =====================================

def player_position(player):

    players = all_players()

    if player not in players:

        return -1

    return players.index(player) + 1


# =====================================
# PLAYER EXISTS
# =====================================

def exists(player):

    return player_found(player)


# =====================================
# GET GROUP
# =====================================

def group(player):

    record = player_record(player)

    if record is None:

        return None

    return record.get("Group")


# =====================================
# PLAYER INFO
# =====================================

def player_info(player):

    record = player_record(player)

    if record is None:

        return None

    return {

        "Name":

            player,

        "Group":

            record.get("Group"),

        "Matches":

            record.get("Matches"),

        "Runs":

            record.get("Aggregate"),

        "Wickets":

            record.get("Wickets"),

        "Catches":

            record.get("Catches")

    }


# =====================================
# REFRESH CACHE
# =====================================

def refresh_database():

    load_database.clear()

    player_index.clear()


# =====================================
# DATABASE READY?
# =====================================

def database_ready():

    try:

        return (

            player_count()

            >

            0

        )

    except:

        return False


# =====================================
# DATABASE STATUS
# =====================================

def database_status():

    return {

        "Loaded":

            database_ready(),

        "Players":

            player_count(),

        "Columns":

            len(

                database_columns()

            )

    }
#-----------part 3b-----#
