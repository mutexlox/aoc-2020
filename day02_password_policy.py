import sys

def validate_pt1(lo, hi, char, pw):
    cnt = pw.count(char)
    return cnt >= lo and cnt <= hi

def validate_pt2(lo, hi, char, pw):
    return (pw[lo - 1] == char) != (pw[hi - 1] == char)


def count_valid(lines, fn):
    valid = 0
    for l in lines:
        parts = l.split()
        lo, hi = parts[0].split('-')
        if fn(int(lo), int(hi), parts[1][:-1], parts[2]):
            valid += 1
    return valid

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(count_valid(lines, validate_pt1))
        print(count_valid(lines, validate_pt2))

if __name__ == "__main__":
    main(sys.argv)
