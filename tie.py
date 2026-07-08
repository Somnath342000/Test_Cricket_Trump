def split_points(points, winners):

    result = {}

    each = points / len(winners)

    for p in winners:
        result[p] = each

    return result


def ranking(values):

    data = sorted(
        values.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return data
