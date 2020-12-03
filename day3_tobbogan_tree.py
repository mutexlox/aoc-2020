import sys

def count_trees(lines, xdel=1, ydel=3, x=0, y=0):
    if x >= len(lines):
        return 0
    count = 0
    if lines[x][y] == '#':
        count += 1
    return count + count_trees(lines, xdel, ydel, x + xdel, (y + ydel) % len(lines[0]))

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(count_trees(lines, xdel=1, ydel=3))

        m1 = count_trees(lines, xdel=1, ydel=1)
        m2 = count_trees(lines, xdel=1, ydel=3)
        m3 = count_trees(lines, xdel=1, ydel=5)
        m4 = count_trees(lines, xdel=1, ydel=7)
        m5 = count_trees(lines, xdel=2, ydel=1)
        print(m1*m2*m3*m4*m5)


if __name__ == "__main__":
    main(sys.argv)
