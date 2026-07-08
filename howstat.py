import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup


@st.cache_data(show_spinner=False)
def get_page(url):

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    r.raise_for_status()

    return r.text


def parse_best(text):

    try:
        w, r = text.split("/")
        return (
            int(w),
            int(r)
        )
    except:
        return (
            0,
            9999
        )


@st.cache_data(show_spinner=False)
def get_player_stats(url):

    html = get_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    txt = soup.get_text(
        "\n",
        strip=True
    )

    stats = {}

    lines = txt.split("\n")

    for i, line in enumerate(lines):

        line = line.strip()

        if "Matches" in line:
            stats["Matches"] = int(
                lines[i + 1]
            )

        elif "Innings" in line:
            stats["Innings"] = int(
                lines[i + 1]
            )

        elif "Aggregate" in line:
            stats["Aggregate"] = int(
                lines[i + 1]
            )

        elif "Highest Score" in line:
            stats["Highest Score"] = int(
                lines[i + 1]
            )

        elif "Average" in line:
            try:
                stats["Average"] = float(
                    lines[i + 1]
                )
            except:
                pass

        elif "50s" in line:
            stats["50s"] = int(
                lines[i + 1]
            )

        elif "100s" in line:
            stats["100s"] = int(
                lines[i + 1]
            )

        elif "200s" in line:
            stats["200s"] = int(
                lines[i + 1]
            )

        elif "300s" in line:
            stats["300s"] = int(
                lines[i + 1]
            )

        elif "Balls Faced" in line:
            stats["Balls Faced"] = int(
                lines[i + 1]
            )

        elif "Wickets" in line:
            stats["Wickets"] = int(
                lines[i + 1]
            )

        elif "Catches" in line:
            stats["Catches"] = int(
                lines[i + 1]
            )

        elif "Best - Innings" in line:
            stats["Best Innings"] = parse_best(
                lines[i + 1]
            )

        elif "Best - Match" in line:
            stats["Best Match"] = parse_best(
                lines[i + 1]
            )

    return stats
    #---------------part 2--------#
    
    def compare_best(a, b):

    wa, ra = a
    wb, rb = b

    if wa > wb:
        return 1

    if wb > wa:
        return -1

    if ra < rb:
        return 1

    if rb < ra:
        return -1

    return 0
