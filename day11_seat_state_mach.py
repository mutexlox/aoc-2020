import collections
import copy
import sys

SCRATCH = None
ROWS = 0
COLS = 0

def copy_state(src, dest):
    for i in range(len(src)):
        for j in range(len(src[i])):
            dest[i][j] = src[i][j]


VISIBLE_SEATS = collections.defaultdict(list)
def get_visible(state, row, col, keep_going):
    if (row, col) not in VISIBLE_SEATS:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                k = 1
                while (row + i * k >= 0 and row + i * k < ROWS and
                    col + j * k >= 0 and col + j * k < COLS):
                    if state[row + i * k][col + j * k] != '.':
                        VISIBLE_SEATS[(row,col)].append((row + i * k, col + j * k))
                        break
                    if not keep_going:
                        break
                    k += 1
    return VISIBLE_SEATS[(row, col)]


def step(state):
    for row in range(ROWS):
        for col in range(COLS):
            if state[row][col] == '.':
                continue
            occ = 0
            for new_i, new_j in get_visible(state, row, col, False):
                if state[new_i][new_j] == '#':
                    occ += 1
            if occ == 0 and state[row][col] == 'L':
                SCRATCH[row][col] = '#'
            elif occ >= 4 and state[row][col] == '#':
                SCRATCH[row][col] = 'L'


def step_pt2(state):
    for row in range(ROWS):
        for col in range(COLS):
            if state[row][col] == '.':
                continue
            occ = 0
            for new_i, new_j in get_visible(state, row, col, True):
                if state[new_i][new_j] == '#':
                    occ += 1
            if occ == 0 and state[row][col] == 'L':
                SCRATCH[row][col] = '#'
            elif occ >= 5 and state[row][col] == '#':
                SCRATCH[row][col] = 'L'


def iterate(init, f):
    global VISIBLE_SEATS
    state = init
    VISIBLE_SEATS = collections.defaultdict(list)
    copy_state(state, SCRATCH)
    f(state)
    while state != SCRATCH:
        copy_state(SCRATCH, state)
        f(state)
    return sum([r.count('#') for r in state])


def main(argv):
    global SCRATCH, ROWS, COLS
    with open(argv[1]) as f:
        lines = [[c for c in x.rstrip()] for x in f]
        ROWS = len(lines)
        COLS = len(lines[0])
        SCRATCH = copy.deepcopy(lines)
        state = copy.deepcopy(lines)
        print(iterate(state, step))
        print(iterate(lines, step_pt2))


if __name__ == "__main__":
    main(sys.argv)

