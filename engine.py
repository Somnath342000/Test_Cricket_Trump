import random

PLAYERS = [
    "Som",
    "Joy",
    "Krish"
]

# =====================================
# SNAKE DRAFT
# =====================================

def snake_order(order):
    """
    Example:
    Joy Krish Som

    Return:
    Joy
    Krish
    Som
    Som
    Krish
    Joy
    """

    return [

        order[0],

        order[1],

        order[2],

        order[2],

        order[1],

        order[0]

    ]


# =====================================
# ALL POSSIBLE TOSS ORDERS
# =====================================

ALL_TOSS = [

    ["Som", "Joy", "Krish"],

    ["Som", "Krish", "Joy"],

    ["Joy", "Som", "Krish"],

    ["Joy", "Krish", "Som"],

    ["Krish", "Som", "Joy"],

    ["Krish", "Joy", "Som"]

]


# =====================================
# RANDOM TOSS
# =====================================

def random_toss():

    return random.choice(
        ALL_TOSS
    )


# =====================================
# RANDOM BATTING TOSS
# =====================================

def batting_toss():

    return random_toss()


# =====================================
# RANDOM BOWLING TOSS
# =====================================

def bowling_toss():

    return random_toss()


# =====================================
# GET PLAYER TURN
# =====================================

def draft_turn(
        order,
        pick
):

    draft = snake_order(
        order
    )

    if pick < 1:
        return None

    if pick > 6:
        return None

    return draft[
        pick - 1
    ]


# =====================================
# PLAYER CAN PICK?
# =====================================

def can_pick(
        player,
        order,
        pick
):

    return (

        draft_turn(
            order,
            pick
        )

        ==

        player

    )


# =====================================
# NEXT PICK
# =====================================

def next_pick(
        order,
        picked
):

    draft = snake_order(
        order
    )

    if picked >= 6:
        return None

    return draft[
        picked
    ]


# =====================================
# DRAFT FINISHED?
# =====================================

def draft_finished(
        picked
):

    return picked >= 6


# =====================================
# PICK NUMBER OF PLAYER
# =====================================

def player_pick_numbers(
        player,
        order
):

    draft = snake_order(
        order
    )

    picks = []

    for i, p in enumerate(
            draft,
            start=1
    ):

        if p == player:
            picks.append(i)

    return picks


# =====================================
# FIRST PICK?
# =====================================

def first_pick(
        player,
        order
):

    return (

        player_pick_numbers(
            player,
            order
        )[0]

    )


# =====================================
# SECOND PICK?
# =====================================

def second_pick(
        player,
        order
):

    return (

        player_pick_numbers(
            player,
            order
        )[1]

    )


# =====================================
# TOSS PRIORITY
# Smaller Index = Higher Priority
# =====================================

def toss_priority(
        order,
        player
):

    return order.index(
        player
    )


# =====================================
# DEFAULT PRIORITY
# Used During Tie
# =====================================

def priority_sort(
        players,
        toss_order
):

    return sorted(

        players,

        key=lambda p:

        toss_priority(
            toss_order,
            p
        )

    )
#--------Part 2------#
# =====================================
# ENGINE PART 2 : 18 CALL ENGINE
# =====================================

CALL_POINTS = [
    6,
    5,
    4,
    3,
    2,
    1,
    6,
    5,
    4,
    3,
    2,
    1,
    6,
    5,
    4,
    3,
    2,
    1
]


# =====================================
# TOTAL CALLS
# =====================================

def total_calls():

    return 18


# =====================================
# CALL POINT
# =====================================

def call_point(call_no):

    if call_no < 1:
        return 0

    if call_no > 18:
        return 0

    return CALL_POINTS[
        call_no - 1
    ]


# =====================================
# CALL SEQUENCE
# =====================================

def build_call_sequence(order):

    sequence = []

    for i in range(6):

        sequence.extend(order)

    return sequence


# =====================================
# CURRENT CALL PLAYER
# =====================================

def current_call_player(
        order,
        call_no
):

    sequence = build_call_sequence(
        order
    )

    if call_no < 1:
        return None

    if call_no > 18:
        return None

    return sequence[
        call_no - 1
    ]


# =====================================
# PLAYER CAN CALL?
# =====================================

def can_call(
        player,
        order,
        call_no
):

    return (

        current_call_player(
            order,
            call_no
        )

        ==

        player

    )


# =====================================
# NEXT CALL PLAYER
# =====================================

def next_call_player(
        order,
        call_no
):

    if call_no >= 18:
        return None

    return current_call_player(
        order,
        call_no + 1
    )


# =====================================
# PREVIOUS CALL PLAYER
# =====================================

def previous_call_player(
        order,
        call_no
):

    if call_no <= 1:
        return None

    return current_call_player(
        order,
        call_no - 1
    )


# =====================================
# PLAYER CALL LIST
# =====================================

def player_calls(
        player,
        order
):

    sequence = build_call_sequence(
        order
    )

    calls = []

    for i, p in enumerate(
            sequence,
            start=1
    ):

        if p == player:

            calls.append(i)

    return calls


# =====================================
# PLAYER POINT LIST
# =====================================

def player_point_list(
        player,
        order
):

    calls = player_calls(
        player,
        order
    )

    points = []

    for c in calls:

        points.append(
            call_point(c)
        )

    return points


# =====================================
# CALL FINISHED?
# =====================================

def call_finished(
        call_no
):

    return call_no >= 18


# =====================================
# REMAINING CALLS
# =====================================

def remaining_calls(
        call_no
):

    return max(
        0,
        18 - call_no
    )


# =====================================
# CALL PROGRESS
# =====================================

def call_progress(
        call_no
):

    return round(
        (call_no / 18) * 100,
        2
    )


# =====================================
# NEXT CALL NUMBER
# =====================================

def next_call_number(
        call_no
):

    if call_no >= 18:
        return None

    return call_no + 1


# =====================================
# PREVIOUS CALL NUMBER
# =====================================

def previous_call_number(
        call_no
):

    if call_no <= 1:
        return None

    return call_no - 1


# =====================================
# CALL SUMMARY
# =====================================

def call_summary(
        order,
        call_no
):

    return {

        "CurrentCall":
            call_no,

        "CurrentPlayer":
            current_call_player(
                order,
                call_no
            ),

        "Point":
            call_point(
                call_no
            ),

        "Remaining":
            remaining_calls(
                call_no
            ),

        "Progress":
            call_progress(
                call_no
            ),

        "NextPlayer":
            next_call_player(
                order,
                call_no
            )

    }
#----------part3----------#
# =====================================
# ENGINE PART 3 : CATEGORY ENGINE
# =====================================

# Higher Value Wins
HIGHER_CATEGORIES = [

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


# =====================================
# Lower Value Wins
# =====================================

LOWER_CATEGORIES = [

    "Ducks",

    "Bowling Average",

    "Economy Rate",

    "Strike Rate",

    "Runs Conceded"

]


# =====================================
# Special Categories
# =====================================

SPECIAL_CATEGORIES = [

    "Best - Innings",

    "Best - Match"

]


# =====================================
# Higher Category?
# =====================================

def is_higher_category(category):

    return category in HIGHER_CATEGORIES


# =====================================
# Lower Category?
# =====================================

def is_lower_category(category):

    return category in LOWER_CATEGORIES


# =====================================
# Special Category?
# =====================================

def is_special_category(category):

    return category in SPECIAL_CATEGORIES


# =====================================
# Valid Category?
# =====================================

def valid_category(category):

    return (

        is_higher_category(category)

        or

        is_lower_category(category)

        or

        is_special_category(category)

    )


# =====================================
# Numeric Value
# =====================================

def numeric(value):

    if value is None:
        return 0

    if value == "":
        return 0

    try:

        return float(value)

    except:

        return 0


# =====================================
# Better Numeric
# =====================================

def better_value(

        value1,

        value2,

        category

):

    value1 = numeric(value1)

    value2 = numeric(value2)

    if is_higher_category(category):

        return value1 > value2

    if is_lower_category(category):

        return value1 < value2

    return False


# =====================================
# Best Numeric
# =====================================

def best_numeric(

        values,

        category

):

    if not values:
        return None

    numbers = [

        numeric(v)

        for v in values

    ]

    if is_higher_category(category):

        return max(numbers)

    if is_lower_category(category):

        return min(numbers)

    return None


# =====================================
# Equal Values
# =====================================

def equal_values(

        value1,

        value2

):

    return (

        numeric(value1)

        ==

        numeric(value2)

    )


# =====================================
# Category Rule
# =====================================

def category_rule(category):

    if is_higher_category(category):

        return "HIGHER"

    if is_lower_category(category):

        return "LOWER"

    if is_special_category(category):

        return "SPECIAL"

    return "UNKNOWN"


# =====================================
# All Categories
# =====================================

def all_categories():

    return (

        HIGHER_CATEGORIES

        +

        LOWER_CATEGORIES

        +

        SPECIAL_CATEGORIES

    )


# =====================================
# Total Categories
# =====================================

def total_categories():

    return len(

        all_categories()

    )


# =====================================
# Category Summary
# =====================================

def category_summary():

    return {

        "Higher":

            HIGHER_CATEGORIES,

        "Lower":

            LOWER_CATEGORIES,

        "Special":

            SPECIAL_CATEGORIES,

        "Total":

            total_categories()

    }
#------part4-----#
# =====================================
# ENGINE PART 4 : BBI / BBM ENGINE
# =====================================

# -------------------------------------
# Parse Bowling Figure
# Example:
# 7/46
# 9/112
# 10/240
# -------------------------------------

def parse_figure(value):

    if value is None:
        return (0, 9999)

    value = str(value).strip()

    if value == "":
        return (0, 9999)

    if "/" not in value:
        return (0, 9999)

    try:

        wickets, runs = value.split("/")

        wickets = int(wickets)

        runs = int(runs)

        return (

            wickets,

            runs

        )

    except:

        return (

            0,

            9999

        )


# -------------------------------------
# Compare Bowling Figure
# Return
# 1 = value1 better
# 2 = value2 better
# 0 = tie
# -------------------------------------

def compare_figure(

        value1,

        value2

):

    w1, r1 = parse_figure(value1)

    w2, r2 = parse_figure(value2)

    # More wickets wins

    if w1 > w2:
        return 1

    if w2 > w1:
        return 2

    # Same wickets
    # Less runs wins

    if r1 < r2:
        return 1

    if r2 < r1:
        return 2

    return 0


# -------------------------------------
# Better Figure?
# -------------------------------------

def better_figure(

        value1,

        value2

):

    return compare_figure(

        value1,

        value2

    ) == 1


# -------------------------------------
# Equal Figure?
# -------------------------------------

def equal_figure(

        value1,

        value2

):

    return compare_figure(

        value1,

        value2

    ) == 0


# -------------------------------------
# Best Figure
# -------------------------------------

def best_figure(values):

    if not values:
        return None

    best = values[0]

    for value in values[1:]:

        if better_figure(

                value,

                best

        ):

            best = value

    return best


# -------------------------------------
# Figure Summary
# -------------------------------------

def figure_summary(value):

    wickets, runs = parse_figure(value)

    return {

        "Wickets": wickets,

        "Runs": runs

    }


# -------------------------------------
# Category Compare
# Used by Winner Engine
# -------------------------------------

def compare_category(

        category,

        value1,

        value2

):

    if category in [

        "Best - Innings",

        "Best - Match"

    ]:

        return compare_figure(

            value1,

            value2

        )

    # Higher Rule

    if is_higher_category(category):

        v1 = numeric(value1)

        v2 = numeric(value2)

        if v1 > v2:
            return 1

        if v2 > v1:
            return 2

        return 0

    # Lower Rule

    if is_lower_category(category):

        v1 = numeric(value1)

        v2 = numeric(value2)

        if v1 < v2:
            return 1

        if v2 < v1:
            return 2

        return 0

    return 0


# -------------------------------------
# Winner Value
# -------------------------------------

def winning_value(

        category,

        values

):

    if not values:
        return None

    if category in [

        "Best - Innings",

        "Best - Match"

    ]:

        return best_figure(values)

    if is_higher_category(category):

        return max(

            numeric(v)

            for v in values

        )

    if is_lower_category(category):

        return min(

            numeric(v)

            for v in values

        )

    return None
#---------Part 5-----#
# =====================================
# ENGINE PART 5 : TIE & WINNER ENGINE
# =====================================

from collections import defaultdict

# =====================================
# Get Winner Value
# =====================================

def winner_value(category, values):

    return winning_value(
        category,
        values
    )


# =====================================
# Winner Players
# =====================================

def winner_players(
        player_values,
        category
):

    best = winner_value(
        category,
        list(player_values.values())
    )

    winners = []

    for player, value in player_values.items():

        if category in [
            "Best - Innings",
            "Best - Match"
        ]:

            if equal_figure(
                value,
                best
            ):
                winners.append(player)

        else:

            if numeric(value) == numeric(best):
                winners.append(player)

    return winners


# =====================================
# Rank Players
# =====================================

def rank_players(
        player_values,
        category,
        toss_order
):

    data = []

    for player, value in player_values.items():

        data.append({

            "Player": player,

            "Value": value

        })

    # Higher Category

    if is_higher_category(category):

        data.sort(

            key=lambda x: (

                -numeric(
                    x["Value"]
                ),

                toss_priority(
                    toss_order,
                    x["Player"]
                )

            )

        )

    # Lower Category

    elif is_lower_category(category):

        data.sort(

            key=lambda x: (

                numeric(
                    x["Value"]
                ),

                toss_priority(
                    toss_order,
                    x["Player"]
                )

            )

        )

    # Special

    else:

        data.sort(

            key=lambda x: (

                -parse_figure(
                    x["Value"]
                )[0],

                parse_figure(
                    x["Value"]
                )[1],

                toss_priority(
                    toss_order,
                    x["Player"]
                )

            )

        )

    return data


# =====================================
# Point Split
# =====================================

def split_points(
        point,
        winners
):

    share = point / len(
        winners
    )

    result = {}

    for player in PLAYERS:

        result[player] = 0

    for player in winners:

        result[player] = share

    return result


# =====================================
# Call Result
# =====================================

def call_result(

        category,

        point,

        player_values,

        toss_order

):

    winners = winner_players(

        player_values,

        category

    )

    ranking = rank_players(

        player_values,

        category,

        toss_order

    )

    score = split_points(

        point,

        winners

    )

    return {

        "Winner":

            winners,

        "Ranking":

            ranking,

        "Points":

            score

    }


# =====================================
# Sequence Engine
# =====================================

def sequence_order(

        ranking

):

    return [

        r["Player"]

        for r in ranking

    ]


# =====================================
# Next Caller Sequence
# =====================================

def next_sequence(

        player_values,

        category,

        toss_order

):

    ranking = rank_players(

        player_values,

        category,

        toss_order

    )

    return sequence_order(

        ranking

    )


# =====================================
# Tie Count
# =====================================

def tie_count(

        player_values,

        category

):

    return len(

        winner_players(

            player_values,

            category

        )

    )


# =====================================
# Is Tie?
# =====================================

def is_tie(

        player_values,

        category

):

    return tie_count(

        player_values,

        category

    ) > 1


# =====================================
# Call Summary
# =====================================

def call_summary(

        category,

        point,

        player_values,

        toss_order

):

    result = call_result(

        category,

        point,

        player_values,

        toss_order

    )

    return {

        "Category":

            category,

        "Point":

            point,

        "Winner":

            result["Winner"],

        "Ranking":

            result["Ranking"],

        "Points":

            result["Points"],

        "Tie":

            is_tie(

                player_values,

                category

            )

    }
#---------part 6-------#
# =====================================
# ENGINE PART 6
# CARD DISTRIBUTION ENGINE
# =====================================

BASE_CARDS = 3


# =====================================
# Three Way Tie
# =====================================

def three_way_tie(score):

    values = list(score.values())

    return values[0] == values[1] == values[2]


# =====================================
# Joint First
# =====================================

def joint_first(data):

    return data[0][1] == data[1][1]


# =====================================
# Joint Second
# =====================================

def joint_second(data):

    return data[1][1] == data[2][1]


# =====================================
# Card Distribution
# =====================================

def card_distribution(result):

    """
    result example

    [
        ("Joy",23),
        ("Som",22),
        ("Krish",18)
    ]
    """

    score = {}

    for p, s in result:
        score[p] = s

    # -------------------------
    # Case 8
    # -------------------------

    if three_way_tie(score):

        return {

            result[0][0]: 3,
            result[1][0]: 3,
            result[2][0]: 3

        }

    # -------------------------
    # Case 5
    # -------------------------

    if joint_first(result):

        return {

            result[0][0]: 4,
            result[1][0]: 4,
            result[2][0]: 1

        }

    # -------------------------
    # Joint Second
    # -------------------------

    if joint_second(result):

        gap = result[0][1] - result[1][1]

        # Case 7

        if gap >= 9:

            return {

                result[0][0]: 7,
                result[1][0]: 1,
                result[2][0]: 1

            }

        # Case 6

        return {

            result[0][0]: 5,
            result[1][0]: 2,
            result[2][0]: 2

        }

    # -------------------------
    # Normal Winner
    # -------------------------

    gap = result[0][1] - result[1][1]

    # -------------------------
    # Case 4
    # -------------------------

    if gap >= 18:

        return {

            result[0][0]: 8,
            result[1][0]: 1,
            result[2][0]: 0

        }

    # -------------------------
    # Case 3
    # -------------------------

    if gap >= 9:

        return {

            result[0][0]: 7,
            result[1][0]: 2,
            result[2][0]: 0

        }

    # -------------------------
    # Case 2
    # -------------------------

    if gap > 2:

        return {

            result[0][0]: 6,
            result[1][0]: 3,
            result[2][0]: 0

        }

    # -------------------------
    # Case 1
    # -------------------------

    return {

        result[0][0]: 5,
        result[1][0]: 4,
        result[2][0]: 0

    }


# =====================================
# Cards Of One Player
# =====================================

def player_cards(result, player):

    cards = card_distribution(result)

    return cards.get(player, 0)


# =====================================
# Winner
# =====================================

def post_winner(result):

    return result[0]


# =====================================
# Runner Up
# =====================================

def runner_up(result):

    return result[1]


# =====================================
# Third Place
# =====================================

def third_place(result):

    return result[2]


# =====================================
# Total Cards Check
# =====================================

def valid_distribution(result):

    cards = card_distribution(result)

    return sum(cards.values()) == 9


# =====================================
# Distribution Case Name
# =====================================

def distribution_case(result):

    score = {}

    for p, s in result:
        score[p] = s

    if three_way_tie(score):
        return "CASE 8"

    if joint_first(result):
        return "CASE 5"

    if joint_second(result):

        gap = result[0][1] - result[1][1]

        if gap >= 9:
            return "CASE 7"

        return "CASE 6"

    gap = result[0][1] - result[1][1]

    if gap >= 18:
        return "CASE 4"

    if gap >= 9:
        return "CASE 3"

    if gap > 2:
        return "CASE 2"

    return "CASE 1"
#--------part 7---------#
# =====================================
# ENGINE PART 7
# POST & MATCH ENGINE
# =====================================

TOTAL_POSTS = 12
CALLS_PER_POST = 18


# =====================================
# First Post?
# =====================================

def first_post(post):

    return post == 1


# =====================================
# Last Post?
# =====================================

def last_post(post):

    return post >= TOTAL_POSTS


# =====================================
# First Call?
# =====================================

def first_call(call):

    return call == 1


# =====================================
# Last Call?
# =====================================

def last_call(call):

    return call >= CALLS_PER_POST


# =====================================
# Next Call
# =====================================

def next_call(post, call):

    if call < CALLS_PER_POST:

        return (

            post,

            call + 1

        )

    if post < TOTAL_POSTS:

        return (

            post + 1,

            1

        )

    return (

        TOTAL_POSTS,

        CALLS_PER_POST

    )


# =====================================
# Previous Call
# =====================================

def previous_call(post, call):

    if call > 1:

        return (

            post,

            call - 1

        )

    if post > 1:

        return (

            post - 1,

            CALLS_PER_POST

        )

    return (

        1,

        1

    )


# =====================================
# Match Finished?
# =====================================

def match_finished(

        post,

        call

):

    return (

        post >= TOTAL_POSTS

        and

        call >= CALLS_PER_POST

    )


# =====================================
# Total Calls Played
# =====================================

def calls_played(

        post,

        call

):

    return (

        (post - 1)

        *

        CALLS_PER_POST

    ) + call


# =====================================
# Remaining Calls
# =====================================

def remaining_calls(

        post,

        call

):

    total = (

        TOTAL_POSTS

        *

        CALLS_PER_POST

    )

    return total - calls_played(

        post,

        call

    )


# =====================================
# Match Progress
# =====================================

def match_progress(

        post,

        call

):

    total = (

        TOTAL_POSTS

        *

        CALLS_PER_POST

    )

    played = calls_played(

        post,

        call

    )

    return round(

        played * 100 / total,

        2

    )


# =====================================
# Overall Ranking
# =====================================

def overall_ranking(

        total_score

):

    return sorted(

        total_score.items(),

        key=lambda x: x[1],

        reverse=True

    )


# =====================================
# Match Winner
# =====================================

def match_winner(

        total_score

):

    return overall_ranking(

        total_score

    )[0]


# =====================================
# Runner Up
# =====================================

def match_runner(

        total_score

):

    return overall_ranking(

        total_score

    )[1]


# =====================================
# Third Place
# =====================================

def match_third(

        total_score

):

    return overall_ranking(

        total_score

    )[2]


# =====================================
# Crown Player
# =====================================

def crown_player(

        total_score

):

    winner = match_winner(

        total_score

    )

    return {

        "Player": winner[0],

        "Score": winner[1],

        "Icon": "👑"

    }


# =====================================
# Match Summary
# =====================================

def match_summary(

        post,

        call,

        total_score

):

    return {

        "Post": post,

        "Call": call,

        "Progress":

            match_progress(

                post,

                call

            ),

        "Remaining":

            remaining_calls(

                post,

                call

            ),

        "Winner":

            crown_player(

                total_score

            )

    }
#------------Part 8a -------#

