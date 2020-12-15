import sys


def get_nth(start, n):
    last = {}
    for i in range(len(start) - 1):
        last[start[i]] = i + 1

    prev = start[-1]
    for i in range(len(start), n):
        old_prev = prev
        if prev not in last:
            prev = 0
        else:
            prev = i - last[prev]
        last[old_prev] = i

    return prev


def main(argv):
    lines = [0,5,4,1,10,14,7]
    print(get_nth(lines, 2020))
    print(get_nth(lines, 30000000))


if __name__ == "__main__":
    main(sys.argv)
