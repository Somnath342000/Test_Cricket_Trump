from score import result

def distribute(match_id):

    s = result(match_id)

    p1,n1 = s[0][1],s[0][0]
    p2,n2 = s[1][1],s[1][0]
    p3,n3 = s[2][1],s[2][0]

    # CASE 8
    if p1==p2==p3:
        return {
            n1:3,
            n2:3,
            n3:3
        }

    # CASE 5
    if p1==p2:
        return {
            n1:4,
            n2:4,
            n3:1
        }

    # CASE 6
    if p2==p3 and p1-p2<=3:
        return {
            n1:5,
            n2:2,
            n3:2
        }

    # CASE 7
    if p2==p3 and p1-p2>=9:
        return {
            n1:7,
            n2:1,
            n3:1
        }

    gap=p1-p2

    # CASE 1
    if gap<=2:
        return {
            n1:5,
            n2:4,
            n3:0
        }

    # CASE 2
    if gap<9:
        return {
            n1:6,
            n2:3,
            n3:0
        }

    # CASE 4
    if gap>=18:
        return {
            n1:8,
            n2:1,
            n3:0
        }

    # CASE 3
    return {
        n1:7,
        n2:2,
        n3:0
    }
