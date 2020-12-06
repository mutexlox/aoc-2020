import sys

def count_yesses(lines):
    group = []
    group_size = 0

    count = 0
    count_all_yes = 0

    for l in lines:
        if not l:
            s = set(group)
            count += len(s)
            for c in s:
                if group.count(c) == group_size:
                    count_all_yes += 1
            group = []
            group_size = 0
        else:
            group.extend(l)
            group_size += 1

    return count, count_all_yes


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        lines.append('')
        print(count_yesses(lines))


if __name__ == "__main__":
    main(sys.argv)
