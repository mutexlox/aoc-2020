import collections
import sys

def step(d1, d2):
    c1 = d1.pop(0)
    c2 = d2.pop(0)
    if c1 < c2:
        d2.append(c2)
        d2.append(c1)
    elif c1 > c2:
        d1.append(c1)
        d1.append(c2)

def run_game(d1, d2):
    while len(d1) and len(d2):
        step(d1, d2)
    return get_score(d1, d2)

def get_score(d1, d2):
    winner = reversed(d1 + d2)
    score = 0
    mul = 1
    for c in winner:
        score += mul * c
        mul += 1
    return score

def round_recursive(visited, d1, d2):
    if (tuple(d1), tuple(d2)) in visited:
        return -1
    visited.add((tuple(d1), tuple(d2)))
    c1 = d1.pop(0)
    c2 = d2.pop(0)
    if c1 <= len(d1) and c2 <= len(d2):
        res = get_winner(d1.copy()[:c1], d2.copy()[:c2])
        if res == -1:
            res = 1
    elif c1 > c2:
        res = 1
    elif c2 > c1:
        res = 2
    else:
        print(c1, c2)
        assert(False)

    if res == 1:
        d1.append(c1)
        d1.append(c2)
    else:
        d2.append(c2)
        d2.append(c1)
    return res

def get_winner(d1, d2):
    visited = set()
    while len(d1) and len(d2):
        res = round_recursive(visited, d1, d2)
        if res == -1:
            d2 = []
            break
    return res

def run_pt2(d1, d2):
    res = get_winner(d1, d2)
    return get_score(d1, d2)

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        d1 = []
        i = 1
        while lines[i]:
            d1.append(int(lines[i]))
            i += 1
        i += 2
        d2 = []
        while i < len(lines):
            d2.append(int(lines[i]))
            i += 1
        print(run_game(d1[:], d2[:]))
        print(run_pt2(d1, d2))

if __name__ == "__main__":
    main(sys.argv)


