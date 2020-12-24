import collections
import itertools
import sys

def canonicalize(line):
    dirs = []
    i = 0
    while i < len(line):
        if line[i] in ('e', 'w'):
            dirs.append(line[i])
            i += 1
        else:
            assert( line[i + 1] in ('e', 'w'))
            dirs.append(line[i:i + 2])
            i += 2

    x_dir = 0
    y_dir = 0
    z_dir = 0
    for d in dirs:
        if d == 'w':
            x_dir -= 1
            z_dir += 1
        elif d == 'e':
            x_dir += 1
            z_dir -= 1
        elif d == 'nw':
            y_dir -= 1
            z_dir += 1
        elif d == 'ne':
            x_dir += 1
            y_dir -= 1
        elif d == 'sw':
            x_dir -= 1
            y_dir += 1
        elif d == 'se':
            y_dir += 1
            z_dir -= 1
    return (x_dir, y_dir, z_dir)

def count_odd_flips(lines):
    state = set()
    for l in lines:
        canon = canonicalize(l)
        if canon in state:
            state.remove(canon)
        else:
            state.add(canon)
    return state, len(state)

def neighbor_coords(*args):
    for deltas in ((0, 1, -1), (1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0)):
        yield tuple(args[i] + deltas[i] for i in range(len(args)))

def step(state):
    neighbor_counts = collections.defaultdict(int)
    new_state = set()
    for t in state:
        count = 0
        for n in neighbor_coords(*t):
            if n in state:
                count += 1
            else:
                neighbor_counts[n] += 1
        if 0 < count and count <= 2:
            new_state.add(t)
    for n, c in neighbor_counts.items():
        if c == 2:
            new_state.add(n)
    return new_state

def do_steps(state, steps):
    for i in range(steps):
        state = step(state)
    return len(state)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        state, count = count_odd_flips(lines)
        print(count)
        print(do_steps(state, 100))

if __name__ == "__main__":
    main(sys.argv)
