from category import (
    is_higher,
    is_lower
)
from tie import split_points


def determine(
        values,
        point,
        category
):

    if is_higher(category):
        best = max(
            values.values()
        )
    else:
        best = min(
            values.values()
        )

    winners = []

    for p, v in values.items():

        if v == best:
            winners.append(p)

    return split_points(
        point,
        winners
    )
