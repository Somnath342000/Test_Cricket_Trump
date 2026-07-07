import streamlit as st
import pandas as pd 
import random
import string
import gspread
from google.oauth2.service_account import Credentials
from sheet import create_match, join_match
from draft import batting_toss, bowling_toss
from group import pick_group
from player import select_player

st.set_page_config(page_title="Cricket Trump Cards", layout="wide")

st.title("🏏 Cricket Stats Trump Cards")

# -------------------------
# Session State
# -------------------------
if "match_id" not in st.session_state:
    st.session_state.match_id = ""

if "player" not in st.session_state:
    st.session_state.player = ""

# -------------------------
# Generate Match ID
# -------------------------
def generate_match():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

menu = st.sidebar.radio(
    "Menu",
    ["Create Match", "Join Match"]
)
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

    sheet = client.open_by_key(
        "1cmH0UZbWBvkmjbPq2dP5HCKsKEY2FFaB"
    )

    return sheet

# -------------------------
# Create Match
# -------------------------
if menu == "Create Match":

    st.header("Create Match")

    player = st.selectbox(
        "Your Name",
        ["Joy", "Krish", "Som"]
    )

    if st.button("Create"):

        match = generate_match()

        st.session_state.match_id = match
        st.session_state.player = player

        sheet = connect_sheet()
        match_sheet = sheet.worksheet("Match")

        match_sheet.append_row([
            match,
            player,
            "Waiting",
            "",
            ""
        ])

        st.success("Match Created")
        st.code(match)
        st.info("Share this Match ID with other players.")

# -------------------------
# Join Match
# -------------------------
else:

    st.header("Join Match")

    player = st.selectbox(
        "Your Name",
        ["Joy", "Krish", "Som"]
    )

    match = st.text_input("Enter Match ID")

    if st.button("Join"):

        sheet = connect_sheet()
        match_sheet = sheet.worksheet("Match")

        rows = match_sheet.get_all_values()

        found = False

        for r in rows:
            if r[0] == match.upper():
                found = True
                break

        if found:

            st.session_state.match_id = match.upper()
            st.session_state.player = player

            st.success("Match Found")
            st.success("Joined Successfully")

        else:
            st.error("Match ID Not Found")

# -------------------------
# Dashboard
# -------------------------
if st.session_state.match_id != "":

    st.divider()

    st.subheader("Current Match")

    col1,col2 = st.columns(2)

    with col1:
        st.metric("Player",st.session_state.player)

    with col2:
        st.metric("Match ID",st.session_state.match_id)

    st.success("Ready for Toss 🎲")

if st.button("🎲 Start Batting Toss"):
    batting_toss()

if st.button("🎯 Start Bowling Toss"):
    bowling_toss()
    
st.header("🏏 Group Draft")

pick_group(
    st.session_state.match_id,
    st.session_state.player,
    "BAT",
    1
)

pick_group(
    st.session_state.match_id,
    st.session_state.player,
    "BOWL",
    1
)
st.header("🏏 Player Selection")

bat = st.text_input("Your Batting Group")

bowl = st.text_input("Your Bowling Group")

if bat:
    batter = select_player(bat, "bat")

if bowl:
    bowler = select_player(bowl, "bowl")

select_player(
    st.session_state.match_id,
    st.session_state.player,
    "A",
    "BAT 1"
)

select_player(
    st.session_state.match_id,
    st.session_state.player,
    "E",
    "BAT 2"
)

select_player(
    st.session_state.match_id,
    st.session_state.player,
    "L",
    "BOWL"
)
