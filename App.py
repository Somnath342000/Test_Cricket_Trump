import streamlit as st
import random
import string
import gspread
from google.oauth2.service_account import Credentials


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

        st.success("Match Created")

        st.write("### Match ID")

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

        st.session_state.match_id = match.upper()
        st.session_state.player = player

        st.success("Joined Successfully")

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
#---------- part 2---------

import streamlit as st
import random

players = ["Joy", "Krish", "Som"]

st.header("🎲 Batting Group Toss")

if st.button("Start Batting Toss"):

    order = random.sample(players,3)

    st.success("Batting Toss Result")

    st.write("🥇 1st :", order[0])
    st.write("🥈 2nd :", order[1])
    st.write("🥉 3rd :", order[2])

    draft_order = [
        order[0],
        order[1],
        order[2],
        order[2],
        order[1],
        order[0]
    ]

    groups = ["A","B","C","D","E","F"]

    st.subheader("Snake Draft")

    for i in range(6):
        st.write(f"Pick {i+1} : {draft_order[i]} chooses one group")
