import sys

def count_valid_pt1(lines):
    valid = 0
    for l in lines:
        parts = l.split()
        lo, hi = parts[0].split('-')
        cnt = parts[2].count(parts[1][:-1])
        if cnt >= int(lo) and cnt <= int(hi):
            valid += 1
    return valid

def count_valid_pt2(lines):
    valid = 0
    for l in lines:
        parts = l.split()
        lo, hi = parts[0].split('-')
        lo, hi = int(lo), int(hi)
        want = parts[1][:-1]
        if (parts[2][lo - 1] == want) != (parts[2][hi - 1] == want):
            valid += 1
    return valid

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(count_valid_pt1(lines))
        print(count_valid_pt2(lines))

if __name__ == "__main__":
    main(sys.argv)
