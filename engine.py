from sheet import (
    get_selection,
    save_call,
    update_post,
    update_call
)

from howstat import get_player_stats
from call import determine
from sequence import (
    next_call,
    next_post
)


# =====================================
# Get card URL by position
# =====================================
def get_card(match_id, post, player, slot):

    cards = get_selection(
        match_id,
        post,
        player
    )

    if cards is None:
        return None

    if slot < 1 or slot > 3:
        return None

    return cards[slot - 1]


# =====================================
# Play One Call
# =====================================
def play_call(
        match_id,
        post,
        call_no,
        category,
        players,
        card_slot,
        point
):

    values = {}

    # -----------------------------
    # Load stats of all players
    # -----------------------------
    for p in players:

        url = get_card(
            match_id,
            post,
            p,
            card_slot
        )

        if not url:
            continue

        stats = get_player_stats(
            url
        )

        value = stats.get(
            category,
            0
        )

        values[p] = value

    if len(values) == 0:
        return None

    # -----------------------------
    # Determine winner
    # -----------------------------
    result = determine(
        values,
        point,
        category
    )

    som = result.get(
        "Som",
        0
    )

    joy = result.get(
        "Joy",
        0
    )

    krish = result.get(
        "Krish",
        0
    )

    # -----------------------------
    # Save in Scores sheet
    # -----------------------------
    save_call(
        match_id,
        post,
        call_no,
        category,
        som,
        joy,
        krish
    )

    # -----------------------------
    # Advance sequence
    # -----------------------------
    new_call = next_call(
        call_no
    )

    if new_call is None:

        new_post = next_post(
            post
        )

        if new_post:

            update_post(
                match_id,
                new_post
            )

            update_call(
                match_id,
                1
            )

    else:

        update_call(
            match_id,
            new_call
        )

    return {
        "category": category,
        "values": values,
        "points": result
    }


# =====================================
# Check post complete
# =====================================
def post_complete(
        call_no
):

    return call_no >= 18


# =====================================
# Check game complete
# =====================================
def game_complete(
        post
):

    return post >= 12


# =====================================
# Total Calls
# =====================================
def total_calls():

    return 12 * 18


# =====================================
# Total Posts
# =====================================
def total_posts():

    return 12
