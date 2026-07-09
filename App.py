import streamlit as st
import random
import string

from sheet import (
    create_match,
    match_exists,
    get_match
)

from draft import (
    batting_toss,
    bowling_toss,
    show_toss
)

from group import (
    draft_screen,
    group_completed
)

from player import (
    selection_page
)

from score import (
    total_score,
    result
)

# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="Cricket Trump Cards",
    layout="wide"
)

st.title("🏏 Cricket Stats Trump Cards")
st.title("🏏 Cricket Stats Trump Cards")

# Google Sheet Test
if st.button("Test Google Sheet"):
    try:
        sh = connect_sheet()
        st.success(f"Connected ✅ {sh.title}")
    except Exception as e:
        st.error(e)

# =====================================
# Session State
# =====================================
if "match_id" not in st.session_state:
    st.session_state.match_id = ""

if "player" not in st.session_state:
    st.session_state.player = ""

# =====================================
# Match ID Generator
# =====================================
def generate_match_id():

    return ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits,
            k=6
        )
    )

# =====================================
# Sidebar
# =====================================
menu = st.sidebar.radio(
    "Menu",
    [
        "Create Match",
        "Join Match"
    ]
)

# =====================================
# Create Match
# =====================================
if menu == "Create Match":

    st.header("Create Match")

    player = st.selectbox(
        "Your Name",
        [
            "Som",
            "Joy",
            "Krish"
        ]
    )

    if st.button("Create Match"):

        match_id = generate_match_id()

        create_match(
            match_id
        )

        st.session_state.match_id = match_id
        st.session_state.player = player

        st.success(
            "Match Created Successfully"
        )

        st.code(match_id)

        st.info(
            "Share this Match ID with other players."
        )

# =====================================
# Join Match
# =====================================
if menu == "Join Match":

    st.header("Join Match")

    player = st.selectbox(
        "Your Name",
        [
            "Som",
            "Joy",
            "Krish"
        ]
    )

    match_id = st.text_input(
        "Enter Match ID"
    )

    if st.button("Join Match"):

        match_id = (
            match_id
            .strip()
            .upper()
        )

        if match_exists(
                match_id
        ):

            st.session_state.match_id = (
                match_id
            )

            st.session_state.player = (
                player
            )

            st.success(
                "Joined Successfully"
            )

        else:
            st.error(
                "Match ID Not Found"
            )

# =====================================
# Dashboard
# =====================================
if st.session_state.match_id:

    st.divider()

    match_id = (
        st.session_state.match_id
    )

    player = (
        st.session_state.player
    )

    st.subheader(
        "Current Match"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Player",
            player
        )

    with c2:
        st.metric(
            "Match ID",
            match_id
        )

    match = get_match(
        match_id
    )

    if match:

        current_post = int(
            match["CurrentPost"]
        )

        current_call = int(
            match["CurrentCall"]
        )

    else:

        current_post = 1
        current_call = 1

    st.info(
        f"Post : {current_post} | Call : {current_call}"
    )

    # =====================================
    # Toss
    # =====================================
    st.divider()

    st.header("🎲 Toss")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
                "Batting Toss"
        ):

            order = batting_toss(
                match_id
            )

            show_toss(
                "🏏 Batting Toss",
                order
            )

    with col2:

        if st.button(
                "Bowling Toss"
        ):

            order = bowling_toss(
                match_id
            )

            show_toss(
                "🎯 Bowling Toss",
                order
            )

    # =====================================
    # Group Draft
    # =====================================
    st.divider()

    st.header(
        "🏏 Group Draft"
    )

    draft_screen(
        match_id,
        player
    )

    # =====================================
    # Player Selection
    # =====================================
    if group_completed(
            match_id,
            player
    ):

        st.divider()

        st.header(
            "🃏 Card Selection"
        )

        selection_page(
            match_id,
            current_post,
            player
        )

    # =====================================
    # Scoreboard
    # =====================================
    st.divider()

    st.header(
        "🏆 Scoreboard"
    )

    score = total_score(
        match_id,
        current_post
    )

    st.dataframe(
        score,
        use_container_width=True
    )

    if st.button(
            "Show Ranking"
    ):

        st.write(
            result(
                match_id,
                current_post
            )
        )
