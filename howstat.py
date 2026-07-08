import requests
import streamlit as st
from bs4 import BeautifulSoup


# ==========================
# Download Page
# ==========================
@st.cache_data(show_spinner=False)
def get_page(url):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    r.raise_for_status()

    return r.text


# ==========================
# Safe Number
# ==========================
def to_int(value):

    try:
        value = value.replace(",", "")
        return int(value)
    except:
        return 0


def to_float(value):

    try:
        value = value.replace(",", "")
        return float(value)
    except:
        return 0.0


# ==========================
# Parse BBI / BBM
# ==========================
def parse_best(text):

    try:
        w, r = text.split("/")
        return (
            int(w.strip()),
            int(r.strip())
        )
    except:
        return (
            0,
            9999
        )


# ==========================
# Compare BBI / BBM
# Return:
# 1 = first wins
# -1 = second wins
# 0 = tie
# ==========================
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


# ==========================
# Parse Statistics
# ==========================
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

    lines = txt.split("\n")

    stats = {}

    for i, line in enumerate(lines):

        line = line.strip()

        try:
            value = lines[i + 1].strip()
        except:
            value = ""

        # -----------------
        # Batting
        # -----------------
        if line == "Matches":
            stats["Matches"] = to_int(value)

        elif line == "Innings":
            stats["Innings"] = to_int(value)

        elif line == "Aggregate":
            stats["Aggregate"] = to_int(value)

        elif line == "Highest Score":
            stats["Highest Score"] = to_int(value)

        elif line == "Average":
            stats["Average"] = to_float(value)

        elif line == "50s":
            stats["50s"] = to_int(value)

        elif line == "100s":
            stats["100s"] = to_int(value)

        elif line == "200s":
            stats["200s"] = to_int(value)

        elif line == "300s":
            stats["300s"] = to_int(value)

        elif line == "4s":
            stats["4s"] = to_int(value)

        elif line == "6s":
            stats["6s"] = to_int(value)

        elif line == "Balls Faced":
            stats["Balls Faced"] = to_int(value)

        elif line == "Top Scored in Innings":
            stats["Top Scored in Innings"] = to_int(value)

        elif line == "Ducks":
            stats["Ducks"] = to_int(value)

        # -----------------
        # Bowling
        # -----------------
        elif line == "Balls":
            stats["Balls"] = to_int(value)

        elif line == "Maidens":
            stats["Maidens"] = to_int(value)

        elif line == "Runs Conceded":
            stats["Runs Conceded"] = to_int(value)

        elif line == "Wickets":
            stats["Wickets"] = to_int(value)

        elif line == "Bowling Average":
            stats["Bowling Average"] = to_float(value)

        elif line == "Economy Rate":
            stats["Economy Rate"] = to_float(value)

        elif line == "Strike Rate":
            stats["Strike Rate"] = to_float(value)

        elif line == "5 Wickets in Innings":
            stats["5 Wickets in Innings"] = to_int(value)

        elif line == "10 Wickets in Match":
            stats["10 Wickets in Match"] = to_int(value)

        elif line == "Best - Innings":
            stats["Best Innings"] = parse_best(value)

        elif line == "Best - Match":
            stats["Best Match"] = parse_best(value)

        # -----------------
        # Fielding
        # -----------------
        elif line == "Catches":
            stats["Catches"] = to_int(value)

        elif line == "Most Catches in Innings":
            stats["Most Catches in Innings"] = to_int(value)

        elif line == "Most Catches in Match":
            stats["Most Catches in Match"] = to_int(value)

    return stats


# ==========================
# Get One Category
# ==========================
def get_value(url, category):

    stats = get_player_stats(url)

    if category in stats:
        return stats[category]

    return 0


# ==========================
# Special Category Check
# ==========================
def is_best_category(category):

    return category in [
        "Best Innings",
        "Best Match"
    ]
