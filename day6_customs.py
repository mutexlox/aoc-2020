import sys

def count_yesses(lines):
    group = []
    count = 0
    for l in lines:
        if not l:
            s = set(group)
            count += len(s)
            group = []
        else:
            group.extend(l)

    return count

def count_all_yesses(lines):
    group = []
    group_size = 0
    count = 0
    for l in lines:
        if not l:
            for c in set(group):
                if group.count(c) == group_size:
                    count += 1
            group = []
            group_size = 0
        else:
            group.extend(l)
            group_size += 1

    return count


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        lines.append('')
        print(count_yesses(lines))
        print(count_all_yesses(lines))


if __name__ == "__main__":
    main(sys.argv)
