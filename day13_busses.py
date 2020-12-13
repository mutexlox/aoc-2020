import functools
import sys


def earliest_bus_id(depart, busses):
    earliest = None
    for b in busses:
        if b == 'x':
            continue
        b = int(b)
        next_time = (depart // b) * b
        if next_time < depart:
            next_time += b
        if earliest is None or earliest[0] > next_time:
            earliest = next_time, b
    return earliest[1] * (earliest[0] - depart)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def constraint_solve(constraints):
    int_cons = [(int(constraints[i]), i) for i in range(len(constraints))
                if constraints[i] != 'x']
    prod = functools.reduce(lambda x,y: x*y, (x[0] for x in int_cons), 1)
    ys = [prod // x[0] for x in int_cons]
    invs = [modinv(ys[i], int_cons[i][0]) for i in range(len(ys))]
    s = 0
    for i in range(len(ys)):
        s += (int_cons[i][0]-int_cons[i][1]) * ys[i] * invs[i]
    return s % prod

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        depart = int(lines[0])
        busses = lines[1].split(',')
        print(earliest_bus_id(depart, busses))
        print(constraint_solve(busses))


if __name__ == "__main__":
    main(sys.argv)
