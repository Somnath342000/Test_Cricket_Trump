import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


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


def create_match(match_id, player):

    ws = connect_sheet().worksheet("Match")

    ws.append_row([
        match_id,
        player,
        "Waiting",
        "",
        ""
    ])


def join_match(match_id):

    ws = connect_sheet().worksheet("Match")

    rows = ws.get_all_values()

    for row in rows[1:]:      # Header row বাদ
        if row[0] == match_id:
            return True

    return False


def get_sheet(name):

    return connect_sheet().worksheet(name)
