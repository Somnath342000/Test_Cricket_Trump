import streamlit as st
import random
import string

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
