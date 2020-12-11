import copy
import sys


def step(state):
    new_state = copy.deepcopy(state)
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == '.':
                continue
            occ = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (row + i >= 0 and row + i < len(state) and
                        col + j >= 0 and col + j < len(state[row])):
                        if state[row + i][col + j] == '#':
                            occ += 1
            if occ == 0 and state[row][col] == 'L':
                new_state[row][col] = '#'
            elif occ >= 4 and state[row][col] == '#':
                new_state[row][col] = 'L'
    return new_state


def step_pt2(state):
    new_state = copy.deepcopy(state)
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == '.':
                continue
            occ = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    k = 1
                    while (row + i * k >= 0 and row + i * k < len(state) and
                        col + j * k >= 0 and col + j * k < len(state[row])):
                        if state[row + i * k][col + j * k] == '#':
                            occ += 1
                            break
                        elif state[row + i * k][col + j * k] == 'L':
                            break
                        k += 1
            if occ == 0 and state[row][col] == 'L':
                new_state[row][col] = '#'
            elif occ >= 5 and state[row][col] == '#':
                new_state[row][col] = 'L'
    return new_state


def iterate(init, f):
    state = init
    new_state = f(state)
    while state != new_state:
        state = new_state
        new_state = f(state)
    return sum([r.count('#') for r in state])


def main(argv):
    with open(argv[1]) as f:
        lines = [[c for c in x.rstrip()] for x in f]
        print(iterate(lines, step))
        print(iterate(lines, step_pt2))


if __name__ == "__main__":
    main(sys.argv)

