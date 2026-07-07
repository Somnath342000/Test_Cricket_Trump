from sheet import get_sheet

def add_score(match_id, player, point):

    ws = get_sheet("Scores")

    rows = ws.get_all_values()

    for i, r in enumerate(rows[1:], start=2):

        if r[0]==match_id and r[1]==player:

            total=int(r[2])+point

            ws.update(f"C{i}", total)

            return

    ws.append_row([match_id, player, point])


def result(match_id):

    ws=get_sheet("Scores")

    rows=ws.get_all_values()

    score=[]

    for r in rows[1:]:

        if r[0]==match_id:

            score.append((r[1],int(r[2])))

    score.sort(key=lambda x:x[1],reverse=True)

    return score
