import itertools
import sys

def get_neighbors(*args):
    for deltas in itertools.product(range(-1, 2), repeat=len(args)):
        if all(d == 0 for d in deltas):
            continue
        yield tuple(args[i] + deltas[i] for i in range(len(args)))

def step(state, bounds):
    new_state = state.copy()
    iters = [range(b[0] - 1, b[1] + 2) for b in bounds]
    for coords in itertools.product(*iters):
        coords = tuple(coords)
        count = 0
        for neighbor_coord in get_neighbors(*coords):
            try:
                if neighbor_coord in state:
                    count += 1
            except KeyError:
                pass
        if coords in state and count not in (2, 3):
            new_state.remove(coords)
        elif coords not in state and count == 3:
            new_state.add(coords)
            # Update bounding box
            for i in range(len(coords)):
                if coords[i] < bounds[i][0]:
                    bounds[i] = (coords[i], bounds[i][1])
                elif coords[i] > bounds[i][1]:
                    bounds[i] = (bounds[i][0], coords[i])

    return new_state, bounds

def nsteps(init, steps, dim):
    state = set()
    for x in range(len(init)):
        for y in range(len(init[x])):
            coord = [x, y]
            coord.extend(0 for _ in range(dim - 2))
            if init[x][y] == '#':
                state.add(tuple(coord))
    bounds = [(0, len(init)), (0, len(init[0]))]
    bounds.extend((0, 1) for _ in range(dim - 2))
    for i in range(steps):
        state, bounds = step(state, bounds)
    return len(state)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(nsteps(lines, 6, 3))
        print(nsteps(lines, 6, 4))

if __name__ == "__main__":
    main(sys.argv)

