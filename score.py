from sheet import get_scores


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
            r["Som"]
        )

        score["Joy"] += float(
            r["Joy"]
        )

        score["Krish"] += float(
            r["Krish"]
        )

    return score


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
