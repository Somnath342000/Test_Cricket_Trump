# ==========================
# Total Constants
# ==========================
TOTAL_POSTS = 12
TOTAL_CALLS = 18
TOTAL_CYCLES = 4


# ==========================
# Next Call
# ==========================
def next_call(call_no):

    call_no = int(call_no)

    if call_no >= TOTAL_CALLS:
        return None

    return call_no + 1


# ==========================
# Previous Call
# ==========================
def previous_call(call_no):

    call_no = int(call_no)

    if call_no <= 1:
        return None

    return call_no - 1


# ==========================
# Next Post
# ==========================
def next_post(post_no):

    post_no = int(post_no)

    if post_no >= TOTAL_POSTS:
        return None

    return post_no + 1


# ==========================
# Previous Post
# ==========================
def previous_post(post_no):

    post_no = int(post_no)

    if post_no <= 1:
        return None

    return post_no - 1


# ==========================
# Is Last Call?
# ==========================
def is_last_call(call_no):

    return int(call_no) == TOTAL_CALLS


# ==========================
# Is Last Post?
# ==========================
def is_last_post(post_no):

    return int(post_no) == TOTAL_POSTS


# ==========================
# Get Cycle
# ==========================
def get_cycle(post_no):

    post_no = int(post_no)

    if post_no <= 3:
        return 1

    if post_no <= 6:
        return 2

    if post_no <= 9:
        return 3

    return 4


# ==========================
# Posts Remaining
# ==========================
def posts_remaining(post_no):

    return TOTAL_POSTS - int(post_no)


# ==========================
# Calls Remaining
# ==========================
def calls_remaining(call_no):

    return TOTAL_CALLS - int(call_no)


# ==========================
# Match Finished?
# ==========================
def match_finished(
        post_no,
        call_no
):

    return (
        int(post_no) == TOTAL_POSTS and
        int(call_no) == TOTAL_CALLS
    )


# ==========================
# Advance State
# ==========================
def advance(
        post_no,
        call_no
):

    post_no = int(post_no)
    call_no = int(call_no)

    if call_no < TOTAL_CALLS:
        return post_no, call_no + 1

    if post_no < TOTAL_POSTS:
        return post_no + 1, 1

    return None, None
