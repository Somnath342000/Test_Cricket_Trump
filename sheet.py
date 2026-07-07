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

    sheet = connect_sheet().worksheet("Match")

    sheet.append_row([
        match_id,
        player,
        "Waiting",
        "",
        ""
    ])


def join_match(match_id):

    sheet = connect_sheet().worksheet("Match")

    rows = sheet.get_all_values()

    for row in rows:
        if row[0] == match_id:
            return True

    return False
