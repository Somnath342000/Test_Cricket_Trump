import random
import streamlit as st
from sheet import (
save_toss,
get_toss
)

PLAYERS = [
"Som",
"Joy",
"Krish"
]

# =====================================

# Snake Draft Order

# =====================================

def snake(order):

```
return [
    order[0],
    order[1],
    order[2],
    order[2],
    order[1],
    order[0]
]
```

# =====================================

# Batting Toss

# =====================================

def batting_toss(match_id):

```
toss = get_toss(match_id)

if (
    toss and
    len(toss["BatDraft"]) == 3
):
    return toss["BatDraft"]

order = random.sample(
    PLAYERS,
    3
)

bowl = []

if toss:
    bowl = toss["BowlDraft"]

save_toss(
    match_id,
    order,
    bowl
)

return order
```

# =====================================

# Bowling Toss

# =====================================

def bowling_toss(match_id):

```
toss = get_toss(match_id)

if (
    toss and
    len(toss["BowlDraft"]) == 3
):
    return toss["BowlDraft"]

order = random.sample(
    PLAYERS,
    3
)

bat = []

if toss:
    bat = toss["BatDraft"]

save_toss(
    match_id,
    bat,
    order
)

return order
```

# =====================================

# Show Toss Result

# =====================================

def show_toss(
title,
order
):

```
st.subheader(title)

st.write(
    f"🥇 1st : {order[0]}"
)

st.write(
    f"🥈 2nd : {order[1]}"
)

st.write(
    f"🥉 3rd : {order[2]}"
)

st.divider()

draft = snake(order)

st.write(
    "### Snake Draft Order"
)

for i, p in enumerate(
        draft,
        start=1
):

    st.write(
        f"Pick {i} : {p}"
    )
```

# =====================================

# Current Turn

# =====================================

def current_turn(
order,
pick_no
):

```
draft = snake(order)

if pick_no < 1:
    return None

if pick_no > 6:
    return None

return draft[pick_no - 1]
```

# =====================================

# Check Turn

# =====================================

def can_pick(
player,
order,
pick_no
):

```
turn = current_turn(
    order,
    pick_no
)

return player == turn
```

# =====================================

# Get Pick Number

# =====================================

def next_pick(order, picked):

```
draft = snake(order)

if picked >= len(draft):
    return None

return draft[picked]
```

# =====================================

# Draft Finished?

# =====================================

def draft_finished(picked):

```
return picked >= 6
```
