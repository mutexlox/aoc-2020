import collections
import itertools
import sys

def get_neighbors(*args):
    for deltas in itertools.product(range(-1, 2), repeat=len(args)):
        if all(d == 0 for d in deltas):
            continue
        yield tuple(args[i] + deltas[i] for i in range(len(args)))

def step(state):
    new_state = set()
    neighbors = collections.defaultdict(int)
    for coords in state:
        count = 0
        for neighbor_coord in get_neighbors(*coords):
            if neighbor_coord in state:
                count += 1
            else:
                neighbors[neighbor_coord] += 1
        if count in (2, 3):
            new_state.add(coords)

    for coords in neighbors:
        if neighbors[coords] == 3:
            new_state.add(coords)

    return new_state

def nsteps(init, steps, dim):
    state = set()
    for x in range(len(init)):
        for y in range(len(init[x])):
            coord = [x, y]
            coord.extend(0 for _ in range(dim - 2))
            if init[x][y] == '#':
                state.add(tuple(coord))
    for i in range(steps):
        state = step(state)
    return len(state)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(nsteps(lines, 6, 3))
        print(nsteps(lines, 6, 4))

if __name__ == "__main__":
    main(sys.argv)

