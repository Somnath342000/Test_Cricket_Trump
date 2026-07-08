from sheet import get_scores


# ==========================
# Total Score Of One Post
# ==========================
def total_score(match_id, post):

    rows = get_scores(
        match_id,
        post
    )

    score = {
        "Som": 0,
        "Joy": 0,
        "Krish": 0
    }

    for r in rows:

        score["Som"] += float(
            r.get("Som", 0) or 0
        )

        score["Joy"] += float(
            r.get("Joy", 0) or 0
        )

        score["Krish"] += float(
            r.get("Krish", 0) or 0
        )

    return score


# ==========================
# Ranking Of One Post
# ==========================
def result(match_id, post):

    score = total_score(
        match_id,
        post
    )

    data = sorted(
        score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return data


# ==========================
# Score Of One Player
# ==========================
def player_score(
        match_id,
        post,
        player
):

    score = total_score(
        match_id,
        post
    )

    return score.get(
        player,
        0
    )


# ==========================
# Overall Match Score
# All 12 Posts
# ==========================
def overall_score(match_id):

    score = {
        "Som": 0,
        "Joy": 0,
        "Krish": 0
    }

    for post in range(1, 13):

        s = total_score(
            match_id,
            post
        )

        score["Som"] += s["Som"]
        score["Joy"] += s["Joy"]
        score["Krish"] += s["Krish"]

    return score


# ==========================
# Final Match Ranking
# ==========================
def final_result(match_id):

    score = overall_score(
        match_id
    )

    data = sorted(
        score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return data


# ==========================
# Winner Of A Post
# ==========================
def post_winner(
        match_id,
        post
):

    data = result(
        match_id,
        post
    )

    if not data:
        return None

    return data[0]


# ==========================
# Final Winner
# ==========================
def match_winner(match_id):

    data = final_result(
        match_id
    )

    if not data:
        return None

    return data[0]
