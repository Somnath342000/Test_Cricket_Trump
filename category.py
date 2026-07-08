HIGHER = [
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

LOWER = [
    "Ducks",
    "Runs Conceded",
    "Bowling Average",
    "Economy Rate",
    "Strike Rate"
]


def is_higher(category):
    return category in HIGHER


def is_lower(category):
    return category in LOWER
