import sys

def bsearch(spec, lo, hi, take_lo, take_hi):
    for c in spec:
        mid = (lo + hi) // 2
        if c == take_lo:
            hi = mid
        elif c == take_hi:
            lo = mid
    assert(lo + 1 == hi)
    return lo

def get_row(seat_spec):
    return bsearch(seat_spec[:7], 0, 128, 'F', 'B')

def get_col(seat_spec):
    return bsearch(seat_spec[7:], 0, 8, 'L', 'R')

def get_seat_id(seat_spec):
    return 8 * get_row(seat_spec) + get_col(seat_spec)

def get_missing_seat_id(specs):
    l = sorted(get_seat_id(s) for s in specs)
    for i in range(len(l) - 1):
        if l[i] + 2 == l[i + 1]:
            return l[i] + 1
    return None

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(max(get_seat_id(l) for l in lines))
        print(get_missing_seat_id(lines))


if __name__ == "__main__":
    main(sys.argv)
