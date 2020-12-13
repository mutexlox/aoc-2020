import collections
import copy
import sys

SCRATCH = None

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
                while (row + i * k >= 0 and row + i * k < len(state) and
                    col + j * k >= 0 and col + j * k < len(state[row])):
                    if state[row + i * k][col + j * k] != '.':
                        VISIBLE_SEATS[(row,col)].append((row + i * k, col + j * k))
                        break
                    if not keep_going:
                        break
                    k += 1
    return VISIBLE_SEATS[(row, col)]


def step(state, keep_going, max_num_occ):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == '.':
                continue
            occ = 0
            for new_i, new_j in get_visible(state, row, col, keep_going):
                if state[new_i][new_j] == '#':
                    occ += 1
            if occ == 0 and state[row][col] == 'L':
                SCRATCH[row][col] = '#'
            elif occ >= max_num_occ and state[row][col] == '#':
                SCRATCH[row][col] = 'L'


def iterate(init, keep_going, max_num_occ):
    global VISIBLE_SEATS
    VISIBLE_SEATS = collections.defaultdict(list)

    state = init
    copy_state(state, SCRATCH)
    step(state, keep_going, max_num_occ)
    while state != SCRATCH:
        copy_state(SCRATCH, state)
        step(state, keep_going, max_num_occ)
    return sum([r.count('#') for r in state])


def main(argv):
    global SCRATCH
    with open(argv[1]) as f:
        lines = [[c for c in x.rstrip()] for x in f]
        SCRATCH = copy.deepcopy(lines)
        state = copy.deepcopy(lines)
        print(iterate(state, False, 4))
        print(iterate(lines, True, 5))


if __name__ == "__main__":
    main(sys.argv)

