# tie.py

def split_points(points, winners):
"""
Example:
6 points, 2 winners
-> {'Som': 3, 'Joy': 3}
"""

```
if not winners:
    return {}

each = points / len(winners)

result = {}

for p in winners:
    result[p] = each

return result
```

def ranking(values):
"""
values example:
{
"Som": 5,
"Joy": 3,
"Krish": 3
}

```
return:
[
    ('Som',5),
    ('Joy',3),
    ('Krish',3)
]
"""

return sorted(
    values.items(),
    key=lambda x: x[1],
    reverse=True
)
```

def winners(values, higher=True):
"""
values:
{
"Som": 100,
"Joy": 90,
"Krish": 90
}

```
return:
['Som']
"""

if not values:
    return []

if higher:
    best = max(values.values())
else:
    best = min(values.values())

return [
    p
    for p, v in values.items()
    if v == best
]
```

def is_tie(values, higher=True):
"""
Returns True if first position tied.
"""

```
return len(
    winners(values, higher)
) > 1
```

def second_place(values, higher=True):
"""
Returns second rank players.
Useful for distribution engine.
"""

```
if len(values) <= 1:
    return []

vals = list(values.values())

if higher:
    ordered = sorted(
        set(vals),
        reverse=True
    )
else:
    ordered = sorted(
        set(vals)
    )

if len(ordered) < 2:
    return []

second = ordered[1]

return [
    p
    for p, v in values.items()
    if v == second
]
```

def third_place(values, higher=True):
"""
Returns third rank players.
"""

```
vals = list(values.values())

if higher:
    ordered = sorted(
        set(vals),
        reverse=True
    )
else:
    ordered = sorted(
        set(vals)
    )

if len(ordered) < 3:
    return []

third = ordered[2]

return [
    p
    for p, v in values.items()
    if v == third
]
```

def rank_number(values, player, higher=True):
"""
Example:

```
values:
{
    'Som':10,
    'Joy':10,
    'Krish':5
}

Som -> 1
Joy -> 1
Krish -> 2
"""

vals = list(values.values())

if higher:
    ordered = sorted(
        set(vals),
        reverse=True
    )
else:
    ordered = sorted(
        set(vals)
    )

player_value = values[player]

return (
    ordered.index(player_value)
    \+ 1
)
```
