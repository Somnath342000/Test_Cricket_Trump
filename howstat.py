import requests
from bs4 import BeautifulSoup
import streamlit as st


@st.cache_data(show_spinner=False)
def get_page(url):

    r = requests.get(
        url,
        timeout=30
    )

    return r.text


def get_stat(url):

    html = get_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup
